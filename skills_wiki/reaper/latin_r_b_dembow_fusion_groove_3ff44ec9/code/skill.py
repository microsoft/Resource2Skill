def create_pattern(
    project_name: str = "Modern_Latin_RnB",
    track_name: str = "Dembow_Groove",
    bpm: int = 95,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Modern Latin R&B pattern featuring a Dembow drum groove, 
    an 808-style sub bass, and lush minor-9th pads in the current REAPER project.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }

    # Setup core pitch info
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Calculate a simple i9 - iv9 progression for the R&B pads
    # Chords defined as indices into the scale
    chord_progression_indices = [0, 0, 3, 3] # i, i, iv, iv
    
    def get_midi_note(degree_idx, oct_offset):
        octave = (degree_idx // 7) + oct_offset
        note_in_scale = scale_intervals[degree_idx % 7]
        return root_val + note_in_scale + (octave * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Helper function to create a track with MIDI item ===
    def create_midi_track(name, is_drum=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def insert_note(take, start_beat, end_beat, pitch, vel):
        start_time = start_beat * sec_per_beat
        end_time = end_beat * sec_per_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 2: Dembow Drums Track ===
    drum_track, drum_take = create_midi_track("Drums", True)
    
    for b in range(bars):
        bar_offset = b * beats_per_bar
        
        # 4-on-the-floor Kick (MIDI 36)
        for beat in [0.0, 1.0, 2.0, 3.0]:
            insert_note(drum_take, bar_offset + beat, bar_offset + beat + 0.25, 36, velocity_base)
            
        # Dembow Rimshot/Snare syncopation (MIDI 37)
        # Hits on: beat 1.75, beat 2.5, beat 3.75, beat 4.5
        for beat in [0.75, 1.5, 2.75, 3.5]:
            insert_note(drum_take, bar_offset + beat, bar_offset + beat + 0.25, 37, velocity_base)
            
        # 8th note Hi-hats (MIDI 42)
        for beat in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            vel = velocity_base - 20 if (beat * 2) % 2 != 0 else velocity_base - 10
            insert_note(drum_take, bar_offset + beat, bar_offset + beat + 0.25, 42, int(vel))

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: 808 Sub Bass Track ===
    bass_track, bass_take = create_midi_track("808_Bass")
    fx_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for 808 Sub (Pure Sine, bit of release)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 1, 0.0) # Saw down
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 2, 0.0) # Square down
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 4, 0.0) # Attack fast
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 5, 0.6) # Release moderately long

    for b in range(bars):
        bar_offset = b * beats_per_bar
        chord_root_idx = chord_progression_indices[b % len(chord_progression_indices)]
        bass_pitch = get_midi_note(chord_root_idx, 2) # Octave 2 for Sub
        
        # Bass rhythm matches the syncopated Dembow snare hits for bounce
        for start_beat, duration in [(0.0, 0.5), (0.75, 0.5), (1.5, 0.5), (2.75, 0.5), (3.5, 0.5)]:
            insert_note(bass_take, bar_offset + start_beat, bar_offset + start_beat + duration, bass_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 4: Lush R&B Pads Track ===
    pad_track, pad_take = create_midi_track("Lush_Pads")
    fx_idx_pad = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for Lush Pad (Square/Saw mix, long attack/release)
    RPR.RPR_TrackFX_SetParam(pad_track, fx_idx_pad, 1, 0.5) # Saw
    RPR.RPR_TrackFX_SetParam(pad_track, fx_idx_pad, 2, 0.5) # Square
    RPR.RPR_TrackFX_SetParam(pad_track, fx_idx_pad, 4, 0.8) # Slow Attack
    RPR.RPR_TrackFX_SetParam(pad_track, fx_idx_pad, 5, 0.8) # Slow Release
    RPR.RPR_SetMediaTrackInfo_Value(pad_track, "D_VOL", 0.5) # Turn down pad slightly

    for b in range(bars):
        bar_offset = b * beats_per_bar
        chord_root_idx = chord_progression_indices[b % len(chord_progression_indices)]
        
        # Build a minor 9th (or diatonic 9th) chord voicing [Root, 3rd, 5th, 7th, 9th]
        chord_degrees = [0, 2, 4, 6, 8] 
        
        for degree in chord_degrees:
            pad_pitch = get_midi_note(chord_root_idx + degree, 4) # Octave 4
            insert_note(pad_take, bar_offset, bar_offset + 4.0, pad_pitch, velocity_base - 30)

    RPR.RPR_MIDI_Sort(pad_take)

    # === Step 5: Update UI ===
    RPR.RPR_UpdateArrange()

    return f"Created Dembow groove with 808 Bass and Pads over {bars} bars at {bpm} BPM in {key} {scale}."
