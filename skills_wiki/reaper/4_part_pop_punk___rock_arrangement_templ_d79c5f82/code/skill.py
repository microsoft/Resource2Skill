def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock_Ensemble",
    bpm: int = 130,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an interlocking 4-part Rock/Pop arrangement (Drums, Bass, Rhythm, Lead)
    using the classic vi-IV-I-V progression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)

    # Progression: vi - IV - I - V (Major) or i - VI - III - VII (Minor)
    if "minor" in scale.lower():
        progression = [0, 5, 2, 4]
    else:
        progression = [5, 3, 0, 4]

    # Helper to calculate diatonic triads
    def get_chord_notes(degree, octave):
        r_idx = degree
        t_idx = degree + 2
        f_idx = degree + 4
        
        r_p = scale_intervals[r_idx % scale_len] + 12 * (r_idx // scale_len)
        t_p = scale_intervals[t_idx % scale_len] + 12 * (t_idx // scale_len)
        f_p = scale_intervals[f_idx % scale_len] + 12 * (f_idx // scale_len)
        
        return [r_p + octave * 12, t_p + octave * 12, f_p + octave * 12]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks and Folder ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)

    tracks = []
    track_roles = ["Drums", "Bass", "Rhythm", "Lead"]
    for i, role in enumerate(track_roles):
        child_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(child_idx, True)
        trk = RPR.RPR_GetTrack(0, child_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", f"{track_name}_{role}", True)
        
        # Close folder on the last track
        if i == len(track_roles) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(trk, "I_FOLDERDEPTH", -1)
            
        tracks.append(trk)

    track_drums, track_bass, track_rhythm, track_lead = tracks

    # Add default synths to melodic tracks
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_rhythm, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_lead, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Items ===
    beat_len = 60.0 / bpm
    total_len = beat_len * 4 * bars

    def add_midi_item(trk):
        item = RPR.RPR_AddMediaItemToTrack(trk)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        return RPR.RPR_AddTakeToMediaItem(item)

    take_d = add_midi_item(track_drums)
    take_b = add_midi_item(track_bass)
    take_r = add_midi_item(track_rhythm)
    take_l = add_midi_item(track_lead)

    def insert_note(take, pitch, beat_start, beat_length, vel):
        start_time = beat_start * beat_len
        end_time = (beat_start + beat_length) * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 4: Populate MIDI Sequences ===
    for b in range(bars):
        bar_beat = b * 4
        degree = progression[b % len(progression)]
        
        # 1. Drums (Rock Groove)
        # Kick (36) on 1, 3, and 3.5
        insert_note(take_d, 36, bar_beat + 0, 0.25, velocity_base)
        insert_note(take_d, 36, bar_beat + 2, 0.25, velocity_base)
        insert_note(take_d, 36, bar_beat + 2.5, 0.25, velocity_base)
        # Snare (38) on 2 and 4
        insert_note(take_d, 38, bar_beat + 1, 0.25, velocity_base)
        insert_note(take_d, 38, bar_beat + 3, 0.25, velocity_base)
        # Hi-Hats (42) on straight 8th notes
        for i in range(8):
            hat_vel = velocity_base if i % 2 == 0 else max(1, velocity_base - 20)
            insert_note(take_d, 42, bar_beat + i * 0.5, 0.25, hat_vel)
        # Crash (49) on very first downbeat
        if b == 0:
            insert_note(take_d, 49, bar_beat + 0, 0.5, velocity_base + 10)

        # 2. Bass (Driving 8th notes)
        chord_notes = get_chord_notes(degree, 3) # Octave 3 reference
        bass_note = chord_notes[0] + root_pitch - 12 # Octave 2 playback
        for i in range(8):
            b_vel = velocity_base if i % 2 == 0 else max(1, velocity_base - 10)
            insert_note(take_b, bass_note, bar_beat + i * 0.5, 0.45, b_vel)

        # 3. Rhythm Guitar (Sustained whole note chords)
        rhythm_chord = get_chord_notes(degree, 4) # Octave 4
        for note in rhythm_chord:
            insert_note(take_r, note + root_pitch, bar_beat, 4.0, velocity_base - 10)

        # 4. Lead Guitar (Arpeggio: Root - 5th - 3rd - 5th)
        lead_chord = get_chord_notes(degree, 5) # Octave 5
        arp_pattern = [0, 2, 1, 2] # Indexing into the triad
        for i in range(8):
            idx = arp_pattern[i % 4]
            lead_note = lead_chord[idx] + root_pitch
            insert_note(take_l, lead_note, bar_beat + i * 0.5, 0.4, velocity_base)

    # Sort MIDI events
    for take in [take_d, take_b, take_r, take_l]:
        RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' ensemble (4 tracks) over {bars} bars at {bpm} BPM in {key} {scale}"
