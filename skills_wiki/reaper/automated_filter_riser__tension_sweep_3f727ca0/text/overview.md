### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Riser (Tension Sweep)

* **Core Musical Mechanism**: The tutorial demonstrates how to use automation modes (Read, Touch, Latch, Write) to manipulate parameters over time. Musically, the most common and impactful use of this technique—which the tutorial explicitly demonstrates at the end—is an automated filter sweep. By slowly opening a low-pass filter (or high-shelf frequency) on a sustained chord, we generate a smooth, continuous increase in spectral density and brightness.

* **Why Use This Skill (Rationale)**: Automating a filter cutoff is a fundamental technique for creating *tension and release* (often used in risers, build-ups, and transitions). Psychoacoustically, as higher frequencies are introduced over a pedal point or drone, the listener perceives an increase in energy and anticipation. Programmatically inserting these envelope points mimics the "Write" or "Latch" automation modes shown in the tutorial, but with mathematical precision.

* **Overall Applicability**: This skill is essential for transitions in electronic music, pop, cinematic scoring, and lo-fi hip-hop. It is typically applied to pads, synth drones, noise sweeps, or full mix buses leading into a chorus or drop.

* **Value Addition**: Compared to a static MIDI clip, this skill encodes the concept of *macro-dynamics and timbral evolution over time*. It bridges the gap between composition (MIDI notes) and mixing/sound design (automation envelopes), allowing an agent to generate living, breathing transition effects rather than flat loops.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: Agnostic (defaults to project or parameter BPM).
  - **Grid/Duration**: The envelope is perfectly aligned to the start (Bar 1) and end (Bar N) of the generated item.
  - **Rhythm**: A single, continuous legato drone that sustains for the entire duration, providing a solid foundation for the filter movement to be audible.

* **Step B: Pitch & Harmony**
  - **Harmony**: Generates a stable, wide chord stack (Root, Fifth, Octave, Tenth/Third) based on the specified key and scale to ensure a rich harmonic spectrum for the filter to act upon.

* **Step C: Sound Design & FX**
  - **Instrument**: ReaSynth (stock REAPER synth) set to generate a harmonically rich tone (saw/square blend).
  - **Effects**: ReaEQ (stock REAPER EQ).
  - **Parameter Mapping**: We target the High-Band Frequency parameter of ReaEQ.

* **Step D: Mix & Automation**
  - **Envelope Creation**: An FX parameter envelope is instantiated for the EQ frequency.
  - **Automation Curve**: A point is placed at `time = 0` with a low normalized value (muffled). A second point is placed at `time = end_of_clip` with a high normalized value (bright/open), creating a sweeping riser.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Drone Pad | MIDI note insertion | Creates the continuous audio source needed to hear the filter sweep clearly. |
| Timbre Generation | FX chain (ReaSynth + ReaEQ) | Uses 100% stock plugins to ensure runtime safety and reproducibility. |
| "Automate Anything" | Automation Envelope (`RPR_GetFXEnvelope`) | Programmatically replicates the tutorial's "Write/Latch" workflow by drawing the precise automation curve the user would perform manually. |

> **Feasibility Assessment**: 100% Reproducible. While the tutorial focuses on the UI workflow of writing automation in real-time, the programmatic translation (inserting envelope points via ReaScript) achieves the exact same audio result deterministically, without requiring real-time playback or mouse interaction.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Riser Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Automated Filter Riser by generating a sustained chord and drawing 
    an automation envelope on a ReaEQ filter, replicating the automation concepts in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the riser will sweep across.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
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

    # Normalize inputs
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Create MIDI Item for Drone ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Timebase conversions
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)
    
    # Generate a wide sustained chord (Root, Fifth, Octave, 10th)
    base_octave = 36 # C2
    chord_degrees = [0, 4, 7, 9] # 1st, 5th, 8ve, 3rd(up an octave)
    
    for degree in chord_degrees:
        # Wrap degree to scale length to allow extensions
        scale_idx = degree % len(scale_intervals)
        octave_shift = degree // len(scale_intervals)
        
        pitch = base_octave + root_val + scale_intervals[scale_idx] + (octave_shift * 12)
        pitch = max(0, min(127, pitch)) # Ensure valid MIDI pitch
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            start_ppq, end_ppq, 
            0, int(pitch), velocity_base, True
        )
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 4: Add FX Chain ===
    # Add Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a richer tone (Mix in some square wave)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5) # Mix param
    
    # Add EQ for the filter sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Find the parameter index for a high frequency band in ReaEQ
    # Standard ReaEQ usually has Band 4 Freq at index 9, but let's be robust
    num_params = RPR.RPR_TrackFX_GetNumParams(track, eq_idx)
    target_param_idx = 0 
    
    for i in range(num_params):
        _, _, _, name, _ = RPR.RPR_TrackFX_GetParamName(track, eq_idx, i, "", 256)
        # Look for the last frequency band (usually High Shelf or Low Pass)
        if "Freq" in name and ("4" in name or "High" in name):
            target_param_idx = i
            break

    # Setup the EQ Band as a Low Pass or pull down the high shelf gain to muffle it
    # Gain for the found band is usually param_idx + 1
    gain_idx = target_param_idx + 1
    if gain_idx < num_params:
        RPR.RPR_TrackFX_SetParam(track, eq_idx, gain_idx, -24.0) # Cut the highs heavily
    
    # === Step 5: Automate the Filter (The Core Tutorial Skill) ===
    # create=True instantiates the envelope
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, target_param_idx, True)
    
    if env:
        # Normalized values (0.0 to 1.0)
        start_val = 0.1 # Very low cutoff frequency
        end_val = 0.9   # High cutoff frequency (fully open)
        
        # Insert point at start (Time 0)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, start_val, 0, 0.0, False, True)
        
        # Insert point at end (Sweep up)
        # Shape 2 is "Slow Start/End" which creates a nice natural sweeping curve
        RPR.RPR_InsertEnvelopePoint(env, item_length_sec, end_val, 2, 0.0, False, True)
        
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' Filter Riser over {bars} bars at {bpm} BPM with FX Automation."
```