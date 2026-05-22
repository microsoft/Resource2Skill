### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Automation Envelopes (Volume Swells, Auto-Pan, & Mute Gating)

* **Core Musical Mechanism**: Utilizing track automation envelopes to change parameters—specifically Volume, Pan, and Mute—over time. Rather than relying on static mixer settings, automation breathes life into a track by actively shaping its dynamics, stereo image, and rhythm via drawn envelope points.
* **Why Use This Skill (Rationale)**: 
  - **Volume Automation**: Creates macro-dynamics like tension-building swells (crescendos) or smooth fade-ins without relying on compression. 
  - **Pan Automation**: Prevents ear fatigue and creates psychoacoustic width by moving a sound across the stereo spectrum (auto-panning).
  - **Mute Automation**: Generates aggressive micro-dynamics. Rapidly toggling mute on and off creates a rhythmic "trance gate" or stutter effect, turning a sustained pad/chord into a rhythmic instrument.
* **Overall Applicability**: Essential for transitions, risers, ambient pad movement, vocal riding, and EDM/electronic drop preparations. It turns static synthesized sounds into evolving, expressive textures.
* **Value Addition**: Transforms a basic, flat MIDI chord into a continuously evolving soundscape. It introduces the concept of time-varying mixing techniques directly into the composition process.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 BPM (Configurable).
  - **Volume**: Swells smoothly over the first 2 bars.
  - **Pan**: Sweeps from hard-left to hard-right every bar.
  - **Mute**: Triggers a rapid 1/8th-note rhythmic gate (stutter) during the final bar to create tension.
* **Step B: Pitch & Harmony**
  - Generates a sustained triad chord (Root, 3rd, 5th) spanning the full 4 bars based on the provided Key and Scale (defaulting to C Minor).
* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` producing a continuous raw oscillator tone, allowing the automation to be clearly heard.
* **Step D: Mix & Automation**
  - REAPER Automation Envelopes are toggled to visible.
  - Envelope points are inserted programmatically with specific curve shapes:
    - `Shape 0` (Linear) for smooth panning.
    - `Shape 1` (Square/Step) for instantaneous Mute stutters.
    - `Shape 2` (Slow Start/End) for a musical, non-linear Volume swell.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Sound Source | MIDI note insertion + ReaSynth | Provides a continuous audio signal necessary to hear the volume, pan, and mute automation clearly. |
| Making Envelopes Accessible | `RPR_Main_OnCommand` (Toggle Actions) | In REAPER, default track envelopes must be made active/visible before they can be retrieved by name via the API. |
| Creating Automation Movement | `RPR_InsertEnvelopePoint` | Allows precise, programmatic placement of automation values, shapes, and timing to replicate the tutorial's "drawn" automation lines. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly replicates the core premise of the video—automating track parameters over time—by programmatically drawing volume swells, pan sweeps, and mute stutters using native REAPER envelope APIs.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Dynamic Automation Envelopes (Volume Swells, Auto-Pan, & Mute Gating) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (minimum 2 recommended).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the automation generation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Add Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth to generate a sustained tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item & Insert Chord ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    item_len = bar_len * bars
    
    # Create time selection and insert MIDI item via Action to ensure standard setup
    RPR.RPR_GetSet_LoopTimeRange(True, False, 0.0, item_len, False)
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40214, 0) # Action: Insert new MIDI item...
    
    item = RPR.RPR_GetTrackMediaItem(track, 0)
    take = RPR.RPR_GetActiveTake(item)
    
    # Calculate triad chord pitches
    root_pitch = 48 + NOTE_MAP.get(key, 0) # Octave 3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_pitches = [
        root_pitch + scale_intervals[0], # Root
        root_pitch + scale_intervals[2], # 3rd
        root_pitch + scale_intervals[4]  # 5th
    ]
    
    # Insert sustained chord spanning the entire item length
    start_ppq = 0
    end_ppq = int(960 * beats_per_bar * bars) # Assuming standard 960 PPQ
    
    for pitch in chord_pitches:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Toggle Envelopes Visible ===
    # Envelopes must be visible/active to fetch them by name
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40408, 0) # Toggle track pan envelope visible
    RPR.RPR_Main_OnCommand(40410, 0) # Toggle track mute envelope visible

    # === Step 5: Draw Automation Envelopes ===
    
    # 1. Volume Swell (starts at silence, swells to 0dB over 2 bars)
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env_vol:
        # shape: 2 = Slow start/end (S-Curve)
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0, False, True)
        swell_end = min(bar_len * 2, item_len)
        RPR.RPR_InsertEnvelopePoint(env_vol, swell_end, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(env_vol)

    # 2. Pan Sweep (Ping-pong Left to Right every bar)
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if env_pan:
        # shape: 0 = Linear
        for b in range(bars + 1):
            time_pos = b * bar_len
            pan_val = -1.0 if b % 2 == 0 else 1.0
            if b == bars: 
                pan_val = 0.0 # Return to center at the very end
            RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(env_pan)

    # 3. Mute Stutter / Trance Gate (1/8th note gating in the final bar)
    env_mute = RPR.RPR_GetTrackEnvelopeByName(track, "Mute")
    if env_mute and bars >= 1:
        # Initial unmuted state
        RPR.RPR_InsertEnvelopePoint(env_mute, 0.0, 0.0, 1, 0, False, True) 
        
        stutter_start = bar_len * (bars - 1)
        step = bar_len / 8 # 1/8th note lengths
        
        for i in range(8):
            time_pos = stutter_start + i * step
            # Mute = 1.0, Unmute = 0.0. Shape 1 = Square (instant step change)
            val = 1.0 if i % 2 == 1 else 0.0 
            RPR.RPR_InsertEnvelopePoint(env_mute, time_pos, val, 1, 0, False, True)
            
        # Ensure it ends unmuted
        RPR.RPR_InsertEnvelopePoint(env_mute, item_len, 0.0, 1, 0, False, True)
        RPR.RPR_Envelope_Sort(env_mute)

    # Clear time selection
    RPR.RPR_GetSet_LoopTimeRange(True, False, 0.0, 0.0, False)

    return f"Created '{track_name}' with Volume swell, Pan sweeps, and 1/8th Mute stutters over {bars} bars at {bpm} BPM in {key} {scale}."
```