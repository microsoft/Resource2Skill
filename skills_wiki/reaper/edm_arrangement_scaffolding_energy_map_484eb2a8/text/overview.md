# EDM Arrangement Scaffolding & Energy Map

## Analysis

# Role: Agent_Skill_Distiller (REAPER Music Production Pattern Extractor)

## 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Arrangement Scaffolding & Energy Map

* **Core Musical Mechanism**: The foundation of modern electronic dance music (EDM) is macro-arrangement using an "Energy Map." Rather than building a track loop by loop, producers plot an emotional roller-coaster across 8-bar and 16-bar phrases (Intro → Verse → Build → Drop → Break → Build → Drop 2 → Outro). This skill generates visual arrangement blocks and automates a volume/energy envelope on a dummy track to serve as a tension/release blueprint for the rest of the production.
* **Why Use This Skill (Rationale)**: The tutorial emphasizes that taking an 8-bar loop to a full track requires guiding the listener on a journey. Creating high-energy "Drops" requires the context of lower-energy "Verses" and tension-ramping "Build-ups." By scaffolding the arrangement and physically drawing an energy map (automation curve) first, producers encode the song's pacing, contrast, and dramatic structure before writing individual instrument parts. 
* **Overall Applicability**: This is the universal blueprint for almost all subgenres of EDM (Slap House, Future Rave, Pop House, Trap). It solves the "stuck in a loop" syndrome by giving the producer empty, labeled buckets to drop their loops into, and a visual guide indicating exactly how dense or loud those buckets should be.
* **Value Addition**: Compared to a blank project, this skill provides a complete, industry-standard song skeleton. It pre-calculates structural timing, names all sections, sets up navigation markers, and draws the psychological tension curve (Energy Map) that dictates arrangement density.

## 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically 120-128 BPM.
  - **Section Phrasing**: Music is built in multiples of 4 bars. Standard EDM sections are mostly 16 bars (Intro, Verse, Drop, Outro) or 8 bars (Build-ups).
  - **The Journey**: The transition between sections is crucial. Build-ups require exponential tension (snare rolls, riser synths, filters opening), followed by the Drop, which provides massive harmonic and sub-bass resolution.

* **Step B: Pitch & Harmony**
  - While this pattern applies to any key, the arrangement dictates harmonic density. Verses often strip back to just chords and vocals, while Drops feature full-spectrum frequency layering (Sub bass + Mid bass + Lead Synth + Full Drums).
  - The "Post-Drop" (the second half of a Drop or Drop 2) is often the harmonic and timbral climax of the track.

* **Step C: Sound Design & FX**
  - In the video, Will explicitly uses a dummy track with a gain plugin to "draw" the energy.
  - We replicate this by using the REAPER track Volume envelope, treating it purely as a visual "Energy Level" curve (0.0 = silence/lowest energy, 1.0 = maximum drop energy).

* **Step D: Mix & Automation**
  - **Energy Mapping curve**:
    - *Intro*: Low, flat energy (20-30%).
    - *Verse 1*: Slight rise in energy as elements are introduced (30-40%).
    - *Build 1*: Exponential ramp (40% to 90%).
    - *Drop 1*: Instant jump to high energy, trailing off slightly (100% to 85%).
    - *Verse 2 / Break*: Drops back down to provide contrast, but often stays slightly more energetic than Verse 1 (35-50%).
    - *Build 2*: Exponential ramp (50% to 95%).
    - *Drop 2*: Climax, sustaining max energy (100%).

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Section Blocks | Empty MIDI Items (`RPR_CreateNewMIDIItemInProj`) | Acts as visual, color-coded "buckets" for the arrangement without emitting sound. |
| Arrangement Navigation | Project Markers (`RPR_AddProjectMarker`) | Allows the producer/agent to easily jump between song sections (Verse, Drop, etc.). |
| Energy Map | Track Volume Envelope (`RPR_GetTrackEnvelopeByName`) | Perfectly replicates the video's technique of drawing an automation curve to visualize track tension. |

