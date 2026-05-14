# 137 BPM Trap/Hip-Hop Skeleton (Half-Time Feel)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 137 BPM Trap/Hip-Hop Skeleton (Half-Time Feel)

* **Core Musical Mechanism**: While this video is strictly a DAW workflow and shortcut tutorial for Ableton Live, the underlying project used to demonstrate these techniques is a modern 137 BPM trap/hip-hop beat. The core musical mechanism here is the **half-time rhythmic feel**. At 137 BPM, placing the snare on beat 3 (instead of beats 2 and 4) cuts the perceived tempo in half (~68.5 BPM), creating the slow, heavy "bounce" characteristic of modern rap and electronic production. 

* **Why Use This Skill (Rationale)**: The half-time feel allows for aggressive, fast subdivisions in the hi-hats (1/8th and 1/16th notes) while maintaining a relaxed, head-nodding groove in the main backbeat. The syncopated kick drum plays off the rigid hi-hat grid to create forward momentum, leaving plenty of frequency space for a heavy sub-bass.

* **Overall Applicability**: This is the foundational rhythmic grid for trap, modern hip-hop, drill, and future bass. It serves as an excellent starting point for building a beat; once this skeleton is laid down, producers can focus on sound design, sample manipulation, and vocal recording.

* **Value Addition**: This skill translates the visual layout of the project shown in the video into a functional REAPER template. Instead of an empty project, it provides a correctly tempo-synced, half-time drum MIDI structure and a tuned sub-bass track, ready for further sound design.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 137 BPM (visible in the DAW top-left at 1:50).
  - **Time Signature**: 4/4, but felt in half-time.
  - **Drum Grid**: 
    - Kicks: Beat 1, and syncopated 8th/16th notes (e.g., the "and" of beat 2).
    - Snares: Exclusively on beat 3 of every bar.
    - Hi-hats: Continuous 8th notes, serving as the metronomic anchor.

* **Step B: Pitch & Harmony**
  - **Bassline**: Follows the root notes of a minor key progression (dynamically calculated based on user input). Visually in the video, the sub-bass notes are long, sustained 808-style notes that hit simultaneously with the kick drum.

* **Step C: Sound Design & FX**
  - **Drums**: Standard MIDI drum mapping (Kick = 36, Snare = 38, Closed Hat = 42).
  - **Sub Bass**: A pure sine wave generator (`ReaSynth`) pitched to the lower octaves (C1-C2 range) to emulate an 808 sub.

* **Step D: Mix & Automation**
  - Sub bass is kept mono and placed centrally.
  - No complex automation is extracted here, as the video focuses on arrangement navigation rather than mixing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Tempo Setup | `RPR_SetCurrentBPM` | Matches the exact 137 BPM tempo of the tutorial's example project. |
| Drum Groove | MIDI note insertion | Allows for exact replication of the half-time trap rhythm (Kick on 1, Snare on 3). |
| Sub Bass Track | MIDI + `ReaSynth` FX | Recreates the visible "SubLab" track using REAPER native tools to provide the low-end foundation. |

> **Feasibility Assessment**: 85%. While the video is an Ableton workflow tutorial, we can reliably extract and reproduce the foundational 137 BPM musical framework of the demo project. The specific external plugins (like SubLab) and audio loops are replaced with REAPER-native MIDI and synthesis to ensure 100% executable reproducibility.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Workflow_Demo_Beat",
    track_name: str = "Trap Drums",
    bpm: int = 137,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 137 BPM Half-Time Trap Skeleton based on the example project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM (defaults to 137).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }

    # Ensure valid inputs
    key_upper = key.capitalize()
    if key_upper not in NOTE_MAP:
        key_upper = "F"
    root_note = NOTE_MAP[key_upper]
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Calculate bass root (Octave 1)
    bass_pitch = root_note + 24 

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Time calculations
    beat_length = 60.0 / bpm
    bar_length = beat_length * 4.0
    total_length = bar_length * bars

    # Helper function to insert MIDI notes safely
    def add_midi_note(take, start_time, duration, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- 1. CREATE DRUM TRACK ---
    num_tracks = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    drum_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", track_name, True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Standard GM Drum Map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    # Populate Drum Pattern
    for b in range(bars):
        bar_start = b * bar_length
        
        # Kick: Beat 1 and the "and" of 2 (syncopated)
        add_midi_note(drum_take, bar_start, beat_length * 0.25, KICK, velocity_base)
        add_midi_note(drum_take, bar_start + (beat_length * 1.5), beat_length * 0.25, KICK, velocity_base - 10)
        
        # Snare: Beat 3 (Half-time feel)
        add_midi_note(drum_take, bar_start + (beat_length * 2.0), beat_length * 0.25, SNARE, velocity_base + 10)
        
        # Hi-Hats: 8th notes
        for h in range(8):
            hat_time = bar_start + (h * (beat_length / 2.0))
            hat_vel = velocity_base if h % 2 == 0 else velocity_base - 20
            add_midi_note(drum_take, hat_time, beat_length * 0.2, HIHAT, hat_vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # --- 2. CREATE SUB BASS TRACK ---
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    sub_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", "Sub Bass", True)

    # Add native sine wave synth
    RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)

    sub_item = RPR.RPR_AddMediaItemToTrack(sub_track)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(sub_item, "D_LENGTH", total_length)
    sub_take = RPR.RPR_AddTakeToMediaItem(sub_item)

    # Populate Sub Pattern (following the kick drum)
    for b in range(bars):
        bar_start = b * bar_length
        # Long sustained sub note on beat 1
        add_midi_note(sub_take, bar_start, beat_length * 1.5, bass_pitch, velocity_base)
        
        # Move pitch up by a minor 3rd (interval index 1) for the second half of the 2nd/4th bars for movement
        current_pitch = bass_pitch
        if b % 2 != 0:
            current_pitch = bass_pitch + scale_intervals[2] # 3rd degree of scale

        add_midi_note(sub_take, bar_start + (beat_length * 1.5), beat_length * 2.0, current_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(sub_take)

    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' and 'Sub Bass' tracks over {bars} bars at {bpm} BPM in {key} {scale}."
```