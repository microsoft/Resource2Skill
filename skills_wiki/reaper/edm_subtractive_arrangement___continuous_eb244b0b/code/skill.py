def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Arrangement",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12, # Total arrangement length
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Subtractive Arrangement (Intro -> Verse -> Drop) in REAPER.
    
    Args:
        project_name: Project identifier.
        track_name: Prefix for generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars (should be multiple of 4, default 12).
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Setup core parameters
    root = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # i - VI - III - VII progression (Standard pop/EDM loop)
    progression = [0, 5, 2, 6] 
    
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    start_time = RPR.RPR_GetCursorPosition()
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    # Helper function to create a track with an instrument
    def create_instrument_track(name, synth=True, low_octave=False):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        if synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            if low_octave:
                # Lower the tuning for bass
                RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.25) # Tuning
                RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.1)  # Extra saw
                RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)  # Attack
                RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.1)  # Release
        else:
            # Drum synthesis via ReaSynth for kicks/snares
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)   # Attack
            RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.05)  # Quick Release
            
        return track

    tracks = {
        "Chords": create_instrument_track("Chords", synth=True),
        "Bass": create_instrument_track("Bass", synth=True, low_octave=True),
        "Drums": create_instrument_track("Drums", synth=False)
    }

    total_notes_created = 0

    # Build the arrangement block by block
    # Block 1 (Bars 0-3): Intro
    # Block 2 (Bars 4-7): Verse
    # Block 3 (Bars 8-11): Chorus (Drop)
    
    for bar in range(bars):
        chord_idx = progression[bar % 4]
        chord_root = root + scale_intervals[chord_idx]
        
        # Determine section
        is_intro = bar < 4
        is_verse = 4 <= bar < 8
        is_chorus = bar >= 8
        
        # PRE-DROP GAP: On the last bar of the verse (bar 7), mute everything on the 4th beat.
        active_beats = 4
        if bar == 7:
            active_beats = 3
            
        bar_start_time = start_time + (bar * bar_len)
        active_duration = beat_len * active_beats

        # --- 1. CHORDS TRACK ---
        # Always plays, to set the progression
        item_c = RPR.RPR_AddMediaItemToTrack(tracks["Chords"])
        RPR.RPR_SetMediaItemInfo_Value(item_c, "D_POSITION", bar_start_time)
        RPR.RPR_SetMediaItemInfo_Value(item_c, "D_LENGTH", active_duration)
        take_c = RPR.RPR_AddTakeToMediaItem(item_c)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_c, bar_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_c, bar_start_time + active_duration)
        
        # Triad
        for offset in [0, 3, 7]: # standard minor triad intervals logic roughly
            pitch = 60 + chord_root + offset
            RPR.RPR_MIDI_InsertNote(take_c, False, False, start_ppq, end_ppq, 0, pitch, 80, False)
            total_notes_created += 1
        RPR.RPR_MIDI_Sort(take_c)

        # --- 2. BASS TRACK ---
        # Plays in Verse and Chorus
        if is_verse or is_chorus:
            item_b = RPR.RPR_AddMediaItemToTrack(tracks["Bass"])
            RPR.RPR_SetMediaItemInfo_Value(item_b, "D_POSITION", bar_start_time)
            RPR.RPR_SetMediaItemInfo_Value(item_b, "D_LENGTH", active_duration)
            take_b = RPR.RPR_AddTakeToMediaItem(item_b)
            
            # Driving 8th notes
            for beat in range(active_beats * 2): # 8th notes
                note_start = bar_start_time + (beat * (beat_len / 2.0))
                note_end = note_start + (beat_len / 2.0) - 0.05 # staccato
                start_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_b, note_start)
                end_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_b, note_end)
                
                RPR.RPR_MIDI_InsertNote(take_b, False, False, start_p, end_p, 0, 36 + chord_root, 100, False)
                total_notes_created += 1
            RPR.RPR_MIDI_Sort(take_b)

        # --- 3. DRUMS TRACK ---
        # Subtractive logic: 
        # Intro: No drums
        # Verse: Kicks only
        # Chorus: Full Kicks, Snares, Hats
        if is_verse or is_chorus:
            item_d = RPR.RPR_AddMediaItemToTrack(tracks["Drums"])
            RPR.RPR_SetMediaItemInfo_Value(item_d, "D_POSITION", bar_start_time)
            RPR.RPR_SetMediaItemInfo_Value(item_d, "D_LENGTH", active_duration)
            take_d = RPR.RPR_AddTakeToMediaItem(item_d)
            
            for beat in range(active_beats):
                # Kick (Every beat)
                k_start = bar_start_time + (beat * beat_len)
                k_start_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_d, k_start)
                k_end_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_d, k_start + 0.1)
                RPR.RPR_MIDI_InsertNote(take_d, False, False, k_start_p, k_end_p, 9, 36, 120, False)
                total_notes_created += 1
                
                if is_chorus:
                    # Snare (Beats 2 and 4)
                    if beat in [1, 3]:
                        RPR.RPR_MIDI_InsertNote(take_d, False, False, k_start_p, k_end_p, 9, 38, 110, False)
                        total_notes_created += 1
                    
                    # Hi-Hat (Offbeats)
                    h_start = bar_start_time + (beat * beat_len) + (beat_len / 2.0)
                    if beat < active_beats - 1 or active_beats == 4: # Don't place hat outside active boundary
                        h_start_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_d, h_start)
                        h_end_p = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_d, h_start + 0.05)
                        RPR.RPR_MIDI_InsertNote(take_d, False, False, h_start_p, h_end_p, 9, 42, 90, False)
                        total_notes_created += 1
                        
            RPR.RPR_MIDI_Sort(take_d)

    RPR.RPR_UpdateArrange()
    return f"Created subtractive arrangement across 3 tracks with {total_notes_created} notes over {bars} bars at {bpm} BPM."
