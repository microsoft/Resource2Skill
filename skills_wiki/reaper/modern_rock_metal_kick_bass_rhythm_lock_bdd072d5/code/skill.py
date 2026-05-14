def create_kick_bass_lock(
    project_name: str = "ModernRockGroove",
    bpm: int = 135,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a locked Kick and Bass groove typical of modern rock/metal in REAPER.
    
    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (should be a multiple of 4 for the progression).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string detailing the tracks and items created.
    """
    import reaper_python as RPR
    import math

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    }

    if scale not in SCALES:
        scale = "minor"
        
    root_val = NOTE_MAP.get(key, 0)
    current_scale = SCALES[scale]
    
    # Epic Rock Progression (i - VI - III - VII) - indices of the scale array
    progression_degrees = [0, 5, 2, 6] 
    bass_octave = 2 # MIDI octave 2 (e.g., D2)

    # Rhythmic Grid (in quarter note beats relative to start of a bar)
    # Syncopated Kick rhythm (16th note feel)
    kick_beats = [0.0, 0.75, 1.5, 2.5, 3.25] 
    snare_beats = [1.0, 3.0]
    hat_beats = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    
    beats_per_bar = 4
    
    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    start_time = RPR.RPR_GetCursorPosition()
    
    # Helper function to create a track and a MIDI item
    def create_midi_track(name, track_idx):
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item_length_sec = (60.0 / bpm) * beats_per_bar * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    num_tracks = RPR.RPR_CountTracks(0)
    
    # === Step 2: Create Drums Track ===
    drum_track, drum_take = create_midi_track("Locked Drums", num_tracks)
    
    # === Step 3: Create Bass Track ===
    bass_track, bass_take = create_midi_track("Locked Bass", num_tracks + 1)
    
    # Add ReaSynth to Bass
    fx_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a grittier bass (Square wave mix, drop tuning)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 1, 0.5) # Mix square wave
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 2, 0.2) # Extra attack
    
    # Add EQ to Bass
    eq_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)

    # === Step 4: Populate MIDI Data ===
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Determine bass pitch for this bar based on progression
        deg_index = progression_degrees[bar % len(progression_degrees)]
        degree_offset = current_scale[deg_index]
        
        # Adjust pitch down an octave if the interval is jumping too high (voice leading)
        if degree_offset > 7:
            degree_offset -= 12
            
        bass_pitch = root_val + (bass_octave * 12) + degree_offset
        
        # Write Hats
        for b in hat_beats:
            abs_beat = bar_start_beat + b
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time + (abs_beat * 60.0 / bpm))
            end_ppq = start_ppq + 120 # Short hat note
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, 42, velocity_base - 20, False)

        # Write Snares
        for b in snare_beats:
            abs_beat = bar_start_beat + b
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time + (abs_beat * 60.0 / bpm))
            end_ppq = start_ppq + 240
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, 38, velocity_base + 10, False)

        # Write Kicks & Locked Bass Notes
        for i, b in enumerate(kick_beats):
            abs_beat = bar_start_beat + b
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, start_time + (abs_beat * 60.0 / bpm))
            
            # Calculate duration until the next kick or the end of the bar
            if i < len(kick_beats) - 1:
                next_beat = kick_beats[i+1]
            else:
                next_beat = beats_per_bar
                
            duration_beats = next_beat - b
            # Leave a slight 16th-note gap for articulation (staccato feel)
            bass_duration = max(0.125, duration_beats - 0.125) 
            
            bass_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time + ((abs_beat + bass_duration) * 60.0 / bpm))
            kick_end_ppq = start_ppq + 120
            
            # Insert Kick (Drum Channel 10 -> index 9)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, kick_end_ppq, 9, 36, velocity_base, False)
            
            # Insert locked Bass note (Channel 1 -> index 0)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, bass_end_ppq, 0, bass_pitch, velocity_base, False)

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(bass_take)
    
    RPR.RPR_UpdateArrange()

    return f"Created Kick-Bass Lock: Added 'Locked Drums' and 'Locked Bass' ({bars} bars at {bpm} BPM in {key} {scale})."
