def create_pattern(
    project_name: str = "Jazz Transcription",
    track_name: str = "Jazz Piano Comp & Solo",
    bpm: int = 120,
    key: str = "F",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a 4-bar Jazz Piano pattern featuring swung 8th-note bebop lines 
    and syncopated rootless ii-V-I comping.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 5) # Default to F
    octave_lh = 48 # C3 for left hand comping
    octave_rh = 72 # C5 for right hand soloing

    # Rootless Voicings for ii - V - I in a Major Key
    # Expressed as semitone offsets from the Key's Root note
    # e.g., In F Major: ii is Gmin9. Rootless voicing is F, A, Bb, D (b7, 9, b3, 5 of G)
    voicings = {
        "ii": [0, 4, 5, 9],    # Minor 9 (rootless)
        "V":  [-1, 4, 5, 9],   # Dom 13 (rootless) - smooth voice leading (F goes down to E)
        "I":  [-1, 2, 4, 7]    # Major 9 (rootless)
    }

    swing_amount = 0.33 # Amount of QN to delay off-beats (0.33 is hard triplet swing)

    # === Step 1: Track & Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to add notes with swing
    def add_midi_note(take, qn_start, qn_len, pitch, vel):
        # Apply Swing Algorithm
        # If the start time is on an "and" (e.g., 0.5, 1.5, 2.5), delay it
        beat_fraction = qn_start % 1.0
        if 0.1 < beat_fraction < 0.9: # It's an off-beat
            qn_start += (swing_amount * beat_fraction)
            # Reduce velocity of off-beats for dynamic groove (ghosting)
            vel = int(vel * 0.75) 
            
        proj_start_time = RPR.RPR_TimeMap2_QNToTime(0, qn_start)
        proj_end_time = RPR.RPR_TimeMap2_QNToTime(0, qn_start + qn_len)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # === Step 3: Generate Left Hand Syncopated Comping ===
    # Bar 1: ii chord
    for note_offset in voicings["ii"]:
        pitch = octave_lh + root_pitch + note_offset
        add_midi_note(take, 0.0, 1.5, pitch, velocity_base)       # Downbeat stab
        add_midi_note(take, 2.5, 1.0, pitch, velocity_base + 10)  # Syncopated "push" on the 'and' of 2
    
    # Bar 2: V chord
    for note_offset in voicings["V"]:
        pitch = octave_lh + root_pitch + note_offset
        add_midi_note(take, 4.0, 1.5, pitch, velocity_base)       # Downbeat stab
        add_midi_note(take, 6.5, 1.0, pitch, velocity_base + 15)  # Syncopated push
        
    # Bar 3-4: I chord
    for note_offset in voicings["I"]:
        pitch = octave_lh + root_pitch + note_offset
        add_midi_note(take, 8.0, 3.5, pitch, velocity_base - 5)   # Resolving downbeat, hold

    # === Step 4: Generate Right Hand Swung Melody ===
    # A simple bebop line utilizing scale degrees and enclosures
    melody_pattern = [
        # Bar 1 (ii chord focus)
        (0.0, 0.5, root_pitch + 9),   # 5th of ii
        (0.5, 0.5, root_pitch + 7),   # 4th
        (1.0, 0.5, root_pitch + 5),   # b3
        (1.5, 0.5, root_pitch + 4),   # passing
        (2.0, 0.5, root_pitch + 2),   # root of ii
        (2.5, 0.5, root_pitch + 4),
        (3.0, 0.5, root_pitch + 5),
        (3.5, 0.5, root_pitch + 7),
        
        # Bar 2 (V chord focus)
        (4.0, 0.5, root_pitch + 9),   # 9th of V
        (4.5, 0.5, root_pitch + 8),   # b9 (tension)
        (5.0, 0.5, root_pitch + 7),   # Root of V
        (5.5, 0.5, root_pitch + 5),   # b7
        (6.0, 0.5, root_pitch + 4),   # 13th
        (6.5, 0.5, root_pitch + 2),
        (7.0, 0.5, root_pitch + 1),   # passing tone
        (7.5, 0.5, root_pitch + 2),
        
        # Bar 3 (I chord resolution)
        (8.0, 2.0, root_pitch + 4),   # 3rd of I (resolution target)
    ]

    for start_offset, length, m_pitch in melody_pattern:
        add_midi_note(take, start_offset, length, octave_rh + m_pitch, velocity_base + 5)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Jazz Electric Piano Tone) ===
    # Add ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.0) # Square mix down
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.4) # Saw mix 
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.1) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.3) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.1) # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.4) # Release

    # Add ReaEQ to muffle the high end, creating a dark, vintage "Rhodes" feel
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4: Low Pass Filter to roll off everything above 2kHz
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 9, 0.0)    # Band 4 Type (Low Pass)
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.4)   # Band 4 Freq (approx 2000 Hz)

    return f"Created '{track_name}' featuring swung right-hand lines and syncopated left-hand ii-V-I rootless chords in Key of {key} over {bars} bars at {bpm} BPM."
