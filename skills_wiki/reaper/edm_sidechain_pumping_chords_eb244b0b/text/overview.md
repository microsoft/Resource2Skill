### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Sidechain Pumping Chords

* **Core Musical Mechanism**: Rhythmic volume ducking (attenuation) of sustained melodic elements (like chords, pads, or bass) triggered exactly on the downbeats by a 4-to-the-floor kick drum. This is typically achieved via sidechain compression, but its essence is a mathematically precise volume LFO synced to the beat.
* **Why Use This Skill (Rationale)**: This technique serves two primary purposes: 
  1. **Psychoacoustic Groove**: The rhythmic swelling creates forward momentum and a "breathing" physical feel that defines Dance/EDM genres.
  2. **Frequency Masking Management**: Sustained, thick synthesizer chords consume massive headroom. Ducking them exactly when the kick drum hits ensures the transient of the kick punches through the mix without clipping the master bus or muddying the low-mid frequencies.
* **Overall Applicability**: Essential for choruses, drops, and high-energy verses in electronic music (House, Trance, Future Bass, Pop). It contrasts heavily with the static, calm arrangements of intro and outro sections.
* **Value Addition**: Automating true sidechain routing in ReaScript can be extremely fragile due to plugin-specific parameter mappings. This skill encodes the exact *musical result* (the rhythmic ducking) by programmatically drawing a synchronized track volume envelope. This guarantees the signature EDM pump while remaining natively editable and plugin-independent.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 - 128 BPM (standard House/EDM).
  - **Grid**: 4/4 time signature. Kick hits on every quarter note (1, 2, 3, 4).
  - **Ducking Shape**: Volume drops instantly on the quarter note to ~15% amplitude (-16.5dB), ramps up exponentially/linearly to 100% amplitude by the 1/8th note, and holds until the next kick.
* **Step B: Pitch & Harmony**
  - Uses a classic 4-chord progression derived diatonic to the input key/scale.
  - Generates lush 4-note diatonic 7th chords in a close voicing, anchored by an octave-down bass note.
  - Chord rhythm: Whole notes (sustained for the entire bar) to maximize the contrast of the volume pumping.
* **Step C: Sound Design & FX**
  - **Kick**: ReaSynth configured as a fast-decay pure sine wave on MIDI note 36 (C2).
  - **Chords**: ReaSynth configured as a rich Pad (mixed Sawtooth and Square waves) with a slight attack and release to avoid clicking. 
* **Step D: Mix & Automation**
  - Instead of routing audio and hoping the compressor settings translate correctly, the exact gain reduction curve is drawn directly onto the Track Volume Envelope, mimicking tools like LFO Tool or VolumeShaper.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| EDM Chord Progression | MIDI note insertion | Allows diatonic 7th chord generation from parameters |
| 4-to-the-floor Beat | MIDI note insertion | Syncs perfectly with the ducking rhythm |
| Synthesizer Sounds | ReaSynth FX chain | Native REAPER synths ensure it works out-of-the-box without missing samples |
| Sidechain Pumping | Volume Envelope Automation | 100% reproducible and math-precise alternative to fragile auxiliary audio routing |

> **Feasibility Assessment**: 100% of the musical *effect* is reproduced. While the video uses specific 3rd-party drum samples and VST synths, the core arrangement pattern (the pumping chords and the 4-on-the-floor beat) is perfectly recreated using stock REAPER tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "Pumping Chords",
    bpm: int = 125,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Sidechain Pumping Pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created chords track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and elements.
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

    # Normalize key input
    key_str = key.capitalize() if len(key) == 1 else key[0].capitalize() + key[1:]
    key_base = NOTE_MAP.get(key_str, 0) + 60 # Default to C4

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    L = len(scale_intervals)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars

    # === Step 2: Create Chords Track & Synth ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", track_name, True)

    fx_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a lush pad (Saw + Square, slow attack/release)
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 0, 0.7)   # Vol
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 2, 0.5)   # Saw
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 3, 0.5)   # Square
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 6, 0.05)  # Attack
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 7, 0.3)   # Release

    # === Step 3: Generate Diatonic Chords ===
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_len)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    # Standard progression based on scale
    if L >= 7:
        if "minor" in scale.lower() or "dorian" in scale.lower():
            progression = [0, 5, 2, 6] # i, VI, III, VII
        else:
            progression = [0, 4, 5, 3] # I, V, vi, IV
    else:
        progression = [0, max(0, L-2), max(0, L-3), max(0, L-1)]

    for i in range(bars):
        deg = progression[i % len(progression)]
        start_time = i * bar_len
        end_time = start_time + bar_len

        # Build diatonic 7th chord with bass root
        root_pitch = key_base + scale_intervals[deg % L] + 12 * (deg // L)
        notes = [root_pitch - 12] # Bass note (-1 octave)
        for j in [0, 2, 4, 6]:    # Triad + 7th
            d = (deg + j) % L
            octave = (deg + j) // L
            notes.append(key_base + scale_intervals[d] + 12 * octave)

        for pitch in notes:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, end_time - 0.05) # slight gap
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
            
    RPR.RPR_MIDI_Sort(chord_take)

    # === Step 4: Simulate Sidechain Pump via Volume Envelope ===
    # Force Volume envelope to be visible to ensure we can grab it
    RPR.RPR_SetOnlyTrackSelected(chord_track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(chord_track, "Volume")
    
    if env:
        for b in range(bars * beats_per_bar):
            t = b * beat_len
            # Duck hard on the beat (0.15 amp approx -16dB)
            RPR.RPR_InsertEnvelopePoint(env, t, 0.15, 0, 0, False, True)
            # Ramp back up by 40% of the beat (mimics fast release)
            RPR.RPR_InsertEnvelopePoint(env, t + beat_len * 0.4, 1.0, 0, 0, False, True)
            # Hold max volume until the next kick
            RPR.RPR_InsertEnvelopePoint(env, t + beat_len - 0.01, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env)

    # === Step 5: Create 4-to-the-floor Kick Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Driver Kick", True)

    kick_fx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a kick-like sub punch (Pure sine, very short decay)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 0, 1.0)  # Vol
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 2, 0.0)  # Saw = 0
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 3, 0.0)  # Square = 0
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 6, 0.0)  # Fast Attack
    RPR.RPR_TrackFX_SetParam(kick_track, kick_fx, 7, 0.05) # Fast Release

    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_len)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    for b in range(bars * beats_per_bar):
        t_start = b * beat_len
        t_end = t_start + 0.1 # Very short trigger note
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, t_start)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, t_end)
        # Note 36 (C2) is standard for General MIDI Kicks
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, 36, 120, False)
        
    RPR.RPR_MIDI_Sort(kick_take)

    return f"Created EDM Sidechain Pattern: '{track_name}' envelope pump and 'Driver Kick' over {bars} bars at {bpm} BPM."
```