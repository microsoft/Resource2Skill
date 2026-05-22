### 1. High-level Design Pattern Extraction

> **Skill Name**: Songwriting Layout & Workflow Scaffold (Reapertips Framework)

* **Core Musical Mechanism**: Structural organization and workflow optimization. This video is a DAW customization and workflow tutorial rather than a music production tutorial (no specific beat, melody, or synth is designed). The core mechanism extracted here is the **Songwriting Track Architecture** and **Macro Automation** demonstrated at `03:10` and `05:03`. By pre-configuring a digital workspace with grouped instruments, visual color-coding, and scale references, the producer removes technical friction from the creative process.

* **Why Use This Skill (Rationale)**: In music production, the speed of translating an idea into the DAW is critical. As noted in the tutorial, getting "lost in the process of perfecting your setup" causes procrastination. By generating a pre-routed, color-coded layout (Drums, Bass, Guitars, Keys) with established tempos and key/scale references, the producer enters an immediate "creative flow" state without wasting 15 minutes adding tracks and routing folders.

* **Overall Applicability**: Used at the very beginning of a project to establish a blank-slate songwriting environment. This mirrors the specific "Songwriting Screenset/Layout" taught in the tutorial, preparing the DAW for additive tracking, MIDI programming, and arranging.

* **Value Addition**: Instead of starting with a completely blank REAPER project, this skill encodes structural DAW knowledge. It automatically builds a folder hierarchy, applies visual organization, and drops a dynamically generated MIDI scale-reference item into the project based on the user's chosen key and scale, acting as a direct guide for writing melodies and chords.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: Dynamic (determined by user parameter, standard songwriting defaults range 90-120 BPM).
  - **Grid**: The script establishes a 4-bar empty canvas, giving a structural starting point for loop-based songwriting. 
  - **Action**: Generates a 1-bar rhythmic reference pulse (quarter notes) on the generated Drum track.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Fully parametric based on user input. 
  - **Implementation**: Because the video does not dictate a specific chord progression, the script generates a "Scale Reference Guide" MIDI item on the Keys track. It computes the exact MIDI pitches of the chosen scale (e.g., C Minor) and writes an ascending scale run over the first bar to guide the producer.

* **Step C: Sound Design & FX**
  - **Track Architecture**: Creates a parent Folder ("SONGWRITING BUS") containing child tracks: "Drums", "Bass", "Guitars", and "Keys".
  - **Stock FX Placeholders**: Inserts standard REAPER stock plugins (`ReaEQ`, `ReaComp`) onto the bus and instrument tracks as lightweight mixing placeholders, mimicking a professional template setup.

* **Step D: Mix & Automation (if applicable)**
  - **Color Coding**: Applies visual color grouping to the tracks (e.g., Drums = Red, Bass = Blue, Keys = Yellow) which is a core tenet of the visual layout organization shown in the tutorial.
  - **Routing**: Automatically configures the REAPER folder depth so the instrument tracks sum into the parent bus.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Architecture | `RPR_InsertTrackAtIndex`, `I_FOLDERDEPTH` | Accurately recreates the grouped "Songwriting Layout" UI shown in the video. |
| Visual Organization | `RPR_SetMediaTrackInfo_Value` (Colors) | Essential for the custom layout/screenset aesthetic emphasized by Reapertips. |
| Key/Scale Integration | MIDI note insertion (`RPR_MIDI_InsertNote`) | Satisfies the requirement to compute music theory arrays into data by providing a scale reference guide item. |
| Workflow Readiness | `RPR_TrackFX_AddByName` | Pre-loads stock EQ and Compression to save the producer clicks during the writing phase. |

