def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Block",
    bpm: int = 120,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full 4-track musical arrangement (Drums, Bass, Chords, Lead) 
    and opens them in a unified MIDI editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks (will be appended).
        bpm: Tempo in BPM.
        key: Root note (e.g., "D", "C#").
        scale: Scale type ("minor", "major").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    if scale not in SCALES:
        scale = "minor"
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 2) + 48 # Base octave C3/D3
    scale_intervals = SCALES[scale]

    # Helper to get scale pitches dynamically across octaves
    def get_pitch(degree):
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[scale_idx] + (octave_shift * 12)

    # Standard i - VI - III - VII progression logic
    # In minor, scale degrees 0, 5, 2, 4 create this progression.
    progression = [0, 5, 2, 4] 

    # Setup tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars

    track_defs = [
        {"name": "DRUMS", "color": 0x1000000 | (150) | (50 << 8) | (150 << 16)},   # Purple
        {"name": "BASS", "color": 0x1000000 | (50) | (50 << 8) | (150 << 16)},     # Blue
        {"name": "CHORDS", "color": 0x1000000 | (150) | (100 << 8) | (50 << 16)},  # Orange
        {"name": "LEAD", "color": 0x1000000 | (50) | (150 << 8) | (150 << 16)}     # Cyan
    ]

    RPR.RPR_Undo_BeginBlock2(0)
    
    start_track_idx = RPR.RPR_CountTracks(0)
    created_items = []

    for i, tdef in enumerate(track_defs):
        # 1. Create Track
        RPR.RPR_InsertTrackAtIndex(start_track_idx + i, True)
        track = RPR.RPR_GetTrack(0, start_track_idx + i)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} - {tdef['name']}", True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", tdef["color"])
        
        # Add basic Synth to tonal tracks to make them audible
        if i > 0:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Attenuate volume to prevent clipping when layering
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

        # 2. Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        created_items.append(item)

        # 3. Populate MIDI Notes
        for bar in range(bars):
            bar_start = bar * bar_length_sec
            chord_degree = progression[bar % len(progression)]
            
            # Helper to insert notes converted to PPQ
            def add_note(start_time, end_time, pitch, vel):
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)

            if tdef["name"] == "DRUMS":
                # Kicks: Beat 1 and "and" of 3 (indices 0 and 5 of 8th notes)
                # Snare: Beat 2 and 4 (indices 2 and 6)
                # Hat: Every 8th note
                for eighth in range(8):
                    pos = bar_start + (eighth * (bar_length_sec / 8))
                    add_note(pos, pos + 0.05, 42, velocity_base - 20) # Hi-hat
                    if eighth in [0, 5]:
                        add_note(pos, pos + 0.1, 36, velocity_base) # Kick
                    if eighth in [2, 6]:
                        add_note(pos, pos + 0.1, 38, velocity_base) # Snare

            elif tdef["name"] == "BASS":
                # Root note, dropping an octave
                p = get_pitch(chord_degree) - 12
                add_note(bar_start, bar_start + bar_length_sec, p, velocity_base)

            elif tdef["name"] == "CHORDS":
                # Triad (Root, 3rd, 5th)
                for d in [chord_degree, chord_degree + 2, chord_degree + 4]:
                    add_note(bar_start, bar_start + bar_length_sec, get_pitch(d), velocity_base - 10)

            elif tdef["name"] == "LEAD":
                # Up-down arpeggio over the triad + octave
                arp_degrees = [chord_degree, chord_degree + 2, chord_degree + 4, chord_degree + 7]
                arp_pattern = [0, 1, 2, 3, 2, 1, 0, 1] # Up and down
                
                for eighth in range(8):
                    d = arp_degrees[arp_pattern[eighth]]
                    pos = bar_start + (eighth * (bar_length_sec / 8))
                    p = get_pitch(d) + 12 # Octave up
                    add_note(pos, pos + (bar_length_sec / 8.5), p, velocity_base)

        # Sort MIDI internally after loop
        RPR.RPR_MIDI_Sort(take)

    # 4. Workflow Emulation: Select all generated items and open in MIDI editor
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    for item in created_items:
        RPR.RPR_SetMediaItemInfo_Value(item, "B_UISEL", 1.0)
    
    # Item: Open in built-in MIDI editor (This will display the multi-track view from the tutorial)
    RPR.RPR_Main_OnCommand(40153, 0) 

    RPR.RPR_Undo_EndBlock2(0, "Create Multi-Track Arrangement Block", -1)

    return f"Created 4 tracks (Drums, Bass, Chords, Lead) with {bars} bars at {bpm} BPM in {key} {scale}."
