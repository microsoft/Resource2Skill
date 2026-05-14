def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a groovy, slapped bassline with syncopation, octave jumps, 
    diatonic approach notes, and humanized timing offsets.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for root notes (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_note_idx = NOTE_MAP.get(key.upper(), 4) # Default to E
    
    # We put the bass in Octave 1 (C1 = 24)
    bass_octave_base = 24 + base_note_idx

    # Simple 4-bar chord progression derived from the scale (e.g., i - iv - i - v)
    # Using indices of the scale_intervals array
    progression_degrees = [0, 3, 0, 4] 

    def get_scale_note(degree):
        # Wraps around the scale and adjusts the octave accordingly
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return bass_octave_base + (octave_shift * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add and Configure FX (ReaSynth for plucky bass) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a "Slap" profile (fast decay, low sustain, some square wave)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.4)  # Square mix (0-1) - Adds bite
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)  # Attack (instant)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.1)  # Decay (short, plucky)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.2)  # Sustain volume (low)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.1)  # Release (quick)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item_start = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_start)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to add a humanized note
    notes_added = 0
    def add_midi_note(start_beat, length_beats, pitch, vel, humanize_timing=True):
        nonlocal notes_added
        
        # Add slight humanization offset (-15ms to +15ms)
        offset_sec = random.uniform(-0.015, 0.015) if humanize_timing else 0.0
        
        start_proj = item_start + (start_beat * beat_sec) + offset_sec
        end_proj = start_proj + (length_beats * beat_sec)
        
        # Convert absolute time to PPQ
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_proj)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_proj)
        
        # Add slight velocity humanization
        vel = max(1, min(127, int(vel + random.uniform(-5, 5))))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
        notes_added += 1

    # === Step 5: Generate the Groove ===
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Get the current chord root for this bar
        current_degree = progression_degrees[bar % len(progression_degrees)]
        root_pitch = get_scale_note(current_degree)
        
        # -- Beat 1: Strong downbeat root --
        add_midi_note(bar_start_beat + 0.0, 0.75, root_pitch, velocity_base)
        
        # -- Beat 1.75: Syncopated octave slap (1/16th note before beat 3) --
        # Short length, max velocity for the "slap"
        add_midi_note(bar_start_beat + 1.75, 0.25, root_pitch + 12, 127)
        
        # -- Beat 2.5: Off-beat root note --
        add_midi_note(bar_start_beat + 2.5, 0.5, root_pitch, velocity_base - 10)
        
        # -- Beat 3.5: Another octave slap --
        add_midi_note(bar_start_beat + 3.5, 0.25, root_pitch + 12, 127)
        
        # -- Beat 4.75: Diatonic approach note leading into the next bar --
        next_degree = progression_degrees[(bar + 1) % len(progression_degrees)]
        # Approach from one scale degree below the next root
        approach_pitch = get_scale_note(next_degree - 1)
        # Ghost note velocity (much quieter)
        add_midi_note(bar_start_beat + 3.75, 0.25, approach_pitch, velocity_base - 30)

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
