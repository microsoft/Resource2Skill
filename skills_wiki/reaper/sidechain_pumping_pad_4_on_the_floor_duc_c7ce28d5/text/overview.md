# Sidechain Pumping Pad (4-on-the-Floor Ducking)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sidechain Pumping Pad (4-on-the-Floor Ducking)

* **Core Musical Mechanism**: The defining characteristic of this pattern is "ducking"—using the audio output of a rhythmic element (usually a kick drum) to momentarily compress and lower the volume of a sustained element (like a synth pad or bass). This creates a rhythmic, breathing, or "pumping" effect on otherwise static audio.
* **Why Use This Skill (Rationale)**: 
  - **Groove & Syncopation**: By suppressing the strong downbeats, you force the listener's brain to focus on the off-beats (when the compressor releases and the volume swells back up). This pushes the groove forward.
  - **Frequency Masking**: It clears space in the mix. The kick drum needs low-end energy to hit hard; ducking the bass or pad out of the way for a few milliseconds prevents muddy frequency clashes.
* **Overall Applicability**: This is the foundational sound of Electronic Dance Music (EDM), House, Techno, and Future Bass. It is also highly effective in Pop and Lo-Fi hip-hop for creating a stylized, bouncing groove.
* **Value Addition**: Instead of a static, lifeless chord, this skill encodes dynamic movement and mix-bus relationship knowledge, tying the rhythm section directly to the harmonic section.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Typically 110–130 BPM for House/EDM styles.
  - **Trigger (Kick)**: 1/4 note grid (4-on-the-floor). Short, staccato hits.
  - **Target (Pad)**: Sustained notes spanning the entire 4-bar duration.
* **Step B: Pitch & Harmony**
  - **Target**: A full 7th chord (1st, 3rd, 5th, 7th scale degrees) based on the chosen key and scale, providing a rich, dense harmonic bed that makes the volume ducking highly noticeable.
  - **Trigger**: A low C2 MIDI note to simulate a kick drum fundamental.
