### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Arrangement Pattern

* **Core Musical Mechanism**: Structural variation on the third repetition of a phrase. The pattern establishes a musical idea (iteration 1), reinforces it to set listener expectation (iteration 2), and then breaks that expectation by introducing new harmonic/melodic information (iteration 3). 
* **Why Use This Skill (Rationale)**: Human brains are highly adept at pattern recognition. According to the video, hearing a phrase twice is enough to recognize the pattern, but hearing it a third time causes the brain to "tune it out" and lose interest (habituation). Changing the progression or melody on the third iteration generates cognitive reward, maintains tension, and keeps the listener engaged. 
* **Overall Applicability**: This is a macro-compositional tool applicable to any genre. It works beautifully for chord progressions, lead melodies, basslines, drum fills, and vocal chops. It is essentially the "A-A-B" or "A-A-A'" structure found in everything from classical sonatas to modern EDM drops.
* **Value Addition**: Instead of simply looping a 4-bar MIDI clip indefinitely (a common amateur mistake), this skill encodes *arrangement intelligence*. It transforms a static loop into a forward-moving composition.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Grid**: 1/8th note arpeggios over whole-note chords.
  - **Phrase Structure**: 3 iterations of a 4-bar phrase (12 bars total). 
  - **Variation Timing**: The variation occurs halfway through the 3rd iteration (bars 11 and 12).

* **Step B: Pitch & Harmony**
  - **Base Phrase (Iterations 1 & 2)**: Alternates between the I and IV chords (degrees 0 and 3). Ascending 8th note arpeggios.
  - **Variation Phrase (Iteration 3)**: Starts with I and IV, but breaks expectation by shifting to the VI and V chords (degrees 5 and 4). The melody contour flips from ascending to descending to emphasize the change.
  - **Key/Scale**: Fully parametric (defaults to C Major).

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` for basic polyphonic tone generation.
  - **Effects**: `ReaDelay` added to provide rhythmic echoes and space, preventing the dry synth from sounding too sterile.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rule of 3 Structure | Python Loop Logic | Allows dynamic generation of the A-A-A' structure regardless of the chosen scale or length. |
| Chords & Melodies | `RPR_MIDI_InsertNote` | Provides precise control over the varying harmonic degrees and melodic contours required to demonstrate the expectation break. |
| Timbre & Space | `RPR_TrackFX_AddByName` | Uses stock REAPER plugins (ReaSynth, ReaDelay) to ensure the script runs immediately without external dependencies. |

> **Feasibility Assessment**: 100% reproducible. The script captures the exact compositional philosophy detailed in the video (Option 2: "Go somewhere different halfway through the 3rd time") using pure music theory math and REAPER's native MIDI API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' compositional structure in the current REAPER project.
    Generates 3 iterations of a phrase, introducing a variation on the 3rd iteration.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Target number of bars. Will be rounded to a multiple of 3 to satisfy the pattern.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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

    # Input sanitization
    scale = scale.lower()
    if scale not in SCALES:
        scale = "major"
    if key not in NOTE_MAP:
        key = "C"
        
    velocity_base = max(10, min(127, velocity_base))
    scale_intervals = SCALES[scale]
    root_pitch = NOTE_MAP[key]

    # === Step 1: Set Tempo & Structure ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Enforce Rule of 3 structure: we need exactly 3 iterations.
    # We divide the requested bars by 3 to find the phrase length.
    total_bars = max(3, (bars // 3) * 3)
    phrase_bars = total_bars // 3
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Helper Functions for MIDI Generation ===
    def get_pitch(octave, degree):
        scale_len = len(scale_intervals)
        octave_offset = degree // scale_len
        scale_degree = degree % scale_len
        return root_pitch + (octave + octave_offset) * 12 + scale_intervals[scale_degree]

    def insert_chord(position_sec, duration_sec, root_deg, octave, velocity):
        # Insert Root, 3rd, and 5th
        for offset in [0, 2, 4]:
            pitch = get_pitch(octave, root_deg + offset)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, position_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, position_sec + duration_sec)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, False)

    def insert_melody(position_sec, duration_sec, root_deg, octave, velocity, descending=False):
        # Standard ascending arpeggio: Root, 3rd, 5th, Octave, 5th, 3rd, Root, 3rd
        offsets = [0, 2, 4, 7, 4, 2, 0, 2]
        
        if descending:
            # Variation descending arpeggio to emphasize the expectation break
            offsets = [7, 4, 2, 0, 2, 4, 7, 4]
            
        step_duration = duration_sec / 8.0
        for i, offset in enumerate(offsets):
            pitch = get_pitch(octave, root_deg + offset)
            start_sec = position_sec + i * step_duration
            end_sec = start_sec + step_duration * 0.8 # 80% legato length
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Accent the first note of the arpeggio
            vel = velocity if i == 0 else int(velocity * 0.8)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 4: Populate MIDI logic (The Rule of 3) ===
    notes_created = 0
    
    for iteration in range(3):
        is_variation_iteration = (iteration == 2)
        
        for bar_in_phrase in range(phrase_bars):
            global_bar = iteration * phrase_bars + bar_in_phrase
            position_sec = global_bar * bar_length_sec
            
            # Determine if we are in the "break expectation" phase 
            # (Latter half of the 3rd iteration)
            is_variation_bar = is_variation_iteration and (phrase_bars == 1 or bar_in_phrase >= phrase_bars / 2)
            
            # Select chord degrees
            if is_variation_bar:
                # Break expectation: shift to VI and V chords
                chord_deg = 5 if bar_in_phrase % 2 == 0 else 4 
            else:
                # Base pattern: alternate between I and IV chords
                chord_deg = 0 if bar_in_phrase % 2 == 0 else 3 
                
            # Insert backing block chords
            insert_chord(position_sec, bar_length_sec, chord_deg, 4, velocity_base - 30)
            notes_created += 3
            
            # Insert lead melody (flips contour during variation bars)
            insert_melody(position_sec, bar_length_sec, chord_deg, 5, velocity_base, descending=is_variation_bar)
            notes_created += 8

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)

    return f"Created '{track_name}' showcasing the Rule of 3: {notes_created} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
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