def create_pattern(
    project_name: str = "GFunk_Project",
    track_name: str = "G-Funk",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create a G-Funk Foundation (Smooth Chords + Bouncy Bass + Drums) in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (must be multiple of 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "minor" # Fallback to minor as G-Funk is heavily minor/dorian
        
    scale_arr = SCALES[scale]
    root_midi = 48 + NOTE_MAP[key] # Base octave is C3 (48)

    # Helper function to get correct pitch based on scale degree
    def get_midi_pitch(degree):
        octave = degree // len(scale_arr)
        scale_idx = degree % len(scale_arr)
        return root_midi + (octave * 12) + scale_arr[scale_idx]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar

    # ==========================================
    # TRACK 1: G-FUNK CHORDS (Electric Piano)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    idx_chords = RPR.RPR_CountTracks(0) - 1
    track_chords = RPR.RPR_GetTrack(0, idx_chords)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name} EP Chords", True)

    item_chords = RPR.RPR_CreateNewMIDIItemInProj(track_chords, 0.0, bars * bar_length_sec, False)
    take_chords = RPR.RPR_GetActiveTake(item_chords)

    # Progression Degrees (Relative to root C3): 1-6-5-4
    # i9, VImaj7, v7, iv7
    chord_voicings = [
        [-7, 0, 2, 4, 6],  # i9
        [-9, 2, 4, 7],     # VImaj7
        [-10, 1, 3, 6],    # v7
        [-11, 0, 2, 5]     # iv7
    ]

    for bar in range(bars):
        start_qn = bar * beats_per_bar
        chord_idx = bar % 4
        voicing = chord_voicings[chord_idx]
        
        for degree in voicing:
            pitch = get_midi_pitch(degree)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_chords, start_qn + 3.8) # Leave slight gap
            vel = velocity_base - 10 # Keep chords soft
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
            
    RPR.RPR_MIDI_Sort(take_chords)
    
    # Basic ReaSynth setup to simulate soft EP
    fx_chords = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 1, 0.0) # Saw mix 0
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 2, 0.0) # Square mix 0
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 3, 0.5) # Triangle mix
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 4, 0.8) # Extra sine
    RPR.RPR_TrackFX_SetParam(track_chords, fx_chords, 7, 0.5) # Release time

    # ==========================================
    # TRACK 2: G-FUNK BASS (Bouncy Synth/Slap)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    idx_bass = RPR.RPR_CountTracks(0) - 1
    track_bass = RPR.RPR_GetTrack(0, idx_bass)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name} Bass", True)

    item_bass = RPR.RPR_CreateNewMIDIItemInProj(track_bass, 0.0, bars * bar_length_sec, False)
    take_bass = RPR.RPR_GetActiveTake(item_bass)

    # Bass rhythm pattern per bar (QN offsets, degree offset from root)
    bass_patterns = [
        [(0.0, -7, 1.0), (1.5, 0, 0.5), (3.5, -5, 0.5)],   # Bar 1 (i)
        [(0.0, -9, 1.0), (1.5, -2, 0.5), (3.5, -10, 0.5)], # Bar 2 (VI)
        [(0.0, -10, 1.0), (1.5, -3, 0.5), (3.5, -11, 0.5)],# Bar 3 (v)
        [(0.0, -11, 1.0), (1.5, -4, 0.5), (3.5, -10, 0.5)] # Bar 4 (iv)
    ]

    for bar in range(bars):
        start_qn = bar * beats_per_bar
        pattern = bass_patterns[bar % 4]
        
        for qn_offset, degree, length in pattern:
            pitch = get_midi_pitch(degree)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, start_qn + qn_offset)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_bass, start_qn + qn_offset + length)
            # Octave jumps (length 0.5 at offbeat) get higher velocity for the slap/pop feel
            vel = velocity_base + 30 if qn_offset == 1.5 else velocity_base + 10
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    RPR.RPR_MIDI_Sort(take_bass)

    # Basic ReaSynth setup for synth bass
    fx_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 1, 0.7) # Saw mix
    RPR.RPR_TrackFX_SetParam(track_bass, fx_bass, 2, 0.3) # Square mix
    
    # Add EQ to roll off highs for the bass
    eq_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track_bass, eq_bass, 12, 0.0) # High shelf gain down

    # ==========================================
    # TRACK 3: BASIC DRUMS (Boom Bap Groove)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    idx_drums = RPR.RPR_CountTracks(0) - 1
    track_drums = RPR.RPR_GetTrack(0, idx_drums)
    RPR.RPR_GetSetMediaTrackInfo_String(track_drums, "P_NAME", f"{track_name} Drums", True)

    item_drums = RPR.RPR_CreateNewMIDIItemInProj(track_drums, 0.0, bars * bar_length_sec, False)
    take_drums = RPR.RPR_GetActiveTake(item_drums)

    # Standard GM Drum mapping
    KICK = 36
    SNARE = 38
    HIHAT = 42

    for bar in range(bars):
        start_qn = bar * beats_per_bar
        
        # Kick (1, 2-and, 3.5 syncopation)
        for qn in [0.0, 1.5, 2.5]:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn + 0.25)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, KICK, 100, False)
            
        # Snare (2, 4)
        for qn in [1.0, 3.0]:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn + 0.25)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, SNARE, 110, False)
            
        # Hi-Hats (Eighth notes)
        for i in range(8):
            qn = i * 0.5
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take_drums, start_qn + qn + 0.25)
            # Accent downbeats
            vel = 90 if i % 2 == 0 else 70
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, start_ppq, end_ppq, 9, HIHAT, vel, False)

    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created G-Funk Groove ('{track_name}'): 3 tracks ({bars} bars at {bpm} BPM in {key} {scale}) with 1-6-5-4 smooth chords, bouncy octave bass, and drums."
