def create_rule_of_three_sequence(
    project_name: str = "MyProject",
    track_name: str = "Rule of Three Piano",
    bpm: int = 90,
    key: str = "C",
    scale: str = "major",
    bars_per_phrase: int = 4,
    num_phrases: int = 3, # Recommended 3 or more to demonstrate the rule
    variation_type: str = "new_melody_same_chords", # Options: "new_melody_same_chords", "new_progression_new_melody"
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a musical sequence demonstrating the "Rule of Three" composition principle.

    This involves repeating a base musical phrase twice, then introducing a variation
    (either a new melody over the same chords, or a new progression with a new melody)
    for subsequent repetitions.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars_per_phrase: Number of bars in each musical phrase (e.g., 4 bars).
        num_phrases: Total number of 4-bar phrases to generate.
                     To properly demonstrate the rule, 3 or more phrases are recommended.
                     Phrases 1 & 2 will be the base idea. Phrase 3 onwards will be variations.
        variation_type: The type of musical change for the third phrase onwards.
                        "new_melody_same_chords": New melody over the original chords.
                        "new_progression_new_melody": Entirely new chords and melody.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific implementation but useful for extensibility).

    Returns:
        Status string, e.g., "Created 'Rule of Three Piano' with 12 bars at 90 BPM (C major)"
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    # Scales are not directly used for this specific hardcoded melody/chords but kept for compliance
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    CHORD_INTERVALS = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7]
    }

    import reaper_python as RPR

    # Helper to calculate absolute MIDI pitch
    def _get_midi_note(base_note_offset, target_key_root_midi, relative_pitch):
        return target_key_root_midi + relative_pitch

    # Calculate global key offset (from C)
    key_root_midi_0 = NOTE_MAP.get(key.upper(), 0) # Default to C if key is invalid

    # Define base 4-bar phrase (chords and melody) relative to C4 (MIDI 60)
    # Based on video demonstration: C-G-Am-F progression
    # Melody: C5 D5 E5 D5 | B4 C5 D5 C5 | C5 D5 E5 D5 | C5 B4 A4 G4
    base_phrase_data = [
        # Bar 1: C Major Chord (root C)
        {"chord_root_offset_from_C": 0, "chord_type": "major", "melody_pitches_relative_to_C4": [72, 74, 76, 74]},
        # Bar 2: G Major Chord (root G)
        {"chord_root_offset_from_C": 7, "chord_type": "major", "melody_pitches_relative_to_C4": [71, 72, 74, 72]},
        # Bar 3: A Minor Chord (root A)
        {"chord_root_offset_from_C": 9, "chord_type": "minor", "melody_pitches_relative_to_C4": [72, 74, 76, 74]},
        # Bar 4: F Major Chord (root F)
        {"chord_root_offset_from_C": 5, "chord_type": "major", "melody_pitches_relative_to_C4": [72, 71, 69, 67]},
    ]

    # Define variation melody for "new_melody_same_chords" option (relative to C4)
    # Contrasting descending melody
    variation_melody_only = [
        # Bar 1 (Cmaj):
        [67, 65, 64, 60], # G4, F4, E4, C4
        # Bar 2 (Gmaj):
        [62, 60, 59, 55], # D4, C4, B3, G3
        # Bar 3 (Amin):
        [64, 62, 60, 57], # E4, D4, C4, A3
        # Bar 4 (Fmaj):
        [65, 67, 69, 72], # F4, G4, A4, C5
    ]

    # Define new 4-bar phrase for "new_progression_new_melody" option (Dm-G-C-F)
    # Chords: D minor (root D), G major (root G), C major (root C), F major (root F)
    variation_phrase_data = [
        # Bar 1: D Minor Chord (root D)
        {"chord_root_offset_from_C": 2, "chord_type": "minor", "melody_pitches_relative_to_C4": [65, 64, 62, 60]},
        # Bar 2: G Major Chord (root G)
        {"chord_root_offset_from_C": 7, "chord_type": "major", "melody_pitches_relative_to_C4": [67, 69, 71, 62]},
        # Bar 3: C Major Chord (root C)
        {"chord_root_offset_from_C": 0, "chord_type": "major", "melody_pitches_relative_to_C4": [64, 62, 60, 59]},
        # Bar 4: F Major Chord (root F)
        {"chord_root_offset_from_C": 5, "chord_type": "major", "melody_pitches_relative_to_C4": [69, 67, 65, 64]},
    ]

    # === Step 1: Set Tempo ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # Cannot be called from a script in REAPER

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as a basic instrument
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    # Calculate timings
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    bar_length_seconds = seconds_per_beat * beats_per_bar
    quarter_note_length_seconds = seconds_per_beat

    item_length = bar_length_seconds * num_phrases
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length), False) # Ensure MIDI source

    # Open MIDI editor for the new item
    # RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length) # ensure item is a MIDI item
    # RPR.RPR_MIDIEditor_OnCommand(RPR.RPR_MIDIEditor_GetActive(), 40003) # open editor for selected item

    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length) # Set take to MIDI
    RPR.RPR_MIDI_ClearEventList(midi_take) # Clear any default notes

    notes_added = 0
    current_time_pos_beats = 0.0

    for phrase_index in range(num_phrases):
        current_phrase_data = base_phrase_data
        current_variation_melody = None

        # Apply variation from the 3rd phrase onwards
        if phrase_index >= 2:
            if variation_type == "new_melody_same_chords":
                # Chords remain from base_phrase_data, but melody comes from variation_melody_only
                current_variation_melody = variation_melody_only
            elif variation_type == "new_progression_new_melody":
                current_phrase_data = variation_phrase_data
            else:
                # Fallback to original if variation type is unrecognized
                pass

        for bar_idx in range(bars_per_phrase):
            bar_data = current_phrase_data[bar_idx]
            chord_root_offset = bar_data["chord_root_offset_from_C"]
            chord_type = bar_data["chord_type"]
            melody_pitches = bar_data["melody_pitches_relative_to_C4"] if current_variation_melody is None else current_variation_melody[bar_idx]

            # Insert Chord Notes (bottom octave 3 relative to C)
            for interval in CHORD_INTERVALS[chord_type]:
                chord_midi_pitch = key_root_midi_0 + chord_root_offset + interval + 36 # C3 base, C4 is MIDI 60, so C3 is MIDI 48
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_time_pos_beats, current_time_pos_beats + beats_per_bar/4.0, 0, velocity_base - 10, chord_midi_pitch, False)
                notes_added += 1

            # Insert Melody Notes (octave 4/5 relative to C)
            for note_idx, melody_rel_pitch in enumerate(melody_pitches):
                melody_midi_pitch = key_root_midi_0 + (melody_rel_pitch - NOTE_MAP['C'])
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, 
                                        current_time_pos_beats + note_idx * (beats_per_bar/4.0), 
                                        current_time_pos_beats + (note_idx + 1) * (beats_per_bar/4.0) - (beats_per_bar/16.0), # Slightly shorter for articulation
                                        0, velocity_base, melody_midi_pitch, False)
                notes_added += 1

            current_time_pos_beats += beats_per_bar # Move to next bar

    # Update MIDI item
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes over {num_phrases * bars_per_phrase} bars at {bpm} BPM in {key} {scale}"

