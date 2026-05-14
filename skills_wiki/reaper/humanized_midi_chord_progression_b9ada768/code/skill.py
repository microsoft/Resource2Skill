import random

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Humanized MIDI Chord Progression in the current REAPER project.
    Simulates the MIDI editor CC velocity humanization taught in the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (defaults to 4).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Progression: I - V - vi - IV (indices in a 7-note scale)
    PROGRESSION = [0, 4, 5, 3] 

    root_pitch = NOTE_MAP.get(key, 0) + 48 # Start at octave 4
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth piano-like settings) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set to a plucky, piano-like envelope: fast attack, medium decay, lower sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release

    # === Step 4: Create MIDI Item & Take ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Insert Humanized MIDI Notes ===
    notes_created = 0
    
    for bar in range(bars):
        # Determine the chord for this bar (looping the progression if necessary)
        chord_degree = PROGRESSION[bar % len(PROGRESSION)]
        
        # Build a triad (root, 3rd, 5th)
        chord_pitches = []
        for interval_offset in [0, 2, 4]:
            scale_idx = (chord_degree + interval_offset) % 7
            octave_shift = ((chord_degree + interval_offset) // 7) * 12
            pitch = root_pitch + scale_intervals[scale_idx] + octave_shift
            chord_pitches.append(pitch)
        
        # Timing: leaving a tiny gap at the end for realistic release
        start_time = bar * bar_length_sec
        end_time = start_time + (bar_length_sec * 0.95)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # Apply humanization to the chord
        for i, pitch in enumerate(chord_pitches):
            # Humanize velocity: Root note heavier, inner notes slightly softer, plus randomness
            if i == 0:
                base_vel = velocity_base + 10  # Root
            elif i == 1:
                base_vel = velocity_base - 10  # Third
            else:
                base_vel = velocity_base       # Fifth
                
            # Simulate the "click and drag" manual variation shown in the video
            humanized_velocity = base_vel + random.randint(-12, 12)
            # Clamp between 1 and 127
            humanized_velocity = max(1, min(127, humanized_velocity))
            
            # Tiny timing offset (strumming effect, simulating non-quantized hands)
            timing_offset_ppq = random.randint(-10, 20)
            note_start_ppq = start_ppq + timing_offset_ppq

            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                note_start_ppq, end_ppq, 
                0, pitch, int(humanized_velocity), False
            )
            notes_created += 1

    # Sort MIDI events after insertion (required by REAPER API)
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM with humanized velocities."
