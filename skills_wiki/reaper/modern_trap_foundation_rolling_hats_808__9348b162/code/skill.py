def create_pattern(
    project_name: str = "Trap_Beat",
    track_name: str = "Trap_Foundation",
    bpm: int = 140,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Modern Trap Foundation (Rolling Hats, Kick, Snare, and minor-scale 808 Sub).
    Includes sidechain compression prep on the 808.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the created folder track.
        bpm: Tempo in BPM (130-150 recommended).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (minor recommended for trap).
        bars: Number of bars to generate (4 is optimal for the progression).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "phrygian": [0, 2, 3, 5, 7, 8, 10],
    }

    # Validate scale and key
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key, 0)
    
    # 808 usually sits in the C1-C2 range (MIDI notes 24 to 35)
    bass_base_pitch = 24 + root_val

    # Set BPM
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def create_midi_track(name: str, folder_idx: int) -> int:
        """Helper to create a track inside a folder and return its media item take."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Set as child in folder (depth = 1)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", 0 if name != "808 Sub" else -1)
        
        # Create MIDI item
        beats_per_bar = 4
        item_length = (60.0 / bpm) * beats_per_bar * bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, take

    def insert_note(take, start_beat, length_beats, pitch, vel):
        """Helper to insert a MIDI note using beat timings."""
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Create Folder Track (Drum Bus) ===
    bus_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(bus_idx, True)
    bus_track = RPR.RPR_GetTrack(0, bus_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", f"{track_name}_Bus", True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1) # Start folder

    # === Track 1: Hi-Hats ===
    hat_track, hat_take = create_midi_track("Hi-Hats", bus_idx)
    hat_pitch = 60 # C4 standard
    for b in range(bars):
        beat_offset = b * 4
        # Standard 16th notes
        for i in range(16):
            pos = beat_offset + (i * 0.25)
            # Create a 32nd note roll on beat 4 of every 2nd bar
            if b % 2 == 1 and i >= 12:
                insert_note(hat_take, pos, 0.125, hat_pitch, velocity_base + (i%2)*10)
                insert_note(hat_take, pos + 0.125, 0.125, hat_pitch, velocity_base - 10 + (i%2)*10)
            else:
                # Slight velocity humanization
                vel = velocity_base if i % 2 == 0 else velocity_base - 15
                insert_note(hat_take, pos, 0.125, hat_pitch, vel)
    RPR.RPR_MIDI_Sort(hat_take)

    # === Track 2: Snare / Clap ===
    snare_track, snare_take = create_midi_track("Snare", bus_idx)
    snare_pitch = 60
    for b in range(bars):
        # Half time feel: hits on beat 3
        insert_note(snare_take, (b * 4) + 2.0, 0.25, snare_pitch, velocity_base + 10)
    RPR.RPR_MIDI_Sort(snare_take)

    # === Track 3: Kick ===
    kick_track, kick_take = create_midi_track("Kick", bus_idx)
    kick_pitch = 60
    # Typical syncopated trap kick rhythm
    kick_rhythm = [0.0, 1.5, 2.5, 3.0] # Beats within a bar
    for b in range(bars):
        beat_offset = b * 4
        for kr in kick_rhythm:
            insert_note(kick_take, beat_offset + kr, 0.25, kick_pitch, velocity_base + 20)
    RPR.RPR_MIDI_Sort(kick_take)

    # === Track 4: 808 Bass ===
    bass_track, bass_take = create_midi_track("808 Sub", bus_idx)
    
    # 808 Harmonic Progression: I - I - VI - VII
    progression_degrees = [0, 0, 5, 6] 
    
    for b in range(bars):
        beat_offset = b * 4
        degree_idx = progression_degrees[b % len(progression_degrees)]
        pitch = bass_base_pitch + scale_intervals[degree_idx % len(scale_intervals)]
        
        # 808 follows kick rhythm, but plays longer legato notes
        for i, kr in enumerate(kick_rhythm):
            # Calculate length to slightly overlap the next note to simulate 808 glide/portamento
            next_kr = kick_rhythm[i+1] if i+1 < len(kick_rhythm) else 4.0
            note_len = (next_kr - kr) + 0.1 # overlap by 0.1 beats
            insert_note(bass_take, beat_offset + kr, note_len, pitch, velocity_base)
    RPR.RPR_MIDI_Sort(bass_take)

    # Add ReaSynth to 808 to generate a sub frequency
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Make it sound like a sub: Square mix down, Triangle mix up
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.0) # Square mix = 0
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.8) # Triangle mix = 0.8
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 1.0) # Attack = slow down slightly to avoid clicks

    # Add ReaComp to 808 for Sidechain
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    # Param 4 in ReaComp is 'Detector Input' (Auxiliary L+R for sidechain)
    # Param 0 is Threshold, Param 1 is Ratio
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 0, -20.0) # Threshold
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 1, 4.0)   # Ratio
    
    return f"Created '{track_name}' folder with Kick, Snare, Hi-Hat rolls, and an 808 Sub Bass playing a {key} {scale} progression at {bpm} BPM."
