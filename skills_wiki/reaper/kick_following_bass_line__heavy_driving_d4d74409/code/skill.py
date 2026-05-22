def create_kick_following_bass_line(
    project_name: str = "MyProject",
    bass_track_name: str = "Kick-Follow Bass",
    drum_track_name: str = "Simple Kicks",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Not directly used for single root note bass, but kept for context
    bars: int = 4,
    bass_velocity_base: int = 110,
    bass_note_duration_ratio: float = 0.9, # Ratio of 1/4 note length (e.g., 0.9 for slightly staccato)
    octave_variation_on_beat_3: bool = True, # As demonstrated in the tutorial
    octave_up_amount: int = 1, # How many octaves up for variation
    **kwargs,
) -> str:
    """
    Creates a bass line that follows a basic kick drum pattern (on 1, 2, 3, 4 beats).
    It also includes a simple kick drum track for context.

    Args:
        project_name: Project identifier (for logging).
        bass_track_name: Name for the created bass track.
        drum_track_name: Name for the created dummy drum track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        bass_velocity_base: Base MIDI velocity for bass notes (0-127).
        bass_note_duration_ratio: Ratio of the quarter note length for bass notes (e.g., 0.9 for slightly staccato).
        octave_variation_on_beat_3: Whether to play the bass note an octave up on beat 3 of each bar.
        octave_up_amount: The number of octaves to jump up for the variation.
        **kwargs: Additional overrides (not used in this skill but for future compatibility).

    Returns:
        Status string, e.g., "Created 'Kick-Follow Bass' with 16 notes and 'Simple Kicks' over 4 bars at 120 BPM"
    """

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Drum Track (for context) ===
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", drum_track_name, True)
    
    # Add ReaSamplOmatic5000 for drums (MIDI controlled)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000 (Cockos)", False, -1)
    # Kick drum is typically MIDI note 36 (C1) in many drum maps.
    kick_midi_note = 36 # Standard MIDI drum map for kick (C1)

    # Create MIDI Item for drums
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    RPR.RPR_MIDI_SetItemExtents(drum_item, 0.0, item_length) # Ensure MIDI item extends
    
    # Edit drum MIDI
    RPR.RPR_MIDI_DisableRecording(drum_take) # prevents undo point issues
    RPR.RPR_MIDI_Clear(drum_take)

    # Simple kick pattern: kick on every beat (1/4 notes)
    for bar in range(bars):
        for beat in range(beats_per_bar):
            position = bar * bar_length_sec + beat * (bar_length_sec / beats_per_bar)
            duration = (bar_length_sec / beats_per_bar) * 0.9 # Slightly shorter 1/4 note for punch
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, position, position + duration, 0, 100, kick_midi_note, True)
            
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Compact(drum_take, True)
    # RPR.RPR_MIDIEditor_OnCommand(RPR.RPR_MIDIEditor_CreateOrGetMIDIEditor(drum_item), 40049); # Close MIDI editor if open
    RPR.RPR_UpdateArrange()

    # === Step 3: Create Bass Track ===
    bass_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", bass_track_name, True)

    # Add ReaSynth to the bass track for a heavy tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth (Cockos)", False, -1)
    # Set a basic heavy bass patch for ReaSynth (parameter IDs are specific to ReaSynth)
    # Param 0: Oscillator 1 Waveform (0=sine, 0.25=saw, 0.5=square, 0.75=triangle)
    # Param 1: ADSR Attack, Param 2: ADSR Decay, Param 3: ADSR Sustain, Param 4: ADSR Release
    # Param 5: Oscillator 2 Waveform, Param 6: Osc 2 Octave, Param 7: Osc 2 Cents, Param 8: Osc 2 Volume
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.25) # Osc 1 Saw wave
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.05) # Short attack
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.2) # Medium decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.8) # High sustain
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.1) # Short release
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.5) # Osc 2 Square wave
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.5) # Osc 2 Octave (e.g., +1 octave from base)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 7, 0.005) # Osc 2 slightly detuned (cents)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 8, 0.7) # Osc 2 Volume

    # Calculate root MIDI note. C2 = MIDI 36. This ensures the key is respected.
    base_midi_note = NOTE_MAP.get(key.upper(), 0) + 36 # Default to C2 if key invalid

    # Create MIDI Item for bass
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    RPR.RPR_MIDI_SetItemExtents(bass_item, 0.0, item_length) # ensure MIDI item extends correctly
    
    # Edit bass MIDI
    RPR.RPR_MIDI_DisableRecording(bass_take)
    RPR.RPR_MIDI_Clear(bass_take)

    notes_inserted = 0
    # Note duration is a ratio of a quarter note
    note_duration_ticks = (bar_length_sec / beats_per_bar) * bass_note_duration_ratio

    for bar in range(bars):
        for beat in range(beats_per_bar):
            position = bar * bar_length_sec + beat * (bar_length_sec / beats_per_bar)
            
            current_midi_note = base_midi_note
            current_velocity = bass_velocity_base

            # Apply octave variation on beat 3 if enabled
            if octave_variation_on_beat_3 and beat == 2: # Beat 3 (index 2)
                current_midi_note += (12 * octave_up_amount) # Jump up by the specified octaves
                # Reduce velocity slightly for higher notes for realism, as demonstrated in the tutorial
                current_velocity = int(bass_velocity_base * 0.9) 
            
            # Insert the bass note
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, position, position + note_duration_ticks, 0, current_velocity, current_midi_note, True)
            notes_inserted += 1

    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Compact(bass_take, True)
    # RPR.RPR_MIDIEditor_OnCommand(RPR.RPR_MIDIEditor_CreateOrGetMIDIEditor(bass_item), 40049); # Close MIDI editor if open
    RPR.RPR_UpdateArrange()

    return f"Created '{bass_track_name}' with {notes_inserted} notes and '{drum_track_name}' over {bars} bars at {bpm} BPM"