> **Feasibility Assessment**: 100% of the *applicable* additive layout concepts from the video are reproduced. Because the video is about UI customization, shortcuts, and custom actions (rather than writing a specific song), generating a parameterized Songwriting Template with a dynamic scale-guide is the most accurate way to translate this workflow tutorial into an executable, additive ReaScript pattern.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Songwriting Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Songwriting Layout Scaffold based on the Reapertips tutorial.
    Generates a folder structure (Drums, Bass, Guitars, Keys), color-codes them,
    adds placeholder FX, and generates a MIDI scale reference based on parameters.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the starting canvas.
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

    # Normalize key and scale
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Establish Root Octave (C3 = 48)
    base_midi_note = 48 + root_val

    # Colors (REAPER format: R + 256*G + 65536*B | 16777216)
    COLOR_PARENT = 16777216 | (50 + 256*50 + 65536*50)   # Dark Gray
    COLOR_DRUMS  = 16777216 | (200 + 256*50 + 65536*50)  # Red
    COLOR_BASS   = 16777216 | (50 + 256*50 + 65536*200)  # Blue
    COLOR_GUITAR = 16777216 | (50 + 256*200 + 65536*50)  # Green
    COLOR_KEYS   = 16777216 | (200 + 256*200 + 65536*50) # Yellow

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track Architecture ===
    start_idx = RPR.RPR_CountTracks(0)
    
    track_definitions = [
        {"name": f"{track_name} BUS", "depth": 1, "color": COLOR_PARENT, "fx": ["ReaEQ", "ReaComp"]},
        {"name": "Drums", "depth": 0, "color": COLOR_DRUMS, "fx": ["ReaEQ"]},
        {"name": "Bass", "depth": 0, "color": COLOR_BASS, "fx": ["ReaEQ"]},
        {"name": "Guitars", "depth": 0, "color": COLOR_GUITAR, "fx": ["ReaEQ"]},
        {"name": "Keys (Scale Ref)", "depth": -1, "color": COLOR_KEYS, "fx": ["ReaEQ", "ReaVerbate"]}
    ]

    created_tracks = []
    
    for i, t_def in enumerate(track_definitions):
        idx = start_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Set Name, Folder Depth, and Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_def["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", t_def["depth"])
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_def["color"])
        
        # Add placeholder FX
        for fx_name in t_def["fx"]:
            RPR.RPR_TrackFX_AddByName(track, fx_name, False, -1)
            
        created_tracks.append(track)

    keys_track = created_tracks[4] # The 'Keys' track
    drums_track = created_tracks[1] # The 'Drums' track

    # === Step 3: Create MIDI Scale Reference Guide ===
    # Calculate timing
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    qn_length = 60.0 / bpm
    
    # 3a. Generate Scale Guide on Keys Track
    item_keys = RPR.RPR_AddMediaItemToTrack(keys_track)
    RPR.RPR_SetMediaItemInfo_Value(item_keys, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_keys, "D_LENGTH", bar_length_sec * bars)
    take_keys = RPR.RPR_AddTakeToMediaItem(item_keys)
    
    RPR.RPR_MIDI_DisableSort(take_keys)
    
    # Write the scale ascending as 8th notes for the first measure
    note_length_ppq = 480 # 8th note
    for i, interval in enumerate(scale_intervals):
        start_ppq = i * note_length_ppq
        end_ppq = start_ppq + note_length_ppq
        pitch = base_midi_note + interval
        
        RPR.RPR_MIDI_InsertNote(
            take_keys, False, False, 
            start_ppq, end_ppq, 
            0, pitch, velocity_base - 20, False
        )
    
    # Add a sustained root chord (I) for the remainder of the 4 bars
    start_ppq = len(scale_intervals) * note_length_ppq
    end_ppq = bars * beats_per_bar * 960 # 960 PPQ per quarter note
    
    # Simple triad: Root, Third, Fifth
    triad_intervals = [scale_intervals[0], scale_intervals[2], scale_intervals[4]]
    for interval in triad_intervals:
        pitch = base_midi_note + interval
        RPR.RPR_MIDI_InsertNote(
            take_keys, False, False, 
            start_ppq, end_ppq, 
            0, pitch, velocity_base - 30, False
        )
        
    RPR.RPR_MIDI_Sort(take_keys)

    # 3b. Generate simple rhythm guide on Drums Track
    item_drums = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_drums, "D_LENGTH", bar_length_sec * bars)
    take_drums = RPR.RPR_AddTakeToMediaItem(item_drums)
    
    RPR.RPR_MIDI_DisableSort(take_drums)
    # Basic four-on-the-floor kick reference (MIDI note 36)
    for bar in range(bars):
        for beat in range(beats_per_bar):
            start_ppq = (bar * beats_per_bar * 960) + (beat * 960)
            end_ppq = start_ppq + 240 # 16th note length
            vel = velocity_base if beat == 0 else velocity_base - 20
            RPR.RPR_MIDI_InsertNote(
                take_drums, False, False,
                start_ppq, end_ppq,
                0, 36, vel, False
            )
            
    RPR.RPR_MIDI_Sort(take_drums)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' Songwriting Scaffold (5 tracks) configured for {key} {scale} at {bpm} BPM with a dynamically generated {bars}-bar scale reference."
```