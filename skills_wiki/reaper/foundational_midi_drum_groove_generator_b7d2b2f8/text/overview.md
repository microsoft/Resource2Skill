### 1. High-level Design Pattern Extraction

> **Skill Name**: Foundational MIDI Drum Groove Generator

* **Core Musical Mechanism**: The video demonstrates a user exploring virtual instruments and algorithmic sequencers (Massive X, Reason Rack's Beat Map, Kong, and Redrum) specifically to generate and sequence drum sounds (kicks, hip-hop kits). Because these are third-party tools that rely on proprietary libraries, the core reusable pattern extracted here is the **algorithmic generation of standard drum MIDI sequences**. This skill generates the rhythmic skeleton (Kick, Snare, Hi-hat) using standard General MIDI notes, serving as the foundational trigger data for any drum VSTi.
* **Why Use This Skill (Rationale)**: Establishing a groove is often the first step in beat-making. A generated MIDI skeleton bypasses tedious manual sequencing. By applying velocity variations (e.g., softer off-beat hi-hats) and syncopation (like the pushed kick in a boom-bap beat), the generated MIDI inherently contains "groove theory" rather than just static, robotic hits.
* **Overall Applicability**: This is the starting point for electronic, hip-hop, or pop music production. It provides an instant rhythm track that can be used to audition drum sounds (as the user was attempting to do with Massive X and Kong) or serve as a metronome while tracking other instruments. 
* **Value Addition**: Compared to an empty track, this skill encodes rhythmic formulas (boom-bap vs. four-on-the-floor) and standard MIDI drum mapping, immediately providing a musical context for sound design.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: Configurable (defaults to 90 BPM, suitable for the hip-hop style kits explored in the video).
  - **Grid**: 1/4 notes for standard kicks/snares, 1/8th notes for hi-hats and syncopated kicks. 
  - **Groove**: Implements velocity accenting (downbeats are harder, upbeats are softer) to provide a natural feel.
* **Step B: Pitch & Harmony**
  - **Pitches**: Unpitched, utilizing General MIDI (GM) standard drum note mapping.
  - Kick = MIDI Note 36 (C1)
  - Acoustic Snare = MIDI Note 38 (D1)
  - Closed Hi-Hat = MIDI Note 42 (F#1)
* **Step C: Sound Design & FX**
  - The script generates standard MIDI. To hear it, the user simply drops their preferred drum VSTi (like Reason Rack or a stock ReaSamplOmatic5000 kit) onto the created track.
* **Step D: Mix & Automation**
  - N/A for this foundational MIDI generation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Drum Sequencing | `RPR_MIDI_InsertNote` | Provides exact programmatic control over note placement, duration, and velocity, mimicking the output of algorithmic sequencers like Reason's "Beat Map". |
| Timing Calculation | `RPR_TimeMap2_QNToTime` & `RPR_MIDI_GetPPQPosFromProjTime` | Ensures notes are perfectly locked to the musical grid (Quarter Notes) regardless of the project's internal resolution or tempo map. |

> **Feasibility Assessment**: 80% — The code perfectly reproduces the *output intent* of the tools used in the video (a sequenced drum beat). However, because the specific third-party plugins (Massive X, Reason Studios) and their proprietary sample libraries are not available in a vanilla REAPER installation, the script relies on generating standardized MIDI that is ready to trigger whichever VSTi the user chooses to load.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Drum Sequencer",
    bpm: int = 90,
    key: str = "C",      # Unused (drums are unpitched)
    scale: str = "major",# Unused
    bars: int = 4,
    velocity_base: int = 100,
    style: str = "boom_bap", # Options: 'boom_bap' or 'four_on_floor'
    **kwargs,
) -> str:
    """
    Create a Foundational MIDI Drum Groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM.
        key: Unused for GM drums.
        scale: Unused for GM drums.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        style: The rhythmic style of the beat ('boom_bap' or 'four_on_floor').
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # General MIDI standard mapping
    KICK = 36
    SNARE = 38
    HAT_CLOSED = 42

    notes_created = 0

    # === Step 4: Generate Rhythm Based on Style ===
    for bar in range(bars):
        bar_start_qn = bar * 4.0

        if style == "four_on_floor":
            # Kicks on every downbeat (1, 2, 3, 4)
            for beat in range(4):
                start_qn = bar_start_qn + beat
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, velocity_base, False)
                notes_created += 1

            # Snares/Claps on 2 and 4
            for beat in [1, 3]:
                start_qn = bar_start_qn + beat
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
                notes_created += 1

            # Driving 8th note Hi-Hats with velocity accenting
            for eighth in range(8):
                start_qn = bar_start_qn + (eighth * 0.5)
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Downbeats hit harder than offbeats
                vel = velocity_base if eighth % 2 == 0 else max(10, velocity_base - 25)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, HAT_CLOSED, vel, False)
                notes_created += 1

        elif style == "boom_bap" or style != "four_on_floor":
            # Syncopated Kicks: 1, 2.5 (the "and" of 2), and 3
            kick_qns = [0.0, 1.5, 2.0]
            for kq in kick_qns:
                start_qn = bar_start_qn + kq
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Ghost note velocity for the syncopated kick
                vel = velocity_base if kq != 1.5 else max(10, velocity_base - 15)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, vel, False)
                notes_created += 1

            # Backbeat Snares on 2 and 4
            for sq in [1.0, 3.0]:
                start_qn = bar_start_qn + sq
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
                notes_created += 1

            # 8th note Hi-Hats with heavy velocity variation for groove
            for eighth in range(8):
                start_qn = bar_start_qn + (eighth * 0.5)
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.125)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                vel = velocity_base if eighth % 2 == 0 else max(10, velocity_base - 35)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, HAT_CLOSED, vel, False)
                notes_created += 1

    # Commit MIDI changes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} GM drum notes (style: {style}) over {bars} bars at {bpm} BPM"
```