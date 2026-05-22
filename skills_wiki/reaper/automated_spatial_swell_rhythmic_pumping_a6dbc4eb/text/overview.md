# Automated Spatial Swell & Rhythmic Pumping (Automation Envelopes)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Spatial Swell & Rhythmic Pumping (Automation Envelopes)

* **Core Musical Mechanism**: Time-varying manipulation of audio parameters using automation envelopes. Instead of static volume or panning, this pattern uses programmatically drawn envelope points to create continuous movement—specifically, a gradual volume swell (crescendo) combined with an automated left-to-right spatial sweep (auto-pan).
* **Why Use This Skill (Rationale)**: Static sounds can quickly cause listener fatigue. Automation breathes life into a track by introducing macro-dynamics (long volume builds over several bars) and stereo width movement. Musically, a volume swell builds tension leading into a new section (a drop or chorus), while automated panning creates psychoacoustic space, preventing masking in the center of the mix.
* **Overall Applicability**: Intro pads, build-ups in EDM/Pop, cinematic risers, and transition effects. It is highly useful for taking a basic, static synthesizer tone and turning it into an evolving, dynamic texture.
* **Value Addition**: This skill moves beyond static MIDI note generation by encoding the ability to script time-based parameter changes (envelopes). It teaches the agent how to instantiate effects and draw precise mathematical curves into REAPER's automation lanes.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: Adapts to project BPM.
  - **Rhythm**: A single, long sustained pad lasting the entire duration of the specified bars.
  - **Envelope Timing**: The volume envelope linearly ramps up over the full duration. The pan envelope oscillates rhythmically (Left to Right) every 2 beats (half-note rate).

* **Step B: Pitch & Harmony**
  - **Harmony**: Generates a sustained root position triad (Root, 3rd, 5th, plus the octave) based on the provided Key and Scale parameters.
  - **Octave**: Placed in the mid-register (around C3/C4) to ensure a thick pad sound that clearly demonstrates the automation.

* **Step C: Sound Design & FX**
  - **Synthesizer**: `ReaSynth` (Stock REAPER synth) with a blend of sawtooth and square waves for harmonic richness.
  - **Automation Target FX**: `JS: Volume/Pan Smoother`. We use this stock JSFX instead of the track fader because it ensures the envelopes are always exposed to the API and guarantees normalized parameter values (0.0 to 1.0) without fighting track trim modes.

* **Step D: Mix & Automation (if applicable)**
  - **Volume Automation**: Sweeps from 0.0 (silence) to 0.8 (~unity gain) linearly.
  - **Pan Automation**: Uses a slow start/end curve (shape 2) oscillating between 0.1 (hard left) and 0.9 (hard right).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Pad Generation | MIDI note insertion | Allows calculation of a sustained triad based on the provided key/scale, ensuring musical context. |
| Sound Source | FX Chain (`ReaSynth`) | Provides a rich, continuous harmonic waveform necessary to make the volume and pan sweeps audible. |
| Parameter Automation | `RPR_GetFXEnvelope` & `RPR_InsertEnvelopePoint` | Replicates the tutorial's focus on drawing automation. Targeting a JS plugin guarantees the parameters are accessible and normalize perfectly from 0.0 to 1.0. |

> **Feasibility Assessment**: 100% — The code fully recreates the automation techniques demonstrated in the tutorial (drawing envelopes), applying them programmatically to pitch-calculated MIDI data using 100% stock REAPER plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with a programmatic volume swell and automated panning.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell to last.
        velocity_base: Base MIDI velocity for the pad notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
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

    # Determine base MIDI note (Octave 4)
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    base_midi_note = 48 + root_val # C3 is 48

    # Build a 1-3-5-8 chord based on the chosen scale
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    chord_degrees = [0, 2, 4] # 1st, 3rd, 5th degrees of the scale
    chord_notes = [base_midi_note + scale_intervals[d % len(scale_intervals)] + (12 * (d // len(scale_intervals))) for d in chord_degrees]
    chord_notes.append(base_midi_note + 12) # Add the octave for thickness

    # === Step 1: Track and Timing Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item & Notes ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Convert to standard PPQ (960) for MIDI
    qn_length = RPR.RPR_TimeMap2_timeToQN(0, total_length_sec)
    ppq_end = int(qn_length * 960)

    # Insert sustained chord
    for pitch in chord_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, ppq_end, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Add FX Chain ===
    # 1. ReaSynth for raw tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Beef up the synth: mix in some saw and square
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8) # Release time

    # 2. JS Volume/Pan Smoother (Provides easy automation targets without fighting track envelopes)
    vol_pan_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume/Pan Smoother", False, -1)

    # === Step 4: Draw Automation Envelopes ===
    # In JS: Volume/Pan Smoother: Param 0 is Volume, Param 1 is Pan
    vol_env = RPR.RPR_GetFXEnvelope(track, vol_pan_idx, 0, True)
    pan_env = RPR.RPR_GetFXEnvelope(track, vol_pan_idx, 1, True)

    # Draw Volume Swell (Linear ramp from 0.0 to 1.0)
    # Shape 0 = Linear
    RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0.0, False, True)
    RPR.RPR_InsertEnvelopePoint(vol_env, total_length_sec, 1.0, 0, 0.0, False, True)
    RPR.RPR_Envelope_SortPoints(vol_env)

    # Draw Rhythmic Auto-Pan (Bounces Left and Right every half note)
    # Shape 2 = Slow Start/End (Smooth sine-like curve)
    current_time = 0.0
    pan_val = 0.1 # Start left (0.5 is center, 0.0 is hard left, 1.0 is hard right)
    
    # Insert points every half note (2 beats)
    step_sec = beat_length_sec * 2 
    while current_time <= total_length_sec + 0.001:
        RPR.RPR_InsertEnvelopePoint(pan_env, current_time, pan_val, 2, 0.0, False, True)
        # Flip pan for next point
        pan_val = 0.9 if pan_val == 0.1 else 0.1
        current_time += step_sec
        
    RPR.RPR_Envelope_SortPoints(pan_env)

    return f"Created '{track_name}' pad with Volume & Pan automation over {bars} bars at {bpm} BPM in {key} {scale}."
```