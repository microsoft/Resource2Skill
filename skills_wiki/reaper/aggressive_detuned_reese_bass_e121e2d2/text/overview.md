# Aggressive Detuned Reese Bass

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Aggressive Detuned Reese Bass

* **Core Musical Mechanism**: The signature sound of a modern "Reese" bass relies on **phase friction and non-linear distortion**. By taking two or more identical waveforms (usually saw waves) and slightly detuning them against each other, you create continuous phase cancellation and "beating." When this beating, undulating signal is driven into a heavy distortion or overdrive, the harmonic profile constantly shifts, creating a "tearing" or "growling" texture. Virtual Riot highlights that applying movement effects (like choruses or notch filters) *before* the final distortion stage makes this tearing effect even more aggressive and vocal-like.

* **Why Use This Skill (Rationale)**: This technique capitalizes on psychoacoustics and frequency masking. A single saw wave is static and easily masked by other elements. Multiple detuned saw waves create a wide stereo image and continuous movement, drawing the ear's attention. Driving this into distortion acts as a form of extreme harmonic compression—the fundamental frequencies squash together, while rich upper harmonics are generated, ensuring the bass translates clearly even on small speakers (like phones or laptops).

* **Overall Applicability**: This pattern is a staple in Electronic Dance Music (EDM), particularly Dubstep, Drum & Bass, Future Bass, and Midtempo. It is typically used for drop basslines, heavy sustained intros, or cinematic lower-register pads.

* **Value Addition**: A standard MIDI clip with a single synth patch sounds thin and generic. This skill encodes the sound design architecture required to build a dense, professional bass patch entirely from scratch, utilizing multi-oscillator summing and a specific, ordered FX chain to create complex timbral friction.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 140–150 BPM (Dubstep) or 170–174 BPM (Drum & Bass).
  - **Rhythm**: Legato (notes touching or overlapping). The continuous sound is crucial so the phase beating never stops abruptly.
  - **Grid**: 1 bar or 1/2 bar sustained notes.

* **Step B: Pitch & Harmony**
  - **Register**: Very low. Sub/bass octaves (C1 to C2, MIDI notes 24-36).
  - **Harmony**: Usually plays the root notes of the underlying chord progression.
  - **Movement**: Often employs portamento (glide) so pitch slides smoothly between notes, causing the "beating" speed to accelerate/decelerate (as Virtual Riot demonstrates in Method 1).

* **Step C: Sound Design & FX**
  - **Oscillators**: 3x Saw waves. Center (0 cents), Left/Up (+15 cents), Right/Down (-15 cents).
  - **Pre-FX**: Dimension expander, chorus, or flanger to smear the phase relationships.
  - **Distortion**: Multiband distortion, overdrive, or wave-shaping to crush the phase differences into aggressive harmonics.
  - **Filtering**: Moving notch filters (to create "AEE-YAA" vocal formant movements).
  - **Post-FX**: Heavy compression or limiting to flatten the dynamics and maximize loudness.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Phase Friction (Detuning) | FX Chain (Multiple `ReaSynth` instances) | Simulates a multi-oscillator synth (like Serum). REAPER processes FX in series/parallel natively. 3 ReaSynths on one track will sum their audio, allowing us to perfectly mimic detuned oscillators. |
| Harmonic Tearing | `JS: Distortion` & `JS: Chorus` | Chorus provides the "dimension" movement, and driving it into the JS distortion creates the aggressive crunch Virtual Riot achieved with external plugins. |
| Legato Bassline | MIDI note insertion | Allows us to define continuous, full-bar notes programmatically based on the requested key and scale. |

