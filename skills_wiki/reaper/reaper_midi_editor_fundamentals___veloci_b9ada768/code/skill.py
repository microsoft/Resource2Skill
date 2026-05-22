def create_midi_editor_fundamentals_demo(
    project_name: str = "MIDI_Editor_Demo",
    track_name: str = "Piano_Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major", # The example shows C major notes
    bars: int = 4,
    velocity_base: int = 80,
    **kwargs,
) -> str:
    """
    Create a demonstration of REAPER MIDI Editor fundamentals including
    track creation, MIDI item insertion, chord progression, and velocity automation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Piano_Demo' with 16 notes over 4 bars at 120 BPM"
    """
    import reaper_python as RPR

    # Music theory lookup tables (simplified for common scales/chords)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        # Add other scales if needed, though C major is implied by the demo
    }
    
    # MIDI note numbers for a C major chord starting at C2 (MIDI 48)
    # C2, E2, G2, C3 (as shown in the video)
    C_MAJOR_CHORD = [48, 52, 55, 60] 
    
    # Calculate root offset based on key
    root_offset = NOTE_MAP.get(key, 0)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add VSTi (Placeholder for Grand Piano) ===
    # The tutorial uses a specific 3rd party VSTi. We'll use ReaSynth as a generic piano-like placeholder.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    item_length = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_GetActiveTake(item)
    
    # Ensure the MIDI item is editable
    RPR.RPR_MIDI_SetItemExtents(take, 0, 0) # Create empty MIDI data

    # Begin editing MIDI directly
    RPR.RPR_MIDI_DisableGridSnap(take) # Temporarily disable snap for fine-tuning
    
    notes_created = 0
    midi_notes = [] # Store notes to apply velocity changes later

    # === Step 5: Add C Major Chord and Automate Velocities ===
    # Simulate adding chords across the bars with varied velocities
    for bar in range(bars):
        position = float(bar * beats_per_bar) # Start of each bar
        
        # Simple velocity automation: gradually increase then decrease
        # Scale velocity based on bar position to simulate manual drag
        velocity_modifier = (bar / (bars - 1)) if bars > 1 else 0.5
        current_velocity = int(velocity_base + (velocity_base * velocity_modifier * 0.5)) # Range ~80-120 if base is 80
        current_velocity = max(10, min(127, current_velocity)) # Clamp to valid MIDI velocity range

        for i, midi_note_number in enumerate(C_MAJOR_CHORD):
            # Apply root offset to the base MIDI notes for the selected key
            actual_midi_note = midi_note_number + root_offset
            
            # Note duration: 1 quarter note (1 beat) for simplicity, matching video example for chords
            note_length_beats = 1.0 
            
            # RPR.MIDI_InsertNote(take, selected, muted, start_beat, end_beat, channel, no_snap_pitch, velocity, no_snap_len)
            # The last two arguments (no_snap_pitch, no_snap_len) are boolean.
            # We want to snap to grid for timing, but not necessarily for pitch (if moved later).
            # The velocity is adjusted later via SetNoteVel.
            note_idx = RPR.RPR_MIDI_InsertNote(take, -1, 0, 0, position, position + note_length_beats, 0, 0, 0, current_velocity, False, False)
            
            # RPR_MIDI_SetNoteVel() takes note_idx, velocity (0-127), and ignore_loop_boundaries
            RPR.RPR_MIDI_SetNoteVel(take, note_idx, current_velocity, True)

            notes_created += 1

    RPR.RPR_MIDI_DisableGridSnap(take) # Re-enable snap after editing
    RPR.RPR_UpdateItemInProject(item) # Update the item in the project view

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM with basic velocity automation."


