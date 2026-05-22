def create_pattern(
    project_name: str = "MultiTrackWorkflow",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part Rock/Metal Multi-Track Scaffold in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (multiples of 4 work best).
        velocity_base: Base MIDI velocity (0-127).
    
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
    
    # Standard rock/pop progression relative to scale root
    # For minor: i (0), VI (5), III (2), VII (6)
    # For major: I (0), vi (5), IV (3), V (4)
    progression_indices = [0, 5, 2, 6] if scale == "minor" else [0, 5, 3, 4]
    
    if key not in NOTE_MAP or scale not in SCALES:
        return "Error: Invalid key or scale provided."
        
    root_midi = NOTE_MAP[key] + 48 # Base octave C3
    scale_intervals = SCALES[scale]

    # Helper function to compute pitch from scale degree
    def get_pitch(degree, octave_offset=0):
        octaves = degree // 7
        scale_idx = degree % 7
        return root_midi + scale_intervals[scale_idx] + ((octaves + octave_offset) * 12)

    # Helper function to generate track colors (R, G, B) to REAPER native format
    def make_color(r, g, b):
        return int(r + (g * 256) + (b * 65536)) | 0x1000000

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    item_length = beat_len * beats_per_bar * bars

    track_configs = [
        {"name": "Drums",      "color": make_color(255, 105, 180)}, # Pink
        {"name": "Bass",       "color": make_color(138, 43, 226)},  # Purple
        {"name": "Rhythm Gtr", "color": make_color(255, 140, 0)},   # Orange
        {"name": "Lead Gtr",   "color": make_color(30, 144, 255)}   # Blue
    ]

    base_track_idx = RPR.RPR_CountTracks(0)

    for i, cfg in enumerate(track_configs):
        track_idx = base_track_idx + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Set name and color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", cfg["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", cfg["color"])
        
        # Add basic synth to tonal tracks so they produce sound
        if cfg["name"] != "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # Populate MIDI data
        for bar in range(bars):
            chord_degree = progression_indices[bar % len(progression_indices)]
            bar_start_time = bar * beats_per_bar * beat_len
            
            if cfg["name"] == "Drums":
                # Kick/Snare/Hat pattern
                for beat in range(beats_per_bar):
                    beat_time = bar_start_time + (beat * beat_len)
                    
                    # Kick on 1 and 3, Snare on 2 and 4
                    is_snare = beat % 2 != 0
                    drum_pitch = 38 if is_snare else 36
                    
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + (beat_len * 0.5))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, drum_pitch, velocity_base, False)
                    
                    # 8th note hi-hats (2 per beat)
                    for eighth in range(2):
                        hh_time = beat_time + (eighth * (beat_len / 2.0))
                        hh_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time)
                        hh_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time + (beat_len * 0.25))
                        RPR.RPR_MIDI_InsertNote(take, False, False, hh_start, hh_end, 9, 42, int(velocity_base * 0.8), False)

            elif cfg["name"] == "Bass":
                # Driving 8th notes on root
                pitch = get_pitch(chord_degree, octave_offset=-2)
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * (beat_len / 2.0))
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (beat_len * 0.45)) # slight staccato
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

            elif cfg["name"] == "Rhythm Gtr":
                # Driving 8th notes (Power Chords: Root + 5th)
                root_p = get_pitch(chord_degree, octave_offset=-1)
                fifth_p = root_p + 7 # Strict perfect 5th for power chord
                
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * (beat_len / 2.0))
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (beat_len * 0.45))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_p, velocity_base, False)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fifth_p, velocity_base, False)

            elif cfg["name"] == "Lead Gtr":
                # Simple slower melodic motif (Root -> 3rd -> 5th based on the scale)
                melody_degrees = [chord_degree, chord_degree + 2, chord_degree + 4]
                
                for i, m_deg in enumerate(melody_degrees):
                    if i > 1 and bar % 2 != 0: 
                        continue # Leave space on alternating bars
                        
                    note_time = bar_start_time + (i * beat_len * 1.5)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + beat_len)
                    
                    pitch = get_pitch(m_deg, octave_offset=1)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base + 10, False)

        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track template (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {scale} at {bpm} BPM."
