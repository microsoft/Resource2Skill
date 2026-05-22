def create_dynamic_beat_arrangement(
    project_name: str = "ArrangementDemo",
    bpm: int = 110,
    key: str = "D",
    scale: str = "minor",
    intro_bars: int = 8,
    chorus_bars: int = 16,
    verse_bars: int = 16,
    outro_bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a dynamic beat arrangement in REAPER with Intro, Chorus, Verse variations,
    transitions, and an outro fade, as demonstrated in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, etc.).
        intro_bars: Number of bars for the intro section.
        chorus_bars: Number of bars for each chorus section.
        verse_bars: Number of bars for each verse section.
        outro_bars: Number of bars for the outro section.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., custom drum sample paths).

    Returns:
        Status string describing what was created.
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

    root_midi = NOTE_MAP[key]
    scale_pattern = SCALES.get(scale, SCALES["minor"])

    def get_scale_notes(root, pattern, octave, offset=0):
        return [root + n + (octave * 12) + offset for n in pattern]

    def insert_midi_notes_on_take(midi_take, start_time, notes_data):
        # notes_data = [(midi_note, start_offset_beats, duration_beats, velocity)]
        for note, offset, duration, velocity in notes_data:
            RPR.MIDI_InsertNote(midi_take, False, False, start_time + offset, start_time + offset + duration, velocity, note, True)

    def add_fx_to_track(track, fx_name, preset=""):
        RPR.RPR_TrackFX_AddByName(track, fx_name, False, -1)
        if preset:
            fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
            RPR.RPR_TrackFX_SetPreset(track, fx_idx, preset)

    # === Setup Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    RPR.RPR_CSurf_OnStop() # Ensure playback is stopped before manipulating items
    RPR.RPR_Main_OnCommand(40003, 0) # Deselect all tracks

    initial_track_count = RPR.RPR_CountTracks(0)
    current_time = 0.0
    notes_inserted_count = 0

    # === Create Instrument Bus ===
    RPR.RPR_InsertTrackAtIndex(initial_track_count, True)
    inst_bus_track = RPR.RPR_GetTrack(0, initial_track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(inst_bus_track, "P_NAME", "INSTRUMENT BUS", True)
    add_fx_to_track(inst_bus_track, "ReaEQ")
    inst_bus_idx = RPR.RPR_GetMediaTrackInfo_Value(inst_bus_track, "m_index") # For automation

    # === Create Drum Bus ===
    RPR.RPR_InsertTrackAtIndex(initial_track_count + 1, True)
    drum_bus_track = RPR.RPR_GetTrack(0, initial_track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_bus_track, "P_NAME", "DRUM BUS", True)
    RPR.RPR_SetMediaTrackInfo_Value(drum_bus_track, "I_NCHAN", 2) # Stereo
    drum_bus_idx = RPR.RPR_GetMediaTrackInfo_Value(drum_bus_track, "m_index")

    # --- Instrument Tracks (routed to INSTRUMENT BUS) ---
    track_names = ["Pads", "Melody", "Bass"]
    inst_tracks = []
    for name in track_names:
        RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
        track = RPR.RPR_GetTrack(0, RPR.RPR_CountTracks(0) - 1)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", 1) # Child of Instrument Bus
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECARM", 1) # Arm for recording to add ReaSynth
        add_fx_to_track(track, "ReaSynth") # Default synth
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECARM", 0) # Disarm
        inst_tracks.append(track)
    RPR.RPR_SetMediaTrackInfo_Value(inst_bus_track, "I_FOLDERDEPTH", -1) # Parent of Instrument Tracks

    # --- Drum Tracks (routed to DRUM BUS) ---
    drum_track_names = ["Kick", "Snare", "Hi-Hat", "Open Hat", "Clap"]
    drum_midi_map = {"Kick": 60, "Snare": 62, "Hi-Hat": 64, "Open Hat": 65, "Clap": 67}
    drum_sample_paths = { # Placeholder sample paths
        "Kick": kwargs.get("kick_sample", "kick.wav"),
        "Snare": kwargs.get("snare_sample", "snare.wav"),
        "Hi-Hat": kwargs.get("hihat_sample", "hihat.wav"),
        "Open Hat": kwargs.get("openhat_sample", "openhat.wav"),
        "Clap": kwargs.get("clap_sample", "clap.wav"),
    }
    drum_tracks = {}
    for name in drum_track_names:
        RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
        track = RPR.RPR_GetTrack(0, RPR.RPR_CountTracks(0) - 1)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_FOLDERDEPTH", 1) # Child of Drum Bus
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECARM", 1) # Arm for recording to add ReaSamplOmatic
        add_fx_to_track(track, "ReaSamplOmatic5000")
        # Load sample if path provided
        fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
        if drum_sample_paths[name]:
            # This part assumes sample is in REAPER's media directory or accessible path
            # User might need to manually set the sample path for ReaSamplOmatic or provide a full path
            # RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0) # Set to sample mode
            # RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Load sample
            # This is complex and depends on user file system. Better to manually load or use ReaPack defaults.
            # For this script, we'll just add the FX.
            pass
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECARM", 0) # Disarm
        drum_tracks[name] = track
    RPR.RPR_SetMediaTrackInfo_Value(drum_bus_track, "I_FOLDERDEPTH", -1) # Parent of Drum Tracks

    # --- Riser/Transition Tracks ---
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    riser_track = RPR.RPR_GetTrack(0, RPR.RPR_CountTracks(0) - 1)
    RPR.RPR_GetSetMediaTrackInfo_String(riser_track, "P_NAME", "Riser", True)
    add_fx_to_track(riser_track, "ReaVerb")
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    cymbal_track = RPR.RPR_GetTrack(0, RPR.RPR_CountTracks(0) - 1)
    RPR.RPR_GetSetMediaTrackInfo_String(cymbal_track, "P_NAME", "Cymbal", True)
    add_fx_to_track(cymbal_track, "ReaDelay")
    add_fx_to_track(cymbal_track, "ReaVerb")

    # --- Pseudo Master Track for global filters ---
    RPR.RPR_InsertTrackAtIndex(initial_track_count, True)
    pseudo_master_track = RPR.RPR_GetTrack(0, initial_track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(pseudo_master_track, "P_NAME", "PSEUDO MASTER", True)
    # Route all other tracks to this pseudo master
    for i in range(RPR.RPR_CountTracks(0)):
        track_i = RPR.RPR_GetTrack(0, i)
        if track_i != pseudo_master_track:
            RPR.RPR_SetTrackSendInfo_Value(track_i, -1, 0, "D_VOL", 0.0) # Mute master send
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "D_VOL", 0.0) # Send to pseudo master
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "B_MAINSEND", 0) # Disable auto-send
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "B_MUTE", 0)
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "D_SNDLEVEL", 0.0) # Unity gain
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "B_MIDI", 0)
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "I_SRCCHAN", -1) # All channels
            RPR.RPR_SetTrackSendInfo_Value(track_i, pseudo_master_track, 0, "I_DSTCHAN", 0) # First pair to first pair
    add_fx_to_track(pseudo_master_track, "ReaEQ")


    # --- Define MIDI Patterns ---
    base_notes = get_scale_notes(root_midi, scale_pattern, 4)
    bass_notes = get_scale_notes(root_midi, scale_pattern, 3)

    # Simple chord progression: I-VII-III-VI (minor key)
    # D minor (D-F-A), C major (C-E-G), F major (F-A-C), G minor (G-Bb-D)
    progression_roots = [
        base_notes[0], # D
        base_notes[5]-2, # C
        base_notes[3], # F
        base_notes[4], # G
    ]

    chorus_melody_pattern = [
        (progression_roots[0] + 12, 0, 1, velocity_base),
        (progression_roots[0] + 7, 1, 1, velocity_base),
        (progression_roots[1] + 12, 2, 1, velocity_base),
        (progression_roots[1] + 7, 3, 1, velocity_base),
        (progression_roots[2] + 12, 4, 1, velocity_base),
        (progression_roots[2] + 7, 5, 1, velocity_base),
        (progression_roots[3] + 12, 6, 1, velocity_base),
        (progression_roots[3] + 7, 7, 1, velocity_base),
    ] # 8-bar melodic phrase, repeated twice for 16 bars

    chorus_pads_pattern = []
    for i in range(4):
        root = progression_roots[i]
        chord = [(root, 0.0, 4.0, velocity_base - 10),
                 (root + scale_pattern[2], 0.0, 4.0, velocity_base - 10),
                 (root + scale_pattern[4], 0.0, 4.0, velocity_base - 10)]
        for note, start_offset, dur, vel in chord:
            chorus_pads_pattern.append((note, i * 4 + start_offset, dur, vel)) # 16-bar chord progression

    chorus_bass_pattern = []
    for i in range(4):
        root = progression_roots[i] - 12
        chorus_bass_pattern.append((root, i * 4, 1, velocity_base + 5))
        chorus_bass_pattern.append((root, i * 4 + 2, 0.5, velocity_base))
        chorus_bass_pattern.append((root + 2, i * 4 + 3, 0.5, velocity_base)) # 16-bar bass progression

    # Drum patterns (simplified for demonstration)
    kick_pattern_chorus = [
        (drum_midi_map["Kick"], 0, 0.5, velocity_base),
        (drum_midi_map["Kick"], 1.5, 0.5, velocity_base),
        (drum_midi_map["Kick"], 2, 0.5, velocity_base),
        (drum_midi_map["Kick"], 3.5, 0.5, velocity_base),
    ] # 4-beat loop

    snare_pattern = [
        (drum_midi_map["Snare"], 1, 0.5, velocity_base),
        (drum_midi_map["Snare"], 3, 0.5, velocity_base),
    ] # 4-beat loop

    hihat_pattern_chorus = []
    for i in range(8):
        hihat_pattern_chorus.append((drum_midi_map["Hi-Hat"], i * 0.5, 0.25, velocity_base - 20))
    # Add some rolls
    hihat_pattern_chorus.append((drum_midi_map["Hi-Hat"], 3.75, 0.125, velocity_base + 10))
    hihat_pattern_chorus.append((drum_midi_map["Hi-Hat"], 3.875, 0.125, velocity_base + 10))
    # 4-beat loop

    # --- Generate Arrangement Sections ---

    # Intro Section
    RPR.RPR_SetEditCurPos(0, True, True)
    RPR.RPR_OnMidiEditorCommand(0, 40058) # Ensure MIDI editor is closed

    # Part 1: Pads + Melody (4 bars)
    pads_item = RPR.RPR_AddMediaItemToTrack(inst_tracks[0])
    RPR.RPR_SetMediaItemInfo_Value(pads_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(pads_item, "D_LENGTH", 4 * (60.0/bpm)*4)
    pads_take = RPR.RPR_AddTakeToMediaItem(pads_item)
    insert_midi_notes_on_take(pads_take, current_time, [(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_pads_pattern if offset < 4])
    notes_inserted_count += len([(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_pads_pattern if offset < 4])

    melody_item = RPR.RPR_AddMediaItemToTrack(inst_tracks[1])
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", 4 * (60.0/bpm)*4)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)
    insert_midi_notes_on_take(melody_take, current_time, [(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_melody_pattern if offset < 4])
    notes_inserted_count += len([(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_melody_pattern if offset < 4])

    current_time += 4 * (60.0/bpm)*4

    # Part 2: Pads + Melody + Cymbal + Riser (4 bars)
    pads_item = RPR.RPR_AddMediaItemToTrack(inst_tracks[0])
    RPR.RPR_SetMediaItemInfo_Value(pads_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(pads_item, "D_LENGTH", 4 * (60.0/bpm)*4)
    pads_take = RPR.RPR_AddTakeToMediaItem(pads_item)
    insert_midi_notes_on_take(pads_take, current_time, [(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_pads_pattern if offset < 4])
    notes_inserted_count += len([(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_pads_pattern if offset < 4])

    melody_item = RPR.RPR_AddMediaItemToTrack(inst_tracks[1])
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", current_time)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", 4 * (60.0/bpm)*4)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)
    insert_midi_notes_on_take(melody_take, current_time, [(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_melody_pattern if offset < 4])
    notes_inserted_count += len([(n, offset, dur, vel) for (n, offset, dur, vel) in chorus_melody_pattern if offset < 4])

    # Placeholder audio for cymbal and riser
    # User needs to manually add actual samples and adjust FX
    cymbal_audio = RPR.RPR_AddMediaItemToTrack(cymbal_track)
    RPR.RPR_SetMediaItemInfo_Value(cymbal_audio, "D_POSITION", current_time + 1.0 * (60.0/bpm)*4) # starts 1 bar in
    RPR.RPR_SetMediaItemInfo_Value(cymbal_audio, "D_LENGTH", 3.0 * (60.0/bpm)*4) # lasts 3 bars
    RPR.RPR_TakeFX_AddByName(RPR.RPR_GetActiveTake(cymbal_audio), "ReaDelay", False, -1)
    RPR.RPR_TakeFX_SetParam(RPR.RPR_GetActiveTake(cymbal_audio), 0, 0, 0.5) # Wet
    RPR.RPR_TakeFX_SetParam(RPR.RPR_GetActiveTake(cymbal_audio), 0, 1, 0.5) # Dry

    riser_audio = RPR.RPR_AddMediaItemToTrack(riser_track)
    RPR.RPR_SetMediaItemInfo_Value(riser_audio, "D_POSITION", current_time + 3.0 * (60.0/bpm)*4) # Starts 1 bar before chorus
    RPR.RPR_SetMediaItemInfo_Value(riser_audio, "D_LENGTH", 1.0 * (60.0/bpm)*4) # lasts 1 bar
    RPR.RPR_TakeFX_AddByName(RPR.RPR_GetActiveTake(riser_audio), "ReaVerb", False, -1)
    RPR.RPR_TakeFX_SetParam(RPR.RPR_GetActiveTake(riser_audio), 0, 0, 0.5) # Wet

    current_time += 4 * (60.0/bpm)*4

    # Chorus 1
    chorus_start_time = current_time
    for track, pattern in zip(inst_tracks, [chorus_pads_pattern, chorus_melody_pattern, chorus_bass_pattern]):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", chorus_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        for i in range(chorus_bars // 4): # Repeat 4-bar pattern
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern])
            notes_inserted_count += len(pattern)

    for drum_name, track in drum_tracks.items():
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", chorus_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        pattern_to_use = []
        if drum_name == "Kick": pattern_to_use = kick_pattern_chorus
        elif drum_name == "Snare": pattern_to_use = snare_pattern
        elif drum_name == "Hi-Hat": pattern_to_use = hihat_pattern_chorus
        elif drum_name == "Clap": pattern_to_use = snare_pattern # Use snare pattern for clap
        for i in range(chorus_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern_to_use])
            notes_inserted_count += len(pattern_to_use)
    current_time += chorus_bars * (60.0/bpm)*4

    # Verse 1
    verse1_start_time = current_time
    # Pads & Melody as in Chorus
    for track, pattern in zip(inst_tracks, [chorus_pads_pattern, chorus_melody_pattern]):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        for i in range(verse_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern])
            notes_inserted_count += len(pattern)

    # Bass (only in second half of verse)
    item = RPR.RPR_AddMediaItemToTrack(inst_tracks[2])
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time + (verse_bars // 2) * (60.0/bpm)*4)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", (verse_bars // 2) * (60.0/bpm)*4)
    take = RPR.RPR_AddTakeToMediaItem(item)
    for i in range(verse_bars // 8): # Repeat 4-bar pattern
        insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in chorus_bass_pattern])
        notes_inserted_count += len(chorus_bass_pattern)


    # Drums for Verse 1 (modified)
    for drum_name, track in drum_tracks.items():
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", verse_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        pattern_to_use = []
        if drum_name == "Kick": 
            # No kicks in first bar of each 4-bar loop
            pattern_to_use = [(n, offset, dur, vel) for (n, offset, dur, vel) in kick_pattern_chorus if offset >= 1]
        elif drum_name == "Snare": pattern_to_use = snare_pattern
        elif drum_name == "Hi-Hat": 
            # Hi-hats stretched to be half speed (8th notes instead of 16th for base pattern)
            pattern_to_use = [(n, offset*2, dur*2, vel) for (n, offset, dur, vel) in hihat_pattern_chorus if offset < 4] # Use 4-beat original, then stretch
        elif drum_name == "Clap": pattern_to_use = snare_pattern
        # Open hat not present in verse
        if drum_name == "Open Hat": RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", 0) # Effectively delete

        for i in range(verse_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern_to_use])
            notes_inserted_count += len(pattern_to_use)
    current_time += verse_bars * (60.0/bpm)*4

    # Chorus 2
    for track, pattern in zip(inst_tracks, [chorus_pads_pattern, chorus_melody_pattern, chorus_bass_pattern]):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", chorus_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        for i in range(chorus_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern])
            notes_inserted_count += len(pattern)

    for drum_name, track in drum_tracks.items():
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", chorus_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        pattern_to_use = []
        if drum_name == "Kick": pattern_to_use = kick_pattern_chorus
        elif drum_name == "Snare": pattern_to_use = snare_pattern
        elif drum_name == "Hi-Hat": pattern_to_use = hihat_pattern_chorus
        elif drum_name == "Clap": pattern_to_use = snare_pattern
        elif drum_name == "Open Hat": pattern_to_use = [(drum_midi_map["Open Hat"], 1.5, 0.5, velocity_base-20), (drum_midi_map["Open Hat"], 3.5, 0.5, velocity_base-20)]
        for i in range(chorus_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern_to_use])
            notes_inserted_count += len(pattern_to_use)
    current_time += chorus_bars * (60.0/bpm)*4

    # Outro (Fade out all samples with master filter)
    # Pads & Melody & Bass
    for track, pattern in zip(inst_tracks, [chorus_pads_pattern, chorus_melody_pattern, chorus_bass_pattern]):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", outro_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        for i in range(outro_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern])
            notes_inserted_count += len(pattern)

    # Drums
    for drum_name, track in drum_tracks.items():
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", current_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", outro_bars * (60.0/bpm)*4)
        take = RPR.RPR_AddTakeToMediaItem(item)
        pattern_to_use = []
        if drum_name == "Kick": pattern_to_use = kick_pattern_chorus
        elif drum_name == "Snare": pattern_to_use = snare_pattern
        elif drum_name == "Hi-Hat": pattern_to_use = hihat_pattern_chorus
        elif drum_name == "Clap": pattern_to_use = snare_pattern
        elif drum_name == "Open Hat": pattern_to_use = [(drum_midi_map["Open Hat"], 1.5, 0.5, velocity_base-20), (drum_midi_map["Open Hat"], 3.5, 0.5, velocity_base-20)]
        for i in range(outro_bars // 4):
            insert_midi_notes_on_take(take, current_time, [(n, offset + i*4, dur, vel) for (n, offset, dur, vel) in pattern_to_use])
            notes_inserted_count += len(pattern_to_use)
    
    # Final cymbal hit at the very end
    final_cymbal = RPR.RPR_AddMediaItemToTrack(cymbal_track)
    RPR.RPR_SetMediaItemInfo_Value(final_cymbal, "D_POSITION", current_time + (outro_bars-1) * (60.0/bpm)*4) # last bar
    RPR.RPR_SetMediaItemInfo_Value(final_cymbal, "D_LENGTH", 2.0 * (60.0/bpm)*4) # long tail


    # === Automation for Outro Master Filter ===
    # Assuming ReaEQ is the first FX on the pseudo_master_track, and band 4 is the High-Shelf/Low-Pass
    # We want to automate the frequency of band 4.
    pseudo_master_fx_idx = 0 # ReaEQ is the first FX
    re_eq_param_freq_idx = 4 # Frequency of band 4 in ReaEQ

    env = RPR.RPR_GetTrackEnvelopeByName(pseudo_master_track, "Track FX 1 - ReaEQ (Cockos) (2in/2out) - Band 4 Freq")
    if not env: # If envelope doesn't exist, create it
        RPR.RPR_SetTrackStateChunk(pseudo_master_track, "<TRACKSTATE><ENVS><ENV P_ID={4} P_FX={1} P_PARAM={4} />", False) # Correct PID and param index for freq
        env = RPR.RPR_GetTrackEnvelopeByName(pseudo_master_track, "Track FX 1 - ReaEQ (Cockos) (2in/2out) - Band 4 Freq")

    if env:
        RPR.RPR_DeleteEnvelopePointRange(env, current_time, current_time + outro_bars * (60.0/bpm)*4)
        # Start at 20kHz, sweep down to 200Hz
        RPR.RPR_InsertEnvelopePoint(env, current_time + (outro_bars - 2) * (60.0/bpm)*4, 1.0, 0, 0, True, True) # 20kHz (normalized 1.0)
        RPR.RPR_InsertEnvelopePoint(env, current_time + outro_bars * (60.0/bpm)*4, 0.0, 0, 0, True, True) # 200Hz (normalized 0.0)
        # Set shape to parabolic for smoother fade - 0.0 for square, 0.5 for default, 1.0 for parabolic (approx)
        # Point 1: Time, Value, Shape (0.0=square, 0.5=linear, 1.0=parabolic), Tension, Selected
        RPR.RPR_SetEnvelopePoint(env, 0, -1, current_time + (outro_bars - 2) * (60.0/bpm)*4, 1.0, 0.7, 0, 0, True) # Make it smooth
        RPR.RPR_SetEnvelopePoint(env, 1, -1, current_time + outro_bars * (60.0/bpm)*4, 0.0, 0.7, 0, 0, True)
        RPR.RPR_Envelope_SortPoints(env) # Sorts points by time

    current_time += outro_bars * (60.0/bpm)*4

    RPR.RPR_UpdateArrange()
    RPR.RPR_Main_OnCommand(40889, 0) # Consolidate all tracks into folders
    
    return f"Created dynamic beat arrangement with {notes_inserted_count} notes over {(intro_bars + 2*chorus_bars + verse_bars + outro_bars)*4} beats at {bpm} BPM"

