def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Grid",
    bpm: int = 120,
    key: str = "C",
    scale: str = "whole_tone",
    bars: int = 1,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create Custom Scale Piano Roll Grid (Muted Template) in the current REAPER project.
    
    This generates a muted track containing every note of the requested scale across
    7 octaves. Use REAPER's "Hide unused note rows" action in the MIDI Editor to 
    collapse your piano roll to only this scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created track.
        bpm: Tempo in BPM (used to set the item length properly).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars the reference notes should span.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10] # Highlighted in tutorial
    }

    # Fallbacks for unrecognized inputs
    clean_key = key if key in NOTE_MAP else "C"
    clean_scale = scale if scale in SCALES else "major"

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track and MUTE it ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    full_track_name = f"{clean_key} {clean_scale.replace('_', ' ').title()} Template (Muted)"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Mute the track so it acts only as a visual guide, not as playable audio
    RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Populate Notes across 7 Octaves ===
    base_pitch = NOTE_MAP[clean_key]
    intervals = SCALES[clean_scale]
    
    # 960 PPQ (Pulses Per Quarter note) is standard. 4 QN per bar.
    start_ppq = 0
    end_ppq = int(960 * 4 * bars)
    
    note_count = 0
    
    # Generate notes from Octave 1 to Octave 7
    for octave in range(1, 8):
        for interval in intervals:
            pitch = (octave * 12) + base_pitch + interval
            if pitch <= 127:
                # Signature: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
                note_count += 1
                
    # Sort MIDI notes once after bulk insertion for efficiency
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateTimeline()

    return f"Created muted '{full_track_name}' track with {note_count} guide notes. Open MIDI Editor and use 'Hide unused note rows'."
