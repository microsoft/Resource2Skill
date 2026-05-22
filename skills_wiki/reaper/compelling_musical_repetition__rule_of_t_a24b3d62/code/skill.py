def create_rule_of_three_example(
    project_name: str = "MyProject",
    track_name_chords: str = "Piano Chords",
    track_name_melody: str = "Piano Melody",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4, # Refers to the length of one musical idea/phrase
    octave_chords: int = 3, # Base octave for the root of the first chord
    octave_melody: int = 4, # Base octave for the melody
    velocity_chords: int = 90,
    velocity_melody: int = 100,
    variation_type: str = "full_new", # "full_new" or "half_new"
    **kwargs,
) -> str:
    """
    Creates a musical example demonstrating the "Rule of Three" principle of repetition and variation.
    The musical idea (chords + melody) is played twice for reinforcement, and the third time
    a variation is introduced to maintain listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name_chords: Name for the chords track.
        track_name_melody: Name for the melody track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for *one* musical idea/phrase (e.g., 4 bars).
        octave_chords: Base octave for the root of the first chord (e.g., 3 for C3).
        octave_melody: Base octave for the melody (e.g., 4 for C4).
        velocity_chords: Base MIDI velocity for chords (0-127).
        velocity_melody: Base MIDI velocity for melody (0-127).
        variation_type: Specifies the type of variation for the third repetition.
                        "full_new" means the entire 3rd repetition is a new melody.
                        "half_new" means the first half of the 3rd repetition is original,
                                   the second half is new melody.
        **kwargs: Additional overrides (not used in this specific skill but for compatibility).

    Returns:
        Status string, e.g., "Created 'Piano Chords' and 'Piano Melody' demonstrating Rule of Three."
    """
    import reaper_python as RPR

    # Music theory lookup tables (from prompt)
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

    def get_midi_note_from_scale_degree(root_midi: int, target_octave: int, scale_degree: int, scale_pattern: list) -> int:
        scale_len = len(scale_pattern)
        octave_adjust = scale_degree // scale_len
        degree_in_pattern = scale_degree % scale_len
        
        # Calculate base octave MIDI value for the root
        # C0 is MIDI 12, C1 is MIDI 24, etc. So C4 is MIDI 60.
        # root_midi is 0-11 for the note. target_octave is the absolute octave number.
        base_midi_for_root_octave = root_midi + (target_octave * 12)
        
        midi_note = base_midi_for_root_octave + scale_pattern[degree_in_pattern] + (octave_adjust * 12)
        return midi_note

    # Get project time information
    RPR.RPR_PreventUIRefresh(1)
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    RPR.RPR_OnStopButton() # Ensure transport is stopped

    root_midi_key = NOTE_MAP.get(key, 0)
    current_scale_pattern = SCALES.get(scale, SCALES["major"])
    
    # Define the 4-bar progression I-V-vi-IV using scale degrees from the root of the progression
    # The video's specific voicings are used for this demonstration
    # Cmaj (I), Gmaj (V), Amin (vi), Fmaj (IV)
    # These are fixed relative to the C major example from the video's voicing.
    # To make it more generic, we would calculate these based on the `key` and `scale`.
    # For now, let's use the absolute MIDI notes from the video's example and adjust by root_midi_key if different from C.

    # The video demonstrated I-V-vi-IV in C Major.
    # To generalize, we need to map the intervals to the new key/scale.
    # For simplicity, I'll calculate the fixed chord voicings and melodies relative to the chosen key.

    # Chord roots as scale degrees (0=root, 4=5th, 5=6th, 3=4th)
    chord_roots_degrees = [0, 4, 5, 3] # I, V, vi, IV
    
    # Chord types: major, major, minor, major
    chord_intervals = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7]
    }

    # Original Melody as scale degrees relative to the key (C major example used 5-6-7-1 for first bar, etc.)
    # We will adjust these based on the actual key and scale.
    original_melody_degrees = [
        # Bar 1 (over I)
        (4, 0.0, 0.25), (5, 0.25, 0.25), (6, 0.5, 0.25), (7, 0.75, 0.25), # G-A-B-C (relative to key, 5-6-7-1 in C)
        # Bar 2 (over V)
        (5, 1.0, 0.25), (4, 1.25, 0.25), (3, 1.5, 0.25), (2, 1.75, 0.25), # A-G-F-E
        # Bar 3 (over vi)
        (3, 2.0, 0.25), (4, 2.25, 0.25), (5, 2.5, 0.25), (6, 2.75, 0.25), # F-G-A-B
        # Bar 4 (over IV)
        (5, 3.0, 0.25), (4, 3.25, 0.25), (7, 3.5, 0.5)                   # A-G-C (last C is 1st degree of next octave)
    ]

    # Variation Melody (new melody for the 3rd cycle)
    variation_melody_degrees = [
        # Bar 1 (over I)
        (9, 0.0, 0.25), (7, 0.25, 0.25), (6, 0.5, 0.25), (5, 0.75, 0.25), # D-C-B-A
        # Bar 2 (over V)
        (4, 1.0, 0.25), (3, 1.25, 0.25), (2, 1.5, 0.25), (1, 1.75, 0.25), # G-F-E-D
        # Bar 3 (over vi)
        (0, 2.0, 0.25), (1, 2.25, 0.25), (2, 2.5, 0.25), (3, 2.75, 0.25), # C-D-E-F
        # Bar 4 (over IV)
        (4, 3.0, 0.25), (5, 3.25, 0.25), (6, 3.5, 0.25), (7, 3.75, 0.25)  # G-A-B-C
    ]
    
    # === Track Creation and Setup ===
    track_chords_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_chords_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_chords_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", track_name_chords, True)
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)

    track_melody_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_melody_idx, True)
    track_melody = RPR.RPR_GetTrack(0, track_melody_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_melody, "P_NAME", track_name_melody, True)
    RPR.RPR_TrackFX_AddByName(track_melody, "ReaSynth", False, -1)

    # === MIDI Item Creation ===
    # A full demonstration includes 3 repetitions of the 'bars' idea
    total_bars = bars * 3
    item_length_beats = total_bars * 4 # Assuming 4 beats per bar
    
    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", item_length_beats / (bpm / 60.0) / 4.0) # Length in seconds
    RPR.RPR_MarkTrackItemsDirty(track_chords, item_chords)
    take_chords = RPR.RPR_GetActiveTake(item_chords)
    RPR.RPR_MIDI_Clear(RPR.RPR_MIDI_GetTakeMidiDataSet(take_chords))

    item_melody = RPR.RPR_AddMediaItemToTrack(track_melody)
    RPR.RPR_SetMediaItemInfo_Value(item_melody, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_melody, "D_LENGTH", item_length_beats / (bpm / 60.0) / 4.0)
    RPR.RPR_MarkTrackItemsDirty(track_melody, item_melody)
    take_melody = RPR.RPR_GetActiveTake(item_melody)
    RPR.RPR_MIDI_Clear(RPR.RPR_MIDI_GetTakeMidiDataSet(take_melody))

    # === Insert MIDI Notes ===
    # Calculate intervals from the root of the chosen key
    root_midi_offset = root_midi_key - NOTE_MAP["C"] # Difference from C to chosen key

    midi_notes_added_count = 0
    for repetition_num in range(3): # For each of the three repetitions
        start_time_offset_beats = repetition_num * bars * 4

        # --- Chords ---
        for bar_idx in range(bars):
            chord_root_degree_in_prog = chord_roots_degrees[bar_idx % len(chord_roots_degrees)]
            chord_base_midi = get_midi_note_from_scale_degree(root_midi_key, octave_chords, chord_root_degree_in_prog, current_scale_pattern)
            
            # Determine if it's major or minor chord for this position in I-V-vi-IV
            if bar_idx % len(chord_roots_degrees) == 2: # vi chord is minor
                intervals = chord_intervals["minor"]
            else: # I, V, IV are major
                intervals = chord_intervals["major"]

            for interval in intervals:
                note_on_beat = start_time_offset_beats + (bar_idx * 4)
                note_off_beat = note_on_beat + 4 # Hold for full bar
                
                midi_note = chord_base_midi + interval
                
                RPR.RPR_MIDI_InsertNote(RPR.RPR_MIDI_GetTakeMidiDataSet(take_chords),
                                       False, False,
                                       note_on_beat, note_off_beat, 0, midi_note, velocity_chords, True)
                midi_notes_added_count += 1
        
        # --- Melody ---
        current_melody_pattern = original_melody_degrees
        if repetition_num == 2: # This is the third time, introduce variation
            if variation_type == "full_new":
                current_melody_pattern = variation_melody_degrees
            elif variation_type == "half_new":
                # For half_new, first half is original, second half is new
                for mel_degree, time_beat, duration_beat in original_melody_degrees:
                    if time_beat < bars * 2: # First half of the phrase (e.g., first 2 bars of a 4-bar phrase)
                        note_on_beat = start_time_offset_beats + time_beat
                        note_off_beat = note_on_beat + duration_beat
                        midi_note = get_midi_note_from_scale_degree(root_midi_key, octave_melody, mel_degree, current_scale_pattern)
                        RPR.RPR_MIDI_InsertNote(RPR.RPR_MIDI_GetTakeMidiDataSet(take_melody),
                                               False, False,
                                               note_on_beat, note_off_beat, 0, midi_note, velocity_melody, True)
                        midi_notes_added_count += 1
                
                # Second half of the phrase is new melody
                for mel_degree, time_beat, duration_beat in variation_melody_degrees:
                    if time_beat >= bars * 2: # Second half of the phrase (e.g., last 2 bars of a 4-bar phrase)
                        note_on_beat = start_time_offset_beats + time_beat
                        note_off_beat = note_on_beat + duration_beat
                        midi_note = get_midi_note_from_scale_degree(root_midi_key, octave_melody, mel_degree, current_scale_pattern)
                        RPR.RPR_MIDI_InsertNote(RPR.RPR_MIDI_GetTakeMidiDataSet(take_melody),
                                               False, False,
                                               note_on_beat, note_off_beat, 0, midi_note, velocity_melody, True)
                        midi_notes_added_count += 1
                continue # Skip the normal loop below for melody if half_new
            
        # Normal melody insertion for original or full_new variation
        for mel_degree, time_beat, duration_beat in current_melody_pattern:
            note_on_beat = start_time_offset_beats + time_beat
            note_off_beat = note_on_beat + duration_beat
            midi_note = get_midi_note_from_scale_degree(root_midi_key, octave_melody, mel_degree, current_scale_pattern)
            RPR.RPR_MIDI_InsertNote(RPR.RPR_MIDI_GetTakeMidiDataSet(take_melody),
                                   False, False,
                                   note_on_beat, note_off_beat, 0, midi_note, velocity_melody, True)
            midi_notes_added_count += 1

    RPR.RPR_MIDI_Sort(RPR.RPR_MIDI_GetTakeMidiDataSet(take_chords))
    RPR.RPR_MIDI_Sort(RPR.RPR_MIDI_GetTakeMidiDataSet(take_melody))
    RPR.RPR_UpdateArrange()
    RPR.RPR_PreventUIRefresh(-1)

    return f"Created '{track_name_chords}' and '{track_name_melody}' demonstrating Rule of Three over {total_bars} bars at {bpm} BPM."

