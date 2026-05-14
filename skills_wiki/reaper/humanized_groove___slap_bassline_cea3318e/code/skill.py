def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groove Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized, syncopated slap bassline pattern in REAPER.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup ===
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add Instrument & FX
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item_start = RPR.RPR_GetCursorPosition()
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_start)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define the Groove Pattern ===
    # Format: (beat_position, pitch_val, is_semitone_interval, length_in_beats, target_vel)
    # is_semitone_interval=True means pitch_val is exact semitones from root (e.g. 12 = Octave)
    # is_semitone_interval=False means pitch_val is an index in the scale array
    pattern = [
        # --- Bar 1 ---
        (0.00,  0,  True,  0.75, 100), # Beat 1.1: Root anchor
        (1.75, 12,  True,  0.15, 127), # Beat 2.4: Octave Slap (staccato, high vel)
        (2.50,  0,  True,  0.50, 90),  # Beat 3.3: Root
        (3.50,  7,  True,  0.25, 95),  # Beat 4.3: 5th degree passing tone
        (3.75, 12,  True,  0.15, 127), # Beat 4.4: Octave Slap
        # --- Bar 2 ---
        (4.00,  0,  True,  0.75, 105), # Beat 1.1: Root anchor
        (5.50,  2,  False, 0.25, 90),  # Beat 2.3: Scale 3rd passing tone
        (6.00, 12,  True,  0.15, 127), # Beat 3.1: Octave Slap
        (7.00, -1,  False, 0.25, 95),  # Beat 4.1: Lower 7th passing tone
        (7.50,  0,  True,  0.50, 90),  # Beat 4.3: Root lead-in
    ]

    root_note = 36 + NOTE_MAP.get(key, 0) # Base octave (E1/C2 range)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    note_count = 0

    # Repeat 2-bar pattern across requested bars
    for bar_pair in range((bars + 1) // 2):
        beat_offset = bar_pair * 8.0
        
        for p_beat, p_val, is_interval, p_len, p_vel in pattern:
            abs_beat = beat_offset + p_beat
            if abs_beat >= bars * beats_per_bar:
                continue
                
            # Pitch Calculation
            if is_interval:
                midi_pitch = root_note + p_val
            else:
                idx = p_val
                if idx < 0:
                    midi_pitch = root_note - 12 + scale_intervals[idx % len(scale_intervals)]
                else:
                    midi_pitch = root_note + scale_intervals[idx % len(scale_intervals)]

            # Humanization (Timing & Velocity Offsets)
            timing_nudge = random.uniform(-0.02, 0.02)
            start_beat = max(0.0, abs_beat + timing_nudge)
            end_beat = start_beat + p_len
            
            vel_nudge = int(random.uniform(-5, 5))
            final_vel = max(1, min(127, p_vel + vel_nudge))

            # Convert Beats to PPQ
            start_time_sec = item_start + (start_beat * (60.0 / bpm))
            end_time_sec = item_start + (end_beat * (60.0 / bpm))
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, final_vel, False)
            note_count += 1

    # Force UI update
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}. High-velocity notes are designed to trigger slap articulations."
