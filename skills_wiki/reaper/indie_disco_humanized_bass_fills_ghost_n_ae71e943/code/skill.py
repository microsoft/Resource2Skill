def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Indie Disco Bass",
    bpm: int = 124,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates an Indie Disco bassline with humanized 16th-note fills and ghost notes.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (must be multiple of 4 for best results).
        velocity_base: Base MIDI velocity for accented notes (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Step 2: Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Step 3: Configure MIDI Item
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    item_length = bar_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Base pitch calculation (E1 = 28 to E2 = 40 is the typical bass "pocket")
    root_val = NOTE_MAP.get(key.capitalize(), 9)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_midi_pitch = 24 + root_val # C1 is 24

    # Helper function to insert a single note
    def insert_note(start_beat, length_beats, pitch, velocity):
        start_time = start_beat * beat_sec
        end_time = start_time + (length_beats * beat_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # The progression from the tutorial: VI - I - VI - VII
    # In minor, these are indices 5, 0, 5, 6.
    prog_indices = [5, 0, 5, 6]
    note_count = 0

    for b_idx in range(bars):
        chord_degree_index = prog_indices[b_idx % len(prog_indices)]
        semitone_offset = scale_intervals[chord_degree_index]
        
        chord_pitch = base_midi_pitch + semitone_offset
        # Fold pitch into the bass pocket (prevent playing too high or low)
        while chord_pitch > 40:
            chord_pitch -= 12
        while chord_pitch < 28:
            chord_pitch += 12

        start_beat_of_bar = b_idx * beats_per_bar

        # If it's the 4th bar of the phrase, inject the 16th-note syncopated fill
        if b_idx % 4 == 3:
            # Beats 1 and 2: Standard 8th notes
            for beat_offset in [0.0, 0.5, 1.0, 1.5]:
                insert_note(start_beat_of_bar + beat_offset, 0.45, chord_pitch, velocity_base)
                note_count += 1
            
            # Beat 3 and 4: Indie Disco Fill with Dead Notes
            # 3.0: Octave (Accented)
            insert_note(start_beat_of_bar + 2.0, 0.23, chord_pitch + 12, velocity_base + 10)
            # 3.25: Ghost note on root
            insert_note(start_beat_of_bar + 2.25, 0.05, chord_pitch, 40)
            # 3.5: Perfect 5th
            insert_note(start_beat_of_bar + 2.5, 0.23, chord_pitch + 7, velocity_base - 5)
            # 3.75: Ghost note on root
            insert_note(start_beat_of_bar + 2.75, 0.05, chord_pitch, 40)
            
            # 4.0: Perfect 5th
            insert_note(start_beat_of_bar + 3.0, 0.23, chord_pitch + 7, velocity_base)
            # 4.25: Octave
            insert_note(start_beat_of_bar + 3.25, 0.23, chord_pitch + 12, velocity_base)
            # 4.5: Ghost note on root
            insert_note(start_beat_of_bar + 3.5, 0.05, chord_pitch, 40)
            # 4.75: Pick-up note into the next bar
            insert_note(start_beat_of_bar + 3.75, 0.25, chord_pitch, velocity_base - 10)
            
            note_count += 8
            
        else:
            # Standard driving 8th notes
            for beat_offset in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
                # Slight velocity humanization (accent the downbeats slightly)
                vel = velocity_base if (beat_offset % 1.0 == 0) else velocity_base - 15
                insert_note(start_beat_of_bar + beat_offset, 0.45, chord_pitch, vel)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # Step 4: Add FX Chain (ReaSynth, ReaEQ, ReaComp)
    # ReaSynth for tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth: fast attack, plucky decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.5)  # Square mix
    
    # ReaEQ to boost low end
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Set band 1 to a low shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0) # Tab 1 (Low Shelf)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 100) # Freq 100Hz (normalized value approx 0.2 in some ReaEQ versions, but keeping simple)
    
    # ReaComp to catch the ghost notes and level the performance
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -18.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio 4:1
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 0.01)  # Fast attack for slap/ghosts
    
    return f"Created '{track_name}' with {note_count} notes over {bars} bars (featuring ghost notes and turnaround fills) at {bpm} BPM."
