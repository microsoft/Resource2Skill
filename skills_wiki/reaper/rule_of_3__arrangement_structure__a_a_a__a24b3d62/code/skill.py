def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Arp",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create an A-A-A' Arrangement ("Rule of 3") in the current REAPER project.
    Generates a 12-bar item that repeats an idea twice, then subverts it on the third time.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (forces 12 bars to properly demonstrate the 3-part rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    base_midi = NOTE_MAP.get(key.capitalize(), 0) + 60 # Default to Octave 4
    scale_arr = SCALES.get(scale.lower(), SCALES["major"])

    def get_diatonic_pitch(root_note, scale_intervals, degree):
        """Converts a 0-indexed scale degree into a MIDI pitch."""
        octaves = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_note + scale_intervals[idx] + (octaves * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure ReaSynth for Plucky Keyboard Sound ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param 2: Attack (0.0 = fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01)
    # Param 3: Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)
    # Param 4: Sustain (low for plucky feel)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.1)
    # Param 5: Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # Hardcoded to 12 to demonstrate the 3-part rule
    item_length_sec = (60.0 / bpm) * beats_per_bar * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Implement the "Rule of 3" Pattern ===
    # Phrase A: I - V - vi - IV (Degrees: 0, 4, 5, 3)
    # Phrase A': I - V - ii - V (Degrees: 0, 4, 1, 4) -> Diverges halfway!
    
    progression_structure = [
        [0, 4, 5, 3], # Bar 1-4: Play Idea
        [0, 4, 5, 3], # Bar 5-8: Repeat Idea
        [0, 4, 1, 4]  # Bar 9-12: Subvert Idea (Change ending)
    ]

    def insert_note(start_beat, end_beat, pitch, vel):
        """Helper to insert a note via time -> PPQ conversion."""
        start_time = (60.0 / bpm) * start_beat
        end_time = (60.0 / bpm) * end_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    current_beat = 0.0
    note_count = 0

    for phrase in progression_structure:
        for chord_degree in phrase:
            # 1. Left Hand Bass Note (Whole Note, Octave 2)
            bass_pitch = get_diatonic_pitch(base_midi - 24, scale_arr, chord_degree)
            insert_note(current_beat, current_beat + 4.0, bass_pitch, max(10, velocity_base - 15))
            note_count += 1

            # 2. Right Hand Arpeggio (Eighth Notes, Octave 4)
            # Pattern: Root, 3rd, 5th, 3rd, Root, 3rd, 5th, 3rd
            arp_intervals = [0, 2, 4, 2, 0, 2, 4, 2] 
            
            for i, interval in enumerate(arp_intervals):
                arp_degree = chord_degree + interval
                arp_pitch = get_diatonic_pitch(base_midi, scale_arr, arp_degree)
                
                start_b = current_beat + (i * 0.5)
                end_b = start_b + 0.45 # slight staccato
                
                # Accents on downbeats
                vel = velocity_base if i % 2 == 0 else velocity_base - 15
                insert_note(start_b, end_b, arp_pitch, vel)
                note_count += 1
                
            current_beat += 4.0 # Move to next bar

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-A' form). {note_count} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
