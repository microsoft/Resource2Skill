def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a tight, modern rock/metal bassline that rhythmically locks 
    to a generated kick drum pattern, featuring velocity attenuation and octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created bass track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Determines the lowest bass note.
        scale: Scale type (not strictly used here as it's a root-pedal pattern, but kept for signature).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). Defaults to 110 to reduce VST harshness.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup for base note
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate lowest root pitch (Octave 1 for bass, e.g., C1 = 24)
    root_pitch = 24 + NOTE_MAP.get(key.capitalize(), 0)

    # Standard REAPER PPQ (Pulses Per Quarter Note)
    PPQ = 960 
    
    # Define a syncopated hard rock/metalcore rhythm in Quarter Note (QN) offsets
    # e.g., 0.0 = Beat 1, 1.0 = Beat 2, 0.75 = 16th note before Beat 2
    kick_rhythm_qn = [0.0, 0.75, 1.5, 2.0, 2.5, 3.5]
    snare_rhythm_qn = [1.0, 3.0] # Snares on 2 and 4

    # Note durations (staccato 16th notes for tightness)
    note_length_qn = 0.25 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Calculate lengths
    beats_per_bar = 4.0
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Get current track count to insert at the end
    track_idx = RPR.RPR_CountTracks(0)

    # === Step 2: Create Reference Drums Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", "Drums (Reference)", True)
    
    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, total_length_sec, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)

    # === Step 3: Create Locked Bass Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", track_name, True)

    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, total_length_sec, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)

    # === Step 4: Populate MIDI Data ===
    notes_created = 0

    for b in range(bars):
        bar_offset_qn = b * beats_per_bar

        # Insert Kicks and locking Bass notes
        for kq in kick_rhythm_qn:
            start_ppq = (bar_offset_qn + kq) * PPQ
            end_ppq = start_ppq + (note_length_qn * PPQ)

            # Drum Track: Kick (Pitch 36), Velocity 100
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 36, 100, False)

            # Bass Track: Lock to kick rhythm
            # Octave jump variation on the last hit of the measure (kq == 3.5)
            current_pitch = root_pitch + 12 if kq == 3.5 else root_pitch
            
            # Use the attenuated velocity_base (110) to avoid VST harshness
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, current_pitch, velocity_base, False)
            notes_created += 1

        # Insert Snares for groove context
        for sq in snare_rhythm_qn:
            start_ppq = (bar_offset_qn + sq) * PPQ
            end_ppq = start_ppq + (note_length_qn * PPQ)
            
            # Drum Track: Snare (Pitch 38), Velocity 100
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, 38, 100, False)

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(bass_take)

    # Optional: Load a basic synth on the bass track to hear the pitch if no VST is present
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)

    return f"Created '{track_name}' and 'Drums (Reference)' with {notes_created} perfectly locked bass notes over {bars} bars at {bpm} BPM (Key: {key})."
