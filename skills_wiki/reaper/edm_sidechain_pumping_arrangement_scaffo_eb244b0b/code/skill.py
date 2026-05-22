def create_pattern(
    project_name: str = "EDM_Project",
    track_name: str = "EDM_Pumping",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates an EDM arrangement featuring an intro and a 'Drop' with a 4-on-the-floor kick 
    and a simulated sidechain pumping effect on the chords.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, etc.).
        scale: Scale type (major, minor).
        bars: Total number of bars (first half is Intro, second half is Drop).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # Music theory dictionaries
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # === 1. Setup Timing & Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    
    # Split arrangement
    intro_bars = max(1, bars // 2)
    drop_bars = bars - intro_bars

    # === 2. Create Tracks ===
    chords_trk_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(chords_trk_idx, True)
    chords_track = RPR.RPR_GetTrack(0, chords_trk_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name}_Chords", True)

    kick_trk_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(kick_trk_idx, True)
    kick_track = RPR.RPR_GetTrack(0, kick_trk_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", f"{track_name}_Kick", True)

    # === 3. Generate Chords MIDI ===
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", bar_len * bars)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    root_val = NOTE_MAP.get(key, 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)

    def get_chord_notes(degree):
        # Generates a triad based on the scale degree
        notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th of the chord
            idx = degree + i
            octave_shift = idx // scale_len
            note_val = root_val + scale_intervals[idx % scale_len] + (12 * octave_shift)
            notes.append(note_val)
        return notes

    # Classic EDM Progression: i - VI - III - VII (indices 0, 5, 2, 6 in minor)
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 3, 4, 5]

    for b in range(bars):
        chord_start = b * bar_len
        chord_end = chord_start + bar_len
        
        deg = progression[b % len(progression)]
        notes = get_chord_notes(deg)
        
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, chord_start)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, chord_end)
        
        for pitch in notes:
            # Shift extremely high notes down an octave for a thicker pad
            if pitch > 65:
                pitch -= 12
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, ppq_start, ppq_end, 0, int(pitch), velocity_base, False)

    # === 4. Insert Sidechain Pumping Effect (CC 11 Expression) ===
    # We apply the pump only during the drop phase
    for b in range(intro_bars, bars):
        for beat in range(beats_per_bar):
            beat_start_time = b * bar_len + beat * beat_len
            
            # Pumping timing points
            t_hit = beat_start_time                # Kick hits (volume drops)
            t_ramp = beat_start_time + (beat_len * 0.25) # 16th note (ramping up)
            t_up = beat_start_time + (beat_len * 0.5)    # 8th note offbeat (fully recovered)
            t_hold = beat_start_time + (beat_len * 0.95) # Hold before next kick
            
            ppq_hit = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_hit)
            ppq_ramp = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_ramp)
            ppq_up = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_up)
            ppq_hold = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t_hold)

            # Insert CC 11 (Expression) - msg2=11
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_hit, 0xB0, 0, 11, 20)  # Ducked heavily
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_ramp, 0xB0, 0, 11, 80) # Swoop curve
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_up, 0xB0, 0, 11, 127)  # Fully back
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_hold, 0xB0, 0, 11, 127)

    RPR.RPR_MIDI_Sort(chords_take)

    # === 5. Generate Drop Kick MIDI ===
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", intro_bars * bar_len)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", drop_bars * bar_len)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)

    for b in range(intro_bars, bars):
        for beat in range(beats_per_bar):
            kick_start = b * bar_len + beat * beat_len
            kick_end = kick_start + 0.15 # Short, punchy kick note
            
            ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, kick_start)
            ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, kick_end)
            
            # C2 (36) is standard kick drum trigger mapping
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, ppq_start, ppq_end, 0, 36, 120, False)

    RPR.RPR_MIDI_Sort(kick_take)

    # === 6. Add Instruments (ReaSynth Placeholders) ===
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)

    return f"Created EDM Arrangement '{track_name}': {intro_bars} bars Intro, {drop_bars} bars Drop with pumping rhythm at {bpm} BPM."
