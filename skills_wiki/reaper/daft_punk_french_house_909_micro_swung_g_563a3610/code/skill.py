def create_pattern(
    project_name: str = "FrenchHouse",
    track_name: str = "909 Groove",
    bpm: int = 124,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a French House drum groove and syncopated bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the base drum track.
        bpm: Tempo in BPM (120-127 recommended for French House).
        key: Root note for the bassline (C, C#, D, ..., B).
        scale: Scale type for the bassline (minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: swing (float) - Swing amount between 0.5 (straight) and 0.75 (dotted). Default 0.62.

    Returns:
        Status string.
    """
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

    import reaper_python as RPR

    # Parameters
    swing_amt = kwargs.get("swing", 0.62)
    swing_amt = max(0.5, min(0.75, swing_amt))  # Clamp between 50% and 75% swing
    
    # 1. Set BPM
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate item length in seconds
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars

    # ==========================================
    # TRACK 1: THE DRUMS (French House Groove)
    # ==========================================
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} (Drums)", True)

    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, item_length, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)

    # Standard GM Drum Map
    KICK = 36
    CLAP = 39
    CH = 42  # Closed Hat
    OH = 46  # Open Hat

    note_count = 0
    def add_drum_note(pitch, start_beat, end_beat, vel):
        nonlocal note_count
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_beat * sec_per_beat)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_beat * sec_per_beat)
        # MIDI channel 10 (index 9) for drums
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, pitch, max(1, min(127, int(vel))), False)
        note_count += 1

    for bar in range(bars):
        for beat in range(4):
            curr_b = bar * 4 + beat

            # 4-on-the-floor Kick
            add_drum_note(KICK, curr_b, curr_b + 0.25, velocity_base + 10)

            # Clap on beats 2 and 4
            if beat in (1, 3):
                add_drum_note(CLAP, curr_b, curr_b + 0.25, velocity_base)

            # Rigid Open Hat on the offbeat
            add_drum_note(OH, curr_b + 0.5, curr_b + 0.75, velocity_base - 5)

            # Ghosted, Swung Closed Hats on the 16th subdivisions ("e" and "a")
            # Using swing parameter to delay these specific notes
            pos_e = curr_b + (swing_amt * 0.5)
            pos_a = curr_b + 0.5 + (swing_amt * 0.5)
            
            # Lower velocity (ghost notes)
            add_drum_note(CH, pos_e, pos_e + 0.15, velocity_base - 35)
            add_drum_note(CH, pos_a, pos_a + 0.15, velocity_base - 35)

    RPR.RPR_MIDI_Sort(drum_take)
    
    # Add Comp to glue the drum bus
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaComp (Cockos)", False, -1)

    # ==========================================
    # TRACK 2: THE BASSLINE (Syncopated)
    # ==========================================
    bass_track_idx = drum_track_idx + 1
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} (Synth Bass)", True)

    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, item_length, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)

    # Music Theory lookup
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    bass_base = 36 + root_val  # Start in C2 octave range

    def get_scale_note(degree, octave=0):
        deg = degree % len(scale_intervals)
        oct_shift = degree // len(scale_intervals)
        return bass_base + scale_intervals[deg] + (oct_shift + octave) * 12

    def add_bass_note(start_beat, end_beat, degree, octave=0, vel=velocity_base):
        nonlocal note_count
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_beat * sec_per_beat)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_beat * sec_per_beat)
        pitch = get_scale_note(degree, octave)
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, pitch, max(1, min(127, int(vel))), False)
        note_count += 1

    for bar in range(bars):
        bar_b = bar * 4
        # Syncopated offbeat bass pattern locking into the drum spaces
        add_bass_note(bar_b + 0.5, bar_b + 1.0, 0, 0)           # Root on the offbeat
        add_bass_note(bar_b + 1.25, bar_b + 1.5, 6, -1)         # Minor 7th (sub-octave drop before beat 2)
        add_bass_note(bar_b + 1.5, bar_b + 2.0, 0, 0)           # Root returns
        add_bass_note(bar_b + 2.5, bar_b + 3.0, 2, 0)           # Minor 3rd bounce
        add_bass_note(bar_b + 3.5, bar_b + 4.0, 4, 0)           # Perfect 5th lead-in

    RPR.RPR_MIDI_Sort(bass_take)

    # Add ReaSynth for basic playback tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)

    return f"Created French House Groove: 2 tracks ('{track_name} Drums' & 'Bass'), {note_count} total notes over {bars} bars at {bpm} BPM with {int(swing_amt*100)}% swing."
