def create_pattern(
    project_name: str = "ArrangementTutorial",
    track_name: str = "SubtractiveBeat",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Arrangement & Filter Drop transitioning from a Verse into a Chorus.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, C#, D).
        scale: Scale type (major, minor, pentatonic_minor, etc.).
        bars: Total number of bars (split 50/50 between Verse and Chorus).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR
    
    # === Setup & Music Theory ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }
    
    root_midi = 36 + NOTE_MAP.get(key, 0) # Start in octave 3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    scale_len = len(scale_intervals)
    
    def get_midi_pitch(degree, octave=0):
        oct_shift = degree // scale_len
        note_idx = degree % scale_len
        return root_midi + ((octave + oct_shift) * 12) + scale_intervals[note_idx]

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars
    mid_point_bars = max(1, bars // 2) # Transition point

    # Helper for MIDI insertion
    def insert_note(take, start_beat, duration_beats, pitch, vel):
        start_time = start_beat * beat_len
        end_time = start_time + (duration_beats * beat_len)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Track Routing ===
    start_idx = RPR.RPR_CountTracks(0)
    
    # 1. Parent Instrument Bus
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    bus_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", f"{track_name}_InstBus", True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1)
    
    # 2. Child: Chords
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    chord_track = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(chord_track, "P_NAME", f"{track_name}_Chords", True)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    
    # 3. Child: Lead
    RPR.RPR_InsertTrackAtIndex(start_idx + 2, True)
    lead_track = RPR.RPR_GetTrack(0, start_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", f"{track_name}_Lead", True)
    RPR.RPR_SetMediaTrackInfo_Value(lead_track, "I_FOLDERDEPTH", -1) # End folder
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)

    # 4. Drums (Outside the instrument filter bus to keep impact)
    RPR.RPR_InsertTrackAtIndex(start_idx + 3, True)
    drum_track = RPR.RPR_GetTrack(0, start_idx + 3)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Drums", True)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)

    # === Add MIDI Items & Logic ===
    # Chords item
    chord_item = RPR.RPR_AddMediaItemToTrack(chord_track)
    RPR.RPR_SetMediaItemInfo_Value(chord_item, "D_LENGTH", total_len)
    chord_take = RPR.RPR_AddTakeToMediaItem(chord_item)

    # Lead item
    lead_item = RPR.RPR_AddMediaItemToTrack(lead_track)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", total_len)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)

    # Drums item
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_len)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Chord progression degrees: i, VI, iv, V (0, 5, 3, 4)
    prog_degrees = [0, 5, 3, 4]
    
    for b in range(bars):
        is_verse = (b < mid_point_bars)
        is_transition_bar = (b == mid_point_bars - 1)
        bar_start_beat = b * beats_per_bar
        deg = prog_degrees[b % 4]
        
        # 1. Chords (Plays entirely through)
        insert_note(chord_take, bar_start_beat, 4.0, get_midi_pitch(deg, 1), velocity_base - 20)
        insert_note(chord_take, bar_start_beat, 4.0, get_midi_pitch(deg + 2, 1), velocity_base - 20)
        insert_note(chord_take, bar_start_beat, 4.0, get_midi_pitch(deg + 4, 1), velocity_base - 20)
        
        # 2. Subtractive Lead (Only plays in Chorus)
        if not is_verse:
            insert_note(lead_take, bar_start_beat + 0.0, 0.5, get_midi_pitch(deg, 3), velocity_base)
            insert_note(lead_take, bar_start_beat + 1.5, 0.5, get_midi_pitch(deg + 2, 3), velocity_base)
            insert_note(lead_take, bar_start_beat + 3.0, 1.0, get_midi_pitch(deg + 4, 3), velocity_base)

        # 3. Subtractive Drums
        kick = 36
        snare = 38
        hh = 42

        # Snare (Steady backbeat)
        if not is_transition_bar or not is_verse:
            insert_note(drum_take, bar_start_beat + 1.0, 0.25, snare, velocity_base)
            insert_note(drum_take, bar_start_beat + 3.0, 0.25, snare, velocity_base)

        # Kick Subtraction Rules
        if is_verse:
            if not is_transition_bar:
                # First kick missing on beat 1! (Subtractive arrangement trick)
                insert_note(drum_take, bar_start_beat + 2.5, 0.25, kick, velocity_base)
                insert_note(drum_take, bar_start_beat + 3.5, 0.25, kick, velocity_base)
            else:
                # Transition bar: sparse kick, nothing on beat 3/4
                insert_note(drum_take, bar_start_beat + 0.0, 0.25, kick, velocity_base)
        else:
            # Full Chorus Kick
            insert_note(drum_take, bar_start_beat + 0.0, 0.25, kick, velocity_base)
            insert_note(drum_take, bar_start_beat + 1.5, 0.25, kick, velocity_base)
            insert_note(drum_take, bar_start_beat + 2.5, 0.25, kick, velocity_base)

        # Hi-hat Subtraction Rules
        if is_verse:
            # Hats enter late in the verse (Wait for beat 2)
            hat_start = 2.0 if (b == 0) else 0.0
            # Play 1/8th hats, but stop during transition
            hat_end = 2.5 if is_transition_bar else 4.0
            
            beat_step = hat_start
            while beat_step < hat_end:
                insert_note(drum_take, bar_start_beat + beat_step, 0.125, hh, velocity_base - 30)
                beat_step += 0.5
        else:
            # Full Chorus 1/16th Hats
            beat_step = 0.0
            while beat_step < 4.0:
                vel = velocity_base - 10 if (beat_step % 0.5 == 0) else velocity_base - 40
                insert_note(drum_take, bar_start_beat + beat_step, 0.125, hh, vel)
                beat_step += 0.25

    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(lead_take)
    RPR.RPR_MIDI_Sort(drum_take)

    # === ReaEQ Filter Drop Automation ===
    fx_idx = RPR.RPR_TrackFX_AddByName(bus_track, "ReaEQ", False, -1)
    
    # In ReaEQ, Band 4 (High Shelf) parameters: Param 9 = Freq, Param 10 = Gain
    # Drop gain to -24dB (0.0 parameter value) so it acts like a filter cut
    RPR.RPR_TrackFX_SetParam(bus_track, fx_idx, 10, 0.0) 
    
    # Automate Band 4 Freq (Param 9)
    env = RPR.RPR_GetFXEnvelope(bus_track, fx_idx, 9, True)
    
    transition_bar_start_time = (mid_point_bars - 1) * bar_len
    sweep_start_time = transition_bar_start_time + (2.0 * beat_len) # Start sweeping on beat 3
    drop_time = mid_point_bars * bar_len # The exact "Chorus" drop
    
    # Envelope points: (env, time, val, shape, tension, selected, noSort)
    # 1. Stay fully open (val 1.0) until sweep
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 1.0, 0, 0.0, False, True)
    # 2. Linear sweep down to low frequency (val 0.15)
    RPR.RPR_InsertEnvelopePoint(env, drop_time - 0.05, 0.15, 0, 0.0, False, True)
    # 3. Snap instantly back to 1.0 right on the drop
    RPR.RPR_InsertEnvelopePoint(env, drop_time, 1.0, 0, 0.0, False, True)
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created subtractive arrangement '{track_name}' (Verse -> Chorus) over {bars} bars at {bpm} BPM with a filter drop at bar {mid_point_bars + 1}."
