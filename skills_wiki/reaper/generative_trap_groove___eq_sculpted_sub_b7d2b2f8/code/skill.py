def create_pattern(
    project_name: str = "Trap_Sub_And_Groove",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative-style Trap Drum Loop and an EQ-sculpted Sub Bass track
    (mimicking the Massive X + Bassroom + Reason Rack workflow).
    """
    import reaper_python as RPR

    # Music theory map to get the root note
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_pitch_class = NOTE_MAP.get(key, 0)
    # Put the sub bass in octave 2 (MIDI notes 24-35)
    sub_midi_note = 24 + root_pitch_class 

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beat_length = 60.0 / bpm
    bar_length = beat_length * 4.0
    total_length = bar_length * bars

    # ==========================================
    # TRACK 1: Algorithmic Drum Beat (Reason Rack Emulation)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", "Generative Drum Loop", True)

    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, total_length, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)

    for b in range(bars):
        bar_start = b * bar_length
        
        # 1. Kicks (MIDI 36) - Syncopated Trap feel: Beat 1 and Beat 2.5
        kicks = [0.0, 1.5]
        for beat_offset in kicks:
            pos_sec = bar_start + (beat_offset * beat_length)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec + (beat_length * 0.25))
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, 36, velocity_base, "")

        # 2. Snare (MIDI 38) - Half-time feel: Beat 3
        pos_sec = bar_start + (2.0 * beat_length)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec + (beat_length * 0.25))
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, 38, velocity_base, "")

        # 3. Hi-Hats (MIDI 42) - Driving 8th notes
        for eighth in range(8):
            pos_sec = bar_start + (eighth * (beat_length * 0.5))
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, pos_sec + (beat_length * 0.2))
            vel = velocity_base if eighth % 2 == 0 else int(velocity_base * 0.7) # Accent on downbeats
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 9, 42, vel, "")

    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # TRACK 2: Processed Sub Bass (Massive X + Bassroom Emulation)
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    sub_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(sub_track, "P_NAME", "Sculpted Sub Bass", True)

    sub_item = RPR.RPR_CreateNewMIDIItemInProj(sub_track, 0.0, total_length, False)
    sub_take = RPR.RPR_GetActiveTake(sub_item)

    # Add a continuous, sustained sub bass note covering the duration
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(sub_take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(sub_take, total_length)
    RPR.RPR_MIDI_InsertNote(sub_take, False, False, start_ppq, end_ppq, 0, sub_midi_note, 110, "")
    RPR.RPR_MIDI_Sort(sub_take)

    # --- Sound Design FX Chain ---
    
    # 1. ReaSynth (Acting as Massive X Sub Preset)
    synth_idx = RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)
    # Params: 0=Vol, 1=Tune, 2=Square, 3=Saw, 4=Tri, 5=ExtraSine
    RPR.RPR_TrackFX_SetParamNormalized(sub_track, synth_idx, 0, 0.5)  # Reduce Volume slightly
    RPR.RPR_TrackFX_SetParamNormalized(sub_track, synth_idx, 2, 0.0)  # No Square
    RPR.RPR_TrackFX_SetParamNormalized(sub_track, synth_idx, 3, 0.0)  # No Saw
    RPR.RPR_TrackFX_SetParamNormalized(sub_track, synth_idx, 5, 0.0)  # Pure Sine

    # 2. ReaEQ (Acting as BASSROOM mix sculpting plugin)
    eq_idx = RPR.RPR_TrackFX_AddByName(sub_track, "ReaEQ", False, -1)
    
    # The BASSROOM Mix Moves:
    # Band 1: High Pass at 20Hz (cut sub-audible rumble)
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 0, 20.0)    # Freq
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 1, 0.0)     # Gain
    
    # Band 2: Sub fundamental boost around 45Hz
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 3, 45.0)    # Freq
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 4, 3.0)     # Gain (+3dB Boost)
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 5, 1.5)     # Q
    
    # Band 3: Low-mid "mud" cut around 250Hz (Makes room for snare)
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 6, 250.0)   # Freq
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 7, -4.0)    # Gain (-4dB Cut)
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 8, 2.0)     # Q

    return f"Created Generative Drum Loop & Bassroom-Sculpted Sub Bass (Key: {key}, {bars} bars at {bpm} BPM)."
