def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 60,
    **kwargs,
) -> str:
    """
    Create a dynamically humanized, velocity-ramped MIDI chord progression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (defaults to 4).
        velocity_base: Starting base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import random
    import math
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # Verify key and scale
    key_upper = key.capitalize()
    if key_upper not in NOTE_MAP:
        key_upper = "C"
    if scale not in SCALES:
        scale = "major"

    # === Chord Progression Logic ===
    # We will build a diatonic array of notes extending across 3 octaves
    base_midi_note = 48 + NOTE_MAP[key_upper] # Start around C3
    scale_degrees = SCALES[scale]
    
    extended_scale = []
    for octave in range(3):
        for d in scale_degrees:
            extended_scale.append(base_midi_note + d + (octave * 12))

    # Standard progression indices (I, vi, IV, V relative to the 7-note scale)
    progression_indices = [0, 5, 3, 4] 
    
    chords = []
    for p in progression_indices:
        # Build a diatonic triad: Root, 3rd, 5th
        root_note = extended_scale[p]
        third_note = extended_scale[p + 2]
        fifth_note = extended_scale[p + 4]
        chords.append([root_note, third_note, fifth_note])

    # === REAPER Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create new track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add native Synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === MIDI Note Insertion & Velocity Humanization ===
    target_peak_velocity = 110
    total_chords = len(chords)
    note_count = 0

    for i in range(bars):
        # Loop the 4-chord progression if bars > 4
        chord = chords[i % total_chords]
        
        # Timing calculations
        start_time = i * bar_length_sec
        end_time = start_time + bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Leave a tiny gap (legato) instead of perfectly touching next chord
        end_ppq -= 20 
        
        # Velocity Ramp Calculation (Crescendo over the bars)
        progress = i / max(1, (bars - 1))
        base_vel = velocity_base + (target_peak_velocity - velocity_base) * progress
        
        # Insert notes for the chord
        for pitch in chord:
            # Humanize: slight random velocity variation per note (±7)
            humanized_vel = int(base_vel + random.randint(-7, 7))
            humanized_vel = max(1, min(127, humanized_vel)) # Clamp 1-127
            
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, humanized_vel, True
            )
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key_upper} {scale}. Applied velocity crescendo."
