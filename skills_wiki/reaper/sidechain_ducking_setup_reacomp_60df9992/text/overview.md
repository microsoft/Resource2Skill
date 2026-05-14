# Sidechain Ducking Setup (ReaComp)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sidechain Ducking Setup (ReaComp)

* **Core Musical Mechanism**: Sidechain compression (often referred to as "ducking") is a dynamic processing technique where the volume of one track (the target) is automatically reduced by the presence of an audio signal from another track (the trigger). This is achieved by routing the trigger audio into an auxiliary input of the compressor on the target track, and telling the compressor to use that auxiliary input as its detection source.

* **Why Use This Skill (Rationale)**: Musically, sidechain ducking serves two primary purposes:
    1. **Frequency Masking / Mix Clarity**: It prevents two elements that share the same frequency range (like a kick drum and a sub-bass, or a voiceover and a backing track) from clashing. By quickly ducking the bass when the kick hits, the kick's transient punches through clearly.
    2. **Groove and Rhythmic Feel**: In EDM, future bass, and hip-hop, heavy, rhythmic sidechaining creates a signature "pumping" or "breathing" effect that glues the track to the drum groove, transforming static sustained sounds (like pads) into rhythmic elements.

* **Overall Applicability**: This technique is universally applied to duck basslines to kick drums in electronic music, to automatically lower music bed volumes during vocal broadcasts/podcasts, and to carve out space for lead vocals against thick rhythm guitars or synth pads.

* **Value Addition**: This skill encodes the specific REAPER routing architecture required for advanced sidechaining: creating auxiliary track channels (Channels 3/4), setting up inter-track sends routed specifically to those auxiliary channels, and configuring ReaComp to listen to that secondary routing stream instead of the primary audio stream.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Trigger**: Typically a staccato, transient-heavy sound (like a 4-on-the-floor kick drum or a spoken vocal).
  - **Target**: Typically a sustained sound (like a pad or bass note).
  - **Compressor Envelope**: The timing is strictly dictated by the compressor's `Attack` and `Release`. Fast attack (0-5ms) ensures immediate ducking. Release (50-200ms) dictates how fast the audio returns; a slower release creates a smooth fade-in, avoiding harsh "jumping" or clicking.

* **Step B: Pitch & Harmony**
  - N/A for the effect itself, but in this implementation, we will generate a sustained minor chord to act as the target, and a low, repeating percussive note to act as the trigger.

* **Step C: Sound Design & FX**
  - **Plugin**: ReaComp.
  - **Detector Input**: Set to `Auxiliary Input L+R` (Channels 3/4).
  - **Ratio**: > 3:1 (higher ratio = harder ducking).
  - **Threshold**: Set low enough that the trigger signal heavily exceeds it.

* **Step D: Mix & Automation (if applicable)**
  - **Track Channels**: The Target track must be set to 4 track channels.
  - **Routing/Sends**: A send is created from the Trigger track (Main 1/2) to the Target track (Aux 3/4).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Creating Trigger/Target | MIDI note insertion | Provides reproducible, synthetic audio sources to clearly demonstrate the ducking effect. |
| Auxiliary Audio Setup | `SetMediaTrackInfo` | Necessary to increase target track channel count from 2 to 4 to receive the sidechain signal. |
| Inter-track Routing | `CreateTrackSend` | Programmatically recreates the drag-and-drop routing shown in the tutorial (Send Ch 1/2 -> Dest Ch 3/4). |
| Sidechain Compression | FX Chain (`ReaComp`) | Configures ReaComp's detector input via API parameters to respond to the auxiliary routing. |

