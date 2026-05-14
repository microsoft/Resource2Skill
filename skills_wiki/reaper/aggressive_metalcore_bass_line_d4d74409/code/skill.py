import reaper_python as RPR

def create_aggressive_metalcore_bass_line(
    project_name: str = "MyProject",
    track_name: str = "Aggro Bass",
    bpm: int = 180, # Metalcore often faster
    key: str = "A", # Root note (C, C#, D, ..., B). 'A' for Drop A example.
    octave: int = 1, # Base octave for the root note (e.g., C1 is MIDI 36, C2 is MIDI 48)
    bars: int = 4,
    velocity_base: int = 110, # Suggested by tutorial to reduce "harshness"
    add_octave_jump: bool = True, # Adds a higher octave note to the pattern
    note_duration_beats: float = 0.45, # Slightly less than 0.5 (eighth note) for staccato feel
    **kwargs,
) -> str:
    """
    Create an aggressive metalcore bass line in the current REAPER project.
    The bass line reinforces the rhythmic pulse and harmonically supports
    the root notes, incorporating velocity variation and optional octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        octave: Base octave for the root note (e.g., C1 = MIDI 36, C2 = MIDI 48).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        add_octave_jump: If True, adds an occasional octave higher note.
        note_duration_beats: Duration of individual MIDI notes in beats (e.g., 0.45 for staccato 8th).
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'Aggro Bass' with 32 notes over 4 bars at 180 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # Ensure valid velocity
    velocity_base = max(0, min(127, velocity_base))

    # Calculate MIDI note for the root
    base_midi_pitch = NOTE_MAP.get(key, 0) + (octave * 12)

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add ReaSynth for a basic bass tone ===
    # This approximates the functionality of Gen Bass, which is a commercial VSTi.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    fx_idx = RPR.RPR_TrackFX_GetByName(track, "ReaSynth", False)
    if fx_idx != -1:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5) # Osc 1 Waveform: Saw
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.2) # Env 1 Release: Punchier bass
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.7) # Env 1 Sustain: Moderate
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.3) # Filter 1 Cutoff: Lower for bass

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at beginning of project
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats * (60.0 / bpm)) # Convert beats to seconds
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_MIDI_SetMediaItemTake_Source(take, RPR.MIDI_CreateNewMIDIItemTake(0), False) # Create new MIDI source

    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length_beats)
    
    # Start MIDI editing
    RPR.RPR_MIDI_DisableSort(take)

    current_beat = 0.0
    note_count = 0

    # Pattern definition: (relative_pitch, velocity_offset_from_base, is_octave_jump_candidate)
    # Relative pitches: 0 = root, -2 = minor 7th below (e.g., G if root is A), -3 = minor 6th below (e.g., F# if root is A)
    # This reflects the visual pattern from the video's example (05:40) in a generalized way.
    four_bar_pattern_sequence = [
        # Bar 1 (all root notes)
        (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False), 
        (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, True), # Last note in bar 1 is candidate for octave jump
        # Bar 2 (all root notes)
        (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False), 
        (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
        # Bar 3 (melodic variation)
        (0, 0, False), (0, 0, False), (-2, 0, False), (-2, 0, True), # Root, Root, G, G (candidate for octave jump)
        (-3, 0, False), (-3, 0, False), (0, 0, False), (0, 0, False), # F#, F#, Root, Root
        # Bar 4 (another melodic variation)
        (-2, 0, False), (-2, 0, True), (0, 0, False), (0, 0, False), # G, G (candidate for octave jump), Root, Root
        (-3, 0, False), (-3, 0, False), (-2, 0, False), (-2, 0, False) # F#, F#, G, G
    ]

    for bar_segment in range(bars // len(four_bar_pattern_sequence) * 8 if bars >= 4 else 1): # Adjust loop for potentially longer bars
        for i, (relative_pitch, velocity_offset, is_octave_jump_candidate) in enumerate(four_bar_pattern_sequence):
            # Calculate actual MIDI pitch relative to the chosen key and base octave
            midi_pitch = base_midi_pitch + relative_pitch
            
            # Apply octave jump if enabled and for specific pattern points
            if add_octave_jump and is_octave_jump_candidate:
                midi_pitch += 12

            # Ensure pitch is within a reasonable bass range (e.g., MIDI 24-60)
            midi_pitch = max(24, min(60, midi_pitch))

            # Calculate velocity
            velocity = max(1, min(127, velocity_base + velocity_offset))

            # Insert MIDI note (pos, end, sel, muted, pitch, vel)
            RPR.RPR_MIDI_InsertNote(take, False, False, current_beat, current_beat + note_duration_beats, False, midi_pitch, velocity, False)
            note_count += 1
            current_beat += 0.5 # Advance by an eighth note

    # End MIDI editing
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_MIDI_DisableSort(take, False)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in key of {key}{octave}"

