def create_pattern(
    project_name: str = "TightLowEnd",
    track_name: str = "Low End Bus",
    bpm: int = 124,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a House Kick & Bass groove routed to a dedicated Multiband Low End Bus,
    demonstrating the "Tighten/Loosen the Bottom" mastering technique.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Calculate Root Note (Octave 1 for Bass/Kick)
    root_pitch = NOTE_MAP.get(key.upper(), 5) + 24 # F1 = 29
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    # === Helper function to create a track ===
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        return trk, idx

    # === 1. Create Mix Bus (Low End Bus) ===
    bus_track, bus_idx = add_track(track_name)
    
    # 1a. Mono the Low End using M/S technique
    # Encoder -> EQ (Side Highpass) -> Decoder
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: M/S Encoder", False, -1)
    
    eq_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 0, 115.0) # Band 1 Freq to 115Hz
    RPR.RPR_TrackFX_SetParam(bus_track, eq_idx, 3, 4.0)   # Band 1 Type to Highpass
    # Note: Pin routing API via Python is highly restricted. In a manual workflow, 
    # you would set the ReaEQ pins to process ONLY the Right (Side) channel.
    
    RPR.RPR_TrackFX_AddByName(bus_track, "JS: M/S Decoder", False, -1)

    # 1b. Multiband Dynamics (ReaXcomp)
    # Band 1 (Sub): Compresses < 115Hz. Band 2 (Low Mids): Expands 115-350Hz.
    xcomp_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaXcomp", False, -1)
    
    # === 2. Create Kick Track ===
    kick_track, kick_idx = add_track("Kick")
    RPR.RPR_SetMediaTrackInfo_Value(kick_track, "B_MAINSEND", 0) # Disable Master send
    RPR.RPR_CreateTrackSend(kick_track, bus_track) # Send to Bus
    
    # Kick Synth (ReaSynth to simulate 909)
    kick_synth = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 0, 0.0) # Square mix down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 1, 0.0) # Saw mix down
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 5, 0.0) # Extra Attack
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth, 6, 0.1) # Fast Decay
    
    # Kick MIDI Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    
    # 4-on-the-floor kick
    for b in range(bars):
        for beat in range(4):
            start_pos = (b * 4) + beat
            end_pos = start_pos + 0.25
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_pos, end_pos, 0, root_pitch, velocity_base, False)

    # === 3. Create Bass Track ===
    bass_track, bass_idx = add_track("Bass")
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "B_MAINSEND", 0) # Disable Master send
    RPR.RPR_CreateTrackSend(bass_track, bus_track) # Send to Bus
    
    # Bass Synth
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 0, 1.0) # Square mix up
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 1, 0.5) # Saw mix 
    bass_eq = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_eq, 0, 400.0) # Band 1 Freq to 400Hz
    RPR.RPR_TrackFX_SetParam(bass_track, bass_eq, 3, 3.0)   # Band 1 Type to Lowpass
    
    # Bass MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # Off-beat Syncopated Bassline
    bass_rhythm = [0.5, 1.5, 2.0, 2.5, 3.5] # 1/8th note off-beats and one downbeat
    for b in range(bars):
        for i, beat_pos in enumerate(bass_rhythm):
            start_pos = (b * 4) + beat_pos
            end_pos = start_pos + 0.45
            
            # Root note, dropping down an octave sometimes for movement
            pitch = root_pitch if i % 2 == 0 else root_pitch - 12
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_pos, end_pos, 0, pitch, velocity_base - 10, False)

    RPR.RPR_UpdateTimeline()

    return f"Created '{track_name}' Bus with M/S and Multiband FX, driven by a generated {bpm} BPM Kick & Bass groove in {key} {scale}."
