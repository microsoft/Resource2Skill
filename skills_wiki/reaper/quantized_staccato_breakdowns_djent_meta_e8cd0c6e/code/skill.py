def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Chug Breakdown",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a tightly quantized, gated/staccato "chug" rhythm (Djent/Metalcore style) 
    that emulates the audio-chopping techniques demonstrated in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (defines the context, though this pattern plays root notes).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for palm mutes (0-127). Accents will be louder.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory / Pitch Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Place in a very low register to emulate drop-tuned guitars/heavy synths (Octave 1)
    root_pitch = NOTE_MAP.get(key, 4) + 24 # Defaults to E1 (MIDI 28)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Syncopated Djent breakdown pattern (16 steps per bar, 1 = hit, 0 = rest)
    # This creates the classic disjointed, heavily syncopated metal groove
    rhythm_pattern = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0]
    note_count = 0

    for b in range(bars):
        for i, hit in enumerate(rhythm_pattern):
            if hit:
                # Calculate timing
                start_beat = b * beats_per_bar + (i * 0.25) # 1/16th grid is 0.25 beats
                
                # STACCATO LENGTH: Emulates the "Dynamic Split / Remove Silence" from the tutorial.
                # A full 1/16 note is 0.25 beats. We make it 0.15 beats to ensure absolute 
                # silence between consecutive hits.
                end_beat = start_beat + 0.15 

                # Convert to seconds then PPQ
                start_time = start_beat * (60.0 / bpm)
                end_time = end_beat * (60.0 / bpm)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

                # Velocity Dynamics: Accents on beats 1 and 3 (index 0 and 8)
                vel = velocity_base
                if i in [0, 8]:
                    vel = min(127, velocity_base + 15) # Emulates an "open" heavy strike
                else:
                    vel = max(1, velocity_base - 10)   # Emulates a tight "palm mute"

                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, vel, False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design FX Chain ===
    # 1. Base Synth (Saw + Square for aggressive tone)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 1.0) # Saw shape 100%
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Square shape 50%
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.0) # Decay off (sustains for the MIDI length, then cuts instantly)

    # 2. Distortion (Emulating a high-gain guitar amplifier)
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    if dist_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 12.0) # Drive/Gain
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 1, 0.5)  # Max Volume Limit

    return f"Created '{track_name}' with {note_count} quantized, gated hits over {bars} bars at {bpm} BPM."
