### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Pumping Filter Sweep Intro & Sparse Verse Drop

* **Core Musical Mechanism**: The arrangement transitions from a tense, rising intro into a driving "sparse verse" drop. This is achieved using three simultaneous mechanisms:
  1. **Sidechain Pumping Illusion**: A rhythmic 4-on-the-floor volume ducking effect applied to sustained chords, creating a strong groove even when the physical drums are absent.
  2. **Filter Sweep**: A slow low-pass/high-shelf filter opening up over the chords, gradually introducing high frequencies to build psychoacoustic tension.
  3. **Pre-Drop Pause**: A complete silencing of all elements on the final beat before the new section starts, creating a contrast that makes the incoming verse/drop hit much harder.

* **Why Use This Skill (Rationale)**: This technique utilizes the psychoacoustic principle of tension and release. By initially depriving the listener of high frequencies (filter) and low-end transient impact (missing drums), the brain anticipates their arrival. The "pumping" effect grounds the listener in the BPM, and the final beat pause acts as a rhythmic vacuum that violently pulls the listener into the full frequency spectrum of the drop.

* **Overall Applicability**: Essential for Dance, House, Future Bass, and Pop-EDM production. It perfectly structures the transition from an atmospheric intro to an energetic Verse or Chorus. 

* **Value Addition**: Instead of generating a static 4-bar loop, this skill encodes a dynamic, timeline-based structural arrangement. It automates sidechain ducks, sweeps EQs, generates an idiomatic chord progression, and models a classic "pre-drop pause" across multiple tracks simultaneously.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 125 BPM (Standard House/EDM).
  - **Grid**: 4/4 time.
  - **Structure**: 8 bars total (Bars 1-4: Intro, Bars 5-8: Verse/Drop).
  - **Pre-Drop Pause**: Bar 4, beat 4 is left completely empty across all instruments.

* **Step B: Pitch & Harmony**
  - **Progression**: The classic epic progression (vi - IV - I - V in Major, or i - VI - III - VII in Minor).
  - **Chords Track**: Plays sustained whole-note triads for the full 8 bars (except the pause). 
  - **Bass Track**: Plays the root note of the chords during the Verse, triggering on the off-beats (the "and" of the beat, e.g., 1.5, 2.5) to lock into the pocket of the pumping rhythm.

* **Step C: Sound Design & FX**
  - **Ghost Kick**: A muted 4-on-the-floor kick pattern strictly used conceptually to trigger the pump. 
  - **Chords**: ReaEQ is added with Band 4's gain dropped to `-inf`, acting as a High Cut filter.
  - **Drums**: Placeholders using `ReaSamplOmatic5000` set up for Kick (MIDI 36), Clap (MIDI 39), and Hats (MIDI 42), ready for the user to drop samples into.

* **Step D: Mix & Automation**
  - **Volume Envelope Pump**: Instead of complex sidechain routing which can be brittle, the chords track has an automated Volume Envelope perfectly mimicking a 4-on-the-floor sidechain compressor (dipping to -20dB on the beat, swelling back to 0dB).
  - **Filter Sweep**: ReaEQ Band 4 Frequency is automated, sweeping from a muffled low frequency to fully open over the first 4 bars.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arrangement Block | Track & MIDI Item creation | Allows for cross-track interaction (the 1-beat pause affects everything). |
| Chord & Bass generation | Algorithmic MIDI | Computes the classic i-VI-III-VII progression relative to user's Key/Scale. |
| Sidechain Pumping | Volume Envelope Automation | Perfectly replicates the LFO/Sidechain pumping effect dynamically without relying on audio routing triggers. |
| Filter Sweep | ReaEQ Parameter Automation | Utilizes stock REAPER FX to create the tension-building cutoff sweep. |

