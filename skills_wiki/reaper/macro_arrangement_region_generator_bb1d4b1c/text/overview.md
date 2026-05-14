# Macro-Arrangement Region Generator

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Macro-Arrangement Region Generator

* **Core Musical Mechanism**: Automating song structuring using timeline visualizer blocks (Regions). The pattern establishes a macro-level harmonic and dynamic roadmap—such as Intro, Verse, Pre-Chorus, Chorus, Bridge, and Outro—color-coded by section energy. 
* **Why Use This Skill (Rationale)**: The tutorial demonstrates how REAPER's "Regions" feature allows producers to click and drag entire sections of a song. Musically, a track requires dynamic contour (tension and release over time). Setting up a region skeleton provides a visual grid for this contour. Because moving a region in REAPER automatically moves all enclosed audio, MIDI, and tempo tracks, establishing this skeleton early allows for rapid iteration of a song's macro-arrangement (e.g., easily deciding to halve the length of a Verse or double a Chorus).
* **Overall Applicability**: Essential for pre-production, demoing, and structuring in almost all grid-based modern music (Pop, EDM, Rock, Hip-Hop). It acts as a blank canvas with guardrails, preventing the "8-bar loop trap" by forcing the producer to see the entire song's layout from the beginning.
* **Value Addition**: Instead of manually selecting an area and pressing `Shift+R` for every section as shown in the video, this skill procedurally generates a complete, industry-standard song structure in one click, mapping out exact bar lengths and assigning distinct colors for quick visual identification.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: Configurable (e.g., 120 BPM).
  - **Grid Divisions**: Macro scale (measured in full bars).
  - **Arrangement Blocks**: 
    - Intro (4 Bars)
    - Verse 1 (8 Bars)
    - Pre-Chorus (4 Bars)
    - Chorus 1 (8 Bars)
    - Verse 2 (8 Bars)
    - Chorus 2 (8 Bars)
    - Bridge (8 Bars)
    - Chorus 3 (8 Bars)
    - Outro (4 Bars)

* **Step B: Pitch & Harmony**
  - N/A for the timeline markers themselves, though these sections usually correspond to distinct functional harmony changes (e.g., Verse on Tonic, Bridge on Subdominant/Relative Minor).

* **Step C: Sound Design & FX**
  - Timeline organization and UI visual feedback via color coding (e.g., High-energy Choruses are bright Red, Verses are Green, Intros/Outros are Blue/Grey).

* **Step D: Mix & Automation**
  - Regions encapsulate all underlying track automations (like tempo maps and volume envelopes). Moving the region moves the automation with it.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Creating Sections | `RPR_AddProjectMarker2` (with `isrgn=True`) | Native API method to construct REAPER timeline Regions, capturing the exact workflow demonstrated. |
| Color Coding | Bitwise RGB integer calculation | Differentiates song sections visually, just as a producer would do manually in the Region Edit dialog. |
| Additive Foundation | `RPR_InsertTrackAtIndex` | Creates an empty "Arrangement/Scratch" track to hold upcoming demos/ideas beneath the regions. |

> **Feasibility Assessment**: 100% reproducible. The script bypasses the manual `Shift+R` and `Shift+Double Click` steps shown in the video by instantly injecting a parameterized, fully colored standard pop/rock arrangement skeleton directly into the project timeline.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Scratchpad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 60, # Total bars fallback
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Macro-Arrangement Region Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created underlying track.
        bpm: Tempo in BPM.
        key: Root note (unused natively in markers, but kept for signature).
        scale: Scale type (unused natively in markers, but kept for signature).
        bars: Total fallback length.
        velocity_base: Base MIDI velocity (unused here).
        **kwargs: Can accept a 'structure' list of tuples (Name, Bars, (R,G,B)).

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Define the Macro Arrangement Structure ===
    # Format: [("Section Name", Length_In_Bars, (R, G, B))]
    structure = kwargs.get("structure", [
        ("Intro",      4, (100, 150, 200)),  # Soft Blue
        ("Verse 1",    8, (150, 200, 100)),  # Green
        ("Pre-Chorus", 4, (200, 175,  50)),  # Orange/Yellow
        ("Chorus 1",   8, (220,  80,  80)),  # Red (High Energy)
        ("Verse 2",    8, (150, 200, 100)),  # Green
        ("Chorus 2",   8, (220,  80,  80)),  # Red
        ("Bridge",     8, (150, 100, 200)),  # Purple (Alternative harmonic center)
        ("Chorus 3",   8, (220,  80,  80)),  # Red
        ("Outro",      4, (100, 100, 100))   # Gray
    ])

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    current_time = 0.0

    # === Step 3: Generate the Timeline Regions ===
    for idx, section in enumerate(structure):
        name = section[0]
        section_bars = section[1]
        r, g, b = section[2]

        # REAPER Custom color bitwise logic: 0x1000000 | (B << 16) | (G << 8) | R
        color_int = 0x1000000 | (b << 16) | (g << 8) | r

        end_time = current_time + (section_bars * bar_length_sec)

        # Add Project Marker as Region (isrgn=True is the 2nd parameter)
        # RPR_AddProjectMarker2(proj, isrgn, pos, rgnend, name, wantidx, color)
        RPR.RPR_AddProjectMarker2(0, True, current_time, end_time, name, -1, color_int)

        current_time = end_time

    # === Step 4: Add an empty Scratchpad Track for pre-pro demoing ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    total_bars_created = sum(sec[1] for sec in structure)
    
    return f"Created {len(structure)} arrangement Regions ({total_bars_created} total bars) and track '{track_name}' at {bpm} BPM"
```