def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Songwriting",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create the 'Reapertips Songwriting Layout' in the current REAPER project.
    Generates color-coded tracks (Drums, Bass, Guitars, Synth, Vox) and 
    inserts a basic 4/4 kick and root-note pad scaffold to start the session.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate for the scaffold.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated layout.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Music theory lookup for the starting pad
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_note = NOTE_MAP.get(key.capitalize(), 0) + 48 # Octave 3 (C3 = 48)

    # Helper to create REAPER native colors (r | g<<8 | b<<16 | 0x1000000)
    def make_color(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    # Layout configuration based on the tutorial's aesthetic
    track_configs = [
        {"suffix": "DRUMS",   "color": make_color(255, 80, 100)},  # Red/Pink
        {"suffix": "BASS",    "color": make_color(255, 200, 80)},  # Yellow
        {"suffix": "GUITARS", "color": make_color(80, 200, 120)},  # Green
        {"suffix": "SYNTH",   "color": make_color(80, 150, 255)},  # Blue
        {"suffix": "VOX",     "color": make_color(200, 100, 255)}  # Purple
    ]

    start_idx = RPR.RPR_CountTracks(0)
    created_tracks = []

    # === Step 2: Create Color-Coded Layout ===
    for i, config in enumerate(track_configs):
        idx = start_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        
        full_name = f"{track_name} - {config['suffix']}"
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", full_name, True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "I_CUSTOMCOLOR", config["color"])
        created_tracks.append(trk)

    # === Step 3: Insert Musical Scaffold (Drums & Synth) ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # 3a. Four-on-the-floor Kick on DRUMS track
    drum_trk = created_tracks[0]
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_trk)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    for b in range(bars * beats_per_bar):
        pos_sec = b * beat_length_sec
        end_sec = pos_sec + (beat_length_sec / 2)
        start_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec))
        end_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, end_sec))
        # Note 36 is standard General MIDI for Kick Drum
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 36, velocity_base, False)

    # 3b. Root note sustained pad on SYNTH track
    synth_trk = created_tracks[3]
    synth_item = RPR.RPR_AddMediaItemToTrack(synth_trk)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length_sec)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    start_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(synth_take, 0.0))
    end_ppq = int(RPR.RPR_MIDI_GetPPQPosFromProjTime(synth_take, total_length_sec))
    RPR.RPR_MIDI_InsertNote(synth_take, False, False, start_ppq, end_ppq, 0, root_note, velocity_base - 20, False)

    # Update arrange view
    RPR.RPR_UpdateTimeline()

    return f"Created 5-track Songwriting Layout starting at index {start_idx}, with {bars}-bar scaffold in {key} {scale} at {bpm} BPM."
