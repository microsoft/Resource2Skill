def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "PopBeat",
    bpm: int = 128,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pop/Hip-Hop 8-Bar Beat Construction (Chords + Drums) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (128 used in tutorial).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (distributes 4 chords evenly across these bars).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Music Theory Setup ===
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

    root_val = NOTE_MAP.get(key, 0)
    root_midi = 48 + root_val  # Base octave C3 = 48
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Generate a diatonic scale array across multiple octaves
    scale_notes = []
    for oct in range(-1, 4): 
        for interval in scale_intervals:
            scale_notes.append(root_midi + interval + (oct * 12))

    def get_chord_from_scale(degree, num_notes=3):
        """Constructs a root position triad by stacking thirds in the generated scale."""
        base_idx = len(scale_intervals) # Points to the root_midi in the 0th octave
        chord = []
        for i in range(num_notes):
            chord.append(scale_notes[base_idx + degree + (i * 2)])
        return chord

    # Target Progression: IV - I - V - vi (0-indexed scale degrees: 3, 0, 4, 5)
    progression_degrees = [3, 0, 4, 5]
    
    # Timing Setup
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4.0
    item_length = bar_len * bars

    # ==========================================
    # === Step 2: Create Chords Track & MIDI ===
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    chords_track_idx = RPR.RPR_CountTracks(0) - 1
    chords_track = RPR.RPR_GetTrack(0, chords_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name} Chords", True)

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", item_length)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Add audible synth to chords track
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)

    # Calculate duration of each chord so they perfectly stretch to fit the `bars` parameter
    chord_len_sec = (bars / len(progression_degrees)) * bar_len
    chord_note_count = 0

    for i, degree in enumerate(progression_degrees):
        chord_notes = get_chord_from_scale(degree, 3)
        start_time = i * chord_len_sec
        end_time = start_time + chord_len_sec - 0.05 # Leave a slight gap for articulation
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        for pitch in chord_notes:
            # Drop velocity slightly for softer pads/chords
            vel = int(velocity_base * 0.8)
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            chord_note_count += 1

    RPR.RPR_MIDI_Sort(chords_take)

    # =========================================
    # === Step 3: Create Drums Track & MIDI ===
    # =========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    drums_track_idx = RPR.RPR_CountTracks(0) - 1
    drums_track = RPR.RPR_GetTrack(0, drums_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_track, "P_NAME", f"{track_name} Drums", True)

    drums_item = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_LENGTH", item_length)
    drums_take = RPR.RPR_AddTakeToMediaItem(drums_item)

    # General MIDI standard map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    sixteenth_len = beat_len / 4.0
    drum_note_count = 0

    for b in range(bars):
        bar_start = b * bar_len
        
        # Syncopated Kick: Beat 1 (Step 0) and Beat 3.5 (Step 10)
        for step in [0, 10]:
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, KICK, velocity_base, False)
            drum_note_count += 1
            
        # Backbeat Snare: Beat 2 (Step 4) and Beat 4 (Step 12)
        for step in [4, 12]:
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
            drum_note_count += 1
            
        # Continuous Hi-Hats with Humanized Alternating Velocity
        for step in range(16):
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            
            # Accent downbeats/eighths, soften sixteenth off-beats
            vel = velocity_base if (step % 2 == 0) else int(velocity_base * 0.7)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, HIHAT, vel, False)
            drum_note_count += 1

    RPR.RPR_MIDI_Sort(drums_take)

    return f"Created Pop/Hip-Hop Beat over {bars} bars at {bpm} BPM. Generated {chord_note_count} chord notes and {drum_note_count} drum hits."
