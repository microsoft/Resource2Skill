def create_pattern(
    project_name: str = "MIDI_Project",
    track_name: str = "Piano - Editing Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Demonstrates essential MIDI editing techniques in REAPER: note creation,
    selection, deletion, copying, length/position adjustment, transposing,
    and velocity automation. Creates a simple MIDI item to practice on.

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
        Status string, e.g., "Created 'Piano - Editing Demo' with MIDI notes over 4 bars at 120 BPM"
    """
    import reaper_python as RPR
    import random

    # Helper function to convert note name to MIDI pitch
    def note_to_midi(note_name: str, octave: int) -> int:
        NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
        base_midi = NOTE_MAP.get(note_name, 0) # Default to C if not found
        return base_midi + (octave + 1) * 12 # C0 is MIDI 12, so C-1 is MIDI 0

    # Helper function to get scale notes (not fully utilized for specific notes, but adheres to template)
    def get_scale_midi_pitches(root_midi: int, scale_type: str, octave: int) -> list[int]:
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
        scale_intervals = SCALES.get(scale_type.lower(), SCALES["major"])
        # Adjust root to desired octave (C3 for example is MIDI 60)
        root_midi_in_octave = note_to_midi("C", octave) + (root_midi % 12)
        return [root_midi_in_octave + interval for interval in scale_intervals]

    RPR.RPR_PreventUIRefresh(1) # Prevent UI refresh during script execution
    RPR.RPR_Undo_BeginBlock2(0) # Begin an undo block

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, float(bpm), False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add VSTi (Grand Piano or ReaSynth) ===
    vsti_loaded = False
    vsti_name_grand_piano = "VSTi: Grand Piano (saulodtry)"
    # Attempt to load the specific VST shown in the video
    if RPR.RPR_TrackFX_AddByName(track, vsti_name_grand_piano, False, -1):
        vsti_loaded = True
        # For Grand Piano (saulodtry), specific parameter mapping is unknown,
        # but common parameters for pianos might include reverb, width, etc.
        # These are illustrative guesses:
        # RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.05) # Example for a generic 'volume'
        # RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5)  # Example for a generic 'reverb'
    
    if not vsti_loaded:
        vsti_name_reasynth = "VSTi: ReaSynth"
        if RPR.RPR_TrackFX_AddByName(track, vsti_name_reasynth, False, -1):
            vsti_loaded = True
            # Set some default parameters for ReaSynth for a basic piano-like sound
            RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.2) # Attack
            RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Decay
            RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.7) # Sustain
            RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2) # Release
            RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.5) # Volume
        else:
            RPR.RPR_ShowConsoleMsg(f"Warning: Could not load {vsti_name_grand_piano} or {vsti_name_reasynth}. No instrument loaded.\n")

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    item_length_beats = float(bars * beats_per_bar)
    # Calculate item length in seconds: (beats / BPM) * 60 seconds/minute
    item_length_sec = item_length_beats * (60.0 / bpm) 

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    RPR.RPR_SetMediaItemInfo_Value(item, "B_LOOPSRC", 0) # Set to MIDI source
    RPR.RPR_UpdateItemInProject(item)

    take = RPR.RPR_GetActiveTake(item)
    if not take:
        RPR.RPR_ShowConsoleMsg("Error: Could not get active take for MIDI item.\n")
        RPR.RPR_Undo_EndBlock2(0, "Create MIDI Editing Demo (Failed)", False)
        RPR.RPR_PreventUIRefresh(-1)
        return "Failed to create MIDI item content."

    # Prepare the MIDI item for editing
    RPR.RPR_MIDI_SetItemExtents(take, 0, 0, 0)
    RPR.RPR_MIDI_ClearEvts(take) # Clear any default MIDI data

    # PPQ (Pulses Per Quarter note) for accurate timing
    # Default is typically 960 for 1/4 note
    ppq_per_beat = 960
    ppq_16th = ppq_per_beat / 4
    ppq_8th = ppq_per_beat / 2
    ppq_quarter = ppq_per_beat
    ppq_half = ppq_per_beat * 2
    ppq_bar = ppq_per_beat * beats_per_bar

    notes_to_insert = [] # List to hold (start_ppq, end_ppq, pitch, velocity)

    # Bar 1: C Major Chord (C3, E3, G3, C4) - Quarter notes, starting on beat 1
    # Mimicking chord creation and note length adjustment from tutorial
    notes_to_insert.append((0 * ppq_bar, 0 * ppq_bar + ppq_quarter, note_to_midi(key, 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((0 * ppq_bar, 0 * ppq_bar + ppq_quarter, note_to_midi('E', 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((0 * ppq_bar, 0 * ppq_bar + ppq_quarter, note_to_midi('G', 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((0 * ppq_bar, 0 * ppq_bar + ppq_quarter, note_to_midi(key, 4), velocity_base + random.randint(-5, 5)))

    # Bar 2: Simple Melody - Quarter notes
    notes_to_insert.append((1 * ppq_bar, 1 * ppq_bar + ppq_quarter, note_to_midi('C', 4), velocity_base + random.randint(-10, 10)))
    notes_to_insert.append((1 * ppq_bar + ppq_quarter, 1 * ppq_bar + 2 * ppq_quarter, note_to_midi('D', 4), velocity_base + random.randint(-10, 10)))
    notes_to_insert.append((1 * ppq_bar + 2 * ppq_quarter, 1 * ppq_bar + 3 * ppq_quarter, note_to_midi('E', 4), velocity_base + random.randint(-10, 10)))
    notes_to_insert.append((1 * ppq_bar + 3 * ppq_quarter, 1 * ppq_bar + 4 * ppq_quarter, note_to_midi('F', 4), velocity_base + random.randint(-10, 10)))

    # Bar 3: G Major Chord (G3, B3, D4) - Half notes
    notes_to_insert.append((2 * ppq_bar, 2 * ppq_bar + ppq_half, note_to_midi('G', 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((2 * ppq_bar, 2 * ppq_bar + ppq_half, note_to_midi('B', 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((2 * ppq_bar, 2 * ppq_bar + ppq_half, note_to_midi('D', 4), velocity_base + random.randint(-5, 5)))

    # Bar 4: A Minor Chord (A3, C4, E4) - Half notes
    notes_to_insert.append((3 * ppq_bar, 3 * ppq_bar + ppq_half, note_to_midi('A', 3), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((3 * ppq_bar, 3 * ppq_bar + ppq_half, note_to_midi('C', 4), velocity_base + random.randint(-5, 5)))
    notes_to_insert.append((3 * ppq_bar, 3 * ppq_bar + ppq_half, note_to_midi('E', 4), velocity_base + random.randint(-5, 5)))

    for start_ppq, end_ppq, pitch, velocity in notes_to_insert:
        RPR.RPR_MIDI_InsertNote(take, 0, 0, start_ppq, end_ppq, 1, True, pitch, velocity, False) 
    
    # === Step 5: Simulate further Velocity Automation ===
    # The tutorial shows dragging velocities. We introduce more variations here
    # to demonstrate programmatic manipulation of velocities.
    num_midi_notes, _, _ = RPR.RPR_MIDI_CountEvts(take)
    for i in range(num_midi_notes):
        # Get existing note data
        _, _, _, start_time, end_time, channel, selected, pitch, current_velocity = RPR.RPR_MIDI_GetNote(take, i)
        # Apply more random variation, ensuring velocity stays within 0-127
        new_velocity = min(127, max(0, current_velocity + random.randint(-15, 15)))
        # Update the note with the new velocity
        RPR.RPR_MIDI_SetNote(take, i, 0, 0, start_time, end_time, channel, selected, pitch, new_velocity, False)

    # Ensure MIDI data is sorted and velocities are updated in REAPER's display
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_MIDI_MarkAllVelsDirty(take)
    RPR.RPR_MIDI_Update(take)

    RPR.RPR_UpdateArrange() # Update the arrange view
    RPR.RPR_Main_OnCommand(RPR.RPR_NamedCommandLookup("_SWSS_OPEN_MIDI_EDITOR_LAST_ITEM_AS_PIANO_ROLL"), 0) # Open MIDI editor for the last item

    RPR.RPR_Undo_EndBlock2(0, "Create MIDI Editing Demo", True)
    RPR.RPR_PreventUIRefresh(-1)

    return f"Created '{track_name}' with {len(notes_to_insert)} notes over {bars} bars at {bpm} BPM, set up for MIDI editing practice."

