def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Drum Sequencer",
    bpm: int = 90,
    key: str = "C",      # Unused (drums are unpitched)
    scale: str = "major",# Unused
    bars: int = 4,
    velocity_base: int = 100,
    style: str = "boom_bap", # Options: 'boom_bap' or 'four_on_floor'
    **kwargs,
) -> str:
    """
    Create a Foundational MIDI Drum Groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM.
        key: Unused for GM drums.
        scale: Unused for GM drums.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        style: The rhythmic style of the beat ('boom_bap' or 'four_on_floor').
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and notes.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # General MIDI standard mapping
    KICK = 36
    SNARE = 38
    HAT_CLOSED = 42

    notes_created = 0

    # === Step 4: Generate Rhythm Based on Style ===
    for bar in range(bars):
        bar_start_qn = bar * 4.0

        if style == "four_on_floor":
            # Kicks on every downbeat (1, 2, 3, 4)
            for beat in range(4):
                start_qn = bar_start_qn + beat
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, velocity_base, False)
                notes_created += 1

            # Snares/Claps on 2 and 4
            for beat in [1, 3]:
                start_qn = bar_start_qn + beat
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
                notes_created += 1

            # Driving 8th note Hi-Hats with velocity accenting
            for eighth in range(8):
                start_qn = bar_start_qn + (eighth * 0.5)
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Downbeats hit harder than offbeats
                vel = velocity_base if eighth % 2 == 0 else max(10, velocity_base - 25)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, HAT_CLOSED, vel, False)
                notes_created += 1

        elif style == "boom_bap" or style != "four_on_floor":
            # Syncopated Kicks: 1, 2.5 (the "and" of 2), and 3
            kick_qns = [0.0, 1.5, 2.0]
            for kq in kick_qns:
                start_qn = bar_start_qn + kq
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Ghost note velocity for the syncopated kick
                vel = velocity_base if kq != 1.5 else max(10, velocity_base - 15)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, KICK, vel, False)
                notes_created += 1

            # Backbeat Snares on 2 and 4
            for sq in [1.0, 3.0]:
                start_qn = bar_start_qn + sq
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.25)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
                notes_created += 1

            # 8th note Hi-Hats with heavy velocity variation for groove
            for eighth in range(8):
                start_qn = bar_start_qn + (eighth * 0.5)
                start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
                end_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn + 0.125)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                vel = velocity_base if eighth % 2 == 0 else max(10, velocity_base - 35)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, HAT_CLOSED, vel, False)
                notes_created += 1

    # Commit MIDI changes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} GM drum notes (style: {style}) over {bars} bars at {bpm} BPM"
