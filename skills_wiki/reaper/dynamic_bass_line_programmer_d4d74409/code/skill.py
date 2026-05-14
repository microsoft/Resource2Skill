def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Adjusted based on tutorial's suggestion
    note_duration: str = "quarter", # "quarter", "eighth", "sixteenth", "full"
    style: str = "kick_follow", # "kick_follow", "guitar_root_follow"
    octave_shift: int = 0, # Additional octave shift for the entire bass line
    **kwargs,
) -> str:
    """
    Create a bass line in the current REAPER project, either following a kick drum
    pattern or a specific guitar riff example.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        note_duration: Default note length ("quarter", "eighth", "sixteenth", "full").
        style: Bass programming style ("kick_follow" or "guitar_root_follow").
        octave_shift: Additional octave shift (e.g., 1 for one octave up).
        **kwargs: Additional overrides.

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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    # Octave 0 in MIDI is C-2, Octave 2 is C0 (midi 24), Octave 3 is C1 (midi 36)
    # Bass typically sits in octave 2-3 (MIDI 24-47) for standard tuning, or lower for drop tunings.
    # Let's target a low octave for the root note, typically A1 to E2 (MIDI 33 to 40) for a standard bass.
    # For a general "C" root, start at C2 (MIDI 36).
    MIDI_OCTAVE_OFFSET = 36 # C2

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Add some basic EQ for bass clarity and low-end boost (optional but good practice)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # RPR.RPR_TrackFX_SetParam(track, 1, 0, 1.0) # Band 1 enable
    RPR.RPR_TrackFX_SetParam(track, 1, 3, 80.0) # Band 1 Freq to 80 Hz
    RPR.RPR_TrackFX_SetParam(track, 1, 4, 6.0) # Band 1 Gain to 6 dB
    RPR.RPR_TrackFX_SetParam(track, 1, 5, 1.0) # Band 1 Q to 1.0
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 2, 0, 0.0) # Threshold to -20 dB
    RPR.RPR_TrackFX_SetParam(track, 2, 1, 0.25) # Ratio to 4:1 (0.25 = 1/4)
    RPR.RPR_TrackFX_SetParam(track, 2, 2, 0.005) # Attack 5 ms
    RPR.RPR_TrackFX_SetParam(track, 2, 3, 0.1) # Release 100 ms

    # === Step 4: Create MIDI Item and Notes ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_MIDI_Clear(take) # Clear any default notes

    root_midi_note = NOTE_MAP.get(key, 0) # Default to C if key is invalid
    scale_intervals = SCALES.get(scale, SCALES["minor"]) # Default to minor

    notes_inserted = 0
    RPR.RPR_MIDI_SetItemExtents(take, 0, item_length) # Set item length for MIDI

    if style == "kick_follow":
        # Simple kick-following pattern (quarter notes on each beat)
        note_len_factor = 0.9 # Default slightly shorter than full duration
        if note_duration == "quarter":
            note_len = beat_length_sec * 0.9
        elif note_duration == "eighth":
            note_len = (beat_length_sec / 2) * 0.9
        elif note_duration == "sixteenth":
            note_len = (beat_length_sec / 4) * 0.9
        elif note_duration == "full":
            note_len = beat_length_sec # sustained

        for bar in range(bars):
            for beat in range(beats_per_bar):
                position = (bar * bar_length_sec) + (beat * beat_length_sec)
                midi_pitch = root_midi_note + MIDI_OCTAVE_OFFSET + (octave_shift * 12)
                RPR.RPR_MIDI_InsertNote(take, False, False, position, position + note_len, velocity_base, 0, midi_pitch)
                notes_inserted += 1

    elif style == "guitar_root_follow":
        # Transcribed bass line from video tutorial's example (5:10 - 5:20)
        # Assumed Drop A tuning implies specific low notes.
        # Notes are relative to A1 (MIDI 33) for clarity here, then converted to absolute.
        # Example pattern for 8 bars, adjust for 'bars' parameter later if needed.
        # This is a fixed pattern for demonstration purposes.

        # The video example shows a bass line that is already adjusted for the guitar riff.
        # Transcribing the "yellow notes" from the piano roll (5:10-5:20)
        # Notes: A1 (MIDI 33), E2 (MIDI 40), C#2 (MIDI 37), D2 (MIDI 38), G2 (MIDI 43), F#2 (MIDI 42)
        
        # Pattern repeats every 4 bars in the example
        # Bar 1 (from example start, which is bar 11 in video timeline): A1 E2 C#2 D2
        # Bar 2 (bar 12): A1 E2 C#2 D2
        # Bar 3 (bar 13): G2 F#2 D2 E2
        # Bar 4 (bar 14): G2 F#2 D2 E2

        # A1 is MIDI 33
        # E2 is MIDI 40
        # C#2 is MIDI 37
        # D2 is MIDI 38
        # G2 is MIDI 43
        # F#2 is MIDI 42

        pattern_notes = [
            # Bar 1
            (33, 0.0, beat_length_sec * 0.75), # A1, quarter-ish
            (40, beat_length_sec * 0.5, beat_length_sec * 0.25), # E2, eighth
            (37, beat_length_sec * 1.0, beat_length_sec * 0.25), # C#2, eighth
            (38, beat_length_sec * 1.5, beat_length_sec * 0.25), # D2, eighth
            # Bar 2
            (33, beat_length_sec * 2.0, beat_length_sec * 0.75), # A1, quarter-ish
            (40, beat_length_sec * 2.5, beat_length_sec * 0.25), # E2, eighth
            (37, beat_length_sec * 3.0, beat_length_sec * 0.25), # C#2, eighth
            (38, beat_length_sec * 3.5, beat_length_sec * 0.25), # D2, eighth

            # Bar 3
            (43, bar_length_sec + 0.0, beat_length_sec * 0.75), # G2, quarter-ish
            (42, bar_length_sec + beat_length_sec * 0.5, beat_length_sec * 0.25), # F#2, eighth
            (38, bar_length_sec + beat_length_sec * 1.0, beat_length_sec * 0.25), # D2, eighth
            (40, bar_length_sec + beat_length_sec * 1.5, beat_length_sec * 0.25), # E2, eighth
            # Bar 4
            (43, bar_length_sec + beat_length_sec * 2.0, beat_length_sec * 0.75), # G2, quarter-ish
            (42, bar_length_sec + beat_length_sec * 2.5, beat_length_sec * 0.25), # F#2, eighth
            (38, bar_length_sec + beat_length_sec * 3.0, beat_length_sec * 0.25), # D2, eighth
            (40, bar_length_sec + beat_length_sec * 3.5, beat_length_sec * 0.25), # E2, eighth
        ]
        
        for bar_offset in range(0, bars, 4): # Loop in 4-bar chunks
            current_bar_start_time = bar_offset * bar_length_sec
            for pitch, start_offset, duration in pattern_notes:
                if current_bar_start_time + start_offset + duration <= item_length:
                    midi_pitch = pitch + (octave_shift * 12)
                    RPR.RPR_MIDI_InsertNote(take, False, False, current_bar_start_time + start_offset, current_bar_start_time + start_offset + duration, velocity_base, 0, midi_pitch)
                    notes_inserted += 1

    else:
        return f"Error: Unknown bass style '{style}'. Please choose 'kick_follow' or 'guitar_root_follow'."

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_inserted} notes over {bars} bars at {bpm} BPM in {style} style."

