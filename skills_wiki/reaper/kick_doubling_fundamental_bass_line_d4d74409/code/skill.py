def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Often bass just uses root, but keep for generality
    bars: int = 4,
    velocity_base: int = 110, # Adjusted down from 127 as shown in tutorial
    base_octave: int = 2, # Common bass octave, C2 = MIDI 36, C3 = MIDI 48
    note_duration_factor: float = 0.9, # 0.9 for slightly staccato, 1.0 for full length
    kick_pattern_beats: list = None, # List of beat positions within a bar for bass notes
    octave_variation_beats: list = None, # List of beat positions to raise an octave
    **kwargs,
) -> str:
    """
    Create a Kick-Doubling Fundamental Bass Line in the current REAPER project.
    The bass line plays root notes (or notes based on the scale) at specified beat positions,
    mimicking a kick drum pattern.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        base_octave: MIDI octave for the base notes (e.g., 2 for C2, 3 for C3).
        note_duration_factor: Controls note length (0.0-1.0). 1.0 = full beat, 0.5 = half beat.
        kick_pattern_beats: List of beat positions (e.g., [0.0, 1.0, 2.0, 3.0]) within a 4/4 bar
                            where bass notes will be placed. Defaults to a common kick pattern.
        octave_variation_beats: List of beat positions (e.g., [3.0]) within a 4/4 bar
                                where the bass note will be played one octave higher.
        **kwargs: Additional overrides (not used in this skill but for future compatibility).

    Returns:
        Status string, e.g., "Created 'Bass' with N notes over 4 bars at 120 BPM"
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolodian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    def get_midi_note(key_root: str, octave: int, scale_degree: int = 0, scale_type: str = "major") -> int:
        """Calculates the MIDI note number for a given key, octave, and scale degree."""
        root_midi = NOTE_MAP.get(key_root, 0)
        scale_intervals = SCALES.get(scale_type, SCALES["major"])
        
        if not scale_intervals:
            return root_midi + (octave * 12) # Fallback if scale is not found
        
        degree_in_octave = scale_intervals[scale_degree % len(scale_intervals)]
        octave_shift = (scale_degree // len(scale_intervals)) * 12
        
        # C-1 is MIDI 0, C0 is MIDI 12, C1 is MIDI 24, C2 is MIDI 36, C3 is MIDI 48
        return root_midi + degree_in_octave + (octave * 12) + octave_shift

    # Initialize REAPER
    RPR.RPR_PreventUIRefresh(1)
    RPR.RPR_Undo_BeginBlock()

    # Set Tempo (already handled by the agent, but good for internal consistency)
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Load ReaSynth for a basic bass sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    if fx_idx != -1:
        # ReaSynth parameters for a simple deep bass (waveform, filter cutoff, resonance)
        # These are rough approximations; actual sound design requires more specific VST.
        # Param IDs can vary, generally 0=Waveform, 4=Cutoff, 5=Resonance
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)  # Waveform to sine (0.0-0.3 for sine-like)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Filter Cutoff (0.0-1.0)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.1)  # Filter Resonance (0.0-1.0)

    # Create MIDI Item
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    item_length_seconds = seconds_per_beat * beats_per_bar * bars
    
    # Start the MIDI item at the current play cursor position
    item_position_seconds = RPR.RPR_GetPlayPosition()

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position_seconds)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take: # Ensure there's an active take for MIDI
        take = RPR.RPR_AddTakeToMediaItem(item)
        
    midi_take = RPR.RPR_MIDI_AllocTemporary(take, True)

    # Default kick pattern if not provided (simple, strong beats)
    if kick_pattern_beats is None:
        kick_pattern_beats = [0.0, 2.0] # Kicks on beat 1 and beat 3 (quarter notes)

    if octave_variation_beats is None:
        octave_variation_beats = [] # No octave variations by default

    total_notes_added = 0
    root_midi_note = get_midi_note(key, base_octave, 0, scale)

    # Insert MIDI notes
    for bar in range(bars):
        for beat_offset in kick_pattern_beats:
            position_beats = (bar * beats_per_bar) + beat_offset
            
            # Note duration in beats (quarter note length, adjusted by factor)
            note_length_beats = 1.0 * note_duration_factor 
            
            velocity = velocity_base

            # Check for octave variation
            current_midi_note = root_midi_note
            if beat_offset in octave_variation_beats:
                current_midi_note += 12 # Raise by one octave

            # RPR_MIDI_InsertNote(MIDI_CONTEXT, SELECTED, MUTE, START_TIME_BEAT, END_TIME_BEAT, CHANNEL, VELOCITY, PITCH, NO_DRAW)
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, position_beats, position_beats + note_length_beats, 0, velocity, current_midi_note, False)
            total_notes_added += 1

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_UpdateAndFree(midi_take, True)

    RPR.RPR_Undo_EndBlock(f"Created '{track_name}' Bass Line", -1)
    RPR.RPR_PreventUIRefresh(-1)

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM"

