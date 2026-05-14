# Procedural Volume Ducking (Pseudo-Sidechain) via Automation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Procedural Volume Ducking (Pseudo-Sidechain) via Automation

* **Core Musical Mechanism**: Automating the primary track volume envelope to create rhythmic "ducking" or "pumping." The script programmatically mimics the result of writing an aggressive volume fader pass using "Write" or "Touch" automation modes, dipping the volume on the downbeat and recovering on the off-beat.
* **Why Use This Skill (Rationale)**: This creates intense rhythmic movement and groove without requiring an actual sidechain compressor setup or a trigger track. By directly writing volume envelope points, you eliminate plugin latency and gain absolute, sample-accurate control over the "pump" curve (the equivalent of a compressor's attack/release). Musically, it ensures sustained elements (like pads or noise) get out of the way of the kick drum (reducing frequency masking) while driving the track forward.
* **Overall Applicability**: Essential for Electronic Dance Music (EDM), Future Bass, House, and Lo-Fi Hip Hop where sustained layers need to breathe rhythmically with the drums. 
* **Value Addition**: Instead of manually drawing dozens of points with the mouse or meticulously recording fader rides over a time selection, this skill calculates precise rhythmic subdivisions based on the BPM and generates the entire automation curve instantly.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - 4/4 time signature.
  - Ducking occurs exactly on the quarter note (every downbeat).
  - Recovery peaks on the 8th note off-beat (exactly 50% through the beat length).
* **Step B: Pitch & Harmony**
  - Uses the input key/scale.
  - Generates a sustained 7th chord (root, 3rd, 5th, 7th) covering the entire item duration to clearly demonstrate the volume pumping effect.
* **Step C: Sound Design & FX**
  - Uses `ReaSynth` to generate a raw synthesized tone.
* **Step D: Mix & Automation**
  - The primary Track Volume Envelope is toggled visible and armed.
  - Envelope values use the linear amplitude scale: `0.15` (approx -16dB) on the downbeat, ramping back to `1.0` (0dB) by the 8th note.
  - Point shapes: Shape `2` (Slow Start/End) is used for the ducking recovery to create a smooth, S-shaped curve resembling an organic compressor release. Shape `0` (Linear) holds the volume steady until the next beat.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sustained Pad Chords | MIDI note insertion | Generates a constant sound source required to actually hear the volume modulation. |
| Sound Source | FX chain (ReaSynth) | Provides a quick, built-in tone generator without external dependencies. |
| Pumping Effect | Automation envelope | Directly applies the concepts of Track Volume Automation shown in the tutorial, allowing sample-accurate manipulation of the mix fader level over time. |

> **Feasibility Assessment**: 100% reproduction of the core concept. While the tutorial focuses on manipulating UI elements to record fader movements, this script directly achieves the exact mathematical outcome (a populated volume envelope) programmatically.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Procedural Volume Ducking (Pseudo-Sidechain) via Automation in the current REAPER project.

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
        Status string describing what was created.
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
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item & Chords ===
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_length_sec = beat_len * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Calculate chord pitches (Root, 3rd, 5th, 7th)
    root_val = NOTE_MAP.get(key, 0) + 48 # Base octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    chord_degrees = [0, 2, 4, 6]
    ppq_length = bars * beats_per_bar * 960
    
    # Insert sustained notes
    for deg in chord_degrees:
        octave_shift = deg // len(scale_intervals)
        note_idx = deg % len(scale_intervals)
        pitch = root_val + scale_intervals[note_idx] + (octave_shift * 12)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, float(ppq_length), 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Generate Volume Automation (Sidechain Pump) ===
    # Attempt to get the envelope. If it doesn't exist, force it visible to create the chunk.
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if env == 0:
        RPR.RPR_Main_OnCommand(40297, 0) # Track: Unselect all tracks
        RPR.RPR_SetTrackSelected(track, True)
        RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
        env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
        
    if env != 0:
        total_beats = bars * beats_per_bar
        for b in range(total_beats + 1):
            t_beat = b * beat_len
            
            if b < total_beats:
                if b > 0:
                    # Point right before the drop to hold the volume at 0dB (Shape 0 = Linear)
                    t_pre = t_beat - 0.01
                    RPR.RPR_InsertEnvelopePoint(env, t_pre, 1.0, 0, 0.0, False, True)
                
                # Drop to ~ -16dB exactly on the beat (Shape 2 = Slow Start/End creates an S-curve release)
                RPR.RPR_InsertEnvelopePoint(env, t_beat, 0.15, 2, 0.0, False, True)
                
                # Recover volume fully by the 8th note
                t_mid = t_beat + (beat_len * 0.5)
                RPR.RPR_InsertEnvelopePoint(env, t_mid, 1.0, 0, 0.0, False, True)
            else:
                # Close the envelope at the end of the item
                RPR.RPR_InsertEnvelopePoint(env, t_beat, 1.0, 0, 0.0, False, True)
                
        # Sort envelope points to apply changes
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with sustained {key} {scale} chord and automated volume ducking over {bars} bars at {bpm} BPM."
```