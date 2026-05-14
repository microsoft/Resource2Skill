# EDM / House Arrangement Macro-Structure Skeleton

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM / House Arrangement Macro-Structure Skeleton

* **Core Musical Mechanism**: This pattern encodes the *macro-arrangement* logic of standard electronic dance music (House, EDM, Pop). Rather than composing a specific melody, it generates an 11-block timeline skeleton (Intro → Break → Build → Drop → Break → Build → Drop → Outro) using color-coded tracks and labeled MIDI items. It also populates foundational rhythms (four-on-the-floor kicks, 2 & 4 claps, off-beat hats, snare rolls, and root-note sub-bass) inside the appropriate structural blocks.
* **Why Use This Skill (Rationale)**: The hardest part of producing a track is often turning a 4-bar loop into a full 5-minute song. This structure manages *energy and tension*. The breakdown removes low-frequency content to create a sense of floating, the build-up uses snare roll crescendos to create rhythmic tension, and the drop resolves both frequency masking and rhythmic syncopation by bringing back the full frequency spectrum and the groove.
* **Overall Applicability**: Essential for any electronic dance music genre (House, Techno, Trance, Dubstep, Future Bass). It acts as an interactive blueprint to cure "blank canvas syndrome", giving the automated agent (or human producer) exactly where to put risers, where to filter synths, and where to place the heaviest bass layers.
* **Value Addition**: Compared to a blank MIDI clip, this skill adds architectural scaffolding. It scales dynamically based on the requested `bars` parameter (defaulting to 16 bars per block, yielding a full 176-bar club track) and automatically anchors the rhythm and key.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Macro Timing**: The track is divided into 11 structural blocks. By default, 1 block = 16 bars.
  - **Micro Timing**: 
    - *Kicks*: 4/4 quarter notes during Drops, Beats, and Builds.
    - *Claps/Snares*: Beats 2 and 4. During build-ups, a snare roll accelerates from quarter notes to 8th notes to 16th notes with a crescendo velocity.
    - *Hats*: Strict off-beat 8th notes.
* **Step B: Pitch & Harmony**
  - **Bass Anchoring**: The Sub Bass track automatically plays long, sustained notes on the root key (e.g., C1) during the "Drop" sections to establish the fundamental harmony.
* **Step C: Sound Design & FX (Structural Roles)**
  - Creates 8 dedicated tracks housed inside a master folder.
  - Generates labeled MIDI items representing structural roles: "Uplifters", "Impacts", "Main Riff (Filtered)", "Vocal Chops". These instruct the producer (or downstream agent) on exactly what sounds to design and where to place them.
  - Applies color coding (Blue for Drums, Cyan for Bass, Purple for Synths, Orange for Vocals, Green for FX) for immediate visual feedback.
* **Step D: Mix & Automation (Implied)**
  - The arrangement visually implies where automation should occur: filters opening during the "Build" items, maximum loudness at the "Drop" items, and sparse mixes during the "Break" items.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Architecture | `RPR_InsertTrackAtIndex` + Folder Depth | Creates an organized, collapsible group that doesn't overwrite existing user tracks. |
| Structural Blueprint | `RPR_CreateNewMIDIItemInProj` + Take Names | Generates editable MIDI items that clearly display text labels in the arrange view. |
| Global Navigation | `RPR_AddProjectMarker2` (Regions) | Creates colored timeline regions (Intro, Drop 1, Build 2) allowing easy navigation and looping. |
| Foundational Rhythms | MIDI Note Insertion | Populates the generated Drop/Build items with actual 4/4 rhythms, snare rolls, and root notes to make the skeleton immediately playable. |

