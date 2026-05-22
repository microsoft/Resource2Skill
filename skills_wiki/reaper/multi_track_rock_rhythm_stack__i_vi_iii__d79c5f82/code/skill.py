def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockStack",
    bpm: int = 150,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 3-track Rock Rhythm Stack (Drums, Bass, Guitars) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "B", "C#", "D").
        scale: Scale type ("major", "minor", etc.).
        bars: Number of bars to generate (cycles a 4-chord loop).
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }

    if scale not in SCALES:
        scale = "minor"
    if key not in NOTE_MAP:
        key = "B"

    scale_intervals = SCALES[scale]
    # Set C2 (MIDI 36) as base, then shift by key. 
    # For "B", this puts the base at 47 (B2).
    base_midi = 36 + NOTE_MAP[key]
    chord_root_midi = base_midi + 12 # Octave 3 for chords

    # i - VI - III - VII in minor, or I - V - vi - IV in major
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 4, 5, 3]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    cursor_pos = RPR.RPR_GetCursorPosition()

    def get_diatonic_triad(root_midi, degree_index):
        notes = []
        for i in [0, 2, 4]: # Root, Third, Fifth
            idx = (degree_index + i) % len(scale_intervals)
            octave_shift = (degree_index + i) // len(scale_intervals)
            notes.append(root_midi + scale_intervals[idx] + (octave_shift * 12))
        return notes

    def add_instrument_track(name, synth_setup_func):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Calculate item length
        beat_len = 60.0 / bpm
        item_len = beat_len * 4 * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Add and configure synth
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        synth_setup_func(track, fx_idx)
        
        return take

    def insert_note(take, start_time_sec, end_time_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # --- Synthesizer Configurations ---
    def setup_drums(track, fx_idx):
        # Percussive snap: 100% square, no sustain, 50ms release
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 1.0) # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0) # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.0) # Sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.05) # Release

    def setup_bass(track, fx_idx):
        # Deep sub bass: 100% triangle
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0) # Tri mix

    def setup_gtr(track, fx_idx):
        # Buzzy rhythm guitar: 80% Saw, 20% Square
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.8)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.0)

    # --- Track Creation ---
    take_drums = add_instrument_track(f"{track_name}_Drums", setup_drums)
    take_bass = add_instrument_track(f"{track_name}_Bass", setup_bass)
    take_gtr = add_instrument_track(f"{track_name}_Gtr", setup_gtr)

    # --- MIDI Generation ---
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    for b in range(bars):
        bar_start = cursor_pos + (b * bar_len)
        chord_idx = b % 4
        degree = progression[chord_idx]
        
        chord_notes = get_diatonic_triad(chord_root_midi, degree)
        bass_note = chord_notes[0] - 24 # Drop bass 2 octaves below chord root

        # 1. Bass: 8th notes
        for eighth in range(8):
            start = bar_start + (eighth * 0.5 * beat_len)
            end = start + (0.45 * beat_len) # Leave a slight gap for articulation
            insert_note(take_bass, start, end, bass_note, velocity_base)

        # 2. Rhythm Guitar: Whole note chords
        for note in chord_notes:
            insert_note(take_gtr, bar_start, bar_start + bar_len - (0.1 * beat_len), note, velocity_base - 15)

        # 3. Drums: Rock Beat
        # Kicks (MIDI 36) on Beat 1, the "and" of 2, and Beat 3
        insert_note(take_drums, bar_start + 0.0 * beat_len, bar_start + 0.2 * beat_len, 36, velocity_base)
        insert_note(take_drums, bar_start + 1.5 * beat_len, bar_start + 1.7 * beat_len, 36, velocity_base - 10)
        insert_note(take_drums, bar_start + 2.0 * beat_len, bar_start + 2.2 * beat_len, 36, velocity_base)

        # Snares (MIDI 38) on Beat 2 and 4
        insert_note(take_drums, bar_start + 1.0 * beat_len, bar_start + 1.2 * beat_len, 38, velocity_base + 5)
        insert_note(take_drums, bar_start + 3.0 * beat_len, bar_start + 3.2 * beat_len, 38, velocity_base + 5)

        # Hi-hats (MIDI 42) on 8th notes
        for eighth in range(8):
            start = bar_start + (eighth * 0.5 * beat_len)
            hat_vel = velocity_base if eighth % 2 == 0 else velocity_base - 25
            insert_note(take_drums, start, start + 0.15 * beat_len, 42, hat_vel)

    # --- Finalize ---
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_gtr)
    RPR.RPR_UpdateArrange()

    return f"Created Multi-Track Rhythm Stack (Drums, Bass, Gtr) over {bars} bars in {key} {scale} at {bpm} BPM."
