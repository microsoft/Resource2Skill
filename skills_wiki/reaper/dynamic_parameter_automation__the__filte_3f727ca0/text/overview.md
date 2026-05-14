### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Parameter Automation (The "Filter Sweep" Pad)

* **Core Musical Mechanism**: The tutorial demonstrates how to rapidly record automation for any plugin parameter by using "Write", "Touch", or "Latch" modes. Musically, the culmination of this technique is the **automated filter sweep**—where an EQ's low-pass filter frequency is dynamically moved over time to change the harmonic content and brightness of a sustained synth chord. 
* **Why Use This Skill (Rationale)**: Automating parameters (like filter cutoff, volume, or delay feedback) breathes life and organic movement into otherwise static digital sounds. A low-pass filter sweep is a fundamental technique in electronic music, pop, and film scoring used to build tension (opening the filter) or create a muffled, underwater transition (closing the filter).
* **Overall Applicability**: This technique is universally applicable. It shines when creating intro pads, riser/drop buildups in EDM, evolving ambient drones, or "lo-fi" transitions where a track temporarily becomes muffled before coming back in full fidelity.
* **Value Addition**: Instead of a flat, static synthesizer chord, this skill generates a living, breathing pad. It encodes the knowledge of how to link a specific plugin parameter (ReaEQ Frequency) to the project timeline via an automation envelope, simulating a human hand turning a knob during playback.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: A slow, continuous change over a long period (e.g., 4 to 8 bars).
  - **Note Duration**: Sustained legato notes holding for the entire duration of the pattern to allow the filter movement to be clearly heard.
* **Step B: Pitch & Harmony**
  - **Voicing**: A thick, sustained pad chord (Root, Fifth, Octave, and Tenth) provides a dense harmonic spectrum for the filter to carve away.
* **Step C: Sound Design & FX**
  - **Instrument**: ReaSynth (generating a basic saw/square wave rich in harmonics).
  - **Effect**: ReaEQ. 
  - **Target Parameter**: Band 1 set to a "Low Pass" filter type. The cutoff frequency is the specific target for automation.
* **Step D: Mix & Automation**
  - **Envelope**: A custom FX parameter envelope is created for the EQ frequency.
  - **Curve**: The automation drops the frequency down to muffle the sound, then slowly raises it back up to full brightness (a "V" or "U" shape curve).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Pad Chord | MIDI note insertion | Creates the continuous audio signal required to hear a filter sweep. |
| Synth Sound | FX chain (ReaSynth) | Provides a harmonically rich source signal. |
| Filter Sweep | FX chain (ReaEQ) + Automation Envelope | Directly replicates the tutorial's technique. Since an agent cannot "perform" physical mouse movements in `Write` mode, we use `RPR_GetFXEnvelope` and `RPR_InsertEnvelopePoint` to programmatically generate the resulting automation curve shown in the video. |

> **Feasibility Assessment**: 100% reproducible. The code uses native REAPER plugins (ReaSynth, ReaEQ) and native envelope API functions to create the exact automated filter sweep demonstrated at the end of the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Automated Pad",
    track_name: str = "Sweeping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with an automated ReaEQ Low-Pass filter sweep.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars for the swell/sweep.
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    if scale not in SCALES:
        scale = "minor"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Setup FX Chain (Synth + EQ) ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak synth for a pad feel (slower attack/release, mix of saw/square)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.4) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 8, 0.6) # Release

    # Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ, Band 1 Type is parameter 3. Value ~0.8 maps to Low Pass.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 3, 0.88)
    
    # === Step 4: Create Automation Envelope ===
    # Parameter 0 in ReaEQ is Band 1 Frequency. We want to automate this.
    # The 'True' flag creates the envelope if it doesn't exist.
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)

    # Calculate timings
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_time_sec = bar_length_sec * bars

    # Insert automation points to create a "V" shape filter sweep
    # RPR_InsertEnvelopePoint(env, time, value, shape, tension, selected, noSortIn)
    # Shape 0 = Linear, Shape 1 = Square, Shape 2 = Slow start/end
    
    # Start bright (normalized frequency near 1.0)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.9, 2, 0.0, False, True)
    # Muffle in the middle of the pattern (normalized frequency low)
    RPR.RPR_InsertEnvelopePoint(env, total_time_sec / 2.0, 0.15, 2, 0.0, False, True)
    # Open back up at the end
    RPR.RPR_InsertEnvelopePoint(env, total_time_sec, 0.9, 0, 0.0, False, True)
    
    # Apply points
    RPR.RPR_Envelope_SortPoints(env)

    # === Step 5: Create MIDI Item & Notes ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_time_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build a lush chord: Root, 5th, Octave, 3rd (an octave up)
    root_pitch = SCALES[scale][0] + NOTE_MAP[key] + 48 # Octave 4
    chord_pitches = [
        root_pitch, 
        root_pitch + SCALES[scale][4],      # 5th
        root_pitch + 12,                    # Octave
        root_pitch + 12 + SCALES[scale][2]  # 10th (3rd octave up)
    ]

    ticks_per_quarter = 960
    total_ticks = int(bars * beats_per_bar * ticks_per_quarter)

    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            0, total_ticks, # Start to End
            0, pitch, velocity_base, False
        )

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with automated EQ filter sweep over {bars} bars at {bpm} BPM."
```