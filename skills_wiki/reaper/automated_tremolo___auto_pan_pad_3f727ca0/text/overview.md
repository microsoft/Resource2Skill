### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Tremolo & Auto-Pan Pad

* **Core Musical Mechanism**: Modulating a track's volume and stereo panning over time using mathematically generated, tempo-synced automation envelopes. By using "Slow Start/End" (S-Curve) envelope points, we replicate the smooth, freehand sine-wave automation drawn in the tutorial.
* **Why Use This (Rationale)**: Static sustained sounds (like synth pads or held guitar chords) can quickly make a mix feel stagnant. By programmatically automating volume and pan, we introduce rhythmic groove (tremolo) and stereo width (auto-pan). Using automation envelopes instead of LFO plugins provides absolute visual control, precise tempo-sync, and the ability to manually tweak individual swells later in the arrangement.
* **Overall Applicability**: This technique is universally applicable for transitioning sections, creating rhythmic pulsing in ambient music, adding stereo interest to lo-fi hip-hop electric pianos, or building tension leading into an EDM drop.
* **Value Addition**: Transforms a flat, lifeless MIDI chord into an evolving, rhythmic texture. It encodes the knowledge of how to interact with REAPER's automation lanes programmatically, bypassing manual fader riding while maintaining perfect grid sync.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid Divisions**: The volume oscillates rapidly every 1/8th note (creating a rhythmic stutter/tremolo). The pan oscillates slowly every 1/2 note (sweeping the stereo field).
  - **Envelope Shapes**: Uses S-Curves (REAPER shape `2`) between min/max points to create smooth, natural-sounding sine waves rather than harsh, robotic linear jumps.

* **Step B: Pitch & Harmony**
  - **Voicing**: Generates a dense 7th chord (Root, 3rd, 5th, 7th) sustained over the entire duration of the generated item.
  - **Scale Mapping**: Dynamically calculates the correct scale degrees based on the provided key and scale parameters to ensure harmonic compliance.

* **Step C: Sound Design & FX**
  - **Instrument**: Uses REAPER's native `ReaSynth` to generate the raw tone.
  - **Spatial FX**: Adds `ReaVerbate` with a high wet mix to wash the raw synth tone out into a wide, atmospheric pad.

* **Step D: Mix & Automation**
  - **Volume Envelope**: Oscillates between `1.0` (0 dB) and `0.25` (-12 dB) to create a deep tremolo effect without fully dropping to silence.
  - **Pan Envelope**: Oscillates between `-0.8` (80% Left) and `0.8` (80% Right) to move the sound across the stereo image.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Pad | MIDI note insertion + ReaSynth | Provides a sustained, tonal foundation for the automation to act upon. |
| Fader Riding / Swells | Volume Automation Envelope | Directly replicates the tutorial's demonstration of drawing a volume sine wave, perfectly synced to the BPM grid. |
| Stereo Movement | Pan Automation Envelope | Replicates the tutorial's secondary demonstration of automating the pan fader. |

> **Feasibility Assessment**: 100% reproducible. REAPER's API provides robust access to track envelopes, allowing us to programmatically insert the exact curve shapes demonstrated by the instructor's mouse movements.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Tremolo Pan Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained synth pad with synchronized Volume and Pan automation.

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
        Status string describing the created automated track.
    """
    import reaper_python as RPR

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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add FX (ReaSynth for tone, ReaVerbate for pad texture)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    # Make the verb very wet for a pad sound (Param 0 = Wet, Param 1 = Dry)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb, 0, 0.8)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb, 1, 0.4)

    # === Step 3: Create Sustained MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Build 7th chord based on the selected scale
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)
    octave = 48 # C3
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th

    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for i, deg in enumerate(chord_degrees):
        octave_shift = (deg // scale_len) * 12
        note_in_scale = scale_intervals[deg % scale_len]
        pitch = octave + root_val + octave_shift + note_in_scale
        
        vel = max(10, velocity_base - (i * 10)) # Softer upper velocities
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Generate Volume Automation (1/8th Note Tremolo) ===
    # Guarantee envelope exists by selecting track and toggling visibility
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not env_vol:
        RPR.RPR_SetOnlyTrackSelected(track)
        RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
        env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")

    if env_vol:
        RPR.RPR_DeleteEnvelopePointRange(env_vol, 0.0, item_length + 1.0)
        eighth_note_len = beat_length_sec / 2.0
        num_vol_points = int(item_length / eighth_note_len)
        
        for i in range(num_vol_points + 1):
            time_pos = i * eighth_note_len
            vol_val = 1.0 if (i % 2 == 0) else 0.25 # Oscillate 0dB to -12dB
            # Shape 2 = Slow start/end (S-Curve) to create a smooth sine wave
            RPR.RPR_InsertEnvelopePoint(env_vol, time_pos, vol_val, 2, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(env_vol)

    # === Step 5: Generate Pan Automation (1/2 Note Sweeps) ===
    env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if not env_pan:
        RPR.RPR_SetOnlyTrackSelected(track)
        RPR.RPR_Main_OnCommand(40407, 0) # Track: Toggle track pan envelope visible
        env_pan = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")

    if env_pan:
        RPR.RPR_DeleteEnvelopePointRange(env_pan, 0.0, item_length + 1.0)
        half_note_len = beat_length_sec * 2.0
        num_pan_points = int(item_length / half_note_len)
        
        for i in range(num_pan_points + 1):
            time_pos = i * half_note_len
            pan_val = -0.8 if (i % 2 == 0) else 0.8 # Oscillate 80% L to 80% R
            # Shape 2 = Slow start/end (S-Curve)
            RPR.RPR_InsertEnvelopePoint(env_pan, time_pos, pan_val, 2, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(env_pan)

    return f"Created '{track_name}': {bars} bars of automated S-Curve Tremolo and Auto-Pan at {bpm} BPM."
```