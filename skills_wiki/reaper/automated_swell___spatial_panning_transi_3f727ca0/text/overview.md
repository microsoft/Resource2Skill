### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Swell & Spatial Panning Transition 

* **Core Musical Mechanism**: The strategic use of automation envelopes (Volume and Pan) over time to create dynamic movement. Rather than static levels, this pattern uses a slow volume swell (fade-in) paired with a rhythmic, bar-synced stereo panning sweep to transition from silence into full width and volume.
* **Why Use This Skill (Rationale)**: Static mixes sound artificial and lifeless. Automation breathes humanity and energy into a track. A volume swell builds anticipation and psychoacoustic tension leading up to a structural change (like a chorus or drop). Pairing this with spatial movement (panning left and right) creates a sense of widening the stereo field, engaging the listener's spatial hearing and making the eventual resolution feel larger.
* **Overall Applicability**: Perfect for intro pads, risers, transition noise sweeps, and build-up synth chords in electronic, pop, and cinematic music. 
* **Value Addition**: Transforms a completely static, flat MIDI chord into a living, moving transitional element. It programmatically encodes the exact "Read" mode automation curves demonstrated in the tutorial, giving an AI agent the ability to inject dynamic sweeps and spatial effects without relying on LFO plugins.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Grid**: Adapts to project BPM.
  - **Timing**: The automation is musically synced. The volume swell happens smoothly across the entire specified duration (e.g., 4 bars). The panning sweeps periodically, hitting Left, Right, and Center precisely on the downbeats of each bar.
  - **Note Duration**: A single, long, sustained pad chord held for the entire length of the transition.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (defaults to C minor).
  - **Voicing**: A dense, 4-note closed-voicing pad chord (Root, 3rd, 5th, Octave) to provide a rich frequency spectrum for the automation to act upon.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a sawtooth pad with a slow release to prevent abrupt cutoffs.
  - **Automation Envelopes**: Native REAPER track envelopes. Volume scales amplitude from `0.0` (-inf) to `1.0` (0dB). Pan scales from `-1.0` (100% Left) to `1.0` (100% Right).

* **Step D: Mix & Automation**
  - **Curve Shapes**: Uses REAPER's shape `2` (Slow start/end or "S-Curve") to ensure smooth, non-linear swelling that sounds natural to the human ear. 
  - **Automation Mode**: Track is set to "Read" (Mode 1), precisely executing the automation playback shown in the tutorial.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Musical Element** | MIDI note insertion | Creates the sustained chord block needed to make the volume/pan automation audible. |
| **Sound Generation** | FX Chain (`ReaSynth`) | Provides a robust, stock sound source without depending on external VSTs or audio files. |
| **Automation** | `RPR_InsertEnvelopePoint` | Directly writes points to the native Volume and Pan envelopes, perfectly mimicking the tutorial's focus on automation lanes. |
| **Envelope Activation** | `RPR_Main_OnCommand` | Guarantees the native Volume and Pan envelopes are visible and instantiated before trying to write to them. |

> **Feasibility Assessment**: 100% reproduction of the tutorial's automation principles. While the tutorial physically showed a user moving faders with a mouse in "Write/Touch/Latch" modes, this code replicates the *end result* of that process—perfectly shaped, playable automation lanes running in "Read" mode.

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
    Create an Automated Swell & Spatial Panning Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell transition.
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

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Sound Design (ReaSynth Pad) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a smoother pad-like sound
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 1.0) # Oscillator shape to Saw
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.8) # Release time (longer tail)

    # === Step 3: Create MIDI Item & Sustained Chord ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 7] # Root, 3rd, 5th, Octave
    base_octave = 48 # C3
    
    end_ppq = int(beats_per_bar * bars * 960) # Standard 960 PPQ per quarter note
    
    for degree in chord_degrees:
        octave_offset = (degree // 7) * 12
        scale_index = degree % 7
        pitch = base_octave + root_val + scale_intervals[scale_index] + octave_offset
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 0, end_ppq, 0, pitch, velocity_base, False
        )
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Native Automation Generation ===
    # Exclusively select the track to perform actions on it
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Action 40406: Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40406, 0)
    # Action 40456: Track: Toggle track pan envelope visible
    RPR.RPR_Main_OnCommand(40456, 0)
    
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    
    # Write Volume Swell (Shape 2 = Slow Start/End 'S-Curve' for natural fade)
    if vol_env:
        # Time 0: Silence (0.0 amplitude)
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 2, 0.0, False, False)
        # End Time: 0dB / Unity Gain (1.0 amplitude)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0.0, False, False)
        RPR.RPR_Envelope_Sort(vol_env)
        
    # Write Bar-Synced Panning Sweep
    if pan_env:
        for b in range(bars + 1):
            time_pos = b * bar_length_sec
            # Alternate pattern: Center -> Left -> Right -> Center -> Left...
            if b % 2 == 0:
                pan_val = 0.0    # Center
            elif b % 4 == 1:
                pan_val = -1.0   # 100% Left
            else:
                pan_val = 1.0    # 100% Right
                
            # Shape 2 provides a smooth sinusoidal movement between pan points
            RPR.RPR_InsertEnvelopePoint(pan_env, time_pos, pan_val, 2, 0.0, False, False)
        RPR.RPR_Envelope_Sort(pan_env)

    # Set Automation Mode to 1 (Read Mode) so the sweeps execute on playback
    RPR.RPR_SetTrackAutomationMode(track, 1)

    return f"Created '{track_name}' with {bars}-bar Volume Swell & Pan Sweep automation at {bpm} BPM in {key} {scale}."
```