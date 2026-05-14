def create_pattern(
    project_name: str = "Arrangement_Template",
    track_name: str = "Subtractive_Arrangement",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16,  # 8 bars verse + 8 bars chorus
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 16-bar Subtractive Arrangement Template (Verse into Chorus)
    demonstrating drop-outs, half-time feel, and a riser transition.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    root = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Simple progression: i - VI - III - VII
    prog_degrees = [0, 5, 2, 6] 

    def get_chord(degree, octave):
        chord = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = (degree + i) % 7
            oct_shift = (degree + i) // 7
            note = root + scale_intervals[idx] + ((octave + oct_shift) * 12)
            chord.append(note)
        return chord

    # Setup tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar

    # Helper function to create a track with an item and take
    def create_instrument_track(name, start_bar, num_bars, use_synth=True):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        if use_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_bar * bar_len)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", num_bars * bar_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, item, take

    # --- 1. CHORDS (Plays continuously through Verse and Chorus) ---
    _, _, chords_take = create_instrument_track(f"{track_name}_Chords", 0, bars)
    for bar in range(bars):
        degree = prog_degrees[bar % 4]
        chord_notes = get_chord(degree, 4) # Octave 4
        
        start_time = bar * bar_len
        end_time = start_time + bar_len - 0.05 # slight gap
        
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, 
                                    start_time * 960 * (bpm/60.0), 
                                    end_time * 960 * (bpm/60.0), 
                                    1, note, int(velocity_base * 0.7), False)

    # --- 2. LEAD (Subtractive: ONLY plays in the Chorus, Bars 8-15) ---
    # (0-indexed: Verse is 0-7, Chorus is 8-15)
    _, _, lead_take = create_instrument_track(f"{track_name}_Lead", 8, 8)
    for bar in range(8, bars):
        degree = prog_degrees[bar % 4]
        # Play an arpeggio over the chord for the lead
        chord_notes = get_chord(degree, 5) # Octave 5
        
        for i in range(4):
            note = chord_notes[i % 3]
            start_time = (bar * bar_len) + (i * beat_len)
            end_time = start_time + (beat_len / 2)
            RPR.RPR_MIDI_InsertNote(lead_take, False, False, 
                                    (start_time - 8*bar_len) * 960 * (bpm/60.0), 
                                    (end_time - 8*bar_len) * 960 * (bpm/60.0), 
                                    1, note + 12, velocity_base, False)

    # --- 3. DRUMS (Trap/Hip-Hop groove) ---
    _, _, drum_take = create_instrument_track(f"{track_name}_Drums", 0, bars, use_synth=False)
    # Using GM Drum Map for placeholder (36=Kick, 38=Snare, 42=HiHat)
    for bar in range(bars):
        bar_start = bar * bar_len
        is_verse = bar < 8
        
        # Subtractive Kicks: Mute kick on bars 0 and 1 completely (Intro to verse drop-out)
        if not (is_verse and bar < 2):
            kick_beats = [0, 2.5] if is_verse else [0, 1.5, 2.5, 3.25]
            for kb in kick_beats:
                st = bar_start + (kb * beat_len)
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                        st * 960 * (bpm/60.0), 
                                        (st + 0.1) * 960 * (bpm/60.0), 
                                        1, 36, velocity_base, False)

        # Snare (Beats 2 and 4, or Beat 1.5 & 3.5 in normal timing) -> Trap Half-time Snare is on Beat 2.0
        for sb in [1.0, 3.0]: 
            # Drop the final snare right before the chorus
            if bar == 7 and sb == 3.0: 
                continue
            st = bar_start + (sb * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    st * 960 * (bpm/60.0), 
                                    (st + 0.1) * 960 * (bpm/60.0), 
                                    1, 38, velocity_base, False)

        # Hi-Hats: Half-time feel in Verse, Double-time feel in Chorus
        hat_step = 0.5 if is_verse else 0.25 # 8th notes vs 16th notes
        for hb in range(int(4 / hat_step)):
            st = bar_start + (hb * hat_step * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                    st * 960 * (bpm/60.0), 
                                    (st + 0.05) * 960 * (bpm/60.0), 
                                    1, 42, int(velocity_base * 0.6), False)

    # --- 4. RISER TRANSITION (Bar 7 -> Bar 8) ---
    # Single high-pitched note with a 1-bar fade-in to create a riser swell
    riser_track, riser_item, riser_take = create_instrument_track(f"{track_name}_Riser", 7, 1)
    # Pitch ReaSynth up by altering tuning params to mimic a squeal/noise
    RPR.RPR_TrackFX_SetParam(riser_track, 0, 1, 0.0) # Saw down
    RPR.RPR_TrackFX_SetParam(riser_track, 0, 2, 1.0) # Square up (buzzy)

    # Apply 1-bar item fade-in to create the "Swell" effect
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_FADEINLEN", bar_len)
    
    # High tension note (Root + 2 octaves + 7 semitones = fifth)
    riser_note = root + 84 + 7 
    RPR.RPR_MIDI_InsertNote(riser_take, False, False, 
                            0, bar_len * 960 * (bpm/60.0), 
                            1, riser_note, 127, False)

    # Sort MIDI items
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(lead_take)
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(riser_take)

    RPR.RPR_UpdateArrange()

    return f"Created 'Subtractive Arrangement' (Verse -> Chorus) over {bars} bars at {bpm} BPM with a Riser transition."
