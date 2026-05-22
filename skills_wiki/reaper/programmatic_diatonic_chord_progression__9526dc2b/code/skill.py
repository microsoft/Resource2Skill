def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Chord Gun Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    progression: list = [1, 5, 6, 4],  # Default to I-V-vi-IV pop progression
    rhythm: str = "quarter",           # Options: "whole" (pad), "quarter" (stabs)
    base_octave: int = 4,              # MIDI octave 4 (starts at middle C, MIDI 60)
    smooth_voicing: bool = True,       # Auto-inverts chords to minimize finger jumping
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a diatonic chord progression with automatic voice-leading inversions,
    emulating the output of the REAPER "Chord Gun" script.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        progression: List of scale degrees (1-indexed) for each bar.
        rhythm: Note subdivision ('whole' or 'quarter').
        base_octave: Base octave for the root note.
        smooth_voicing: Keep notes within a 1-octave range for tight voice leading.
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    if scale not in SCALES:
        scale = "major"
    
    scale_intervals = SCALES[scale]
    root_pitch = NOTE_MAP[key] + (base_octave + 1) * 12 # Octave offset adjustment

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Setup Audio ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Lower track volume to prevent clipping when playing polyphonic chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.3) 

    # Add Instrument (ReaSynth)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Mathematical Diatonic Chord Generation ===
    note_count = 0
    scale_len = len(scale_intervals)

    for bar in range(bars):
        # Determine current chord degree (1-indexed) based on progression loop
        degree = progression[bar % len(progression)]
        root_idx = degree - 1  # 0-indexed scale index
        
        # Build Triad (Root, 3rd, 5th)
        chord_indices = [root_idx, root_idx + 2, root_idx + 4]

        # Rhythm Configuration
        if rhythm == "quarter":
            beat_steps = 4
            step_len_beats = 1.0
        else:
            beat_steps = 1
            step_len_beats = 4.0 # Whole note pad

        # Apply Notes
        for beat in range(beat_steps):
            start_sec = (bar * beats_per_bar + beat * step_len_beats) * sec_per_beat
            # 95% gate length to allow synth envelope reset on stabs
            end_sec = start_sec + (step_len_beats * sec_per_beat) * 0.95 

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

            for idx in chord_indices:
                # Calculate scale wrap-around for chords extending past the octave
                octave_shift = idx // scale_len
                wrapped_idx = idx % scale_len
                
                pitch = root_pitch + (octave_shift * 12) + scale_intervals[wrapped_idx]

                # Automatic Voice Leading (Inversions)
                if smooth_voicing:
                    # Force all chord notes to stay within a 12-semitone range above the root.
                    # This naturally creates 1st and 2nd inversions for chords like IV and V.
                    target_max = root_pitch + 11
                    while pitch > target_max:
                        pitch -= 12
                    while pitch < root_pitch:
                        pitch += 12

                # Bound limits to legal MIDI 0-127
                pitch = max(0, min(127, pitch))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, True)
                note_count += 1

    # Apply changes to MIDI item
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}': {note_count} notes over {bars} bars ({rhythm} rhythm) in {key} {scale} at {bpm} BPM."
