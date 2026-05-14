def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered from 127 to reduce harshness as per tutorial
    **kwargs,
) -> str:
    """
    Creates a modern rock/metal bass MIDI pattern that locks to a syncopated kick rhythm
    and utilizes 12th-fret octave jumps to follow guitar riffs.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). 
        scale: Scale type (defines the harmonic context, though this focuses on the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (110 recommended to avoid virtual bass harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Note mapping (Starting low to simulate drop tuning, e.g., C1)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave for metal bass (MIDI note 24 is C1)
    root_midi_pitch = NOTE_MAP.get(key.capitalize(), 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_length = 60.0 / bpm
    bar_length_sec = qn_length * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Cursor to 0
    RPR.RPR_SetEditCurPos(0.0, True, False)
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define a 1-bar syncopated metal rhythm matching a typical kick pattern
    # Format: (start_16th_index, length_in_16ths, is_octave_up)
    # The 'is_octave_up' represents jumping to the 12th fret on the guitar
    metal_riff_grid = [
        (0,  1, False), # Downbeat, low
        (2,  1, False), # 16th syncopation
        (3,  1, False), 
        (5,  1, True),  # Accent / 12th fret jump
        (8,  1, False), # Beat 3
        (10, 1, False), # 16th syncopation
        (11, 1, False),
        (14, 2, True)   # Accent / 12th fret jump, held slightly longer
    ]

    sixteenth_length = qn_length / 4.0
    note_count = 0

    # Generate MIDI notes
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        for start_16th, length_16ths, is_octave_up in metal_riff_grid:
            note_start_time = bar_start_time + (start_16th * sixteenth_length)
            # Subtract 0.01s to make the bass notes slightly staccato, allowing the kick to breathe
            note_end_time = note_start_time + (length_16ths * sixteenth_length) - 0.015 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
            
            # Jump up 12 semitones if following the high guitar fret
            pitch = root_midi_pitch + 12 if is_octave_up else root_midi_pitch
            
            # Slight velocity emphasis on the octave jumps
            vel = min(127, velocity_base + 8) if is_octave_up else velocity_base
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (DI Bass Placeholder) ===
    # Add a synthesizer to act as our virtual bass
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a more "bass guitar" DI sound (blend square and saw, lower tune)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0)    # Tuning (already handled by low MIDI note)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5)    # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.5)    # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.05)   # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.3)    # Release

    # Add ReaEQ to cut harsh top end (mimicking the velocity technique's tonal effect)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 (High Shelf) -> pull down top end
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 0.0) # Type: High Shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 4000.0) # Freq: 4kHz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, -6.0) # Gain: -6dB

    return f"Created '{track_name}' with {note_count} locked/octave-jumping bass notes over {bars} bars at {bpm} BPM."
