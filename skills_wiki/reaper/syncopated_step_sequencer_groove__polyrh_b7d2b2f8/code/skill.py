def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative_Groove",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a polyrhythmic step-sequenced bassline and offbeat drum groove.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # === Music Theory / Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate base MIDI pitch (Octave 2 for Bass)
    base_midi = 36 + NOTE_MAP.get(key.upper(), 0)
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    step_len = bar_length_sec / 16.0  # Length of one 16th note in seconds

    # Helper function to insert notes using accurate PPQ timing
    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        # Ensure velocity is within bounds
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 1: Create Bass Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_SeqBass", True)

    # Add ReaSynth for basic tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Create MIDI Item for Bass
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", bar_length_sec * bars)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Insert Bass Notes (3-3-3-3-4 Euclidean rhythm)
    bass_steps = [0, 3, 6, 9, 12]
    total_bass_notes = 0
    for b in range(bars):
        bar_offset = b * bar_length_sec
        for step in bass_steps:
            start_time = bar_offset + step * step_len
            end_time = start_time + (step_len * 0.7) # Staccato 16th length
            
            # Octave jump on the last step of the bar for variation
            pitch = base_midi if step != 12 else base_midi + 12
            
            insert_note(bass_take, start_time, end_time, pitch, velocity_base)
            total_bass_notes += 1

    # === Step 2: Create Drum Track ===
    drum_track_idx = track_idx + 1
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)

    # Create MIDI Item for Drums
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", bar_length_sec * bars)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    total_drum_notes = 0
    for b in range(bars):
        bar_offset = b * bar_length_sec
        
        # Kick (Steps 0, 4, 8, 12) - GM MIDI 36
        for step in [0, 4, 8, 12]:
            st = bar_offset + step * step_len
            insert_note(drum_take, st, st + (step_len * 0.5), 36, velocity_base)
            total_drum_notes += 1
            
        # Snare (Steps 4, 12) - GM MIDI 38
        for step in [4, 12]:
            st = bar_offset + step * step_len
            insert_note(drum_take, st, st + (step_len * 0.5), 38, velocity_base)
            total_drum_notes += 1

        # Hi-Hats (Offbeats: 2, 6, 10, 14 + syncopation on 15) - GM MIDI 42
        for step in [2, 6, 10, 14, 15]:
            st = bar_offset + step * step_len
            vel = velocity_base if step != 15 else int(velocity_base * 0.7) # Ghost note on 15
            insert_note(drum_take, st, st + (step_len * 0.5), 42, vel)
            total_drum_notes += 1

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drum_take)

    return f"Created {track_name}_SeqBass and {track_name}_Drums over {bars} bars at {bpm} BPM with {total_bass_notes + total_drum_notes} notes."
