def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Emo Punk Rhythm Guitar",
    bpm: int = 150,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a driving Emo-Punk Power Chord Rhythm in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (150 is typical for this genre).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate (loops a 4-bar progression).
        velocity_base: Base MIDI velocity (0-127) for the aggressive down-picking.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
    }

    # Extract scale intervals, default to major if not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # I-V-vi-IV progression (degrees 0, 4, 5, 3 in 0-indexed scale)
    progression = [0, 4, 5, 3]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    # Lower track volume to leave headroom for heavy distortion
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Add FX Chain for "Punk Guitar" tone ===
    # Add Synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set to a mix of Saw (aggressive) and Square (hollow/woody)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0) # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.8) # Saw
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4) # Square
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0) # Triangle
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.8) # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.05) # Release

    # Add Amp Sim for distortion
    amp_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Guitar/amp-model", False, -1)
    if amp_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, amp_idx, 0, 1.0) # Preamp drive (high for punk)
        RPR.RPR_TrackFX_SetParam(track, amp_idx, 1, -6.0) # Output trim

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Insert MIDI Notes ===
    note_count = 0
    base_note = 36 + NOTE_MAP.get(key, 2) # e.g. D2 = 38

    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Calculate root pitch for this chord
        root_pitch = base_note + scale_intervals[degree]
        
        # Voice leading: drop octave if pitch gets too high (keep it chunky)
        if root_pitch > 45:
            root_pitch -= 12
            
        power_chord_pitches = [
            root_pitch,          # Root
            root_pitch + 7,      # Perfect 5th
            root_pitch + 12      # Octave
        ]

        # 8 strokes per bar (continuous 8th notes)
        for stroke in range(8):
            start_qn = bar * 4.0 + (stroke * 0.5)
            # Make the note length slightly less than a full 8th note (0.45) for rhythmic clarity
            end_qn = start_qn + 0.45 
            
            # Simulate down-picking dynamics (downbeats harder than upbeats)
            stroke_velocity = velocity_base if (stroke % 2 == 0) else velocity_base - 15
            # Add slight humanization
            stroke_velocity = max(1, min(127, int(stroke_velocity)))

            start_time = start_qn * (60.0 / bpm)
            end_time = end_qn * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            for pitch in power_chord_pitches:
                # Add note to MIDI item
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # Selected
                    False,          # Muted
                    start_ppq, 
                    end_ppq, 
                    0,              # Channel 1
                    pitch, 
                    stroke_velocity, 
                    False           # No sort yet
                )
                note_count += 1

    # Finalize MIDI structure
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes ({bars} bars of I-V-vi-IV at {bpm} BPM in {key} {scale})"
