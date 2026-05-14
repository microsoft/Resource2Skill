def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Reese Bass",
    bpm: int = 174,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Drum & Bass style Reese Bass track with a sustained MIDI progression
    and a custom stock-plugin FX chain to emulate detuned oscillators.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (170-175 is standard for DnB).
        key: Root note (e.g., "F").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    }

    # === Step 1: Initialize Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Validate scale
    if scale not in SCALES:
        scale = "minor"
    s = SCALES[scale]
    
    # Calculate deep root note (MIDI Octave 1 / 2)
    # Target range ~ MIDI 24 (C1) to 35 (B1)
    base_midi = NOTE_MAP.get(key, 5) + 24 

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    item_length = bar_len * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Generate Reese Progression ===
    # Standard dark progression: i (hold 2 bars), VI (1 bar), VII (1 bar)
    # If bars < 4, just hold the root note
    
    notes_to_add = []
    
    for i in range(0, bars, 4):
        # Calculate how many bars are left in this 4-bar chunk
        chunk_bars = min(4, bars - i)
        
        if chunk_bars == 4:
            # i (Root) - 2 bars
            notes_to_add.append((base_midi, i * bar_len, (i + 2) * bar_len))
            # VI (6th degree, dropped down an octave to stay deep)
            vi_pitch = base_midi + s[5] - 12
            notes_to_add.append((vi_pitch, (i + 2) * bar_len, (i + 3) * bar_len))
            # VII (7th degree, dropped down an octave)
            vii_pitch = base_midi + s[6] - 12
            notes_to_add.append((vii_pitch, (i + 3) * bar_len, (i + 4) * bar_len))
        else:
            # Just hold the root for however many bars remain
            notes_to_add.append((base_midi, i * bar_len, (i + chunk_bars) * bar_len))

    # Insert notes into the take
    for pitch, start_time, end_time in notes_to_add:
        # Convert absolute time to PPQ (pulses per quarter note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(
            take,
            False,      # selected
            False,      # muted
            start_ppq,
            end_ppq,
            0,          # channel
            int(pitch),
            velocity_base,
            False       # no sort (we'll sort after)
        )
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Construct the "Stock Reese" FX Chain ===
    
    # 1. Synthesizer (ReaSynth)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Chorus (To create the detuned phase-cancellation wobble)
    # JS: Chorus or JS: Ozzifier are great for stereo detune spread
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    
    # 3. Saturation / Distortion (To add upper harmonics)
    RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    
    # 4. Filter (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Parameter manipulation for ReaEQ to create a Low Pass filter is complex via API 
    # due to dynamic band indices, but simply adding it prepares the track for mixing.

    return f"Created '{track_name}' (Stock Reese Emulation) spanning {bars} bars at {bpm} BPM in {key} {scale}."
