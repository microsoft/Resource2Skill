def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Drum Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a layered 16th-note drum groove and a fully routed multi-out drum bus.
    Replicates the track management, routing, and dynamic processing shown in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the master drum folder.
        bpm: Tempo in BPM.
        key: Root note (unused for drums, preserved for signature).
        scale: Scale type (unused for drums, preserved for signature).
        bars: Number of bars to generate (default 2 to match tutorial loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated track architecture.
    """
    import reaper_python as RPR

    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Get current state
    num_tracks = RPR.RPR_CountTracks(0)
    cursor_pos = RPR.RPR_GetCursorPosition()
    
    # Track indices for our creation block
    idx_folder = num_tracks
    idx_midi = num_tracks + 1
    idx_kick = num_tracks + 2
    idx_snare = num_tracks + 3
    idx_hats = num_tracks + 4
    idx_claps = num_tracks + 5

    # === 1. Create Master Folder Track ===
    RPR.RPR_InsertTrackAtIndex(idx_folder, True)
    folder_trk = RPR.RPR_GetTrack(0, idx_folder)
    RPR.RPR_GetSetMediaTrackInfo_String(folder_trk, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(folder_trk, "I_FOLDERDEPTH", 1) # Start folder

    # === 2. Create MIDI Sequencer Track ===
    RPR.RPR_InsertTrackAtIndex(idx_midi, True)
    midi_trk = RPR.RPR_GetTrack(0, idx_midi)
    RPR.RPR_GetSetMediaTrackInfo_String(midi_trk, "P_NAME", f"{track_name} MIDI", True)
    RPR.RPR_SetMediaTrackInfo_Value(midi_trk, "I_FOLDERDEPTH", 0)

    # Calculate item length
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Create MIDI Item
    item = RPR.RPR_AddMediaItemToTrack(midi_trk)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to insert drum notes
    def add_drum_note(beat_pos, pitch, vel, dur_beats=0.25):
        # We loop the core 2-bar pattern across however many 'bars' the user requested
        total_beats = bars * 4
        current_beat = 0.0
        while current_beat < total_beats:
            # The base pattern is 8 beats long (2 bars)
            pattern_offset = current_beat
            start_time = (60.0 / bpm) * (pattern_offset + beat_pos)
            end_time = start_time + ((60.0 / bpm) * dur_beats)
            
            # Avoid placing notes outside the total requested bars
            if (pattern_offset + beat_pos) >= total_beats:
                break
                
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos + start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, cursor_pos + end_time)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, "")
            
            current_beat += 8.0 # Step by 2 bars

    # Groove Note Placements (relative to a 2-bar / 8-beat loop)
    # Kicks (36) - Syncopated pop/hip-hop pattern
    for b in [0.0, 1.5, 2.0, 3.5, 4.0, 5.5, 6.0, 7.5]:
        add_drum_note(b, 36, velocity_base)
        
    # Snares (38) - Backbeats
    for b in [1.0, 3.0, 5.0, 7.0]:
        add_drum_note(b, 38, velocity_base)
        
    # Claps (39) - Layered with snare, slightly lower velocity
    for b in [1.0, 3.0, 5.0, 7.0]:
        add_drum_note(b, 39, velocity_base - 10)
        
    # Closed Hats (42) - Driving 8th notes
    for b in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]:
        add_drum_note(b, 42, velocity_base - 20)
        
    # Open Hats (46) - On the 'and' of beat 4, choked by the next closed hat
    for b in [3.5, 7.5]:
        add_drum_note(b, 46, velocity_base - 5, dur_beats=0.5)

    RPR.RPR_MIDI_Sort(take)

    # === 3. Create Audio/Sampler Routing & FX Chains ===
    def setup_drum_track(idx, name, midi_src_track, is_last_in_folder=False, add_comp=False):
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        
        # Close folder if it's the last track
        if is_last_in_folder:
            RPR.RPR_SetMediaTrackInfo_Value(trk, "I_FOLDERDEPTH", -1)
            
        # Route MIDI from the sequencer track to this specific audio track
        RPR.RPR_CreateTrackSend(midi_src_track, trk)
        
        # Add a native REAPER sampler placeholder
        RPR.RPR_TrackFX_AddByName(trk, "ReaSamplOmatic5000", False, -1)
        
        # Add and configure ReaComp based on the tutorial's punchy drum settings
        if add_comp:
            comp_idx = RPR.RPR_TrackFX_AddByName(trk, "ReaComp (Cockos)", False, -1)
            RPR.RPR_TrackFX_SetParam(trk, comp_idx, 1, 4.0)   # Ratio: 4.0:1
            RPR.RPR_TrackFX_SetParam(trk, comp_idx, 2, 3.0)   # Attack: 3.0 ms
            RPR.RPR_TrackFX_SetParam(trk, comp_idx, 3, 100.0) # Release: 100 ms

        # Add ReaEQ as shown in tutorial (flat, ready for mixing)
        RPR.RPR_TrackFX_AddByName(trk, "ReaEQ (Cockos)", False, -1)
        return trk

    # Build the individual kit piece tracks
    setup_drum_track(idx_kick, "Kick", midi_trk, False, True)
    setup_drum_track(idx_snare, "Snare", midi_trk, False, True)
    setup_drum_track(idx_hats, "Hats", midi_trk, False, False)
    setup_drum_track(idx_claps, "Claps", midi_trk, True, True)

    return f"Created '{track_name}' folder bus with multi-out routing, 2-bar MIDI groove, and FX templates over {bars} bars at {bpm} BPM."
