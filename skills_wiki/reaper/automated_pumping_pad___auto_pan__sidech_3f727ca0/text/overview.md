### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Pumping Pad & Auto-Pan (Sidechain Simulation)

* **Core Musical Mechanism**: This pattern utilizes REAPER's automation envelopes (specifically Track Volume and Pan) to programmatically draw rhythmic volume ducking and spatial movement. Instead of relying on a compressor sidechained to a kick drum, we draw the exact amplitude curve directly onto the track, creating a perfect "four-on-the-floor" volume pulse.
* **Why Use This Skill (Rationale)**: Automating volume and pan adds intense rhythmic groove and width to otherwise static, sustained sounds (like chords or pads). Volume ducking creates psychoacoustic space for a kick drum and imparts a "breathing" or "pumping" feeling. Sweeping the pan envelope slowly across the stereo field creates spatial evolution, keeping the listener engaged over longer progressions.
* **Overall Applicability**: This technique is ubiquitous in EDM, Future Bass, Lo-Fi Hip Hop, and Pop synth production. It is used to turn static synth layers into rhythmic, driving elements that lock perfectly into the track's tempo grid.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes music theory (building diatonic 7th chords based on scale degrees) alongside advanced mixing automation (mathematically precise 1/8th note sidechain volume curves and 2-bar LFO-style pan sweeps).

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature/Grid**: 4/4 grid.
  - **Envelope Rhythm**: The volume envelope drops sharply at the start of every downbeat (1, 2, 3, 4) and smoothly swells back to 0dB exactly halfway through the beat (the 1/8th off-beat).
  - **Pan Rhythm**: The pan envelope executes a slow, symmetrical sweep from Left to Right every 2 bars.
* **Step B: Pitch & Harmony**
  - **Scale/Key**: Parameterized (defaults to C minor).
  - **Progression**: A classic i7 - VImaj7 - IIImaj7 - VII7 chord progression. 
  - **Voicing**: 4-note diatonic chords calculated mathematically from the scale intervals, sustained for 1 entire bar each to maximize the effect of the volume pumping.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` to provide a dense, harmonically rich electronic pad.
* **Step D: Mix & Automation**
  - **Volume Automation**: Drops to 0.1 amplitude (-20dB) on the beat, swells to 1.0 amplitude (0dB) using Shape 2 (Slow Start/End).
  - **Pan Automation**: Oscillates between -0.7 (70% Left) and 0.7 (70% Right).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Progression | MIDI note insertion | Allows algorithmic generation of diatonic 7th chords based on user parameters. |
| Pad Sound | FX chain (`ReaSynth`) | Native, lightweight synth to provide immediate audio output for the envelopes to modulate. |
| Rhythmic Ducking | `RPR_InsertEnvelopePoint` on Volume | Exact, sample-accurate amplitude modulation mirroring the drawn automation from the tutorial. |
| Spatial Sweeps | `RPR_InsertEnvelopePoint` on Pan | Creates movement without needing LFO plugins, demonstrating spatial automation. |

> **Feasibility Assessment**: 100% reproducible. REAPER's API natively supports toggling track automation lanes and injecting precisely calculated time-value points into Volume and Pan envelopes.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Automated_Swell",
    track_name: str = "Pumping_Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Automated Pumping Pad with volume ducking and pan sweeps.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing what was created.
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

    # === Step 1: Initialize Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 2: Create Track and Synth ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item and Chords ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_scale_pitch(degree, root, intervals):
        octave = degree // len(intervals)
        idx = degree % len(intervals)
        return root + (octave * 12) + intervals[idx]

    # i - VI - III - VII progression
    chord_degrees = [0, 5, 2, 6] 
    root_val = NOTE_MAP.get(key.upper(), 0) + 48 # Base Octave 3

    note_count = 0
    for bar in range(bars):
        degree = chord_degrees[bar % len(chord_degrees)]
        start_sec = bar * bar_length_sec
        end_sec = start_sec + bar_length_sec
        
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        # Build 4-note diatonic 7th chords
        for i in [0, 2, 4, 6]: 
            pitch = get_scale_pitch(degree + i, root_val, scale_intervals)
            RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, pitch, velocity_base, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Write Automation Envelopes ===
    RPR.RPR_SetOnlyTrackSelected(track)
    
    # Volume Ducking (Sidechain pump on every downbeat)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        total_beats = bars * beats_per_bar
        for beat in range(total_beats):
            t_start = beat * (60.0 / bpm)
            t_off = t_start + (30.0 / bpm) # Halfway through the beat (1/8th note)
            
            # Shape 2 is "Slow start/end" which gives a smooth, sine-like swell curve
            # 0.1 amplitude = severe ducking, 1.0 amplitude = 0dB (full volume)
            RPR.RPR_InsertEnvelopePoint(vol_env, t_start, 0.1, 2, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(vol_env, t_off, 1.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(vol_env)

    # Spatial Panning (Sweep left to right)
    RPR.RPR_Main_OnCommand(40456, 0) # Toggle track pan envelope visible
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        sweep_len = bar_length_sec * 2 # Sweep back and forth every 2 bars
        num_sweeps = int(item_length / sweep_len)
        if num_sweeps == 0: num_sweeps = 1
        for i in range(num_sweeps + 1):
            t = i * sweep_len
            val = -0.7 if i % 2 == 0 else 0.7 # Alternate Left/Right by 70%
            RPR.RPR_InsertEnvelopePoint(pan_env, t, val, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(pan_env)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM, featuring rhythmic volume ducking and pan sweeping automation."
```