def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Melodic Chords",
    bpm: int = 85,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Top-Down Melodic Chord Progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created element.
    """
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }
    
    current_scale = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = NOTE_MAP.get(key.upper(), 0)

    def get_pitch(degree_0_indexed, target_octave):
        """Returns the exact MIDI pitch for a diatonic scale degree in a specific octave."""
        scale_len = len(current_scale)
        # Wrap degree to stay within the scale array
        safe_degree = degree_0_indexed % scale_len
        # Calculate pitch (Octave 0 starts at MIDI note 12)
        pitch = root_midi + ((target_octave + 1) * 12) + current_scale[safe_degree]
        return pitch

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_midi_note(pitch, start_qn, end_qn, vel):
        start_time = start_qn * (60.0 / bpm)
        end_time = end_qn * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # Constrain velocity
        safe_vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), safe_vel, False)

    # Progression definition: (chord_root_degree, melody_degree, melody_octave)
    # Degrees are 0-indexed (e.g., 3 = IV chord, 4 = V chord)
    progression = [
        (3, 0, 5), # Bar 1: IV chord, Melody on the 1st degree (e.g. Fmaj9 with C on top)
        (4, 1, 5), # Bar 2: V chord, Melody on the 2nd degree (e.g. Gdom7 with D on top)
        (0, 4, 4), # Bar 3: I chord, Melody on the 5th degree (e.g. Cmaj7 with G on top)
        (5, 2, 4), # Bar 4: vi chord, Melody on the 3rd degree (e.g. Amin7 with E on top)
    ]

    # Strumming delay in Quarter Notes
    strum_delay = 0.04

    # Generate the chords
    for i in range(bars):
        # Loop progression if bars > 4
        root_deg, mel_deg, mel_oct = progression[i % len(progression)]
        
        # Calculate shell voicing + melody pitches
        bass_pitch = get_pitch(root_deg, 2)            # Root
        third_pitch = get_pitch(root_deg + 2, 3)       # 3rd
        seventh_pitch = get_pitch(root_deg + 6, 3)     # 7th
        mel_pitch = get_pitch(mel_deg, mel_oct)        # Top Melody
        
        # Timing (Leave a small gap at the end of the bar for articulation)
        start_qn = i * beats_per_bar
        end_qn = start_qn + beats_per_bar - 0.15
        
        # Insert notes with "guitar strum" timing offsets and velocity layering
        # Bass (Hardest, exactly on beat)
        insert_midi_note(bass_pitch, start_qn, end_qn, velocity_base)
        
        # 7th (Softer, slightly delayed)
        insert_midi_note(seventh_pitch, start_qn + (strum_delay * 1), end_qn, velocity_base - 15)
        
        # 3rd (Softer, slightly delayed)
        insert_midi_note(third_pitch, start_qn + (strum_delay * 2), end_qn, velocity_base - 10)
        
        # Melody (Loudest, shines on top)
        insert_midi_note(mel_pitch, start_qn + (strum_delay * 3), end_qn, velocity_base + 15)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design FX ===
    # 1. ReaSynth (Warm Pad/Organ Tone)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.08)  # Attack (soften transient)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.40)  # Release (longer tail)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.25)  # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.15)  # Saw wave mix

    # 2. ReaDelay (Space & Ambience)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, 0.0)   # Wet mix (-6dB approx)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 1, -6.0)  # Dry mix
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 4, 1.5)   # Length (Quarter dot)

    return f"Created '{track_name}' with {bars} bars of Top-Down Melodic Chords in {key} {scale} at {bpm} BPM."
