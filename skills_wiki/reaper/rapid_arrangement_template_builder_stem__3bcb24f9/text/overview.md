# Rapid Arrangement Template Builder (Stem Buses, Folders & Regions)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Rapid Arrangement Template Builder (Stem Buses, Folders & Regions)

* **Core Musical Mechanism**: This skill encapsulates structural workflow and macro-arrangement. Rather than a specific melody, it generates the architectural foundation of a track: a pre-routed track hierarchy (Stem Folders), standardized arrangement blocks (Intro, Verse, Chorus via Regions), and timeline markers. It also injects a foundational rhythmic groove into the newly created drum buses to immediately establish a musical context.
* **Why Use This Skill (Rationale)**: The blank canvas is the biggest hurdle in music production. By immediately generating a categorized stem structure (Drum Bus, Instrument Bus) and labeling the timeline, cognitive load is drastically reduced. From a mixing perspective, grouping instruments into sub-mix buses early encourages "top-down mixing" (processing groups as cohesive units), which glues elements together more effectively than individual track processing.
* **Overall Applicability**: Essential for the start of *any* new session. It shines in modern pop, hip-hop, and EDM workflows where structured arrangement (8-bar intros, 16-bar verses) and stem-based routing are standard industry practice. 
* **Value Addition**: Compared to a blank REAPER project, this skill automatically encodes structural music theory (standard section lengths) and audio engineering best practices (sub-group routing, visual color-coding, and pre-loaded bus compression).

### 2. Technical Breakdown

* **Step A: Rhythm & Timing (Arrangement Structure)**
  - **Grid/Timeline**: Translates musical bars into absolute time using REAPER's internal Quarter Note (QN) mapping.
  - **Regions**: Generates a standard pop/hip-hop structure:
    - Intro: Bars 1-9 (8 bars)
    - Verse: Bars 9-25 (16 bars)
    - Chorus: Bars 25-33 (8 bars)
  - **Groove**: Injects a 4-to-the-floor kick and backbeat snare (2 & 4) over the first 4 bars to instantly establish the tempo.

* **Step B: Pitch & Harmony**
  - **Kick**: C1 (MIDI 36)
  - **Snare**: D1 (MIDI 38)
  - **Hi-hat**: F#1 (MIDI 42)

* **Step C: Sound Design & FX**
  - **Routing Hierarchy**: Utilizes REAPER's `I_FOLDERDEPTH` property.
    - Drum Bus (Parent: +1) → Kick (0), Snare (0), Hats (-1 to close folder)
    - Inst Bus (Parent: +1) → Bass (0), Synth (-1 to close folder)
  - **Pre-loaded FX**: Instantiates `ReaComp` (Stock Compressor) on the Drum Bus for immediate top-down transient control.

* **Step D: Mix & Automation**
  - Applies distinct custom colors to track groups (e.g., Red for Drums, Blue for Instruments) to mimic the auto-coloring workflow showcased in the tutorial.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Project Structure & Regions | `RPR_AddProjectMarker2` | Perfectly replicates the video's technique of organizing the timeline with visual boundaries. |
| Track Busing & Folders | `RPR_SetMediaTrackInfo_Value` (`I_FOLDERDEPTH`) | REAPER's native, programmatic way of creating track groups and stems. |
| Base Drum Groove | MIDI Note Insertion | Proves the routing works by providing immediate, tempo-synced musical feedback on the new tracks. |
| Bus Compression | `RPR_TrackFX_AddByName` | Mirrors the tutorial's focus on having go-to FX ready on specific sub-mixes. |

