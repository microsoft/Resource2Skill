def create_dynamic_beat_arrangement(
    project_name: str = "ArrangementProject",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    intro_bars: int = 8,
    chorus_bars: int = 8,
    verse_bars: int = 16,
    outro_bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a dynamic beat arrangement in REAPER with an intro, chorus, and verse structure
    optimized for vocalists, incorporating various transitions and instrumentation changes.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, etc.).
        intro_bars: Number of bars for the intro.
        chorus_bars: Number of bars for each chorus section.
        verse_bars: Number of bars for each verse section.
        outro_bars: Number of bars for the outro section.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Music theory lookup tables (simplified for demonstration)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
    }
    root_midi = NOTE_MAP.get(key, 0)
    scale_pattern = SCALES.get(scale, SCALES["minor"])

    def get_midi_note(degree, octave=4):
        # Maps scale degree to MIDI note, relative to root_midi and octave
        base_octave_midi = (octave + 1) * 12 # C0 is midi 12, C1 is 24...
        return base_octave_midi + root_midi + scale_pattern[degree % len(scale_pattern)]

    # --- Setup Project Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Create Tracks and Buses ---
    track_configs = [
        ("INSTRUMENT BUS", True, False, ""),
        ("  Pad (ReaSynth)", False, True, "ReaSynth"),
        ("  Melody (ReaSynth)", False, True, "ReaSynth"),
        ("  Bass (ReaSynth)", False, True, "ReaSynth"),
        ("DRUM BUS", True, False, ""),
        ("  Kick", False, True, "ReaSamplOmatic5000"),
        ("  Snare", False, True, "ReaSamplOmatic5000"),
        ("  Hi-Hat (Full)", False, True, "ReaSamplOmatic5000"),
        ("  Hi-Hat (Slow)", False, True, "ReaSamplOmatic5000"), # For stretched pattern
        ("  Cymbal", False, True, "ReaSamplOmatic5000"),
        ("  Riser (Sample)", False, True, ""), # Placeholder for audio sample
        ("DELAY BUS", True, False, "ReaDelay"),
        ("REVERB BUS", True, False, "ReaVerb"),
    ]

    tracks = {}
    track_idx_counter = RPR.RPR_CountTracks(0)
    for name, is_bus, is_instrument, fx_name in track_configs:
        RPR.RPR_InsertTrackAtIndex(track_idx_counter, True)
        track = RPR.RPR_GetTrack(0, track_idx_counter)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", (1 if is_bus else 0) - (1 if name.endswith("BUS") else 0)) # Set folder depth properly
        
        if is_instrument and fx_name:
            RPR.RPR_TrackFX_AddByName(track, fx_name, False, -1)
            if fx_name == "ReaSamplOmatic5000":
                # Default to a generic sound for ReaSamplOmatic5000
                RPR.RPR_TrackFX_SetPreset(track, RPR.RPR_TrackFX_GetCount(track) -1, "Kick - Big Room 1", False) # Generic Kick for example
        if name == "DELAY BUS":
            readelay_idx = RPR.RPR_TrackFX_GetCount(track) - 1
            RPR.RPR_TrackFX_SetParam(track, readelay_idx, 1, 0.5) # Wetness
            RPR.RPR_TrackFX_SetParam(track, readelay_idx, 2, 0.5) # Dryness
            RPR.RPR_TrackFX_SetParam(track, readelay_idx, 3, 0.5) # Delay Time (1/2 note)
        if name == "REVERB BUS":
            reaverb_idx = RPR.RPR_TrackFX_GetCount(track) - 1
            RPR.RPR_TrackFX_SetPreset(track, reaverb_idx, "Large Room", False)
            RPR.RPR_TrackFX_SetParam(track, reaverb_idx, 1, 0.3) # Wetness
            RPR.RPR_TrackFX_SetParam(track, reaverb_idx, 2, 0.7) # Dryness

        tracks[name] = track
        track_idx_counter += 1

    # Route instruments to buses
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Pad (ReaSynth)"], 0, -1, "I_SRCTRACK", 0.0) # To parent (INSTRUMENT BUS)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Melody (ReaSynth)"], 0, -1, "I_SRCTRACK", 0.0)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Bass (ReaSynth)"], 0, -1, "I_SRCTRACK", 0.0)

    RPR.RPR_SetTrackSendInfo_Value(tracks["  Kick"], 0, -1, "I_SRCTRACK", 0.0) # To parent (DRUM BUS)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Snare"], 0, -1, "I_SRCTRACK", 0.0)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Hi-Hat (Full)"], 0, -1, "I_SRCTRACK", 0.0)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Hi-Hat (Slow)"], 0, -1, "I_SRCTRACK", 0.0)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Cymbal"], 0, -1, "I_SRCTRACK", 0.0)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Riser (Sample)"], 0, -1, "I_SRCTRACK", 0.0)

    # Route cymbal to delay bus (send 1 on cymbal track)
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Cymbal"], RPR.RPR_SetTrackSendInfo_Value(tracks["  Cymbal"], -1, tracks["DELAY BUS"], "I_SRCMODE", 0), tracks["DELAY BUS"], "D_VOL", 0.8) # Post-fader send
    # Route riser to reverb bus
    RPR.RPR_SetTrackSendInfo_Value(tracks["  Riser (Sample)"], RPR.RPR_SetTrackSendInfo_Value(tracks["  Riser (Sample)"], -1, tracks["REVERB BUS"], "I_SRCMODE", 0), tracks["REVERB BUS"], "D_VOL", 0.7)

    # --- Musical Patterns (Simplified/Placeholder MIDI) ---
    bar_length_beats = 4
    beats_per_measure = 4
    beat_length_sec = 60.0 / bpm

    # Pad (sustained chord progression: i-VI-VII-i in minor)
    pad_pattern_notes = [
        (get_midi_note(0, 4), get_midi_note(3, 4), get_midi_note(7, 4), 0.0, bar_length_beats * beat_length_sec), # i chord
        (get_midi_note(8, 3), get_midi_note(0, 4), get_midi_note(3, 4), bar_length_beats * beat_length_sec, bar_length_beats * beat_length_sec), # VI chord
        (get_midi_note(10, 3), get_midi_note(2, 4), get_midi_note(5, 4), 2 * bar_length_beats * beat_length_sec, bar_length_beats * beat_length_sec), # VII chord
        (get_midi_note(0, 4), get_midi_note(3, 4), get_midi_note(7, 4), 3 * bar_length_beats * beat_length_sec, bar_length_beats * beat_length_sec), # i chord
    ]

    # Bass (simple root notes)
    bass_pattern_notes = [
        (get_midi_note(0, 3), 0.0, beat_length_sec),
        (get_midi_note(0, 3), beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 2 * beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 3 * beat_length_sec, beat_length_sec),
        (get_midi_note(8, 2), 4 * beat_length_sec, beat_length_sec),
        (get_midi_note(8, 2), 5 * beat_length_sec, beat_length_sec),
        (get_midi_note(8, 2), 6 * beat_length_sec, beat_length_sec),
        (get_midi_note(8, 2), 7 * beat_length_sec, beat_length_sec),
        (get_midi_note(10, 2), 8 * beat_length_sec, beat_length_sec),
        (get_midi_note(10, 2), 9 * beat_length_sec, beat_length_sec),
        (get_midi_note(10, 2), 10 * beat_length_sec, beat_length_sec),
        (get_midi_note(10, 2), 11 * beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 12 * beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 13 * beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 14 * beat_length_sec, beat_length_sec),
        (get_midi_note(0, 3), 15 * beat_length_sec, beat_length_sec),
    ]

    # Kick (4 on the floor)
    kick_pattern_notes = [
        (36, 0.0, beat_length_sec * 0.9),
        (36, 4 * beat_length_sec, beat_length_sec * 0.9),
        (36, 8 * beat_length_sec, beat_length_sec * 0.9),
        (36, 12 * beat_length_sec, beat_length_sec * 0.9),
    ]

    # Snare (2 & 4)
    snare_pattern_notes = [
        (38, 4 * beat_length_sec, beat_length_sec * 0.9),
        (38, 12 * beat_length_sec, beat_length_sec * 0.9),
    ]

    # Hi-Hat (Full - 1/8th notes)
    hihat_full_pattern_notes = []
    for i in range(16):
        hihat_full_pattern_notes.append((42, i * beat_length_sec / 2, beat_length_sec * 0.1))

    # Hi-Hat (Slow - stretched 1/4 notes)
    hihat_slow_pattern_notes = []
    for i in range(4): # 4 quarter notes per bar
        hihat_slow_pattern_notes.append((42, i * beat_length_sec, beat_length_sec * 0.1)) # Shorter duration to sound sparse

    # Cymbal (one shot at start)
    cymbal_pattern_notes = [
        (49, 0.0, beat_length_sec * 0.9), # Cymbals can be different MIDI notes for different sounds
    ]

    # --- Arrangement Logic ---
    current_time = 0.0
    total_notes_created = 0

    # Intro Section
    intro_item = RPR.RPR_AddMediaItemToTrack(tracks["  Pad (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(intro_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(intro_item, "D_LENGTH", intro_bars * bar_length_beats * beat_length_sec)
    intro_take = RPR.RPR_GetMediaItemTake(intro_item, 0)
    RPR.RPR_MIDI_SetItemExtents(intro_item, current_time, intro_bars * bar_length_beats * beat_length_sec)
    for p_notes in pad_pattern_notes:
        for note_midi in p_notes[:-2]: # All notes in chord
            RPR.RPR_MIDI_InsertNote(intro_take, False, False, current_time + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base + 10, False)
        total_notes_created += 1

    # Cymbal for intro build-up (delayed reflection)
    cymbal_intro_item = RPR.RPR_AddMediaItemToTrack(tracks["  Cymbal"])
    RPR.RPR_SetMediaItemInfo_Value(cymbal_intro_item, "D_POSITION", current_time + (intro_bars - 4) * bar_length_beats * beat_length_sec) # Last 4 bars of intro
    RPR.RPR_SetMediaItemInfo_Value(cymbal_intro_item, "D_LENGTH", 4 * bar_length_beats * beat_length_sec)
    cymbal_intro_take = RPR.RPR_GetMediaItemTake(cymbal_intro_item, 0)
    RPR.RPR_MIDI_SetItemExtents(cymbal_intro_item, current_time + (intro_bars - 4) * bar_length_beats * beat_length_sec, 4 * bar_length_beats * beat_length_sec)
    for midi_note, start_offset, duration in cymbal_pattern_notes:
        RPR.RPR_MIDI_InsertNote(cymbal_intro_take, False, False, current_time + (intro_bars - 4) * bar_length_beats * beat_length_sec + start_offset, duration, 0, midi_note, velocity_base + 20, False)
        total_notes_created += 1

    # Riser (audio sample placeholder) before chorus
    # Assuming 'Cynatics Millennium Riser Loop.wav' is available in REAPER's project folder or a known path
    # For a truly reproducible script without external files, one might synthesize a riser with ReaSynth/JSFX.
    riser_item = RPR.RPR_AddMediaItemToTrack(tracks["  Riser (Sample)"])
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_POSITION", current_time + (intro_bars - 2) * bar_length_beats * beat_length_sec) # 2 bars before chorus
    RPR.RPR_SetMediaItemInfo_Value(riser_item, "D_LENGTH", 2 * bar_length_beats * beat_length_sec)
    # RPR.RPR_GetSetMediaItemTakeInfo_String(RPR.RPR_GetMediaItemTake(riser_item,0), "P_UITEM_FILE", "Cynatics Millennium Riser Loop.wav", True) # Uncomment if sample is available
    
    current_time += intro_bars * bar_length_beats * beat_length_sec

    # Chorus 1 Section
    for track_name, notes_pattern in [
        ("  Pad (ReaSynth)", pad_pattern_notes),
        ("  Melody (ReaSynth)", [(get_midi_note(0, 5), 0.0, beat_length_sec/2), (get_midi_note(2, 5), beat_length_sec/2, beat_length_sec/2), (get_midi_note(3, 5), beat_length_sec, beat_length_sec)]), # Simple melody
        ("  Bass (ReaSynth)", bass_pattern_notes),
        ("  Kick", kick_pattern_notes),
        ("  Snare", snare_pattern_notes),
        ("  Hi-Hat (Full)", hihat_full_pattern_notes),
        ("  Cymbal", cymbal_pattern_notes),
    ]:
        if "Melody" in track_name:
             item_len = chorus_bars * bar_length_beats * beat_length_sec / 2 # Melody loop is shorter
        else:
            item_len = chorus_bars * bar_length_beats * beat_length_sec

        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
        take = RPR.RPR_GetMediaItemTake(item, 0)
        RPR.RPR_MIDI_SetItemExtents(item, current_time, item_len)

        for p_notes in notes_pattern:
            start_offset = p_notes[-2]
            duration = p_notes[-1]
            for note_midi in p_notes[:-2]:
                RPR.RPR_MIDI_InsertNote(take, False, False, current_time + start_offset, duration, 0, note_midi, velocity_base, False)
            total_notes_created += 1

    # Filter automation on INSTRUMENT BUS before Chorus 1
    inst_bus_track = tracks["INSTRUMENT BUS"]
    RPR.RPR_TrackFX_AddByName(inst_bus_track, "ReaEQ", False, -1)
    reaeq_idx = RPR.RPR_TrackFX_GetCount(inst_bus_track) - 1
    # Assuming ReaEQ band 4 (high shelf) will be used as a low-pass for demonstration
    # In a real scenario, you'd automate a dedicated low-pass filter or ReaEQ's band type.
    freq_param_idx = 4 # Index for Frequency of Band 4
    
    env_freq = RPR.RPR_GetTrackEnvelopeByName(inst_bus_track, f"FX {reaeq_idx+1} (ReaEQ) Param {freq_param_idx+1}")
    if not env_freq:
        env_freq = RPR.RPR_CreateTrackEnvelope(inst_bus_track)
        RPR.RPR_SetEnvelopeState(env_freq, f"P_NAME=FX {reaeq_idx+1} (ReaEQ) Param {freq_param_idx+1}\n")

    RPR.RPR_InsertEnvelopePoint(env_freq, current_time - (intro_bars * bar_length_beats * beat_length_sec), 20000.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(env_freq, current_time - (2 * bar_length_beats * beat_length_sec), 500.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(env_freq, current_time, 20000.0, 0, 0, False, False, False)

    current_time += chorus_bars * bar_length_beats * beat_length_sec

    # Verse 1 Section (Sparser)
    verse_1_end = current_time + verse_bars * bar_length_beats * beat_length_sec
    
    # Pad remains
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Pad (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time, verse_bars * bar_length_beats * beat_length_sec)
    for p_notes in pad_pattern_notes:
        for note_midi in p_notes[:-2]:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base - 10, False)
        total_notes_created += 1

    # Kick & Snare in all verse, but Hi-Hat only in second half
    # First half of verse 1: only Kick and Snare
    for track_name, notes_pattern in [
        ("  Kick", kick_pattern_notes),
        ("  Snare", snare_pattern_notes),
    ]:
        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * bar_length_beats * beat_length_sec)
        take = RPR.RPR_GetMediaItemTake(item, 0)
        RPR.RPR_MIDI_SetItemExtents(item, current_time, verse_bars * bar_length_beats * beat_length_sec)
        for midi_note, start_offset, duration in notes_pattern:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + start_offset, duration, 0, midi_note, velocity_base, False)
            total_notes_created += 1

    # Bass in second half of verse 1
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Bass (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", (verse_bars // 2) * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec, (verse_bars // 2) * bar_length_beats * beat_length_sec)
    for p_notes in bass_pattern_notes:
        for note_midi in p_notes[:-2]:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base, False)
        total_notes_created += 1

    # Slow hi-hats in second half of verse 1
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Hi-Hat (Slow)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", (verse_bars // 2) * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec, (verse_bars // 2) * bar_length_beats * beat_length_sec)
    for midi_note, start_offset, duration in hihat_slow_pattern_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec + start_offset, duration, 0, midi_note, velocity_base, False)
        total_notes_created += 1

    current_time = verse_1_end

    # Chorus 2 Section (Full instrumentation) - same as Chorus 1
    for track_name, notes_pattern in [
        ("  Pad (ReaSynth)", pad_pattern_notes),
        ("  Melody (ReaSynth)", [(get_midi_note(0, 5), 0.0, beat_length_sec/2), (get_midi_note(2, 5), beat_length_sec/2, beat_length_sec/2), (get_midi_note(3, 5), beat_length_sec, beat_length_sec)]),
        ("  Bass (ReaSynth)", bass_pattern_notes),
        ("  Kick", kick_pattern_notes),
        ("  Snare", snare_pattern_notes),
        ("  Hi-Hat (Full)", hihat_full_pattern_notes),
        ("  Cymbal", cymbal_pattern_notes),
    ]:
        if "Melody" in track_name:
             item_len = chorus_bars * bar_length_beats * beat_length_sec / 2 # Melody loop is shorter
        else:
            item_len = chorus_bars * bar_length_beats * beat_length_sec

        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
        take = RPR.RPR_GetMediaItemTake(item, 0)
        RPR.RPR_MIDI_SetItemExtents(item, current_time, item_len)
        for p_notes in notes_pattern:
            start_offset = p_notes[-2]
            duration = p_notes[-1]
            for note_midi in p_notes[:-2]:
                RPR.RPR_MIDI_InsertNote(take, False, False, current_time + start_offset, duration, 0, note_midi, velocity_base, False)
            total_notes_created += 1
    
    current_time += chorus_bars * bar_length_beats * beat_length_sec

    # Verse 2 Section (More intense than Verse 1)
    verse_2_end = current_time + verse_bars * bar_length_beats * beat_length_sec
    
    # Pad remains
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Pad (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time, verse_bars * bar_length_beats * beat_length_sec)
    for p_notes in pad_pattern_notes:
        for note_midi in p_notes[:-2]:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base - 10, False)
        total_notes_created += 1

    # Bass throughout verse 2
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Bass (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time, verse_bars * bar_length_beats * beat_length_sec)
    for p_notes in bass_pattern_notes:
        for note_midi in p_notes[:-2]:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base, False)
        total_notes_created += 1

    # Kick & Snare throughout verse 2
    for track_name, notes_pattern in [
        ("  Kick", kick_pattern_notes),
        ("  Snare", snare_pattern_notes),
    ]:
        item = RPR.RPR_AddMediaItemToTrack(tracks[track_name])
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * bar_length_beats * beat_length_sec)
        take = RPR.RPR_GetMediaItemTake(item, 0)
        RPR.RPR_MIDI_SetItemExtents(item, current_time, verse_bars * bar_length_beats * beat_length_sec)
        for midi_note, start_offset, duration in notes_pattern:
            RPR.RPR_MIDI_InsertNote(take, False, False, current_time + start_offset, duration, 0, midi_note, velocity_base, False)
            total_notes_created += 1

    # Full hi-hats in second half of verse 2
    item = RPR.RPR_AddMediaItemToTrack(tracks["  Hi-Hat (Full)"])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", (verse_bars // 2) * bar_length_beats * beat_length_sec)
    take = RPR.RPR_GetMediaItemTake(item, 0)
    RPR.RPR_MIDI_SetItemExtents(item, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec, (verse_bars // 2) * bar_length_beats * beat_length_sec)
    for midi_note, start_offset, duration in hihat_full_pattern_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, current_time + (verse_bars // 2) * bar_length_beats * beat_length_sec + start_offset, duration, 0, midi_note, velocity_base, False)
        total_notes_created += 1

    current_time = verse_2_end

    # Outro Section (Pad fade out with remaining instruments)
    outro_item = RPR.RPR_AddMediaItemToTrack(tracks["  Pad (ReaSynth)"])
    RPR.RPR_SetMediaItemInfo_Value(outro_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(outro_item, "D_LENGTH", outro_bars * bar_length_beats * beat_length_sec)
    outro_take = RPR.RPR_GetMediaItemTake(outro_item, 0)
    RPR.RPR_MIDI_SetItemExtents(outro_item, current_time, outro_bars * bar_length_beats * beat_length_sec)
    for p_notes in pad_pattern_notes:
        for note_midi in p_notes[:-2]:
            RPR.RPR_MIDI_InsertNote(outro_take, False, False, current_time + p_notes[-2], p_notes[-1], 0, note_midi, velocity_base - 20, False)
        total_notes_created += 1

    # Automate main master volume fade out
    master_track = RPR.RPR_GetMasterTrack(0)
    vol_env = RPR.RPR_GetTrackEnvelopeByName(master_track, "Volume")
    if not vol_env:
        vol_env = RPR.RPR_CreateTrackEnvelope(master_track)
        RPR.RPR_SetEnvelopeState(vol_env, "P_NAME=Volume\n")
    RPR.RPR_InsertEnvelopePoint(vol_env, current_time, 1.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(vol_env, current_time + outro_bars * bar_length_beats * beat_length_sec, 0.0, 0, 0, False, False, False)


    RPR.RPR_UpdateArrange()
    return f"Created '{project_name}' arrangement with approx. {total_notes_created} notes over {intro_bars + chorus_bars + verse_bars * 2 + outro_bars} bars at {bpm} BPM."

