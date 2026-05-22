def create_algorithmic_bass_and_offbeat_synth(
    project_name: str = "GrooveProject",
    bpm: int = 120,
    key: str = "G",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an electronic groove featuring a sequenced 16th-note pentatonic 
    bassline and an offbeat synth, approximating the setup from the tutorial.

    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'G').
        scale: Scale type (defaults to 'pentatonic_minor' as seen in the video).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Fallback to minor pentatonic if scale not found
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    root_idx = NOTE_MAP.get(key.capitalize(), 7) # Default to G
    
    # Octave 2 for Bass (~MIDI 36-47), Octave 4 for Synth (~MIDI 60-71)
    bass_root_midi = root_idx + 36 
    synth_root_midi = root_idx + 60

    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_len_sec = 60.0 / bpm
    bar_len_sec = beat_len_sec * 4
    total_length_sec = bar_len_sec * bars

    def add_midi_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # ==========================================
    # === Step 2: 16th Note Bassline Track ===
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{key} {scale} Bass Sequence", True)

    # Bass FX: ReaSynth -> ReaEQ (Lowpass)
    synth_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 0, 0.5)  # Vol
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 2, 0.7)  # Square Mix
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 3, 0.8)  # Saw Mix
    
    eq_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    # Set Band 4 to LowPass (Type 8 usually, index 3 is band 4)
    RPR.RPR_TrackFX_SetParam(bass_track, eq_fx, 11, 800.0 / 24000.0) # Approx 800Hz Cutoff

    # Bass MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Simulating the Reason Bassline Generator algorithm (1 bar repeating pattern)
    # Indices map to the chosen scale (0=Root, 1=m3, 2=P4, 3=P5)
    seq_pattern = [0, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 3, 1, 0, 0]
    
    for bar in range(bars):
        bar_start_time = bar * bar_len_sec
        for step in range(16):
            step_time = bar_start_time + (step * (beat_len_sec / 4.0))
            note_duration = (beat_len_sec / 4.0) * 0.85 # Staccato 16th
            
            scale_degree = seq_pattern[step]
            # Ensure we wrap around the scale if degree is higher than scale length
            octave_shift = (scale_degree // len(scale_intervals)) * 12
            interval = scale_intervals[scale_degree % len(scale_intervals)]
            
            pitch = bass_root_midi + interval + octave_shift
            
            # Accent the downbeats slightly
            vel = velocity_base if step % 4 == 0 else velocity_base - 15
            add_midi_note(bass_take, step_time, step_time + note_duration, pitch, vel)

    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # === Step 3: Offbeat Synth Track ===
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", "Offbeat Synth Stabs", True)

    # Synth FX: ReaSynth -> ReaEQ (Highpass)
    synth_fx2 = RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx2, 0, 0.4)  # Vol
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx2, 2, 0.9)  # Square focus
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx2, 3, 0.1)  # Low saw
    RPR.RPR_TrackFX_SetParam(synth_track, synth_fx2, 4, 0.1)  # Fast decay
    
    eq_fx2 = RPR.RPR_TrackFX_AddByName(synth_track, "ReaEQ", False, -1)
    # Add Highpass to keep it out of the bass
    RPR.RPR_TrackFX_SetParam(synth_track, eq_fx2, 0, 400.0 / 24000.0)

    # Synth MIDI Item
    synth_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length_sec)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    # Generate minor triad chords on the 1/8th offbeats (the "ands")
    synth_chord = [
        synth_root_midi,
        synth_root_midi + scale_intervals[1], # minor 3rd
        synth_root_midi + scale_intervals[3]  # perfect 5th
    ]

    for bar in range(bars):
        bar_start_time = bar * bar_len_sec
        for beat in range(4):
            # Calculate the "and" of the beat (beat + 0.5)
            offbeat_start = bar_start_time + (beat * beat_len_sec) + (beat_len_sec * 0.5)
            note_duration = (beat_len_sec / 2.0) * 0.7 # Plucky/staccato 8th
            
            for pitch in synth_chord:
                add_midi_note(synth_take, offbeat_start, offbeat_start + note_duration, pitch, velocity_base - 10)

    RPR.RPR_MIDI_Sort(synth_take)

    # Update REAPER UI
    RPR.RPR_UpdateArrange()

    return f"Created Bassline and Offbeat Synth groove in {key} {scale} over {bars} bars at {bpm} BPM."
