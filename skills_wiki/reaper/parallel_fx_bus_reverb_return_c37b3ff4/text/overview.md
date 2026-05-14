# Parallel FX Bus (Reverb Return)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Parallel FX Bus (Reverb Return)

* **Core Musical Mechanism**: Decoupling the spatial or time-based effects (reverb, delay) from the source audio tracks by routing the source signals post-fader into a dedicated, 100% wet auxiliary track (the "Bus" or "Return").
* **Why Use This Skill (Rationale)**: 
  1. **Acoustic Cohesion (Glue)**: By sending multiple tracks (drums, synths, vocals) to the same reverb bus, it places disparate elements into a shared acoustic environment, creating depth and a unified mix.
  2. **Transient Preservation**: Parallel processing allows the original track to remain completely uncompromised (100% dry, preserving punch and transients) while the bus track handles the dense, sustained wet signal. 
  3. **Efficiency**: It saves CPU by using one high-quality reverb plugin for the entire mix rather than instantiating a separate reverb on every track.
* **Overall Applicability**: This is a mandatory, foundational mixing technique used in nearly every genre. It is primarily used for spatial effects (Reverb, Delay) and parallel dynamic/harmonic processing (e.g., parallel "fuzz" distortion or parallel "New York" compression, as demonstrated in the video).
* **Value Addition**: Compared to a blank project or a track with an insert reverb, this script encodes professional mix-routing architecture. It sets up the source track, the FX bus, configures the FX plugin for return duty (Dry muted, Wet active), and establishes the post-fader send with calibrated levels.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: Tempo-agnostic, but typically evaluated at 120 BPM.
  - **Grid/Durations**: To demonstrate the reverb tail effectively, a staccato or mid-length chord progression is utilized so the "wet" tail can be heard in the gaps between the dry notes.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. (Default: C Major).
  - **Chord Progression**: A classic I - vi - IV - V progression to provide a broad frequency spectrum for the reverb to process.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` on the source track (acts as the dry signal).
  - **Bus FX**: `ReaVerbate` (Stock REAPER Reverb) on the destination track.
  - **FX Parameters**: On an Aux Return, the reverb plugin must be set to 0% Dry (to prevent doubling the original volume) and 100% Wet. Room size and dampening are set to create a lush, audible tail.
* **Step D: Mix & Automation**
  - **Send Routing**: A track send is created from the Source Track to the Bus Track.
  - **Send Mode**: Post-Fader (Mode 0). This ensures that if the source track's volume is faded down, the reverb tail fades proportionally, maintaining the wet/dry balance.
  - **Send Level**: Defaulting to -6dB to taste.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Bus Architecture** | Track routing (`RPR_InsertTrackAtIndex`) | Creates the exact master-parent and bus topology shown in the video. |
| **Reverb Setup** | FX Chain (`ReaVerbate` + Parameter Set) | Configures the native reverb for "Return" duty (Dry = -inf) without needing third-party VSTs. |
| **Send Routing** | Track Send (`RPR_CreateTrackSend`) | Replicates the drag-and-drop send mechanism from the tutorial, explicitly setting Post-Fader and linear volume. |
| **Audio Source** | MIDI note insertion + `ReaSynth` | Provides a self-contained, additive dry signal to audibly demonstrate the parallel processing. |

> **Feasibility Assessment**: 100% Reproducible. The routing architecture, native plugins (ReaVerbate, ReaSynth), and post-fader send mechanisms are fully accessible via the REAPER Python API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Reverb Return Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    send_db: float = -6.0,
    **kwargs,
) -> str:
    """
    Create a Parallel Reverb Bus and route a generated Synth track to it.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created FX bus track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        send_db: Volume of the send from the source to the bus (in dB).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the tracks and routing.
    """
    import math
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate Root Note
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_chord(degree, octave=4):
        """Builds a basic triad based on the scale degree (0-indexed)."""
        notes = []
        for i in [0, 2, 4]:  # Root, 3rd, 5th
            idx = (degree + i) % len(scale_intervals)
            octave_shift = (degree + i) // len(scale_intervals)
            pitch = (octave + octave_shift + 1) * 12 + root_val + scale_intervals[idx]
            notes.append(pitch)
        return notes

    # === Step 2: Create Source Track (Dry Signal) ===
    track_count = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    src_track = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(src_track, "P_NAME", "Dry Synth", True)

    # Add Instrument to Source
    RPR.RPR_TrackFX_AddByName(src_track, "ReaSynth", False, -1)

    # Create MIDI Item for Source
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(src_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Progression: I - vi - IV - V (Degrees 0, 5, 3, 4)
    progression = [0, 5, 3, 4] 
    
    # Insert MIDI Notes
    qn_length = 60.0 / bpm
    ppq = 960 # Ticks per quarter note
    
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        chord_notes = get_chord(degree, octave=4)
        
        # Staccato chord on beat 1 and 3 to leave room for reverb tail
        for beat in [0, 2]:
            start_pos = (bar * beats_per_bar * qn_length) + (beat * qn_length)
            end_pos = start_pos + (qn_length * 0.5) # 8th note duration
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            for pitch in chord_notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Create Parallel FX Bus Track ===
    bus_idx = track_count + 1
    RPR.RPR_InsertTrackAtIndex(bus_idx, True)
    bus_track = RPR.RPR_GetTrack(0, bus_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", track_name, True)

    # Add ReaVerbate to Bus
    fx_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaVerbate", False, -1)
    
    # Configure ReaVerbate for Return Bus (Wet=100%, Dry=0%)
    # In ReaVerbate: Param 0 is Wet, Param 1 is Dry, Param 2 is Room Size
    RPR.RPR_TrackFX_SetParamNormalized(bus_track, fx_idx, 0, 0.75) # Wet up
    RPR.RPR_TrackFX_SetParamNormalized(bus_track, fx_idx, 1, 0.0)  # Dry at -inf
    RPR.RPR_TrackFX_SetParamNormalized(bus_track, fx_idx, 2, 0.8)  # Large Room Size

    # === Step 4: Create Track Send (Source -> Bus) ===
    send_idx = RPR.RPR_CreateTrackSend(src_track, bus_track)
    
    # Configure Send Properties
    # Convert dB to linear scalar (10^(dB/20))
    send_vol_linear = 10 ** (send_db / 20.0) if send_db > -144 else 0.0
    
    # Send Mode: 0 = Post-Fader (Post-Pan), 1 = Pre-FX, 3 = Pre-Fader (Post-FX)
    RPR.RPR_SetTrackSendInfo_Value(src_track, 0, send_idx, "I_SENDMODE", 0)
    # Send Volume
    RPR.RPR_SetTrackSendInfo_Value(src_track, 0, send_idx, "D_VOL", send_vol_linear)

    return f"Created 'Dry Synth' and '{track_name}' tracks. Configured parallel post-fader send at {send_db}dB."
```