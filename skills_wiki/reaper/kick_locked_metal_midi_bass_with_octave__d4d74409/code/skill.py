def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Locked Metal Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a tight, syncopated metal bass line locked to a theoretical kick pattern,
    utilizing strict velocity control and octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "D"). Drop C is common for this style.
        scale: Scale type (default minor).
        bars: Number of bars to generate.
        velocity_base: Reduced base velocity (~110) to avoid extreme string clack.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Metal Bass FX Chain (Stock REAPER Proxy) ===
    # 1. ReaSynth for raw tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth: Sawtooth heavy, some sub-sine, fast attack
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.4)  # Vol
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Square Mix
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.8)  # Saw Mix (growl)
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.6)  # Extra Sine (sub)
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.0)  # Fast Attack
    
    # 2. Distortion to simulate driving an amp
    RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 1, 0, 15.0) # Gain
    
    # 3. EQ to carve it
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Low Shelf (Boost 80Hz)
    RPR.RPR_TrackFX_SetParam(track, 2, 0, 0.0)     # Tab 1
    RPR.RPR_TrackFX_SetParam(track, 2, 0+2, 4.0)   # Gain (dB)
    # Band 4: High cut (Tame distortion fizz above 4kHz)
    RPR.RPR_TrackFX_SetParam(track, 2, 9, 3.0)     # Tab 4
    RPR.RPR_TrackFX_SetParam(track, 2, 9+1, 4000.0)# Freq

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Note Mapping (C1 is note 24, excellent for heavy bass)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave is 1 (MIDI note 24 = C1)
    root_pitch = 24 + NOTE_MAP.get(key.capitalize(), 0)

    # Rhythm Definition: (Start Beat, Duration Beats, Octave Offset)
    # Simulates a heavy, syncopated kick chug pattern with an octave jump
    rhythm_pattern = [
        (0.0,  0.25, 0),   # 16th Note
        (0.5,  0.25, 0),   # 16th Note
        (0.75, 0.25, 0),   # 16th Note
        (1.5,  0.25, 0),   # 16th Note (Syncopated)
        (2.0,  0.5,  0),   # 8th Note Chug
        (2.5,  0.25, 0),   # 16th Note
        (3.0,  0.25, 12),  # +1 Octave Jump Fill!
        (3.5,  0.25, 0)    # Return to Root
    ]

    total_notes = 0

    # === Step 5: Insert MIDI Notes ===
    for b in range(bars):
        bar_offset_beats = b * beats_per_bar
        
        # On the last bar, we do a slightly different fill (double octave jump)
        is_last_bar = (b == bars - 1)
        
        for pos, dur, oct_off in rhythm_pattern:
            # Modify the last bar for a turnaround fill
            if is_last_bar and pos >= 3.0:
                dur = 0.125  # 32nd notes
                oct_off = 12 # Keep it in the upper octave

            start_time = ((bar_offset_beats + pos) / bpm) * 60.0
            end_time = ((bar_offset_beats + pos + dur) / bpm) * 60.0

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            pitch = root_pitch + oct_off
            
            # Add slight humanization to velocity, keeping it below 115
            import random
            vel = max(90, min(115, velocity_base + random.randint(-5, 5)))

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes += 1
            
            # Complete the fill for the last bar
            if is_last_bar and pos == 3.0:
                for extra in range(1, 4):
                    st = ((bar_offset_beats + pos + (0.125 * extra)) / bpm) * 60.0
                    et = ((bar_offset_beats + pos + (0.125 * (extra + 1))) / bpm) * 60.0
                    s_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, st)
                    e_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, et)
                    RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, pitch, vel, True)
                    total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
