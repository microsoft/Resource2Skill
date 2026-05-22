def create_pattern(
    project_name: str = "Neo-Soul",
    track_name: str = "Neo-Soul Backing",
    bpm: int = 90,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul Backing Track (Drums, Bass, Keys) in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (90 is ideal).
        key: Root note (C, C#, D, ..., B).
        scale: Ignored for exact progression replication, kept for signature.
        bars: Number of bars to generate (must be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_idx = NOTE_MAP.get(key.capitalize(), 0)
    
    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Helper to insert a media item with a MIDI take
    def create_midi_item(track, bars, bpm):
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # Helper to insert a MIDI note using beat timings
    def insert_note_by_beat(take, start_beat, end_beat, pitch, vel, bpm):
        beat_len = 60.0 / bpm
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # 2. Create Tracks
    total_tracks = RPR.RPR_CountTracks(0)
    
    RPR.RPR_InsertTrackAtIndex(total_tracks, True)
    track_drums = RPR.RPR_GetTrack(0, total_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{track_name} Drums (GM)", True)
    
    RPR.RPR_InsertTrackAtIndex(total_tracks + 1, True)
    track_bass = RPR.RPR_GetTrack(0, total_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name} Bass", True)
    
    RPR.RPR_InsertTrackAtIndex(total_tracks + 2, True)
    track_keys = RPR.RPR_GetTrack(0, total_tracks + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(track_keys, "P_NAME", f"{track_name} Keys", True)

    # 3. Create Items
    take_drums = create_midi_item(track_drums, bars, bpm)
    take_bass = create_midi_item(track_bass, bars, bpm)
    take_keys = create_midi_item(track_keys, bars, bpm)

    # Define drum MIDI pitches (General MIDI Standard)
    KICK = 36
    SNARE = 38
    CHH = 42
    OHH = 46

    # 4. Generate Patterns
    for bar in range(bars):
        base_beat = bar * 4
        
        # --- DRUMS ---
        # Kick: Beat 1, Beat 2.75 (16th before 3), Beat 3
        insert_note_by_beat(take_drums, base_beat + 0.0, base_beat + 0.5, KICK, velocity_base, bpm)
        insert_note_by_beat(take_drums, base_beat + 1.75, base_beat + 2.0, KICK, velocity_base - 10, bpm)
        insert_note_by_beat(take_drums, base_beat + 2.0, base_beat + 2.5, KICK, velocity_base + 5, bpm)
        
        # Snare: Beat 2, Beat 4
        insert_note_by_beat(take_drums, base_beat + 1.0, base_beat + 1.25, SNARE, velocity_base, bpm)
        insert_note_by_beat(take_drums, base_beat + 3.0, base_beat + 3.25, SNARE, velocity_base, bpm)
        
        # Hi-Hats: 8th notes
        for hh_pos in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            # Alternate velocity slightly to mimic the panning/human feel
            vel_mod = 5 if int(hh_pos * 2) % 2 == 0 else -5
            insert_note_by_beat(take_drums, base_beat + hh_pos, base_beat + hh_pos + 0.25, CHH, velocity_base - 20 + vel_mod, bpm)
        
        # Open Hi-Hat: Beat 4.5
        insert_note_by_beat(take_drums, base_beat + 3.5, base_beat + 4.0, OHH, velocity_base - 10, bpm)

        # --- BASS & KEYS ---
        # Determine the chord for this specific bar in the 4-bar loop
        chord_idx = bar % 4
        
        if chord_idx == 0:
            # Imaj7
            root_note = root_idx + 36 # C2
            chord_intervals = [0, 4, 7, 11]
            chord_root = root_idx + 48 # C3
        elif chord_idx == 1:
            # II7 (Secondary Dominant)
            root_note = root_idx + 38 # D2
            chord_intervals = [2, 6, 9, 12]
            chord_root = root_idx + 48 
        elif chord_idx == 2:
            # iii7
            root_note = root_idx + 40 # E2
            chord_intervals = [4, 7, 11, 14]
            chord_root = root_idx + 48
        else:
            # V7 with 7th in the bass (Voice Leading down to I)
            root_note = root_idx + 31 # G1
            chord_intervals = [5, 7, 11, 14] # F is 5, G is 7...
            chord_root = root_idx + 48
            
        # Bass follows the exact Kick rhythm
        insert_note_by_beat(take_bass, base_beat + 0.0, base_beat + 1.5, root_note, velocity_base, bpm)
        insert_note_by_beat(take_bass, base_beat + 1.75, base_beat + 2.0, root_note, velocity_base - 10, bpm)
        insert_note_by_beat(take_bass, base_beat + 2.0, base_beat + 3.5, root_note, velocity_base, bpm)
        
        # Keys play the full chord (Strummed feel by letting it ring)
        for interval in chord_intervals:
            insert_note_by_beat(take_keys, base_beat + 0.0, base_beat + 3.5, chord_root + interval, velocity_base - 15, bpm)

    # Sort MIDI items so REAPER processes them cleanly
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_keys)

    # 5. Add Sound Design (FX Chains)
    
    # Bass FX: ReaSynth (Sine/Triangle mix)
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(track_bass, "D_VOL", 0.8)
    
    # Keys FX: ReaSynth -> ReaVerbate (Pad sound)
    RPR.RPR_TrackFX_AddByName(track_keys, "ReaSynth", False, -1)
    # Tame the highs of ReaSynth by default by making it softer, and add Reverb
    RPR.RPR_TrackFX_AddByName(track_keys, "ReaVerbate", False, -1)
    RPR.RPR_SetMediaTrackInfo_Value(track_keys, "D_VOL", 0.4) # Keys sit lower in the mix
    
    return f"Created Neo-Soul groove across 3 tracks (Drums, Bass, Keys) with {bars} bars at {bpm} BPM in {key} Major."
