# Pentatonic Motif Developer (Catchy Melody Generator)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pentatonic Motif Developer (Catchy Melody Generator)

* **Core Musical Mechanism**: This pattern relies on two fundamental songwriting principles: restricted pitch selection and structured phrase development. It strictly uses the **Pentatonic Scale** to avoid dissonant half-steps, and builds a phrase using a core **A-A'-B** sequence: Establish a motif, Repeat it (exact or with slight variation), and finally execute a Complete Variation to resolve the phrase.
* **Why Use This Skill (Rationale)**: Human psychology craves a balance of predictability and surprise. By establishing a short 2-3 note motif (predictability), repeating it (reinforcement), and then varying it (surprise), you create "catchiness." The pentatonic scale is universally utilized because its lack of tritone or minor-second intervals makes virtually any sequence of notes sound harmonically agreeable.
* **Overall Applicability**: This is the universal blueprint for pop toplines, memorable synth leads, catchy vocal hooks, and foundational basslines. It thrives in any genre where immediate memorability is required (Pop, EDM, Hip-Hop, Indie).
* **Value Addition**: Compared to a random sequence of MIDI notes, this skill algorithmically enforces proper musical phrasing and tension/resolution, ensuring the generated melody acts as a cohesive musical "sentence" rather than disorganized noise.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4/4 time signature.
  - **Motif Rhythm**: Simple quarter notes (1/4) and eighth notes (1/8) to leave breathing room.
  - **Phrase Structure**: 4-bar loop.
    - Bar 1: Establish motif.
    - Bar 2: Exact repetition.
    - Bar 3: Repetition with rhythmic/pitch variation.
    - Bar 4: Complete variation (different rhythm and notes).
* **Step B: Pitch & Harmony**
  - **Scale**: Major Pentatonic (Root, 2, 3, 5, 6) or Minor Pentatonic.
  - **Interval Selection**: 
    - Motif: Scale degrees 2 and 3 (e.g., D and E in C major).
    - Variation: Adds Scale degree 1 (the Root) to ground the phrase.
    - Complete Variation: Reaches up to Scale degrees 3, 5, and 6 to open up the melody before looping.
* **Step C: Sound Design & FX**
  - **Instrument**: A basic pluck or lead synth (using REAPER's native `ReaSynth`).
  - **Timbre**: A mix of sawtooth and square waves with a moderate release to create a distinct, "singable" pluck. 
* **Step D: Mix & Automation**
  - Moderate velocity (around 100) to ensure clarity. 
  - Notes are perfectly quantized to the grid to maintain the catchy, locked-in pop feel.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Melodic Phrasing | MIDI note insertion | Allows precise, parametric control over pitch, grid quantization, and the A-A'-B structural generation. |
| Pitch Restriction | Algorithmic scale mapping | Computes MIDI notes dynamically based on the input key and the pentatonic scale arrays, avoiding hardcoded pitches. |
| Catchy Timbre | FX chain (ReaSynth) | Provides a standalone, recognizable lead sound out-of-the-box using purely native plugins. |

> **Feasibility Assessment**: 100% reproducible. The mathematical relationship of the pentatonic scale and the exact phrase structure (Establish -> Repeat/Vary -> Complete Variation) demonstrated in the tutorial translates perfectly to structured MIDI generation inside REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Catchy Motif Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pentatonic Motif Melody in the current REAPER project.
    Implements the "Establish -> Repeat -> Vary -> Complete Variation" method.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (default to pentatonic_major).
        bars: Number of bars to generate (should be multiples of 4 for phrasing).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Normalize inputs
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_major"])
    
    # Base octave for a lead melody (C4 = 60)
    base_octave = 5 

    def calc_pitch(degree: int) -> int:
        """Converts a scale degree into a pure MIDI pitch."""
        scale_len = len(scale_intervals)
        octave_shift = degree // scale_len
        scale_idx = degree % scale_len
        return (base_octave + octave_shift) * 12 + root_val + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Define the Melodic Phrase (4-Bar structure) ===
    # Each note dictionary defines start_beat, length_in_beats, and scale degree
    phrase_blueprint = [
        # Bar 1 (Establish): 2-note motif
        {"b_start": 0.0, "b_len": 1.0, "degree": 1},
        {"b_start": 1.0, "b_len": 1.0, "degree": 2},
        
        # Bar 2 (Exact Repetition)
        {"b_start": 4.0, "b_len": 1.0, "degree": 1},
        {"b_start": 5.0, "b_len": 1.0, "degree": 2},
        
        # Bar 3 (Repetition with Variation): Speeds up, adds the root note (degree 0)
        {"b_start": 8.0, "b_len": 1.0, "degree": 1},
        {"b_start": 9.0, "b_len": 0.5, "degree": 2},
        {"b_start": 9.5, "b_len": 1.5, "degree": 0},
        
        # Bar 4 (Complete Variation): Reaches higher into the scale
        {"b_start": 12.0, "b_len": 1.0, "degree": 2},
        {"b_start": 13.0, "b_len": 1.0, "degree": 3},
        {"b_start": 14.0, "b_len": 2.0, "degree": 4}
    ]

    # === Step 4: Create MIDI Item and Populate Notes ===
    beats_per_bar = 4.0
    sec_per_beat = 60.0 / bpm
    
    # Ensure minimum of 4 bars to complete one full phrase loop
    total_bars = max(4, bars - (bars % 4) if bars % 4 != 0 else bars)
    total_beats = total_bars * beats_per_bar
    item_length_sec = total_beats * sec_per_beat
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Loop the 4-bar phrase across the requested total bars
    phrase_repeats = total_bars // 4
    note_count = 0

    for repeat in range(phrase_repeats):
        beat_offset = repeat * 16.0  # 4 bars * 4 beats
        
        for note in phrase_blueprint:
            absolute_beat_start = beat_offset + note["b_start"]
            absolute_beat_end = absolute_beat_start + note["b_len"]
            
            start_time = absolute_beat_start * sec_per_beat
            end_time = absolute_beat_end * sec_per_beat
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = calc_pitch(note["degree"])
            
            # Add slight velocity humanization on downbeats vs upbeats
            vel = velocity_base if (absolute_beat_start % 1.0 == 0) else max(10, velocity_base - 15)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Sound Design) ===
    # Add native ReaSynth to create a catchy pluck lead
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth: Saw/Square blend with a moderate release for a "pluck" sound
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Waveform blend (mix of saw/square)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01)  # Attack time (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.35)  # Release time (musical fade)

    return f"Created '{track_name}' with {note_count} catchy melody notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale? (Yes, uses `calc_pitch` helper parsing scale intervals).
- [x] Is it purely ADDITIVE? (Yes, uses `RPR_InsertTrackAtIndex` safely).
- [x] Does it set the track name? (Yes, explicitly names it "Catchy Motif Lead").
- [x] Are all velocity values in the 0-127 MIDI range? (Yes, safely scales around `velocity_base`).
- [x] Are note timings quantized to the musical grid? (Yes, driven by exact beat divisions).
- [x] Does the function return a descriptive status string? (Yes).
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, it strictly executes the "Establish -> Repeat -> Rep/Var -> Comp/Var" template demonstrated).
- [x] Does it respect the parameters? (Yes, supports arbitrary keys, tempos, and dynamically scales to requested lengths in chunks of 4).
- [x] Does it avoid hardcoded file paths? (Yes, pure MIDI and stock ReaSynth generation).