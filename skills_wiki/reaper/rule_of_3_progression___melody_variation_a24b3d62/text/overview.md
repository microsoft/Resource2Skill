### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Progression & Melody Variation

* **Core Musical Mechanism**: The "Rule of 3" is a psychological and compositional principle. When a listener hears a musical idea (like a chord progression or melody) once, it is introduced. When heard a second time, it is reinforced. If played exactly the same a third time, the brain tunes it out. The core mechanism here is an **A -> A -> B structure**: playing the idea twice to build an expectation, and then deliberately breaking that expectation on the third repetition by introducing a melodic climb and a harmonic variation (a turnaround).
* **Why Use This Skill (Rationale)**: The human brain craves a balance between the familiar and the novel. By adhering to the Rule of 3, you maintain the listener's attention. The familiar repetition anchors them, while the variation triggers a dopamine release by subverting their established expectations.
* **Overall Applicability**: This applies to structural song arrangement (e.g., AAB verse forms), looping beatmaking (4-bar beat looped twice, then a 4-bar fill/bridge), and melodic phrasing.
* **Value Addition**: Compared to a standard looped MIDI clip, this skill encodes tension-and-release mechanics. It dynamically alters the harmony and increases the velocity and pitch contour during the crucial third repetition, forcing the listener to stay engaged.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Time Signature**: 4/4 Time Signature.
  - **Structure**: 12 bars total, composed of three 4-bar phrases. 
  - **Rhythm**: Bass and chords hold for full bars (whole notes), while the melody plucks an 8th-note arpeggio pattern over the top.

* **Step B: Pitch & Harmony**
  - **Phrase 1 & 2 (The Setup)**: Uses a standard Pop/Rock progression: `I - IV - vi - V`.
  - **Phrase 3 (The Variation)**: Starts identically `I - IV` to trick the listener, but then branches off into a `ii - V7` turnaround.
  - **Melodic Contour**: During Phrases 1 and 2, the arpeggio is static and contained within the 5th octave. During the harmonic variation in Phrase 3, the melody begins a climbing crescendo, physically moving up octaves to build kinetic tension leading into the next theoretical section of the song.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` for clear, audible tonal demonstration.
  - **FX Chain**: `ReaVerbate` is added to give the synth physical space and prevent harsh, dry transients.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| AAB Progression Structure | MIDI note insertion | Allows for exact programmatic control over chords, inversions, and scale degrees to demonstrate the variation. |
| Melodic Tension | MIDI Velocity & Pitch Math | Dynamically calculating scale wrapping enables the arpeggio to climb octaves and crescendo during the 3rd repetition. |
| Sound Generation | FX Chain (ReaSynth + ReaVerbate) | Ensures the pattern is immediately audible using self-contained, native REAPER plugins without needing external VSTs or samples. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly implements the exact psychological structure (A->A->B progression/melody variations) described in the tutorial using diatonic math.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule_of_3_Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a musical demonstration of the "Rule of 3" in the current REAPER project.
    Generates three phrases (default 4 bars each, 12 bars total). Phrase 1 and 2 are identical. 
    Phrase 3 introduces harmonic variation and a climbing melodic crescendo to retain listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Length of the base phrase in bars (total generated length is bars * 3).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated sequence.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Helper to calculate precise MIDI pitches based on scale degree
    def get_pitch(degree: int, base_octave: int) -> int:
        root_pitch = NOTE_MAP.get(key, 0)
        octave_offset = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        # +1 because Octave 4 starts at MIDI 60 (Middle C)
        return int(root_pitch + (base_octave + 1 + octave_offset) * 12 + scale_intervals[scale_degree])

    # === Step 1: Initialize Project Temp ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Additive Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add native plugins for immediate auditioning
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    # === Step 3: Math for Time and Length ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    total_bars = bars * 3
    item_length = bar_length_sec * total_bars
    
    # Create the media item
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(start_sec, end_sec, pitch, velocity):
        # Convert absolute seconds into MIDI PPQ for strict grid alignment
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        pitch = max(0, min(127, int(pitch)))
        velocity = max(1, min(127, int(velocity)))
        # pass True to noSort for batch speed; we'll sort at the end
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, True)

    # === Step 4: Rule of 3 Logic Execution ===
    
    # Diatonic scale degrees (0-indexed): I=0, ii=1, IV=3, V=4, vi=5
    prog_A = [0, 3, 5, 4]  # Phrase 1 & 2: I, IV, vi, V
    prog_B = [0, 3, 1, 4]  # Phrase 3: I, IV, ii, V (The Variation)
    
    chords_per_phrase = len(prog_A)
    beats_per_chord = (bars * beats_per_bar) / chords_per_phrase
    note_count = 0
    
    for phrase in range(3):
        is_phrase_B = (phrase == 2) # The 3rd repetition
        prog = prog_B if is_phrase_B else prog_A
        phrase_start_sec = phrase * bars * bar_length_sec
        
        for idx, root_deg in enumerate(prog):
            chord_start_sec = phrase_start_sec + idx * beats_per_chord * beat_len_sec
            chord_end_sec = chord_start_sec + (beats_per_chord - 0.2) * beat_len_sec
            
            # Stack fundamental thirds for chords
            chord_degrees = [root_deg, root_deg + 2, root_deg + 4]
            if is_phrase_B and idx == chords_per_phrase - 1:
                # Add the 7th scale degree to the final V chord for resolving tension
                chord_degrees.append(root_deg + 6) 
                
            # 1. Bass note layer
            insert_note(chord_start_sec, chord_end_sec, get_pitch(root_deg, 3), velocity_base - 10)
            note_count += 1
            
            # 2. Chord stack layer
            for deg in chord_degrees:
                insert_note(chord_start_sec, chord_end_sec, get_pitch(deg, 4), velocity_base - 20)
                note_count += 1
                
            # 3. Arpeggiated Melody layer
            # Apply the "Rule of 3" variation on the second half of the 3rd phrase
            is_variation = is_phrase_B and (idx >= chords_per_phrase / 2)
            num_8th_notes = int(beats_per_chord * 2)
            
            for i in range(num_8th_notes):
                note_start = chord_start_sec + i * 0.5 * beat_len_sec
                note_end = note_start + 0.4 * beat_len_sec
                
                if not is_variation:
                    # Expectation: Static, predictable looping arp
                    note_idx = i % len(chord_degrees)
                    pitch = get_pitch(chord_degrees[note_idx], 5)
                    vel = velocity_base if i % 2 == 0 else velocity_base - 15
                else:
                    # Variation: Subvert expectation by climbing octaves and crescendoing 
                    scale_len = len(scale_intervals)
                    octave_bump = i // len(chord_degrees)
                    deg = chord_degrees[i % len(chord_degrees)] + (octave_bump * scale_len)
                    pitch = get_pitch(deg, 5)
                    vel = velocity_base + (i * 2) # Crescendo effect
                
                insert_note(note_start, note_end, pitch, vel)
                note_count += 1

    # Cleanup and sort MIDI events
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {note_count} notes demonstrating the Rule of 3 (A-A-B variation) over {total_bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?