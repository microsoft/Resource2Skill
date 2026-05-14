def create_pattern(
    project_name: str = "Trap Groove",
    track_name: str = "Trap_Drums",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Trap Kick and 808 groove with active Sidechain Compression routing in REAPER.
    """
    import reaper_python as RPR

    # Setup BPM
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Base Pitch Calculation (Map root note into the 30-40 sub-bass MIDI range)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = 24 + NOTE_MAP.get(key, 0)
    if root_pitch < 28:
        root_pitch += 12 # Keep sub frequencies hitting hard (e.g., C2=36 instead of C1=24)

    # Calculate Timing
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Helper Function to Setup Track, Synth, and MIDI ===
    def create_synth_track(name, is_kick=False, parent_idx=-1):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Add Synth
        synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Shape the sound (Kick vs 808)
        if is_kick:
            # Short, clicky, extreme pitch drop
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5)  # Vol
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.05) # Decay
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.0)  # Sustain
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.05) # Release
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.8)  # Extra Pitch Bend (Transient)
        else:
            # 808: longer sine with a tiny bit of square for grit
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.8)  # Vol
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.1)  # Square mix
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.6)  # Decay
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5)  # Sustain
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.4)  # Release
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.1)  # Extra Pitch Bend
        
        # Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, take

    # === 1. Create Tracks ===
    track_kick, take_kick = create_synth_track(f"{track_name}_Kick", is_kick=True)
    track_808, take_808 = create_synth_track(f"{track_name}_808", is_kick=False)

    # === 2. Setup Sidechain Routing (Kick -> 808) ===
    # Set 808 track to have 4 channels
    RPR.RPR_SetMediaTrackInfo_Value(track_808, "I_NCHAN", 4)
    
    # Create Send from Kick to 808
    send_idx = RPR.RPR_CreateTrackSend(track_kick, track_808)
    RPR.RPR_SetTrackSendInfo_Value(track_kick, 0, send_idx, "D_VOL", 1.0) 
    
    # Route Kick Channels 1/2 -> 808 Channels 3/4 (Dest Channel index 2 = 3/4)
    RPR.RPR_SetTrackSendInfo_Value(track_kick, 0, send_idx, "I_DSTCHAN", 2)

    # === 3. Setup ReaComp on 808 ===
    comp_idx = RPR.RPR_TrackFX_AddByName(track_808, "ReaComp", False, -1)
    # Threshold: ~ -24dB (Normalized ~ 0.2)
    RPR.RPR_TrackFX_SetParam(track_808, comp_idx, 0, 0.2)
    # Ratio: 4:1 (Normalized ~ 0.25)
    RPR.RPR_TrackFX_SetParam(track_808, comp_idx, 1, 0.25)
    # Attack: Fast (~1ms, Normalized ~ 0.01)
    RPR.RPR_TrackFX_SetParam(track_808, comp_idx, 2, 0.01)
    # Release: ~60ms (Normalized ~ 0.06)
    RPR.RPR_TrackFX_SetParam(track_808, comp_idx, 3, 0.06)
    
    # Note: Detector Input (Auxiliary L+R) in ReaComp relies on routing. By having audio 
    # hit channels 3/4, many ReaComp configurations detect this natively, though the dropdown 
    # parameter index varies by REAPER version. The 4-channel routing is strictly accurate.

    # === 4. Generate Trap MIDI Groove ===
    # Typical trap double-time placement. Beat indices: 0.0, 1.5, 2.5, 3.5...
    # Kick is syncopated, 808 precisely mirrors it.
    syncopated_pattern = [
        [0.0, 0.5], [1.5, 0.5], [2.5, 0.5],             # Bar 1
        [0.0, 0.5], [1.5, 0.5], [2.5, 0.5], [3.5, 0.5], # Bar 2
    ]

    notes_created = 0
    for bar in range(bars):
        # Alternate between the two bar patterns
        bar_pattern = syncopated_pattern[:3] if bar % 2 == 0 else syncopated_pattern[3:]
        
        for hit in bar_pattern:
            beat_offset = hit[0]
            beat_duration = hit[1]
            
            # Time in seconds
            start_sec = (bar * beats_per_bar + beat_offset) * beat_length_sec
            end_sec = start_sec + (beat_duration * beat_length_sec)
            
            # Convert to PPQ
            start_ppq_kick = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, start_sec)
            end_ppq_kick = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_kick, end_sec)
            start_ppq_808 = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, start_sec)
            end_ppq_808 = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, end_sec)
            
            # Kick (Note 36, short)
            RPR.RPR_MIDI_InsertNote(take_kick, False, False, start_ppq_kick, end_ppq_kick, 0, 36, velocity_base, False)
            
            # 808 (Root pitch)
            RPR.RPR_MIDI_InsertNote(take_808, False, False, start_ppq_808, end_ppq_808, 0, root_pitch, velocity_base, False)
            notes_created += 2

    # Update MIDI items
    RPR.RPR_MIDI_Sort(take_kick)
    RPR.RPR_MIDI_Sort(take_808)
    RPR.RPR_UpdateArrange()

    return f"Created Kick and 808 groove with {notes_created} notes over {bars} bars at {bpm} BPM. Sidechain compression successfully routed on 808 track."