> **Feasibility Assessment**: 100% — While we cannot auto-generate a Grammy-winning David Guetta vocal and bassline from thin air, we *can* perfectly reproduce the macro-arrangement strategy, structure blocks, and energy mapping technique Will demonstrates.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Energy Map & Structure",
    bpm: int = 126,
    key: str = "C",
    scale: str = "minor",
    bars: int = 104,  # Overridden by structural math
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an industry-standard EDM arrangement scaffold with an automated Energy Map.
    Inserts labeled, color-coded block items, project markers, and an automation curve 
    representing the track's tension/release journey.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created structure track.
        bpm: Tempo in BPM.
        key: Root note (unused directly, but fits signature).
        scale: Scale type (unused directly, but fits signature).
        bars: Total duration (managed internally by sections).
        velocity_base: Unused for arrangement.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Initialize Tempo & Math ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # Helper function to generate safe OS-native colors
    def make_color(r, g, b):
        return int(r + (g << 8) + (b << 16) | 0x1000000)

    # Standard EDM Arrangement Journey (Length in bars, Energy 0.0 - 1.0)
    sections = [
        {"name": "Intro",   "bars": 16, "e_start": 0.20, "e_end": 0.30, "color": make_color(50, 150, 200)},  # Blue
        {"name": "Verse 1", "bars": 16, "e_start": 0.30, "e_end": 0.40, "color": make_color(50, 200, 50)},   # Green
        {"name": "Build 1", "bars": 8,  "e_start": 0.40, "e_end": 0.90, "color": make_color(220, 200, 50)},  # Yellow
        {"name": "Drop 1",  "bars": 16, "e_start": 1.00, "e_end": 0.85, "color": make_color(250, 50, 50)},   # Red
        {"name": "Verse 2", "bars": 16, "e_start": 0.35, "e_end": 0.50, "color": make_color(50, 200, 50)},   # Green
        {"name": "Build 2", "bars": 8,  "e_start": 0.50, "e_end": 0.95, "color": make_color(220, 200, 50)},  # Yellow
        {"name": "Drop 2",  "bars": 16, "e_start": 1.00, "e_end": 0.90, "color": make_color(250, 50, 50)},   # Red
        {"name": "Outro",   "bars": 16, "e_start": 0.50, "e_end": 0.00, "color": make_color(100, 100, 100)}  # Grey
    ]

    # === Step 2: Create Structure Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup Energy Map (Volume Envelope) ===
    # Select only the new track and make the volume envelope visible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Command: "Track: Toggle track volume envelope visible"
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    current_time = 0.0
    marker_idx = 1
    
    # === Step 4: Scaffold the Track ===
    for sec in sections:
        sec_len_sec = sec["bars"] * bar_length_sec

        # A. Insert Navigation Marker
        RPR.RPR_AddProjectMarker(0, False, current_time, 0, sec["name"], marker_idx)
        marker_idx += 1

        # B. Insert Structural Block (Empty MIDI Item)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, current_time, current_time + sec_len_sec, False)
        
        # Colorize the item based on energy/function
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", sec["color"])
        
        # Name the item take to display the section name
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", sec["name"], True)

        # C. Draw the Energy Curve (Volume Automation)
        if env:
            # RPR_InsertEnvelopePoint params: env, time, value, shape, tension, selected, noSort
            # shape 0 = Linear (perfect for mapping builds and fades)
            RPR.RPR_InsertEnvelopePoint(env, current_time, sec["e_start"], 0, 0, False, True)
            RPR.RPR_InsertEnvelopePoint(env, current_time + sec_len_sec - 0.001, sec["e_end"], 0, 0, False, True)

        current_time += sec_len_sec

    # Sort envelope points to ensure proper display
    if env:
        RPR.RPR_Envelope_SortPoints(env)

    total_bars_created = sum(s["bars"] for s in sections)
    return f"Created EDM Arrangement Scaffold: {len(sections)} sections ({total_bars_created} bars) at {bpm} BPM with Energy Map curve."
```