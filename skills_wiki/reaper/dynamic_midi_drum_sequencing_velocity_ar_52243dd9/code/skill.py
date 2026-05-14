def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Drum Kit",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Dynamic MIDI Drum Groove with velocity articulations.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (used to offset GM drum map for tuned 808s; C = standard GM).
        scale: Scale type (unused for standard drums, kept for signature compatibility).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for accents.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Music theory lookup table to determine root offset
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key, 0)
    
    # Compute MIDI pitches based on Key. 
    # If key is "C" (0), standard GM mapping is perfectly preserved.
    # If another key is provided, the kit transposes (useful for pitched 808s).
    kick_note = 36 + root_val
    snare_note = 38 + root_val
    hh_closed = 42 + root_val
    crash = 49 + root_val

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
    
    # Add a MIDI item that spans the requested number of bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    note_count = 0

    # === Step 4: Populate Rhythmic Pattern with Dynamic Velocity ===
    for b in range(bars):
        bar_qn = b * 4.0
        
        # 1. KICK: On beats 1, 3, and a syncopated kick on the "and" of 3
        kicks_qn = [0.0, 2.0, 2.5]
        for q in kicks_qn:
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.25),
                1, kick_note, velocity_base, False)
            note_count += 1
                
        # 2. SNARE: Backbeats on 2 and 4, plus 16th ghost notes
        # Format: (QN position, velocity)
        snares = [
            (1.0, velocity_base),                     # Solid backbeat (Beat 2)
            (2.75, int(velocity_base * 0.4)),         # Ghost note before Beat 4
            (3.0, velocity_base),                     # Solid backbeat (Beat 4)
            (4.75, int(velocity_base * 0.4))          # Ghost note leading into next bar
        ]
        for q, vel in snares:
            # Prevent ghost notes from bleeding past bar 4.0
            if q < 4.0:
                RPR.RPR_MIDI_InsertNote(take, False, False, 
                    RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                    RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.15),
                    1, snare_note, vel, False)
                note_count += 1
                
        # 3. HI-HAT: 8th notes with alternating accents
        for i in range(8):
            q = i * 0.5
            # Accent the downbeats (0.0, 1.0, 2.0, 3.0), lower velocity on off-beats
            hh_vel = velocity_base if i % 2 == 0 else int(velocity_base * 0.6)
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.15),
                1, hh_closed, hh_vel, False)
            note_count += 1
                
        # 4. CRASH: Emphasize the downbeat of the very first bar
        if b == 0:
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + 0.0),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + 0.5),
                1, crash, velocity_base, False)
            note_count += 1

    # Finalize MIDI structure
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Drum Bus FX Chain ===
    # Pre-loading standard mixing tools for the drum bus
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)

    return f"Created '{track_name}' with {note_count} articulated drum notes over {bars} bars at {bpm} BPM."
