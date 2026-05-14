### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Parameter Automation Swell (Volume, Pan & Filter)

* **Core Musical Mechanism**: The procedural application of continuous parameter changes over time—specifically volume fades, stereo panning movement, and resonant filter sweeps. This recreates the effect of "riding the faders" or twisting synthesizer knobs during a live performance to create evolving, breathing soundscapes.
* **Why Use This Skill (Rationale)**: Static mixes sound artificial. Automation provides macro-dynamics (long-term changes in loudness) and psychoacoustic movement. A volume swell builds structural tension; a panning envelope creates a sense of spatial width and motion; a filter sweep emphasizes the harmonic series, slowly revealing high-frequency energy to drive a transition (a staple in electronic music build-ups).
* **Overall Applicability**: This technique is universally applicable. It shines on intro pad synths, transition risers, sustaining strings, and build-ups prior to a drop in EDM, Pop, and cinematic scoring. 
* **Value Addition**: Compared to a static MIDI clip, this skill encodes the concept of *macro-movement*. It transforms a simple block chord into a living, breathing texture that guides the listener's attention across the stereo field and frequency spectrum.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: Continuous unquantized automation curves.
  - **Duration**: The sweeps are mapped proportionally to the length of the requested bars, allowing the tension to scale with the section length. 
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (e.g., C minor).
  - **Voicing**: A sustained 7th chord (Root, 3rd, 5th, 7th) is generated to provide a thick harmonic bed that responds well to filtering.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` acts as the raw waveform generator.
  - **FX Chain**: `ReaEQ` is inserted after the synth. Band 2 (a parametric peak filter by default) is given a gain boost and a tightened Q (resonance).
* **Step D: Mix & Automation**
  - **Automation Modes**: The track is programmatically set to `Read` mode (Automation Mode 1), meaning the faders and knobs will visibly move during playback.
  - **Volume**: Fades in from $-\infty$ (0.0 amp) to 0dB (1.0 amp) at the midpoint, then fades out.
  - **Pan**: Sweeps from left (-0.7) to right (+0.7) on every bar.
  - **Filter**: The ReaEQ Band 2 Frequency is swept from low to high and back down, acting as a classic resonant wah/sweep.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Bed | MIDI note insertion | Provides precise, parametric control over the chord voicing to feed the effects. |
| Timbre & Filter | FX Chain (`ReaSynth` + `ReaEQ`) | Stock REAPER plugins ensure 100% compatibility; boosting an EQ peak creates the resonance needed for a sweep. |
| Movement & Swells | Automation Envelopes (`Volume`, `Pan`, `FX Param`) | Accurately recreates the continuous fader/knob movements demonstrated in the tutorial's Write/Touch modes. |

> **Feasibility Assessment**: 100% — The generated script perfectly translates the human action of writing volume, pan, and FX automation into precise mathematical curves using REAPER's native envelope APIs.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustaining 7th chord pad with automated Volume, Pan, and a resonant EQ sweep.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the sweep over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
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

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & 7th Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 6] # Root, 3rd, 5th, 7th
    octave = 4
    base_midi = octave * 12 + root_val
    
    for degree in chord_degrees:
        octave_offset = degree // 7
        scale_idx = degree % len(scale_intervals)
        midi_pitch = base_midi + (octave_offset * 12) + scale_intervals[scale_idx]
        # Insert sustained note for the entire duration of the item
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, True)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Configure ReaEQ Band 2 (Peak filter) to act as a resonant sweep
    # Param 6: Band 2 Gain (Set to ~0.7 for an audible boost peak)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 6, 0.7)
    # Param 7: Band 2 Q (Set to ~0.6 for narrower, squelchy resonance)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 7, 0.6)

    # === Step 5: Automate Volume, Pan, and FX ===
    # Enable Read mode (1) so faders visibly move during playback as shown in the tutorial
    RPR.RPR_SetTrackAutomationMode(track, 1) 
    RPR.RPR_SetOnlyTrackSelected(track)

    # 1. Volume Envelope Swell
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # Values represent Amplitude: 0.0 = -inf, 1.0 = 0dB. Shape 0 = Linear.
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length / 2.0, 1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    # 2. Panning Envelope Movement
    RPR.RPR_Main_OnCommand(40456, 0) # Toggle track pan envelope visible
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if env_pan:
        # Sweep Pan back and forth across the bars
        for b in range(bars + 1):
            time_pos = b * bar_length_sec
            pan_val = -0.7 if b % 2 == 0 else 0.7
            RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_pan)

    # 3. FX Parameter Envelope (ReaEQ Band 2 Frequency)
    # Param 5 is Band 2 Frequency. "True" creates the envelope if hidden.
    env_eq = RPR.RPR_GetFXEnvelope(track, eq_idx, 5, True)
    if env_eq:
        # Normalized values (0.0 to 1.0 representing 20Hz to 24000Hz approx)
        RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 0.1, 0, 0.0, False, True) 
        RPR.RPR_InsertEnvelopePoint(env_eq, item_length / 2.0, 0.9, 0, 0.0, False, True) 
        RPR.RPR_InsertEnvelopePoint(env_eq, item_length, 0.1, 0, 0.0, False, True) 
        RPR.RPR_Envelope_SortPoints(env_eq)

    return f"Created '{track_name}' with automated Volume, Pan, and EQ sweeps over {bars} bars at {bpm} BPM in key of {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?