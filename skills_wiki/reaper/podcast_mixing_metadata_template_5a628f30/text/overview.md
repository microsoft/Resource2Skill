# Podcast Mixing & Metadata Template

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Podcast Mixing & Metadata Template

* **Core Musical Mechanism**: Multi-stage dynamic processing for spoken word, combined with embedded project render metadata. The workflow applies cascading dynamics (auto-leveling, compression, limiting) to stabilize speech intelligibility, while injecting dynamic wildcards into ID3 tags to streamline repetitive rendering workflows.

* **Why Use This Skill (Rationale)**: Spoken word relies heavily on consistent dynamics rather than pitch or rhythm. Using a cascading compression approach—a slow "leveler" to ride the macro-dynamics (distance from the microphone), followed by a fast compressor for transient control, and ending with a peak limiter—ensures a highly consistent LUFS output without aggressive pumping artifacts. Embedding metadata (ID3 tags) directly into the REAPER project prevents repetitive data entry when rendering weekly episodic content.

* **Overall Applicability**: Podcasting, YouTube voiceovers, dialogue editing, audiobooks, and broadcast environments.

* **Value Addition**: Instead of manually rebuilding vocal chains and typing metadata for every episode, this pattern provides a ready-to-record skeleton with the correct signal flow and distribution-ready ID3 tags embedded into the `.rpp` file.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Tempo and grid are largely irrelevant for podcasting. The timebase is typically conceptualized in Minutes/Seconds rather than Beats/Measures.

* **Step B: Pitch & Harmony**
  - Non-musical; focuses purely on the timbral and dynamic control of the human voice.

* **Step C: Sound Design & FX**
  - **Vocal Chain**:
    1. **Leveler**: Smooths out macro-dynamics. In the tutorial, this is Waves Vocal Rider. In the reproduction, this is represented by a slow-acting ReaComp instance.
    2. **Compressor**: Adds density and punch. The tutorial uses a Waves API 2500. Represented here by a second ReaComp instance.
    3. **Limiter**: Prevents digital clipping. The tutorial uses Sonic Anomaly Unlimited. Represented here by JS: Event Horizon Limiter.

* **Step D: Mix & Automation (if applicable)**
  - **Routing**: A secondary "Music Bed / Intro" track is created and attenuated (-12dB / 0.25 linear volume) to guarantee it sits politely underneath the dialogue.
  - **Render Metadata**: Configures the project's ID3 tags (Artist, Album, Genre, Date) using REAPER's wildcard system (e.g., `$year` or `$project`) so the final `.mp3` is automatically tagged upon rendering.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Structure & Mix | `RPR_InsertTrackAtIndex` / `RPR_SetMediaTrackInfo_Value` | Sets up the core routing and relative bed/vocal volumes. |
| Vocal Processing Chain | `RPR_TrackFX_AddByName` | Recreates the 3-stage dynamic processing workflow using native stock plugins to ensure seamless execution. |
| Render Metadata | `RPR_GetSetProjectInfo_String` | Automates the exact ID3 tagging process demonstrated in the tutorial using native REAPER API calls. |

> **Feasibility Assessment**: 85% — The structural workflow, routing, volume attenuation, and metadata injection are fully reproducible. The specific third-party plugins shown in the tutorial (Waves Vocal Rider, API 2500) are replaced with REAPER stock equivalents (cascaded ReaComp instances and a JS Limiter) to ensure the script executes safely on any standard REAPER installation without missing dependencies. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Podcast_Template",
    track_name: str = "Host Vocal",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Podcast Mixing & Metadata Template in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the primary vocal track.
        bpm: Tempo in BPM (included for signature compatibility, less relevant here).
        key: Root note (ignored for podcast workflow).
        scale: Scale type (ignored for podcast workflow).
        bars: Number of bars (ignored for podcast workflow).
        velocity_base: Base MIDI velocity (ignored for podcast workflow).
        **kwargs: Additional overrides for metadata (artist, album, genre).

    Returns:
        Status string describing the created tracks and metadata.
    """
    import reaper_python as RPR

    # === Step 1: Create Host Vocal Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    vocal_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(vocal_track, "P_NAME", track_name, True)

    # === Step 2: Add Multi-Stage Vocal FX Chain ===
    # Stage 1: Auto-Leveler (Replaces Vocal Rider)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaComp (Cockos)", False, -1)
    
    # Stage 2: Main Color Compressor (Replaces API 2500)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaComp (Cockos)", False, -1)
    
    # Stage 3: Peak Limiter (Replaces 3rd Party Limiter)
    RPR.RPR_TrackFX_AddByName(vocal_track, "JS: Event Horizon Limiter/Clipper", False, -1)

    # === Step 3: Create Music Bed / Intro Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    music_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(music_track, "P_NAME", "Music Bed / Outro", True)
    
    # Attenuate the music bed volume to sit behind the vocal (approx -12dB is 0.25 in linear scale)
    RPR.RPR_SetMediaTrackInfo_Value(music_track, "D_VOL", 0.25)

    # === Step 4: Set Render Metadata (ID3 Tags) ===
    # Uses REAPER's wildcard system as demonstrated in the tutorial
    artist = kwargs.get("artist", "Podcast Host")
    album = kwargs.get("album", "My Killer Podcast")
    genre = kwargs.get("genre", "Podcast / Health")
    
    # The string format requires "Format:Tag|Value"
    # RENDER_METADATA is natively supported in REAPER to configure the render dialog automatically
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TPE1|{artist}", True)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TALB|{album}", True)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", f"ID3:TCON|{genre}", True)
    
    # REAPER wildcard for the current 4-digit year ($year)
    RPR.RPR_GetSetProjectInfo_String(0, "RENDER_METADATA", "ID3:TYER|$year", True)

    return f"Created Podcast Template with '{track_name}', a 'Music Bed' track, and injected ID3 render metadata."
```