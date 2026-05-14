def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo_Soul_Groove",
    bpm: int = 88,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul / Vintage Synth multi-track arrangement in the current REAPER project.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key, 5) # Default to F if not found
    base_pitch = 48 + root_val # 48 is C3

    # === Step 2: Track & Item Helper Functions ===
    def create_track_with_item(name, index, length_sec):
        RPR.RPR_InsertTrackAtIndex(index, True)
        track = RPR.RPR_GetTrack(0, index)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def insert_note(take, start_qn, end_qn, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # Calculate item lengths
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    num_tracks = RPR.RPR_CountTracks(0)

    # Create 5 distinct arrangement layers
    track_drums, take_drums = create_track_with_item(f"{track_name}_Drums", num_tracks, total_length_sec)
    track_pad, take_pad = create_track_with_item(f"{track_name}_SynthPad", num_tracks + 1, total_length_sec)
    track_piano, take_piano = create_track_with_item(f"{track_name}_RhythmStabs", num_tracks + 2, total_length_sec)
    track_bass, take_bass = create_track_with_item(f"{track_name}_GrittyBass", num_tracks + 3, total_length_sec)
    track_arp, take_arp = create_track_with_item(f"{track_name}_HighArp", num_tracks + 4, total_length_sec)

    # Mix levels (Linear volume, 1.0 = +0dB)
    RPR.RPR_SetMediaTrackInfo_Value(track_drums, "D_VOL", 0.8)
    RPR.RPR_SetMediaTrackInfo_Value(track_pad, "D_VOL", 0.45)
    RPR.RPR_SetMediaTrackInfo_Value(track_piano, "D_VOL", 0.5)
    RPR.RPR_SetMediaTrackInfo_Value(track_bass, "D_VOL", 0.85)
    RPR.RPR_SetMediaTrackInfo_Value(track_arp, "D_VOL", 0.35)

    # === Step 3: MIDI Generation ===
    
    # Neo-Soul / Jazz Turnaround (Intervals relative to Key Root)
    chords = [
        [0, 3, 7, 10, 14],      # i min9
        [7, 10, 14, 17, 21],    # v min9 (Root on 5th)
        [8, 12, 15, 19],        # VI maj7
        [7, 11, 14, 17]         # V dom7
    ]

    for bar in range(bars):
        bar_qn = bar * 4
        
        # --- DRUMS ---
        # Kick (36)
        insert_note(take_drums, bar_qn + 0.0, bar_qn + 0.25, 36, velocity_base)
        insert_note(take_drums, bar_qn + 1.5, bar_qn + 1.75, 36, velocity_base - 15)
        insert_note(take_drums, bar_qn + 2.5, bar_qn + 2.75, 36, velocity_base)
        if bar % 2 == 1: # Turnaround kick
            insert_note(take_drums, bar_qn + 3.75, bar_qn + 4.0, 36, velocity_base - 20)

        # Snare (38)
        insert_note(take_drums, bar_qn + 1.0, bar_qn + 1.25, 38, velocity_base + 10)
        insert_note(take_drums, bar_qn + 3.0, bar_qn + 3.25, 38, velocity_base + 10)
        # Ghost snares
        insert_note(take_drums, bar_qn + 2.75, bar_qn + 3.0, 38, velocity_base - 45)
        if bar % 2 == 0:
            insert_note(take_drums, bar_qn + 1.75, bar_qn + 2.0, 38, velocity_base - 45)

        # Hats (42)
        for i in range(8):
            hat_qn = bar_qn + (i * 0.5)
            vel = velocity_base if i % 2 == 0 else velocity_base - 25
            insert_note(take_drums, hat_qn, hat_qn + 0.25, 42, vel)
            # Syncopated 16th hats
            if i == 4 or i == 6:
                insert_note(take_drums, hat_qn + 0.25, hat_qn + 0.5, 42, vel - 30)

        # --- CHORDS, BASS & MELODY ---
        chord_idx = bar % len(chords)
        chord_notes = chords[chord_idx]
        
        # Pad - Legato Sustained
        for interval in chord_notes:
            insert_note(take_pad, bar_qn, bar_qn + 3.5, base_pitch + interval, velocity_base - 20)
            
        # Piano/Stabs - Syncopated Bounce
        stabs_qn = [0.0, 0.75, 1.5, 2.5]
        for start_offset in stabs_qn:
            for interval in chord_notes:
                insert_note(take_piano, bar_qn + start_offset, bar_qn + start_offset + 0.25, base_pitch + interval, velocity_base)
                
        # Gritty Bass - Syncopated root notes
        bass_root = (base_pitch - 24) + chord_notes[0]
        insert_note(take_bass, bar_qn + 0.0, bar_qn + 0.75, bass_root, velocity_base)
        insert_note(take_bass, bar_qn + 1.5, bar_qn + 2.0, bass_root, velocity_base)
        insert_note(take_bass, bar_qn + 2.5, bar_qn + 3.5, bass_root, velocity_base)

        # Arp - Alternating root and 5th of current chord
        arp_base = base_pitch + 24
        for i in range(8):
            arp_qn = bar_qn + (i * 0.5)
            note_offset = chord_notes[0] if i % 2 == 0 else chord_notes[2]
            insert_note(take_arp, arp_qn, arp_qn + 0.25, arp_base + note_offset, velocity_base - 15)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_pad)
    RPR.RPR_MIDI_Sort(take_piano)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_arp)

    # === Step 4: Sound Design / FX Chains ===
    
    # Drums: Saturation for vintage breakbeat grit
    RPR.RPR_TrackFX_AddByName(track_drums, "JS: Saturation", False, -1)

    # Pad: Warm analog synth (Saw/Square mix + Slow Attack/Release)
    RPR.RPR_TrackFX_AddByName(track_pad, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_pad, 0, 2, 0.15) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track_pad, 0, 5, 0.4)  # Release
    RPR.RPR_TrackFX_SetParamNormalized(track_pad, 0, 6, 0.5)  # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_pad, 0, 7, 0.5)  # Saw Mix
    RPR.RPR_TrackFX_AddByName(track_pad, "JS: Chorus", False, -1)

    # Piano/Stabs: Plucky synth (Saw wave + Fast decay, zero sustain)
    RPR.RPR_TrackFX_AddByName(track_piano, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_piano, 0, 2, 0.0) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track_piano, 0, 3, 0.1) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track_piano, 0, 4, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track_piano, 0, 7, 1.0) # Saw Mix

    # Bass: Gritty Square Wave
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, 0, 6, 0.9) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_bass, 0, 7, 0.1) # Saw Mix
    RPR.RPR_TrackFX_AddByName(track_bass, "JS: Saturation", False, -1)

    # Arp: Soft Bell/Triangle Wave
    RPR.RPR_TrackFX_AddByName(track_arp, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track_arp, 0, 6, 0.0) # Square Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_arp, 0, 7, 0.0) # Saw Mix
    RPR.RPR_TrackFX_SetParamNormalized(track_arp, 0, 8, 1.0) # Triangle Mix

    return f"Created '{track_name}' multi-track arrangement ({bars} bars) at {bpm} BPM in {key}."
