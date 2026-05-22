def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "80s Electro Algorithmic Drums",
    bpm: int = 120,
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an 80s Electro Offbeat Drum Sequence in the current REAPER project.
    Mimics the output of an algorithmic drum sequencer using standard MIDI mapping.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for accented downbeats (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string with details of the generated sequence.
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
    qns_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    def insert_note(qn_pos, qn_len, pitch, vel):
        """Helper to insert a note based on quarter note positions."""
        start_time = qn_pos * (60.0 / bpm)
        end_time = (qn_pos + qn_len) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    note_count = 0
    
    # === Step 4: Generate Drum Pattern ===
    # MIDI Map: 36=Kick, 38=Snare, 42=Closed Hat, 46=Open Hat
    for b in range(bars):
        offset = b * qns_per_bar

        # Kick Drum: Syncopated electro pattern (Beats 1, 2.5, 3, 4.5)
        kicks = [0.0, 1.5, 2.0, 3.5]
        for k in kicks:
            insert_note(offset + k, 0.25, 36, velocity_base)
            note_count += 1

        # Snare Drum: Solid backbeat (Beats 2, 4)
        snares = [1.0, 3.0]
        for s in snares:
            insert_note(offset + s, 0.25, 38, velocity_base)
            note_count += 1

        # Hi-hats: Continuous 16th notes with velocity dynamics
        for i in range(16):
            hat_pos = i * 0.25
            
            if i % 4 == 0:
                # Downbeats (Quarter notes) - Full accent
                vel = velocity_base
                insert_note(offset + hat_pos, 0.125, 42, vel)
            elif i % 2 == 0:
                # Upbeats (8th notes) - Medium accent
                vel = int(velocity_base * 0.8)
                
                # Replace specific closed hats with open hats for 'pump' effect
                # Placed on the "and" of beat 2 and the "and" of beat 4
                if i == 6 or i == 14:
                    insert_note(offset + hat_pos, 0.25, 46, vel) 
                else:
                    insert_note(offset + hat_pos, 0.125, 42, vel)
            else:
                # 16th note subdivisions - Softest hits
                vel = int(velocity_base * 0.6)
                insert_note(offset + hat_pos, 0.125, 42, vel)
                
            note_count += 1

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} programmatic MIDI drum notes over {bars} bars at {bpm} BPM."
