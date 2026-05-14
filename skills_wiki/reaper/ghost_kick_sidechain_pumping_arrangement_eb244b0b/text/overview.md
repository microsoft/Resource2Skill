### 1. High-level Design Pattern Extraction

**Skill Name**: Ghost Kick Sidechain Pumping Arrangement

* **Core Musical Mechanism**: The tutorial highlights a fundamental EDM/House arrangement technique: separating the *audible* kick drum from the *sidechain trigger* kick. By duplicating the kick track and routing it *only* to a compressor's sidechain (disabling its master send), you create a "Ghost Kick". This creates a rhythmic 1/4-note volume ducking (pumping) effect on synths and basses that persists even during quiet intros or verses where the main kick drum is muted.
* **Why Use This Skill (Rationale)**: Constant 4-on-the-floor kick drums can cause ear fatigue. Arrangers often drop the drums out during a verse to create a dynamic contrast before the chorus/drop. However, entirely removing the ducking groove makes the track lose its "dance" feel. The Ghost Kick allows the mix to remain deeply rhythmic and pumping, providing a subconscious groove even when the arrangement is stripped back.
* **Overall Applicability**: Essential for Electronic Dance Music, House, Lo-Fi, and Pop. Used specifically for transitions, breakdowns, intros, and verses where you want rhythmic energy without heavy percussion. 
* **Value Addition**: This skill encodes complex DAW routing (disabling Master send, configuring 4-channel track audio, sidechain MIDI routing, and ReaComp detector parameter tuning) into a single, composable setup.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Typically 120-128 BPM (House/EDM standard).
  - **Trigger Rhythm**: A persistent 4-on-the-floor pattern (1/4 notes) running continuously.
  - **Target Rhythm**: Sustained legato chords or long bass notes to clearly showcase the volume pumping.

* **Step B: Pitch & Harmony**
  - **Ghost Kick**: A low transient note (e.g., C2 / MIDI 36). Pitch doesn't strictly matter as it is muted, but it triggers the compressor.
  - **Target Instrument**: A lush, wide chord (e.g., C Minor triad) held over multiple bars to emphasize the dynamic ducking.

* **Step C: Sound Design & FX**
  - **Trigger (Ghost Kick)**: ReaSynth playing a short, punchy sine wave. 
  - **Target (Chords)**: ReaSynth playing a square/saw wave pad.
  - **FX Chain (ReaComp)**: Added to the target track. 
    - *Threshold*: Low (-25dB)
    - *Ratio*: Aggressive (4:1 or 6:1)
    - *Attack*: Fast (~2ms)
    - *Release*: Synced to tempo, usually ~150ms for a breathing pump.
    - *Detector Input*: Set to Auxiliary L+R (Channels 3/4).

* **Step D: Mix & Automation**
  - **Master Send**: The Ghost Kick track has `B_MAINSEND` set to `0` (muted from the master bus).
  - **Track Send**: Audio routed from Ghost Kick channels 1/2 to Target Track channels 3/4.
  - Target Track requires `I_NCHAN` set to 4 to receive the sidechain signal.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arrangement Tracks | `RPR_InsertTrackAtIndex` | Creates the isolated Trigger and Target tracks non-destructively. |
| Invisible Trigger | `B_MAINSEND` = 0 | Mutes the Ghost Kick from the master output exactly as described in the tutorial. |
| Sidechain Routing | `RPR_CreateTrackSend` | Automatically pipes the trigger signal to Channels 3/4 of the target track. |
| Pumping Effect | `RPR_TrackFX_SetParam` | Configures ReaComp's threshold, ratio, and crucially, the Detector Input (Aux L+R). |
| Musical Data | `RPR_MIDI_InsertNote` | Generates the 4-on-the-floor trigger and the sustained target chords dynamically based on key/scale. |

