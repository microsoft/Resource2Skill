import reaper_python as RPR

def create_kick_sync_drop_bass_line(
    project_name: str = "MyProject",
    track_name: str = "Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Not strictly used for root bass, but kept for consistency
    bars: int = 4,
    velocity_base: int = 110, # Adjusted as per tutorial's preference
    root_octave: int = 3, # C3 as a common bass root
    staccato_length_factor: float = 0.5, # For shorter notes
    quarter_note_length_factor: float = 0.9, # Slightly shorter than full for definition
    **kwargs,
) -> str:
    """
    Creates a kick-synchronized bass line in drop tuning style in the current REAPER project.
    The bass line primarily follows a simple kick pattern, with some rhythmic and octave variations.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). This will be the main bass note.
        scale: Scale type (major, minor, etc.). Not directly used for root bass lines, but kept.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), adjusted for less harshness.
        root_octave: The octave for the main bass root note (e.g., 3 for C3).
        staccato_length_factor: Factor to shorten note length for staccato feel (e.g., 0.5 for 1/8th note).
        quarter_note_length_factor: Factor to shorten quarter notes slightly (e.g., 0.9).
        **kwargs: Additional overrides (not used in this specific pattern).

    Returns:
        Status string, e.g., "Created 'Bass' with 16 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    if key not in NOTE_MAP:
        return f"Error: Key '{key}' not recognized. Please use standard note names (C, C#, D, etc.)."

    root_midi_note = NOTE_MAP[key] + (root_octave * 12)
    
    # === Step 1: Set Tempo (if not already set globally) ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This might affect other items, so keep commented for additive

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth for a basic bass sound) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Optional: set a basic bass preset on ReaSynth
    # RPR.RPR_TrackFX_SetPreset(track, 0, "Basic Bass") # Requires a preset named "Basic Bass"

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", RPR.RPR_GetCursorPosition())
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    midi_take = RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length) # Get/create MIDI take
    
    RPR.RPR_MIDI_Clear(midi_take) # Clear any default notes
    
    num_notes = 0

    # Define the bass pattern (based on the tutorial's final example played at 4:50)
    # Kick pattern is roughly on beats 1 and 3 of each bar.
    # Pattern:
    # Bar 1: Root (1/4), Root (1/4)
    # Bar 2: Root (1/8), Root (1/8) - staccato
    # Bar 3: Root (1/4), Root+Octave (1/8)
    # Bar 4: Root (1/8), Root+Octave (1/8) - staccato

    midi_notes_to_insert = [] # (start_time_beats, duration_beats, pitch, velocity)

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar

        # Beat 1 (always root)
        midi_notes_to_insert.append((bar_start_beat, 1 * quarter_note_length_factor, root_midi_note, velocity_base))
        
        # Beat 3 (root or octave up, with varied length)
        if bar % 4 == 0: # Bar 1 and 5...
            midi_notes_to_insert.append((bar_start_beat + 2, 1 * quarter_note_length_factor, root_midi_note, velocity_base))
        elif bar % 4 == 1: # Bar 2 and 6... (staccato)
            midi_notes_to_insert.append((bar_start_beat + 2, 1 * staccato_length_factor, root_midi_note, velocity_base))
        elif bar % 4 == 2: # Bar 3 and 7... (octave up, staccato)
            midi_notes_to_insert.append((bar_start_beat + 2, 1 * staccato_length_factor, root_midi_note + 12, velocity_base))
        elif bar % 4 == 3: # Bar 4 and 8... (octave up, staccato)
            midi_notes_to_insert.append((bar_start_beat + 2, 1 * staccato_length_factor, root_midi_note + 12, velocity_base))
            
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length) # Ensure MIDI item is correctly sized
    RPR.RPR_MIDI_SetPPQ(midi_take, RPR.RPR_MIDI_GetPPQ(midi_take)) # Set default PPQ if needed

    # Insert notes into the MIDI take
    RPR.RPR_MIDI_DisableGrid(midi_take) # Disable grid for more precise placement
    for start_beat, duration_beats, pitch, velocity in midi_notes_to_insert:
        RPR.RPR_MIDI_InsertNote(
            midi_take,
            False, # selected
            True,  # no_edit
            start_beat * RPR.RPR_MIDI_GetPPQ(midi_take) / beats_per_bar, # start_tick
            (start_beat + duration_beats) * RPR.RPR_MIDI_GetPPQ(midi_take) / beats_per_bar, # end_tick
            0, # channel
            velocity, # velocity
            pitch # pitch
        )
        num_notes += 1
    RPR.RPR_MIDI_EnableGrid(midi_take) # Re-enable grid if it was disabled
    RPR.RPR_MIDI_Sort(midi_take) # Sort notes after insertion
    RPR.RPR_MIDI_Commit(midi_take) # Commit MIDI changes

    return f"Created '{track_name}' with {num_notes} notes over {bars} bars at {bpm} BPM."

