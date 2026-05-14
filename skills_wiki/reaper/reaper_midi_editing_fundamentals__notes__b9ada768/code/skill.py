import reaper_python as RPR

def create_midi_editing_fundamentals(
    project_name: str = "MyProject",
    track_name: str = "MIDI Notes Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    octave: int = 3, # Default octave for the base notes
    **kwargs,
) -> str:
    """
    Creates a new track with a MIDI item demonstrating basic MIDI editing fundamentals:
    notes, a simple chord, and varied velocities.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        octave: MIDI octave for the root of the notes (e.g., 3 for C3).
        **kwargs: Additional overrides (not used in this skill but for future expansion).

    Returns:
        Status string, e.g., "Created 'MIDI Notes Demo' with 16 notes over 4 bars at 120 BPM"
    """
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

    # Ensure key and scale are valid
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Choose from {list(NOTE_MAP.keys())}"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Choose from {list(SCALES.keys())}"

    root_midi = NOTE_MAP[key] + (octave * 12)
    current_scale = SCALES[scale]

    # === Step 1: Set Tempo ===
    # Note: RPR_SetCurrentBPM changes global project BPM.
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) ===
    # The tutorial used "VSTi: Grand Piano (saudade.lv2)", which is not stock.
    # Using ReaSynth as a general VSTi for MIDI playback.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Could set a basic sound for ReaSynth if a known preset exists or params are provided.
    # For now, default ReaSynth sound is used.

    # === Step 4: Create MIDI Item ===
    # Timebase: REAPER's time unit is usually in quarter notes, 1.0 = 1 quarter note.
    # For a 4/4 bar: 4.0 quarter notes.
    quarter_note_len = 60.0 / bpm
    bar_length_qn = 4.0 # 4 quarter notes per bar (4/4 time)
    item_length_qn = bar_length_qn * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_qn * quarter_note_len) # Length in seconds

    take = RPR.RPR_AddTakeToMediaItem(item)
    if not take:
        RPR.RPR_DeleteTrack(track)
        return "Error: Could not add take to media item."

    RPR.RPR_MIDI_SetItemExtents(item, 0, item_length_qn) # Set item length in quarter notes

    # Get the MIDI take for editing
    midi_take = RPR.RPR_MIDI_GetTake(take)
    if not midi_take:
        RPR.RPR_DeleteTrack(track)
        return "Error: Could not get MIDI take."

    RPR.RPR_MIDI_BeginEdit(midi_take)

    # === Step 5: Insert Notes (Melody & Chord) and Adjust Velocities ===
    note_count = 0
    # Simple melody (like the video's double-click examples)
    # Using notes from the selected scale
    melody_notes = [current_scale[0], current_scale[2], current_scale[4], current_scale[5]] # C, E, G, F (in C major)
    melody_octave_offset = 12 # One octave higher than base

    for i in range(bars):
        # Melody part
        for j, scale_degree_offset in enumerate(melody_notes):
            pos_qn = float(i * bar_length_qn) + (j * 0.5) # Each note 1/8th note apart
            note_len_qn = 0.4 # Slightly less than 1/8th note for separation (staccato feel)
            midi_note = root_midi + melody_octave_offset + scale_degree_offset

            # Velocity variation for realism (as shown in tutorial)
            velocity = velocity_base + (j % 2 * 10) - 5 # Alternating velocity slightly
            
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, pos_qn, pos_qn + note_len_qn, 0, midi_note, velocity, False)
            note_count += 1

        # Simple chord (like the video's C chord example)
        # Root position C major chord in the base octave
        if i % 2 == 0: # Place a chord every other bar
            chord_pos_qn = float(i * bar_length_qn) + 2.0 # Start mid-bar
            chord_len_qn = 1.5 # Longer duration chord
            chord_pitches = [root_midi, root_midi + current_scale[2], root_midi + current_scale[4], root_midi + 12] # C3, E3, G3, C4
            
            for k, pitch in enumerate(chord_pitches):
                # More velocity variation for chords
                velocity = velocity_base - (k * 5) + 15 # Descending velocity for chord notes
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, chord_pos_qn, chord_pos_qn + chord_len_qn, 0, pitch, velocity, False)
                note_count += 1

    RPR.RPR_MIDI_EndEdit(midi_take)

    # === Step 6: Select the created MIDI item and open MIDI editor for demonstration ===
    RPR.RPR_SetMediaItemSelected(item, True)
    RPR.RPR_Main_OnCommand(40866, 0) # View: Open item in MIDI editor

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"

