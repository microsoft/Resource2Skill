import reaper_python as RPR
import random

# Music theory lookup tables (pre-defined in the agent's environment)
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

def create_bassline_redbone_groove(
    project_name: str = "MyProject",
    track_name: str = "Redbone Bassline",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor", # Not directly used for intervals in this pattern, but for context
    bars: int = 4,
    base_octave: int = 2,
    velocity_base: int = 100,
    humanize: bool = True,
    **kwargs,
) -> str:
    """
    Create a bassline inspired by the "Redbone" style groove, featuring root notes, passing tones,
    and higher 'slap' notes, with optional humanization.

    The pattern implemented is a 2-bar repeating phrase based on the visual example at 0:28-0:30
    of the tutorial, generalized for any given key. It features a i-v chord progression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note of the bassline progression (e.g., "C").
        scale: Scale type (e.g., "minor"). Used for context, not direct interval calculation in this specific pattern.
        bars: Number of bars to generate.
        base_octave: The base octave for the root notes (e.g., 1 for C1, 2 for C2).
        velocity_base: Base MIDI velocity (0-127).
        humanize: If True, apply subtle random timing and velocity offsets.
        **kwargs: Additional overrides (not used directly here but good practice).

    Returns:
        Status string, e.g., "Created 'Redbone Bassline' with 24 notes over 4 bars at 120 BPM"
    """
    RPR.Undo_BeginBlock() # Start undo block

    # --- Step 1: Create Track ---
    track_idx = RPR.CountTracks(0)
    RPR.InsertTrackAtIndex(track_idx, True)
    track = RPR.GetTrack(0, track_idx)
    RPR.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- Step 2: Add ReaSynth for bass sound ---
    RPR.TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth parameters for a basic bass sound
    RPR.TrackFX_SetParam(track, 0, 11, 0.5) # Waveform: Saw (0.0=Sine, 0.5=Saw, 1.0=Square)
    RPR.TrackFX_SetParam(track, 0, 29, 0.0) # ADSR Attack (0.0=instant)
    RPR.TrackFX_SetParam(track, 0, 30, 0.3) # ADSR Decay (0.3=short)
    RPR.TrackFX_SetParam(track, 0, 31, 0.7) # ADSR Sustain (0.7=medium)
    RPR.TrackFX_SetParam(track, 0, 32, 0.2) # ADSR Release (0.2=short)
    RPR.TrackFX_SetParam(track, 0, 17, 0.3) # Filter Cutoff (lower for bass)
    RPR.TrackFX_SetParam(track, 0, 18, 0.5) # Filter Resonance

    # --- Step 3: Create MIDI Item ---
    beats_per_bar = 4
    item_length_beats = bars * beats_per_bar
    
    # Insert MIDI item
    item = RPR.AddMediaItemToTrack(track)
    RPR.SetMediaItemInfo_Value(item, "D_POSITION", RPR.GetCursorPosition()) # Place at current cursor position
    RPR.SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats) # Length in beats
    take = RPR.GetMediaItemTake(item, 0)
    if not take:
        take = RPR.AddTakeToMediaItem(item)

    # Set MIDI content start/end in beats for the take
    RPR.MIDI_SetItemExtents(take, 0.0, item_length_beats, True) 

    # Calculate base MIDI note for the `key` and `base_octave`
    # E.g., if key="C", base_octave=2, initial_root_midi = 36 (C2)
    initial_root_midi = NOTE_MAP.get(key.upper(), 0) + (base_octave * 12)

    # Define the 2-bar bassline pattern. Pitches are relative to `initial_root_midi`.
    # Each element: (interval_from_initial_root, duration_beats, velocity_multiplier, beat_offset_in_2bar_pattern)
    pattern_template_2bars = [
        # --- Bar 1 (Tonic - i chord feel, relative to initial_root_midi) ---
        # C2 (Root, long)
        (0,  1.0, 1.0, 0.0),
        # Eb2 (minor 3rd, rhythmic hit)
        (3,  0.5, 0.8, 1.0),
        # F2 (perfect 4th, rhythmic hit)
        (5,  0.5, 0.8, 1.5),
        # G3 (perfect 5th + octave, 'slap' accent)
        (7 + 12, 0.25, 1.1, 2.0),
        # G2 (perfect 5th, sustained)
        (7,  1.0, 0.9, 2.5),
        # Bb3 (minor 7th + octave, 'slap' accent)
        (10 + 12, 0.25, 1.15, 3.5),

        # --- Bar 2 (Dominant - v chord feel, relative to initial_root_midi) ---
        # G1 (perfect 5th down an octave from C, acting as root for this bar)
        (7 - 12,  1.0, 1.0, 4.0),
        # Bb1 (minor 3rd relative to G, rhythmic hit)
        (10 - 12, 0.5, 0.8, 5.0),
        # C2 (perfect 4th relative to G, rhythmic hit)
        (12 - 12, 0.5, 0.8, 5.5),
        # D3 (perfect 5th relative to G + octave, 'slap' accent)
        (14,      0.25, 1.1, 6.0), # 14 semitones from C is D, which is P5 of G.
        # D2 (perfect 5th relative to G, sustained)
        (14 - 12, 1.0, 0.9, 6.5),
        # F3 (minor 7th relative to G + octave, 'slap' accent)
        (17,      0.25, 1.15, 7.5), # 17 semitones from C is F, which is m7 of G.
    ]

    notes_inserted_count = 0
    two_bar_phrase_length_beats = 2 * beats_per_bar # 8 beats

    for current_pattern_start_beat in range(0, item_length_beats, two_bar_phrase_length_beats):
        if current_pattern_start_beat + two_bar_phrase_length_beats > item_length_beats:
            # Avoid inserting notes beyond the item_length if `bars` is not a multiple of 2
            continue 

        for (interval, duration, vel_mult, beat_offset_in_pattern) in pattern_template_2bars:
            midi_pitch = initial_root_midi + interval
            velocity = int(velocity_base * vel_mult)

            # Calculate actual start beat for the note relative to the start of the MIDI item
            note_start_beat_in_item = current_pattern_start_beat + beat_offset_in_pattern
            
            # Apply humanization (slight timing and velocity offsets)
            if humanize:
                timing_offset_ms = random.uniform(-10.0, 10.0) # +/- 10ms
                timing_offset_beats = timing_offset_ms / 1000.0 * (bpm / 60.0) # Convert ms to beats
                note_start_beat_in_item += timing_offset_beats

                velocity += random.randint(-5, 5) # +/- 5 velocity
                velocity = max(0, min(127, velocity)) # Clamp velocity between 0-127

            # Insert note into the take
            RPR.MIDI_InsertNote(take, False, False, note_start_beat_in_item, note_start_beat_in_item + duration, velocity, True, midi_pitch, False)
            notes_inserted_count += 1

    RPR.MIDI_Sort(take) # Sort notes in the take by position
    RPR.MIDI_SetItemExtents(take, 0.0, float(item_length_beats), True) # Ensure MIDI content matches item length
    RPR.UpdateArrange() # Refresh REAPER's display
    RPR.Undo_EndBlock2(0, f"Created {track_name}") # End undo block

    return f"Created '{track_name}' with {notes_inserted_count} notes over {bars} bars at {bpm} BPM, inspired by Redbone bassline."

