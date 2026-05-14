def create_pattern(
    project_name: str = "Trap Foundation",
    bpm: int = 140,
    key: str = "C#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Dark Trap/Drill foundation including block chords, an arpeggiated layer,
    and trap hi-hats with 1/32nd rolls.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    # Input validation and setup
    root_val = NOTE_MAP.get(key, 1) # Default to C#
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    qn_sec = 60.0 / bpm
    bar_sec = qn_sec * 4.0
    item_length = bar_sec * bars

    def get_scale_note(degree, base_octave=4):
        """Convert a scale degree (0-indexed) to a MIDI note number."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_val + ((base_octave + octave_shift) * 12) + scale_intervals[scale_idx]

    def create_track_with_midi(name, fx_settings=None):
        """Helper to create a track, add a MIDI item, and setup ReaSynth."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Add placeholder synth
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        if fx_settings:
            for param, val in fx_settings.items():
                RPR.RPR_TrackFX_SetParam(track, fx_idx, param, val)
                
        return take

    # ==========================================
    # 1. TRAP PIANO (Block Chords: i - VI)
    # ==========================================
    # ReaSynth Piano-ish settings (Saw/Square blend, fast decay)
    piano_fx = {1: 0.0, 2: 0.3, 3: 0.1, 4: 0.3, 5: 0.5, 7: 0.2}
    piano_take = create_track_with_midi("Trap Piano (Chords)", piano_fx)
    
    for bar in range(bars):
        # Alternate between i chord (degrees 0, 2, 4) and VI chord (degrees 5, 7, 9)
        chord_degrees = [0, 2, 4] if bar % 2 == 0 else [5, 7, 9]
        
        start_time = bar * bar_sec
        end_time = start_time + bar_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(piano_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(piano_take, end_time)
        
        for deg in chord_degrees:
            pitch = get_scale_note(deg, base_octave=4)
            RPR.RPR_MIDI_InsertNote(piano_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 10, False)
    
    RPR.RPR_MIDI_Sort(piano_take)

    # ==========================================
    # 2. ARP LAYER (1/8th notes)
    # ==========================================
    # ReaSynth Sine Pluck settings
    arp_fx = {1: 0.0, 2: 0.1, 3: 0.0, 4: 0.1, 5: 0.0, 7: 0.0}
    arp_take = create_track_with_midi("Trap Arp", arp_fx)
    
    for bar in range(bars):
        chord_degrees = [0, 2, 4] if bar % 2 == 0 else [5, 7, 9]
        for eighth_step in range(8):
            start_time = (bar * bar_sec) + (eighth_step * (qn_sec / 2.0))
            end_time = start_time + (qn_sec / 2.0) - 0.05 # Staccato gap
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(arp_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(arp_take, end_time)
            
            # Cycle through chord notes
            deg = chord_degrees[eighth_step % len(chord_degrees)]
            pitch = get_scale_note(deg, base_octave=5) # 1 octave higher
            
            RPR.RPR_MIDI_InsertNote(arp_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(arp_take)

    # ==========================================
    # 3. TRAP HI-HATS (1/8th base + 1/32nd rolls)
    # ==========================================
    # ReaSynth Noise mode to emulate a short hi-hat click
    hat_fx = {1: 0.0, 2: 0.02, 3: 0.0, 4: 0.01, 5: 0.0, 6: 1.0, 7: 0.0}
    hat_take = create_track_with_midi("Trap Hats", hat_fx)
    hat_pitch = 60 # C4
    
    for bar in range(bars):
        for beat in range(4):
            for eighth in range(2):
                step_time = (bar * bar_sec) + (beat * qn_sec) + (eighth * (qn_sec / 2.0))
                
                # Create a 1/32nd note roll on beat 4 of alternating bars
                is_roll = (bar % 2 != 0) and (beat == 3)
                
                if is_roll:
                    # Insert 4 rapid notes (1/32nds) in the space of this 1/8th note
                    step_32 = (qn_sec / 2.0) / 4.0
                    for sub in range(4):
                        roll_start = step_time + (sub * step_32)
                        roll_end = roll_start + step_32 - 0.01
                        
                        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(hat_take, roll_start)
                        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(hat_take, roll_end)
                        
                        # Ramp velocity down for effect
                        roll_vel = velocity_base - (sub * 10) 
                        RPR.RPR_MIDI_InsertNote(hat_take, False, False, start_ppq, end_ppq, 0, hat_pitch, roll_vel, False)
                else:
                    # Standard 1/8th note hat
                    hat_end = step_time + 0.05 # Short hit
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(hat_take, step_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(hat_take, hat_end)
                    
                    # Accent the on-beats slightly
                    vel = velocity_base if eighth == 0 else velocity_base - 20
                    RPR.RPR_MIDI_InsertNote(hat_take, False, False, start_ppq, end_ppq, 0, hat_pitch, vel, False)

    RPR.RPR_MIDI_Sort(hat_take)
    RPR.RPR_UpdateArrange()

    return f"Created Trap Foundation (Piano, Arp, Hats) in {key} {scale} over {bars} bars at {bpm} BPM."