* **Step C: Sound Design & FX**
  - **Instruments**: `ReaSynth` on both tracks.
  - **FX Chain**: The Target track uses `ReaComp` (REAPER's native compressor).
  - **ReaComp Settings**:
    - **Detector Input**: Set to *Auxiliary L+R* (this tells the compressor to listen to channels 3/4 instead of its own audio on 1/2).
    - **Threshold**: -20 dB (low enough to catch the trigger).
    - **Ratio**: 5.0 (heavy compression for an obvious pump).
    - **Attack**: 5 ms (fast enough to duck immediately, slow enough to avoid clicking).
    - **Release**: 150 ms (timed to swell back up rhythmically before the next quarter note).
* **Step D: Mix & Automation**
  - **Routing**: Audio send from the Trigger track (Channels 1/2) to the Target track (Channels 3/4). MIDI send is disabled so the pad track doesn't play the kick drum's MIDI notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm / Harmony | `RPR_MIDI_InsertNote()` | Allows precise creation of the 4-on-the-floor trigger and the sustained 7th chord. |
| Sidechain Routing | `RPR_CreateTrackSend()` & `RPR_SetTrackSendInfo_Value()` | Accurately replicates the drag-and-drop routing shown in the tutorial, explicitly targeting channels 3/4. |
| Ducking Effect | `RPR_TrackFX_SetParam()` | Configures ReaComp's hidden parameters, specifically setting the Detector Input to read the sidechain signal. |

> **Feasibility Assessment**: 100% reproduction. The ReaScript API allows for the exact configuration of auxiliary sends, track channel counts, and plugin parameter manipulation required to build a textbook sidechain compressor. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Sidechain Pumping Pad in the current REAPER project.
    Generates a 4-on-the-floor trigger track and a sustained chord track, 
    linked via ReaComp for rhythmic ducking.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 2: Create Target Track (Sustained Synth Pad) ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    target_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(target_track, "P_NAME", f"{track_name}_Pad", True)
    
    # Enable 4 track channels to receive sidechain audio
    RPR.RPR_SetMediaTrackInfo_Value(target_track, "I_NCHAN", 4)

    target_item = RPR.RPR_AddMediaItemToTrack(target_track)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(target_item, "D_LENGTH", item_length)
    target_take = RPR.RPR_AddTakeToMediaItem(target_item)
    RPR.RPR_SetMediaItemTakeInfo_Value(target_take, "B_ISMIDI", 1)

    # Calculate 7th chord from key/scale parameters
    root_note = NOTE_MAP.get(key.capitalize(), 0) + 60 # C4
    scale_notes = SCALES.get(scale.lower(), SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th scale degrees
    chord_intervals = [scale_notes[i % len(scale_notes)] + 12 * (i // len(scale_notes)) for i in chord_degrees]

    # Insert sustained chord spanning the entire item
    for interval in chord_intervals:
        insert_note(target_take, 0.0, item_length, root_note + interval, velocity_base - 10)
    RPR.RPR_MIDI_Sort(target_take)

    # Add Target FX (ReaSynth + ReaComp)
    RPR.RPR_TrackFX_AddByName(target_track, "ReaSynth", False, -1)
    comp_fx = RPR.RPR_TrackFX_AddByName(target_track, "ReaComp", False, -1)
    
    # Configure ReaComp for Sidechain Ducking
    num_params = RPR.RPR_TrackFX_GetNumParams(target_track, comp_fx)
    for i in range(num_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(target_track, comp_fx, i, "", 256)
        name = name.lower()
        if "thresh" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, -20.0) # -20 dB Threshold
        elif "ratio" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 5.0)   # 5:1 Ratio
        elif "detector" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 1.0)   # 1.0 = Aux L+R Input
        elif "attack" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 5.0)   # 5 ms Attack
        elif "release" in name:
            RPR.RPR_TrackFX_SetParam(target_track, comp_fx, i, 150.0) # 150 ms Release

    # === Step 3: Create Trigger Track (4-on-the-Floor Kick) ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    trigger_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trigger_track, "P_NAME", f"{track_name}_Trigger", True)

    trigger_item = RPR.RPR_AddMediaItemToTrack(trigger_track)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(trigger_item, "D_LENGTH", item_length)
    trigger_take = RPR.RPR_AddTakeToMediaItem(trigger_item)
    RPR.RPR_SetMediaItemTakeInfo_Value(trigger_take, "B_ISMIDI", 1)

    # Insert 1/4 note rhythmic triggers
    kick_pitch = 36 # C2
    quarter_note_sec = 60.0 / bpm
    total_beats = bars * beats_per_bar
    for beat in range(int(total_beats)):
        start_sec = beat * quarter_note_sec
        end_sec = start_sec + (quarter_note_sec * 0.5) # 8th note duration
        insert_note(trigger_take, start_sec, end_sec, kick_pitch, velocity_base)
    RPR.RPR_MIDI_Sort(trigger_take)

    RPR.RPR_TrackFX_AddByName(trigger_track, "ReaSynth", False, -1)

    # === Step 4: Routing (The Sidechain Link) ===
    send_idx = RPR.RPR_CreateTrackSend(trigger_track, target_track)
    # Send Audio to Channels 3/4 on the target track (Value 2)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_DSTCHAN", 2) 
    # Send from Channels 1/2 on the trigger track (Value 0)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_SRCCHAN", 0) 
    # Disable MIDI send (Magic number 417792 / 0x66000 prevents the pad from playing the kick notes)
    RPR.RPR_SetTrackSendInfo_Value(trigger_track, 0, send_idx, "I_MIDIFLAGS", 417792)

    return f"Created Sidechain Pumping setup (Tracks: Pad & Trigger) over {bars} bars in {key} {scale} at {bpm} BPM"
```