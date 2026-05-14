# Lead "Vocal Polish" Multi-FX Chain

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Lead "Vocal Polish" Multi-FX Chain

* **Core Musical Mechanism**: The video acts as a masterclass on the standard audio engineering toolkit (EQ, Compression, Saturation, Chorus, Delay, Reverb, etc.). The underlying pattern here isn't a specific beat, but rather the **standard sequential signal flow** used to polish a dry lead element (like a vocal or synth lead). This flow consists of: Tonal Sculpting (EQ) $\rightarrow$ Dynamic Control (Compression) $\rightarrow$ Harmonic Excitement (Saturation/Chorus) $\rightarrow$ Spatial Depth (Delay/Reverb).
* **Why Use This Skill (Rationale)**: This specific plugin order works synergistically based on psychoacoustics. Corrective EQ removes low-end mud *before* compression so that unwanted frequencies don't trigger the compressor. Compression then stabilizes the volume. Saturation and Chorus thicken the stabilized signal by adding harmonic overtones and micro-pitch shifting. Finally, Delay and Reverb push the sound back into a three-dimensional space, preventing the dry signal from feeling artificially disconnected from the mix.
* **Overall Applicability**: This is the universal starting template for mixing lead vocals, solo synthesizers, electric guitars, or any focal element that needs to sound upfront, rich, and spacious.
* **Value Addition**: Instead of generating a dry MIDI clip, this skill encodes professional mixing architecture. It automatically builds out the complete, ordered effects chain on a synthesized lead line, providing a ready-to-tweak channel strip template.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM Range**: 90-140 BPM (standard for pop/hip-hop vocals).
  - **Rhythm**: A syncopated, staccato 1/8th note melodic motif with intentional gaps. These rhythmic gaps are crucial because they provide the acoustic space for the Delay and Reverb tails to be heard.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (defaults to C Minor).
  - **Melody**: Uses the Root, minor 3rd, 4th, and 5th scale degrees. 
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` acts as a placeholder for a dry vocal or lead.
  - **Sculpting**: `ReaEQ` (prepares the tone, removes mud).
  - **Dynamics**: `ReaComp` (evens out the performance).
  - **Color**: `JS: Saturation` (adds analog drive) and `JS: Chorus` (adds a doubling effect).
  - **Space**: `ReaDelay` (creates rhythmic echoes) and `ReaVerbate` (places the sound in a room).
* **Step D: Mix & Automation**
  - Track volume is slightly attenuated to accommodate the volume buildup caused by adding multiple saturators and spatial effects in sequence.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Melodic Source | MIDI note insertion + ReaSynth | Generates a clean, dry source signal to demonstrate the mixing chain since external vocal audio files cannot be assumed. |
| Signal Flow Architecture | `RPR_TrackFX_AddByName` | Replicates the sequential mixing concepts taught in the video by stacking stock REAPER equivalents of the featured plugins. |

> **Feasibility Assessment**: 85% — The conceptual order and functional application of the mixing tools are perfectly reproduced using REAPER's native stock plugins. The remaining 15% accounts for the specific analog colorations of the third-party VSTs shown in the video (like FabFilter, Waves, and Valhalla), which are approximated using REAPER's JSFX.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Polish Chain",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lead "Vocal Polish" Multi-FX Chain in the current REAPER project.
    Generates a staccato lead melody and processes it through a standard 
    mixing template: EQ -> Comp -> Saturation -> Chorus -> Delay -> Reverb.

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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Lower track volume slightly to prevent clipping from additive FX
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.7)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Staccato MIDI Motif ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    octave = 5
    base_midi = root_val + (octave * 12)
    
    # Pattern: (start_beat, length_beats, scale_degree)
    # Designed with rhythmic gaps to showcase the delay/reverb tails
    pattern_beats = [
        (0.0, 0.5, 0),     # Root
        (0.5, 0.5, 4),     # 5th
        (1.5, 0.5, 2),     # 3rd
        (4.0, 0.5, 3),     # 4th (start of next bar)
        (5.0, 0.5, 4),     # 5th
        (6.0, 1.0, 0)      # Root
    ]
    
    qlen = 60.0 / bpm
    
    # Populate notes across requested bars
    for bar in range(bars // 2):
        bar_offset_beats = bar * 8.0 
        for start_b, len_b, deg in pattern_beats:
            pitch = base_midi + scale_intervals[deg % len(scale_intervals)]
            start_t = (bar_offset_beats + start_b) * qlen
            end_t = (bar_offset_beats + start_b + len_b) * qlen
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_t)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_t)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), False)
            
    # Handle odd number of bars remaining
    if bars % 2 != 0:
        bar_offset_beats = (bars - 1) * 4.0
        for start_b, len_b, deg in pattern_beats[:3]:
            pitch = base_midi + scale_intervals[deg % len(scale_intervals)]
            start_t = (bar_offset_beats + start_b) * qlen
            end_t = (bar_offset_beats + start_b + len_b) * qlen
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_t)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_t)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Build the Multi-FX Processing Chain ===
    # 1. Source Generation
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Tonal Sculpting (Highpass & Polish)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # 3. Dynamic Control (Evening out the volume)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # 4. Harmonic Excitement (Analog feel)
    RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    
    # 5. Thickening / Doubling Effect
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    
    # 6. Spatial Depth (Rhythmic echoes)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    
    # 7. Spatial Space (Room/Hall simulation)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    return f"Created '{track_name}' with a complete mixing chain (EQ -> Comp -> Saturation -> Chorus -> Delay -> Reverb) spanning {bars} bars at {bpm} BPM."
```