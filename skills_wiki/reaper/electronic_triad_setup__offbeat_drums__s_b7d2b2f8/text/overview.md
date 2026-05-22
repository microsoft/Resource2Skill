### 1. High-level Design Pattern Extraction

**Skill Name**: Electronic Triad Setup (Offbeat Drums, Synth Bass, Harmonic Pad)

* **Core Musical Mechanism**: This technique establishes the foundational "triad" of electronic music: a synthesized drum beat, a rhythmic bassline, and a harmonic chord progression. The video demonstrates setting up this architecture using third-party VSTs (Massive X, Reason's Beat Map / Kong, and Reaktor 6). The rhythmic signature is driven by an "OffBeat" drum algorithm, which heavily relies on four-on-the-floor kicks accompanied by syncopated offbeat hi-hats.
* **Why Use This Skill (Rationale)**: Setting up the rhythm (drums), foundation (bass), and harmony (pad) immediately establishes the groove and tonal center of a track. The "offbeat" hi-hat pattern creates a push-and-pull rhythmic tension against the steady kick, which is a fundamental groove theory principle in house, techno, and electronic pop.
* **Overall Applicability**: This is the perfect starting point or scaffold for almost any electronic genre. It provides a cohesive instrumental bed over which melodies, vocals, or lead synths can be layered.
* **Value Addition**: While the video merely loads third-party plugins and creates empty MIDI clips, this generated skill explicitly encodes the music theory. It computes a minor/major chord progression, creates an interlocking 8th-note bassline, and generates a fully quantized Offbeat drum groove using native REAPER instruments—bypassing the need for expensive third-party VSTs.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo:** 120 BPM (classic house/electronic tempo).
  - **Time Signature:** 4/4.
  - **Drum Pattern:** Kick on every downbeat (1, 2, 3, 4). Snare/Clap on beats 2 and 4. Hi-hat strictly on the offbeats (1.5, 2.5, 3.5, 4.5).
  - **Bassline:** Staccato 8th notes following the chord roots, adding driving low-end momentum.

* **Step B: Pitch & Harmony**
  - **Progression:** A classic i - VI - III - VII progression.
  - **Voicings:** 3-note diatonic triads (root, third, fifth) computed dynamically based on the input key and scale.
  - **Bass:** Plays the root note of the current chord, shifted down two octaves (Octave 2).

* **Step C: Sound Design & FX**
  - Since the third-party VSTs (Massive X, Reason Rack, Reaktor 6) cannot be guaranteed on all systems, we reconstruct their roles using stock plugins.
  - **Drums:** Three instances of `ReaSamplOmatic5000` (acting as the Reason Kong Drum Designer).
  - **Bass:** `ReaSynth` configured with a sawtooth wave mix to emulate Reaktor's TRK-01 Bass.
  - **Pad:** `ReaSynth` with a slowed-down attack and release to emulate Massive X's Retro Pad patches.

* **Step D: Mix & Automation**
  - Track naming is strictly managed (`{track_name} Drums`, `{track_name} Bass`, etc.) to allow for easy identification and future sidechain routing. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Architecture | `RPR_InsertTrackAtIndex` | Replicates the user's multi-track workflow in the video. |
| Offbeat Drum Groove | MIDI note insertion | Allows for exact replication of the Reason "Beat Map" algorithmic drum pattern. |
| Harmony & Bassline | MIDI pitch computation | Encodes the harmonic rules so the pattern can adapt to any key/scale parameter. |
| Sound Generators | FX Chain (`ReaSynth`, `RS5K`) | Replaces Massive X/Reaktor with 100% stock REAPER plugins to guarantee runtime safety and reproducibility. |

**Feasibility Assessment:** 100% reproducible regarding the musical architecture, rhythm, and harmony. The precise timbral character of Massive X and Reaktor 6 cannot be cloned with ReaSynth, but the native synthesis provides a perfectly viable compositional scaffold.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Electro_Triad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Electronic Triad Setup (Drums, Bass, Pad) in the current REAPER project.
    Simulates the Massive X + Reason Rack + Reaktor workflow using native plugins.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "F#").
        scale: Scale type ("minor", "major", etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the creation.
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

    # Helper functions for harmonic computation
    def get_note_by_degree(base_str, scale_str, degree, octave):
        base_note = NOTE_MAP.get(base_str.capitalize(), 0)
        scale_intervals = SCALES.get(scale_str, SCALES["minor"])
        idx = degree % len(scale_intervals)
        octave_shift = degree // len(scale_intervals)
        # +1 because standard MIDI C4 is note 60 (0 + 5 * 12)
        return base_note + scale_intervals[idx] + (octave + octave_shift + 1) * 12

    def get_chord(base_str, scale_str, degree, octave=4):
        return [get_note_by_degree(base_str, scale_str, degree + i, octave) for i in [0, 2, 4]]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_length = bar_len * bars
    
    # Progressions: i - VI - III - VII
    progression = [0, 5, 2, 6] 

    def get_ppq(take, time_sec):
        return RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)

    # ==========================================
    # 1. DRUM TRACK (Offbeat Pattern Simulation)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    # Add 3 RS5K instances as placeholders for Kick, Snare, Hat
    for _ in range(3):
        RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
        
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    for b in range(bars):
        bar_start = b * bar_len
        for beat in range(4):
            beat_start = bar_start + (beat * beat_len)
            
            # Kick (C2 - 36) on every downbeat
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    get_ppq(drum_take, beat_start), get_ppq(drum_take, beat_start + 0.1), 
                                    0, 36, velocity_base, False)
            
            # Snare (D2 - 38) on beats 2 and 4
            if beat % 2 == 1:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                        get_ppq(drum_take, beat_start), get_ppq(drum_take, beat_start + 0.1), 
                                        0, 38, velocity_base, False)
                
            # Hi-Hat (F#2 - 42) on the offbeats
            hat_start = beat_start + (beat_len * 0.5)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    get_ppq(drum_take, hat_start), get_ppq(drum_take, hat_start + 0.1), 
                                    0, 42, int(velocity_base * 0.8), False)
    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # 2. BASS TRACK (Reaktor Synth Simulation)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)
    
    # Configure ReaSynth as a Bass (Saw wave, tuned down)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 1.0) # Saw shape mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.2) # Short release
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    for b in range(bars):
        degree = progression[b % len(progression)]
        bass_note = get_note_by_degree(key, scale, degree, 2) # Octave 2
        bar_start = b * bar_len
        
        # 8th note rhythm
        for i in range(8):
            start_time = bar_start + i * (beat_len * 0.5)
            end_time = start_time + (beat_len * 0.4) # Slightly staccato
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, 
                                    get_ppq(bass_take, start_time), get_ppq(bass_take, end_time), 
                                    0, bass_note, velocity_base, False)
    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # 3. PAD TRACK (Massive X Simulation)
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    pad_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", f"{track_name} Pad", True)
    
    # Configure ReaSynth as a Pad (Slow attack, long release)
    RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 5, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(pad_track, 0, 6, 0.7) # Release
    
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", total_length)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)
    
    for b in range(bars):
        degree = progression[b % len(progression)]
        chord_notes = get_chord(key, scale, degree, 4) # Octave 4
        
        start_time = b * bar_len
        end_time = start_time + bar_len
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(pad_take, False, False, 
                                    get_ppq(pad_take, start_time), get_ppq(pad_take, end_time), 
                                    0, note, int(velocity_base * 0.7), False)
    RPR.RPR_MIDI_Sort(pad_take)

    return f"Created Electronic Triad scaffold (Drums, Bass, Pad) in {key} {scale} over {bars} bars at {bpm} BPM."
```