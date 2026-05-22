import reaper_python as RPR

def create_rhythmic_arpeggiated_synth_layer(
    project_name: str = "MyProject",
    track_name: str = "ArpeggioSynth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    start_octave: int = 3, # C3
    end_octave: int = 4,   # C4
    **kwargs,
) -> str:
    """
    Create a rhythmic, arpeggiated synth layer using Massive X, Reason Rack Plugin, and ReaEQ.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        start_octave: Starting octave for the arpeggio (e.g., 3 for C3).
        end_octave: Ending octave for the arpeggio (e.g., 4 for C4).
        **kwargs: Additional overrides (not used in this skill).

    Returns:
        Status string, e.g., "Created 'ArpeggioSynth' with 32 notes over 4 bars at 120 BPM"
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

    # === Step 1: Set Tempo (if different from current project tempo) ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This is a project-level change, might not be desired for a skill.
                                          # Assuming global BPM is already set or will be handled by orchestrator.

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add VST Instruments (placeholders, manual preset loading required) ===
    # Native Instruments Massive X
    RPR.RPR_TrackFX_AddByName(track, "Massive X (Native Instruments)", False, -1)
    # Reason Rack Plugin
    RPR.RPR_TrackFX_AddByName(track, "Reason Rack Plugin (Reason Studios)", False, -1)

    # === Step 4: Add ReaEQ for filtering ===
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)
    # Configure ReaEQ for a high-pass filter
    # ReaEQ parameter mapping (approximate based on common UI/docs):
    # Parameter 0: Band 1 Bypass (0=On, 1=Off)
    # Parameter 1: Band 1 Gain
    # ...
    # Parameter 20: Band 5 Bypass
    # Parameter 21: Band 5 Gain
    # Parameter 22: Band 5 Freq
    # Parameter 23: Band 5 Q
    # Parameter 24: Band 5 Type (1=HPF)
    
    # Enable Band 5
    RPR.RPR_TrackFX_SetParam(track, 2, 20, 0.0) # Band 5 Bypass OFF
    # Set Band 5 type to High Pass Filter (Type ID for HPF is often 1 or similar)
    # This might vary slightly based on ReaEQ version, but 1 is common for HPF
    RPR.RPR_TrackFX_SetParam(track, 2, 24, 1.0) # Set Band 5 Type to HPF
    # Set Band 5 Frequency to 150 Hz (normalized 0-1 range)
    # ReaEQ Freq is log-scaled. 150Hz on a 20Hz-20kHz scale is roughly log10(150/20) / log10(20000/20) = 0.35
    freq_norm = (RPR.RPR_log(150.0) - RPR.RPR_log(20.0)) / (RPR.RPR_log(20000.0) - RPR.RPR_log(20.0))
    RPR.RPR_TrackFX_SetParam(track, 2, 22, freq_norm) # Set Band 5 Freq to 150Hz
    # Set Band 5 Q (ReaEQ default Q for HPF is often 0.707 or a fixed value, leave as default for now if not specified)
    # If the video clearly showed a different Q, it would be added here.

    # === Step 5: Create MIDI Item with an arpeggiated pattern ===
    tempo_ratio = bpm / 120.0 # Adjust timing based on BPM
    seconds_per_beat = 60.0 / bpm
    
    item_position = 0.0
    item_length = bars * 4 * seconds_per_beat # 4 beats per bar
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_position)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_AllocTemporary(item, True)) # Make it a new MIDI source

    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_SetItemExtents(midi_take, item_length, item_position)

    root_midi_note = NOTE_MAP.get(key, 0) # Default to C if key not found
    scale_intervals = SCALES.get(scale, SCALES["major"]) # Default to major scale
    
    # Generate an ascending arpeggio (16th notes)
    notes_per_bar = 16 # for 1/16th notes
    notes_to_generate = bars * notes_per_bar
    note_duration_beats = 0.25 # 1/16th note
    note_duration_seconds = note_duration_beats * seconds_per_beat

    current_time_beats = 0.0
    note_count = 0

    for _ in range(notes_to_generate):
        # Calculate scale degree and octave dynamically
        scale_degree_index = note_count % len(scale_intervals)
        octave_offset = (note_count // len(scale_intervals)) 
        
        # Adjust octave to stay within start_octave and end_octave range
        base_midi_note = root_midi_note + (start_octave * 12)
        midi_note = base_midi_note + scale_intervals[scale_degree_index] + (octave_offset * 12)

        # Simple wrap-around if it exceeds the end_octave
        if midi_note >= (root_midi_note + (end_octave * 12) + 12): # Check for next octave after end_octave
             midi_note -= (end_octave - start_octave + 1) * 12 # Wrap back to start_octave
             
        # Ensure minimum pitch
        if midi_note < (root_midi_note + (start_octave * 12)):
            midi_note = (root_midi_note + (start_octave * 12)) + scale_intervals[scale_degree_index] # Reset to lowest note in scale if somehow too low

        RPR.RPR_MIDI_InsertNote(midi_take,
                                 False, # Selected
                                 False, # Muted
                                 current_time_beats, # Start position in beats
                                 current_time_beats + note_duration_beats, # End position in beats
                                 velocity_base, # Velocity
                                 midi_note, # Pitch
                                 False # No slip/slide
                                )
        current_time_beats += note_duration_beats
        note_count += 1
    
    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_MarkAllNotes(midi_take, False)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' track with Massive X, Reason Rack Plugin, ReaEQ, and an arpeggiated MIDI item ({note_count} notes over {bars} bars at {bpm} BPM). Remember to manually load VST presets ('Retro Phish' for Massive X, 'Beat Map/Clockwork dispatch' for Reason Rack Plugin)."


