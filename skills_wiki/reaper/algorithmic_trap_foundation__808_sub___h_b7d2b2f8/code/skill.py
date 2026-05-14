def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Trap Beat",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Algorithmic Trap Drum Groove and an 808 Sub Bass in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (typically 130-150 for trap).
        key: Root note (e.g., C, C#, D).
        scale: Scale type (e.g., minor, harmonic_minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Music theory lookup tables for the 808 Bassline
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beat_len = 60.0 / bpm
    sixteenth_len = beat_len / 4.0
    bar_len = beat_len * 4

    # Helper function to create a track and a full-length MIDI item
    def setup_track_and_item(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_len * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === Step 2: Track Setup ===
    track_808, take_808 = setup_track_and_item(f"{track_name} 808 Sub")
    track_drums, take_drums = setup_track_and_item(f"{track_name} Drums (Kong/BeatMap)")

    # Construct the 808 Sub tone using ReaSynth
    # 1 is the 'instantiate' flag to add the FX
    fx_idx = RPR.RPR_TrackFX_AddByName(track_808, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 0, 0.8)  # Volume
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 2, 0.0)  # Square mix (0%)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 3, 0.0)  # Saw mix (0%)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 4, 0.3)  # Triangle mix (30% for harmonics)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 5, 1.0)  # Extra Sine (100% for sub pressure)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 6, 0.0)  # Attack (Instant)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 9, 0.7)  # Release (Long decay for trap 808s)
    
    # Calculate base 808 pitch (Ensure it sits in the 40-60Hz sub range)
    root_idx = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_pitch = root_idx + 24  # Starts at C1
    if base_pitch < 28:         # If lower than E1, pitch up an octave to avoid muddiness
        base_pitch += 12

    # === Step 3: MIDI Pattern Generation ===
    for b in range(bars):
        base_step = b * 16
        
        # --- Kick Drum & 808 Harmonics ---
        kicks = [0, 10]          # Kick on Beat 1, and the 'and' of Beat 3
        if b % 2 == 1:
            kicks.append(14)     # Add syncopated kick before the end of even bars
            
        for k in kicks:
            start = (base_step + k) * sixteenth_len
            
            # Insert Kick Drum (GM Note 36)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start + sixteenth_len), 
                                    0, 36, velocity_base, False)
            
            # Insert 808 Sub (Follows Kick rhythm, changes pitch based on progression)
            pitch = base_pitch
            if b % 4 == 2:
                pitch = base_pitch + scale_intervals[5 % len(scale_intervals)] # Move to 6th degree
            elif b % 4 == 3:
                pitch = base_pitch + scale_intervals[4 % len(scale_intervals)] # Move to 5th degree
                
            RPR.RPR_MIDI_InsertNote(take_808, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, start), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, start + sixteenth_len * 3.5), 
                                    0, pitch, velocity_base, False)

        # --- Halftime Snare ---
        snare_start = (base_step + 8) * sixteenth_len # Beat 3
        RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, snare_start), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, snare_start + sixteenth_len), 
                                0, 38, velocity_base, False)

        # --- Algorithmic Hi-Hats with Rolls ---
        for h in range(16):
            play_hat = False
            # Standard 8th notes
            if h % 2 == 0:
                play_hat = True
            # Trap Roll logic: Insert fast 16ths at specific turnaround points
            elif b % 2 == 1 and h in [13, 15]: 
                play_hat = True
            elif b % 4 == 3 and h in [5, 7]:   
                play_hat = True
                
            if play_hat:
                hat_start = (base_step + h) * sixteenth_len
                # Add slight velocity variation to rolls to mimic realistic beat machines
                vel = int(velocity_base * 0.8) if h % 2 == 0 else int(velocity_base * 0.95)
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                        RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hat_start), 
                                        RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hat_start + sixteenth_len * 0.5), 
                                        0, 42, vel, False)

    # Sort MIDI items to finalize insertion
    RPR.RPR_MIDI_Sort(take_808)
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_UpdateArrange()

    return f"Created Trap Beat ({bars} bars, {bpm} BPM) with dynamic 808 Sub Bass in {key} {scale}."
