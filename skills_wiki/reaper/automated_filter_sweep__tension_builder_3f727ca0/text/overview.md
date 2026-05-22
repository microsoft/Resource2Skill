### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Sweep (Tension Builder)

* **Core Musical Mechanism**: The pattern relies on **Parameter Automation** to create dynamic movement over time. Specifically, it applies a low-pass filter (or high-cut shelf) to a sustained synthetic sound and gradually automates the cutoff frequency from low to high. 
* **Why Use This Skill (Rationale)**: Static synthetic pads and drones can quickly become fatiguing or uninteresting. By automating the filter cutoff over a period of bars, we introduce *timbral motion*. This leverages the psychoacoustic principle of "opening up" the frequency spectrum, which inherently builds musical tension. This is a foundational technique for creating transitions, risers, and drop build-ups.
* **Overall Applicability**: Essential for EDM, Pop, Ambient, and Cinematic music. It is typically used on pads, synth leads, or full mix buses right before a structural change in the song (e.g., Verse transitioning to Chorus, or a build-up leading into a drop).
* **Value Addition**: Instead of manually "riding the fader" or drawing complex envelopes by hand, this skill programmatically calculates the time bounds of the musical phrase and maps a perfect linear sweep across the exact duration of the chord, ensuring perfect synchronization with the project grid.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Sustained over the entirety of the specified phrase (e.g., 4 bars).
  - **Rhythm**: 1 long, continuous legato MIDI note block without re-triggering.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (e.g., C Minor).
  - **Voicing**: A dense, wide 7th chord (Root, 3rd, 5th, 7th) to provide a rich harmonic spectrum. The rich harmonic spectrum is necessary because a filter sweep requires higher harmonics to "reveal" as the cutoff frequency rises. 

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured to output a mix of Sawtooth and Pulse waves (rich in harmonics).
  - **Effects**: `ReaEQ` inserted after the synth.
  - **Parameter**: Band 4 Frequency (Parameter Index 9 in ReaEQ).

* **Step D: Mix & Automation**
  - **Automation Mode**: Track set to `Read` mode.
  - **Envelope Curve**: A linear automation curve drawn directly into the ReaEQ parameter envelope lane, starting at a normalized value of `0.1` (muffled/dark) and rising to `0.9` (bright/open) exactly at the end of the MIDI item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Pad | MIDI note insertion | Provides precise timing and programmatic 7th chord generation from parameters. |
| Timbre Generation | FX chain (ReaSynth) | Creates the necessary harmonic content natively without external VSTis. |
| The Filter | FX chain (ReaEQ) | Matches the tutorial's use of ReaEQ for frequency sweeping. |
| The "Sweep" (Motion) | Automation Envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly mimics the video's core lesson of writing envelope data over time to control FX parameters. |

> **Feasibility Assessment**: 100% reproducible. The script utilizes pure REAPER API to create the media, insert the native plugins, generate the MIDI, and explicitly draw the parameter automation points.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Filter Sweep in the current REAPER project.
    Generates a sustained 7th chord on a synth and automates a ReaEQ filter
    sweeping upwards over the duration of the item to build tension.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars the sweep will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Enable "Read" automation mode (Value 1) so automation plays back
    RPR.RPR_SetTrackAutomationMode(track, 1)

    # === Step 3: Add Synth & EQ ===
    # Add ReaSynth
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a harmonically rich pad (Saw + Pulse)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.2)  # Master Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 1, 0.6)  # Sawtooth mix
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.6)  # Pulse mix
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 4, 0.8)  # Extra Release time

    # Add ReaEQ for the sweep
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 4: Create MIDI Item & Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_midi = 48 + NOTE_MAP.get(key, 0) # Start around C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # Root, 3rd, 5th, 7th

    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for degree in chord_degrees:
        octave_offset = degree // 7
        scale_degree = degree % 7
        pitch = root_midi + (octave_offset * 12) + scale_intervals[scale_degree]

        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            0.0, end_ppq, 
            1, pitch, velocity_base, False
        )

    # === Step 5: Automate EQ Filter Sweep ===
    # In ReaEQ: Parameter 9 is "Freq-Band 4" (defaults to high shelf/cut)
    # We will automate this parameter from a low value to a high value over the bars
    param_idx_band4_freq = 9 
    
    # RPR_GetFXEnvelope returns the envelope, creating it if it doesn't exist (True flag)
    env = RPR.RPR_GetFXEnvelope(track, fx_eq, param_idx_band4_freq, True)
    
    if env:
        # Insert Envelope Point at Start (Time 0.0) - Closed filter (approx 0.1 normalized)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 0, 0.0, False, True)
        
        # Insert Envelope Point at End (item_length) - Open filter (approx 0.9 normalized)
        RPR.RPR_InsertEnvelopePoint(env, item_length, 0.9, 0, 0.0, False, True)
        
        # Sort points to finalize the envelope
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with automated filter sweep over {bars} bars at {bpm} BPM in {key} {scale}"
```