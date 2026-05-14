def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Fixed internally to 12 to demonstrate the 3-part sequence
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' Arrangement Structure in the current REAPER project.
    Generates an A-A-B timeline sequence demonstrating repetition and variation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored (overridden to 12 bars to fit the pattern logic).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks and FX ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Chords Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chords_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)
    RPR.RPR_SetMediaTrackInfo_Value(chords_track, "D_VOL", 0.4)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)

    # Melody Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    melody_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(melody_track, "P_NAME", f"{track_name}_Melody", True)
    RPR.RPR_SetMediaTrackInfo_Value(melody_track, "D_VOL", 0.6)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaDelay", False, -1)

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
    
    root_midi = NOTE_MAP.get(key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])

    # === Helper Functions ===
    def get_pitch(degree, r_midi, inters, oct_val):
        idx = degree % len(inters)
        oct_offset = degree // len(inters)
        return r_midi + inters[idx] + (oct_val + oct_offset) * 12

    def get_chord_pitches(degree, r_midi, inters, oct_val=4):
        return [get_pitch(degree + i, r_midi, inters, oct_val) for i in [0, 2, 4]]

    def insert_midi_item(track, start_beat, length_beats, name):
        sec_per_beat = 60.0 / bpm
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_beat * sec_per_beat)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_beats * sec_per_beat)
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", name, True)
        return take, start_beat * sec_per_beat

    def add_note(take, item_start_sec, start_beat_in_item, len_beats, pitch, vel):
        sec_per_beat = 60.0 / bpm
        start_time = item_start_sec + start_beat_in_item * sec_per_beat
        end_time = start_time + len_beats * sec_per_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        safe_vel = max(1, min(127, int(vel)))
        safe_pitch = max(0, min(127, int(pitch)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, safe_pitch, safe_vel, False)

    # === Note Generation Routines ===
    def populate_chords_A(take, st_sec):
        degrees = [3, 4, 2, 5] # IV, V, iii, vi
        for bar, deg in enumerate(degrees):
            pitches = get_chord_pitches(deg, root_midi, intervals, 4)
            bass = get_pitch(deg, root_midi, intervals, 3)
            for p in pitches + [bass]:
                add_note(take, st_sec, bar * 4.0, 4.0, p, velocity_base - 10)
        RPR.RPR_MIDI_Sort(take)

    def populate_melody_A(take, st_sec):
        # Syncopated rhythm: (beat_in_bar, length, scale_degree)
        motif = [(0.0, 1.5, 5), (1.5, 1.0, 4), (2.5, 1.5, 3)]
        offsets = [0, 1, -1, 2] # Shift motif with chords
        for bar, offset in enumerate(offsets):
            for beat, length, deg in motif:
                pitch = get_pitch(deg + offset, root_midi, intervals, 5)
                add_note(take, st_sec, bar * 4.0 + beat, length, pitch, velocity_base)
        RPR.RPR_MIDI_Sort(take)

    def populate_chords_B(take, st_sec):
        degrees = [1, 4, 0, 3] # Contrasting progression: ii, V, I, IV
        for bar, deg in enumerate(degrees):
            pitches = get_chord_pitches(deg, root_midi, intervals, 4)
            bass = get_pitch(deg, root_midi, intervals, 3)
            for p in pitches + [bass]:
                add_note(take, st_sec, bar * 4.0, 4.0, p, velocity_base - 10)
        RPR.RPR_MIDI_Sort(take)

    def populate_melody_B(take, st_sec):
        # Contrasting fast arpeggiated motif
        bases = [1, 4, 0, 3]
        for bar, base_deg in enumerate(bases):
            for i, step in enumerate([0, 2, 4, 7]): # Arpeggio 1-3-5-8
                pitch = get_pitch(base_deg + step, root_midi, intervals, 5)
                add_note(take, st_sec, bar * 4.0 + (i * 1.0), 1.0, pitch, velocity_base + 10)
        RPR.RPR_MIDI_Sort(take)

    # === Step 3: Arrange Items on Timeline ===
    
    # Iteration 1: Idea A (Establish) -> Bars 1-4 (Beats 0-16)
    t_c1, s_c1 = insert_midi_item(chords_track, 0, 16, "Idea A (Establish)")
    populate_chords_A(t_c1, s_c1)
    t_m1, s_m1 = insert_midi_item(melody_track, 0, 16, "Idea A (Establish)")
    populate_melody_A(t_m1, s_m1)

    # Iteration 2: Idea A (Reinforce) -> Bars 5-8 (Beats 16-32)
    t_c2, s_c2 = insert_midi_item(chords_track, 16, 16, "Idea A (Reinforce)")
    populate_chords_A(t_c2, s_c2)
    t_m2, s_m2 = insert_midi_item(melody_track, 16, 16, "Idea A (Reinforce)")
    populate_melody_A(t_m2, s_m2)

    # Iteration 3: Idea B (Vary) -> Bars 9-12 (Beats 32-48)
    t_c3, s_c3 = insert_midi_item(chords_track, 32, 16, "Idea B (Vary - Break the loop!)")
    populate_chords_B(t_c3, s_c3)
    t_m3, s_m3 = insert_midi_item(melody_track, 32, 16, "Idea B (Vary - Break the loop!)")
    populate_melody_B(t_m3, s_m3)

    return f"Created 'Rule of 3' arrangement tracks ({track_name}) with an A-A-B structural variation over 12 bars at {bpm} BPM."
