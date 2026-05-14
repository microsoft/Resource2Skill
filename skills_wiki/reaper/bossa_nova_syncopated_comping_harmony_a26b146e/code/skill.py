def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bossa Comping",
    bpm: int = 140,
    key: str = "F",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Bossa Nova Syncopated Comping pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (120-140 recommended).
        key: Root note (default F).
        scale: Scale type (harmony overrides this to play exact jazz progression).
        bars: Number of bars to generate (loops the 8-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI note (Offsetting to octave 2 for bass)
    root_val = NOTE_MAP.get(key, 5) + 36 

    # Classic "Girl from Ipanema" 8-bar progression
    progression = [
        {"root_offset": 0, "bass2_offset": 7, "chord": [11, 16, 19]}, # Bar 0: Imaj7
        {"root_offset": 0, "bass2_offset": 7, "chord": [11, 16, 19]}, # Bar 1: Imaj7
        {"root_offset": 2, "bass2_offset": 7, "chord": [10, 16, 18]}, # Bar 2: II7#11
        {"root_offset": 2, "bass2_offset": 7, "chord": [10, 16, 18]}, # Bar 3: II7#11
        {"root_offset": 2, "bass2_offset": 7, "chord": [10, 15, 19]}, # Bar 4: ii7
        {"root_offset": 1, "bass2_offset": 7, "chord": [10, 16, 19]}, # Bar 5: bII7 (Tritone Sub)
        {"root_offset": 0, "bass2_offset": 7, "chord": [11, 16, 19]}, # Bar 6: Imaj7
        {"root_offset": 0, "bass2_offset": 7, "chord": [11, 16, 19]}  # Bar 7: Imaj7
    ]

    # Rhythmic Clave (Hit Position in beats, Duration in beats, Velocity Modifier)
    chord_hits_A = [(0.0, 0.75, 0), (1.5, 0.4, -15), (2.0, 0.75, 0), (3.5, 0.4, -15)]
    chord_hits_B = [(1.5, 0.4, -15), (2.0, 1.0, 0)]

    note_count = 0
    quarter_note_len = 60.0 / bpm

    for i in range(bars):
        bar_start_sec = i * bar_length_sec
        bar_idx = i % 8
        chord_data = progression[bar_idx]
        
        r = root_val + chord_data["root_offset"]
        
        # Determine Bass Notes
        bass1 = r
        bass2 = r + chord_data["bass2_offset"]
        
        # --- Inject Bass Notes ---
        # Beat 1
        start_sec = bar_start_sec
        end_sec = bar_start_sec + (1.25 * quarter_note_len)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
            RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec), 
            RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec), 
            0, int(velocity_base + 10), bass1, False)
        note_count += 1
        
        # Beat 3
        start_sec = bar_start_sec + (2.0 * quarter_note_len)
        end_sec = bar_start_sec + (3.25 * quarter_note_len)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
            RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec), 
            RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec), 
            0, int(velocity_base), bass2, False)
        note_count += 1

        # --- Inject Chord Voicings ---
        hits = chord_hits_A if i % 2 == 0 else chord_hits_B
        for hit_pos, hit_dur, vel_mod in hits:
            start_sec = bar_start_sec + (hit_pos * quarter_note_len)
            end_sec = start_sec + (hit_dur * quarter_note_len)
            vel = max(1, min(127, int(velocity_base + vel_mod - 10)))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            for note_offset in chord_data["chord"]:
                RPR.RPR_MIDI_InsertNote(take, False, False, 
                    start_ppq, end_ppq, 0, vel, r + note_offset, False)
                note_count += 1

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design FX Chain ===
    # Add ReaSynth for a mellow nylon/rhodes tone
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.2)   # Volume down
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01)  # Fast Attack (Pluck)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.4)   # Decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)   # Zero Sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.4)   # Smooth Release
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.2)   # Square wave mix (warmth)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.8)  # Extra Sine mix (body)

    # Add ReaVerbate for intimate acoustic space
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    if verb_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.25) # Wet
        RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.75) # Dry
        RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.5)  # Roomsize

    return f"Created '{track_name}' featuring a Bossa Nova clave with {note_count} notes over {bars} bars at {bpm} BPM in {key}."