> **Feasibility Assessment**: 100% reproducible. The routing, sidechain compression, and MIDI relationships described in the video can be entirely reconstructed using REAPER's native ReaScript API and stock ReaComp/ReaSynth plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping_Chords",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Ghost Kick Sidechain Pumping Arrangement in the current REAPER project.
    Generates a muted 4-on-the-floor trigger track that pumps a sustained chord progression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created target track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10]
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)

    # === Step 1: Create Target Track (The audible chords) ===
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    target_tr = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(target_tr, "P_NAME", track_name, True)
    # Give track 4 channels so it can receive sidechain audio on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(target_tr, "I_NCHAN", 4) 

    # === Step 2: Create Trigger Track (The Ghost Kick) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    ghost_tr = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_tr, "P_NAME", f"Ghost Kick (Trigger)", True)
    # Crucial: Disable master send so the kick isn't heard
    RPR.RPR_SetMediaTrackInfo_Value(ghost_tr, "B_MAINSEND", 0) 

    # === Step 3: Configure Audio Routing ===
    # Send from Ghost Kick to Target Track
    send_idx = RPR.RPR_CreateTrackSend(ghost_tr, target_tr)
    # Set Destination to Channels 3/4 (Value '2' translates to Ch 3/4 in REAPER API)
    RPR.RPR_SetTrackSendInfo_Value(ghost_tr, 0, send_idx, "I_DSTCHAN", 2) 

    # === Step 4: MIDI Generation ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    total_len = bar_len * bars

    # Create sustained Chords MIDI item
    target_item = RPR.RPR_CreateNewMIDIItemInProj(target_tr, 0.0, total_len, False)
    target_take = RPR.RPR_GetActiveTake(target_item)
    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, 0.0)
    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, total_len)

    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # e.g., C3 = 48
    chord_notes = [
        root_midi,
        root_midi + scale_intervals[2 % len(scale_intervals)],
        root_midi + scale_intervals[4 % len(scale_intervals)],
        root_midi + 12 # Octave
    ]

    # Insert long notes covering the whole item
    for n in chord_notes:
        RPR.RPR_MIDI_InsertNote(target_take, False, False, ppq_start, ppq_end, 0, n, velocity_base - 20, False)

    # Create 4-on-the-floor Ghost Kick MIDI item
    ghost_item = RPR.RPR_CreateNewMIDIItemInProj(ghost_tr, 0.0, total_len, False)
    ghost_take = RPR.RPR_GetActiveTake(ghost_item)

    total_beats = bars * beats_per_bar
    for b in range(total_beats):
        pos_sec = b * (60.0 / bpm)
        p_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, pos_sec)
        p_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(ghost_take, pos_sec + 0.1) # Short percussive trigger
        RPR.RPR_MIDI_InsertNote(ghost_take, False, False, p_start, p_end, 0, 36, 127, False)

    # === Step 5: Sound Design & Sidechain FX ===
    # Target Pad FX
    t_synth = RPR.RPR_TrackFX_AddByName(target_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(target_tr, t_synth, 1, 0.4) # Introduce square wave for lush tone
    RPR.RPR_TrackFX_SetParamNormalized(target_tr, t_synth, 4, 0.8) # Long release

    # Target Sidechain Compressor
    t_comp = RPR.RPR_TrackFX_AddByName(target_tr, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(target_tr, t_comp, 0, -28.0) # Param 0: Threshold (dB)
    RPR.RPR_TrackFX_SetParam(target_tr, t_comp, 1, 5.0)   # Param 1: Ratio
    RPR.RPR_TrackFX_SetParam(target_tr, t_comp, 2, 2.0)   # Param 2: Attack (ms)
    RPR.RPR_TrackFX_SetParam(target_tr, t_comp, 3, 120.0) # Param 3: Release (ms) - tuned for pumping groove
    RPR.RPR_TrackFX_SetParam(target_tr, t_comp, 10, 1.0)  # Param 10: Detector Input -> set to 'Auxiliary L+R'

    # Trigger Synth (Doesn't need to sound good, just needs a clean transient)
    g_synth = RPR.RPR_TrackFX_AddByName(ghost_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(ghost_tr, g_synth, 1, 0.0) # Pure Sine
    RPR.RPR_TrackFX_SetParamNormalized(ghost_tr, g_synth, 3, 0.0) # Fast Decay

    return f"Created '{track_name}' and invisible 'Ghost Kick' track sidechain arrangement for {bars} bars at {bpm} BPM in {key} {scale}."
```