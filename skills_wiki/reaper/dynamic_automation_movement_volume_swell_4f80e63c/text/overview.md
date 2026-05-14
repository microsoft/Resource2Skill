# Dynamic Automation Movement (Volume Swell & Pan Sweep)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Automation Movement (Volume Swell & Pan Sweep)

* **Core Musical Mechanism**: Modulating track parameters over time using automation envelopes. Instead of static volume and panning, this pattern applies continuous time-based changes (a fade-in volume "swell" and a left-to-right panning sweep) to a sustained musical drone, turning a lifeless synth tone into a breathing, evolving texture.

* **Why Use This Skill (Rationale)**: Static sounds quickly lead to listener fatigue. By automating amplitude (volume) and spatial placement (pan), we introduce psychoacoustic movement. A volume swell fundamentally manipulates tension—it implies an approach or a build-up towards a structural downbeat (like a drop or a chorus transition). Pan automation pulls the listener's ear across the stereo field, creating a sense of three-dimensional space and widening the mix without adding new instruments.

* **Overall Applicability**: This technique is universally necessary. Specifically, it shines for creating ambient intros, cinematic transition risers, evolving synth pads, and bringing "life" to background elements in electronic, pop, and rock mixes.

* **Value Addition**: Compared to a raw MIDI clip, this skill encodes the concept of *macro-dynamics*—structuring the intensity and spatial position of a sound over a multi-bar phrase rather than just at the note level. 


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature/BPM**: Follows project constraints (e.g., 120 BPM).
  - **Rhythm**: A single, continuous sustained chord (drone) spanning the entire requested number of bars.
  - **Note Duration**: 100% legato/tied for the full phrase length to provide a continuous signal for the automation to shape.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Dynamically calculated from parameters.
  - **Voicing**: A classic, stable 1-5-8 (Root, Fifth, Octave) open chord voicing. This avoids muddy thirds in the lower registers and provides a rich, harmonically stable bed that emphasizes the volume and pan movement over complex melodic movement.

* **Step C: Sound Design & FX**
  - **Instrument**: ReaSynth.
  - **Parameter Tuning**: Attack and release times are slightly increased to create a pad-like texture, preventing harsh clicks at the start and end of the item.

* **Step D: Mix & Automation (if applicable)**
  - **Volume Automation**: An S-curve (slow start/end) envelope fading from `-inf` (0.0 amplitude) to `0dB` (1.0 amplitude) over the duration of the item.
  - **Pan Automation**: A slow sine-like sweep starting center (0.0), drifting hard left (-0.8), swinging hard right (0.8), and returning to center.
  - **Automation Mode**: Set to `Read` (Fader turns green, locking out manual trim and forcing REAPER to strictly follow the drawn envelope lines, as demonstrated in the tutorial).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Drone | MIDI note insertion | Provides the continuous audio signal required to actually hear the automation working. |
| Pad Sound | FX chain (ReaSynth) | Stock REAPER instrument capable of generating a stable, sustained oscillator tone. |
| Volume/Pan Movement | Track Envelopes (`RPR_GetTrackEnvelopeByName`) | Directly mimics the tutorial's focus on opening automation lanes and drawing time-locked parameter curves. |
| Automation Enforcement | Track Automation Mode (`RPR_SetTrackAutomationMode`) | Mirrors the video's explanation of switching from `Trim/Read` to `Read` mode to force faders to follow the envelope. |

> **Feasibility Assessment**: 100% — The creation of tracks, insertion of MIDI, and drawing of track automation envelopes (Volume and Pan) can be fully accomplished using REAPER's native Python API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Drone/Pad with Volume Swells and Pan Sweeps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate the swell over.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the track and automation.
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

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Calculate timing
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth to generate sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a pad-like envelope: Attack (param 4) and Release (param 5)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1) # 100ms attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5) # 500ms release

    # Create MIDI Item and Take
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine Base Pitch (Octave 3 = 48)
    root_pitch = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Voicing: 1 - 5 - 8 (Root, Fifth, Octave) for a stable, wide drone
    chord_pitches = [
        root_pitch, 
        root_pitch + scale_intervals[4 % len(scale_intervals)], # 5th
        root_pitch + 12 # Octave
    ]

    # Insert sustained drone notes
    start_qn = 0.0
    end_qn = bars * beats_per_bar
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                start_qn * 960, end_qn * 960, 
                                0, pitch, velocity_base, False)

    # === AUTOMATION SETUP ===
    # To reliably get envelopes in REAPER, we ensure they are visible first
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40407, 0) # Track: Toggle track pan envelope visible

    # 1. Volume Swell Envelope
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        # shape: 2 = Slow start/end (S-Curve) for smooth swells
        # Insert start point (0.0 amplitude = -inf)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, True)
        # Insert end point (1.0 amplitude = 0dB) at the end of the item
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(vol_env)

    # 2. Pan Sweep Envelope
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        # shape: 2 = Slow start/end
        # Center -> Left -> Right -> Center
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.33, -0.8, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.66, 0.8, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_Sort(pan_env)

    # 3. Change Automation Mode to "Read" (1)
    # Mode 1 forces the UI faders (which will turn green) to physically move and follow the drawn envelopes
    RPR.RPR_SetTrackAutomationMode(track, 1)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' drone with Volume Swell and Pan Sweep automation over {bars} bars in {key} {scale}."
```