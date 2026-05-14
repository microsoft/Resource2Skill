def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sketchpad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Songwriter's Diatonic Sketchpad in the current REAPER project.
    Generates a color-coded multitrack setup with Drums, Bass, and Chords.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated setup.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (default 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # --- Music Theory Configuration ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    scale_type = scale.lower() if scale.lower() in SCALES else "major"
    intervals = SCALES[scale_type]
    root_pitch = NOTE_MAP.get(key.capitalize(), 0)

    # Standard Pop progressions (0-indexed degrees)
    if scale_type == "major":
        progression = [0, 4, 5, 3] # I - V - vi - IV
    else:
        progression = [0, 5, 2, 6] # i - VI - III - VII

    def get_diatonic_pitch(degree, base_octave):
        """Calculates exact MIDI pitch for a diatonic scale degree"""
        octave_shift = degree // len(intervals)
        scale_degree = degree % len(intervals)
        return root_pitch + intervals[scale_degree] + ((base_octave + octave_shift) * 12)

    # --- Step 1: Set Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars

    # --- Step 2: Helper for Track Creation ---
    def create_track_with_midi(name, color_hex, create_synth=False):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Parse hex color and apply REAPER native format
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        reaper_color = RPR.RPR_ColorToNative(r, g, b) | 0x1000000
        RPR.RPR_SetTrackColor(track, reaper_color)
        
        # Add basic Synth
        if create_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Lower volume to prevent master clipping (-12dB approx)
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.25)

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        return take

    # --- Step 3: Generate Tracks & MIDI ---
    
    # 1. DRUMS (Red)
    take_drums = create_track_with_midi("DRUMS", "FF4444")
    for b in range(bars):
        for qn in range(4):
            # Kick (36) on every quarter note
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn + 0.25)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, 36, velocity_base, True)
            
            # Snare (38) on beats 2 and 4 (QN index 1 and 3)
            if qn % 2 != 0:
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, 38, velocity_base, True)
            
            # Hi-hat (42) on 8th notes (every 0.5 QN)
            hh_start = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn)
            hh_end = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn + 0.25)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, hh_start, hh_end, 9, 42, int(velocity_base*0.8), True)
            
            hh_offbeat_start = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn + 0.5)
            hh_offbeat_end = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, (b * 4) + qn + 0.75)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, hh_offbeat_start, hh_offbeat_end, 9, 42, int(velocity_base*0.6), True)
    RPR.RPR_MIDI_Sort(take_drums)

    # 2. BASS (Blue)
    take_bass = create_track_with_midi("BASS", "4488FF", create_synth=True)
    for b in range(bars):
        degree = progression[b % len(progression)]
        pitch = get_diatonic_pitch(degree, base_octave=2) # Octave 2 for Bass
        
        # 8th note driving bassline
        for eighth in range(8):
            start_qn = (b * 4) + (eighth * 0.5)
            end_qn = start_qn + 0.45 # slightly detached
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, end_qn)
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
    RPR.RPR_MIDI_Sort(take_bass)

    # 3. CHORDS (Green)
    take_chords = create_track_with_midi("CHORDS", "44FF44", create_synth=True)
    for b in range(bars):
        degree = progression[b % len(progression)]
        start_qn = b * 4
        end_qn = start_qn + 4.0
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, end_qn)
        
        # Build Triad (Root, Third, Fifth)
        for chord_tone in [0, 2, 4]:
            pitch = get_diatonic_pitch(degree + chord_tone, base_octave=4)
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base*0.8), True)
    RPR.RPR_MIDI_Sort(take_chords)

    # Update arrange view
    RPR.RPR_UpdateArrange()

    return f"Created Songwriter Sketchpad (Drums, Bass, Chords) with {bars} bars in {key} {scale_type} at {bpm} BPM."
