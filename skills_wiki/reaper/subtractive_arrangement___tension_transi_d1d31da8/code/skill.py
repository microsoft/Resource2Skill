def create_pattern(
    project_name: str = "Arrangement",
    track_name: str = "Arrangement_Root",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 20,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Subtractive Beat Arrangement with Riser and Filter Transitions.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the generated arrangement structure.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Total length (overridden by fixed arrangement map for demonstration).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    root_bass = 36 + root_val # C2 range
    root_mid = 60 + root_val  # C4 range
    third_val = scale_intervals[2]
    fifth_val = scale_intervals[4]
    chord_notes = [root_mid, root_mid + third_val, root_mid + fifth_val]

    # Step 1: Initialize Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    def beat_to_time(b):
        return (60.0 / bpm) * b

    # Track creation helper with folder depth management
    track_count = RPR.RPR_CountTracks(0)
    def new_track(name, depth=0):
        nonlocal track_count
        RPR.RPR_InsertTrackAtIndex(track_count, True)
        trk = RPR.RPR_GetTrack(0, track_count)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", f"{track_name} {name}", True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "I_FOLDERDEPTH", depth)
        
        # Add a basic placeholder synth so the arrangement is audible
        RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
        track_count += 1
        return trk

    # Step 2: Build Routing & Folder Structure
    t_drums = new_track("DRUMS", 1)      # Start Folder
    t_kick = new_track("Kick", 0)
    t_snare = new_track("Snare", 0)
    t_hihat = new_track("Hihats", -1)    # End Folder

    t_inst = new_track("INSTRUMENTS", 1) # Start Folder
    t_chords = new_track("Chords", 0)
    t_lead = new_track("Lead", -1)       # End Folder

    t_bass = new_track("Bass", 0)
    t_fx = new_track("FX (Riser)", 0)

    # Step 3: MIDI generation helper
    def create_midi_part(track, type_name, start_beat, end_beat):
        start_time = beat_to_time(start_beat)
        end_time = beat_to_time(end_beat)
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", end_time - start_time)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Loop generating notes every 4 beats (1 bar)
        for b in range(int(start_beat), int(end_beat), 4):
            notes = []
            if type_name == "kick":
                notes = [(0, 1, 36), (2.5, 3, 36)]
            elif type_name == "snare":
                if start_beat == 16: # V1a (Half-time energy drop)
                    notes = [(2, 3, 60)]
                else:
                    notes = [(1, 2, 60), (3, 4, 60)]
            elif type_name == "hihat":
                if start_beat == 16: # V1a (Sparse)
                    notes = [(0, 0.25, 72), (1, 1.25, 72), (2, 2.25, 72), (3, 3.25, 72)]
                else:
                    notes = [(i*0.5, i*0.5+0.25, 72) for i in range(8)]
            elif type_name == "chords":
                notes = [(0, 3.8, chord_notes[0]), (0, 3.8, chord_notes[1]), (0, 3.8, chord_notes[2])]
            elif type_name == "bass":
                notes = [(0, 1.5, root_bass), (2.5, 3.8, root_bass)]
            elif type_name == "lead":
                notes = [(0, 0.5, root_mid + 12), (1.5, 2.0, root_mid + 12 + scale_intervals[1]), (3, 3.5, root_mid + 12 + fifth_val)]
            elif type_name == "riser":
                notes = [(0, 4.0, 60)]

            for offset_start, offset_end, pitch in notes:
                abs_s = b + offset_start
                abs_e = b + offset_end
                if abs_s >= end_beat: continue

                ppq_s = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_to_time(abs_s))
                ppq_e = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_to_time(abs_e))
                RPR.RPR_MIDI_InsertNote(take, False, False, ppq_s, ppq_e, 0, pitch, velocity_base, False)
                
        RPR.RPR_MIDI_Sort(take)

    # Step 4: Map the Arrangement (Subtractive Methodology)
    # Intro (Bars 1-5 / Beats 0-16)
    create_midi_part(t_chords, "chords", 0, 16)

    # Verse 1a (Bars 5-9 / Beats 16-32) - Subtractive (No Kick/Bass, half-time snare)
    create_midi_part(t_chords, "chords", 16, 32)
    create_midi_part(t_snare, "snare", 16, 32)
    create_midi_part(t_hihat, "hihat", 16, 32)

    # Verse 1b (Bars 9-13 / Beats 32-48) - Build up
    create_midi_part(t_chords, "chords", 32, 48)
    create_midi_part(t_kick, "kick", 32, 48)
    create_midi_part(t_snare, "snare", 32, 48)
    create_midi_part(t_hihat, "hihat", 32, 48)
    create_midi_part(t_bass, "bass", 32, 48)

    # Chorus (Bars 13-21 / Beats 48-80) - Full Energy
    create_midi_part(t_chords, "chords", 48, 80)
    create_midi_part(t_lead, "lead", 48, 80)
    create_midi_part(t_kick, "kick", 48, 80)
    create_midi_part(t_snare, "snare", 48, 80)
    create_midi_part(t_hihat, "hihat", 48, 80)
    create_midi_part(t_bass, "bass", 48, 80)

    # Riser Item (Beat 44-48, right before chorus)
    create_midi_part(t_fx, "riser", 44, 48)

    # Step 5: Transitions & Automation
    # 5a. Riser Volume Swell
    fx_idx_vol = RPR.RPR_TrackFX_AddByName(t_fx, "JS: Volume Adjustment", False, -1)
    if fx_idx_vol >= 0:
        env_vol = RPR.RPR_GetFXEnvelope(t_fx, fx_idx_vol, 0, True) # Param 0 is Volume dB
        if env_vol:
            RPR.RPR_InsertEnvelopePoint(env_vol, beat_to_time(44), -60.0, 0, 0, False, True)
            RPR.RPR_InsertEnvelopePoint(env_vol, beat_to_time(48), 0.0, 0, 0, False, True)
            RPR.RPR_Envelope_SortPoints(env_vol)

    # 5b. Instrument Bus Lowpass Filter Sweep
    fx_idx_eq = RPR.RPR_TrackFX_AddByName(t_inst, "ReaEQ", False, -1)
    if fx_idx_eq >= 0:
        env_filter = RPR.RPR_GetFXEnvelope(t_inst, fx_idx_eq, 9, True) # Param 9 is Band 4 Frequency
        if env_filter:
            RPR.RPR_InsertEnvelopePoint(env_filter, beat_to_time(44), 1.0, 0, 0, False, True)   # Open
            RPR.RPR_InsertEnvelopePoint(env_filter, beat_to_time(48), 0.2, 0, 0, False, True)   # Muffled/Tension
            RPR.RPR_InsertEnvelopePoint(env_filter, beat_to_time(48.01), 1.0, 0, 0, False, True)# Snap back for Chorus
            RPR.RPR_Envelope_SortPoints(env_filter)

    return f"Created subtractive arrangement structure with filter/riser transitions from Bar 1 to 21 at {bpm} BPM in {key} {scale}."
