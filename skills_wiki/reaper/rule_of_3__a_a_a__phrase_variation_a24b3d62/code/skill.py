def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Melody",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  # Hardcoded to 12 in logic to demonstrate 3x 4-bar phrases
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' (A/A/A' Variation) phrase in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Ignored for this specific skill (forces 12 bars to perfectly match the tutorial).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        # Fallback to major if unsupported scale is provided
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.upper(), 0)

    def degree_to_pitch(degree, root_note=60):
        """Converts a scale degree (0-indexed) to an absolute MIDI pitch."""
        octave = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_note + (octave * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = 12 # 3 iterations of 4 bars
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(start_sec, end_sec, pitch, vel):
        """Helper to insert a note via PPQ calculation."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 4: Generate Rule of 3 Pattern ===
    bar_idx = 0
    
    for iteration in range(3):
        # 4 bars per iteration
        for b in range(4):
            is_variation = False
            
            # THE RULE OF 3: On the 3rd iteration (index 2), diverge halfway through (bars 3 & 4)
            if iteration == 2 and b >= 2:
                is_variation = True

            # Progression Selection
            if is_variation:
                if b == 2: chord_degree = 1 # ii chord (diverges)
                else: chord_degree = 4      # V chord (resolution)
            else:
                if b == 0: chord_degree = 0   # I chord
                elif b == 1: chord_degree = 4 # V chord
                elif b == 2: chord_degree = 5 # vi chord
                else: chord_degree = 3        # IV chord

            start_offset = bar_idx * bar_length_sec
            
            # Write Bass Note (1 octave lower, holds for whole bar)
            bass_pitch = degree_to_pitch(chord_degree, root_note=root_val + 36)
            insert_note(start_offset, start_offset + bar_length_sec - 0.1, bass_pitch, velocity_base - 10)

            # Write Arpeggiated Melody
            # If it's the variation, we push the melody up an octave to increase energy
            oct_offset = 7 if is_variation else 0
            
            # Simple 8th note arpeggio motif (Root, 3rd, 5th, 3rd, Oct, 5th, 3rd, Root)
            melody_degrees = [
                (0.0, chord_degree + oct_offset),
                (0.5, chord_degree + 2 + oct_offset),
                (1.0, chord_degree + 4 + oct_offset),
                (1.5, chord_degree + 2 + oct_offset),
                (2.0, chord_degree + 7 + oct_offset),
                (2.5, chord_degree + 4 + oct_offset),
                (3.0, chord_degree + 2 + oct_offset),
                (3.5, chord_degree + 0 + oct_offset),
            ]
            
            for beat, deg in melody_degrees:
                pitch = degree_to_pitch(deg, root_note=root_val + 60)
                note_start = start_offset + (beat * 60.0 / bpm)
                note_end = note_start + (0.45 * 60.0 / bpm) # Detached for clarity
                
                # Highlight variation with slightly higher velocity
                vel = velocity_base + 10 if is_variation else velocity_base
                insert_note(note_start, note_end, pitch, vel)

            bar_idx += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape synth to be a soft triangle wave (sounds a bit like an electric piano/pad)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.0) # Saw shape down
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 1, 0.0) # Square shape down
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 1.0) # Triangle shape up
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.1) # Extra Sine 

    return f"Created '{track_name}' demonstrating Rule of 3 phrasing over 12 bars at {bpm} BPM in {key} {scale}."
