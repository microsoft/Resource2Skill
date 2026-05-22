def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Keys",
    bpm: int = 85,
    key: str = "Eb",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Creates a Neo-Soul/Gospel extended chord progression (v7 - VImaj9 - V7#5 - i7 - iv11)
    similar to the Ripchord presets showcased in the tutorial. Includes a humanized strum effect.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (80-90 recommended).
        key: Root note (e.g., Eb).
        scale: Scale type (defaults to minor context for this specific progression).
        bars: Number of bars (generates a 4-bar loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Base dictionary for notes to MIDI value (Octave 0)
    NOTE_MAP = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
        "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
    }

    # Extract root pitch (Default Eb -> 3). We set the base octave to 2 (36) for rich low-mid chords.
    root_pitch = NOTE_MAP.get(key.capitalize(), 3)
    base_note = 36 + root_pitch 

    # Define the Neo-Soul progression based on the tutorial's Ripchord preset
    # Format: (semitones_from_root, [chord_intervals_in_semitones], duration_in_beats)
    progression = [
        # Bar 1: v7 -> VImaj9
        (7, [0, 3, 7, 10], 2.0),           # v7 (e.g., Bbm7)
        (8, [0, 4, 7, 11, 14], 2.0),       # VImaj9 (e.g., Bmaj9 / Cbmaj9)
        # Bar 2: V7#5 (Turnaround)
        (7, [0, 4, 8, 10], 4.0),           # V7#5 (e.g., Bb7#5)
        # Bar 3: i7 (Tonic)
        (0, [0, 3, 7, 10], 4.0),           # i7 (e.g., Ebm7)
        # Bar 4: iv11 (Subdominant extension)
        (5, [0, 3, 7, 10, 17], 4.0),       # iv11 (e.g., Abm11)
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_beats = 16 # 4-bar loop
    total_length_sec = (60.0 / bpm) * total_beats
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate MIDI Notes ===
    current_beat = 0.0
    sec_per_beat = 60.0 / bpm
    strum_delay_sec = 0.012  # 12ms delay per note for the "humanized" feel
    
    note_count = 0

    # Repeat progression to fill requested bars (chunked in 4-bar blocks)
    loops = max(1, bars // 4)
    
    for loop in range(loops):
        for chord in progression:
            root_offset, intervals, duration_beats = chord
            
            chord_root_pitch = base_note + root_offset
            
            # Start and end time for the entire chord block
            chord_start_time = current_beat * sec_per_beat
            # Leave a tiny gap before the next chord
            chord_end_time = (current_beat + duration_beats) * sec_per_beat - 0.05 
            
            # Add each note in the chord with a slight humanized strum offset
            for i, interval in enumerate(intervals):
                pitch = chord_root_pitch + interval
                # Keep pitch in valid MIDI range
                pitch = max(0, min(127, pitch))
                
                note_start_time = chord_start_time + (i * strum_delay_sec)
                
                # Convert seconds to PPQ (MIDI ticks)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_end_time)
                
                # Velocity variation for humanization
                vel = velocity_base - (i * 3) # Higher notes slightly softer
                vel = max(1, min(127, vel))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
                note_count += 1
                
            current_beat += duration_beats

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument & FX Chain ===
    
    # 1. ReaSynth (Electric Piano / Warm Pad style setup)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.4)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.1)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.7)  # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.8)  # Sine mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.05) # Attack (soft)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.6)  # Release (let chords ring)

    # 2. ReaEQ (Lowpass to remove harsh digital highs and make it warm)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 (High shelf/pass usually). We'll gently roll off highs by dropping gain on high bands.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 8, -12.0) # Lower gain on highest band to warm up the tone

    # 3. ReaDelay (Subtle widening)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, 0.05) # Very low wet mix
    
    # 4. ReaVerbate (Lush room space)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.3)   # Wet mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.8)   # Dry mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.7)   # Room size

    return f"Created '{track_name}' with {note_count} humanized Neo-Soul notes over {loops*4} bars at {bpm} BPM in {key} minor."
