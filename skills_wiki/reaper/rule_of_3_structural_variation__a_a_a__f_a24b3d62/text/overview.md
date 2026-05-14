### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Structural Variation (A-A-A' Form)

* **Core Musical Mechanism**: The "Rule of 3" is a structural and compositional pacing technique. A musical idea (like a 4-bar chord progression and melody) is presented once to introduce it, repeated a second time to reinforce and establish familiarity, and altered on the third repetition to subvert expectation. This typically takes the form of an A-A-A' structure, where the third repetition starts identically to the first two but diverts to a new chord progression or melodic tail halfway through.
* **Why Use This Skill (Rationale)**: This technique exploits human psychoacoustics and cognitive processing. The brain naturally seeks patterns. The first listen introduces the pattern. The second listen confirms it, providing a dopamine hit of predictability. By the third listen, the brain categorizes the information as "known" and begins to tune it out. By introducing a variation precisely at this moment, the composer forces the brain to re-engage with the music. 
* **Overall Applicability**: This is a universal compositional tool applicable to almost any genre. It works exceptionally well for 4-bar drop progressions in EDM, 2-bar drum loops in Hip-Hop (adding a fill on the 3rd repetition), or 8-bar verse melodies in Pop music. 
* **Value Addition**: Compared to a looped MIDI clip, this skill encodes active structural pacing. It prevents a composition from feeling overly repetitive by dynamically generating variations at the exact moment the listener's attention begins to wane.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4/4 time signature.
  - **Phrase Length**: A 4-bar musical phrase.
  - **Structure**: The 4-bar phrase is repeated 3 times (12 bars total).
  - **Rhythmic Motif**: A steady quarter-note melodic rhythm over whole-note chords, establishing a highly predictable pattern that makes the eventual variation more impactful.

* **Step B: Pitch & Harmony**
  - **Repetitions 1 & 2 (The "A" Section)**: Uses a standard, highly recognizable pop progression: **I - V - vi - IV**.
  - **Repetition 3 (The "A'" Variation)**: Starts the same but changes the ending to build tension: **I - V - ii - V**. 
  - **Melodic Variation**: The melody arpeggiates the underlying chords. On the final bar of the 3rd repetition, the melody steps upward to create a leading-tone tension that begs for a resolution.

* **Step C: Sound Design & FX**
  - **Instrument**: A basic ReaSynth is loaded as a placeholder to make the structural timing immediately audible. 

* **Step D: Mix & Automation**
  - **Velocities**: The underlying chord pad is played at a slightly lower velocity (70% of base) compared to the lead melody to ensure harmonic clarity without muddying the transient of the lead line.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| A-A-A' Structural Loop | Procedural MIDI Generation | Allows conditional logic (`if iteration == 3`) to dynamically alter notes and chords inside a single cohesive MIDI item. |
| Harmonic Math | Scale Degree Array Mapping | Enables the pattern to be transposed to any Key or Scale while maintaining correct diatonic triad structures. |
| Sound Source | `ReaSynth` FX | Guarantees the structural variation can be heard immediately in a stock REAPER session without external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The tutorial focuses purely on the theoretical structure of arrangement and composition ("how many times to repeat an idea"), which maps perfectly to deterministic Python control flow. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 (A-A-A')",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, 
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar progression demonstrating the 'Rule of 3' variation technique.
    It generates a 4-bar phrase, loops it exactly once, and on the 3rd iteration, 
    alters the second half to keep the listener engaged.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (overridden to 12 internally to ensure the 3-part structure fits).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Extract scale details
    root_midi = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)
    
    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Step 2: Create Track (Additive)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a stock synth so the chords are immediately audible
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # Step 3: Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    
    # We enforce exactly 12 bars to properly demonstrate the 3-iteration structure (3 x 4 bars)
    total_bars = 12
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to compute specific MIDI notes diatonically
    def get_note(degree: int, base_octave: int = 4) -> int:
        octave_shift = degree // scale_len
        note = (base_octave * 12) + root_midi + scale_intervals[degree % scale_len] + (12 * octave_shift)
        return int(max(0, min(127, note)))

    # Step 4: Generate the A - A - A' structure
    for bar in range(total_bars):
        iter_num = bar // 4       # Iteration 0, 1, or 2
        bar_in_phrase = bar % 4   # Bar 0, 1, 2, or 3 within the current iteration
        
        # --- APPLYING THE RULE OF 3 ---
        if iter_num < 2:
            # Iteration 1 & 2: Introduce and establish the standard progression (I, V, vi, IV)
            progression = [0, 4, 5, 3] 
        else:
            # Iteration 3: Subvert expectation! Start the same, but end on a turnaround (I, V, ii, V)
            progression = [0, 4, 1, 4]
            
        chord_root_deg = progression[bar_in_phrase]
        bar_start_sec = bar * bar_length_sec
        
        # Calculate time boundaries for the chord (whole note pad)
        chord_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_sec)
        chord_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_sec + bar_length_sec * 0.95)
        
        # Insert Chord (Diatonic Triad, Base Octave 4)
        pad_vel = int(velocity_base * 0.7)
        for offset in [0, 2, 4]:
            note = get_note(chord_root_deg + offset, base_octave=4)
            RPR.RPR_MIDI_InsertNote(take, False, False, chord_start_ppq, chord_end_ppq, 0, note, pad_vel, False)
            
        # Insert Melody (Arpeggiated motif over the chords, Base Octave 5)
        # Standard Motif: play the root, 3rd, 5th, 3rd of the current underlying chord
        melody_offsets = [0, 2, 4, 2]
        
        # Subvert expectation on the very last bar of the 3rd iteration
        if iter_num == 2 and bar_in_phrase == 3:
            # Step upwards at the end of the phrase to create unresolved tension 
            # leading perfectly into a next song section
            melody_offsets = [0, 2, 4, 5] 
            
        for i, offset in enumerate(melody_offsets):
            note = get_note(chord_root_deg + offset, base_octave=5)
            m_start_sec = bar_start_sec + i * (bar_length_sec / 4.0)
            m_end_sec = m_start_sec + (bar_length_sec / 4.0) * 0.8  # slightly detached
            
            m_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, m_start_sec)
            m_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, m_end_sec)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, m_start_ppq, m_end_ppq, 0, note, velocity_base, False)

    # Sort MIDI events to ensure valid REAPER processing
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' demonstrating the 'Rule of 3' (A-A-A') over {total_bars} bars at {bpm} BPM in {key} {scale}"
```