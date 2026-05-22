# Synthwave Pop Arrangement Structure

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Synthwave Pop Arrangement Structure

* **Core Musical Mechanism**: The "Rollercoaster" Energy Profile over a strict 8-bar block grid. This pattern maps out a song into distinct 8-bar and 16-bar sections that gradually increase in overall energy as the song progresses. The defining characteristic is the offset dips in energy—each verse or bridge drops the energy down from the preceding chorus, but *never as low as the previous verse*. For example, Verse 1 has no drums, but Verse 2 introduces a drum groove, ensuring the song's momentum constantly moves forward.

* **Why Use This Skill (Rationale)**: This structure satisfies deeply ingrained listener expectations derived from 80s pop and cinematic synth soundtracks. It prevents a track from feeling like an aimless "8-bar loop" by creating explicit tension (verses/build-ups) and release (choruses). The "8-bar rule" aligns perfectly with hyper-symmetrical Western musical phrasing, making it easy for listeners to anticipate structural changes and feel the groove.

* **Overall Applicability**: This arrangement blueprint is essential for Synthwave, Retrowave, Pop-EDM, and any vocal-centric electronic music that relies on traditional pop songwriting structures rather than EDM "Build/Drop" structures. 

* **Value Addition**: Instead of a blank project, this skill provides a complete macroscopic timeline blueprint. It encodes the pacing and energy dynamics of a full 96-bar track into colored DAW regions and placeholder items, telling the producer exactly where to add or remove elements (like drums, solos, or thick chord stacks).


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM Range**: Typically 90-120 BPM.
  - **Time Signature**: 4/4 time.
  - **Phrasing**: Strictly adheres to the "8-bar rule". Every section is either 8 bars, or a multiple of 8 (e.g., 16-bar choruses). 

* **Step B: Pitch & Harmony (Structural Context)**
  - **Verses**: Typically sit on the tonic or a looping 4-bar progression.
  - **Pre-Chorus**: Harmonic rhythm speeds up to create tension.
  - **Choruses**: Full, wide chord voicings (e.g., dense saw pads).
  - **Bridge**: Often shifts to the relative major/minor or introduces chromatic mode mixture to provide a stark contrast before the final chorus.

* **Step C: Sound Design & FX (Energy Mapping)**
  - **Verse 1**: Sparse. Bassline, maybe a light pad/arpeggio, NO main drums (maybe just a kick or snap).
  - **Pre-Chorus**: Sweeps, risers, and drum fills added to build tension. 
  - **Chorus**: Full frequency spectrum. Heavy snare/kick, thick wide pads, lead melodies.
  - **Verse 2**: Same as Verse 1, but *with* a basic drum beat to maintain the new baseline energy.
  - **Chorus 2 (Double)**: 16 bars. The second half often introduces a new element, like a saxophone solo or a synth lead solo.

* **Step D: Mix & Automation**
  - Volume automation typically pushes the master bus or instrument busses up by 1-2dB during the Choruses to make them "pop".
  - Low-pass filter sweeps are frequently used during Intro and Pre-Chorus sections to muffle the sound before opening up wide at the Chorus boundary.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Song Arrangement Layout | Empty Media Items | Provides distinct, selectable blocks on a timeline that visually represent structural timing. |
| Section Naming & Navigation | Project Regions | Allows the agent/user to instantly jump to different parts of the song (e.g., Chorus 2 vs Bridge) and see the structure globally. |
| Energy Level Mapping | Item & Region Colors | Visual color coding (cool colors for low energy, hot colors for high energy) translates the abstract "rollercoaster" concept into DAW data. |

> **Feasibility Assessment**: 100% of the structural layout and timing strategy from the tutorial is reproduced. Because this tutorial is strictly about macro-level song arrangement rather than specific notes or synthesizer patches, the code generates an Arrangement Guide Track rather than audio, which serves as a necessary scaffolding for generating further musical elements.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Synthwave_Pop",
    track_name: str = "Arrangement Guide",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 96,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete Synthwave Pop Arrangement template in the current REAPER project.
    Generates colored empty media items and Project Regions to map out the "Rollercoaster" 
    energy structure detailed in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created arrangement guide track.
        bpm: Tempo in BPM.
        key: Root note (ignored for structure, kept for signature).
        scale: Scale type (ignored for structure, kept for signature).
        bars: Total bars (overridden by the fixed 96-bar pop structure).
        velocity_base: Base MIDI velocity (ignored for structure).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing the structure created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Define the Synthwave Pop Structure ===
    # Format: (Section Name, Length in Bars, R, G, B)
    # Colors represent energy: Blues/Cool = Low Energy, Purples = Medium, Reds/Oranges = High Peak Energy
    structure = [
        ("Intro",                   8,  50,  50, 150),  # Low energy
        ("Verse 1 (No Drums)",      8,  50, 100, 150),  # Low energy
        ("Pre-Chorus 1",            8, 100,  50, 150),  # Tension building
        ("Chorus 1",                8, 200,  50,  50),  # First Peak
        ("Verse 2 (Drums In)",      8,  50, 150, 150),  # Energy dips, but higher than V1
        ("Pre-Chorus 2",            8, 150,  50, 150),  # Tension building
        ("Chorus 2 (Double/Solo)", 16, 220,  50,  50),  # Second Peak (Longer, features solo)
        ("Bridge",                  8, 100, 100, 200),  # Harmonic shift / Energy dip
        ("Chorus 3 (Max Energy)",  16, 255,   0,   0),  # Final Climax
        ("Outro",                   8,  50,  50,  50)   # Energy decay
    ]

    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar

    # === Step 3: Create Arrangement Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    current_bar = 0

    # === Step 4: Populate Timeline with Regions and Blocks ===
    for name, length_bars, r, g, b in structure:
        start_time = current_bar * sec_per_bar
        end_time = (current_bar + length_bars) * sec_per_bar

        # 4a. Add Empty Media Item as a placeholder block
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_bars * sec_per_bar)

        # Convert RGB to REAPER's native custom color format (r + g*256 + b*65536 | 0x1000000 flag)
        native_color = int(r + (g * 256) + (b * 65536)) | 0x1000000
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", native_color)

        # 4b. Add Take and Name it so it displays on the item
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", name, True)

        # 4c. Add Project Region for global DAW navigation
        # AddProjectMarker2(proj, isrgn, pos, rgnend, name, wantidx, color)
        RPR.RPR_AddProjectMarker2(0, True, start_time, end_time, name, -1, native_color)

        current_bar += length_bars

    # Update REAPER UI to show the new items and regions
    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' and Project Regions mapping a {current_bar}-bar Synthwave Pop structure at {bpm} BPM."
```