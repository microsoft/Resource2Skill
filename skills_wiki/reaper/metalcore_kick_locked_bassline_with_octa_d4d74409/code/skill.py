def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a metalcore/rock bassline locked to a syncopated kick rhythm,
    using 110 velocity to tame VST harshness and octave jumps for fills.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "D").
        scale: Ignored in this specific script as we only play the root and octave.
        bars: Number of bars to generate.
        velocity_base: Set to 110 as per tutorial to reduce virtual pick harshness.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated bassline.
    """
    import reaper_python as RPR

    # Note mapping to calculate root pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Bass root usually sits around MIDI note 24 (C1) to 36 (C2)
    # We will assume a low C1 tuning for heavy music
    base_octave = 1
    root_midi = NOTE_MAP.get(key, 0) + (base_octave + 1) * 12

    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # 1. Create a new track for the Bass
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # 2. Add ReaSynth as a placeholder instrument
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more "bass" character: 
    # Osc 1: Saw, Filter down a bit
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 1.0)    # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.0)    # Pulse mix

    # 3. Create MIDI item
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    start_time = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 4. Define the kick-locked rhythm pattern
    # Format: (start_beat, length_in_beats, is_octave_jump)
    # A standard syncopated metalcore groove
    kick_groove = [
        (0.0, 0.25, False),   # Beat 1
        (0.5, 0.25, False),   # Beat 1 &
        (1.25, 0.25, False),  # Beat 2 e
        (2.0, 0.25, False),   # Beat 3
        (2.5, 0.25, False),   # Beat 3 &
        (3.5, 0.25, True),    # Beat 4 & -> Octave Fill!
    ]

    # 5. Insert MIDI notes
    note_count = 0
    for b in range(bars):
        # Every 4th bar, we alter the turnaround to show the "following the guitar" / more variations idea
        is_turnaround = (b % 4 == 3)
        
        for beat_start, beat_length, octave_jump in kick_groove:
            # On turnarounds, make the last two hits octave jumps
            if is_turnaround and beat_start >= 2.5:
                octave_jump = True

            note_time = start_time + (b * beats_per_bar + beat_start) * sec_per_beat
            note_end_time = note_time + (beat_length * sec_per_beat)

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)

            pitch = root_midi + 12 if octave_jump else root_midi
            
            # The crucial lesson from the video: velocity_base = 110 (not 127)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} notes over {bars} bars locked to syncopated kick rhythm at {bpm} BPM in {key}."
