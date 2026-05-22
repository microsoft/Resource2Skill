### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Cinematic Swell & Pan Sweep

* **Core Musical Mechanism**: This pattern transforms a static sustained chord into a dynamic, evolving musical gesture using **Automation Envelopes**. By programmatically drawing points on the Track Volume and Track Pan envelopes, it creates a gradual fade-in (swell) accompanied by spatial movement across the stereo field. 
* **Why Use This Skill (Rationale)**: Static synthesized sounds often lack human feel and can clutter a mix. Automation introduces macro-dynamics. A volume swell builds tension leading into a new structural section (like a drop or chorus), utilizing the psychoacoustic effect of approaching sound. Panning automation prevents the sound from masking the center-panned elements (kick, snare, vocals) while adding a sense of physical width and motion.
* **Overall Applicability**: Essential for ambient textures, transition effects (risers/swells), cinematic drones, and evolving pad sounds in electronic music, pop, and film scoring.
* **Value Addition**: Compared to a static MIDI clip, this skill encodes the concept of *macro-movement over time*. It demonstrates how to interact with REAPER's envelope API to programmatically shape the amplitude and stereo position of an item, setting the track to "Read" mode so the faders actively mirror the automation during playback.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Duration**: A single, continuous event spanning the entire requested number of `bars`.
  - **Envelope Timing**: Automation points are mathematically tied to the item duration (e.g., pan reaches maximum left at 25% of the item length, and maximum right at 75%).
* **Step B: Pitch & Harmony**
  - **Voicing**: Generates a lush, wide chord spanning two octaves. It extracts the 1st, 3rd, 5th, and 7th degrees of the given scale, plus a sub-octave root note for depth (e.g., a min9 or maj7 depending on the input scale).
* **Step C: Sound Design & FX**
  - **Generator**: `ReaSynth` blending square (50%) and sawtooth (70%) waveforms for a rich harmonic spectrum.
  - **Spatial FX**: `JS: Chorus` added to immediately widen the initial mono synth patch.
* **Step D: Mix & Automation**
  - **Volume Envelope**: Interpolates from `-inf` (0.0 amplitude) to `0dB` (1.0 amplitude) using a "Slow Start/End" curve (Shape 2) for a natural, exponential-sounding swell.
  - **Pan Envelope**: Sweeps from Center (0.0) -> Left (-0.7) -> Right (+0.7) -> Center (0.0) using smooth curves.
  - **Automation Mode**: Track is set to `Read` mode (Mode 1), mirroring the tutorial's demonstration of fader playback.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Base | MIDI note insertion | Provides the raw sustained pitches required for a swell. |
| Timbre | FX chain (ReaSynth + Chorus) | Creates a harmonically rich sound capable of being shaped by the automation. |
| Macro-Dynamics | Track Envelope API (`GetTrackEnvelopeByName`, `InsertEnvelopePoint`) | Directly reproduces the video's core focus: automating parameters over time to create movement. |

> **Feasibility Assessment**: 100% reproducible. The script utilizes native REAPER API functions to generate the envelopes, insert precise points, and set the specific automation reading modes discussed in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Automated Cinematic Swell & Pan Sweep in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the swell will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created automated track.
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

    scale_degrees = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.title(), 0) + 48 # Base octave 4

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Setup ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Exclusively select this track so action commands target it reliably
    RPR.RPR_SetOnlyTrackSelected(track)

    # === Step 3: Add FX Chain ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth for a rich pad tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5) # Square Mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.7) # Saw Mix
    
    # Add Chorus for stereo width before we pan it
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)

    # === Step 4: Create MIDI Content ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build a lush 4-note chord + sub bass
    chord_indices = [0, 2, 4, 6] 
    pitches = [root_pitch - 12] # Sub octave
    for i in chord_indices:
        octave_shift = i // len(scale_degrees)
        deg = scale_degrees[i % len(scale_degrees)]
        pitches.append(root_pitch + deg + (octave_shift * 12))

    start_qn = 0.0
    end_qn = bars * beats_per_bar

    for pitch in pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_qn * 960, end_qn * 960, 1, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Program Automation Envelopes ===
    
    # Reveal Volume Envelope via Action (requires track selected)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    # Reveal Pan Envelope via Action
    RPR.RPR_Main_OnCommand(40456, 0) # Track: Toggle track pan envelope visible
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")

    shape_slow_start_end = 2

    if vol_env:
        # Clear any existing points in the timeline
        RPR.RPR_DeleteEnvelopePointRange(vol_env, -1.0, item_length + 1.0)
        
        # Swell Volume from 0.0 (-inf) to 1.0 (0dB)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    if pan_env:
        RPR.RPR_DeleteEnvelopePointRange(pan_env, -1.0, item_length + 1.0)
        
        # Sweep Pan: Center -> Left -> Right -> Center
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.25, -0.7, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length * 0.75, 0.7, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.0, shape_slow_start_end, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(pan_env)

    # Set Track Automation Mode to 'Read' (1) so faders move visually during playback
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' with {len(pitches)}-note chord, automated Volume swell and Pan sweep over {bars} bars at {bpm} BPM."
```