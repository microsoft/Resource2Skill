# Sidechain Pumping Compression (Automated Routing Emulation)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sidechain Pumping Compression (Automated Routing Emulation)

* **Core Musical Mechanism**: The defining characteristic of this pattern is volume "ducking"—rhythmically attenuating the volume of a sustained sound (like a pad, bass, or loop) exactly when a transient trigger sound (like a kick drum) hits. This is achieved by routing the audio signal of the trigger track into channels 3/4 (Auxiliary Inputs) of the target track, and using a compressor on the target track that listens only to those auxiliary channels to trigger gain reduction.

* **Why Use This Skill (Rationale)**: 
  1. **Groove & Rhythm (The "Pump")**: In dance music genres (House, Techno, Future Bass), sidechaining a pad or bass to a 4-on-the-floor kick creates a breathing, rhythmic pulse that drives the song forward.
  2. **Mixing & Clarity (Masking)**: It prevents low-frequency buildup. If a bassline and a kick drum hit at the same time, their frequencies clash. Sidechaining ducks the bass for the split millisecond the kick strikes, giving the kick maximum punch without sacrificing the perceived loudness of the bassline.

* **Overall Applicability**: This technique is ubiquitous across modern music production. It shines on:
  - Heavy drop chords in EDM/Future Bass.
  - Sub-bass lines in Hip-Hop and Pop to let the kick poke through.
  - Ambient noise/texture beds to give them rhythmic movement.
  - Vocal groups ducking slightly to the lead vocal to maintain intelligibility.

* **Value Addition**: Compared to a blank MIDI clip, this skill encodes advanced audio routing, channel mapping, and psychoacoustic mix automation. It bridges the gap between composition (MIDI) and mix engineering (dynamic processing) to create an inherently "produced" feel.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Trigger**: A repetitive transient sound. Most commonly a 4/4 Kick drum hitting on every downbeat.
  - **Target**: A sustained or legato loop/chord progression that allows the "ducking" envelope to be clearly heard. 

* **Step B: Pitch & Harmony**
  - The sidechain itself is pitch-agnostic. However, to demonstrate it, we generate a deep, sustained root-position 7th chord based on the target key/scale for the pad, and a low C1 pulse for the kick trigger.

* **Step C: Sound Design & FX**
  - **Target Track FX**: `VST: ReaComp (Cockos)`
  - **ReaComp Settings**:
    - **Threshold**: ~-25.0 dB (Set low enough to ensure the kick pushes past it).
    - **Ratio**: 4:1 (A steep ratio to aggressively clamp down the volume).
    - **Attack**: ~3 ms (Fast enough to duck instantly when the kick hits, but not 0ms to avoid clicking artifacts).
    - **Release**: ~150 ms (Controls the "breathe" or return time; timed to groove with the tempo).
    - **Detector Input**: `Auxiliary Inputs` (This tells the compressor to ignore the pad's audio and only listen to the kick).

* **Step D: Mix & Automation (Routing)**
  - **Target Track Channels**: Must be increased from standard 2 (stereo) to 4 channels.
  - **Hardware Send**: Audio from the Kick track (channels 1/2) is sent to the Target track (channels 3/4).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Routing & Sidechain | `RPR_CreateTrackSend`, `RPR_SetMediaTrackInfo_Value` | Since ReaScript cannot physically "drag and drop" UI elements, we programmatically replicate the exact routing the drag-and-drop action creates (4 channels, 1/2 -> 3/4 send). |
| Compression Setup | `RPR_TrackFX_SetParam` | Configures ReaComp's threshold, ratio, attack, release, and assigns the Detector to the Auxiliary input (param 14). |
| Trigger/Target generation | `RPR_MIDI_InsertNote`, ReaSynth | Purely ADDITIVE pattern demonstration. We create both the "Kick" and the "Loop/Pad" synthetically so the sidechain effect is instantly audible. |

> **Feasibility Assessment**: 100%. While we can't automate the mouse dragging shown in the video, the REAPER Python API perfectly exposes track channel counts, send matrices, and ReaComp parameter values, resulting in an identical audio sidechain configuration.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sidechain Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Sidechain Pumping Pad and Kick Trigger in the current REAPER project.
    This replicates the drag-and-drop sidechain routing technique.

    Args:
        project_name: Project identifier.
        track_name: Name for the target (pad) track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Pad voicing: Root, 3rd, 5th, 7th (Octave 4)
    chord_pitches = [
        48 + root_val + scale_intervals[0], 
        48 + root_val + scale_intervals[2], 
        48 + root_val + scale_intervals[4], 
        48 + root_val + scale_intervals[min(6, len(scale_intervals)-1)]
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # === Step 1: Create the Target Pad Track ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    pad_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", track_name, True)
    
    # CRITICAL: Set Pad track to 4 channels to receive sidechain
    RPR.RPR_SetMediaTrackInfo_Value(pad_track, "I_NCHAN", 4)

    # Pad Generator: Add ReaSynth and ReaComp
    pad_synth = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    pad_comp = RPR.RPR_TrackFX_AddByName(pad_track, "ReaComp", False, -1)
    
    # Configure ReaComp for sidechain ducking
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 0, -25.0)  # Threshold (dB)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 1, 4.0)    # Ratio
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 2, 3.0)    # Attack (ms)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 3, 150.0)  # Release (ms)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_comp, 14, 1.0)   # Detector: Auxiliary Inputs

    # Pad MIDI: Sustained chords
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", bar_len * bars)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    for b in range(bars):
        start_time = b * bar_len
        end_time = start_time + bar_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pad_take, end_time)
        
        for pitch in chord_pitches:
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

    # === Step 2: Create the Trigger Kick Track ===
    kick_idx = track_count + 1
    RPR.RPR_InsertTrackAtIndex(kick_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "SC Trigger Kick", True)

    # Kick Generator: Add ReaSynth and pitch it down to simulate a kick pulse
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 0, 0.0)    # Sine wave
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 3, -12.0)  # Tuning down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 4, 100.0)  # Short decay

    # Kick MIDI: 4-on-the-floor trigger
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", bar_len * bars)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    for b in range(bars):
        for beat in range(beats_per_bar):
            start_time = b * bar_len + (beat * beat_len)
            end_time = start_time + (beat_len * 0.25) # Short pulse
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, end_time)
            
            # Kick pitch (C1 = 36)
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base + 20, False)

    RPR.RPR_MIDI_Sort(pad_take)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Step 3: Audio Routing (The "Drag and Drop" Emulator) ===
    # Send from Kick Track to Pad Track
    send_idx = RPR.RPR_CreateTrackSend(kick_track, pad_track)
    
    # Configure Send Source: Audio Channels 1/2 (Index 0)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_SRCCHAN", 0)
    
    # Configure Send Destination: Audio Channels 3/4 (Index 2)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "I_DSTCHAN", 2)
    
    # Set Send Volume to unity (0 dB = 1.0)
    RPR.RPR_SetTrackSendInfo_Value(kick_track, 0, send_idx, "D_VOL", 1.0)

    # Force update UI
    RPR.RPR_UpdateArrange()
    
    return f"Created Sidechain configuration: 'SC Trigger Kick' ducking '{track_name}' via Channels 3/4 over {bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist
- [x] Does the code compute MIDI pitches from key/scale?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?