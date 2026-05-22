def create_pattern(
    project_name: str = "BossaProject",
    track_name: str = "Bossa",
    bpm: int = 80,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a complete Bossa Nova groove (Drums, Bass, Chords, Solo) in REAPER.
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    base_note = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    def get_scale_pitch(degree, octave):
        """Map a scale degree (0-indexed) to a MIDI note."""
        scale_len = len(scale_intervals)
        oct_shift = degree // scale_len
        wrapped_deg = degree % scale_len
        return base_note + (octave + oct_shift + 1) * 12 + scale_intervals[wrapped_deg]

    # --- Setup Project ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    def create_bossa_track(name, is_drums=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI Item
        beats_per_bar = 4
        bar_len_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_len_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, item, take

    def add_midi_note(item, take, start_beat, length_beats, pitch, vel, chan=0):
        item_pos = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")
        item_qn = RPR.RPR_TimeMap2_TimeToQN(0, item_pos)
        start_proj_qn = item_qn + start_beat
        end_proj_qn = start_proj_qn + length_beats
        start_proj_time = RPR.RPR_TimeMap2_QNToTime(0, start_proj_qn)
        end_proj_time = RPR.RPR_TimeMap2_QNToTime(0, end_proj_qn)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_proj_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_proj_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), "")

    # ==========================================
    # TRACK 1: DRUMS (GM Channel 10)
    # ==========================================
    track_drums, item_drums, take_drums = create_bossa_track(f"{track_name}_Drums", True)
    
    for b in range(bars):
        offset = b * 4.0
        # Kick (36) - Root beats and anticipations
        add_midi_note(item_drums, take_drums, offset + 0.0, 0.5, 36, 100, 9)
        add_midi_note(item_drums, take_drums, offset + 1.5, 0.5, 36, 80, 9)
        add_midi_note(item_drums, take_drums, offset + 2.0, 0.5, 36, 100, 9)
        add_midi_note(item_drums, take_drums, offset + 3.5, 0.5, 36, 80, 9)
        
        # Hi-Hat (42) - Steady 8ths
        for i in range(8):
            add_midi_note(item_drums, take_drums, offset + i * 0.5, 0.25, 42, 70 if i % 2 != 0 else 90, 9)
            
        # Triangle (81) - Fun syncopations
        for i in [1, 3, 5, 7]:
            add_midi_note(item_drums, take_drums, offset + i * 0.5, 0.25, 81, 100, 9)

        # Clave (Snare Cross-stick 37) - 3-2 Pattern
        if b % 2 == 0:
            add_midi_note(item_drums, take_drums, offset + 0.0, 0.5, 37, 110, 9)
            add_midi_note(item_drums, take_drums, offset + 1.5, 0.5, 37, 110, 9)
            add_midi_note(item_drums, take_drums, offset + 3.0, 0.5, 37, 110, 9)
        else:
            add_midi_note(item_drums, take_drums, offset + 1.0, 0.5, 37, 110, 9)
            add_midi_note(item_drums, take_drums, offset + 2.0, 0.5, 37, 110, 9)

    # ==========================================
    # TRACK 2: BASS (ReaSynth Upright/Sine)
    # ==========================================
    track_bass, item_bass, take_bass = create_bossa_track(f"{track_name}_Bass")
    fx_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 0, 0.8)   # Vol
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 2, 0.0)   # 100% Sine
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 6, 0.4)   # Med decay
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 7, 0.8)   # High Sustain

    progression = [0, 5, 1, 4] # I, VI, II, V
    
    for b in range(bars):
        offset = b * 4.0
        chord_root = progression[b % 4]
        bass_root = get_scale_pitch(chord_root, 2)
        bass_fifth = get_scale_pitch(chord_root + 4, 2) # Diatonic 5th
        
        # Classic Ba-Dum Rhythm
        add_midi_note(item_bass, take_bass, offset + 0.0, 1.25, bass_root, 100)
        add_midi_note(item_bass, take_bass, offset + 1.5, 0.5, bass_fifth, 85)
        add_midi_note(item_bass, take_bass, offset + 2.0, 1.25, bass_fifth, 100)
        add_midi_note(item_bass, take_bass, offset + 3.5, 0.5, bass_root, 85)

    # ==========================================
    # TRACK 3: CHORDS (ReaSynth E-Piano)
    # ==========================================
    track_chords, item_chords, take_chords = create_bossa_track(f"{track_name}_Chords")
    fx_chords = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 0, 0.4)   # Vol lowered
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 2, 0.3)   # Sine/Square mix
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 5, 0.05)  # Soft attack
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 6, 1.0)   # Long decay
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 7, 0.2)   # Low sustain
    
    for b in range(bars):
        offset = b * 4.0
        chord_root = progression[b % 4]
        
        # 4-part jazz voicings (Maj7, Min7, Min7, Dom7 handled diatonically)
        chord_notes = [
            get_scale_pitch(chord_root, 4),
            get_scale_pitch(chord_root + 2, 4),
            get_scale_pitch(chord_root + 4, 4),
            get_scale_pitch(chord_root + 6, 4)
        ]
        
        # Rhythm engine mirroring the clave
        rhythms = [
            (0.0, 1.0) if b % 2 == 0 else (0.5, 1.0),
            (1.5, 1.0) if b % 2 == 0 else (2.0, 1.5),
            (3.0, 0.75) if b % 2 == 0 else None
        ]
        
        for start, length in [r for r in rhythms if r is not None]:
            for note in chord_notes:
                add_midi_note(item_chords, take_chords, offset + start, length, note, 75)

    # ==========================================
    # TRACK 4: SOLO (ReaSynth Vibraphone)
    # ==========================================
    track_solo, item_solo, take_solo = create_bossa_track(f"{track_name}_Solo")
    fx_solo = RPR.RPR_TrackFX_AddByName(track_solo, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_solo, fx_solo, 0, 0.6)     # Vol
    RPR.RPR_TrackFX_SetParam(track_solo, fx_solo, 2, 0.0)     # 100% Sine
    RPR.RPR_TrackFX_SetParam(track_solo, fx_solo, 5, 0.005)   # Pluck attack
    RPR.RPR_TrackFX_SetParam(track_solo, fx_solo, 6, 0.6)     # Quick decay
    RPR.RPR_TrackFX_SetParam(track_solo, fx_solo, 7, 0.0)     # Zero sustain (percussive)

    for b in range(bars):
        offset = b * 4.0
        chord_root = progression[b % 4]
        
        # 16th note jazz runs
        if b % 2 == 0:
            # Ascending run into chord tone
            run = [chord_root, chord_root+1, chord_root+2, chord_root+3]
            for i, deg in enumerate(run):
                add_midi_note(item_solo, take_solo, offset + 1.0 + (i * 0.25), 0.25, get_scale_pitch(deg, 5), 85)
            # Resolve
            add_midi_note(item_solo, take_solo, offset + 2.0, 1.0, get_scale_pitch(chord_root+4, 5), 100)
        else:
            # Descending run
            run = [chord_root+4, chord_root+3, chord_root+2, chord_root+1]
            for i, deg in enumerate(run):
                add_midi_note(item_solo, take_solo, offset + 2.0 + (i * 0.25), 0.25, get_scale_pitch(deg, 5), 85)
            # Resolve
            add_midi_note(item_solo, take_solo, offset + 3.0, 1.0, get_scale_pitch(chord_root, 5), 100)

    # Force UI update
    RPR.RPR_UpdateArrange()

    return f"Created Bossa Nova Groove with Drums, Bass, Chords, and Solo over {bars} bars at {bpm} BPM in {key} {scale}."