> **Feasibility Assessment**: 100% — REAPER's routing matrix and ReaComp parameter set are perfectly exposed via the ReaScript API, allowing us to generate the entire sidechain ecosystem from scratch with exact precision.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain_Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete Sidechain Ducking setup in the current REAPER project.
    Generates a Pad track (Target) and a Kick track (Trigger), routes them 
    appropriately, and configures ReaComp for auxiliary sidechain ducking.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the target ducked track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    root = NOTE_MAP.get(key, 0) + 48 # Base C3
    intervals = SCALES.get(scale, SCALES["minor"])
    # Create a simple triad based on the root
    chord_notes = [root, root + intervals[2], root + intervals[4]]

    # === Step 2: Create Target Track (Pad) ===
    track_idx_tgt = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_tgt, True)
    tgt_track = RPR.RPR_GetTrack(0, track_idx_tgt)
    RPR.RPR_GetSetMediaTrackInfo_String(tgt_track, "P_NAME", track_name, True)
    
    # CRITICAL: Increase track channels to 4 so it can receive sidechain audio on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(tgt_track, "I_NCHAN", 4)

    # Add Pad MIDI Item (one long sustained chord)
    item_tgt = RPR.RPR_AddMediaItemToTrack(tgt_track)
    RPR.RPR_SetMediaItemInfo_Value(item_tgt, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_tgt, "D_LENGTH", item_length)
    take_tgt = RPR.RPR_AddTakeToMediaItem(item_tgt)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_tgt, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_tgt, item_length)
    
    for note in chord_notes:
        RPR.RPR_MIDI_InsertNote(take_tgt, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
    RPR.RPR_MIDI_Sort(take_tgt)

    # Add Pad Instrument (ReaSynth)
    fx_synth_tgt = RPR.RPR_TrackFX_AddByName(tgt_track, "ReaSynth", False, -1)
    # Make it pad-like (long release)
    RPR.RPR_TrackFX_SetParam(tgt_track, fx_synth_tgt, 2, 0.8) # Long Release

    # Add Sidechain Compressor (ReaComp)
    fx_comp = RPR.RPR_TrackFX_AddByName(tgt_track, "ReaComp", False, -1)
    
    # Dynamically find and set ReaComp Parameters
    num_params = RPR.RPR_TrackFX_GetNumParams(tgt_track, fx_comp)
    for i in range(num_params):
        name_res = RPR.RPR_TrackFX_GetParamName(tgt_track, fx_comp, i, "", 256)
        param_name = name_res[4].lower()
        if "detector" in param_name:
            # ReaComp Detector: 0=Main, 1=Aux L+R, 2=Aux L, 3=Aux R, 4=Output...
            # 1.0 / 6.0 approx 0.1667 (Index 1 out of 7 choices)
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 1.0/6.0)
        elif "thresh" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.3) # Lower threshold for heavy ducking
        elif "ratio" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.2) # High ratio
        elif "attack" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.0) # Fast attack
        elif "release" in param_name:
            RPR.RPR_TrackFX_SetParam(tgt_track, fx_comp, i, 0.15) # Smooth release (~150ms) to avoid clicking

    # === Step 3: Create Trigger Track (Kick) ===
    track_idx_trig = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_trig, True)
    trig_track = RPR.RPR_GetTrack(0, track_idx_trig)
    RPR.RPR_GetSetMediaTrackInfo_String(trig_track, "P_NAME", "Trigger_Kick", True)

    # Add Kick MIDI Item (4-on-the-floor pattern)
    item_trig = RPR.RPR_AddMediaItemToTrack(trig_track)
    RPR.RPR_SetMediaItemInfo_Value(item_trig, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_trig, "D_LENGTH", item_length)
    take_trig = RPR.RPR_AddTakeToMediaItem(item_trig)
    
    kick_pitch = 36 # C2
    note_length_sec = 0.2 # Short percussive hits
    
    for b in range(bars * beats_per_bar):
        note_start_sec = b * (60.0 / bpm)
        note_end_sec = note_start_sec + note_length_sec
        n_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_trig, note_start_sec)
        n_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_trig, note_end_sec)
        RPR.RPR_MIDI_InsertNote(take_trig, False, False, n_start_ppq, n_end_ppq, 0, kick_pitch, 120, False)
    RPR.RPR_MIDI_Sort(take_trig)

    # Add Kick Instrument (ReaSynth)
    fx_synth_trig = RPR.RPR_TrackFX_AddByName(trig_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(trig_track, fx_synth_trig, 1, 0.0) # Instant attack
    RPR.RPR_TrackFX_SetParam(trig_track, fx_synth_trig, 2, 0.05) # Super fast release for staccato kick

    # === Step 4: Setup Sidechain Routing (Send Trigger 1/2 -> Target 3/4) ===
    # 0 in CreateTrackSend indicates a standard track-to-track send
    send_idx = RPR.RPR_CreateTrackSend(trig_track, tgt_track)
    # I_SRCCHAN: 0 = Channels 1/2
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_SRCCHAN", 0)
    # I_DSTCHAN: 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(trig_track, 0, send_idx, "I_DSTCHAN", 2)

    return f"Created sidechain setup: '{track_name}' (Pad) ducking to 'Trigger_Kick' over {bars} bars at {bpm} BPM in {key} {scale}."
```