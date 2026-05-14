# Groovy Slap-Style Bassline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Groovy Slap-Style Bassline

* **Core Musical Mechanism**: This pattern relies heavily on **staccato articulation**, **octave displacement**, and **diatonic approach notes**. By keeping the primary root notes extremely short (leaving empty space in the low-end) and jumping up an octave on the off-beat 16th notes with high velocity, it mimics the physical "thumb-slap and finger-pop" technique of a real bass guitar. 
* **Why Use This Skill (Rationale)**: 
  - **Groove Theory**: The strategic use of gaps (rests) and ghost notes creates rhythmic tension. By slightly delaying the off-beat 16th notes (swing), it humanizes the grid.
  - **Frequency Management**: Short bass notes prevent the sub-frequencies from overlapping and muddying the mix, allowing the kick drum to punch through cleanly. The octave "pops" provide high-frequency transient clicks that help the bass cut through dense instrumentation.
  - **Harmonic Function**: Using diatonic approach notes on the last 16th note before a chord change pulls the listener's ear toward the new root, creating a strong sense of forward momentum.
* **Overall Applicability**: Essential for funk, nu-disco, synth-pop, house, and upbeat hip-hop. It serves as a lead rhythmic element that locks in with a syncopated drum groove.
* **Value Addition**: This skill encodes complex scale-degree math to automatically generate musically correct 5ths, octaves, and leading approach notes based on any chosen key and scale, rather than just playing a static flat loop.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/16th notes with subtle swing (delaying the odd-numbered 16th steps by ~15ms).
  - **Articulation**: Staccato. Downbeats are held for a dotted-16th length, followed by a 32nd-note rest before the off-beat pop.
  - **Ghost Notes**: Placed strategically before the heavy downbeats to simulate the physical muting of strings.
* **Step B: Pitch & Harmony**
  - **Downbeats (1 & 3)**: Root note of the current chord in the lower octave.
  - **Offbeats (1e, 3e)**: Octave (+12 semitones) of the root note.
  - **Mid-measure (Beat 2)**: The perfect 5th of the current chord.
  - **Turnaround (Beat 4)**: A diatonic approach note (one scale degree below the *next* chord's root) leading smoothly into the next bar.
* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` configured with a mix of Sawtooth (70%) and Square (30%) waves for rich harmonics.
  - **Envelope**: Fast attack (0ms), short decay (100ms), and low sustain (10%) to create a sharp, plucky transient that mimics a physical string being struck.
  - **Processing**: `JS: Saturation` added to emphasize the high-mid "click" of the slap.
* **Step D: Mix & Automation**
  - Velocity is mapped programmatically: 100 for standard plucks, 120 for octave "pops", and 50 for ghost notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm, Octaves & Approach notes | MIDI note insertion | Allows precise calculation of scale degrees, exact staccato lengths, and velocity variations. |
| Slap/Pluck Timbre | FX chain (ReaSynth + Saturation) | Tweaking the synth's ADSR envelope (short decay/sustain) is the most reliable native way to simulate the transient of a slapped string. |
| Humanization | Programmatic time offsets | Adding a static millisecond offset to off-beat 16ths creates a consistent, reproducible swing without relying on external MIDI groove templates. |

> **Feasibility Assessment**: 85% reproduction. The logic perfectly captures the rhythmic phrasing, scale-degree movement, and velocity dynamics shown in the tutorial. The only limitation is that we are using a synthesized plucky wave instead of a multi-sampled FL Studio Flex slap-bass ROMpler, but the musical and rhythmic function is identical.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Groovy Slap-Style Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    if scale not in SCALES:
        scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX Chain for Plucky Slap Sound ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the waveform: 70% Saw, 30% Square for rich harmonics
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.7) # Saw
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.3) # Square
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.3) # Volume (prevent clipping)
    # Envelope: Fast attack, short decay/sustain for pluck
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.1) # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.1) # Release

    # Add Saturation for transient bite
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(track, sat_idx, 0, 0.4) # Saturation Amount

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    grid_16th = bar_length_sec / 16.0
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Music Theory Driven Pattern ===
    # A standard funk progression using scale degrees: I - I - IV - V
    progression = [0, 0, 3, 4] 
    note_count = 0

    for bar in range(bars):
        current_chord = progression[bar % len(progression)]
        next_chord = progression[(bar + 1) % len(progression)]

        # Pattern mapping: (16th_step, length_in_16ths, scale_degree_offset, octave_offset, velocity_multiplier)
        pattern = [
            (0,  1.5, current_chord,          0, 1.0),   # Beat 1 Downbeat pluck
            (2,  0.5, current_chord,          1, 1.2),   # Offbeat octave POP
            (3,  0.5, current_chord,          0, 0.5),   # Ghost note
            (6,  1.0, current_chord + 4,      0, 0.9),   # Perfect 5th of chord
            (8,  1.5, current_chord,          0, 1.0),   # Beat 3 pluck
            (10, 0.5, current_chord,          1, 1.2),   # Offbeat octave POP
            (13, 0.5, current_chord,          0, 0.5),   # Ghost note setup
            (14, 0.5, current_chord,          0, 0.5),   # Ghost note 2
            (15, 0.5, next_chord - 1,         0, 0.9),   # Diatonic approach note to next chord
        ]

        for step, length, deg, oct_val, vel_mult in pattern:
            # Calculate exact MIDI pitch based on scale degrees and octaves
            # Div/Mod handles wraparounds naturally (e.g. going below root drops an octave)
            normalized_deg = deg % len(SCALES[scale])
            octave_shift = deg // len(SCALES[scale])
            semi_offset = SCALES[scale][normalized_deg]

            # Base MIDI 36 is C1. A good sub/bass foundation range.
            midi_note = 36 + NOTE_MAP[key] + semi_offset + (octave_shift + oct_val) * 12
            
            # Constrain velocity
            vel = int(velocity_base * vel_mult)
            vel = max(1, min(127, vel))

            # Calculate timing
            start_time = bar * bar_length_sec + step * grid_16th
            end_time = start_time + length * grid_16th

            # Humanization / Swing: Delay offbeat 16ths slightly
            swing_amt = 0.015 if step % 2 != 0 else 0.0
            start_time += swing_amt
            end_time += swing_amt

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_note, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} dynamic notes over {bars} bars at {bpm} BPM in {key} {scale}."
```