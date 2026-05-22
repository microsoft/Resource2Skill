import reaper_python as RPR

# Music theory lookup tables (simplified for direct transposition as per video example)
NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
# Scale is less directly used for chord/melody construction here, more for context.
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

def create_rule_of_three_demonstration(
    project_name: str = "RuleOfThreeProject",
    track_name: str = "Piano Idea",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major", # Context for user, not directly used for note calculation here
    bars: int = 4, # Length of one musical phrase (as in video's 4-bar phrase)
    velocity_base: int = 90,
    variation_type: str = "new_melody", # "new_melody" or "divergent"
    **kwargs,
) -> str:
    """
    Creates a musical demonstration of the "Rule of Three" by generating three
    consecutive 4-bar MIDI items on a new track. The first two items are
    identical, and the third applies a specified variation to maintain interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). All notes will be transposed by this key.
        scale: Scale type (major, minor, etc.). Used for context but not direct note generation here.
        bars: Number of bars for *each* musical phrase (video demonstrates 4-bar phrases).
        velocity_base: Base MIDI velocity (0-127).
        variation_type: Type of variation for the third repetition:
                        "new_melody": Changes the melody while keeping the chord progression.
                        "divergent": Changes the progression and melody mid-phrase.
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created 'Piano Idea' demonstration with 3 items (12 bars total) at 120 BPM"
    """
    RPR.Undo_BeginBlock2(0) # Begin undo block

    # === 1. Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === 2. Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as instrument
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Calculate transposition offset
    root_offset = NOTE_MAP.get(key.upper(), 0) # Default to C (0) if key not found

    # Define the core 4-bar musical phrase
    # Format: (start_beat_in_phrase, end_beat_in_phrase, note_number_relative_to_C4, velocity, is_chord_note)
    # All note_numbers are absolute MIDI notes based on C4 (60)
    phrase_length_beats = bars * 4 # 4 bars * 4 beats/bar = 16 beats

    original_phrase_notes = []
    # Bar 1 (C Maj)
    original_phrase_notes.extend([
        (0.0, 4.0, 60, velocity_base, True), # C4 chord
        (0.0, 4.0, 64, velocity_base, True), # E4 chord
        (0.0, 4.0, 67, velocity_base, True), # G4 chord
        (0.0, 1.0, 67, min(127, velocity_base + 10), False), # G4 melody
        (1.0, 2.0, 72, min(127, velocity_base + 10), False), # C5 melody
        (2.0, 3.0, 64, min(127, velocity_base + 10), False), # E4 melody
        (3.0, 4.0, 67, min(127, velocity_base + 10), False), # G4 melody
    ])
    # Bar 2 (A Min)
    original_phrase_notes.extend([
        (4.0, 8.0, 57, velocity_base, True), # A3 chord
        (4.0, 8.0, 60, velocity_base, True), # C4 chord
        (4.0, 8.0, 64, velocity_base, True), # E4 chord
        (4.0, 5.0, 64, min(127, velocity_base + 10), False), # E4 melody
        (5.0, 6.0, 69, min(127, velocity_base + 10), False), # A4 melody
        (6.0, 7.0, 72, min(127, velocity_base + 10), False), # C5 melody
        (7.0, 8.0, 69, min(127, velocity_base + 10), False), # A4 melody
    ])
    # Bar 3 (F Maj)
    original_phrase_notes.extend([
        (8.0, 12.0, 53, velocity_base, True), # F3 chord
        (8.0, 12.0, 57, velocity_base, True), # A3 chord
        (8.0, 12.0, 60, velocity_base, True), # C4 chord
        (8.0, 9.0, 60, min(127, velocity_base + 10), False), # C4 melody
        (9.0, 10.0, 65, min(127, velocity_base + 10), False), # F4 melody
        (10.0, 11.0, 57, min(127, velocity_base + 10), False), # A3 melody
        (11.0, 12.0, 65, min(127, velocity_base + 10), False), # F4 melody
    ])
    # Bar 4 (G Maj)
    original_phrase_notes.extend([
        (12.0, 16.0, 55, velocity_base, True), # G3 chord
        (12.0, 16.0, 59, velocity_base, True), # B3 chord
        (12.0, 16.0, 62, velocity_base, True), # D4 chord
        (12.0, 13.0, 62, min(127, velocity_base + 10), False), # D4 melody
        (13.0, 14.0, 67, min(127, velocity_base + 10), False), # G4 melody
        (14.0, 15.0, 59, min(127, velocity_base + 10), False), # B3 melody
        (15.0, 16.0, 67, min(127, velocity_base + 10), False), # G4 melody
    ])

    # Define varied melody notes for "new_melody" option
    # Chord notes remain the same as original_phrase_notes (is_chord_note=True)
    new_melody_only_notes = []
    # Bar 1 (C Maj)
    new_melody_only_notes.extend([
        (0.0, 1.0, 76, min(127, velocity_base + 10), False), # E5
        (1.0, 2.0, 74, min(127, velocity_base + 10), False), # D5
        (2.0, 3.0, 72, min(127, velocity_base + 10), False), # C5
        (3.0, 4.0, 67, min(127, velocity_base + 10), False), # G4
    ])
    # Bar 2 (A Min)
    new_melody_only_notes.extend([
        (4.0, 5.0, 72, min(127, velocity_base + 10), False), # C5
        (5.0, 6.0, 71, min(127, velocity_base + 10), False), # B4
        (6.0, 7.0, 69, min(127, velocity_base + 10), False), # A4
        (7.0, 8.0, 64, min(127, velocity_base + 10), False), # E4
    ])
    # Bar 3 (F Maj)
    new_melody_only_notes.extend([
        (8.0, 9.0, 69, min(127, velocity_base + 10), False), # A4
        (9.0, 10.0, 67, min(127, velocity_base + 10), False), # G4
        (10.0, 11.0, 65, min(127, velocity_base + 10), False), # F4
        (11.0, 12.0, 60, min(127, velocity_base + 10), False), # C4
    ])
    # Bar 4 (G Maj)
    new_melody_only_notes.extend([
        (12.0, 13.0, 67, min(127, velocity_base + 10), False), # G4
        (13.0, 14.0, 65, min(127, velocity_base + 10), False), # F4
        (14.0, 15.0, 64, min(127, velocity_base + 10), False), # E4
        (15.0, 16.0, 62, min(127, velocity_base + 10), False), # D4
    ])

    # Define divergent phrase notes for "divergent" option
    # Bars 1-2 same as original
    divergent_phrase_notes = original_phrase_notes[0:14] + original_phrase_notes[14:28] # Copy first 2 bars (C-Am)
    
    # Bar 3 (D Min - new chord progression)
    divergent_phrase_notes.extend([
        (8.0, 12.0, 62, velocity_base, True), # D4 chord
        (8.0, 12.0, 65, velocity_base, True), # F4 chord
        (8.0, 12.0, 69, velocity_base, True), # A4 chord
        (8.0, 9.0, 69, min(127, velocity_base + 10), False), # A4 melody
        (9.0, 10.0, 74, min(127, velocity_base + 10), False), # D5 melody
        (10.0, 11.0, 65, min(127, velocity_base + 10), False), # F4 melody
        (11.0, 12.0, 74, min(127, velocity_base + 10), False), # D5 melody
    ])
    # Bar 4 (G Maj - original chord, but new melody)
    divergent_phrase_notes.extend([
        (12.0, 16.0, 55, velocity_base, True), # G3 chord
        (12.0, 16.0, 59, velocity_base, True), # B3 chord
        (12.0, 16.0, 62, velocity_base, True), # D4 chord
        (12.0, 13.0, 67, min(127, velocity_base + 10), False), # G4 melody
        (13.0, 14.0, 71, min(127, velocity_base + 10), False), # B4 melody
        (14.0, 15.0, 74, min(127, velocity_base + 10), False), # D5 melody
        (15.0, 16.0, 67, min(127, velocity_base + 10), False), # G4 melody
    ])

    num_notes_created = 0

    def create_midi_item_with_notes(start_time_beats, notes_data, item_label):
        item = RPR.RPR_AddMediaItemToTrack(track)
        
        # Calculate item start and length in seconds
        item_start_seconds = start_time_beats / (4.0 * bars) * (bars * 4.0) * (60.0 / bpm) # Total beats / (beats per bar) * total bars * sec/beat
        item_length_seconds = phrase_length_beats / (4.0 * bars) * (bars * 4.0) * (60.0 / bpm) # Should simplify to phrase_length_beats * (60.0/bpm)
        item_length_seconds = phrase_length_beats * (60.0 / bpm) / 4.0 * bars # Length of the item for "bars" at this BPM.
        item_length_seconds = bars * (60.0 / bpm) * 4.0 / 4.0 # For clarity
        item_length_seconds = bars * (60.0 / bpm) # For the 4-bar phrase, this is 4 * (60/bpm) seconds
        item_length_seconds = (phrase_length_beats / 4.0) * (60.0 / bpm) # 16 beats / 4 beats/quarter * seconds_per_quarter = 4 * seconds_per_quarter

        # The phrase_length_beats is 16 beats, representing 4 bars.
        # A bar has 4 beats. So, 16 beats = 4 bars.
        # Length of 1 beat in seconds = 60/bpm
        # Length of 16 beats (4 bars) in seconds = 16 * (60/bpm)
        item_length_seconds = phrase_length_beats * (60.0 / bpm)

        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time_beats * (60.0 / bpm))
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)
        RPR.RPR_GetSetMediaItemInfo_String(item, "P_NAME", item_label, True)
        
        take = RPR.RPR_GetActiveTake(item)
        if take:
            RPR.MIDI_SetItemExtents(item, 0, phrase_length_beats) # Set MIDI item length in beats
            RPR.MIDI_Clear(take, 0) # Clear any existing notes in a new take for safety
            RPR.MIDI_SetPPQ(take, 960) # Standard PPQ for resolution
            
            for start, end, note, vel, _ in notes_data:
                note_transposed = note + root_offset
                # Clip notes to valid MIDI range if out of bounds after transposition
                note_transposed = max(0, min(127, note_transposed))
                RPR.MIDI_InsertNote(take, False, False, start, end, 0, note_transposed, vel, True) # channel 0, not selected, not muted, update
            RPR.MIDI_Sort(take)
            RPR.RPR_UpdateItemInProject(item)
            return len(notes_data)
        return 0

    # === Create 3 MIDI items ===
    current_time_beats = 0.0

    # Item 1: Original phrase (first time)
    num_notes = create_midi_item_with_notes(current_time_beats, original_phrase_notes, "RuleOf3 - Original Idea 1")
    num_notes_created += num_notes
    current_time_beats += phrase_length_beats

    # Item 2: Original phrase (second time)
    num_notes = create_midi_item_with_notes(current_time_beats, original_phrase_notes, "RuleOf3 - Original Idea 2")
    num_notes_created += num_notes
    current_time_beats += phrase_length_beats

    # Item 3: Varied phrase (third time)
    final_phrase_notes_for_item = []
    if variation_type == "new_melody":
        # Combine chord notes from original with new melody notes
        chord_notes_only = [n for n in original_phrase_notes if n[4]]
        final_phrase_notes_for_item = chord_notes_only + new_melody_only_notes
    elif variation_type == "divergent":
        final_phrase_notes_for_item = divergent_phrase_notes
    else: # Default to new_melody if unrecognized variation_type
        chord_notes_only = [n for n in original_phrase_notes if n[4]]
        final_phrase_notes_for_item = chord_notes_only + new_melody_only_notes

    num_notes = create_midi_item_with_notes(current_time_beats, final_phrase_notes_for_item, f"RuleOf3 - Varied Idea ({variation_type})")
    num_notes_created += num_notes
    current_time_beats += phrase_length_beats

    RPR.Undo_EndBlock2(0, f"Created Rule of Three Demonstration ({variation_type})", True)
    return f"Created '{track_name}' demonstration with 3 items ({bars*3} bars total) and {num_notes_created} notes at {bpm} BPM"

