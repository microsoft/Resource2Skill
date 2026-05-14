def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Punchy Kick",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Punchy Kick track demonstrating transient shaping via compression.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note for the kick pitch.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Setup basic pitch lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch = NOTE_MAP.get(key, 0)
    # Target C2 range for a kick (MIDI note 36 is C2)
    kick_note = 36 + root_pitch 
    if kick_note > 41:  # Keep it in the low/bass register
        kick_note -= 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Sound Source (ReaSynth) ===
    # We create a synthesized kick sound so the compressor has a signal to shape.
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth settings for a subby kick (approx normalized values)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)  # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)  # Saw/Square mix: 0 (Pure Sine)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.0)  # Attack: 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.15) # Decay: Short (~150ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 10, 0.0) # Sustain: 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 11, 0.2) # Release: Short

    # === Step 4: Add Transient Shaping Compressor (ReaComp) ===
    # This is the core skill extracted from the tutorial
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # ReaComp parameters (normalized values 0.0 to 1.0)
    # Param 0: Threshold (-60dB to 12dB). Target: -12dB -> ( -12 - (-60) ) / 72 = 48/72 = 0.666
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, 0.66)
    
    # Param 1: Ratio. Target: ~3.0:1. 
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 0.12)
    
    # Param 2: Attack. Target: ~40ms (Allows the transient "punch" to escape)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 0.08)
    
    # Param 3: Release. Target: ~200ms (Shapes the "depth/tail" nicely before next hit)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 0.04)
    
    # Param 15: Wet / Makeup Gain. Target: +2.5dB (Restores loudness, emphasizing transient)
    # Slider 0.0 to 1.0 maps to -inf to +24dB, with 0dB typically around 0.5 depending on pan law
    # We slightly boost the output to replicate the video's makeup gain.
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 15, 0.55)

    # === Step 5: Create MIDI Item & Sequence ===
    beats_per_bar = 4
    beats_total = bars * beats_per_bar
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert Four-on-the-floor quarter notes
    note_length_beats = 0.5 # Staccato 1/8th note duration
    note_length_sec = (60.0 / bpm) * note_length_beats
    
    beats_count = 0
    note_count = 0
    while beats_count < beats_total:
        start_pos = (60.0 / bpm) * beats_count
        end_pos = start_pos + note_length_sec
        
        # Convert seconds to PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, kick_note, velocity_base, False)
        
        beats_count += 1.0 # Advance by one quarter note (1 beat)
        note_count += 1
        
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} punchy kicks over {bars} bars at {bpm} BPM using ReaComp transient shaping (40ms attack, 200ms release)."
