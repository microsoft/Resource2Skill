def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered to reduce harsh pick attack as per tutorial
    **kwargs,
) -> str:
    """
    Create a heavy kick-locked bass pattern with octave jumps and velocity taming.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note for the drop-tuned pedal.
        scale: Scale type (unused as we strictly pedal the root/octave here).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (capped lower to tame harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    # Note lookup table
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as a placeholder DI Bass
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to a low, tight square/saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Tuning (0 = neutral)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5) # Saw shape
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0) # Release (tight/staccato)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)

    # === Step 4: Generate Kick-Locked MIDI Notes ===
    # A standard syncopated Djent/Metalcore kick groove (positions in beats)
    kick_rhythm = [0.0, 0.75, 1.5, 2.0, 2.5, 3.25]
    
    # Staccato notes to leave space in the riff
    note_length_beats = 0.25 
    
    # Establish drop tuning root (MIDI note 24 = C1, typical metal bass register)
    root_note = NOTE_MAP.get(key, 0) + 24 
    octave_note = root_note + 12
    
    qn_length = 60.0 / bpm
    note_count = 0
    
    for b in range(bars):
        for pos_beats in kick_rhythm:
            # Emulate the tutorial's variation: On the final bar, follow the guitar up to the 12th fret
            is_octave_jump = (b == bars - 1 and pos_beats >= 2.0)
            pitch = octave_note if is_octave_jump else root_note
            
            # Minor velocity humanization, heavily centered around the tamed '110' mark
            vel = max(10, min(127, velocity_base - (note_count % 3)))
            
            start_time = (b * beats_per_bar * qn_length) + (pos_beats * qn_length)
            end_time = start_time + (note_length_beats * qn_length)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, vel, False
            )
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} staccato notes over {bars} bars. Velocity tamed to {velocity_base} and locked to a syncopated groove in Drop {key}."
