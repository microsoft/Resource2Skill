def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Trap Beat",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Trap Half-Time Drum Groove with Diatonic Chords and 808 in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length_sec = (sec_per_beat * beats_per_bar) * bars

    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_pitch(degree):
        """Convert a 0-indexed scale degree into a relative semitone pitch."""
        octave = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        return root_pitch + (octave * 12) + scale_intervals[rem]

    def get_diatonic_chord(degree, num_notes=3, octave_shift=4):
        """Build a diatonic chord by stacking thirds within the scale."""
        notes = []
        for i in range(num_notes):
            chord_degree = degree + (i * 2)
            pitch = get_pitch(chord_degree) + (octave_shift * 12)
            notes.append(pitch)
        return notes

    def insert_note(take, beat_pos, pitch, velocity, length_beats=0.25):
        """Helper to safely insert a MIDI note using beat positions."""
        start_sec = beat_pos * sec_per_beat
        end_sec = start_sec + (length_beats * sec_per_beat)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    notes_created = 0

    # ==========================================
    # Track 1: Trap Drums (Standard GM Mapping)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Patterns defined over a 2-bar loop (8 beats)
    kick_pattern = [0.0, 1.5, 4.0, 5.0, 6.5]
    snare_pattern = [2.0, 6.0]
    hat_pattern = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 
                   4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.25, 7.5, 7.75]

    for bar_pair in range((bars + 1) // 2):
        offset_beats = bar_pair * 8
        
        for b in kick_pattern:
            if offset_beats + b < bars * beats_per_bar:
                insert_note(drum_take, offset_beats + b, 36, velocity_base, 0.25)
                notes_created += 1
                
        for b in snare_pattern:
            if offset_beats + b < bars * beats_per_bar:
                insert_note(drum_take, offset_beats + b, 38, velocity_base, 0.25)
                notes_created += 1
                
        for b in hat_pattern:
            if offset_beats + b < bars * beats_per_bar:
                # Add dynamic velocity for hi-hat realism (accents on the beat, softer on rolls)
                vel = velocity_base if (b % 1 == 0) else int(velocity_base * 0.8)
                if b % 0.5 != 0: vel = int(velocity_base * 0.6) # 16th note rolls
                insert_note(drum_take, offset_beats + b, 42, vel, 0.125)
                notes_created += 1

    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # Track 2: 808 Bass (Matches Kick Rhythm)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} 808 Bass", True)
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # Simple sine synth to approximate an 808 tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)

    # (beat_pos, scale_degree, length)
    bass_pattern = [
        (0.0, 0, 1.0),   # Root
        (1.5, 0, 0.5),   # Root
        (4.0, 5, 0.5),   # 6th degree
        (5.0, 5, 0.5),   # 6th degree
        (6.5, 4, 1.0)    # 5th degree
    ]

    for bar_pair in range((bars + 1) // 2):
        offset_beats = bar_pair * 8
        for b_pos, degree, length in bass_pattern:
            if offset_beats + b_pos < bars * beats_per_bar:
                pitch = get_pitch(degree) + 36  # Base octave C2
                insert_note(bass_take, offset_beats + b_pos, pitch, velocity_base, length)
                notes_created += 1

    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # Track 3: Diatonic Pad/Chords
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    chord_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name} Chords", True)
    
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", item_length_sec)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)
    
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)

    # i to VI chord progression
    chords_pattern = [
        (0.0, 0, 4.0),  # Scale degree 0 (e.g. C minor)
        (4.0, 5, 4.0)   # Scale degree 5 (e.g. Ab Major)
    ]

    for bar_pair in range((bars + 1) // 2):
        offset_beats = bar_pair * 8
        for b_pos, degree, length in chords_pattern:
            if offset_beats + b_pos < bars * beats_per_bar:
                # Retrieve the correct diatonic triad for this scale degree
                chord_pitches = get_diatonic_chord(degree, num_notes=3, octave_shift=4)
                for p in chord_pitches:
                    insert_note(chord_take, offset_beats + b_pos, p, int(velocity_base * 0.7), length)
                    notes_created += 1

    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_UpdateTimeline()

    return f"Created Trap Groove (Drums, 808, Chords) with {notes_created} total notes over {bars} bars at {bpm} BPM in {key} {scale}."
