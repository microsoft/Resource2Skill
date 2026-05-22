def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arr_TwoLoop",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 32,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a full 32-bar structure using the Two-Loop Rule arrangement strategy.
    Builds an evolving track with Chords, Drums, and Bass across 4 distinct sections.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Should ideally be 32 for the full 4-section evolution.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    root_midi = 60 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # 4-bar progression using scale degrees (I, vi, IV, V mapped generically)
    chord_progression_degrees = [0, 5, 3, 4]
    
    # Helper to convert beats into REAPER MIDI ticks
    def pos(take, beat_abs):
        proj_time = beat_abs * (60.0 / bpm)
        return RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_time)

    # Helper to spawn tracks
    def create_track_item(name, total_beats_len):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item_length_sec = total_beats_len * (60.0 / bpm)
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    total_beats = bars * 4
    
    # Create the 3 functional groups
    t_chords, tk_chords = create_track_item(f"{track_name}_Chords", total_beats)
    t_drums, tk_drums = create_track_item(f"{track_name}_Drums", total_beats)
    t_bass, tk_bass = create_track_item(f"{track_name}_Bass", total_beats)
    
    # Apply Sound Design parameters to synths
    RPR.RPR_TrackFX_AddByName(t_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(t_chords, 0, 8, 0.7)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(t_chords, 0, 5, 0.5)  # Longer release for pads
    RPR.RPR_TrackFX_SetParam(t_chords, 0, 0, -6.0) # Volume
    
    RPR.RPR_TrackFX_AddByName(t_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(t_bass, 0, 7, 1.0)    # Square wave mix
    RPR.RPR_TrackFX_SetParam(t_bass, 0, 5, 0.1)    # Fast release for plucky bass
    RPR.RPR_TrackFX_SetParam(t_bass, 0, 0, -3.0)   # Volume
    
    # Standard GM Drum mapping pitches
    kick, snare, hat, crash = 36, 38, 42, 49
    
    for bar in range(bars):
        beat_start = bar * 4
        degree = chord_progression_degrees[bar % 4]
        
        # 1. GENERATE CHORDS (Plays all 32 bars, changes expression in last 8)
        notes = []
        for offset in [0, 2, 4]: # Triads
            idx = degree + offset
            octave = idx // 7
            interval = scale_intervals[idx % 7]
            notes.append(root_midi + interval + octave * 12)
            
        if bar < 24: # Section 1, 2, 3 (High energy syncopation)
            for note in notes:
                RPR.RPR_MIDI_InsertNote(tk_chords, False, False, pos(tk_chords, beat_start), pos(tk_chords, beat_start + 1.5), 1, note, velocity_base, False)
                RPR.RPR_MIDI_InsertNote(tk_chords, False, False, pos(tk_chords, beat_start + 2.5), pos(tk_chords, beat_start + 4.0), 1, note, max(1, velocity_base - 15), False)
        else: # Section 4 Breakdown (Low energy, sustained chords an octave down)
            for note in notes:
                RPR.RPR_MIDI_InsertNote(tk_chords, False, False, pos(tk_chords, beat_start), pos(tk_chords, beat_start + 4.0), 1, note - 12, max(1, velocity_base - 25), False)
                
        # 2. GENERATE BASS (Enters in Section 3, exits in Section 4)
        if 16 <= bar < 24:
            root_note = root_midi - 24 + scale_intervals[degree % 7] + (degree // 7)*12
            if bar == 23: # Truncate last bar of Section 3 to setup the breakdown transition
                for b in [0, 1.5]:
                    RPR.RPR_MIDI_InsertNote(tk_bass, False, False, pos(tk_bass, beat_start+b), pos(tk_bass, beat_start+b+0.5), 1, root_note, velocity_base, False)
            else:
                for b in [0, 1.5, 2.5, 3]: # 8th note driving groove
                    RPR.RPR_MIDI_InsertNote(tk_bass, False, False, pos(tk_bass, beat_start+b), pos(tk_bass, beat_start+b+0.5), 1, root_note, velocity_base, False)
        
        # 3. GENERATE DRUMS (Evolves per Section)
        if bar < 8: # Section 1 (Silence + Transition fill)
            if bar == 7: 
                for b in [2, 2.5, 3, 3.25, 3.5, 3.75]: # Escalating Snare Roll
                    RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+b), pos(tk_drums, beat_start+b+0.2), 1, snare, min(127, 80+int(b*10)), False)
                    
        elif bar < 16: # Section 2 (Basic Kick & Snare)
            RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start), pos(tk_drums, beat_start+0.5), 1, kick, 100, False)
            RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+2), pos(tk_drums, beat_start+2.5), 1, kick, 100, False)
            RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+1), pos(tk_drums, beat_start+1.5), 1, snare, 100, False)
            if bar == 15:
                for b in [3, 3.25, 3.5, 3.75]: # Snare roll fill
                    RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+b), pos(tk_drums, beat_start+b+0.2), 1, snare, 110, False)
            else:
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+3), pos(tk_drums, beat_start+3.5), 1, snare, 100, False)
                
        elif bar < 24: # Section 3 (Added Hats & Syncopated Kicks)
            RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start), pos(tk_drums, beat_start+0.5), 1, kick, 100, False)
            RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+1.5), pos(tk_drums, beat_start+2), 1, kick, 90, False)
            if bar == 23:
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+1), pos(tk_drums, beat_start+1.5), 1, snare, 110, False)
                # Drop kick/snare on beat 3/4 to create negative space before breakdown
            else:
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+2), pos(tk_drums, beat_start+2.5), 1, kick, 100, False)
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+1), pos(tk_drums, beat_start+1.5), 1, snare, 110, False)
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+3), pos(tk_drums, beat_start+3.5), 1, snare, 110, False)
                for i in range(8): # Hi-hats
                    RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start+i*0.5), pos(tk_drums, beat_start+i*0.5+0.25), 1, hat, 80 if i%2 else 100, False)
                    
        else: # Section 4 (Breakdown)
            if bar == 24: # Massive crash/impact at the start of the breakdown, then silence
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start), pos(tk_drums, beat_start+4), 1, crash, 110, False)
                RPR.RPR_MIDI_InsertNote(tk_drums, False, False, pos(tk_drums, beat_start), pos(tk_drums, beat_start+1), 1, kick, 110, False)

    # Apply changes to MIDI items
    RPR.RPR_MIDI_Sort(tk_chords)
    RPR.RPR_MIDI_Sort(tk_drums)
    RPR.RPR_MIDI_Sort(tk_bass)
    
    return f"Created 32-bar structure '{track_name}' using the Two-Loop Rule at {bpm} BPM in {key} {scale}"
