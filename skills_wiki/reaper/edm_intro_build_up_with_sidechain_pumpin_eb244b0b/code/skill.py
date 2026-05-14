def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars_per_section: int = 8,
    melody_octave: int = 4,
    chord_octave: int = 3,
    bass_octave: int = 2,
    kick_vel: int = 100,
    snare_vel: int = 90,
    hat_vel: int = 70,
    eq_sweep_start_freq: float = 200.0,  # Hz
    eq_sweep_end_freq: float = 12000.0, # Hz
    comp_thresh: float = -20.0,
    comp_ratio: float = 4.0,
    comp_attack: float = 0.01, # ms
    comp_release: float = 100.0, # ms
    **kwargs,
) -> str:
    """
    Create an EDM arrangement pattern (Intro, Chorus, Verse) in the current REAPER project,
    featuring EQ filter sweeps and sidechain pumping.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars_per_section: Number of bars for each major section (Intro, Verse, Chorus).
        melody_octave: Octave for the melody (e.g., 4 for C4).
        chord_octave: Octave for the root of chords (e.g., 3 for C3).
        bass_octave: Octave for the bassline (e.g., 2 for C2).
        kick_vel: MIDI velocity for kick drum.
        snare_vel: MIDI velocity for snare/clap.
        hat_vel: MIDI velocity for hi-hat.
        eq_sweep_start_freq: Starting frequency for the EQ low-pass sweep (Hz).
        eq_sweep_end_freq: Ending frequency for the EQ low-pass sweep (Hz).
        comp_thresh: Compressor threshold in dB.
        comp_ratio: Compressor ratio.
        comp_attack: Compressor attack in ms.
        comp_release: Compressor release in ms.
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created EDM arrangement with Intro, Verse, Chorus sections."
    """
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
    DRUM_MAP = {
        "kick": 36,  # C1
        "snare": 38, # D1 (for claps/snares)
        "hihat_closed": 42, # F#1
        "hihat_open": 46 # A#1
    }

    import reaper_python as RPR

    def get_midi_note(root_key, scale_name, degree, octave):
        root_midi = NOTE_MAP[root_key] + (octave * 12)
        scale_intervals = SCALES.get(scale_name)
        if scale_intervals and degree < len(scale_intervals):
            return root_midi + scale_intervals[degree]
        return -1 # Invalid degree or scale

    def get_chord_notes(root_key, chord_type, octave):
        root_midi = NOTE_MAP[root_key] + (octave * 12)
        if chord_type == "Cm":
            return [root_midi, root_midi + 3, root_midi + 7] # C Eb G
        elif chord_type == "Bb":
            return [root_midi, root_midi + 4, root_midi + 7] # Bb D F (relative to Bb root)
        elif chord_type == "F":
            return [root_midi, root_midi + 4, root_midi + 7] # F A C (relative to F root)
        elif chord_type == "G":
            return [root_midi, root_midi + 4, root_midi + 7] # G B D (relative to G root)
        return []

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_names = ["Piano Melody", "Piano Chords", "Bass", "Drums", "Sidechain Kick"]
    tracks = {}
    for i, name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track
        # Add ReaSynth to melodic/harmonic tracks
        if name in ["Piano Melody", "Piano Chords", "Bass"]:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Basic ReaSynth patch: Volume = 0.5, Attack = 0.01, Decay = 0.5, Sustain = 0.5, Release = 0.5 (normalized values)
            RPR.RPR_TrackFX_SetParamNormalized(track, 0, 0, 0.5) # Volume
            RPR.RPR_TrackFX_SetParamNormalized(track, 0, 1, 0.01) # Attack
            RPR.RPR_TrackFX_SetParamNormalized(track, 0, 2, 0.5) # Decay
            RPR.RPR_TrackFX_SetParamNormalized(track, 0, 3, 0.5) # Sustain
            RPR.RPR_TrackFX_SetParamNormalized(track, 0, 4, 0.5) # Release
        # Add ReaComp for sidechain to relevant tracks
        if name in ["Piano Melody", "Piano Chords", "Bass"]:
            comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, comp_thresh) # Threshold
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, comp_ratio) # Ratio
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, comp_attack) # Attack
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, comp_release) # Release
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 5, 0.5) # Detector Input: Auxiliary L+R
        
        # Add ReaEQ for Piano Chords
        if name == "Piano Chords":
            RPR.RPR_TrackFX_AddByName(track, "ReaEQ (2-Band)", False, -1) # ReaEQ plugin

    # Mute Sidechain Kick track (it's only for triggering)
    RPR.RPR_SetMediaTrackInfo_Value(tracks["Sidechain Kick"], "B_MUTE", 1.0)
    
    # === Step 3: Define Musical Patterns ===
    # Melody pattern (8 bars)
    melody_pattern = [
        (0.0, 1.0, get_midi_note(key, scale, 0, melody_octave + 1), 80), # C4
        (1.0, 1.0, get_midi_note(key, scale, 2, melody_octave + 1), 80), # Eb4
        (2.0, 1.0, get_midi_note(key, scale, 4, melody_octave + 1), 80), # G4
        (3.0, 1.0, get_midi_note(key, scale, 3, melody_octave + 1), 80), # F4
        (4.0, 1.0, get_midi_note(key, scale, 2, melody_octave + 1), 80), # Eb4
        (5.0, 1.0, get_midi_note(key, scale, 1, melody_octave + 1), 80), # D4
        (6.0, 1.0, get_midi_note(key, scale, 0, melody_octave + 1), 80), # C4
        (7.0, 1.0, get_midi_note(key, scale, 6, melody_octave), 80),   # Bb3
    ]
    melody_loop = []
    for bar_offset in range(2): # For 8 bars
        for pos, dur, note, vel in melody_pattern:
            melody_loop.append((pos + (bar_offset * 4), dur, note, vel))

    # Chord progression (8 bars)
    chord_progression_roots = [
        (key, chord_octave, "Cm"), # Bar 1
        (key, chord_octave, "Cm"), # Bar 2
        ("Bb", chord_octave - 1, "Bb"), # Bar 3 (Bb2)
        ("Bb", chord_octave - 1, "Bb"), # Bar 4
        ("F", chord_octave - 1, "F"), # Bar 5 (F2)
        ("F", chord_octave - 1, "F"), # Bar 6
        ("G", chord_octave - 1, "G"), # Bar 7 (G2)
        ("G", chord_octave - 1, "G"), # Bar 8
    ]
    chord_loop = []
    for bar_idx, (root_key, octave, chord_type) in enumerate(chord_progression_roots):
        notes = get_chord_notes(root_key, chord_type, octave)
        for note in notes:
            chord_loop.append((float(bar_idx), 1.0, note, 75)) # Each chord lasts 1 bar

    # Bassline pattern (8 bars)
    bass_pattern_roots = [
        (key, bass_octave), # Bar 1
        (key, bass_octave), # Bar 2
        ("Bb", bass_octave - 1), # Bar 3 (Bb1)
        ("Bb", bass_octave - 1), # Bar 4
        ("F", bass_octave - 1), # Bar 5 (F1)
        ("F", bass_octave - 1), # Bar 6
        ("G", bass_octave - 1), # Bar 7 (G1)
        ("G", bass_octave - 1), # Bar 8
    ]
    bass_loop = []
    for bar_idx, (root_key, octave) in enumerate(bass_pattern_roots):
        root_midi = NOTE_MAP[root_key] + (octave * 12)
        for step in range(8): # 8th notes
            bass_loop.append((float(bar_idx) + (step * 0.5), 0.5, root_midi, 90))

    # Drum pattern (4 bars, standard house kick/snare, 1/8 hats)
    drum_loop_4_bars = []
    for bar_idx in range(4):
        # Kick on every 1/4 note
        for beat in range(4):
            drum_loop_4_bars.append((float(bar_idx) + beat, 0.25, DRUM_MAP["kick"], kick_vel))
        # Snare on 2 and 4
        drum_loop_4_bars.append((float(bar_idx) + 1, 0.25, DRUM_MAP["snare"], snare_vel))
        drum_loop_4_bars.append((float(bar_idx) + 3, 0.25, DRUM_MAP["snare"], snare_vel))
        # Closed Hi-hat on every 1/8 note
        for sixteenth in range(8):
            drum_loop_4_bars.append((float(bar_idx) + (sixteenth * 0.5), 0.5, DRUM_MAP["hihat_closed"], hat_vel))

    # Sidechain Kick pattern (1/4 notes, 8 bars)
    sidechain_kick_loop = []
    for bar_idx in range(bars_per_section):
        for beat in range(4):
            sidechain_kick_loop.append((float(bar_idx) + beat, 0.25, DRUM_MAP["kick"], 127)) # Max velocity for trigger

    # === Step 4: Arrange Sections ===
    current_time = 0.0
    total_bars = 0

    # Intro (Melody + Chords with EQ sweep)
    intro_start_time = current_time
    item_melody_intro = RPR.RPR_AddMediaItemToTrack(tracks["Piano Melody"])
    item_chords_intro = RPR.RPR_AddMediaItemToTrack(tracks["Piano Chords"])
    RPR.RPR_SetMediaItemInfo_Value(item_melody_intro, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item_melody_intro, "D_LENGTH", bars_per_section * (60.0 / bpm) * 4)
    RPR.RPR_SetMediaItemInfo_Value(item_chords_intro, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item_chords_intro, "D_LENGTH", bars_per_section * (60.0 / bpm) * 4)
    take_melody_intro = RPR.RPR_AddTakeToMediaItem(item_melody_intro)
    take_chords_intro = RPR.RPR_AddTakeToMediaItem(item_chords_intro)
    midi_melody_intro = RPR.MIDI_SetItemExtents(item_melody_intro, True, True)
    midi_chords_intro = RPR.MIDI_SetItemExtents(item_chords_intro, True, True)

    for pos, dur, note, vel in melody_loop:
        RPR.MIDI_InsertNote(midi_melody_intro, False, False, pos, pos + dur, 0, note, vel, False)
    for pos, dur, note, vel in chord_loop:
        RPR.MIDI_InsertNote(midi_chords_intro, False, False, pos, pos + dur, 0, note, vel, False)
    RPR.MIDI_Sort(midi_melody_intro)
    RPR.MIDI_Sort(midi_chords_intro)
    RPR.MIDI_Commit(midi_melody_intro)
    RPR.MIDI_Commit(midi_chords_intro)

    # Apply EQ automation to Piano Chords (Intro section)
    # Param 4 is "Low-Pass Filter 1 Frequency" for ReaEQ (2-Band)
    eq_fx_idx = RPR.RPR_TrackFX_GetFXIdxByName(tracks["Piano Chords"], "ReaEQ (2-Band)", False)
    if eq_fx_idx >= 0:
        freq_env = RPR.RPR_TrackFX_GetEnvelope(tracks["Piano Chords"], eq_fx_idx, 4, True) # param 4 is Low-Pass Freq
        RPR.RPR_DeleteEnvelopePointRange(freq_env, 0, 9999999) # Clear existing points
        
        # Automation points: (time, value) - value is normalized (0-1)
        # ReaEQ frequency ranges from 20 Hz to 20000 Hz for low-pass typically.
        # We need to map eq_sweep_start_freq and eq_sweep_end_freq to 0-1 normalized values.
        # The exact mapping depends on ReaEQ's internal scaling, which is often logarithmic.
        # Let's approximate a reasonable sweep.
        
        # Assuming a linear sweep for normalized values for simplicity.
        # Start low (e.g., 200 Hz), rise over 4 bars, stay open for 4 bars.
        start_norm = RPR.RPR_TrackFX_GetParamFromNormalized(tracks["Piano Chords"], eq_fx_idx, 4, eq_sweep_start_freq, 0)
        end_norm = RPR.RPR_TrackFX_GetParamFromNormalized(tracks["Piano Chords"], eq_fx_idx, 4, eq_sweep_end_freq, 0)

        RPR.RPR_InsertEnvelopePoint(freq_env, intro_start_time, start_norm, 0, 0.0, False, True) # Start low
        RPR.RPR_InsertEnvelopePoint(freq_env, intro_start_time + (bars_per_section / 2) * (60.0 / bpm) * 4, end_norm, 0, 0.0, False, True) # Reach high at midpoint
        RPR.RPR_InsertEnvelopePoint(freq_env, intro_start_time + bars_per_section * (60.0 / bpm) * 4, end_norm, 0, 0.0, False, True) # Stay high

    current_time += bars_per_section * (60.0 / bpm) * 4
    total_bars += bars_per_section

    # --- Sidechain setup (done after all tracks are created) ---
    for track_name in ["Piano Melody", "Piano Chords", "Bass"]:
        dest_track = tracks[track_name]
        src_track = tracks["Sidechain Kick"]
        send_idx = RPR.RPR_CreateTrackSend(src_track, dest_track)
        RPR.RPR_SetTrackSendInfo_Value(src_track, send_idx, "D_VOL", 1.0) # Full volume for send
        RPR.RPR_SetTrackSendInfo_Value(src_track, send_idx, "I_SRCCHAN", 1) # Source channels (1 for mono, 1 for L, 2 for R for stereo)
        RPR.RPR_SetTrackSendInfo_Value(src_track, send_idx, "I_DSTCHAN", 3) # Destination channels (3 for ReaComp's aux input 1)
        RPR.RPR_SetTrackSendInfo_Value(src_track, send_idx, "I_SENDMODE", 2) # 2 = Pre-FX

    # Chorus 1 (Melody + Chords + Bass + Drums + Sidechain)
    for track_name, midi_data in [
        ("Piano Melody", melody_loop),
        ("Piano Chords", chord_loop),
        ("Bass", bass_loop),
        ("Drums", drum_loop_4_bars * (bars_per_section // 4)), # Duplicate drum loop to match section length
        ("Sidechain Kick", sidechain_kick_loop)
    ]:
        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars_per_section * (60.0 / bpm) * 4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        midi_item = RPR.MIDI_SetItemExtents(item, True, True)
        for pos, dur, note, vel in midi_data:
            RPR.MIDI_InsertNote(midi_item, False, False, pos, pos + dur, 0, note, vel, False)
        RPR.MIDI_Sort(midi_item)
        RPR.MIDI_Commit(midi_item)
        
    # Reset EQ automation for Piano Chords (full range in chorus)
    eq_fx_idx = RPR.RPR_TrackFX_GetFXIdxByName(tracks["Piano Chords"], "ReaEQ (2-Band)", False)
    if eq_fx_idx >= 0:
        freq_env = RPR.RPR_TrackFX_GetEnvelope(tracks["Piano Chords"], eq_fx_idx, 4, True)
        end_norm = RPR.RPR_TrackFX_GetParamFromNormalized(tracks["Piano Chords"], eq_fx_idx, 4, eq_sweep_end_freq, 0)
        RPR.RPR_InsertEnvelopePoint(freq_env, current_time, end_norm, 0, 0.0, False, True)

    current_time += bars_per_section * (60.0 / bpm) * 4
    total_bars += bars_per_section

    # Verse 1 (Chords + Bass + Drums + Sidechain - no melody)
    for track_name, midi_data in [
        ("Piano Chords", chord_loop),
        ("Bass", bass_loop),
        ("Drums", drum_loop_4_bars * (bars_per_section // 4)),
        ("Sidechain Kick", sidechain_kick_loop)
    ]:
        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars_per_section * (60.0 / bpm) * 4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        midi_item = RPR.MIDI_SetItemExtents(item, True, True)
        for pos, dur, note, vel in midi_data:
            RPR.MIDI_InsertNote(midi_item, False, False, pos, pos + dur, 0, note, vel, False)
        RPR.MIDI_Sort(midi_item)
        RPR.MIDI_Commit(midi_item)

    current_time += bars_per_section * (60.0 / bpm) * 4
    total_bars += bars_per_section

    # Chorus 2 (Melody + Chords + Bass + Drums + Sidechain)
    for track_name, midi_data in [
        ("Piano Melody", melody_loop),
        ("Piano Chords", chord_loop),
        ("Bass", bass_loop),
        ("Drums", drum_loop_4_bars * (bars_per_section // 4)),
        ("Sidechain Kick", sidechain_kick_loop)
    ]:
        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars_per_section * (60.0 / bpm) * 4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        midi_item = RPR.MIDI_SetItemExtents(item, True, True)
        for pos, dur, note, vel in midi_data:
            RPR.MIDI_InsertNote(midi_item, False, False, pos, pos + dur, 0, note, vel, False)
        RPR.MIDI_Sort(midi_item)
        RPR.MIDI_Commit(midi_item)

    current_time += bars_per_section * (60.0 / bpm) * 4
    total_bars += bars_per_section
    
    RPR.RPR_UpdateArrange() # Update REAPER display

    return f"Created EDM arrangement with {len(track_names)} tracks and {total_bars} bars at {bpm} BPM."

