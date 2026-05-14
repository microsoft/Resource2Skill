### 1. High-level Design Pattern Extraction

**Skill Name**: Automated Volume Swell & Pan Sweep (Dynamic Pad)

* **Core Musical Mechanism**: Automation is the process of recording parameter changes over time. While the tutorial focuses on writing automation via physical/virtual fader movements in real-time (Write/Touch/Latch modes), the underlying musical mechanism is the **programmatic control of dynamics and spatial positioning**. This pattern creates a swelling pad that fades in (Volume automation) while sweeping across the stereo field (Pan automation).
* **Why Use This Skill (Rationale)**: Static sounds can quickly become ear-fatiguing. By automating volume and panning, you introduce *macro-dynamics* and movement. A volume swell is a classic technique for building tension leading into a new section (a riser or transition), while auto-panning creates a sense of spatial width and psychoacoustic depth, keeping the listener engaged. 
* **Overall Applicability**: This technique is essential for transitions, risers, evolving ambient pads, and creating movement in otherwise static synth textures or soundscapes in any genre (especially Electronic, Lo-Fi, and Cinematic).
* **Value Addition**: Compared to a static MIDI clip, this skill encodes the concept of *temporal modulation*. It doesn't just place notes on a grid; it breathes life into the instrument by shaping its envelope and stereo image algorithmically over a specific musical duration.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Configurable (defaults to 120 BPM).
  - **Rhythm**: Sustained over the entire generated duration (e.g., a 4-bar long legato chord).
  - **Envelope Timing**: The automation spans exactly the length of the MIDI item, ensuring the swell peaks exactly at the transition point (end of the bar).

* **Step B: Pitch & Harmony**
  - **Key & Scale**: Parametric.
  - **Voicing**: A sustained diatonic triad (Root, 3rd, 5th of the chosen scale) in the 3rd octave to act as a mid-low pad.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` used as a basic placeholder texture.

* **Step D: Mix & Automation**
  - **Volume Envelope**: Sweeps from `-inf` (silence/0.0 value) to `0 dB` (1.0 value) and back down, using a "Slow Start/End" curve (Shape 2) for a natural, tape-like fade.
  - **Pan Envelope**: Sweeps from `100% Left` (-1.0) to `100% Right` (1.0) linearly (Shape 0) over the duration of the item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Pad | MIDI note insertion | Allows us to define the exact diatonic chord based on user input. |
| Making the track audible | FX Chain (ReaSynth) | Ensures the track produces sound using stock, native REAPER tools without external dependencies. |
| Volume Swell | `RPR_GetTrackEnvelopeByName` | Directly reproduces the tutorial's core concept of the "Volume" automation lane (`v` shortcut). |
| Spatial Movement | `RPR_GetTrackEnvelopeByName` + Pan | Reproduces the Pan automation discussed in the tutorial using direct programmatic point insertion rather than real-time fader riding. |

> **Feasibility Assessment**: 100% reproducible. REAPER's ReaScript API allows direct access to create and populate track automation envelopes (Volume and Pan) bypassing the need to physically "ride the fader" in Write/Touch modes.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a sustained pad with an automated Volume swell and Pan sweep in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the pad and sweep will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

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

    # === Step 3: Add Instrument ===
    # Add stock ReaSynth to ensure we have a sound source for the pad
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Slightly lower the ReaSynth default volume to avoid harsh clipping
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.5) 

    # === Step 4: Create MIDI Item & Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate PPQ bounds for exact note durations
    start_qn = RPR.RPR_TimeMap2_timeToQN(0, 0.0)
    end_qn = RPR.RPR_TimeMap2_timeToQN(0, item_length)
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

    # Generate chord (Root, 3rd, 5th)
    root_val = NOTE_MAP.get(key, 0) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_intervals = [scale_intervals[0], scale_intervals[2], scale_intervals[4]]

    for interval in chord_intervals:
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            start_ppq, end_ppq, 
            0, root_val + interval, velocity_base, False
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate Volume (The Swell) ===
    # Select only this track and run the action to make the Volume envelope visible
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # Values: 0.0 = -inf, 1.0 = +0dB. 
        # Shape 2 is "Slow start/end" which creates a smooth, musical swell curve.
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length * 0.75, 1.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 0.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    # === Step 6: Automate Pan (The Sweep) ===
    # Make Pan envelope visible
    RPR.RPR_Main_OnCommand(40456, 0) # Track: Toggle track pan envelope visible
    
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        # Values: -1.0 = 100% L, 1.0 = 100% R
        # Shape 0 is "Linear" for a straight sweep across the stereo field.
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, -1.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 1.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(pan_env)

    return f"Created '{track_name}' pad with Volume swell and Pan sweep over {bars} bars at {bpm} BPM."
```