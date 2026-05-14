def create_pattern(
    project_name: str = "VGM_Project",
    track_name: str = "VGM_Loop",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8, # Ensure this is an even number, preferably 8
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a seamless VGM loop demonstrating Tip 10 (Melody on Top) 
    and Tip 12 (Dominant V7 Turnaround).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars (should be multiple of 4, e.g., 4 or 8).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string detailing the track creation.
    """
    import reaper_python as RPR

    # Note to MIDI base value mapping (Octave 4)
    NOTE_MAP = {"C": 60, "C#": 61, "Db": 61, "D": 62, "D#": 63, "Eb": 63,
                "E": 64, "F": 65, "F#": 66, "Gb": 66, "G": 67, "G#": 68,
                "Ab": 68, "A": 69, "A#": 70, "Bb": 70, "B": 71}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "minor"
        
    root_midi = NOTE_MAP[key] - 12 # Drop to octave 3 for chords
    scale_intervals = SCALES[scale]
    
    # 4-bar chord progression mapped to scale degrees (0-indexed: 0=I, 3=IV, 5=vi, 4=V)
    progression_degrees = [0, 3, 5, 4] 

    # --- Setup Project Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars

    def create_vgm_track(name, is_melody):
        # Insert Track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Add ReaSynth
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        # Tweak ReaSynth for retro VGM feel: Mix of square and saw
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)  # Volume
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.7)  # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)  # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1)  # Attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.4)  # Decay
        
        # Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        return track, take

    # Create Tracks
    chord_track, chord_take = create_vgm_track(f"{track_name}_Chords", False)
    melody_track, melody_take = create_vgm_track(f"{track_name}_Melody", True)
    
    # Lower the volume of the chord track slightly to keep Melody on Top (Tip 10)
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "D_VOL", 0.7)

    # --- Generate MIDI ---
    for bar in range(bars):
        # Determine which chord in the 4-bar sequence we are on
        prog_idx = bar % len(progression_degrees)
        scale_degree = progression_degrees[prog_idx]
        
        bar_start_sec = bar * bar_length_sec
        bar_end_sec = (bar + 1) * bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, bar_start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, bar_end_sec)
        
        # --- Tip 12: Dominant Turnaround Override ---
        # If this is the absolute last bar of the loop, force a V7 chord
        if bar == bars - 1:
            # V7 chord structure relative to root note
            chord_notes = [
                root_midi + 7,  # Perfect 5th
                root_midi + 11, # Major 3rd (forces dominant feel even in minor)
                root_midi + 14, # Minor 7th
                root_midi + 19  # Octave + P5
            ]
        else:
            # Build standard diatonic triad
            root_idx = scale_degree
            third_idx = (scale_degree + 2) % 7
            fifth_idx = (scale_degree + 4) % 7
            
            octave_offset_root = (scale_degree // 7) * 12
            octave_offset_third = ((scale_degree + 2) // 7) * 12
            octave_offset_fifth = ((scale_degree + 4) // 7) * 12
            
            chord_notes = [
                root_midi + scale_intervals[root_idx] + octave_offset_root,
                root_midi + scale_intervals[third_idx] + octave_offset_third,
                root_midi + scale_intervals[fifth_idx] + octave_offset_fifth
            ]

        # Insert Chord Notes (Whole Notes)
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, int(note), velocity_base, True)
            
        # Insert Melody/Arp Notes (8th notes, Octave higher)
        # Tip 10: Melody on top, rhythmically driving the piece
        beat_length_ppq = (end_ppq - start_ppq) / 8 # 8th notes
        for i in range(8):
            note_start = start_ppq + (i * beat_length_ppq)
            note_end = note_start + (beat_length_ppq * 0.8) # Slight staccato
            
            # Simple arpeggiator pattern bouncing between chord notes
            arp_note = chord_notes[i % len(chord_notes)] + 12 # Up 1 octave
            
            # Add dynamic velocity for a more "played" feel
            vel = velocity_base if i % 2 == 0 else int(velocity_base * 0.8)
            
            RPR.RPR_MIDI_InsertNote(melody_take, False, False, note_start, note_end, 0, int(arp_note), vel, True)

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(melody_take)
    
    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created VGM loop: '{track_name}_Chords' and '{track_name}_Melody' ({bars} bars, {bpm} BPM, {key} {scale}) featuring a V7 Turnaround."
