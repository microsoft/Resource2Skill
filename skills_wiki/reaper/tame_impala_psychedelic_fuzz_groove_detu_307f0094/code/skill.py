def create_pattern(
    project_name: str = "TameImpalaVibe",
    track_name: str = "Psych Fuzz Groove",
    bpm: int = 115,
    key: str = "C",
    scale: str = "harmonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Psychedelic Fuzz-Groove & Detuned Bass pattern in REAPER.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for created tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C").
        scale: Scale type (forces 'harmonic_minor' logic if available).
        bars: Number of bars to generate (best in multiples of 4).
        velocity_base: Base MIDI velocity.
        
    Returns:
        Status string detailing the created elements.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11], # The Tame Impala dark flavor
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    # Ensure valid scale selection
    scale_intervals = SCALES.get(scale, SCALES["harmonic_minor"])
    root_midi = 36 + NOTE_MAP.get(key.capitalize(), 0) # Base octave 3

    # Helper function to insert MIDI notes
    def add_midi_note(take, start_qn, duration_qn, pitch, vel, chan=0):
        start_pos = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
        end_pos = RPR.RPR_TimeMap2_QNToTime(0, start_qn + duration_qn)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), b"")

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Calculate item length in seconds
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars

    # === TRACK 1: FUZZ DRUMS ===
    num_tracks = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    drum_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Fuzz Drums", True)
    
    # Add Drum FX Chain (Guitar Amp/Fuzz emulation)
    RPR.RPR_TrackFX_AddByName(drum_track, "JS: Fuzz", False, -1)
    # Roll off harsh digital highs from the fuzz
    eq_idx = RPR.RPR_TrackFX_AddByName(drum_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, eq_idx, 0, 1) # Band 1 type: Low Shelf
    RPR.RPR_TrackFX_SetParam(drum_track, eq_idx, 3, 0) # Band 4 type: High Cut (LPF)
    RPR.RPR_TrackFX_SetParam(drum_track, eq_idx, 12, 5000) # LPF freq
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    # Drum Pattern Generation (General MIDI mapping)
    for b in range(bars):
        offset = b * beats_per_bar
        # Kick (36)
        add_midi_note(drum_take, offset + 0.0, 0.25, 36, velocity_base)
        add_midi_note(drum_take, offset + 1.5, 0.25, 36, velocity_base - 10) # syncopated
        add_midi_note(drum_take, offset + 2.0, 0.25, 36, velocity_base)
        # Snare/Clap (38/39)
        add_midi_note(drum_take, offset + 1.0, 0.25, 38, velocity_base)
        add_midi_note(drum_take, offset + 1.0, 0.25, 39, velocity_base) # Layered clap
        add_midi_note(drum_take, offset + 3.0, 0.25, 38, velocity_base)
        add_midi_note(drum_take, offset + 3.0, 0.25, 39, velocity_base)
        # 16th Hi-hats (42)
        for i in range(16):
            hat_vel = velocity_base if i % 4 == 0 else velocity_base - 30
            add_midi_note(drum_take, offset + (i * 0.25), 0.125, 42, hat_vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # === TRACK 2: DETUNED MOOG-STYLE BASS ===
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    bass_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} - Detuned Bass", True)

    # Add Bass FX Chain
    synth_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, synth_idx, 1, -12) # Tune down 1 octave
    RPR.RPR_TrackFX_SetParam(bass_track, synth_idx, 2, 1.0) # Square wave mix
    RPR.RPR_TrackFX_AddByName(bass_track, "JS: Chorus", False, -1) # Juno thickness
    dist_idx = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Distortion", False, -1) # Decapitator style grit
    RPR.RPR_TrackFX_SetParam(bass_track, dist_idx, 0, 5.0) # Gain

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Bass Pattern Generation
    for b in range(bars):
        offset = b * beats_per_bar
        # Bouncy section for first 2 bars
        if b % 4 < 2:
            # 16th note bounce off the kick
            add_midi_note(bass_take, offset + 0.0, 0.25, root_midi, velocity_base)
            add_midi_note(bass_take, offset + 0.5, 0.25, root_midi + 12, velocity_base - 10) # octave jump
            add_midi_note(bass_take, offset + 1.5, 0.25, root_midi, velocity_base)
            add_midi_note(bass_take, offset + 2.0, 0.25, root_midi, velocity_base)
            add_midi_note(bass_take, offset + 2.75, 0.25, root_midi, velocity_base - 10)
        # Sustained sidechain section for last 2 bars
        else:
            add_midi_note(bass_take, offset + 0.0, 4.0, root_midi, velocity_base - 5)

    RPR.RPR_MIDI_Sort(bass_take)

    # === TRACK 3: DARK PROPHET PADS (Sidechained) ===
    RPR.RPR_InsertTrackAtIndex(num_tracks + 2, True)
    pad_track = RPR.RPR_GetTrack(0, num_tracks + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", f"{track_name} - Dark Pads", True)

    # Add Pad FX Chain
    pad_synth = RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, pad_synth, 3, 1.0) # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(pad_track, pad_synth, 0, -6.0) # Lower volume
    RPR.RPR_TrackFX_AddByName(pad_track, "JS: Chorus", False, -1)
    
    # 1/4 note ducking to simulate kick sidechain (Shapebox style)
    trem_idx = RPR.RPR_TrackFX_AddByName(pad_track, "JS: Tremolo", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, trem_idx, 0, 2.0) # Amount
    
    pad_item = RPR.RPR_AddMediaItemToTrack(pad_track)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pad_item, "D_LENGTH", item_length_sec)
    pad_take = RPR.RPR_AddTakeToMediaItem(pad_item)

    # Dark Harmonic Minor Progression: i -> i -> iv -> V
    progression = [
        [0, 2, 4], # i
        [0, 2, 4], # i
        [3, 5, 0], # iv (inversion)
        [4, 6, 1]  # V (incorporates the raised 7th of harmonic minor)
    ]

    for b in range(bars):
        offset = b * beats_per_bar
        chord_idx = b % len(progression)
        chord_degrees = progression[chord_idx]
        
        for degree in chord_degrees:
            # Handle octave wraparound for inversions
            octave_shift = 12 if degree < chord_degrees[0] else 0
            # Wrap degree to scale bounds safely
            mapped_pitch = root_midi + 12 + scale_intervals[degree % len(scale_intervals)] + octave_shift
            add_midi_note(pad_take, offset, 4.0, mapped_pitch, velocity_base - 20)

    RPR.RPR_MIDI_Sort(pad_take)

    # Update REAPER UI
    RPR.RPR_UpdateArrange()

    return f"Created {track_name} (3 tracks: Fuzz Drums, Detuned Bass, Dark Pads) over {bars} bars at {bpm} BPM in {key} {scale}."
