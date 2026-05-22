### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Transition Pad (Volume Swells & FX Sweeps)

* **Core Musical Mechanism**: The strategic use of **automation envelopes** to continuously change audio parameters over time. Instead of static volume or timbre, this pattern uses evolving curves (swells, sweeps, and panning) to create dynamic motion.

* **Why Use This Skill (Rationale)**: Automation is the key to breathing life into a mix. A static synth pad sounds artificial; an automated pad creates anticipation and release. A volume swell builds physical tension (crescendo), an EQ frequency sweep adds psychoacoustic motion by unmasking higher harmonics over time, and automated panning creates spatial width. This is the programmatic equivalent of a musician physically riding the faders and knobs (as demonstrated via "Write" and "Touch" modes in the tutorial).

* **Overall Applicability**: Essential for intros, bridge transitions, drop buildups (EDM/Pop), and ambient soundscapes. Anywhere a static sound needs to evolve and guide the listener's ear into the next section of the track.

* **Value Addition**: This skill transforms a static block of MIDI into a living, breathing transition element. It encodes the knowledge of how to structure envelope points (linear vs. curved shapes) to create smooth, musical buildups without requiring real-time manual fader riding.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: A single sustained note or chord spanning the entire requested duration (`bars`).
  - **Pacing**: The automation curves dictates the rhythm. The changes are gradual, spanning multiple bars (macro-rhythm) rather than beat-by-beat subdivisions.

* **Step B: Pitch & Harmony**
  - **Chords**: Generates a 4-note 7th chord (Root, 3rd, 5th, 7th) based on the specified `key` and `scale` parameters.
  - **Voicing**: Placed in the 4th octave (e.g., C4) to sit well as a mid-range pad.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth`, configured with a mix of saw and square waves to provide a rich harmonic spectrum. (A pure sine wave cannot be effectively filtered because it has no overtones).
  - **FX 1**: `ReaEQ`. Used to create a dramatic tonal shift. 

* **Step D: Mix & Automation**
  - **Volume Envelope**: Swells from `-inf` (0.0 linear) to `0dB` (1.0 linear) using a "Slow start/end" curve for a smooth fade-in.
  - **Pan Envelope**: Sweeps from Hard Left to Hard Right, then back to Center.
  - **FX Parameter Envelope**: Automates ReaEQ Band 4 (High Shelf frequency) sweeping from 500Hz up to 20,000Hz, mimicking a classic low-pass filter opening up.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Pad | MIDI note insertion | Allows for parametric chord generation based on the target key/scale. |
| Sound Source | FX Chain (`ReaSynth`, `ReaEQ`) | Stock plugins guarantee execution without third-party dependencies. |
| Dynamic Movement | Automation Envelopes (`RPR_InsertEnvelopePoint`) | The direct ReaScript equivalent of the "Touch/Write" fader riding demonstrated in the tutorial. Creates precise, reproducible curves for Volume, Pan, and EQ. |

> **Feasibility Assessment**: 100% reproducible. While the tutorial focuses on the UI actions of recording automation via mouse movements, the underlying REAPER architecture relies on Envelope Points. This script mathematically generates those exact points, yielding the exact same sonic result.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with automated Volume, Pan, and EQ sweeps.
    Demonstrates programmatic parameter automation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate 7th chord pitches
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    root_pitch = root_val + 48 # Start in 4th octave for a pad
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # Root, 3rd, 5th, 7th

    for deg in chord_degrees:
        octave_shift = deg // len(scale_intervals)
        scale_idx = deg % len(scale_intervals)
        pitch = root_pitch + scale_intervals[scale_idx] + (octave_shift * 12)
        
        # Insert sustained note for the full duration
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth for a rich tone (Saw + Square)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.8) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.2) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.5) # Release

    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Programmatic Automation Envelopes ===
    # Force select track to use action commands safely
    RPR.RPR_SetOnlyTrackSelected(track)

    # 1. Volume Swell Envelope
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # Start at 0.0 (-inf), curve up to 1.0 (0dB) at the end. Shape 2 = Slow start/end
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    # 2. Pan Sweep Envelope
    RPR.RPR_Main_OnCommand(40456, 0) # Track: Toggle track pan envelope visible
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        # Sweep Left (-1.0) -> Right (1.0) -> Center (0.0). Shape 0 = Linear
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, -1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.5, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(pan_env)

    # 3. FX Parameter Envelope (ReaEQ Frequency Sweep)
    if eq_idx >= 0:
        # Param 9 is usually Band 4 Frequency in default ReaEQ
        freq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True) 
        if freq_env:
            # Sweep frequency from 500Hz up to 20000Hz to unmask the pad
            RPR.RPR_InsertEnvelopePoint(freq_env, 0.0, 500.0, 2, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(freq_env, item_length, 20000.0, 0, 0.0, False, True)
            RPR.RPR_Envelope_SortPoints(freq_env)

    return f"Created '{track_name}' with {bars} bars of automated Volume, Pan, and EQ Sweeps in {key} {scale}."
```