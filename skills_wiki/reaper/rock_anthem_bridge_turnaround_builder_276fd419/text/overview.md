# Rock Anthem Bridge & Turnaround Builder

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Rock Anthem Bridge & Turnaround Builder

* **Core Musical Mechanism**: The pattern transitions the song's energy by moving away from the tonic using a diatonic rising progression, resolving with a dominant 7th turnaround. It relies on a three-layered arrangement: a sustained pad/organ providing harmonic glue, a driving straight-eighth-note bass locking down the root, and a rhythmically locked "modern" chordal guitar pumping eighth notes.
* **Why Use This Skill (Rationale)**: This is a classic rock/pop arrangement technique. Harmonically, stepping through diatonic chords (iv - v - III) creates a sense of journey or "lifting" away from the verse. Ending on the v7 (minor dominant 7th) introduces harmonic tension that desperately wants to resolve back to the tonic (verse or chorus). Rhythmically, moving from syncopated verse patterns to straight driving 8th notes creates a "wall of sound" urgency characteristic of a bridge.
* **Overall Applicability**: Perfect for connecting sections in rock, pop-punk, and alternative tracks. The rigid eighth-note drive works beautifully to build momentum before a massive final chorus drop.
* **Value Addition**: This skill encodes multi-track arrangement theory. Instead of just pasting a chord progression, it automatically voices the chords, separates the harmonic functions (sustained vs. driving), and sets up the turnaround tension computationally based on the key and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, optimally between 90-110 BPM (tutorial uses 94 BPM).
  - **Rhythmic Grid**: The organ plays whole notes (1 per bar). The bass and guitar play rigid, continuous 1/8th notes. 
  - **Note Duration**: The 1/8th notes are played slightly detached (staccato/marcato) at around 85-90% of the grid length to prevent the mix from turning to mud.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: F minor (tutorial specific, but algorithmically adaptable).
  - **Progression**: iv - v - III - v7 (Bbm - Cm - Ab - Cm7 in F minor).
  - **Voicing**: 
    - Bass plays root note only, transposed down 2 octaves.
    - Organ plays close-voiced root position triads (and a 4-note 7th chord for the turnaround).
    - Guitar mirrors the organ chords but transposed down 1 octave to sit in the midrange.

* **Step C: Sound Design & FX**
  - **Instruments**: To emulate the VSTs without external dependencies, we use `ReaSynth` shaped for different timbres.
    - *Organ*: Soft square wave blend.
    - *Bass*: Heavy sawtooth blend for aggressive bite.
    - *Guitar*: Blended square/saw with slight EQ/Drive characteristics.
  - **Mixing**: Bass is centered, Organ is widened or panned slightly, Guitar is kept punchy.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Multi-track Arranging** | Track creation & FX allocation | The tutorial explicitly splits the bridge into Organ (chords), Bass (roots), and Guitar (rhythm). |
| **Diatonic Progression** | Programmatic MIDI generation | Computing pitches via scale indices ensures the turnaround (v7) adapts perfectly to any key passed to the agent. |
| **Rhythmic Drive** | `RPR_MIDI_InsertNote` looping | Generates the continuous 8th-note "modern chord" pumping effect without needing a 3rd party arpeggiator/generator. |

