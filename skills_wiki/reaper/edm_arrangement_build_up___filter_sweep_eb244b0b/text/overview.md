### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Arrangement Build-Up & Filter Sweep

* **Core Musical Mechanism**: This pattern structurally defines an EDM transition from a tension-building "Intro" into a hard-hitting "Drop" or "Verse". It relies on two primary mechanisms:
  1. **Timbral Tension via Filter Automation**: A sustained chord progression starts heavily muffled (Low-Pass Filter) and gradually opens up, increasing high-frequency energy and creating psychoacoustic anticipation. 
  2. **Rhythmic Contrast & Groove Extraction**: When the filter fully opens, the arrangement instantly switches from a static harmonic bed into a highly rhythmic state, introducing a 4-to-the-floor kick drum paired with an off-beat syncopated bassline. The off-beat bass perfectly mimics the "pumping" effect of heavy sidechain compression without needing complex routing.

* **Why Use This Skill (Rationale)**: The filter sweep is one of the most reliable ways to signal a structural change to the listener. By temporarily masking the high frequencies, you hold back the full energy of the track. When the filter opens and the drums hit simultaneously, the contrast creates a massive release of energy. The off-beat bass avoids frequency masking with the kick drum on the downbeats, naturally sitting in the pocket of the groove.

* **Overall Applicability**: Essential for EDM, House, Techno, and Future Bass tracks. It works perfectly for transitions from an intro to a verse, a breakdown to a drop, or a verse to a pre-chorus.

* **Value Addition**: This skill moves beyond a simple static loop; it encodes **time-based arrangement logic**. It generates a multi-track composition where elements enter at specific structural boundaries (e.g., halfway through the generated loop), tied together by an automation curve that perfectly aligns with those boundaries.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Typically 120-128 BPM (defaulting to 125 BPM).
  - **Grid**: 4/4 time signature.
  - **Chords**: Sustained for full measures (whole notes) to provide a smooth bed for the filter sweep.
  - **Kick**: Strict 4-to-the-floor pattern (playing on beats 1, 2, 3, 4) starting halfway through the arrangement.
  - **Bass**: Syncopated 8th notes playing strictly on the "and" of each beat (1 **&** 2 **&** 3 **&** 4 **&**), creating a pumping groove against the kick.

* **Step B: Pitch & Harmony**
  - **Progression**: A driving, emotional minor progression: `i - VI - III - VII`.
  - **Bassline**: Tracks the root note of the active chord, transposed down two octaves to sit in the sub-frequency range.

* **Step C: Sound Design & FX**
  - **Pad/Chords**: A blend of saw and square waves (using ReaSynth) with a longer release.
  - **Filter Sweep**: A `ReaEQ` instance with Band 4 (High Shelf) gain dropped to `-inf`, effectively turning it into a Low Pass filter.
  - **Kick/Bass**: ReaSynth tweaked for punchy low-end (short release for bass, sine wave with fast attack for kick).

* **Step D: Mix & Automation**
  - **Filter Automation**: An envelope on the `ReaEQ` Band 4 Frequency parameter. It starts closed (~300Hz) at bar 1, and ramps up linearly to fully open (~15kHz) exactly at the start of the drop.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Arrangement Structure** | Track creation & delayed Media Items | Allows elements (Kick, Bass) to enter exactly at the structural midpoint (the drop). |
| **Filter Sweep** | `RPR_InsertEnvelopePoint` on `ReaEQ` | Matches the tutorial's technique of automating an EQ curve to build tension over time. |
| **Pumping Groove** | MIDI note insertion (Off-beat bass timing) | Mimics the rhythmic result of sidechain compression flawlessly, guaranteeing runtime execution without fragile plugin pin routing. |
| **Harmonic Movement** | Algorithmic diatonic chord generation | Ensures the progression is musically valid in any key or scale parameter provided. |

