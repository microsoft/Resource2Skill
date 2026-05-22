def create_pattern(
    project_name: str = "WodzuArrangement",
    track_name: str = "Verse_Builder",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Subtractive Verse Arrangement' (Drop & Build) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars (fixed to 8 for this structural pattern).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * 8

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_chord(degree, root_pitch):
        """Returns 3 notes for a triad based on diatonic scale degree (0-indexed)."""
        notes = []
        for i in [0, 2, 4]:
            idx = degree + i
            octave = idx // len(scale_intervals)
            rem = idx % len(scale_intervals)
            notes.append(root_pitch + scale_intervals[rem] + (octave * 12))
        return notes

    # === Helper: Add Track & MIDI Item ===
    def add_midi_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take
        
    def insert_note(take, start_beat, end_beat, pitch, vol):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vol), True)

    # Progression: i - VI - III - VII
    chord_progression = [0, 5, 2, 6, 0, 5, 2, 6] 

    # === Step 2: Continuous Element (Chords) ===
    track_chords, take_chords = add_midi_track(f"{track_name}_Chords")
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    
    for bar in range(8):
        degree = chord_progression[bar]
        chord_notes = get_chord(degree, root_val + 48) # C3/C4 range
        start_b = bar * 4
        # Cut short on the final turnaround bar
        end_b = start_b + 4 if bar < 7 else start_b + 3
        for pitch in chord_notes:
            insert_note(take_chords, start_b, end_b, pitch, velocity_base - 20)
    RPR.RPR_MIDI_Sort(take_chords)

    # === Step 3: Subtractive Element (Bass) ===
    track_bass, take_bass = add_midi_track(f"{track_name}_Bass")
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    
    # Bass is MUTED for bars 0-3 (The Drop). Enters at bar 4 (The Build).
    for bar in range(4, 8): 
        degree = chord_progression[bar]
        bass_note = get_chord(degree, root_val + 36)[0] # Root note, C2 range
        start_b = bar * 4
        
        if bar < 7:
            # Syncopated groove
            insert_note(take_bass, start_b, start_b + 1, bass_note, velocity_base)
            insert_note(take_bass, start_b + 1.5, start_b + 2.5, bass_note, velocity_base)
            insert_note(take_bass, start_b + 3, start_b + 3.5, bass_note, velocity_base)
        else:
            # Turnaround cut
            insert_note(take_bass, start_b, start_b + 1, bass_note, velocity_base)
            insert_note(take_bass, start_b + 1.5, start_b + 2.5, bass_note, velocity_base)
    RPR.RPR_MIDI_Sort(take_bass)

    # === Step 4: Drums (Kick/Snare) ===
    track_drums, take_drums = add_midi_track(f"{track_name}_Drums")
    KICK = 36
    SNARE = 38
    
    for bar in range(8):
        b_offset = bar * 4
        
        # Snare (Plays continuously until turnaround)
        if bar < 7:
            insert_note(take_drums, b_offset + 1, b_offset + 1.25, SNARE, velocity_base)
            insert_note(take_drums, b_offset + 3, b_offset + 3.25, SNARE, velocity_base)
        else:
            # Bar 8: Turnaround snare fill
            insert_note(take_drums, b_offset + 1, b_offset + 1.25, SNARE, velocity_base)
            insert_note(take_drums, b_offset + 3, b_offset + 3.25, SNARE, velocity_base)
            insert_note(take_drums, b_offset + 3.25, b_offset + 3.5, SNARE, velocity_base - 10)
            insert_note(take_drums, b_offset + 3.5, b_offset + 3.75, SNARE, velocity_base)
            insert_note(take_drums, b_offset + 3.75, b_offset + 4.0, SNARE, velocity_base - 10)
            
        # Kick Subtractive Logic
        if bar == 0:
            # THE DOWNBEAT DROP: Kick omitted on beat 0
            insert_note(take_drums, b_offset + 2.5, b_offset + 2.75, KICK, velocity_base)
        elif bar < 4:
            # Sparse kick pattern
            insert_note(take_drums, b_offset + 0, b_offset + 0.25, KICK, velocity_base)
            insert_note(take_drums, b_offset + 2.5, b_offset + 2.75, KICK, velocity_base)
        elif bar < 7:
            # Full energy kick pattern
            insert_note(take_drums, b_offset + 0, b_offset + 0.25, KICK, velocity_base)
            insert_note(take_drums, b_offset + 1.5, b_offset + 1.75, KICK, velocity_base)
            insert_note(take_drums, b_offset + 2.5, b_offset + 2.75, KICK, velocity_base)
            insert_note(take_drums, b_offset + 3.5, b_offset + 3.75, KICK, velocity_base - 20)
        elif bar == 7:
            # Stops early for turnaround
            insert_note(take_drums, b_offset + 0, b_offset + 0.25, KICK, velocity_base)
    RPR.RPR_MIDI_Sort(take_drums)

    # === Step 5: Hi-Hats (Energy Build) ===
    track_hats, take_hats = add_midi_track(f"{track_name}_Hats")
    HAT = 42
    
    for bar in range(8):
        b_offset = bar * 4
        if bar < 4:
            # Half-time feel (8th notes) for sparse intro verse
            for i in range(8):
                beat = b_offset + (i * 0.5)
                insert_note(take_hats, beat, beat + 0.25, HAT, velocity_base - (15 if i%2!=0 else 0))
        else:
            # Full-time feel (16th notes) to build energy
            num_notes = 16 if bar < 7 else 8 # Cut out halfway through the 8th bar
            for i in range(num_notes):
                beat = b_offset + (i * 0.25)
                insert_note(take_hats, beat, beat + 0.125, HAT, velocity_base - (20 if i%2!=0 else 0))
    RPR.RPR_MIDI_Sort(take_hats)

    RPR.RPR_UpdateArrange()

    return f"Created subtractive verse arrangement (4 tracks, 8 bars) demonstrating drop, half-time hats, and energy build at {bpm} BPM."
