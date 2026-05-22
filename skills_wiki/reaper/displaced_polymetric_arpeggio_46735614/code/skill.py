def create_pattern(
    project_name: str = "DisplacedArpProject",
    track_name: str = "Displaced_Arp",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a "Displaced Polymetric Arpeggio" pattern.
    Generates two tracks: A 7-step looping plucky arpeggio, and a 4-bar slow pad progression underneath.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, G, D#).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (should be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

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

    if scale not in SCALES:
        scale = "minor"
    
    root_val = NOTE_MAP.get(key.capitalize(), 7) # Default G
    scale_intervals = SCALES[scale]

    # Helper function to convert scale degrees to absolute MIDI notes
    def get_midi_note(degree, octave=4):
        oct_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_val + ((octave + oct_shift) * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # ==========================================
    # === Step 2: Create Arpeggio Track (T1) ===
    # ==========================================
    track_idx_arp = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_arp, True)
    track_arp = RPR.RPR_GetTrack(0, track_idx_arp)
    RPR.RPR_GetSetMediaTrackInfo_String(track_arp, "P_NAME", f"{track_name}_Pluck", True)

    item_arp = RPR.RPR_AddMediaItemToTrack(track_arp)
    RPR.RPR_SetMediaItemInfo_Value(item_arp, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_arp, "D_LENGTH", item_length)
    take_arp = RPR.RPR_AddTakeToMediaItem(item_arp)

    # 7-step sequence (Root, 5th, Octave, 5th, 3rd, 5th, 2nd) represented in scale degrees
    arp_pattern_degrees = [0, 4, 7, 4, 2, 4, 1] 
    note_length_beats = 0.25 # 16th notes
    total_16th_notes = int(bars * beats_per_bar * 4)

    for i in range(total_16th_notes):
        degree = arp_pattern_degrees[i % len(arp_pattern_degrees)]
        pitch = get_midi_note(degree, octave=5)
        
        start_time = i * note_length_beats * (60.0 / bpm)
        end_time = start_time + (note_length_beats * (60.0 / bpm) * 0.8) # 80% gate length for pluck
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_arp, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_arp, end_time)
        
        # Add dynamic velocity based on position in the 7-step sequence to emphasize the polymeter
        vel = velocity_base if (i % 7 == 0) else velocity_base - 20
        
        RPR.RPR_MIDI_InsertNote(take_arp, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take_arp)

    # Add Plucky Synth & Delay to Arp
    synth_arp = RPR.RPR_TrackFX_AddByName(track_arp, "ReaSynth", False, -1)
    # Param 1: Attack (fast), Param 2: Decay (short), Param 3: Sustain (none), Param 4: Release (short)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 1, 0.0)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 2, 0.1)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 3, 0.0)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 4, 0.1)
    RPR.RPR_TrackFX_SetParam(track_arp, synth_arp, 5, 0.7) # Square wave mix for bite

    delay = RPR.RPR_TrackFX_AddByName(track_arp, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track_arp, delay, 0, -6.0) # Wet mix

    # =======================================
    # === Step 3: Create Pad Track (T2)   ===
    # =======================================
    track_idx_pad = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_pad, True)
    track_pad = RPR.RPR_GetTrack(0, track_idx_pad)
    RPR.RPR_GetSetMediaTrackInfo_String(track_pad, "P_NAME", f"{track_name}_Pad", True)
    
    # Lower pad volume
    RPR.RPR_SetMediaTrackInfo_Value(track_pad, "D_VOL", 0.5) 

    item_pad = RPR.RPR_AddMediaItemToTrack(track_pad)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_pad, "D_LENGTH", item_length)
    take_pad = RPR.RPR_AddTakeToMediaItem(item_pad)

    # Progression: i - VI - III - VII (represented as root scale degrees)
    progression = [0, 5, 2, 6] 

    for bar in range(bars):
        root_degree = progression[bar % len(progression)]
        
        # Create a triad: Root, 3rd, 5th based on the current scale degree
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_pad, end_time)
        
        for deg in chord_degrees:
            pitch = get_midi_note(deg, octave=3) # Play pad in lower octave
            RPR.RPR_MIDI_InsertNote(take_pad, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 15, False)

    RPR.RPR_MIDI_Sort(take_pad)

    # Add Lush Synth to Pad
    synth_pad = RPR.RPR_TrackFX_AddByName(track_pad, "ReaSynth", False, -1)
    # Slow attack, high sustain, slow release
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 1, 0.4) # Attack
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 2, 0.5) # Decay
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 3, 0.8) # Sustain
    RPR.RPR_TrackFX_SetParam(track_pad, synth_pad, 4, 0.6) # Release
    
    RPR.RPR_TrackFX_AddByName(track_pad, "ReaVerbate", False, -1)

    return f"Created Displaced Polymetric Arp setup ('{track_name}_Pluck' and '{track_name}_Pad') over {bars} bars in {key} {scale} at {bpm} BPM."