> **Feasibility Assessment**: 100% reproducible. The tutorial is fundamentally about track structuring, labeling, and timeline placement. By creating dynamic MIDI items across the timeline, we successfully digitize the exact arrangement methodology taught in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Arrangement", 
    bpm: int = 128,
    key: str = "F",
    scale: str = "minor",
    bars: int = 16, 
    velocity_base: int = 100,
    **kwargs
) -> str:
    """
    Create an EDM Arrangement Macro-Structure Skeleton.
    The `bars` parameter defines the length of one macro-block (default 16 bars).
    Generates 11 blocks total (Intro, Break, Build, Drop 1, Break 2, Build 2, Drop 2, Outro).
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo and Define Root Note ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root_note = NOTE_MAP.get(key, 0)
    
    # Each structural block will be this many bars long
    block_size = max(4, bars) 
    instrument = kwargs.get("instrument", "EDM")
    
    def make_color(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    # Data Structure: (Track Name, Color, [(Start_Block, End_Block, Item_Label)])
    tracks_data = [
        ("Kick", make_color(50, 100, 255), [
            (0, 1, "Beat"),
            (2, 3, "Building 4/4"),
            (3, 5, "Main Kick"),
            (6, 8, "Building 4/4"),
            (8, 10, "Main Kick"),
            (10, 11, "Beat")
        ]),
        ("Snare/Clap", make_color(50, 100, 255), [
            (0, 1, "Claps"),
            (2, 3, "Snare Roll"),
            (3, 5, "Claps"),
            (6, 8, "Snare Roll"),
            (8, 10, "Claps"),
            (10, 11, "Claps")
        ]),
        ("Hi-Hats", make_color(50, 100, 255), [
            (0, 1, "Hats"),
            (2, 3, "Building Hats"),
            (3, 5, "Full Hats"),
            (6, 8, "Building Hats"),
            (8, 10, "Full Hats"),
            (10, 11, "Hats")
        ]),
        ("Sub Bass", make_color(50, 200, 200), [
            (3, 5, "Main Sub"),
            (8, 10, "Main Sub")
        ]),
        ("Bass Groove", make_color(50, 200, 200), [
            (0, 1, "Groove Intro"),
            (3, 5, "Main Groove"),
            (8, 10, "Main Groove"),
            (10, 11, "Groove Outro")
        ]),
        ("Synth Lead", make_color(150, 50, 255), [
            (1, 2, "Main Riff (Filtered)"),
            (2, 3, "Alternate Riff (Rising)"),
            (3, 5, "Main Riff (Full)"),
            (5, 6, "Alternate Riff"),
            (6, 8, "Main Riff (Rising)"),
            (8, 10, "Main Riff (Full + Layers)")
        ]),
        ("Vocals", make_color(255, 150, 50), [
            (1, 2, "Verse Vocals"),
            (2, 3, "Build Vocals"),
            (3, 5, "Vocal Chops"),
            (5, 8, "Verse 2 / Build Vocals"),
            (8, 10, "Vocal Chops")
        ]),
        ("FX", make_color(50, 255, 100), [
            (1, 1.1, "Crash"),
            (2, 3, "Uplifters"),
            (3, 3.1, "Impact"),
            (5, 5.1, "Crash"),
            (6, 8, "Uplifters"),
            (8, 8.1, "Impact"),
            (10, 10.1, "Crash")
        ])
    ]

    regions = [
        (0, 1, "Intro"),
        (1, 2, "Break / Verse 1"),
        (2, 3, "Build 1"),
        (3, 5, "Drop 1"),
        (5, 6, "Break 2"),
        (6, 8, "Build 2"),
        (8, 10, "Drop 2"),
        (10, 11, "Outro")
    ]

    beat_len = 60.0 / bpm
    bar_len = beat_len * 4
    block_len = bar_len * block_size

    # Helper function to insert foundational MIDI notes into specific items
    def add_notes(take, start_time, length, item_name):
        num_beats = int(round(length / beat_len))
        num_bars = int(round(length / bar_len))
        notes_added = False
        
        if item_name in ["Beat", "Building 4/4", "Main Kick"]:
            for b in range(num_beats):
                pos = start_time + b * beat_len
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos + beat_len*0.5)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
                notes_added = True
                
        elif item_name == "Claps":
            for b in range(num_beats):
                if b % 4 == 1 or b % 4 == 3: # Beats 2 and 4
                    pos = start_time + b * beat_len
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos + beat_len*0.5)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 39, velocity_base, False)
                    notes_added = True
                    
        elif item_name == "Full Hats":
            for b in range(num_beats):
                pos = start_time + b * beat_len + beat_len * 0.5 # Off-beat
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos + beat_len*0.25)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 42, max(10, velocity_base - 20), False)
                notes_added = True
                
        elif item_name == "Main Sub":
            for b in range(num_bars):
                pos = start_time + b * bar_len
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos + bar_len * 0.8) # 80% legato
                # Anchor sub bass to the root key (C1 range)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_note + 36, velocity_base, False)
                notes_added = True
                
        elif item_name == "Snare Roll":
            for b in range(num_bars):
                # Speed up the roll over time
                if b < num_bars * 0.5:
                    divs = 4 # Quarters
                elif b < num_bars * 0.75:
                    divs = 8 # Eighths
                else:
                    divs = 16 # Sixteenths
                    
                step = bar_len / divs
                for d in range(divs):
                    pos = start_time + b * bar_len + d * step
                    progress = (b * divs + d) / max(1, num_bars * divs)
                    # Crescendo velocity from 40 up to velocity_base
                    vel = int(40 + (velocity_base - 40) * progress)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos + step*0.5)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, 38, vel, False)
                    notes_added = True

        if notes_added:
            RPR.RPR_MIDI_Sort(take)

    # === Step 2: Create Master Folder Track ===
    # Append to the very bottom of the existing project
    folder_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(folder_idx, True)
    folder_tr = RPR.RPR_GetTrack(0, folder_idx)
    folder_name = f"{instrument.title()} Arrangement Skeleton" if instrument != "None" else "EDM Arrangement Skeleton"
    RPR.RPR_GetSetMediaTrackInfo_String(folder_tr, "P_NAME", folder_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(folder_tr, "I_FOLDERDEPTH", 1)
    
    current_idx = folder_idx + 1

    # === Step 3: Populate Architecture ===
    for i, (tr_name, color, items) in enumerate(tracks_data):
        RPR.RPR_InsertTrackAtIndex(current_idx, True)
        tr = RPR.RPR_GetTrack(0, current_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", tr_name, True)
        RPR.RPR_SetMediaTrackInfo_Value(tr, "I_CUSTOMCOLOR", color)
        
        # Last track closes the folder
        if i == len(tracks_data) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(tr, "I_FOLDERDEPTH", -1)
            
        # Create Items and Insert Rhythms
        for (start_block, end_block, item_name) in items:
            start_time = start_block * block_len
            length = (end_block - start_block) * block_len
            
            item = RPR.RPR_CreateNewMIDIItemInProj(tr, start_time, start_time + length, False)
            RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", color)
            
            take = RPR.RPR_GetActiveTake(item)
            RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", item_name, True)
            
            add_notes(take, start_time, length, item_name)
            
        current_idx += 1

    # === Step 4: Add Navigation Regions ===
    for (start_block, end_block, reg_name) in regions:
        start_time = start_block * block_len
        end_time = end_block * block_len
        # wantidx = -1 auto-assigns region ID
        RPR.RPR_AddProjectMarker2(0, True, start_time, end_time, reg_name, -1, 0)

    RPR.RPR_UpdateArrange()

    total_bars = 11 * block_size
    return f"Created {folder_name} (11 structural blocks, {total_bars} bars total) with foundational MIDI rhythms mapped to {key} at {bpm} BPM."
```