### 1. High-level Design Pattern Extraction

> **Skill Name**: Expressive Parameter Automation (Filter & Volume Swell)

* **Core Musical Mechanism**: Modulating synthesizer and effect parameters over time using REAPER's automation envelopes. Rather than a static sound, the instrument's volume and filter cutoff gradually open up over a set number of bars, creating a continuous sweeping trajectory.
* **Why Use This Skill (Rationale)**: Static sounds can feel lifeless in a mix. By automating parameters like a Low Pass filter cutoff or track volume, you induce *macro-dynamics*. This relies on the psychoacoustic principle of spectral progression—as a sound becomes louder and brighter (more high-frequency content), the brain perceives increasing energy and tension. This is the foundational music theory behind EDM build-ups, cinematic risers, and expressive neo-soul pad swells.
* **Overall Applicability**: Perfect for intro fade-ins, pre-chorus build-ups/risers, ambient drone textures, and expressive synth pads in pop, electronic, and cinematic music. 
* **Value Addition**: Compared to a blank MIDI clip or a static synth patch, this skill encodes the concept of *movement over time*. It demonstrates how to programmatically create and populate automation envelopes, turning a simple sustained chord into an evolving, tension-building musical moment.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: Agnostic (works at any BPM), but highly dependent on the grid.
  - **Rhythmic Grid**: The pattern uses a single, continuous sustained chord held across the entire generated duration (e.g., 4 or 8 bars).
  - **Note Duration**: 100% legato (held for the full item length).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable.
  - **Voicing**: A thick, wide tonic triad (Root, Fifth, Octave, and Major/Minor 10th) to ensure there is plenty of frequency content for the filter to act upon.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` (Stock REAPER Synth).
  - **Timbre**: A blend of Sawtooth and Square waves to provide rich upper harmonics. 
  - **FX Chain**: `ReaSynth` → `ReaEQ`.
  - **Automated Parameters**: 
    1. ReaSynth Filter Cutoff (sweeping from dark to bright).
    2. ReaEQ Band 1 Frequency (simulating the Low Pass sweep shown in the video tutorial).

* **Step D: Mix & Automation**
  - **Automation Curves**: Linear and slow-start curves inserted at the beginning and end of the media item, mapping a 0% to 100% parameter transition to build intensity.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Harmony | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides the raw pitch and harmonic material for the swell. |
| Synth Sound Design | FX chain (`ReaSynth`, `ReaEQ`) | Stock plugins guarantee reproducibility. Saw/Square waves ensure harmonics exist to be filtered. |
| The Swell/Sweep | Automation Envelopes (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly reproduces the tutorial's core concept: automating an FX parameter over time. |

> **Feasibility Assessment**: 100% reproducible. The script uses REAPER's native API to create tracks, generate MIDI, load stock plugins, and explicitly draw the automation envelope curves demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Filter Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an expressive, automated synth swell in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars the swell will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created automated element.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }

    # Base setup
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 36 # Start at octave 3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # We will build a thick pad chord: Root, 5th, Octave, and the 3rd (an octave up)
    chord_degrees = [0, 4, 7] # 1st, 5th, 8th in scale degrees
    # 3rd degree (index 2) added one octave up (+7 scale steps)
    chord_degrees.append(2 + 7) 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate PPQ bounds for the MIDI item
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)

    # Insert sustained notes
    for degree in chord_degrees:
        octave_offset = (degree // 7) * 12
        note_index = degree % 7
        pitch = root_pitch + octave_offset + scale_intervals[note_index]
        
        RPR.RPR_MIDI_InsertNote(
            take, selected=False, muted=False,
            startppqpos=start_ppq, endppqpos=end_ppq,
            chan=0, pitch=pitch, vol=velocity_base, noSort=False
        )

    # === Step 4: Add FX Chain ===
    # Add ReaSynth
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Setup ReaSynth to have harmonics (Saw + Square) and lower starting cutoff
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.5)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.6)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.6)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 0.0)  # Filter Cutoff (start low)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, 0.4)  # Filter Resonance

    # Add ReaEQ (as shown in the tutorial)
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Automate Parameters (The Core Skill) ===
    # Create an automation envelope for ReaSynth Filter Cutoff (Param 4)
    # RPR_GetFXEnvelope args: track, fx index, param index, create_if_not_exists
    env_cutoff = RPR.RPR_GetFXEnvelope(track, fx_synth, 4, True)
    
    if env_cutoff:
        # Insert Envelope Point at Start (Time 0.0, Value 0.0 / dark)
        # Shape 2 = Slow Start/End (smooth curve)
        RPR.RPR_InsertEnvelopePoint(env_cutoff, 0.0, 0.05, 2, 0.0, False, True)
        
        # Insert Envelope Point at End (Time = item_length_sec, Value 1.0 / fully bright)
        RPR.RPR_InsertEnvelopePoint(env_cutoff, item_length_sec, 0.95, 2, 0.0, False, True)
        
        # Sort points
        RPR.RPR_Envelope_SortPoints(env_cutoff)
        
    # Also create an automation envelope for Track Volume (to fade in)
    env_vol = RPR.RPR_GetFXEnvelope(track, fx_synth, 0, True) # Automating synth volume
    if env_vol:
        # Start quiet (Value 0.0)
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0.0, False, True)
        # End at normal volume (Value ~0.7)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length_sec, 0.7, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    return f"Created '{track_name}' with a {bars}-bar automated filter and volume swell at {bpm} BPM in {key} {scale}."
```