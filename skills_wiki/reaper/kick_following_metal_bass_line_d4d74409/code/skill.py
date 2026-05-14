import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass_KickFollow",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Not directly used for bass, but kept for consistency
    bars: int = 4,
    velocity_base: int = 110, # As suggested by the speaker
    bass_octave: int = 2, # Corresponds to C2 as the lowest C in the video's example
    staccato_ratio: float = 0.75, # A ratio to shorten note durations (e.g., 0.75 for 75% of full duration)
    **kwargs,
) -> str:
    """
    Create a kick-following bass line in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        bass_octave: The MIDI octave for the root bass note (e.g., 2 for C2).
        staccato_ratio: A ratio to shorten note durations (e.g., 0.75 for 75% of full duration).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Bass_KickFollow' with N notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This command might cause issues with existing tempo changes, better to let user manage global tempo or override at track/item level if advanced.

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth as a placeholder instrument ===
    # The tutorial uses a third-party VST (GinnBass). ReaSynth is used here as a stock alternative.
    # Users should replace this with their preferred bass VST for optimal results.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Attempt to load a generic bass preset if available (this might not be cross-platform/version reliable)
    # RPR.RPR_TrackFX_SetPreset(track, 0, "Bass", False) # This requires a specific preset name which may not exist.

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    quarter_note_duration = 60.0 / bpm / beats_per_bar # Duration of 1 beat in seconds
    item_length = quarter_note_duration * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", RPR.RPR_GetPlayPosition()) # Start at current play position
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_GetActiveTake(item)
    midi_take = RPR.RPR_MIDI_SetItemExtents(take, 0, 0) # Get MIDI take pointer

    # Root MIDI note calculation
    root_note_val = NOTE_MAP.get(key.upper(), 0) # Default to C if key not found
    base_midi_pitch = (bass_octave * 12) + root_note_val

    # Define a single-bar bass pattern (relative beats, pitch offset semitones, duration_beats)
    # This pattern is inspired by the various notes drawn in the video, emphasizing kick syncopation and octave variation.
    bass_pattern_notes = [
        # (start_beat_in_bar, pitch_offset_semitones, duration_beats)
        (0.0, 0, 1.0), # Quarter note on beat 1
        (1.5, 0, 0.5), # Eighth note on beat 1.5
        (2.5, 0, 0.5), # Eighth note on beat 2.5
        (3.0, 0, 1.0), # Quarter note on beat 3
        (3.5, 12, 0.5), # Eighth note on beat 3.5, one octave up (variation as shown in video)
    ]

    total_notes_inserted = 0
    for bar_offset in range(bars):
        for note_data in bass_pattern_notes:
            start_beat_relative = note_data[0]
            pitch_offset = note_data[1]
            raw_duration_beats = note_data[2]

            start_time_beats = (bar_offset * beats_per_bar) + start_beat_relative
            end_time_beats = start_time_beats + (raw_duration_beats * staccato_ratio)
            
            midi_pitch = base_midi_pitch + pitch_offset
            
            # Insert MIDI note (MIDI_InsertNote expects seconds, so convert beats to seconds)
            # RPR_MIDI_InsertNote(MIDI_take, is_selected, is_ghost, start_time_seconds, end_time_seconds, no_chg_vel, velocity, no_chg_chan, channel)
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, 
                                    start_time_beats * quarter_note_duration, 
                                    end_time_beats * quarter_note_duration, 
                                    False, velocity_base, False, 0)
            total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_Commit(midi_take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes_inserted} notes over {bars} bars at {bpm} BPM"

