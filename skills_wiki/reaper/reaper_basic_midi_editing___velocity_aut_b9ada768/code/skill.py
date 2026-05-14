import reaper_python as RPR
import math

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "MIDI Editor Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Demonstrates essential REAPER MIDI editor techniques: note creation, length adjustment,
    and velocity automation. Creates a scale and a chord with varying velocities.
    The pattern spans 4 bars: 2 bars for an ascending scale, followed by 2 bars for a sustained chord.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, pentatonic_minor, etc.).
        bars: Total number of bars for the MIDI item. The actual musical content will fill the first 4 bars.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides for future extensions.

    Returns:
        Status string, e.g., "Created 'MIDI Editor Demo' with MIDI notes and velocities over 4 bars at 120 BPM"
    """
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
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Ensure key and scale are valid
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Please choose from {list(NOTE_MAP.keys())}."
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Please choose from {list(SCALES.keys())}."

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add ReaSynth for sound (stock REAPER VSTi) ===
    # The tutorial uses an external VSTi: "Grand Piano (saulodai_v3) (x64)".
    # ReaSynth is used as a stock alternative for sound generation.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    seconds_per_8th_note = seconds_per_beat / 2
    seconds_per_whole_note = seconds_per_beat * beats_per_bar
    
    # The pattern will fill 4 bars of content. Item length matches requested bars.
    item_content_bars = 4 
    item_length_seconds = seconds_per_whole_note * bars 

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SNM_SetMediaItemTake_SourceMIDI(take, 1) # Set take to be new MIDI source

    # Ensure MIDI item extents match the desired length for editing
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length_seconds) 

    # Root MIDI note for the chosen key (e.g., C4 = 60)
    root_midi_base = NOTE_MAP[key]
    
    # Get scale degrees for the chosen scale
    current_scale_degrees = SCALES[scale]

    # Initialize MIDI event list
    midi_events = RPR.MIDI_CreateEvts()
    midi_notes_inserted = 0

    # === Section 1: Ascending Scale (First 2 bars) ===
    current_time_pos = 0.0
    scale_octave = 4 # Start base at C4
    notes_per_bar_for_scale = int(beats_per_bar / (seconds_per_8th_note / seconds_per_beat)) # 8 notes per bar for 8th notes

    for bar_num in range(min(2, bars)): # Generate scale for up to 2 bars or fewer if total bars is less
        for i in range(notes_per_bar_for_scale):
            if current_time_pos >= seconds_per_whole_note * item_content_bars: # Stop if exceeding content length
                break

            # Determine pitch: cycle through scale degrees, moving up an octave as needed
            scale_degree_idx = i % len(current_scale_degrees)
            octave_shift = i // len(current_scale_degrees) # How many full scale runs have occurred
            
            midi_pitch = root_midi_base + current_scale_degrees[scale_degree_idx] + ((scale_octave + octave_shift) * 12)
            
            # Simple velocity variation (simulating manual adjustment)
            velocity = max(60, min(127, velocity_base + int(math.sin(i * 0.5) * 20 + 10))) 

            RPR.MIDI_InsertNote(midi_events, 0, 0, current_time_pos, current_time_pos + seconds_per_8th_note, 0, velocity, midi_pitch, False)
            midi_notes_inserted += 1
            current_time_pos += seconds_per_8th_note
        if current_time_pos >= seconds_per_whole_note * item_content_bars: # Stop if exceeding content length
                break

    # === Section 2: Sustained Chord (Next 2 bars, starting from bar 3) ===
    # This section starts after the scale, at the beginning of the 3rd logical bar.
    chord_start_time = seconds_per_whole_note * 2 
    chord_duration = seconds_per_whole_note * 2 # Chord plays for 2 bars

    if chord_start_time < item_length_seconds: # Only add chord if there's space
        # C major triad intervals
        c_major_triad_intervals = [0, 4, 7] 
        chord_octave = 3 # Start at C3

        for interval in c_major_triad_intervals:
            midi_pitch = root_midi_base + interval + (chord_octave * 12)
            # Consistent, slightly louder velocity for the chord
            velocity = max(80, min(127, velocity_base + 15)) 
            
            # Ensure chord does not extend beyond item length
            actual_chord_end_time = min(chord_start_time + chord_duration, item_length_seconds)
            
            if actual_chord_end_time > chord_start_time: # Only insert if duration is positive
                RPR.MIDI_InsertNote(midi_events, 0, 0, chord_start_time, actual_chord_end_time, 0, velocity, midi_pitch, False)
                midi_notes_inserted += 1
    
    # Write all collected MIDI events to the take
    RPR.MIDI_SetEvts(take, midi_events, True)
    RPR.MIDI_FreeEvts(midi_events) # Free the MIDI events object

    return f"Created '{track_name}' with {midi_notes_inserted} notes (scale & chord) over {bars} bars at {bpm} BPM"

