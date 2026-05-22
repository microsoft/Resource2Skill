def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Moving Bassline",
    bpm: int = 110,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a dual-layer Slap Bass Groove (Foundation + Slap) in REAPER.
    """
    import reaper_python as RPR
    import random

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

    if scale not in SCALES:
        scale = "minor"
    
    # Base MIDI note (e.g., E1)
    root_midi = 24 + NOTE_MAP.get(key, 4)
    scale_intervals = SCALES[scale]

    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    cursor_pos = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def create_bass_layer(name, is_slap):
        # Create track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} - {name}", True)
        
        # Add ReaSynth
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        # Tweak ReaSynth for bass
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0) # Volume
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Tuning
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 1.0) # Attack (0=fast)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.4 if is_slap else 0.8) # Decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1 if is_slap else 0.5) # Sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2) # Release

        if is_slap:
            # Add Compressor to slap track for transient snap
            comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -15.0) # Thresh
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 4.0)   # Ratio
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 5.0)   # Attack (ms)
            RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 50.0)  # Release (ms)
        else:
            # Add EQ to foundation track to make it mellow ("fingered")
            eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 0.0) # High Shelf / Lowpass type
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 800.0) # Cutoff Hz
            RPR.RPR_TrackFX_SetParam(track, eq_idx, 14, -12.0) # Gain down

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, take

    foundation_track, foundation_take = create_bass_layer("Fingered", False)
    slap_track, slap_take = create_bass_layer("Slap", True)

    # Note definitions: (beat_pos, duration_beats, scale_degree, octave_offset, base_vel, is_slap)
    # 2-bar looping groove
    groove_pattern = [
        # Bar 1 (Focus on root foundation and snappy upper octave)
        (0.0,  0.75, 0, 0, 95, False), # Downbeat root
        (0.75, 0.15, 0, 1, 120, True),  # 16th slap (octave)
        (1.5,  0.5,  0, 0, 85, False), # 8th root syncopation
        (2.5,  0.5,  2, 0, 90, False), # Walk up to the 3rd
        (3.0,  0.5,  3, 0, 90, False), # Walk up to the 4th
        (3.75, 0.15, 3, 1, 115, True),  # 16th slap on the 4th (octave up)
        
        # Bar 2 (Adding ghost notes and more movement)
        (4.0,  0.5,  4, 0, 95, False), # Downbeat 5th
        (4.5,  0.15, 4, 1, 100, True),  # Ghost slap
        (5.0,  0.5,  0, 0, 95, False), # Back to root
        (5.75, 0.15, 0, 1, 125, True),  # Heavy slap
        (6.5,  0.5,  0, 0, 85, False), # Foundation
        (7.25, 0.15, 2, 1, 115, True),  # Slap on the 3rd
        (7.75, 0.15, 3, 1, 120, True),  # Slap on the 4th leading back to 1
    ]

    notes_created = 0

    # Generate MIDI for all bars
    for bar in range(0, bars, 2):
        for note in groove_pattern:
            b_pos, b_dur, scale_deg, oct_off, vel, is_slap = note
            
            # If we are on the last bar and it's an odd number of bars, don't write the 2nd half of the pattern
            if bar + 1 >= bars and b_pos >= 4.0:
                continue

            # Calculate actual scale pitch
            degree = scale_deg % len(scale_intervals)
            octave_shift = (scale_deg // len(scale_intervals)) + oct_off
            pitch = root_midi + scale_intervals[degree] + (octave_shift * 12)
            
            # Humanize timing (-10ms to +10ms)
            humanize_offset = random.uniform(-0.01, 0.01)
            
            # Calculate absolute time
            start_time = cursor_pos + ((bar * 4) + b_pos) * beat_length_sec + humanize_offset
            end_time = start_time + (b_dur * beat_length_sec)
            
            # Humanize velocity
            final_vel = int(min(127, max(1, vel + random.randint(-8, 8))))
            
            # Select proper take based on articulation
            current_take = slap_take if is_slap else foundation_take
            
            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(current_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(current_take, end_time)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(current_take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, True)
            notes_created += 1

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(foundation_take)
    RPR.RPR_MIDI_Sort(slap_take)

    return f"Created dual-layer '{track_name}' (Fingered + Slap) with {notes_created} notes over {bars} bars at {bpm} BPM in {key} {scale}."
