### 1. High-level Design Pattern Extraction

> **Skill Name**: Structural Phrasing: The "Rule of Three" (ABAC/AAB Form)

* **Core Musical Mechanism**: Managing repetition and listener expectation. The pattern establishes a musical idea (iteration 1), reinforces it (iteration 2), and then intentionally breaks the pattern (iteration 3) to prevent the listener's brain from tuning it out. 
* **Why Use This Skill (Rationale)**: Human brains are pattern-recognition machines. One instance is an anomaly, two establish a pattern, and three of the exact same thing causes the brain to "habituate" and stop paying attention ("too much of a good thing"). By altering the third repetition (either entirely or halfway through), you reward the listener's attention with novelty while maintaining thematic cohesion.
* **Overall Applicability**: This applies universally across genres to chord progressions, melodies, drum loops, basslines, and arrangement sections. It is the core difference between a static "4-bar loop" beat and a dynamic, evolving song structure.
* **Value Addition**: Compared to looping a MIDI clip infinitely, this skill encodes structural music theory. It generates a dynamic 12-bar macro-phrase where the final 4 bars pivot into a rhythmic and harmonic variation, automatically resolving the tension introduced by repetition.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Feel**: 4/4 time signature.
  - **Macro-Structure**: A 4-bar phrase repeated in a 12-bar sequence.
  - **Note Duration**: The base melody uses steady quarter notes (reinforcing stability), while the variation introduces staccato 8th notes to increase rhythmic density and signal structural change.

* **Step B: Pitch & Harmony**
  - Demonstrates the tutorial's "Option 2" (Start the same, go somewhere different halfway through).
  - **Base Progression** (Bars 1-4, 5-8): I - V - vi - IV (Establishing the pattern).
  - **Variation Progression** (Bars 9-12): I - V - ii - V (Breaking the pattern).
  - The melody arpeggiates the chords for stability, then breaks out into a descending scale run during the variation.

* **Step C: Sound Design & FX**
  - A stock instance of `ReaSynth` is used to clearly demonstrate the chordal and melodic structural changes without timbral distraction. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord & Melody Generation | MIDI note insertion | Allows algorithmic control over pitch and rhythmic density to explicitly build the 12-bar variation structure. |
| Structural Timing | `RPR_MIDI_GetPPQPosFromProjTime` | Ensures the mathematical 4-bar and 12-bar structures remain perfectly synced to the REAPER timeline regardless of BPM. |
| Sound | FX chain (ReaSynth) | Provides an immediate, stock, self-contained audible representation of the harmonic changes. |

> **Feasibility Assessment**: 100% reproducible. The psychological composition technique described in the video is perfectly encoded into an algorithmic 12-bar MIDI generator that automatically creates the "Idea -> Reinforcement -> Variation" structure in any key or scale.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule_Of_3_Demo",
    bpm: int = 120,
    key: str = "F",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar musical progression demonstrating the 'Rule of 3' structure.
    Bars 1-4: Idea established
    Bars 5-8: Idea reinforced
    Bars 9-12: Variation introduced halfway through (Option 2)

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., F, C#, Bb).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars to generate (defaults to 12 to show the full structure).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Normalize inputs
    key = key.capitalize() if key else "C"
    if key not in NOTE_MAP:
        key = "C"
    root_midi = NOTE_MAP[key]
    scale_arr = SCALES.get(scale.lower(), SCALES["major"])

    def get_note_in_scale(root_note, sc_arr, degree, octave):
        """Returns MIDI pitch for a given scale degree (0-indexed)."""
        octave_offset = degree // len(sc_arr)
        scale_idx = degree % len(sc_arr)
        return root_note + (octave + octave_offset) * 12 + sc_arr[scale_idx]

    def get_triad(root_note, sc_arr, root_degree, octave):
        """Returns a 3-note triad built on the specified scale degree."""
        n1 = get_note_in_scale(root_note, sc_arr, root_degree, octave)
        n2 = get_note_in_scale(root_note, sc_arr, root_degree + 2, octave)
        n3 = get_note_in_scale(root_note, sc_arr, root_degree + 4, octave)
        return [n1, n2, n3]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Stock Synth) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper to insert notes using accurate PPQ calculations
    def add_note(pitch, start_sec, end_sec, vel):
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        st_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        en_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, st_ppq, en_ppq, 0, pitch, vel, True)

    # === Step 5: Generate Structure ===
    for i in range(bars):
        phrase_iteration = i // 4
        bar_in_phrase = i % 4
        
        # Rule of 3 Logic: Determine the progression based on phrase iteration
        if phrase_iteration % 3 == 2:
            # 3rd iteration: Variation (starts the same, diverges halfway)
            prog = [0, 4, 1, 4] # I - V - ii - V
            is_variation = True
        else:
            # 1st & 2nd iterations: Base progression
            prog = [0, 4, 5, 3] # I - V - vi - IV
            is_variation = False
            
        chord_degree = prog[bar_in_phrase]
        
        # Generate Chords (Octave 3, soft velocity)
        chord_notes = get_triad(root_midi, scale_arr, chord_degree, 3)
        for pitch in chord_notes:
            add_note(pitch, i * bar_length_sec, (i + 1) * bar_length_sec, velocity_base - 30)
            
        # Generate Melody Base Notes (Octave 5)
        mel_notes = get_triad(root_midi, scale_arr, chord_degree, 5)
        mel_notes.append(get_note_in_scale(root_midi, scale_arr, chord_degree, 6)) # Octave up
        
        qn_length = bar_length_sec / 4
        
        # Introduce melodic and rhythmic novelty during the second half of the variation phrase
        if is_variation and bar_in_phrase >= 2:
            # Rhythmic increase: Descending 8th-note run down the scale
            for j in range(8):
                deg = chord_degree + 7 - j
                pitch = get_note_in_scale(root_midi, scale_arr, deg, 5)
                n_start = i * bar_length_sec + j * (qn_length / 2)
                n_end = n_start + (qn_length / 2) * 0.8 # Staccato articulation
                add_note(pitch, n_start, n_end, velocity_base + 10)
        else:
            # Stability: Steady quarter-note ascending arpeggio
            for j, pitch in enumerate(mel_notes):
                n_start = i * bar_length_sec + j * qn_length
                n_end = n_start + qn_length * 0.9 # Legato articulation
                add_note(pitch, n_start, n_end, velocity_base)

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()
    
    return f"Created '{track_name}' demonstrating Rule of 3 over {bars} bars at {bpm} BPM in {key} {scale}"
```