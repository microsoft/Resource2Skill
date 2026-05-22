def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano Chords (Filter Build)",
    bpm: int = 125,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an EDM Intro/Build Filter Sweep in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate for the intro build.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # --- Musical Configuration ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # We will use a standard i - VI - III - VII progression
    # In minor, these correspond to scale indices: 0, 5, 2, 6
    progression_indices = [0, 5, 2, 6]
    base_octave = 4

    # --- Step 1: Initialize Track & Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Step 2: Create MIDI Item & Chords ---
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Duration of each chord block
    chords_count = len(progression_indices)
    bars_per_chord = bars / chords_count
    ticks_per_quarter = 960
    ticks_per_bar = ticks_per_quarter * 4
    chord_duration_ticks = int(ticks_per_bar * bars_per_chord)

    def get_chord_notes(degree_idx):
        notes = []
        for interval in [0, 2, 4]: # Root, 3rd, 5th triad
            scale_idx = (degree_idx + interval) % len(scale_intervals)
            octave_offset = (degree_idx + interval) // len(scale_intervals)
            note = root_val + scale_intervals[scale_idx] + ((base_octave + octave_offset) * 12)
            # Bound the note to valid MIDI range
            notes.append(max(0, min(127, note)))
        return notes

    # Insert MIDI notes
    for i, degree in enumerate(progression_indices):
        start_tick = int(i * chord_duration_ticks)
        end_tick = int(start_tick + chord_duration_ticks)
        notes = get_chord_notes(degree)
        
        for pitch in notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 1, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # --- Step 3: Sound Design (Synth Setup) ---
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth to behave more like a pad (slower attack, longer release, saw wave)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.1)  # Attack 
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.4)  # Release
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 1.0)  # Saw shape mix

    # --- Step 4: Add Filter & Create Automation Sweep ---
    # JS: Filters/resonantlowpass is perfectly suited for EDM sweeps
    fx_filter = RPR.RPR_TrackFX_AddByName(track, "JS: Filters/resonantlowpass", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_filter, 1, 0.4) # Add slight resonance for that classic EDM peak
    
    # Get the envelope for Parameter 0 (Frequency Cutoff)
    # The 'True' flag creates the envelope if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, fx_filter, 0, True)
    
    # Add points to the envelope
    # Param goes from ~0.0 to 1.0. We sweep from muffled (0.05) to fully open (1.0)
    start_val = 0.05 
    end_val = 1.0
    
    # Point 1: Start muffled
    RPR.RPR_InsertEnvelopePoint(env, 0.0, start_val, 0, 0, False, True)
    
    # Point 2: Fully open at the very end of the item
    RPR.RPR_InsertEnvelopePoint(env, total_length_sec, end_val, 0, 0, False, True)
    
    RPR.RPR_Envelope_SortOrder(env)

    return f"Created '{track_name}': {bars}-bar chord progression with an automated low-pass filter sweep at {bpm} BPM in {key} {scale}."