> **Feasibility Assessment**: 100% reproducible for the structural and MIDI elements. The exact timbral richness of the VST synths used in the video is approximated using REAPER's native `ReaSynth` and `ReaEQ`, capturing the complete musical intent and mechanism natively.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM_Build",
    bpm: int = 125,
    key: str = "G",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Arrangement Build-Up with an EQ filter sweep in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars (first half is the build, second half is the drop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
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
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # === Step 2: Create Tracks ===
    base_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Chords (Pad)
    RPR.RPR_InsertTrackAtIndex(base_idx, True)
    track_chords = RPR.RPR_GetTrack(0, base_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    
    # Track 2: Kick
    RPR.RPR_InsertTrackAtIndex(base_idx + 1, True)
    track_kick = RPR.RPR_GetTrack(0, base_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_kick, "P_NAME", f"{track_name}_Kick", True)
    
    # Track 3: Bass
    RPR.RPR_InsertTrackAtIndex(base_idx + 2, True)
    track_bass = RPR.RPR_GetTrack(0, base_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name}_Bass", True)

    # === Helper Functions ===
    def insert_midi_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    def get_chord_notes(root_idx, scale_arr):
        n1 = scale_arr[root_idx % len(scale_arr)] + 12 * (root_idx // len(scale_arr))
        n2 = scale_arr[(root_idx + 2) % len(scale_arr)] + 12 * ((root_idx + 2) // len(scale_arr))
        n3 = scale_arr[(root_idx + 4) % len(scale_arr)] + 12 * ((root_idx + 4) // len(scale_arr))
        return [n1, n2, n3]

    root_offset = NOTE_MAP.get(key, 0) + 48 # Base octave 4
    scale_notes = SCALES.get(scale, SCALES["minor"])
    progression = [0, 5, 2, 6] # Diatonic i, VI, III, VII
    drop_start_time = (bars // 2) * bar_len
    drop_bars = bars - (bars // 2)

    # === Step 3: Chords & Filter Automation ===
    # Set up ReaSynth Pad
    synth_chords = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 1, 0.6) # Saw Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 2, 0.4) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, synth_chords, 4, 0.7) # Release

    # Set up ReaEQ Filter
    eq_idx = RPR.RPR_TrackFX_AddByName(track_chords, "ReaEQ", False, -1)
    # Param 10 is Band 4 Gain. 0.0 effectively makes the High Shelf act as a Low Pass Cut.
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, eq_idx, 10, 0.0) 
    
    # Automate Band 4 Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(track_chords, eq_idx, 9, True)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True) # Start muffled (~300Hz)
    RPR.RPR_InsertEnvelopePoint(env, drop_start_time, 0.9, 0, 0, False, True) # Open at the drop (~15kHz)
    RPR.RPR_Envelope_SortPoints(env)

    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bar_len * bars)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    for b in range(bars):
        chord_idx = progression[b % len(progression)]
        notes = get_chord_notes(chord_idx, scale_notes)
        start_time = b * bar_len
        end_time = start_time + bar_len * 0.95 # Leave a slight gap for breathing room
        for n in notes:
            insert_midi_note(take_chords, start_time, end_time, root_offset + n, int(velocity_base * 0.8))

    # === Step 4: Kick Drum (Enters at Drop) ===
    synth_kick = RPR.RPR_TrackFX_AddByName(track_kick, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 3, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 4, 0.05) # Release (tight)
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 1, 0.0)  # No Saw
    RPR.RPR_TrackFX_SetParamNormalized(track_kick, synth_kick, 2, 0.0)  # No Pulse (Pure Sine)

    item_kick = RPR.RPR_AddMediaItemToTrack(track_kick)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_POSITION", drop_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item_kick, "D_LENGTH", drop_bars * bar_len)
    take_kick = RPR.RPR_AddTakeToMediaItem(item_kick)

    for b in range(drop_bars):
        for beat in range(4):
            start_time = drop_start_time + b * bar_len + beat * beat_len
            end_time = start_time + beat_len * 0.25
            insert_midi_note(take_kick, start_time, end_time, 36, velocity_base) # C1 Kick

    # === Step 5: Off-beat Bass (Enters at Drop) ===
    synth_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 1, 0.0) # No Saw
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 2, 0.7) # Square wave for EDM buzz
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, synth_bass, 4, 0.15) # Plucky release

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", drop_start_time)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", drop_bars * bar_len)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    for b in range(drop_bars):
        overall_bar = (bars // 2) + b
        chord_idx = progression[overall_bar % len(progression)]
        root_note = scale_notes[chord_idx % len(scale_notes)] + 12 * (chord_idx // len(scale_notes))
        pitch = root_offset + root_note - 24 # Drop 2 octaves into sub range
        
        start_time = drop_start_time + b * bar_len
        
        # Off-beat 8th notes (playing strictly on the 'AND' of each beat)
        for i in range(4):
            note_start = start_time + (i * beat_len) + (beat_len / 2)
            note_end = note_start + (beat_len / 2) * 0.8
            insert_midi_note(take_bass, note_start, note_end, pitch, velocity_base)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_kick)
    RPR.RPR_MIDI_Sort(take_bass)

    return f"Created '{track_name}' EDM arrangement ({bars} bars) at {bpm} BPM in {key} {scale} with an automated filter sweep."
```