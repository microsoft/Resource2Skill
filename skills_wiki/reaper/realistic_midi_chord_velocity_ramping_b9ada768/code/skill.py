def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a chord progression with humanized velocity swells in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Peak MIDI velocity (0-127) at the height of the swell.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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

    # Ensure valid inputs
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Common 4-bar progression (1-index corresponding to I, VI, III, VII)
    progression_degrees = [0, 5, 2, 6] 

    def get_scale_pitch(degree: int, octave: int = 4) -> int:
        """Returns the MIDI pitch for a given scale degree (0-indexed)."""
        scale_length = len(scale_intervals)
        octave_offset = degree // scale_length
        scale_degree = degree % scale_length
        return root_pitch + (octave + octave_offset) * 12 + scale_intervals[scale_degree]

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

    # === Step 4: Add Chords & Velocity Swells ===
    total_notes_created = 0
    note_duration_qn = 0.45  # Slightly less than an 8th note (0.5 QN) for staccato articulation
    
    for bar in range(bars):
        chord_root_deg = progression_degrees[bar % len(progression_degrees)]
        
        # Build triad (Root, 3rd, 5th)
        chord_degrees = [chord_root_deg, chord_root_deg + 2, chord_root_deg + 4]
        
        # 8 pulses per bar (8th notes)
        for eighth_note in range(8):
            # Calculate absolute time in seconds, then convert to PPQ
            start_qn = (bar * beats_per_bar) + (eighth_note * 0.5)
            end_qn = start_qn + note_duration_qn
            
            # Use REAPER TimeMap functions to resolve PPQ
            start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Mathematical Velocity Swell: Creates a triangle wave shape mimicking mouse-drag automation.
            # Middle of the bar (eighth_note = 3.5) hits hardest at velocity_base.
            # Edges drop down by ~35 units.
            swell_offset = abs(eighth_note - 3.5) * 10
            vel = int(velocity_base - swell_offset)
            vel = max(1, min(127, vel)) # Clamp 1-127

            # Add each note of the triad
            for deg in chord_degrees:
                pitch = get_scale_pitch(deg, octave=4)
                
                # Add slight humanization to individual triad velocities
                humanized_vel = vel
                if deg == chord_degrees[1]:
                    humanized_vel -= int(velocity_base * 0.1) # 3rd is slightly softer
                elif deg == chord_degrees[2]:
                    humanized_vel -= int(velocity_base * 0.05) # 5th is medium
                
                humanized_vel = max(1, min(127, humanized_vel))

                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # Selected
                    False,          # Muted
                    start_ppq, 
                    end_ppq, 
                    0,              # Channel
                    pitch, 
                    humanized_vel, 
                    True            # noSort
                )
                total_notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    # Using stock ReaSynth as a stand-in for the Grand Piano
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth slightly to sound more like an electric key (lower sustain, some decay)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3) # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1) # Sustain

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes_created} humanized velocity notes over {bars} bars at {bpm} BPM."
