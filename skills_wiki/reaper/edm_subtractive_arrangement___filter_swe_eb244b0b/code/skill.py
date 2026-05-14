def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "EDM_Group",
    bpm: int = 125,
    key: str = "F",
    scale: str = "minor",
    bars: int = 8,  # First half is Build, second half is Drop
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Build-to-Drop arrangement featuring subtractive drums, 
    bass layering, and an automated low-pass filter sweep on the chords.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = NOTE_MAP.get(key.upper(), 5) + 48 # Octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # House progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 
    
    # Rhythm pattern for chords/bass (in quarter notes): Beat 1, Beat 2.5 (offbeat), Beat 3.5 (offbeat)
    stab_rhythm = [0.0, 1.5, 2.5]
    stab_length = 0.5

    # === Project & Timing Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    
    # Split arrangement: First half is Build, Second half is Drop
    bars_build = bars // 2
    bars_drop = bars - bars_build
    total_length = bars * bar_len

    # Helper function to create tracks
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        return tr

    # Helper function to add MIDI item
    def add_midi_item(track, start_time, length):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # === Track 1: Drums ===
    drum_track = add_track(f"{track_name}_Drums")
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1) # Placeholder for drum sampler
    drum_take = add_midi_item(drum_track, 0, total_length)

    # === Track 2: Synth Chords ===
    chord_track = add_track(f"{track_name}_Chords")
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    
    # Add ReaEQ for the Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1)
    # Band 4 Freq is parameter 9 in ReaEQ
    env = RPR.RPR_GetFXEnvelope(chord_track, eq_idx, 9, True)
    
    # Automate EQ Sweep: Muffled at start, rising to open right before drop
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.2, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, bars_build * bar_len, 0.8, 0, 0, False, True)
    # Drop stays wide open
    RPR.RPR_InsertEnvelopePoint(env, (bars_build * bar_len) + 0.01, 0.95, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    chord_take = add_midi_item(chord_track, 0, total_length)

    # === Track 3: Drop Bass ===
    bass_track = add_track(f"{track_name}_Bass")
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Bass only exists during the Drop
    bass_take = add_midi_item(bass_track, bars_build * bar_len, bars_drop * bar_len)

    # === Generate MIDI Data ===
    for b in range(bars):
        bar_start = b * bar_len
        is_drop = b >= bars_build
        
        # 1. Drum Pattern
        for beat in range(4):
            beat_pos = bar_start + (beat * beat_len)
            
            # Kick (MIDI 36) - Only in Drop! (Subtractive arrangement)
            if is_drop:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                        beat_pos, beat_pos + 0.1, 
                                        0, 36, velocity_base, False)
            
            # Clap (MIDI 39) - Beats 2 and 4 (indices 1 and 3)
            if beat % 2 != 0:
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                        beat_pos, beat_pos + 0.1, 
                                        0, 39, velocity_base, False)
            
            # Hi-Hat (MIDI 42) - Upbeats (every beat + 0.5)
            hat_pos = beat_pos + (0.5 * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    hat_pos, hat_pos + 0.1, 
                                    0, 42, int(velocity_base * 0.8), False)

        # 2. Chord & Bass Pattern
        degree = progression_degrees[b % len(progression_degrees)]
        root_note = root_midi + scale_intervals[degree]
        # Triad intervals within the scale
        chord_notes = [
            root_note,
            root_midi + scale_intervals[(degree + 2) % len(scale_intervals)] + (12 if degree + 2 >= len(scale_intervals) else 0),
            root_midi + scale_intervals[(degree + 4) % len(scale_intervals)] + (12 if degree + 4 >= len(scale_intervals) else 0)
        ]
        
        for pos in stab_rhythm:
            start_time = bar_start + (pos * beat_len)
            end_time = start_time + (stab_length * beat_len)
            
            # Insert Chords
            for note in chord_notes:
                RPR.RPR_MIDI_InsertNote(chord_take, False, False, 
                                        start_time, end_time, 
                                        0, note, velocity_base, False)
            
            # Insert Bass (Only if in the Drop section)
            if is_drop:
                bass_note = root_note - 12 # One octave lower
                bass_start_time = (b - bars_build) * bar_len + (pos * beat_len)
                bass_end_time = bass_start_time + (stab_length * beat_len)
                
                RPR.RPR_MIDI_InsertNote(bass_take, False, False, 
                                        bass_start_time, bass_end_time, 
                                        0, bass_note, velocity_base + 10, False)

    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created EDM Arrangement with Filter Sweep Build ({bars_build} bars) into Drop ({bars_drop} bars) at {bpm} BPM in {key} {scale}."
