import reaper_python as RPR
import random

def create_bass_kick_follow_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass",
    bpm: int = 120,
    key: str = "C",
    midi_octave_offset: int = 0,  # Offset in octaves from C2 (MIDI 48) - e.g., 0 for C2, -12 for C1
    bars: int = 4,
    velocity_base: int = 110,  # Base MIDI velocity (0-127). Tutorial suggests 110.
    include_octave_variation: bool = False,  # If True, randomly shifts some notes up an octave for variation.
    **kwargs,
) -> str:
    """
    Create a bass line that follows a common kick drum pattern, as demonstrated in the tutorial.
    The pattern is: quarter note on beat 1, then eighth notes on 2.5, 3.0, 3.5, repeated per bar.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) for the bass line.
        midi_octave_offset: MIDI note offset in semitones (12 semitones = 1 octave).
                            e.g., 0 for C2 (MIDI 48), -12 for C1 (MIDI 36), +12 for C3 (MIDI 60).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). Tutorial suggests 110.
        include_octave_variation: If True, randomly shifts some notes up an octave for variation.
        **kwargs: Additional overrides (not used in this skill but for composability).

    Returns:
        Status string, e.g., "Created 'Bass' track with 16 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # Ensure key is valid
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}"

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add a VSTi (ReaSynth as a generic bass, mention Ugzinbass) ===
    # Adding ReaSynth as a simple placeholder. User can replace with Ugzinbass or other bass VST.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Optionally, set a basic patch for ReaSynth if known, but for generic use, default is fine.

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    item_length_time = RPR.RPR_QN_2_TIME(item_length_beats, bpm)

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)  # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_time)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Insert MIDI Notes ===
    # Get MIDI_Take for note manipulation
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length_time)
    midi_take = take # Correctly refers to the MIDI data within the active take
    
    # Base MIDI note: C2 (MIDI 48) is a good starting point for a bass instrument.
    # The tutorial draws notes which visually appear to be around C2.
    root_midi_note = NOTE_MAP[key] + 48 + midi_octave_offset

    # The kick pattern based on the video demonstration (01:34-01:42)
    # (position_in_beats_relative_to_bar_start, duration_in_beats)
    bass_pattern_relative = [
        (0.0, 1.0),  # Beat 1 (quarter note)
        (2.5, 0.5),  # Beat 2.5 (eighth note)
        (3.0, 0.5),  # Beat 3 (eighth note)
        (3.5, 0.5),  # Beat 3.5 (eighth note)
    ]
    
    total_notes_inserted = 0
    RPR.RPR_MIDI_DisableSort(midi_take)  # For efficiency when inserting many notes

    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for beat_offset, duration in bass_pattern_relative:
            note_start_beat = bar_start_beat + beat_offset
            note_end_beat = note_start_beat + duration
            
            # RPR_MIDI_InsertNote uses quarter notes as its time unit
            qn_start = note_start_beat
            qn_end = note_end_beat

            current_midi_note = root_midi_note
            if include_octave_variation and random.random() < 0.2:  # 20% chance to jump an octave up
                current_midi_note += 12

            RPR.RPR_MIDI_InsertNote(midi_take, False, False, qn_start, qn_end, velocity_base, 0, current_midi_note, False)
            total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(midi_take)  # Re-sort notes after insertion
    RPR.RPR_MIDI_SetOpenState(midi_take, False)  # Close MIDI editor
    RPR.RPR_UpdateArrange()  # Update REAPER arrange view

    return f"Created '{track_name}' track with {total_notes_inserted} notes over {bars} bars at {bpm} BPM. (Using ReaSynth, consider Ugzinbass for actual sound)"

