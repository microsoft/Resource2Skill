def create_pattern(
    project_name: str = "RetroSynthwave",
    track_name: str = "Stranger Arp",
    bpm: int = 84,  # Tutorial tempo
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a retro 80s Synthwave Arpeggio and Beat in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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

    # Set root pitch (C3 = 48 as base for bass, C4 = 60 for arp)
    root_val = NOTE_MAP.get(key, 0)
    root_pitch_bass = 36 + root_val
    root_pitch_arp = 60 + root_val
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Calculate pitch based on scale degree (0-indexed)
    def get_pitch(base_pitch, degree):
        octave_offset = degree // len(scale_intervals)
        remainder = degree % len(scale_intervals)
        return base_pitch + (octave_offset * 12) + scale_intervals[remainder]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    total_beats = bars * beats_per_bar

    # Helpers for tracking and MIDI
    def add_track(name):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    def add_midi_item(track, length):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def insert_note(take, pos_beats, len_beats, pitch, vel):
        pos_sec = pos_beats * (60.0 / bpm)
        len_sec = len_beats * (60.0 / bpm)
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, pos_sec)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, pos_sec + len_sec)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 2: Create Tracks & Items ===
    drum_track = add_track(f"{track_name} - Drums")
    bass_track = add_track(f"{track_name} - Bass")
    arp_track = add_track(f"{track_name} - Arp Synth")

    drum_take = add_midi_item(drum_track, item_length)
    bass_take = add_midi_item(bass_track, item_length)
    arp_take = add_midi_item(arp_track, item_length)

    # === Step 3: Add Sound Design (FX Chains) ===
    # Bass Synth: Sawtooth + Sub
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 1.0)  # Mix Saw
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.5)  # Mix Sub
    
    # Arp Synth: Square wave + Delay for cinematic feel
    RPR.RPR_TrackFX_AddByName(arp_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(arp_track, 0, 1, 0.0)   # Mix Saw
    RPR.RPR_TrackFX_SetParam(arp_track, 0, 5, 0.8)   # Mix Square
    RPR.RPR_TrackFX_SetParam(arp_track, 0, 8, 0.2)   # Release
    RPR.RPR_TrackFX_AddByName(arp_track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(arp_track, 1, 0, 0.1)   # Delay Dry/Wet

    # === Step 4: Populate MIDI Notes ===
    # Arpeggio scale degrees: 1st, 3rd, 5th, 7th, 8ve, 7th, 5th, 3rd (0-indexed)
    arp_degrees = [0, 2, 4, 6, 7, 6, 4, 2]
    
    note_count = 0
    for b in range(int(total_beats * 4)):  # 16th notes iterations
        beat_pos = b * 0.25

        # --- ARPEGGIO (16th notes) ---
        degree = arp_degrees[b % len(arp_degrees)]
        pitch = get_pitch(root_pitch_arp, degree)
        insert_note(arp_take, beat_pos, 0.20, pitch, velocity_base - 15)
        note_count += 1

        # --- DRUMS ---
        # Kick (downbeats)
        if b % 4 == 0:
            insert_note(drum_take, beat_pos, 0.2, 36, 120)
            note_count += 1
        # Snare (beats 2 & 4)
        if b % 8 == 4:
            insert_note(drum_take, beat_pos, 0.2, 38, 115)
            note_count += 1
        # Hi-hat (16th notes, 8th note accents)
        hh_vel = 100 if b % 2 == 0 else 70
        insert_note(drum_take, beat_pos, 0.1, 42, hh_vel)
        note_count += 1

        # --- BASS (8th notes pulse) ---
        if b % 2 == 0:
            insert_note(bass_take, beat_pos, 0.45, root_pitch_bass, velocity_base)
            note_count += 1

    # Apply MIDI sorting
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(arp_take)

    return f"Created Retro Synthwave pattern with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
