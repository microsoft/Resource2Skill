def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 96,
    **kwargs,
) -> str:
    """
    Create a Scale-Locked Piano Roll Generator in the current REAPER project.
    
    Creates a muted reference MIDI item containing all valid notes of the chosen scale.
    Select this item along with your active item, open the MIDI editor, and trigger
    "View: Hide unused note rows" to collapse the piano roll to strictly diatonic notes.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, whole_tone, etc.).
        bars: Number of bars for the reference item (1 is sufficient).
        velocity_base: Base MIDI velocity for reference notes.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
        "whole_tone":       [0, 2, 4, 6, 8, 10]  # Featured in the tutorial
    }

    # === Parse Inputs ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # === Step 1: Create the Guide Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Name the track explicitly so the user knows what scale it holds
    display_name = f"[{key} {scale.replace('_', ' ').title()}] Guide"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", display_name, True)

    # === Step 2: Create a Muted MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Mute the item - crucial so it doesn't output sound if synth is added
    RPR.RPR_SetMediaItemInfo_Value(item, "B_MUTE", 1.0)

    # === Step 3: Populate Diatonic Notes Across All Octaves ===
    note_count = 0
    # Quarter note duration in PPQ (Pulses Per Quarter)
    note_length_ppq = 960.0 
    
    for pitch in range(128):
        # Calculate distance from root, wrapped to a single octave (0-11)
        interval_from_root = (pitch - root_val) % 12
        
        if interval_from_root in scale_intervals:
            # Insert note: take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort
            RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, note_length_ppq, 0, pitch, velocity_base, True)
            note_count += 1

    # Apply the insertions
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{display_name}' track with {note_count} muted reference notes. Select this alongside your active MIDI item and use 'Hide unused note rows'."