> **Feasibility Assessment**: 85% — The core musical arrangement, harmony, and rhythm are reproduced perfectly. The exact tonal quality of RapidComposer's internal VSTs cannot be achieved via stock ReaSynth, but the track structure, MIDI logic, and arrangement theory are fully intact and ready for the user to swap out synths.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Bridge",
    bpm: int = 94,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a multi-track Rock Bridge (iv-v-III-v7) with driving 8th notes in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (will loop the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10]
    }

    root_val = NOTE_MAP.get(key, 5) # Default F
    intervals = SCALES.get(scale, SCALES["minor"])
    
    # 0-indexed scale degrees for: iv, v, III, v7
    bridge_progression = [
        {"degree": 3, "num_notes": 3}, # Bar 1: subdominant triad
        {"degree": 4, "num_notes": 3}, # Bar 2: dominant triad
        {"degree": 2, "num_notes": 3}, # Bar 3: mediant triad
        {"degree": 4, "num_notes": 4}, # Bar 4: dominant 7th (turnaround)
    ]

    def get_diatonic_chord(root_deg, num_notes, octave):
        notes = []
        for i in range(num_notes):
            deg = root_deg + (i * 2) # Stack thirds
            oct_offset = deg // len(intervals)
            scale_idx = deg % len(intervals)
            pitch = root_val + intervals[scale_idx] + (octave + oct_offset) * 12
            notes.append(pitch)
        return notes

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0.0, -1, -1, bpm, 4, 4, True)

    beats_per_bar = 4
    quarter_len = 60.0 / bpm
    bar_len = quarter_len * beats_per_bar
    total_len = bar_len * bars

    # Helper to create a track with an item and basic FX
    def setup_track(name_suffix, vol_db):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", f"{track_name} {name_suffix}", True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_VOL", 10**(vol_db/20.0))
        
        # Add basic synth
        fx_idx = RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
        
        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(trk, 0.0, total_len, False)
        take = RPR.RPR_GetActiveTake(item)
        return trk, take, fx_idx

    # --- TRACK 1: ORGAN (Sustained Chords) ---
    trk_org, take_org, fx_org = setup_track("Organ", -6.0)
    # Tweak ReaSynth for an organ-like square tone
    RPR.RPR_TrackFX_SetParam(trk_org, fx_org, 2, 0.6) # Square mix

    # --- TRACK 2: BASS (Driving 8ths) ---
    trk_bas, take_bas, fx_bas = setup_track("Bass", -3.0)
    # Tweak ReaSynth for aggressive saw bass
    RPR.RPR_TrackFX_SetParam(trk_bas, fx_bas, 3, 0.9) # Saw mix
    
    # --- TRACK 3: GUITAR (Driving 8th Chords) ---
    trk_gtr, take_gtr, fx_gtr = setup_track("Guitar", -8.0)
    # Tweak ReaSynth for blended bright tone
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 2, 0.4) 
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 3, 0.5)

    # Generate MIDI Data
    eighth_len = quarter_len / 2.0
    
    for bar in range(bars):
        bar_start_time = bar * bar_len
        # Loop progression every 4 bars
        chord_def = bridge_progression[bar % 4] 
        
        chord_pitches_org = get_diatonic_chord(chord_def["degree"], chord_def["num_notes"], 5)
        chord_pitches_gtr = get_diatonic_chord(chord_def["degree"], chord_def["num_notes"], 4)
        bass_pitch = chord_pitches_org[0] - 24 # Drop 2 octaves

        # 1. Insert Organ Notes (Whole note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_org, bar_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_org, bar_start_time + bar_len)
        for pitch in chord_pitches_org:
            RPR.RPR_MIDI_InsertNote(take_org, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.8), False)

        # 2. Insert Bass & Guitar Notes (Driving 8th notes)
        for e in range(8): # 8 eighths in a 4/4 bar
            note_start_time = bar_start_time + (e * eighth_len)
            note_end_time = note_start_time + (eighth_len * 0.85) # 85% length for separation/drive
            
            # Bass
            b_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bas, note_start_time)
            b_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bas, note_end_time)
            # Add slight velocity humanization/accent on downbeats
            b_vel = velocity_base if e % 2 == 0 else int(velocity_base * 0.85)
            RPR.RPR_MIDI_InsertNote(take_bas, False, False, b_start_ppq, b_end_ppq, 0, bass_pitch, b_vel, False)

            # Guitar
            g_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_gtr, note_start_time)
            g_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_gtr, note_end_time)
            g_vel = int(velocity_base * 0.9) if e % 2 == 0 else int(velocity_base * 0.75)
            for pitch in chord_pitches_gtr:
                RPR.RPR_MIDI_InsertNote(take_gtr, False, False, g_start_ppq, g_end_ppq, 0, pitch, g_vel, False)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_org)
    RPR.RPR_MIDI_Sort(take_bas)
    RPR.RPR_MIDI_Sort(take_gtr)

    return f"Created multi-track '{track_name}' (Organ, Bass, Guitar) covering {bars} bars at {bpm} BPM in {key} {scale}."
```