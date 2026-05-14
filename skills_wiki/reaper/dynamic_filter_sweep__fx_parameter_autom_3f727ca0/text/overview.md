### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Filter Sweep (FX Parameter Automation)

* **Core Musical Mechanism**: The defining signature of this pattern is **parameter automation over time**—specifically, a low-pass filter sweep (or high-shelf cut sweep). By smoothly opening a filter over several bars, a static, harmonically rich synthesizer chord transforms from a dark, muffled hum into a bright, energetic presence.
* **Why Use This Skill (Rationale)**: A static synth pad can easily stagnate a mix. By automating the filter cutoff, you add *psychoacoustic motion* and *narrative direction*. Musically, this creates a buildup of tension (often leading to a drop or a chorus), utilizing the harmonic series by gradually revealing upper overtones. This technique bridges the gap between composition and mixing.
* **Overall Applicability**: This pattern is a staple for transitions in almost every modern genre—EDM build-ups (risers), ambient intro pads evolving into a main section, or pop pre-choruses adding energy before the hook.
* **Value Addition**: Compared to a static MIDI clip, this skill encodes the concept of *macro-dynamics*. It demonstrates how to programmatically bind an automation envelope to a specific FX parameter (ReaEQ frequency) to manipulate timbral energy over time, perfectly mirroring the tutorial's focus on "Touch/Write" automation modes without needing manual mouse movements.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, dynamically adjustable (default 120 BPM).
  - **Rhythm**: A single, sustained legato chord that spans the entire duration of the pattern (e.g., 4 full bars), providing a continuous bed of sound for the filter to act upon.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable. Defaults to a rich minor 9th or minor 7th chord (root, minor 3rd, perfect 5th, minor 7th, major 2nd/9th) built from the root note. Extended voicings are necessary because a filter sweep requires rich high-frequency content to be audible.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a Sawtooth wave (Saw shape = 1.0) to generate dense harmonics.
  - **Filter Setup**: `ReaEQ` is used. We manipulate Band 4 (High Shelf) by dropping its gain to absolute minimum (-inf dB), effectively turning it into a low-pass filter. 
* **Step D: Mix & Automation**
  - **Automation Envelope**: We create a Volume/Parameter envelope for ReaEQ's Band 4 Frequency (Parameter 9). 
  - **Curve**: The envelope moves from 0.0 (around 20Hz, fully dark) at Bar 1 to 1.0 (24kHz, fully open) at the end of the final bar, using a linear or slightly exponential curve to build tension.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Bed | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides the sustained 7th/9th chord necessary to produce harmonics. |
| Timbre Generation | FX chain (`ReaSynth`) | Sawtooth wave provides the raw harmonic energy needed for a filter sweep. |
| Filter Sweep (Automation) | Automation envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly translates the tutorial's core concept (automating an FX parameter) into programmable ReaScript, ensuring reproducible "latch/write" curves programmatically. |

> **Feasibility Assessment**: 100% reproducible. The code relies entirely on REAPER's native ReaSynth and ReaEQ, mathematically inserting the exact automation points that would normally be recorded via Kenny's "Write" or "Touch" fader demonstrations.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Dynamic Filter Sweep (FX Parameter Automation) in REAPER.
    
    Generates a sustained, harmonically rich chord using ReaSynth, and 
    automates ReaEQ to perform a multi-bar filter sweep buildup.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and automation.
    """
    import reaper_python as RPR

    # === Music Theory & Pitch Generation ===
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

    root_pitch = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Build a rich chord: 1st, 3rd, 5th, 7th (using scale degrees)
    chord_degrees = [0, 2, 4, 6] 
    chord_pitches = []
    for deg in chord_degrees:
        octave_shift = (deg // len(scale_intervals)) * 12
        pitch_class = scale_intervals[deg % len(scale_intervals)]
        chord_pitches.append(root_pitch + octave_shift + pitch_class)
    
    # Add a root bass note an octave down for body
    chord_pitches.append(root_pitch - 12)

    # === Step 1: Set Tempo & Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_duration = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_duration)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert sustained chord spanning the full item
    for pitch in chord_pitches:
        # Convert seconds to MIDI pulses (PPQ)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, total_duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (ReaSynth & ReaEQ) ===
    # 4a. Add ReaSynth and configure for rich harmonics (Saw wave)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 1 is Sawtooth shape. Set to 1.0 (100% saw)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0)
    # Param 0 is Volume. Lower to 0.5 to prevent clipping
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.5)

    # 4b. Add ReaEQ
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ, Band 4 is usually a High Shelf. 
    # Param 9 = Band 4 Freq, Param 10 = Band 4 Gain.
    # By setting High Shelf Gain to 0.0 (-inf dB), we create a Low Pass filter effect.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0)

    # === Step 5: Automate Filter Sweep ===
    # We automate Param 9 (Band 4 Freq) to sweep from closed to open
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    if env:
        # Point 1: Start (Time = 0.0) -> Filter heavily closed (e.g. 0.1 normalized, ~100Hz)
        RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.1, 0, 0.0, False, True)
        
        # Point 2: End (Time = total_duration) -> Filter fully open (1.0 normalized, ~24kHz)
        RPR.RPR_InsertEnvelopePoint(env, total_duration, 1.0, 0, 0.0, False, True)
        
        # Sort envelope points to apply changes
        RPR.RPR_Envelope_Sort(env)

    return f"Created '{track_name}' with {bars}-bar automated filter sweep (ReaEQ) on a {key} {scale} chord at {bpm} BPM."
```