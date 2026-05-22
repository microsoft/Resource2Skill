def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Bass",
    bpm: int = 95,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul/R&B Syncopated Bassline in the current REAPER project.
    Demonstrates the use of Octave jumps, Perfect 5ths, and Minor 7th passing tones.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (defaults to minor for the iv-i progression).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add and Configure ReaSynth (Warm Sub Bass) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 0: Volume, 2: Square, 3: Saw, 4: Triangle, 5: Attack, 8: Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.7)   # Volume slightly reduced
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)   # No square wave
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.05)  # Tiny bit of saw for bite
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.6)   # Triangle for warmth
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.02)  # Soft attack to prevent clicks
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.15)  # Smooth release

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory lookup for root note
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)

    # Minor progression: iv -> i (e.g. Fm -> Cm in C minor)
    # Relative to the root note: Degree 4 is +5 semitones, Degree 1 is +0 semitones
    chords = [5, 0] 
    
    # Base octave for bass (MIDI octave 1)
    base_midi = 24 + root_val

    def insert_note(start_sec, length_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + length_sec)
        # noSort is set to True, we will sort at the end
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    quarter_note_sec = 60.0 / bpm
    sixteenth_sec = quarter_note_sec / 4.0

    # === Step 5: Generate the Syncopated Bassline Pattern ===
    for bar in range(bars):
        chord_root_rel = chords[bar % len(chords)]
        bar_start_sec = bar * bar_length_sec
        
        # Calculate diatonic intervals for the current chord
        root_pitch = base_midi + chord_root_rel
        
        # Keep bass within reasonable low range (wrap down if getting too high)
        if root_pitch > 35:
            root_pitch -= 12
            
        octave_pitch = root_pitch + 12
        fifth_pitch = root_pitch + 7
        min7_pitch = root_pitch + 10  # Diatonic passing tone

        # 1. Root on beat 1.0 (duration: 3/16)
        insert_note(bar_start_sec + 0 * sixteenth_sec, 3 * sixteenth_sec, root_pitch, velocity_base)
        
        # 2. Octave jump on beat 2.75 (syncopated 16th upbeat)
        insert_note(bar_start_sec + 7 * sixteenth_sec, 1 * sixteenth_sec, octave_pitch, velocity_base * 0.8)
        
        # 3. Perfect 5th on beat 3.5 (8th note upbeat)
        insert_note(bar_start_sec + 10 * sixteenth_sec, 2 * sixteenth_sec, fifth_pitch, velocity_base * 0.85)
        
        # 4. Octave jump on beat 4.0 (downbeat)
        insert_note(bar_start_sec + 12 * sixteenth_sec, 1 * sixteenth_sec, octave_pitch, velocity_base * 0.9)
        
        # 5. Minor 7th passing tone on beat 4.5 (8th note upbeat, leading into next chord)
        insert_note(bar_start_sec + 14 * sixteenth_sec, 2 * sixteenth_sec, min7_pitch, velocity_base * 0.75)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with Neo-Soul syncopated bassline over {bars} bars at {bpm} BPM."