> **Feasibility Assessment**: 100% reproduction of the workflow philosophy. While the exact 3rd-party plugins or custom custom themes shown in the video cannot be generated via raw scripting, the underlying structural mechanism (Folders, Regions, Markers, FX instantiation, and routing) is fully natively reproduced.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Template_Project",
    track_name: str = "Master_Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Rapid Arrangement Template (Buses, Folders, Regions) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused directly here (we create a specific multi-track structure).
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars for the initial drum groove.
        velocity_base: Base MIDI velocity for the groove.
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the template creation.
    """
    import reaper_python as RPR

    # === Helper Functions ===
    def add_track_with_folder(index, name, folder_depth, r, g, b):
        """Creates a track, sets its folder depth, and colors it."""
        RPR.RPR_InsertTrackAtIndex(index, True)
        track = RPR.RPR_GetTrack(0, index)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", folder_depth)
        
        # REAPER Native Color Format: r + (g * 256) + (b * 65536) + 16777216
        color_val = int(r + (g * 256) + (b * 65536) + 16777216)
        RPR.RPR_SetTrackColor(track, color_val)
        return track

    def add_midi_item_to_track(track, start_qn, end_qn):
        """Creates a MIDI item mapped exactly to quarter notes."""
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", end_time - start_time)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    def insert_note(take, qn_start, qn_len, pitch, vel):
        """Inserts a note based on Quarter Note absolute positions."""
        start_time = RPR.RPR_TimeMap2_QNToTime(0, qn_start)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, qn_start + qn_len)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Timeline Regions ===
    # Using standardized arrangements: Intro (8 bars), Verse (16 bars), Chorus (8 bars)
    # QN math: 4 QN per bar (assuming 4/4)
    regions = [
        {"name": "Intro",  "start_bar": 1,  "len_bars": 8,  "color": (100, 200, 100)},
        {"name": "Verse",  "start_bar": 9,  "len_bars": 16, "color": (100, 150, 200)},
        {"name": "Chorus", "start_bar": 25, "len_bars": 8,  "color": (200, 100, 100)}
    ]
    
    for idx, reg in enumerate(regions):
        start_qn = (reg["start_bar"] - 1) * 4
        end_qn = start_qn + (reg["len_bars"] * 4)
        start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
        c_val = int(reg["color"][0] + (reg["color"][1] * 256) + (reg["color"][2] * 65536) + 16777216)
        RPR.RPR_AddProjectMarker2(0, True, start_time, end_time, reg["name"], idx+1, c_val)

    # === Step 3: Create Track Folder Hierarchy ===
    start_idx = RPR.RPR_CountTracks(0)
    
    # 3a. Drum Bus Structure
    drum_bus = add_track_with_folder(start_idx, "Drum Bus", 1, 220, 80, 80) # Parent, Red
    kick_trk = add_track_with_folder(start_idx + 1, "Kick", 0, 255, 120, 120)
    snare_trk = add_track_with_folder(start_idx + 2, "Snare", 0, 255, 120, 120)
    hat_trk = add_track_with_folder(start_idx + 3, "Hi-Hats", -1, 255, 120, 120) # -1 Closes folder
    
    # 3b. Instrument Bus Structure
    inst_bus = add_track_with_folder(start_idx + 4, "Inst Bus", 1, 80, 180, 220) # Parent, Blue
    bass_trk = add_track_with_folder(start_idx + 5, "Bass", 0, 120, 200, 255)
    synth_trk = add_track_with_folder(start_idx + 6, "Synth", -1, 120, 200, 255) # -1 Closes folder

    # === Step 4: Add Top-Down FX to Buses ===
    # Emulates the tutorial's workflow of having default reverbs/compressors ready
    RPR.RPR_TrackFX_AddByName(drum_bus, "ReaComp", False, -1)
    
    # Enable a basic instrument on the generated kick/snare so they make sound
    RPR.RPR_TrackFX_AddByName(kick_trk, "ReaSamplOmatic5000", False, -1)
    RPR.RPR_TrackFX_AddByName(snare_trk, "ReaSamplOmatic5000", False, -1)

    # === Step 5: Inject Foundational Groove ===
    # Creates a 4-bar groove (as requested by 'bars' param) so the template isn't completely empty
    groove_len_qn = bars * 4
    
    _, kick_take = add_midi_item_to_track(kick_trk, 0, groove_len_qn)
    _, snare_take = add_midi_item_to_track(snare_trk, 0, groove_len_qn)
    _, hat_take = add_midi_item_to_track(hat_trk, 0, groove_len_qn)

    # MIDI Pitches
    PITCH_KICK = 36 # C1
    PITCH_SNARE = 38 # D1
    PITCH_HAT = 42 # F#1

    for bar in range(bars):
        bar_qn = bar * 4
        # 4-to-the-floor kick
        for beat in range(4):
            insert_note(kick_take, bar_qn + beat, 0.25, PITCH_KICK, velocity_base)
            # 8th note hi-hats
            insert_note(hat_take, bar_qn + beat, 0.25, PITCH_HAT, velocity_base - 20)
            insert_note(hat_take, bar_qn + beat + 0.5, 0.25, PITCH_HAT, velocity_base - 40)
        
        # Snare on 2 and 4
        insert_note(snare_take, bar_qn + 1.0, 0.25, PITCH_SNARE, velocity_base + 10)
        insert_note(snare_take, bar_qn + 3.0, 0.25, PITCH_SNARE, velocity_base + 10)

    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(snare_take)
    RPR.RPR_MIDI_Sort(hat_take)

    return f"Created Stem Folder Template with 7 tracks (Drums & Inst), 3 timeline Regions, and {bars} bars of foundational groove at {bpm} BPM."
```