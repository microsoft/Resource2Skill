def create_pattern(
    project_name: str = "MultiTrack Workflow",
    track_name: str = "Arrangement", # Base name, will create 4 specific tracks
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Interlocking Multi-Track Arrangement in the current REAPER project.
    Generates color-coded Drums, Bass, Rhythm, and Lead tracks to practice
    multi-track MIDI editing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored here, creates specific instruments).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate (cycles through 4-chord loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key, 11) + 48 # Default to B2 (MIDI 59)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper function to get scale pitches across octaves
    def get_scale_pitch(base_note, intervals, degree):
        octave_shift = degree // len(intervals)
        scale_idx = degree % len(intervals)
        return base_note + intervals[scale_idx] + (octave_shift * 12)

    # Helper function to insert a note
    def add_note(take, start_beat, end_beat, pitch, velocity):
        # Convert beats to time (1 beat = 1 quarter note)
        beat_len = 60.0 / bpm
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars

    track_setup = [
        {"name": "Drums",  "color": 255 + (0 * 256) + (0 * 65536) | 16777216,   "synth": None},       # Red
        {"name": "Bass",   "color": 128 + (0 * 256) + (128 * 65536) | 16777216, "synth": "ReaSynth"}, # Purple
        {"name": "Rhythm", "color": 0 + (128 * 256) + (255 * 65536) | 16777216, "synth": "ReaSynth"}, # Blue
        {"name": "Lead",   "color": 255 + (165 * 256) + (0 * 65536) | 16777216, "synth": "ReaSynth"}  # Orange
    ]

    takes = {}

    # === Step 2 & 3: Create Tracks & MIDI Items ===
    for i, setup in enumerate(track_setup):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", setup["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", setup["color"])
        
        if setup["synth"]:
            RPR.RPR_TrackFX_AddByName(track, setup["synth"], False, -1)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes[setup["name"]] = take

    # === Step 4: Populate MIDI Notes ===
    # Progression: i - VI - III - VII (0, 5, 2, 6 in scale degrees)
    progression = [0, 5, 2, 6] 

    for bar in range(bars):
        deg = progression[bar % len(progression)]
        bar_beat_start = bar * 4

        # 1. DRUMS (Kick: 36, Snare: 38, Hat: 42)
        for beat in range(8): # 8th notes
            beat_pos = bar_beat_start + (beat * 0.5)
            
            # Hi-hat on every 8th note
            add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 42, velocity_base - 10)
            
            # Snare on beats 2 and 4 (indices 2 and 6 in 8th-note array)
            if beat == 2 or beat == 6:
                add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 38, velocity_base + 10)
                
            # Kick on 1, 2-AND, 3 (indices 0, 3, 4)
            if beat == 0 or beat == 3 or beat == 4:
                add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 36, velocity_base + 15)

        # 2. BASS (8th notes, following the root, 2 octaves down)
        bass_pitch = get_scale_pitch(root_midi - 24, scale_intervals, deg)
        for beat in range(8):
            beat_pos = bar_beat_start + (beat * 0.5)
            add_note(takes["Bass"], beat_pos, beat_pos + 0.45, bass_pitch, velocity_base)

        # 3. RHYTHM (Whole note block chords)
        chord_pitches = [
            get_scale_pitch(root_midi, scale_intervals, deg),     # Root
            get_scale_pitch(root_midi, scale_intervals, deg + 2), # Third
            get_scale_pitch(root_midi, scale_intervals, deg + 4)  # Fifth
        ]
        for p in chord_pitches:
            add_note(takes["Rhythm"], bar_beat_start, bar_beat_start + 4.0, p, velocity_base - 15)

        # 4. LEAD (8th note arpeggio using the chord tones, 1 octave up)
        for beat in range(8):
            beat_pos = bar_beat_start + (beat * 0.5)
            # Cycle through the triad: Root -> Third -> Fifth -> Root...
            arp_pitch = chord_pitches[beat % 3] + 12 
            add_note(takes["Lead"], beat_pos, beat_pos + 0.4, arp_pitch, velocity_base + 5)

    # Sort MIDI events for all takes
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created multi-track arrangement (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
