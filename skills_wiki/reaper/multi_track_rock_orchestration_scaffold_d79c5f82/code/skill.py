def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Arrangement",
    bpm: int = 120,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Track Rock Orchestration Scaffold in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (should be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Base MIDI note mapping (C3 = 48)
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    base_midi = NOTE_MAP.get(key.capitalize(), 50)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Define standard 4-chord progression based on scale
    if scale.lower() == "major":
        degrees = [5, 3, 0, 4]  # vi - IV - I - V
    else:
        degrees = [0, 5, 2, 6]  # i - VI - III - VII

    def get_chord_notes(root_midi, scale_int, degree):
        """Helper to get Root, 3rd, and 5th pitches for a given scale degree (0-indexed)."""
        def get_pitch(deg):
            octave = deg // 7
            idx = deg % 7
            return root_midi + (octave * 12) + scale_int[idx]
        return [get_pitch(degree), get_pitch(degree + 2), get_pitch(degree + 4)]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Folder Track Structure ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Parent Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    parent_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1) # Start folder

    instrument_roles = ["Drums", "Bass", "Rhythm Guitar", "Lead Guitar"]
    
    # Pre-calculate project timings
    total_length_sec = bars * 4 * (60.0 / bpm)
    
    # Create children tracks
    for i, role in enumerate(instrument_roles):
        child_idx = track_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(child_idx, True)
        child_track = RPR.RPR_GetTrack(0, child_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", role, True)
        
        if i == len(instrument_roles) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", -1) # End folder
            
        # Create MIDI Item for the child track
        item = RPR.RPR_CreateNewMIDIItemInProj(child_track, 0.0, total_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # === Step 3: Insert Musical Patterns ===
        for bar in range(bars):
            deg = degrees[bar % 4]
            chord = get_chord_notes(base_midi, scale_intervals, deg)
            
            # --- DRUMS ---
            if role == "Drums":
                for beat in range(4):
                    beat_abs = bar * 4 + beat
                    t_start = beat_abs * (60.0 / bpm)
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
                    
                    # Kick (36) on beats 1 & 3
                    if beat in [0, 2]:
                        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start + (60.0/bpm)*0.5)
                        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 36, velocity_base+10, False)
                    
                    # Snare (38) on beats 2 & 4
                    if beat in [1, 3]:
                        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start + (60.0/bpm)*0.5)
                        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 38, velocity_base+15, False)
                    
                    # Hi-Hats (42) straight 8ths
                    for hh in range(2):
                        hh_start = t_start + hh * (60.0 / bpm) * 0.5
                        hh_end = hh_start + (60.0 / bpm) * 0.25
                        ppq_h_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_start)
                        ppq_h_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_end)
                        v = velocity_base if hh == 0 else velocity_base - 20 # Accent
                        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_h_start, ppq_h_end, 0, 42, v, False)

            # --- BASS ---
            elif role == "Bass":
                root_pitch = int(chord[0] - 12) # Down an octave
                for eighth in range(8):
                    t_start = (bar * 4 + eighth * 0.5) * (60.0 / bpm)
                    t_end = t_start + (60.0 / bpm) * 0.45 # Detached 8th
                    ppq_s = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
                    ppq_e = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_s, ppq_e, 0, root_pitch, velocity_base+5, False)

            # --- RHYTHM GUITAR ---
            elif role == "Rhythm Guitar":
                # Power chords (Root, Fifth, Octave)
                p_chords = [int(chord[0]), int(chord[2]), int(chord[0] + 12)]
                t_start = bar * 4 * (60.0 / bpm)
                t_end = (bar * 4 + 4) * (60.0 / bpm) # Whole note
                ppq_s = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
                ppq_e = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
                for pitch in p_chords:
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_s, ppq_e, 0, pitch, velocity_base, False)

            # --- LEAD GUITAR ---
            elif role == "Lead Guitar":
                # Arpeggiate (Root, 3rd, 5th, Octave) two octaves up
                arp_notes = [int(chord[0]+24), int(chord[1]+24), int(chord[2]+24), int(chord[0]+36)]
                for sixteenth in range(16):
                    pitch = arp_notes[sixteenth % 4]
                    t_start = (bar * 4 + sixteenth * 0.25) * (60.0 / bpm)
                    t_end = t_start + (60.0 / bpm) * 0.2 # Staccato 16th
                    ppq_s = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
                    ppq_e = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_s, ppq_e, 0, pitch, velocity_base-10, False)
                    
        RPR.RPR_MIDI_Sort(take)

    # Update arrange view
    RPR.RPR_UpdateArrange()

    return f"Created Multi-Track Scaffold '{track_name}' (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
