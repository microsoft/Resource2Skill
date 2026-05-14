def create_pattern(
    project_name: str = "PhaseOptimizedLowEnd",
    track_name: str = "Kick & Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Phase-Optimized Kick and Bass setup using harmonic saturation 
    and transient expansion to prevent low-end phase cancellation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Helper function to convert note to MIDI pitch
    def get_midi_pitch(root_note, octave, scale_type, degree):
        root_pitch = NOTE_MAP.get(root_note.upper().capitalize(), 0)
        scale_intervals = SCALES.get(scale_type, SCALES["minor"])
        interval = scale_intervals[degree % len(scale_intervals)]
        octave_offset = degree // len(scale_intervals)
        return (octave + 1 + octave_offset) * 12 + root_pitch + interval

    # Define frequencies/pitches
    # Kick is rooted extremely low (Octave 1)
    kick_pitch = get_midi_pitch(key, 1, scale, 0)
    # Bass is rooted an octave higher (Octave 2) to naturally avoid phase masking
    bass_pitch = get_midi_pitch(key, 2, scale, 0)

    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # 2. Create Tracks
    track_idx = RPR.RPR_CountTracks(0)
    
    # KICK TRACK
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    kick_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(kick_track, "P_NAME", "Optimized Kick", True)
    
    # BASS TRACK
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", "Optimized Bass", True)

    # 3. Add FX Chains
    # Kick FX: Synth -> Saturation -> Transient Controller
    kick_synth_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    # Set ReaSynth as a percussive kick: fast decay, no sustain
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth_idx, 0, 0.7)  # Vol
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth_idx, 2, 0.0)  # Attack 0ms
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth_idx, 3, 0.2)  # Decay ~100ms
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth_idx, 4, 0.0)  # Sustain 0
    RPR.RPR_TrackFX_SetParam(kick_track, kick_synth_idx, 5, 0.05) # Release fast
    
    # Harmonic Excitement (JS: Saturation)
    kick_sat_idx = RPR.RPR_TrackFX_AddByName(kick_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_sat_idx, 0, 50.0) # Amount % (generates upper harmonics)

    # Transient Enhancement (JS: Transient Controller)
    kick_trans_idx = RPR.RPR_TrackFX_AddByName(kick_track, "JS: Transient Controller", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, kick_trans_idx, 0, 30.0) # Attack +30% (emphasizes first 50ms)

    # Bass FX: Synth -> Saturation
    bass_synth_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Set ReaSynth as a sustained sub bass
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth_idx, 0, 0.6)  # Vol
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth_idx, 2, 0.05) # Attack (slight fade to avoid click)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth_idx, 4, 1.0)  # Sustain full
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth_idx, 5, 0.1)  # Release short
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth_idx, 6, 0.3)  # Sawtooth mix (for natural harmonics)

    # Harmonic Excitement (JS: Saturation)
    bass_sat_idx = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_sat_idx, 0, 40.0) # Amount %

    # 4. Create MIDI Items & Patterns
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Create Kick Item
    kick_item = RPR.RPR_AddMediaItemToTrack(kick_track)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(kick_item, "D_LENGTH", total_length_sec)
    kick_take = RPR.RPR_AddTakeToMediaItem(kick_item)
    RPR.RPR_MIDI_InsertEvt(kick_take, False, False, 0, bytes([0x90, 0, 0]), 3) # Initialize MIDI take

    # Create Bass Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    RPR.RPR_MIDI_InsertEvt(bass_take, False, False, 0, bytes([0x90, 0, 0]), 3)

    # Determine PPQ (Pulses Per Quarter Note)
    ppq = 960

    for bar in range(bars):
        for beat in range(beats_per_bar):
            # KICK: On the downbeats (0, 1, 2, 3)
            kick_start_ppq = (bar * beats_per_bar + beat) * ppq
            kick_end_ppq = kick_start_ppq + int(ppq * 0.25) # 1/16th note length
            
            RPR.RPR_MIDI_InsertNote(kick_take, False, False, 
                                    kick_start_ppq, kick_end_ppq, 
                                    0, kick_pitch, velocity_base, False)

            # BASS: On the off-beats (0.5, 1.5, 2.5, 3.5)
            # This compositional separation + harmonic mixing solves the phase cancellation perfectly.
            bass_start_ppq = (bar * beats_per_bar + beat + 0.5) * ppq
            bass_end_ppq = bass_start_ppq + int(ppq * 0.5) # 1/8th note length
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, 
                                    int(bass_start_ppq), int(bass_end_ppq), 
                                    0, bass_pitch, int(velocity_base * 0.9), False)

    # Force REAPER to redraw and apply the MIDI edits
    RPR.RPR_MIDI_Sort(kick_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created Phase-Optimized Kick & Bass over {bars} bars at {bpm} BPM in {key} {scale}. Applied Saturation and Transient Enhancement to resolve phase issues."
