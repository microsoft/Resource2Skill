def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groove Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Syncopated Split-Articulation Slap Bass Pattern in REAPER.
    Generates two linked tracks (Finger and Slap) to mimic physical bass dynamics,
    applying 16th-note ghost syncopations, octave leaps, and micro-timing humanization.
    """
    import reaper_python as RPR
    import random

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
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Step 1: Initialize Settings & Math ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    cursor_pos = RPR.RPR_GetCursorPosition()
    
    # Calculate base MIDI note (targeting Octave 1, MIDI notes 24-35)
    base_note = NOTE_MAP.get(key.capitalize(), 4) + 24 
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_pitch(degree, octave_offset=0):
        """Helper to get scale degrees safely"""
        degree = degree % len(scale_intervals)
        return base_note + scale_intervals[degree] + (octave_offset * 12)

    # Note Definitions for the 2-Bar Groove Pattern
    # Format: (beat_pos, duration_beats, pitch_func_args, vel_multiplier, is_slap_track)
    groove_pattern = [
        # Bar 1
        (0.00, 0.35, (0, 0), 1.00, False),  # Downbeat Root (Finger)
        (1.75, 0.15, (0, 0), 0.60, False),  # 16th Pickup Ghost (Finger)
        (2.00, 0.15, (0, 1), 1.20, True),   # Backbeat Octave (Slap)
        (2.50, 0.25, (0, 0), 0.85, False),  # Offbeat Root (Finger)
        (3.75, 0.15, (0, 0), 0.65, False),  # 16th Pickup Ghost (Finger)
        # Bar 2
        (4.00, 0.15, (0, 1), 1.20, True),   # Downbeat Octave (Slap)
        (4.50, 0.25, (4, 0), 0.85, False),  # Offbeat 5th (Finger)
        (5.75, 0.15, (0, 0), 0.60, False),  # 16th Pickup Ghost (Finger)
        (6.00, 0.15, (0, 1), 1.20, True),   # Backbeat Octave (Slap)
        (6.75, 0.20, (6, 0), 0.75, False),  # 16th minor 7th / leading tone
        (7.00, 0.15, (0, 1), 1.15, True),   # Octave Slap
        (7.50, 0.25, (0, 0), 0.90, False),  # Offbeat Root (Finger)
    ]

    # === Step 2: Create Tracks & FX Chains ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # Track A: Finger Bass (Warm, Lowpass)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    track_finger = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(track_finger, "P_NAME", f"{track_name} - Finger", True)
    
    RPR.RPR_TrackFX_AddByName(track_finger, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_finger, "ReaEQ", False, -1)
    # Param 0: Vol (-6dB), Param 1: Tuning, Param 4: Triangle (warm)
    RPR.RPR_TrackFX_SetParam(track_finger, 0, 0, 0.5) 
    RPR.RPR_TrackFX_SetParam(track_finger, 0, 4, 1.0)
    # EQ: Lowpass on band 4 to dull the sound
    RPR.RPR_TrackFX_SetParam(track_finger, 1, 11, 0.0) # Enable band 4
    
    # Track B: Slap Bass (Bright, Compressed)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    track_slap = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", f"{track_name} - Slap", True)
    
    RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_slap, "ReaComp", False, -1)
    # Param 0: Vol (-3dB), Param 3: Saw (bright)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 0, 0.7)
    RPR.RPR_TrackFX_SetParam(track_slap, 0, 3, 1.0) 
    # Comp: Fast attack, high ratio for transient pop
    RPR.RPR_TrackFX_SetParam(track_slap, 1, 0, 0.0) # Threshold low
    RPR.RPR_TrackFX_SetParam(track_slap, 1, 1, 0.8) # Ratio high

    # === Step 3: Create MIDI Items ===
    beats_per_bar = 4
    bar_len_sec = (60.0 / bpm) * beats_per_bar
    total_len_sec = bar_len_sec * bars

    item_finger = RPR.RPR_AddMediaItemToTrack(track_finger)
    RPR.RPR_SetMediaItemInfo_Value(item_finger, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(item_finger, "D_LENGTH", total_len_sec)
    take_finger = RPR.RPR_AddTakeToMediaItem(item_finger)

    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", cursor_pos)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", total_len_sec)
    take_slap = RPR.RPR_AddTakeToMediaItem(item_slap)

    # === Step 4: Generate MIDI Notes with Humanization ===
    notes_added = 0
    for bar in range(0, bars, 2): # Pattern is 2 bars long
        for note in groove_pattern:
            beat_pos, duration, pitch_args, vel_mult, is_slap = note
            
            # Avoid writing past the requested total bars
            if bar + (beat_pos / 4.0) >= bars:
                continue

            # Humanize Timing: "It is nice to just slightly offset your notes"
            timing_offset_beats = random.uniform(-0.015, 0.015)
            actual_start_beat = (bar * beats_per_bar) + beat_pos + timing_offset_beats
            actual_end_beat = actual_start_beat + duration
            
            # Convert beats to time, then to PPQ for exact item placement
            start_time = cursor_pos + (actual_start_beat * 60.0 / bpm)
            end_time = cursor_pos + (actual_end_beat * 60.0 / bpm)
            
            target_take = take_slap if is_slap else take_finger
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, end_time)

            # Humanize Velocity
            base_v = int(velocity_base * vel_mult)
            vel = max(1, min(127, base_v + random.randint(-6, 6)))
            
            pitch = get_pitch(pitch_args[0], pitch_args[1])
            
            RPR.RPR_MIDI_InsertNote(target_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_added += 1

    # Force item updates
    RPR.RPR_UpdateItemInProject(item_finger)
    RPR.RPR_UpdateItemInProject(item_slap)

    return f"Created split-articulation bass on '{track_name}' (Finger + Slap) with {notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
