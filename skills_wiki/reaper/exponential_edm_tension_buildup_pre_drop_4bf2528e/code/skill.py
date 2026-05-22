def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Buildup_Generator",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Exponential EDM Tension Buildup in the current REAPER project.
    Generates 3 additive tracks: Snare Roll, Tension Arp, and Riser/Downer Sweeps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars for the buildup (typically 4 or 8).
        velocity_base: Max MIDI velocity climax (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
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

    # Validate scale and calculate root
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    root_midi = 48 + root_val  # C3ish

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Timing calculations
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    # REAPER MIDI defaults to 960 PPQ (Pulses Per Quarter Note)
    ppq_per_qn = 960
    total_ppq = total_beats * ppq_per_qn
    gap_ppq = ppq_per_qn  # 1 beat of absolute silence at the end
    build_ppq = total_ppq - gap_ppq

    notes_created = 0

    def create_buildup_track(name_suffix: str):
        """Helper to create a track and a MIDI item on it."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name_suffix}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Add basic ReaSynth so it makes sound out of the box
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return take

    RPR.RPR_Undo_BeginBlock2(0)

    # ==========================================
    # TRACK 1: Exponential Snare / Clap Roll
    # ==========================================
    take_drums = create_buildup_track("Snares")
    pos = 0
    while pos < build_ppq:
        current_bar = pos / (ppq_per_qn * 4)
        
        # Exponential pacing logic
        if current_bar < bars / 2:
            step = ppq_per_qn            # 1/4 notes
        elif current_bar < bars * 0.75:
            step = int(ppq_per_qn / 2)   # 1/8 notes
        elif current_bar < bars - 0.5:
            step = int(ppq_per_qn / 4)   # 1/16 notes
        else:
            step = int(ppq_per_qn / 8)   # 1/32 notes

        # Linear tension velocity ramp
        progress = pos / build_ppq
        vel = int(50 + (77 * progress))
        vel = min(127, max(1, vel))

        # Insert snare note (General MIDI Snare = D2 = 38)
        RPR.RPR_MIDI_InsertNote(take_drums, False, False, pos, pos + int(step*0.5), 1, 38, vel, False)
        notes_created += 1
        pos += step


    # ==========================================
    # TRACK 2: Tension Arp
    # ==========================================
    take_arp = create_buildup_track("Tension_Arp")
    arp_pos = 0
    arp_step = int(ppq_per_qn / 4) # 1/16th notes
    
    # Safe chord degrees (Root, 3rd, 5th) mapping for scale lengths
    idx_3rd = 2 if len(scale_intervals) > 5 else 1
    idx_5th = 4 if len(scale_intervals) > 5 else 3
    arp_motif = [0, idx_3rd, idx_5th, 0] # Repeating 4-note contour
    
    step_count = 0
    while arp_pos < build_ppq:
        deg = arp_motif[step_count % 4]
        note = root_midi + scale_intervals[deg]
        
        # Tension multiplier: Jump an octave in the second half of the buildup
        if arp_pos > build_ppq / 2:
            note += 12
            
        progress = arp_pos / build_ppq
        vel = int(70 + (50 * progress))

        RPR.RPR_MIDI_InsertNote(take_arp, False, False, arp_pos, arp_pos + int(arp_step * 0.8), 1, note, vel, False)
        notes_created += 1
        arp_pos += arp_step
        step_count += 1


    # ==========================================
    # TRACK 3: Risers and Downers
    # ==========================================
    take_fx = create_buildup_track("Risers_FX")
    
    # The Downer (Long, low sub hit at the very beginning to mark the transition)
    RPR.RPR_MIDI_InsertNote(take_fx, False, False, 0, ppq_per_qn * 4, 1, root_midi - 24, 110, False)
    notes_created += 1

    # The Riser (Ascending overlapping notes acting as a pitch sweep)
    riser_pos = 0
    riser_step = ppq_per_qn * 2 # Half note blocks
    while riser_pos < build_ppq:
        progress = riser_pos / build_ppq
        # Ascend a full 2 octaves over the duration of the buildup
        sweep_note = root_midi + int(progress * 24) 
        vel = int(60 + (67 * progress))
        
        # Overlapping notes to simulate a continuous sweep
        RPR.RPR_MIDI_InsertNote(take_fx, False, False, riser_pos, riser_pos + riser_step + int(ppq_per_qn/2), 1, sweep_note, vel, False)
        notes_created += 1
        riser_pos += riser_step

    RPR.RPR_Undo_EndBlock2(0, "Create Exponential Buildup Pattern", -1)
    RPR.RPR_UpdateArrange()

    return f"Created Buildup elements ({notes_created} notes total across 3 tracks) over {bars} bars at {bpm} BPM with a 1-beat pre-drop gap."
