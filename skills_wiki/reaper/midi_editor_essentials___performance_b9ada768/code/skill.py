import reaper_python as RPR

def create_midi_editor_demo_pattern(
    project_name: str = "MIDI_Project",
    track_name: str = "MIDI Editor Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a simple MIDI item with a 4-bar progression demonstrating
    basic note creation and velocity variations, as seen in the REAPER MIDI editor tutorial.

    The pattern consists of:
    - Bar 1: A short melodic phrase with varied note lengths and velocities.
    - Bar 2, 3, 4: Repeated C Major chords with varied velocities.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'MIDI Editor Demo' with 17 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11], # Intervals: R, M2, M3, P4, P5, M6, M7
        "minor":            [0, 2, 3, 5, 7, 8, 10], # Intervals: R, M2, m3, P4, P5, m6, m7
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}."
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Must be one of {list(SCALES.keys())}."

    root_midi_base = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # Helper function to get MIDI pitch
    def get_midi_pitch(root, interval_idx_in_scale, octave_c0_relative):
        return root + scale_intervals[interval_idx_in_scale] + (12 * octave_c0_relative)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as a placeholder for the Grand Piano VSTi shown in the tutorial.
    # The tutorial used 'Grand Piano - Substantial' VSTi, which is not a stock REAPER plugin.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_seconds = float(bars * beats_per_bar) * (60.0 / bpm)
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)

    take = RPR.RPR_GetActiveTake(item)
    if not take:
        RPR.RPR_DeleteTrack(track) # Clean up if take creation failed
        return "Error: Failed to create active take for MIDI item."

    RPR.RPR_MIDI_SetItemExtents(item, 0.0, float(bars * beats_per_bar)) # Set item length in beats
    midi_take = RPR.RPR_MIDI_AllocTemporary(take, True) # Allocate temporary MIDI buffer

    note_count = 0
    current_beat_pos = 0.0

    # --- Bar 1: Melodic phrase (as demonstrated in tutorial) ---
    # Notes are relative to C major scale for consistency with tutorial's examples
    # Pitches: C4, C4, G3, E3, C3 (using C as root for these relative calcs)
    
    # C4 (Root, octave 4)
    pitch_c4 = get_midi_pitch(root_midi_base, 0, 4)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base, False, pitch_c4, 0)
    note_count += 1
    current_beat_pos += 0.5

    # C4 (Root, octave 4, longer duration)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 1.0, velocity_base + 10, False, pitch_c4, 0)
    note_count += 1
    current_beat_pos += 1.0

    # Skip 1 beat to beat 2.5
    current_beat_pos += 1.0

    # G3 (Perfect 5th, octave 3)
    pitch_g3 = get_midi_pitch(root_midi_base, 4, 3) # Index 4 in major scale is P5
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 5, False, pitch_g3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # E3 (Major 3rd, octave 3)
    pitch_e3 = get_midi_pitch(root_midi_base, 2, 3) # Index 2 in major scale is M3
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 10, False, pitch_e3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # C3 (Root, octave 3)
    pitch_c3 = get_midi_pitch(root_midi_base, 0, 3)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 15, False, pitch_c3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # Align to start of Bar 2 (next full bar)
    current_beat_pos = float(beats_per_bar)

    # --- Bar 2, 3, 4: C Major Chord (repeated for copy/paste concept) ---
    # Voicing: C3, E3, G3, C4
    chord_pitches_cmaj = [
        get_midi_pitch(root_midi_base, 0, 3), # C3
        get_midi_pitch(root_midi_base, 2, 3), # E3
        get_midi_pitch(root_midi_base, 4, 3), # G3
        get_midi_pitch(root_midi_base, 0, 4)  # C4
    ]
    
    # Velocities for each note in the chord (simulating automation)
    chord_vels = [velocity_base + 20, velocity_base + 10, velocity_base, velocity_base - 10]

    for bar_offset in range(1, bars): # Start from Bar 2 (index 1) up to 'bars'
        bar_start_beat = float(bar_offset * beats_per_bar)
        for i, pitch in enumerate(chord_pitches_cmaj):
            velocity = max(1, min(127, chord_vels[i] + (bar_offset * 5))) # Add slight variation per bar
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, velocity, False, pitch, 0)
            note_count += 1

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_FreeTemporary(midi_take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"

