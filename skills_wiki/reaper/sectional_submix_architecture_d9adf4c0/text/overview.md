# Sectional Submix Architecture

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sectional Submix Architecture

* **Core Musical Mechanism**: Dynamic arrangement processing via routing. Instead of automating bypass states or EQ parameters on a single track to change the sound between sections, the song arrangement is physically split. Each section (Verse, Pre-Chorus, Chorus) is moved to a dedicated child track, all grouped under a single parent folder track. 
* **Why Use This Skill (Rationale)**: Automating dozens of parameters (EQ bands, compressor thresholds, volume) across song transitions is tedious and error-prone. Dedicated tracks per section allow for dramatic tonal shifts—such as making the verse intentionally lo-fi, or widening and saturating the chorus—using static, easily adjustable plugin chains. 
* **Overall Applicability**: This pattern is crucial for stem mastering, dynamic vocal mixing (treating verse vocals differently from chorus vocals), and beat-making where drops require entirely different processing than build-ups.
* **Value Addition**: Compared to a basic track layout, this skill encodes professional mixing workflow architecture. It implements non-destructive crossfading across multiple lanes and establishes a top-down mixing hierarchy (Global glue compression -> Section-specific EQ/Saturation).

### 2. Technical Breakdown

* **Step A: Structure & Routing**
  - **Parent Track ("Master Bus")**: Acts as the summing bus. Set as a Folder Parent (`I_FOLDERDEPTH = 1`).
  - **Child Tracks ("Verse", "Pre-Chorus", "Chorus")**: Routed through the parent. The last track closes the folder (`I_FOLDERDEPTH = -1`).
* **Step B: Splitting & Fades**
  - Audio/MIDI items are split exactly at section boundaries (e.g., every 4 bars).
  - To prevent pops and ensure seamless flow, a 50ms overlap and crossfade is applied. Because the items are on different tracks but sum to the same parent, concurrent fade-outs and fade-ins mathematically behave as a perfect crossfade.
* **Step C: Sound Design & FX**
  - **Parent Track**: Bus Compressor (ReaComp) -> Limiter (ReaLimit) for global dynamic control and "glue".
  - **Verse Track**: Lower track volume (`-3dB` / `0.7` linear), ReaEQ applied for a tamer, controlled sound.
  - **Pre-Chorus Track**: Moderate track volume (`-1.4dB` / `0.85` linear), building energy.
  - **Chorus Track**: Full track volume (`0dB` / `1.0` linear), ReaEQ + Saturation added for a wider, more aggressive tonal character.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Sectional Routing** | `RPR_InsertTrackAtIndex` & `I_FOLDERDEPTH` | Establishes the parent/child folder hierarchy shown in the video. |
| **Sectional FX Processing** | `RPR_TrackFX_AddByName` & `D_VOL` | Instantiates distinct plugins (EQ, Limiter, Saturation) and baseline levels for each structural track. |
| **Crossfading** | `D_FADEINLEN` & `D_FADEOUTLEN` | Extending item lengths by 50ms and applying fades simulates the auto-crossfade split behavior on the parent bus. |

> **Feasibility Assessment**: 100%. While the specific threshold knob values for third-party plugins (like "The Glue") vary, the structural routing, crossfading behavior, and section-specific FX instantiation translate perfectly to REAPER's native API using equivalent stock plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "SectionalMastering",
    track_name: str = "Master Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 16,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Sectional Submix Architecture in the current REAPER project.
    
    Creates a master folder track with glue compression, and child tracks
    for Verse, Pre-Chorus, and Chorus with their own specific levels/FX.
    Generates placeholder regions with overlapping crossfades.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (unused, structural skill).
        scale: Scale type (unused, structural skill).
        bars: Total number of bars to generate the arrangement for.
        velocity_base: Base MIDI velocity (unused, structural skill).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created routing architecture.
    """
    import reaper_python as RPR
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 1: Create Parent Track ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    # Set as Folder Parent
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1) 
    
    # Add Glue Compressor and Limiter to Parent
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaLimit", False, -1)
    
    # === Step 2: Create Child Tracks (Sections) ===
    unique_sections = ["Verse", "Pre-Chorus", "Chorus"]
    track_refs = {}
    
    for i, sec_name in enumerate(unique_sections):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        child_track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", sec_name, True)
        
        # Folder depth: -1 on the last track closes the folder grouping
        depth = -1 if i == len(unique_sections) - 1 else 0
        RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", depth)
        
        # Add baseline EQ to all sections
        RPR.RPR_TrackFX_AddByName(child_track, "ReaEQ", False, -1)
        
        # Distinguish sections by volume and specific FX processing
        if sec_name == "Verse":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 0.7)  # Tame, quiet
        elif sec_name == "Pre-Chorus":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 0.85) # Building energy
        elif sec_name == "Chorus":
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "D_VOL", 1.0)  # Full power
            # Add saturation to make the chorus pop
            RPR.RPR_TrackFX_AddByName(child_track, "JS: Saturation", False, -1)
            
        track_refs[sec_name] = child_track

    # === Step 3: Layout Arrangement with Crossfades ===
    # Dynamically generate 4-bar sections up to the requested 'bars' limit
    sections_layout = []
    current_bar = 1
    cycle_idx = 0
    
    while current_bar <= bars:
        sec_name = unique_sections[cycle_idx % len(unique_sections)]
        len_bars = min(4, bars - current_bar + 1)
        if len_bars <= 0:
            break
            
        sections_layout.append({"name": sec_name, "start_bar": current_bar, "len_bars": len_bars})
        current_bar += len_bars
        cycle_idx += 1
    
    beats_per_bar = 4
    crossfade_len = 0.05 # 50ms overlap to ensure seamless transitions
    
    for i, sec in enumerate(sections_layout):
        track = track_refs[sec["name"]]
        start_sec = (60.0 / bpm) * beats_per_bar * (sec["start_bar"] - 1)
        length_sec = (60.0 / bpm) * beats_per_bar * sec["len_bars"]
        
        is_first = (i == 0)
        is_last = (i == len(sections_layout) - 1)
        
        item_len = length_sec
        # Extend item length slightly to overlap with the next section
        if not is_last:
            item_len += crossfade_len 
            
        # Create a placeholder MIDI item to represent the section's audio
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_sec, start_sec + item_len, False)
        
        # Apply fades: Because they sum to the same parent bus, concurrent 
        # fade-outs and fade-ins mathematically create a perfect crossfade.
        if not is_first:
            RPR.RPR_SetMediaItemInfo_Value(item, "D_FADEINLEN", crossfade_len)
        if not is_last:
            RPR.RPR_SetMediaItemInfo_Value(item, "D_FADEOUTLEN", crossfade_len)
            
        # Give the region a visible name
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", f"{sec['name']} Region", True)
        
    return f"Created Sectional Submix Architecture ('{track_name}') mapping {len(sections_layout)} sections over {bars} bars at {bpm} BPM."
```