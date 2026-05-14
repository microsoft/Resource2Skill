def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockBand",
    bpm: int = 130,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock Band Arrangement (Drums, Bass, Rhythm Gtr, Lead Gtr) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 2: Music Theory & Pitch Mapping ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.capitalize(), 11)  # Default to B

    # Generate a flat list of all diatonic notes across 10 octaves
    diatonic_notes = []
    for oct in range(11):
        for interval in scale_intervals:
            val = (oct * 12) + root_val + interval
            if 0 <= val <= 127:
                diatonic_notes.append(val)

    # Progression: Scale degrees 1, 6, 3, 7 (0-indexed: 0, 5, 2, 6)
    prog_indices = [0, 5, 2, 6]

    # === Step 3: Track & Item Creation ===
    roles = ["Drums", "Bass", "Rhythm_Guitar", "Lead_Guitar"]
    takes = {}

    for role in roles:
        # Create track
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        t_name = f"{track_name}_{role}"
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_name, True)

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes[role] = take

        # Add ReaSynth to tonal tracks to guarantee out-of-the-box sound
        if role != "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    def insert_note(take_ptr, start_sec, end_sec, pitch, vel):
        """Helper to safely add MIDI notes using absolute seconds converted to PPQ."""
        start_ppq = RPR.RPR_MIDI_TimeToPPQ(take_ptr, start_sec)
        end_ppq = RPR.RPR_MIDI_TimeToPPQ(take_ptr, end_sec)
        RPR.RPR_MIDI_InsertNote(take_ptr, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 4: Musical Arrangement Loop ===
    for b in range(bars):
        bar_start = b * bar_length_sec
        degree = prog_indices[b % 4]

        # --- A. Drums ---
        # Kick on 1 and 3
        insert_note(takes["Drums"], bar_start, bar_start + 0.1, 36, velocity_base)
        insert_note(takes["Drums"], bar_start + 2*sec_per_beat, bar_start + 2*sec_per_beat + 0.1, 36, velocity_base)
        # Snare on 2 and 4
        insert_note(takes["Drums"], bar_start + 1*sec_per_beat, bar_start + 1*sec_per_beat + 0.1, 38, velocity_base)
        insert_note(takes["Drums"], bar_start + 3*sec_per_beat, bar_start + 3*sec_per_beat + 0.1, 38, velocity_base)
        # Hi-hats on 8th notes (accents on downbeats)
        for eighth in range(8):
            time_ofs = eighth * (sec_per_beat / 2)
            vel = velocity_base if eighth % 2 == 0 else max(10, velocity_base - 25)
            insert_note(takes["Drums"], bar_start + time_ofs, bar_start + time_ofs + 0.1, 42, vel)
        # Crash on the very first downbeat
        if b == 0:
            insert_note(takes["Drums"], bar_start, bar_start + 0.1, 49, min(127, velocity_base + 15))

        # --- B. Bass ---
        bass_octave = 2
        bass_root_idx = (bass_octave * len(scale_intervals)) + degree
        if bass_root_idx < len(diatonic_notes):
            bass_pitch = diatonic_notes[bass_root_idx]
            # Driving 8th notes
            for eighth in range(8):
                time_ofs = eighth * (sec_per_beat / 2)
                insert_note(takes["Bass"], bar_start + time_ofs, bar_start + time_ofs + (sec_per_beat/2 * 0.85), bass_pitch, velocity_base)

        # --- C. Rhythm Guitar ---
        gtr_octave = 3
        gtr_root_idx = (gtr_octave * len(scale_intervals)) + degree
        if gtr_root_idx + 4 < len(diatonic_notes):
            # Diatonic Triad: Root, 3rd, 5th
            chord_pitches = [
                diatonic_notes[gtr_root_idx],
                diatonic_notes[gtr_root_idx + 2],
                diatonic_notes[gtr_root_idx + 4]
            ]
            for p in chord_pitches:
                insert_note(takes["Rhythm_Guitar"], bar_start, bar_start + bar_length_sec * 0.95, p, max(10, velocity_base - 10))

        # --- D. Lead Guitar ---
        lead_octave = 4
        lead_root_idx = (lead_octave * len(scale_intervals)) + degree
        if lead_root_idx + 4 < len(diatonic_notes):
            # Arpeggiator pattern: Root -> 3rd -> 5th -> 3rd
            arp_pitches = [
                diatonic_notes[lead_root_idx],
                diatonic_notes[lead_root_idx + 2],
                diatonic_notes[lead_root_idx + 4],
                diatonic_notes[lead_root_idx + 2]
            ]
            for eighth in range(8):
                time_ofs = eighth * (sec_per_beat / 2)
                p = arp_pitches[eighth % 4]
                insert_note(takes["Lead_Guitar"], bar_start + time_ofs, bar_start + time_ofs + (sec_per_beat/2 * 0.8), p, velocity_base)

    # Sort MIDI events sequentially on all tracks
    for role in roles:
        RPR.RPR_MIDI_Sort(takes[role])

    return f"Created Multi-Track Rock Arrangement '{track_name}' (4 tracks) over {bars} bars at {bpm} BPM in {key} {scale}."
