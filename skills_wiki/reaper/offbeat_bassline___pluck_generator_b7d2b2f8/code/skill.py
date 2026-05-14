def create_pattern(
    project_name: str = "Offbeat_Groove",
    track_name: str = "Offbeat Bass",
    bpm: int = 124,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create an offbeat bassline and a sine pluck chord progression.

    Args:
        project_name: Project identifier.
        track_name: Name for the bass track.
        bpm: Tempo in BPM (120-128 is ideal for this genre).
        key: Root note.
        scale: Scale type (major, minor).
        bars: Number of bars.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Logic ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key, 9)  # Default A
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard EDM Progression: i - VI - III - VII (represented as scale degrees)
    chords = [
        [0, 2, 4],   # i   (Root, 3rd, 5th)
        [5, 7, 9],   # VI  (6th, Root+Oct, 3rd+Oct)
        [2, 4, 6],   # III (3rd, 5th, 7th)
        [6, 8, 10]   # VII (7th, 2nd+Oct, 4th+Oct)
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    notes_added = 0

    # === Track 1: Sine Pluck ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    pluck_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(pluck_track, "P_NAME", "Sine Pluck Chords", True)
    
    # Configure Pluck Synth
    RPR.RPR_TrackFX_AddByName(pluck_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 0, 0.4)   # Vol (sine baseline)
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 2, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 3, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 4, 0.5)   # Triangle mix (adds pluck warmth)
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 5, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 6, 0.15)  # Decay (Pluck)
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 7, 0.0)   # Sustain
    RPR.RPR_TrackFX_SetParam(pluck_track, 0, 8, 0.2)   # Release
    
    pluck_item = RPR.RPR_AddMediaItemToTrack(pluck_track)
    RPR.RPR_SetMediaItemInfo_Value(pluck_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(pluck_item, "D_LENGTH", item_length)
    pluck_take = RPR.RPR_AddTakeToMediaItem(pluck_item)
    
    # Generate Pluck Chords
    for b in range(bars):
        chord_idx = b % len(chords)
        chord_degrees = chords[chord_idx]
        
        start_time = b * bar_length_sec
        end_time = start_time + (bar_length_sec * 0.75) # Sustained chord
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pluck_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(pluck_take, end_time)
        
        for degree in chord_degrees:
            octave_shift = degree // 7
            scale_idx = degree % 7
            pitch = 60 + root_val + scale_intervals[scale_idx] + (octave_shift * 12)
            RPR.RPR_MIDI_InsertNote(pluck_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 15, False)
            notes_added += 1

    # === Track 2: Offbeat Bassline ===
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", track_name, True)
    
    # Configure Bass Synth (Gritty Saw)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.8)    # Vol
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.2)    # Square mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 1.0)    # Saw mix (Aggressive)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.01)   # Attack
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.2)    # Decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 7, 0.3)    # Sustain
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    # Generate Offbeat Bass Sequence
    bass_root_octave = 36 # C2 range
    
    for b in range(bars):
        chord_idx = b % len(chords)
        root_degree = chords[chord_idx][0]
        # Follow the root note of the active chord
        bass_pitch = bass_root_octave + root_val + scale_intervals[root_degree % 7] + ((root_degree // 7) * 12)
        
        # 4 off-beats per bar (the "and" of beats 1, 2, 3, 4)
        for beat in range(4):
            # Timing calculation: 0.5 beats offset places it exactly on the upbeat
            start_time = (b * bar_length_sec) + ((beat + 0.5) * beat_sec)
            end_time = start_time + (0.25 * beat_sec) # Crisp 16th-note length
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, False)
            notes_added += 1

    # Cleanup and update
    RPR.RPR_MIDI_Sort(pluck_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_UpdateArrange()

    return f"Created 'Sine Pluck' and '{track_name}' with {notes_added} sequenced notes over {bars} bars at {bpm} BPM"