> **Feasibility Assessment**: 85%. While we cannot execute external third-party VSTs (like Xfer Serum used in the tutorial's Methods 2 & 3), we can perfectly recreate the *signal flow and physics* of a Detuned Reese using REAPER's stock `ReaSynth` and JSFX suite. The exact tone of the distortion will differ from Serum's specific algorithms, but the mechanical principle (detuned saws -> chorus -> distortion -> compression) is faithfully reproduced.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "VirtualRiot_Reese",
    track_name: str = "Detuned Reese Bass",
    bpm: int = 140,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates an aggressive, detuned Reese bass utilizing multi-oscillator 
    phase friction and heavy distortion, mimicking Virtual Riot's Reese techniques.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track.
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
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Sound Design / FX Chain Generation ===
    # To create the "Detuned Reese", we stack 3 ReaSynths. 
    # ReaSynth passes audio through, meaning they will sum together.
    
    # Osc 1: Center Saw
    rs1 = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, rs1, 0, 0.4)  # Vol
    RPR.RPR_TrackFX_SetParamNormalized(track, rs1, 1, 0.5)  # Tuning (center)
    RPR.RPR_TrackFX_SetParamNormalized(track, rs1, 7, 0.0)  # Sine mix 0
    RPR.RPR_TrackFX_SetParamNormalized(track, rs1, 9, 1.0)  # Saw mix 100%

    # Osc 2: Sharp Saw (+15 cents)
    rs2 = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, rs2, 0, 0.3)  # Slightly quieter
    RPR.RPR_TrackFX_SetParamNormalized(track, rs2, 1, 0.5015) # Detune UP
    RPR.RPR_TrackFX_SetParamNormalized(track, rs2, 7, 0.0)  
    RPR.RPR_TrackFX_SetParamNormalized(track, rs2, 9, 1.0)  

    # Osc 3: Flat Saw (-15 cents)
    rs3 = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, rs3, 0, 0.3)  
    RPR.RPR_TrackFX_SetParamNormalized(track, rs3, 1, 0.4985) # Detune DOWN
    RPR.RPR_TrackFX_SetParamNormalized(track, rs3, 7, 0.0)  
    RPR.RPR_TrackFX_SetParamNormalized(track, rs3, 9, 1.0)  

    # Movement Effect: Chorus (adds width and phase smearing before distortion)
    chorus = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus, 2, 0.6) # Depth
    RPR.RPR_TrackFX_SetParamNormalized(track, chorus, 3, 0.4) # Rate

    # Aggressive Distortion: Squashes the detuned waveforms together to create harmonic tearing
    dist = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, dist, 0, 0.8) # High Drive

    # Post-Compression: Flatten dynamics
    comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, comp, 0, 0.2) # Low Threshold
    RPR.RPR_TrackFX_SetParamNormalized(track, comp, 1, 0.8) # High Ratio (Limit)

    # === Step 4: Create MIDI Item & Legato Bassline ===
    # 1 bar per note for a heavy, sustained drop feel
    beats_per_bar = 4
    ppq_per_beat = 960 
    ppq_per_bar = beats_per_bar * ppq_per_beat
    
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate pitches in Sub/Bass octave (Octave 1: MIDI 24-35)
    root_val = NOTE_MAP.get(key, 0)
    base_pitch = 24 + root_val 
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Common EDM heavy bass progression: i - VI - iv - v (in root scale degrees)
    # E.g. in F minor: F - Db - Bb - C
    progression_degrees = [0, 5, 3, 4] 
    
    for i in range(bars):
        degree_idx = progression_degrees[i % len(progression_degrees)]
        
        # Wrap octave if degree index exceeds scale length (though these are all < 7)
        octave_shift = degree_idx // len(scale_intervals)
        rem_idx = degree_idx % len(scale_intervals)
        
        pitch = base_pitch + scale_intervals[rem_idx] + (octave_shift * 12)
        
        start_ppq = i * ppq_per_bar
        end_ppq = (i + 1) * ppq_per_bar  # Legato: note ends exactly when the next begins
        
        RPR.RPR_MIDI_InsertNote(
            take, False, False, 
            start_ppq, end_ppq, 
            0, int(pitch), velocity_base, True
        )

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' (Detuned Reese) with 3x Oscillators and FX over {bars} bars at {bpm} BPM."
```