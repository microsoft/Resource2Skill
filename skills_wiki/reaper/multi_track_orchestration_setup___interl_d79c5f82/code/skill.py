def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Logic_Workflow_Scaffold",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a colored, 4-track interlocking MIDI arrangement to demonstrate 
    multi-track MIDI editing workflows.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "B", "C").
        scale: Scale type (e.g., "minor", "major").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

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

    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "minor"

    root_midi = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # Helper: Convert scale degree to MIDI pitch
    def get_pitch(degree: int, octave: int) -> int:
        normalized_degree = degree % len(scale_intervals)
        octave_offset = degree // len(scale_intervals)
        return root_midi + ((octave + octave_offset) * 12) + scale_intervals[normalized_degree]

    # Progression: i - VI - III - VII (mapped to scale degrees relative to root)
    # In 0-indexed minor: 0 (i), 5 (VI), 2 (III), 6 (VII)
    # Standardized to sound good in most scales: Root, 5th degree down, 2nd degree up, 6th degree down
    chord_progression_degrees = [0, -2, 2, -1] 

    # Colors (R, G, B) converted to REAPER native
    def make_color(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    track_setup = [
        {"name": f"{track_name}_Drums", "color": make_color(0, 200, 100), "type": "drums"},
        {"name": f"{track_name}_Bass", "color": make_color(150, 50, 200), "type": "bass"},
        {"name": f"{track_name}_Chords", "color": make_color(255, 150, 0), "type": "chords"},
        {"name": f"{track_name}_Lead", "color": make_color(50, 150, 255), "type": "lead"}
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    # Start position at current edit cursor
    start_time = RPR.RPR_GetCursorPosition()

    # Track insertion loop
    created_tracks = 0
    total_notes = 0
    start_track_idx = RPR.RPR_CountTracks(0)

    for i, ts in enumerate(track_setup):
        track_idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Naming and Coloring
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", ts["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", ts["color"])

        # Add generic Synth for harmonic content to be audible
        if ts["type"] != "drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create Item and Take
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Helper to add MIDI notes
        def add_note(pitch: int, pos_beats: float, len_beats: float, vel: int):
            nonlocal total_notes
            start_sec = start_time + (pos_beats * (60.0 / bpm))
            end_sec = start_sec + (len_beats * (60.0 / bpm))
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes += 1

        # Generate Musical Patterns
        for bar in range(bars):
            bar_beat_offset = bar * beats_per_bar
            prog_idx = bar % len(chord_progression_degrees)
            root_degree = chord_progression_degrees[prog_idx]

            if ts["type"] == "drums":
                for beat in range(4):
                    # Kick on 1, 3
                    if beat == 0 or beat == 2:
                        add_note(36, bar_beat_offset + beat, 0.25, velocity_base)
                    # Syncopated kick
                    if beat == 2:
                        add_note(36, bar_beat_offset + beat + 0.5, 0.25, int(velocity_base * 0.8))
                    # Snare on 2, 4
                    if beat == 1 or beat == 3:
                        add_note(38, bar_beat_offset + beat, 0.25, velocity_base)
                    # Hats every 8th note
                    add_note(42, bar_beat_offset + beat, 0.25, int(velocity_base * 0.7))
                    add_note(42, bar_beat_offset + beat + 0.5, 0.25, int(velocity_base * 0.5))

            elif ts["type"] == "bass":
                pitch = get_pitch(root_degree, 3) # Octave 3 bass
                # 8th note driving pulse
                for eighth in range(8):
                    pos = bar_beat_offset + (eighth * 0.5)
                    add_note(pitch, pos, 0.45, velocity_base if eighth % 2 == 0 else int(velocity_base * 0.8))

            elif ts["type"] == "chords":
                # Triad block chords
                chord_pitches = [
                    get_pitch(root_degree, 4),      # Root
                    get_pitch(root_degree + 2, 4),  # Third
                    get_pitch(root_degree + 4, 4)   # Fifth
                ]
                for p in chord_pitches:
                    add_note(p, bar_beat_offset, 3.9, int(velocity_base * 0.7))

            elif ts["type"] == "lead":
                # Syncopated Arp/Motif
                arp_degrees = [root_degree + 4, root_degree + 2, root_degree] # 5th, 3rd, Root
                rhythms = [0.75, 1.5, 2.5] # Syncopated 16th/8th placements
                for i, r_pos in enumerate(rhythms):
                    p = get_pitch(arp_degrees[i], 5) # Octave 5
                    add_note(p, bar_beat_offset + r_pos, 0.25, velocity_base)

        RPR.RPR_MIDI_Sort(take)
        created_tracks += 1

    return f"Created 4-track interlocking scaffold ('{track_name}') in {key} {scale} containing {total_notes} notes over {bars} bars at {bpm} BPM."
