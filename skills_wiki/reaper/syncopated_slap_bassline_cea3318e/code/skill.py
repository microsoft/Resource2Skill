def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass Groove",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Syncopated Slap Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard notes (0-127). High slaps will be louder.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR
    import random

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

    # Normalize inputs
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_idx = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 4)
    
    # Bass register: typically C1 (24) to B1 (35)
    base_midi_pitch = 24 + root_idx

    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # 2. Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 3. Add Instrument & Shape the Envelope (Plucky/Slap style)
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth parameter indices:
    # 0: Volume, 1: Tuning, 2: Attack, 3: Decay, 4: Sustain, 5: Release, 6: Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.7)    # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)    # Attack (0 = sharp transient)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.15)   # Decay (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.05)   # Sustain (very low)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2)    # Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.3)    # Add a bit of square wave for harmonics

    # 4. Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine passing notes based on scale
    fifth_interval = scale_intervals[4] if len(scale_intervals) > 4 else 7
    # Use the 7th degree of the scale down an octave as a pickup
    lower_seventh_interval = scale_intervals[6] - 12 if len(scale_intervals) > 6 else -2 

    # Define a 2-bar fundamental groove pattern
    # Format: (Beat_Position, Pitch_Offset, Velocity_Multiplier, Length_in_Beats, Is_Slap)
    groove_pattern = [
        # --- BAR 1 ---
        (0.0,  0, 1.0, 0.5,   False), # Beat 1: Downbeat Root
        (1.0,  0, 0.8, 0.25,  False), # Beat 2: Ghost Root
        (1.75, 12, 1.4, 0.125, True),  # Beat 2 "a": High Slap Octave (staccato)
        (2.5,  0, 0.9, 0.5,   False), # Beat 3 "&": Syncopated Root
        (3.75, 12, 1.4, 0.125, True),  # Beat 4 "a": High Slap Octave
        
        # --- BAR 2 ---
        (4.0,  0, 1.1, 0.5,   False), # Beat 1: Downbeat Root
        (5.5,  fifth_interval, 0.7, 0.25, False), # Beat 2 "&": Passing 5th
        (5.75, 12, 1.4, 0.125, True),  # Beat 2 "a": High Slap Octave
        (6.5,  0, 0.9, 0.5,   False), # Beat 3 "&": Syncopated Root
        (7.5,  lower_seventh_interval, 0.85, 0.25, False), # Beat 4 "&": Passing lower 7th leading back to 1
    ]

    # 5. Insert MIDI Notes
    notes_added = 0
    bps = bpm / 60.0
    
    # Loop over the requested number of bars, 2 bars at a time
    for bar_offset in range(0, bars, 2):
        for note in groove_pattern:
            beat_pos, pitch_offset, vel_mult, length_beats, is_slap = note
            
            # Stop if the pattern extends past the requested number of bars
            if (bar_offset * 4) + beat_pos >= bars * 4:
                continue
                
            # Humanize timing (offset by -0.01 to +0.02 beats)
            # Avoid negative times on the absolute first note
            time_offset_beats = random.uniform(-0.02, 0.04)
            actual_beat_pos = (bar_offset * 4) + beat_pos + time_offset_beats
            if actual_beat_pos < 0: actual_beat_pos = 0.0
            
            start_time = actual_beat_pos / bps
            
            # Length: Make slaps extra staccato
            actual_length = length_beats if not is_slap else length_beats * 0.7
            end_time = start_time + (actual_length / bps)
            
            # Pitch
            midi_pitch = base_midi_pitch + pitch_offset
            
            # Humanize velocity
            vel_variation = random.uniform(0.9, 1.05)
            midi_velocity = int(velocity_base * vel_mult * vel_variation)
            midi_velocity = max(1, min(127, midi_velocity)) # Clamp to 1-127
            
            # Insert Note into the take
            RPR.RPR_MIDI_InsertNote(
                take, 
                False, # selected
                False, # muted
                start_time, 
                end_time, 
                0, # channel
                midi_pitch, 
                midi_velocity, 
                False # do not sort yet
            )
            notes_added += 1

    # Sort MIDI notes once all are inserted
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {notes_added} humanized groove notes over {bars} bars at {bpm} BPM in {key} {scale}."