> **Feasibility Assessment**: 100% reproducible. The code fully scaffolds the 8-bar arrangement, writes the MIDI patterns, shapes the pumping automation, and sweeps the EQ natively in REAPER. (Note: Drum tracks use `ReaSamplOmatic5000` scaffolds ready for the user's custom WAV samples, but the rhythmic MIDI is fully programmed).

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Hardcoded to 8 internally to demonstrate 4-bar intro + 4-bar verse
    **kwargs,
) -> str:
    """
    Create an EDM Pumping Intro transitioning into a Sparse Verse Drop.
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

    # Set up Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_sec = 60.0 / bpm
    
    root_val = NOTE_MAP.get(key, 0)
    root_midi = 48 + root_val  # Start around C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Classic EDM Progression: i - VI - III - VII (minor) or vi - IV - I - V (major)
    progression = [0, 5, 2, 6] if "minor" in scale else [5, 3, 0, 4]

    def get_chord_pitches(degree, intervals, root):
        scale_len = len(intervals)
        pitches = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = degree + i
            octave = idx // scale_len
            note_idx = idx % scale_len
            pitches.append(root + intervals[note_idx] + (octave * 12))
        return pitches

    def create_midi_take(track, start_s, end_s):
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_s, end_s, False)
        return RPR.RPR_GetActiveTake(item)

    def add_note(take, start_s, end_s, pitch, vel):
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_s)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_s)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    track_count = RPR.RPR_CountTracks(0)

    # --- 1. GHOST KICK (For Sidechain Concept) ---
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    ghost_tr = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_tr, "P_NAME", "Ghost Kick (Muted)", True)
    RPR.RPR_SetMediaTrackInfo_Value(ghost_tr, "B_MUTE", 1.0)
    
    ghost_take = create_midi_take(ghost_tr, 0.0, 8 * 4 * beat_sec)
    for bar in range(8):
        for beat in range(4):
            if bar == 3 and beat == 3: continue # Pre-drop pause
            t = (bar * 4 + beat) * beat_sec
            add_note(ghost_take, t, t + 0.1, 36, 100)
    RPR.RPR_MIDI_Sort(ghost_take)

    # --- 2. PUMPING CHORDS ---
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    chords_tr = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_tr, "P_NAME", "Pumping Chords", True)
    RPR.RPR_TrackFX_AddByName(chords_tr, "ReaSynth", False, -1)
    
    chords_take = create_midi_take(chords_tr, 0.0, 8 * 4 * beat_sec)
    for bar in range(8):
        pitches = get_chord_pitches(progression[bar % 4], scale_intervals, root_midi)
        start_t = bar * 4.0 * beat_sec
        end_t = (bar + 1) * 4.0 * beat_sec
        if bar == 3: end_t -= beat_sec # Pre-drop pause
        for p in pitches:
            add_note(chords_take, start_t, end_t, p, 80)
    RPR.RPR_MIDI_Sort(chords_take)

    # Filter Sweep Setup
    eq_idx = RPR.RPR_TrackFX_AddByName(chords_tr, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(chords_tr, eq_idx, 10, 0.0) # Band 4 Gain down (creates shelf)
    env_eq = RPR.RPR_GetFXEnvelope(chords_tr, eq_idx, 9, True) # Show env for Band 4 Freq
    if env_eq:
        RPR.RPR_InsertEnvelopePoint(env_eq, 0.0, 0.2, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_eq, 3.0 * 4.0 * beat_sec + 3.0 * beat_sec, 0.9, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env_eq)

    # Pumping Volume Envelope Setup
    RPR.RPR_SetOnlyTrackSelected(chords_tr)
    RPR.RPR_Main_OnCommand(41866, 0) # Track: Show track volume envelope
    env_vol = RPR.RPR_GetTrackEnvelopeByName(chords_tr, "Volume")
    if env_vol:
        for bar in range(8):
            for beat in range(4):
                time_beat = (bar * 4 + beat) * beat_sec
                if bar == 3 and beat == 3:
                    RPR.RPR_InsertEnvelopePoint(env_vol, time_beat, 0.0, 0, 0, False, True)
                    continue
                # 0.716 normalized is approx 0dB. 0.05 is heavily ducked. Shape 2 is slow start/end.
                RPR.RPR_InsertEnvelopePoint(env_vol, time_beat, 0.05, 2, 0, False, True)
                RPR.RPR_InsertEnvelopePoint(env_vol, time_beat + beat_sec * 0.4, 0.716, 0, 0, False, True)
                RPR.RPR_InsertEnvelopePoint(env_vol, time_beat + beat_sec * 0.95, 0.716, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    # --- 3. DROP DRUMS ---
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    drums_tr = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_tr, "P_NAME", "Drop Drums (Load RS5K Samples)", True)
    
    # Setup RS5k Placeholders
    for pitch in [36, 39, 42]:
        fx = RPR.RPR_TrackFX_AddByName(drums_tr, "ReaSamplOmatic5000", False, -1)
        RPR.RPR_TrackFX_SetParamNormalized(drums_tr, fx, 3, pitch / 128.0) # Start note
        RPR.RPR_TrackFX_SetParamNormalized(drums_tr, fx, 4, pitch / 128.0) # End note

    drums_take = create_midi_take(drums_tr, 4 * 4 * beat_sec, 8 * 4 * beat_sec)
    for bar in range(4, 8):
        for beat in range(4):
            t = (bar * 4 + beat) * beat_sec
            add_note(drums_take, t, t + 0.1, 36, 110) # Kick
            if beat in [1, 3]: # Clap on 2 and 4 (0-indexed)
                add_note(drums_take, t, t + 0.1, 39, 100)
            t_off = t + beat_sec / 2.0
            add_note(drums_take, t_off, t_off + 0.05, 42, 90) # Off-beat Hat
    RPR.RPR_MIDI_Sort(drums_take)

    # --- 4. DROP BASS ---
    RPR.RPR_InsertTrackAtIndex(track_count + 3, True)
    bass_tr = RPR.RPR_GetTrack(0, track_count + 3)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_tr, "P_NAME", "Drop Bass", True)
    bass_fx = RPR.RPR_TrackFX_AddByName(bass_tr, "ReaSynth", False, -1)
    
    bass_take = create_midi_take(bass_tr, 4 * 4 * beat_sec, 8 * 4 * beat_sec)
    for bar in range(4, 8):
        bass_pitch = get_chord_pitches(progression[bar % 4], scale_intervals, root_midi - 24)[0]
        for beat in range(4):
            # Play bouncy 8th notes on the off-beats
            t = (bar * 4 + beat) * beat_sec + (beat_sec / 2.0)
            add_note(bass_take, t, t + beat_sec / 2.5, bass_pitch, 100)
    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created EDM 8-Bar Intro to Drop Sequence at {bpm} BPM in {key} {scale}."
```