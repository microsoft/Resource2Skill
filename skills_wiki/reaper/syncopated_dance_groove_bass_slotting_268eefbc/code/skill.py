def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Dance Groove",
    bpm: int = 124,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Syncopated Dance Groove & Slotted Bassline in REAPER.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created drum track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for strong beats (0-127).
        **kwargs: Additional overrides.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Ensure valid scale and root
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_offset = NOTE_MAP.get(key.upper() if len(key) == 1 else key.capitalize(), 0)
    
    # Setup timing
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Helper function to write MIDI notes using absolute beats
    def add_midi_note(take, beat_pos, duration_beats, pitch, vel, is_swingable=False):
        swing_amount = 0.05 if is_swingable and (beat_pos % 0.5 != 0) else 0.0
        start_beat = beat_pos + swing_amount
        end_beat = beat_pos + duration_beats + swing_amount
        
        start_time = (60.0 / bpm) * start_beat
        end_time = (60.0 / bpm) * end_beat
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === TRACK 1: DRUMS ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # General MIDI Notes
    KICK = 36
    CLAP = 39
    CLOSED_HAT = 42
    OPEN_HAT = 46
    PERC = 60 # Hi Bongo

    # Build the 1-bar drum loop, repeated across specified bars
    for b in range(bars):
        bar_offset = b * 4
        
        # Quarter Notes (4-on-the-floor)
        for i in range(4):
            add_midi_note(drum_take, bar_offset + i, 0.25, KICK, velocity_base)
            
        # Claps (2 and 4)
        add_midi_note(drum_take, bar_offset + 1, 0.25, CLAP, velocity_base)
        add_midi_note(drum_take, bar_offset + 3, 0.25, CLAP, velocity_base)

        # Eighth notes (Open Hats on the off-beats)
        for i in [0.5, 1.5, 2.5, 3.5]:
            add_midi_note(drum_take, bar_offset + i, 0.25, OPEN_HAT, int(velocity_base * 0.85))

        # Sixteenth note Syncopations (Ghost notes/Percussion)
        # These use lower velocity and swing to create groove
        syncopations = [0.75, 1.25, 2.25, 2.75, 3.25]
        for s in syncopations:
            add_midi_note(drum_take, bar_offset + s, 0.125, PERC, int(velocity_base * 0.65), is_swingable=True)

    RPR.RPR_MIDI_Sort(drum_take)

    # === TRACK 2: SLOTTED BASS ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Load stock synth to make it audible
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Tune ReaSynth down 1 octave and square wave it for a bassy tone
    # Param 0 = Volume, Param 1 = Tuning, Param 4 = Square Mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, -12.0) # Tune down 12 semitones
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.5)   # Add 50% square wave

    # Base octave for bass (MIDI 36 = C2)
    bass_base_pitch = 36 + root_offset
    
    def get_scale_pitch(degree):
        # Wraps around scale list for octaves
        octave = degree // len(scale_intervals)
        note = scale_intervals[degree % len(scale_intervals)]
        return bass_base_pitch + note + (octave * 12)

    # Build the 1-bar bass loop
    # Notice the bass hits specifically AVOID 0.0, 1.0, 2.0, 3.0 (Kick drums)
    bass_pattern = [
        # (beat_position, scale_degree, duration)
        (0.75, 0, 0.25),  # Root on the "a" of 1
        (1.5,  2, 0.25),  # Minor 3rd on the "&" of 2
        (2.25, 4, 0.25),  # Perfect 5th on the "e" of 3
        (2.75, 3, 0.25),  # 4th on the "a" of 3
        (3.5,  0, 0.5),   # Root on the "&" of 4, held slightly longer
    ]

    for b in range(bars):
        bar_offset = b * 4
        for beat_pos, degree, duration in bass_pattern:
            pitch = get_scale_pitch(degree)
            add_midi_note(bass_take, bar_offset + beat_pos, duration, pitch, velocity_base, is_swingable=True)

    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created '{track_name} Drums' and Bass over {bars} bars at {bpm} BPM with slotted 16th-note syncopation."
