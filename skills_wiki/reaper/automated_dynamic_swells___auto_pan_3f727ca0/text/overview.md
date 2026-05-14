### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Dynamic Swells & Auto-Pan

* **Core Musical Mechanism**: The programmatic generation of track automation envelopes (Volume and Pan) to introduce rhythmic movement into an otherwise static sound. This reproduces the manual "Write/Touch" fader-riding techniques demonstrated in the tutorial, but executes them with mathematical precision to create a recurring sine-wave-like tremolo and auto-pan effect.
* **Why Use This Skill (Rationale)**: Sustained sounds (like synth pads or drones) can quickly become fatiguing and consume static space in a mix. By automating volume in an S-curve, we simulate the "breathing" of an acoustic instrument or a sidechain compression pump. Simultaneously automating pan creates spatial width, pulling the listener's ear across the stereo field and preventing masking with center-panned elements like kick, snare, or lead vocals.
* **Overall Applicability**: Perfect for background pads, ambient textures, riser/transition effects, or taking a boring mono synth and turning it into a wide, rhythmic groove element.
* **Value Addition**: Transforms a block of static MIDI chords into a dynamic, mixed element that evolves over time. It encodes the REAPER API knowledge required to expose and manipulate underlying track envelopes natively.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: The volume swells follow a half-bar rhythm (1/2 note pulse). The volume is lowest at the downbeat (beat 1), peaks at the middle of the bar (beat 3), and fades out towards the next downbeat. 
  - **Pan Sweep**: The panning moves at half the speed of the volume, taking a full bar to sweep Left, and a full bar to sweep Right.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parameterized.
  - **Progression**: Generates a classic 4-bar sustained chord progression based on scale degrees `[i, VI, III, VII]` to provide a lush harmonic bed that highlights the envelope movement.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` to generate a pure, sustained tone. 

* **Step D: Mix & Automation**
  - **Volume Envelope**: Points inserted at the start, mid, and end of each bar. Values range from `0.1` (quiet) to `0.8` (loud). Curve shape is set to `2` (Slow start/end) to mimic the smooth fader riding seen in the video.
  - **Pan Envelope**: Points inserted at the start of each bar. Values alternate between `-0.8` (Left) and `0.8` (Right) using the same smooth curve shape.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Bed | `RPR_CreateNewMIDIItemInProj` & `RPR_MIDI_InsertNote` | Provides a sustained audio source to actually hear the automation working. |
| Instrument | `RPR_TrackFX_AddByName` | Adds REAPER's native ReaSynth for immediate audio output. |
| Volume/Pan Envelopes | `RPR_GetTrackEnvelopeByName` & `RPR_InsertEnvelopePoint` | Programmatically recreates the real-time fader riding (Write/Touch automation modes) demonstrated by Kenny Gioia, ensuring perfect rhythmic sync. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly simulates the "Draw a sine wave on the envelope" and "Ride the faders" techniques shown in the tutorial using native REAPER API envelope functions.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Pad Swells",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a sustained chord progression with rhythmic Volume and Pan automation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
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

    # === Step 3: Create Harmonic Bed (MIDI Chords) ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    
    # Generate 3 octaves of the scale
    scale_notes = []
    for oct in range(3):
        for interval in intervals:
            scale_notes.append(root_val + interval + (oct * 12))
            
    # Chord progression degrees: i - VI - III - VII
    chord_progression = [0, 5, 2, 6]
    note_count = 0
    
    for b in range(bars):
        degree = chord_progression[b % len(chord_progression)]
        
        # Build a basic triad in the 4th octave (MIDI ~48)
        chord_notes = [
            scale_notes[degree] + 48,      # Root
            scale_notes[degree + 2] + 48,  # Third
            scale_notes[degree + 4] + 48   # Fifth
        ]
        
        start_sec = b * bar_length_sec
        end_sec = start_sec + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        for pitch in chord_notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 5: Automate Volume & Pan ===
    # Select the track to ensure visibility toggles target the correct track
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Expose envelopes using native actions
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40456, 0) # Track: Toggle track pan envelope visible
    
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    
    shape_slow_start_end = 2 # S-curve shape mimicking smooth fader movements
    
    for b in range(bars):
        bar_start = b * bar_length_sec
        bar_mid = bar_start + (bar_length_sec / 2.0)
        bar_end = bar_start + bar_length_sec
        
        # Swell Volume (Quiet -> Loud -> Quiet)
        if vol_env:
            RPR.RPR_InsertEnvelopePoint(vol_env, bar_start, 0.1, shape_slow_start_end, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(vol_env, bar_mid, 0.8, shape_slow_start_end, 0.0, False, True)
            # Ensure the final point drops back down
            if b == bars - 1:
                RPR.RPR_InsertEnvelopePoint(vol_env, bar_end, 0.1, shape_slow_start_end, 0.0, False, True)
                
        # Sweep Pan (Alternating Left and Right)
        if pan_env:
            pan_val = -0.8 if b % 2 == 0 else 0.8
            next_pan_val = 0.8 if b % 2 == 0 else -0.8
            RPR.RPR_InsertEnvelopePoint(pan_env, bar_start, pan_val, shape_slow_start_end, 0.0, False, True)
            if b == bars - 1:
                RPR.RPR_InsertEnvelopePoint(pan_env, bar_end, next_pan_val, shape_slow_start_end, 0.0, False, True)
                
    if vol_env:
        RPR.RPR_Envelope_SortPoints(vol_env)
    if pan_env:
        RPR.RPR_Envelope_SortPoints(pan_env)

    return f"Created '{track_name}' with {note_count} MIDI notes and programmed Volume/Pan automation sweeps over {bars} bars at {bpm} BPM."
```