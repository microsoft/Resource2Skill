def create_pattern(
    project_name: str = "Mix Demo",
    track_name: str = "Low End System",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Kick and Bass track with predefined MIDI, static EQ frequency separation, 
    and sidechain routing/compression to eliminate low-end masking.
    """
    import reaper_python as RPR
    import math

    # Lookup table for MIDI notes
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key, 4)
    bass_octave = 24  # C1-B1 range
    bass_note = root_pitch + bass_octave
    kick_note = 36  # C2 for kick trigger

    # 1. Setup Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper function to convert Hz to ReaEQ slider values (Logarithmic mapping)
    def hz_to_reaeq(hz):
        # ReaEQ maps 20Hz to 24000Hz over 0.0 to 1.0 logarithmically
        return (math.log(hz) - math.log(20)) / (math.log(24000) - math.log(20))

    # Helper function to get PPQ from time
    def get_ppq(take, time):
        return RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time)

    # 2. Add Tracks
    start_idx = RPR.RPR_CountTracks(0)
    
    # Kick Track
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    kick_tr = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_tr, "P_NAME", f"{track_name} - Kick", True)
    
    # Bass Track
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    bass_tr = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_tr, "P_NAME", f"{track_name} - Bass", True)
    
    # Setup Bass Track for Sidechain (4 Channels)
    RPR.RPR_SetMediaTrackInfo_Value(bass_tr, "I_NCHAN", 4)

    # 3. Create Routing (Kick 1/2 -> Bass 3/4)
    send_idx = RPR.RPR_CreateTrackSend(kick_tr, bass_tr)
    RPR.RPR_SetTrackSendInfo_Value(kick_tr, 0, send_idx, "I_DSTCHAN", 2) # 2 = Channels 3/4
    RPR.RPR_SetTrackSendInfo_Value(kick_tr, 0, send_idx, "D_VOL", 1.0)

    # 4. Create MIDI Items
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Kick Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_tr)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", item_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # Bass Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_tr)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Generate MIDI Notes
    beat_sec = 60.0 / bpm
    for bar in range(bars):
        for beat in range(4):
            time_start = (bar * bar_length_sec) + (beat * beat_sec)
            
            # Kick Note (Quarter notes)
            k_start = get_ppq(kick_take, time_start)
            k_end = get_ppq(kick_take, time_start + (beat_sec * 0.25))
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, k_start, k_end, 0, kick_note, velocity_base, False)
            
            # Bass Notes (8th notes: Downbeat and Offbeat)
            b_start_down = get_ppq(bass_take, time_start)
            b_end_down = get_ppq(bass_take, time_start + (beat_sec * 0.45))
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, b_start_down, b_end_down, 0, bass_note, velocity_base, False)
            
            b_start_off = get_ppq(bass_take, time_start + (beat_sec * 0.5))
            b_end_off = get_ppq(bass_take, time_start + (beat_sec * 0.95))
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, b_start_off, b_end_off, 0, bass_note, velocity_base - 10, False)

    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(bass_take)

    # 5. Add Instruments & Synths
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_tr, "ReaSynth", False, -1)
    # Pitch envelope for kick punch
    RPR.RPR_TrackFX_SetParam(kick_tr, kick_synth, 4, 0.0) # Decay short
    
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_synth, 1, 0.5) # Add sawtooth for grit

    # 6. Static EQ Separation
    # Kick EQ
    kick_eq = RPR.RPR_TrackFX_AddByName(kick_tr, "ReaEQ", False, -1)
    # Band 1 (Low Shelf): Roll off ultra lows
    RPR.RPR_TrackFX_SetParam(kick_tr, kick_eq, 0, hz_to_reaeq(35.0)) # Freq
    RPR.RPR_TrackFX_SetParam(kick_tr, kick_eq, 1, 0.4) # Slight Cut (-dB)
    # Band 2 (Bell): Boost punch
    RPR.RPR_TrackFX_SetParam(kick_tr, kick_eq, 3, hz_to_reaeq(60.0)) # Freq
    RPR.RPR_TrackFX_SetParam(kick_tr, kick_eq, 4, 0.55) # Slight Boost (+dB)

    # Bass EQ
    bass_eq = RPR.RPR_TrackFX_AddByName(bass_tr, "ReaEQ", False, -1)
    # Band 1 (Low Shelf): High pass the sub rumble
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_eq, 0, hz_to_reaeq(50.0))
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_eq, 1, 0.3) # Cut (-dB)
    # Band 2 (Bell): Cut at the Kick's punch frequency (60Hz)
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_eq, 3, hz_to_reaeq(60.0))
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_eq, 4, 0.45) # Slight Cut (-dB)
    
    # 7. Sidechain Dynamic Ducking (ReaComp)
    bass_comp = RPR.RPR_TrackFX_AddByName(bass_tr, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_comp, 0, -20.0 / 60.0) # Threshold approx mapping
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_comp, 1, 0.15)  # Ratio ~ 4:1
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_comp, 2, 0.0)   # Attack 0ms
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_comp, 3, 0.05)  # Release 50ms
    
    # Crucial step: Route Auxiliary inputs (Channels 3/4) into the compressor detector
    # In ReaComp, Param 13 is Detector Input. Value ~0.2 or greater sets it to Aux L+R
    RPR.RPR_TrackFX_SetParam(bass_tr, bass_comp, 13, 0.25) 

    return f"Created Kick and Bass system with Static EQ Carving and 3/4 Sidechain Ducking over {bars} bars at {bpm} BPM."
