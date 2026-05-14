def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Band Template", # Base name, will be expanded
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Multi-Instrument Framework (Drums, Bass, Rhythm, Lead)
    to facilitate multi-track MIDI editing and composition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored here as we hardcode the 4 roles).
        bpm: Tempo in BPM.
        key: Root note (e.g., "B").
        scale: "major" or "minor".
        bars: Number of bars for the looping progression.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # Set up music theory constants
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Choose progression based on scale type
    if scale.lower() == "minor":
        prog_degrees = [0, 5, 2, 6]  # i - VI - III - VII
    else:
        prog_degrees = [0, 4, 5, 3]  # I - V - vi - IV
        scale = "major" # fallback normalization
        
    scale_intervals = SCALES[scale]
    root_base = NOTE_MAP.get(key, 11) + 48  # Octave 4 base (e.g., C4 = 48)

    # Initialize Environment
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    proj_start_time = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    def make_color(r, g, b):
        # REAPER custom color encoding
        return (r | (g << 8) | (b << 16)) | 0x1000000

    tracks_to_create = [
        {"name": "01 MIDI Drums", "color": make_color(50, 50, 255), "role": "drums"},
        {"name": "02 BASS", "color": make_color(150, 50, 200), "role": "bass"},
        {"name": "03 GTR RHY", "color": make_color(255, 120, 50), "role": "rhythm"},
        {"name": "04 GTR LEAD", "color": make_color(50, 200, 255), "role": "lead"},
    ]

    total_notes_created = 0

    for i, t_info in enumerate(tracks_to_create):
        # 1. Create Track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])

        # 2. Add ReaSynth to ensure it's audible
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        if t_info["role"] == "bass":
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

        # 3. Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", proj_start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # 4. Generate MIDI Notes based on Role
        for bar in range(bars):
            bar_start_time = proj_start_time + (bar * bar_length_sec)
            
            # Figure out current chord
            deg = prog_degrees[bar % len(prog_degrees)]
            chord_notes = []
            for third in [0, 2, 4]: # Root, 3rd, 5th
                idx = (deg + third) % 7
                octave_shift = (deg + third) // 7
                chord_notes.append(root_base + scale_intervals[idx] + (octave_shift * 12))

            # Role: DRUMS
            if t_info["role"] == "drums":
                for beat in range(4):
                    beat_time = bar_start_time + (beat * beat_length_sec)
                    # Kick on 1 and 3
                    if beat in [0, 2]:
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + 0.1)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 36, velocity_base, False)
                        total_notes_created += 1
                    # Snare on 2 and 4
                    if beat in [1, 3]:
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + 0.1)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 38, velocity_base, False)
                        total_notes_created += 1
                    # Hats every 8th note
                    for hh in range(2):
                        hh_time = beat_time + (hh * beat_length_sec / 2.0)
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time + 0.05)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 42, velocity_base - 20, False)
                        total_notes_created += 1

            # Role: BASS
            elif t_info["role"] == "bass":
                root_bass = chord_notes[0] - 24 # 2 octaves down
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * bar_length_sec / 8.0)
                    st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (bar_length_sec / 8.0) - 0.02)
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, root_bass, velocity_base, False)
                    total_notes_created += 1

            # Role: RHYTHM GUITAR
            elif t_info["role"] == "rhythm":
                st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
                en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time + bar_length_sec - 0.05)
                for note in chord_notes:
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, note - 12, velocity_base - 10, False)
                    total_notes_created += 1

            # Role: LEAD GUITAR
            elif t_info["role"] == "lead":
                arp_pattern = [chord_notes[0], chord_notes[2], chord_notes[0]+12, chord_notes[2]]
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * bar_length_sec / 8.0)
                    st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (bar_length_sec / 8.0) - 0.02)
                    arp_note = arp_pattern[eighth % 4]
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, arp_note, velocity_base + 10, False)
                    total_notes_created += 1

        # Sort MIDI events for the track so it plays properly
        RPR.RPR_MIDI_Sort(take)

    # Optional: Update arrange view
    RPR.RPR_UpdateTimeline()

    return f"Created 4-track band template ({key} {scale}) with {total_notes_created} notes over {bars} bars at {bpm} BPM."
