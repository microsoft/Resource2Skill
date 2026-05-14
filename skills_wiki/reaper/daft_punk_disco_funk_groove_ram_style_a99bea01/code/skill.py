def create_pattern(
    project_name: str = "RandomAccessMemories",
    track_name: str = "Daft_Groove",
    bpm: int = 115,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Daft Punk style Disco-Funk groove (ii-IV-vi-V) with Drums, Bass, Keys, and Guitar tracks.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_arr = SCALES.get(scale.lower(), SCALES["major"])
    
    # The Daft Punk signature loop: ii -> IV -> vi -> V (0-indexed degrees: 1, 3, 5, 4)
    progression_degrees = [1, 3, 5, 4]

    def get_scale_pitch(root_note, deg):
        octave = deg // len(scale_arr)
        idx = deg % len(scale_arr)
        return root_note + scale_arr[idx] + (octave * 12)

    # === Helper Functions ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len_sec = 60.0 / bpm

    def create_track_with_midi(name, length_bars):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item_length_sec = length_bars * 4 * beat_len_sec
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def add_note(take, beat_start, duration_beats, pitch, vel):
        proj_start = beat_start * beat_len_sec
        proj_length = duration_beats * beat_len_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start + proj_length)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    RPR.RPR_Undo_BeginBlock2(0)

    # === 1. DRUMS (4-on-the-floor Disco) ===
    drum_track, drum_take = create_track_with_midi(f"{track_name}_Drums", bars)
    for bar in range(bars):
        bar_beat = bar * 4
        # Kick (every beat)
        for b in [0, 1, 2, 3]:
            add_note(drum_take, bar_beat + b, 0.25, 36, velocity_base + 10)
        # Snare/Clap (beats 2 and 4)
        for b in [1, 3]:
            add_note(drum_take, bar_beat + b, 0.25, 38, velocity_base)
        # Closed Hat (on the beat)
        for b in [0.0, 1.0, 2.0, 3.0]:
            add_note(drum_take, bar_beat + b, 0.125, 42, velocity_base - 20)
        # Open Hat (on the off-beats)
        for b in [0.5, 1.5, 2.5, 3.5]:
            add_note(drum_take, bar_beat + b, 0.25, 46, velocity_base)
    RPR.RPR_MIDI_Sort(drum_take)

    # === 2. GROOVY BASS ===
    bass_track, bass_take = create_track_with_midi(f"{track_name}_Bass", bars)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    
    bass_rhythm = [0.0, 0.75, 1.5, 2.25, 3.0, 3.75] # Syncopated 16th groove
    for bar in range(bars):
        bar_beat = bar * 4
        deg = progression_degrees[bar % 4]
        root_pitch = get_scale_pitch(root_val + 36, deg) # C2 octave
        
        for r in bass_rhythm:
            add_note(bass_take, bar_beat + r, 0.25, root_pitch, velocity_base)
    RPR.RPR_MIDI_Sort(bass_take)

    # === 3. RHODES CHORDS ===
    chords_track, chords_take = create_track_with_midi(f"{track_name}_Keys", bars)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaEQ", False, -1) # Lowpass filter effect
    
    for bar in range(bars):
        bar_beat = bar * 4
        deg = progression_degrees[bar % 4]
        # Build a 7th chord (Root, 3rd, 5th, 7th in the scale)
        chord_pitches = [
            get_scale_pitch(root_val + 60, deg),
            get_scale_pitch(root_val + 60, deg + 2),
            get_scale_pitch(root_val + 60, deg + 4),
            get_scale_pitch(root_val + 60, deg + 6)
        ]
        
        # Rhythm: Big sustained chord on 1, anticipated push on 2.5
        for pitch in chord_pitches:
            add_note(chords_take, bar_beat + 0.0, 1.25, pitch, velocity_base - 10)
            add_note(chords_take, bar_beat + 1.5, 2.50, pitch, velocity_base - 10)
    RPR.RPR_MIDI_Sort(chords_take)

    # === 4. BONE TONE GUITAR ===
    gtr_track, gtr_take = create_track_with_midi(f"{track_name}_Guitar", bars)
    RPR.RPR_TrackFX_AddByName(gtr_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(gtr_track, "ReaEQ", False, -1) # Highpass for spanky tone
    RPR.RPR_TrackFX_AddByName(gtr_track, "ReaComp", False, -1)
    
    # 16th note stabs on the "e" and "a" of the beat
    gtr_rhythm = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75]
    for bar in range(bars):
        bar_beat = bar * 4
        deg = progression_degrees[bar % 4]
        # Play high triads
        chord_pitches = [
            get_scale_pitch(root_val + 72, deg),
            get_scale_pitch(root_val + 72, deg + 2),
            get_scale_pitch(root_val + 72, deg + 4)
        ]
        
        for r in gtr_rhythm:
            for pitch in chord_pitches:
                add_note(gtr_take, bar_beat + r, 0.1, pitch, velocity_base - 5)
    RPR.RPR_MIDI_Sort(gtr_take)

    RPR.RPR_Undo_EndBlock2(0, "Create Daft Punk Groove", -1)

    return f"Created Daft Punk style rhythm section ({bars} bars, {bpm} BPM) in {key} {scale}."
