# Complementary EQ & Frequency Unmasking (Kick/Bass Separation)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Complementary EQ & Frequency Unmasking (Kick/Bass Separation)

* **Core Musical Mechanism**: The pattern revolves around identifying and resolving frequency collisions (masking) in the low-end of a mix using complementary EQ. By visually analyzing where instruments overlap (e.g., Kick and Bass both heavily occupying 70Hz-150Hz), you carve out dedicated "pockets" for each element. When one track is boosted at a specific fundamental frequency, the competing track is severely cut at that exact same frequency.
* **Why Use This Skill (Rationale)**: Low-frequency sound waves carry massive physical energy. When a Kick drum and a Bass synth hit simultaneously and share the exact same frequency band, their waveforms interact unpredictably—sometimes summing to eat up all your mix headroom, and sometimes phase-canceling to eliminate the low-end entirely. Complementary EQ solves this by assigning specific roles: e.g., the Kick controls the 75Hz "sub/thump", while the Bass is shifted slightly higher to the 130Hz "punch/body".
* **Overall Applicability**: This technique is mandatory in any genre with heavy, driving low-end arrangements (EDM, Hip-Hop, Pop, Rock, and Metal). It is usually applied during the mid-stages of mixing when balancing the rhythm section, or when setting up Sidechain/Mid-Side EQ processing to keep the mono channel tight.
* **Value Addition**: A blank MIDI clip provides no mix clarity. This skill encodes professional mixing intuition: it sets up a foundational rhythmic groove and automatically applies precisely mathematically calculated EQ bands to ensure the instruments fit together like puzzle pieces instead of muddying the master bus.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Time signature is 4/4.
  - Kick drum operates on a "Four-on-the-Floor" grid (1/4 notes).
  - Bass operates on driving 1/8th notes. Since the Bass plays on the downbeats simultaneously with the Kick, frequency masking is intentionally maximized, making the complementary EQ essential.
* **Step B: Pitch & Harmony**
  - Bass follows a classic minor scale progression (i - VI - III - VII).
  - Pitch relies on sub/low octaves (MIDI notes 24-45).
* **Step C: Sound Design & FX**
  - **Instruments**: `ReaSynth` used as a sound-generator scaffold for both elements.
  - **FX Chain**: `ReaEQ` is applied to both tracks with mirrored, complementary settings.
  - **Kick EQ Parameters**: 
    - Band 1: +6dB Boost at ~75Hz (Sub impact).
    - Band 2: -6dB Cut at ~130Hz (Clearing room for the bass).
  - **Bass EQ Parameters**:
    - Band 1: Deep Low-Shelf Cut (-24dB) at ~75Hz (Yielding the sub to the kick).
    - Band 2: +6dB Boost at ~130Hz (Adding body/punch to the bass).
    - Band 3: +4dB Boost at ~1kHz (Adding articulation so the bass is audible on small speakers).
* **Step D: Mix & Automation (if applicable)**
  - No automation needed here; the static complementary EQ curves handle the separation inherently.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm / Harmonic Interaction | MIDI note insertion | Guarantees exact temporal overlap (Kick and Bass hitting on the downbeats) to demonstrate the masking effect. |
| Frequency Unmasking | FX chain (`ReaEQ`) | ReaEQ is perfectly suited for parametric carving. We compute the normalized float values for frequencies and gain to instantly apply the mix decisions from the tutorial. |
| Sound Generators | `ReaSynth` | Stock REAPER plugin provides immediate audio tones in the sub-frequencies so the EQ separation is audible without needing 3rd-party drum samples. |

> **Feasibility Assessment**: 85% reproduction of the core musical concept. The video relies on third-party visualizers (Voxengo SPAN, Melda MMultiAnalyzer) and complex Mid/Side VST configurations. Since we must remain entirely within stock REAPER without external dependencies, we approximate the *result* of the visual analysis using precise `ReaEQ` parametric moves and stock synthesis. The Mid/Side side-channel high-pass concept is described above, but the code focuses on the primary Kick/Bass unmasking.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Unmasking_Mix",
    track_name: str = "Unmasking",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Kick and Bass groove with Complementary EQ to resolve frequency masking.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key, 0)
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Prog: i - VI - III - VII (indices: 0, 5, 2, 4 in minor)
    progression = [0, 5, 2, 4] if len(scale_intervals) >= 7 else [0, 0, 0, 0]

    # --- TRACK 1: KICK ---
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_kick = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_kick, "P_NAME", f"{track_name}_Kick", True)

    item_length = (60.0 / bpm) * 4 * bars
    item_kick = RPR.RPR_AddMediaItemToTrack(track_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", item_length)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)
    
    # 4-on-the-floor Kick
    for i in range(bars * 4): 
        start_time = i * (60.0 / bpm)
        end_time = start_time + (60.0 / bpm) * 0.15 # Staccato hit
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, end_time)
        RPR.RPR_MIDI_InsertNote(take_kick, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take_kick)

    # Kick FX Setup
    RPR.RPR_TrackFX_AddByName(track_kick, "ReaSynth", False, -1)
    fx_kick_eq = RPR.RPR_TrackFX_AddByName(track_kick, "ReaEQ", False, -1)
    
    # ReaEQ Parameter logic: Freq is log scaled roughly: val = log(Hz/20)/log(24000/20)
    # 75Hz ~ 0.186, 130Hz ~ 0.264
    # Gain is 0.0 to 1.0 (0.5 = 0dB). +6dB ~ 0.625, -6dB ~ 0.375
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, fx_kick_eq, 0, 0.186) # B1 Freq (75Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, fx_kick_eq, 1, 0.625) # B1 Gain (+6dB)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, fx_kick_eq, 3, 0.264) # B2 Freq (130Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, fx_kick_eq, 4, 0.375) # B2 Gain (-6dB)

    # --- TRACK 2: BASS ---
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_bass = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name}_Bass", True)

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", item_length)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    # Driving 1/8th note Bass
    for b in range(bars):
        chord_idx = progression[b % len(progression)]
        pitch = root_val + scale_intervals[chord_idx] + 24 # Sub/C1 Octave
        for i in range(8):
            start_time = b * (60.0 / bpm) * 4 + i * (60.0 / bpm) * 0.5
            end_time = start_time + (60.0 / bpm) * 0.45
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, end_time)
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 10, False)

    RPR.RPR_MIDI_Sort(take_bass)

    # Bass FX Setup
    fx_bass_synth = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    # Make the bass synth a sawtooth for harmonic richness
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_synth, 1, 0.5) 
    
    fx_bass_eq = RPR.RPR_TrackFX_AddByName(track_bass, "ReaEQ", False, -1)
    
    # Complementary EQ on Bass
    # 1kHz ~ 0.551. +4dB ~ 0.583. -24dB cut ~ 0.0
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 0, 0.186) # B1 Freq (75Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 1, 0.000) # B1 Gain (Severe Cut/HPF at 75Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 3, 0.264) # B2 Freq (130Hz)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 4, 0.625) # B2 Gain (+6dB Boost)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 6, 0.551) # B3 Freq (1kHz)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, fx_bass_eq, 7, 0.583) # B3 Gain (+4dB Articulation)

    return f"Created {track_name} (Kick + Bass) demonstrating Complementary EQ masking resolution over {bars} bars at {bpm} BPM."
```