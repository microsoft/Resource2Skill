# Tearout Harmonic Fifth Bass (Intermodulation Bass)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Tearout Harmonic Fifth Bass (Intermodulation Bass)

* **Core Musical Mechanism**: The defining signature of this heavy, vocalic "tearout" bass is the generation of **intermodulation distortion**. This is achieved by taking a fundamental Saw wave and layering it with a Sine wave pitched up exactly +7 semitones (a perfect fifth), then running both through a short, plucky amplitude envelope directly into heavy tube/hard-clip distortion. 
* **Why Use This Skill (Rationale)**: When a root note and its perfect fifth are fed into a non-linear distortion algorithm, the distortion generates "sum and difference" tones (intermodulation). This creates extremely dense, growling lower harmonics that acoustic instruments cannot produce naturally. It is the acoustic equivalent of an electric guitar "power chord", but hyper-synthesized. Multiband compression (OTT-style) is then applied to flatten the dynamics, which brings out the crunchy, watery tails of the distortion.
* **Overall Applicability**: This technique is the cornerstone of modern dubstep, drum & bass, mid-tempo, and future bass drops (e.g., Skrillex, REAPER, Blanke). It works best as an aggressive off-beat rhythmic layer or a sustained drop bass.
* **Value Addition**: A standard synth bass simply plays a wave. This skill encodes the sound-design architecture needed for modern bass music: multi-oscillator harmonic staging, pre-distortion enveloping, and post-distortion multiband flattening. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 140–175 BPM (typically half-time feel).
  - **Rhythm Grid**: Heavily syncopated 1/8th and 1/16th notes.
  - **Duration**: Notes are short and plucky (staccato) to trigger the distortion impact, occasionally sustaining on the turnaround.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically Minor or Phrygian (D# minor is a staple for heavy sub-bass frequency response).
  - **Voicing**: The MIDI clip plays single root notes, but the *synth engine* internally voices a power chord (Root + Perfect 5th + Sub octave). 

* **Step C: Sound Design & FX**
  - **Oscillator 1**: Saw wave (fundamental punch).
  - **Oscillator 2**: Sine wave pitched +7 semitones (harmonic excitement).
  - **Sub Oscillator**: Square or Triangle pitched -12 semitones (weight).
  - **Envelope**: Fast attack (0ms), medium decay (250-300ms), low sustain (10%), fast release.
  - **Distortion**: Hard clipping or fuzz applied *after* the envelope so the distortion aggressively saturates the transient and cleans up on the decay.
  - **Compression**: OTT (Upward/Downward Multiband Compression) to squash the tail and make the distortion sound "flat" and massive.

* **Step D: Mix & Automation**
  - Narrow EQ peak on the 5th harmonic (to accentuate the "metallic/vocal" quality).
  - High shelf boost for crunch.
  - Stereo dimension (Chorus/Hyper-dimension) applied lightly on the top end to widen the bass without muddying the sub.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm / Syncopation | MIDI Note Insertion | Allows programmatic generation of a syncopated dubstep groove based on scale parameters. |
| Harmonic Staging (Root + 5th + Sub) | `ReaSynth` Parameters | ReaSynth natively includes a main pulse/saw osc, an "Extra Sine" osc, and an "Extra Triangle" osc, allowing us to build the exact 3-layer architecture in a single lightweight plugin. |
| Pre-Distortion Enveloping | `ReaSynth` ADSR | Sets the "pluck" shape *before* the signal hits the distortion plugins, crucial for the sound design. |
| Drive & Squash | `JS: distortion` + `ReaComp` | Simulates the Tube Distortion and OTT multiband flattening from the tutorial using stock plugins. |

> **Feasibility Assessment**: 85% — The core intermodulation distortion, harmonic staging, and rhythmic bounce are perfectly reproduced using REAPER stock plugins. The remaining 15% is the Kilohearts "Disperser" (all-pass filter transient smearing) and Vocodex processing, which are highly specific third-party DSPs that cannot be fully replicated with stock plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Tearout Fifth Bass",
    bpm: int = 150,
    key: str = "D#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 115,
    **kwargs,
) -> str:
    """
    Create a heavily distorted Tearout Intermodulation Bass in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., D# is optimal for sub weight).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # === Step 3: Add Instrument & FX Chain ===
    
    # 1. Synthesis Staging (Root Saw + 5th Sine + Sub Tri)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_synth >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 0, 0.7)    # Vol
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 1, 0.5)    # Tune (0)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.0)    # Attack (Fast)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.03)   # Decay (~300ms pluck)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 4, 0.1)    # Sustain (Low)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 5, 0.01)   # Release (Fast)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 7, 0.0)    # Main Osc: Saw shape
        # The Secret Sauce: 5th Harmonic Exciter
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 9, 0.7)    # Extra Sine Vol
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 10, 0.52916) # Extra Sine Tune (+7st)
        # Sub
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 11, 0.7)   # Extra Tri Vol
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 12, 0.45)  # Extra Tri Tune (-12st)

    # 2. Hard Distortion (To create intermodulation)
    fx_dist = RPR.RPR_TrackFX_AddByName(track, "JS: distortion", False, -1)
    if fx_dist >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_dist, 0, 0.7) # Push gain into clipper
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_dist, 1, 0.3) # Hard clip ceiling limit

    # 3. Flattening / OTT Squash
    fx_comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    if fx_comp >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 0, 0.2)  # Low Threshold
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 1, 0.9)  # High Ratio (Squash)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 2, 0.0)  # Fast Attack
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 3, 0.1)  # Fast Release
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_comp, 8, 0.7)  # Output gain makeup

    # 4. EQ (Boost 5th harmonic & top end crunch)
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    if fx_eq >= 0:
        # Band 3 (Peak for vocalic tone)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq, 6, 0.65) # Freq ~1.5kHz
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq, 7, 0.65) # Gain Boost
        # Band 4 (High Shelf for noise/distortion tail)
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq, 9, 0.8)  # Freq ~8kHz
        RPR.RPR_TrackFX_SetParamNormalized(track, fx_eq, 10, 0.65) # Gain Boost

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Base octave for heavy bass is typically C1 to C2 (MIDI 24 - 36)
    root_midi = 24 + NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else "D#", 3)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Syncopated rhythm pattern: (beat_start, length_in_beats, scale_degree)
    rhythm_pattern = [
        (0.0,  0.5,  0), # Downbeat hit
        (0.75, 0.25, 0), # 16th syncopation
        (1.5,  0.5,  0), # Offbeat before snare
        (2.5,  0.5,  0), # Offbeat after snare
        (3.5,  0.5,  0)  # Turnaround hit
    ]

    note_count = 0
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        for beat_start, length_beats, degree in rhythm_pattern:
            
            # Subtle pitch movement: pop up a minor 3rd at the end of every other bar
            current_degree = degree
            if bar % 2 == 1 and beat_start > 2.0:
                current_degree = 2 # Usually a minor 3rd in minor scale
                
            note_pitch = root_midi + scale_intervals[current_degree % len(scale_intervals)]
            
            start_time_sec = (bar_offset_beats + beat_start) * (60.0 / bpm)
            end_time_sec = start_time_sec + (length_beats * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            # Slight velocity humanization for the syncopated 16th hit
            vel = velocity_base if length_beats >= 0.5 else int(velocity_base * 0.85)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, note_pitch, vel, False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' generating {note_count} tearout bass hits over {bars} bars at {bpm} BPM in {key} {scale}."
```