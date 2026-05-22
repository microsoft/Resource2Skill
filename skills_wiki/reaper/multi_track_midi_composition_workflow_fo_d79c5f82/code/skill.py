import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a multi-track MIDI composition demonstrating workflow elements.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides for track names or specific notes.

    Returns:
        Status string, e.g., "Created 'Drums' with 32 notes over 4 bars at 120 BPM"
    """
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

    root_midi = NOTE_MAP.get(key, 0) # Default to C if key not found
    current_scale = SCALES.get(scale, SCALES["minor"])

    def get_midi_note(degree, octave, root=root_midi):
        return root + current_scale[degree % len(current_scale)] + (12 * octave)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    all_created_tracks_info = []

    # Track definitions
    track_configs = [
        {"name": kwargs.get("drums_track_name", "MIDI Drums"), "instrument": "ReaSamplOmatic5000", "notes": []},
        {"name": kwargs.get("bass_track_name", "BASS"), "instrument": "ReaSynth", "notes": []},
        {"name": kwargs.get("gtr_rhy_track_name", "GTR RHY"), "instrument": "ReaSynth", "notes": []},
        {"name": kwargs.get("gtr_lead_track_name", "GTR LEAD"), "instrument": "ReaSynth", "notes": []},
    ]

    # Chord progression (Am, G, C, F) mapped to MIDI roots for A minor
    # Am (A), G (G), C (C), F (F)
    chord_roots = [
        get_midi_note(0, 2), # A2 for Am
        get_midi_note(5, 2), # G2 for G
        get_midi_note(2, 3), # C3 for C
        get_midi_note(4, 2)  # F2 for F
    ]
    
    # Initialize notes for each track based on the demo
    # GTR RHY (Power chords: Root, +7, +12)
    gtr_rhy_notes_pattern = []
    for bar_offset in range(bars):
        root = chord_roots[bar_offset % len(chord_roots)]
        gtr_rhy_notes_pattern.extend([
            (root, bar_offset + 0.0, 2.0, velocity_base),          # Root
            (root + 7, bar_offset + 0.0, 2.0, velocity_base),      # Fifth
            (root + 12, bar_offset + 0.0, 2.0, velocity_base)     # Octave
        ])

    # BASS (Root notes, 8th notes)
    bass_notes_pattern = []
    for bar_offset in range(bars):
        root = chord_roots[bar_offset % len(chord_roots)] - 12 # One octave lower for bass
        bass_notes_pattern.extend([
            (root, bar_offset + 0.0, 0.5, velocity_base),
            (root, bar_offset + 0.5, 0.5, velocity_base),
            (root, bar_offset + 1.0, 0.5, velocity_base),
            (root, bar_offset + 1.5, 0.5, velocity_base),
            (root, bar_offset + 2.0, 0.5, velocity_base),
            (root, bar_offset + 2.5, 0.5, velocity_base),
            (root, bar_offset + 3.0, 0.5, velocity_base),
            (root, bar_offset + 3.5, 0.5, velocity_base),
        ])

    # MIDI Drums
    drum_notes_pattern = []
    for bar_offset in range(bars):
        # Kick (C1/MIDI 36) - on 1 and 3
        drum_notes_pattern.extend([
            (36, bar_offset + 0.0, 0.25, velocity_base),
            (36, bar_offset + 2.0, 0.25, velocity_base),
        ])
        # Snare (D1/MIDI 38) - on 2 and 4
        drum_notes_pattern.extend([
            (38, bar_offset + 1.0, 0.25, velocity_base),
            (38, bar_offset + 3.0, 0.25, velocity_base),
        ])
        # Hi-hat (F#1/MIDI 42) - 8th notes
        for beat in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            drum_notes_pattern.append((42, bar_offset + beat, 0.25, velocity_base - 10))
    
    # Tom fills in last bar (based on 11:29-11:31 in video for 4-bar loop)
    if bars >= 4:
        last_bar_offset = bars - 1
        drum_notes_pattern.extend([
            (45, last_bar_offset + 3.0, 0.25, velocity_base), # Tom 1 (A1)
            (43, last_bar_offset + 3.5, 0.25, velocity_base), # Tom 2 (G1)
            (47, last_bar_offset + 0.0, 0.25, velocity_base + 10) # Crash
        ])


    # GTR LEAD (Arpeggiated melody over chords)
    gtr_lead_notes_pattern = []
    lead_arpeggios = [
        [get_midi_note(0, 3), get_midi_note(2, 3), get_midi_note(4, 3), get_midi_note(0, 4)], # Am: A3, C4, E4, A4
        [get_midi_note(5, 3), get_midi_note(7, 3), get_midi_note(9, 3), get_midi_note(5, 4)], # G: G3, B3, D4, G4
        [get_midi_note(2, 4), get_midi_note(4, 4), get_midi_note(7, 4), get_midi_note(2, 5)], # C: C4, E4, G4, C5
        [get_midi_note(4, 3), get_midi_note(0, 4), get_midi_note(2, 4), get_midi_note(4, 4)], # F: F3, A3, C4, F4
    ]

    for bar_offset in range(bars):
        arpeggio = lead_arpeggios[bar_offset % len(lead_arpeggios)]
        # First 2 beats as 1/16th arpeggio
        for i, note_pitch in enumerate(arpeggio):
            gtr_lead_notes_pattern.append((note_pitch, bar_offset + i * 0.25, 0.25, velocity_base))
        # Second 2 beats as sustained note (e.g., the 3rd note of the arpeggio)
        gtr_lead_notes_pattern.append((arpeggio[2], bar_offset + 2.0, 2.0, velocity_base))

    track_configs[0]["notes"] = drum_notes_pattern
    track_configs[1]["notes"] = bass_notes_pattern
    track_configs[2]["notes"] = gtr_rhy_notes_pattern
    track_configs[3]["notes"] = gtr_lead_notes_pattern

    for i, config in enumerate(track_configs):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", config["name"], True)
        RPR.RPR_GetSetMediaTrackInfo_Value(track, "I_WNDCMDX", i + 1) # Set track color for demo

        # Add instrument FX
        if config["instrument"] == "ReaSamplOmatic5000":
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
            # No specific sample loaded via script due to file path dependencies
        elif config["instrument"] == "ReaSynth":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Basic preset selection (ReaSynth has limited scriptable presets easily)
            # For a more "guitar-like" sound on GTR RHY/LEAD, manual tweaking of ReaSynth or a VSTi would be needed.

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * (60.0 / bpm) * 4) # 4 beats per bar
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Prepare MIDI for insertion
        RPR.RPR_MIDI_SetItemExtents(take, 0, 0, bars * 4) # Set MIDI item length in beats
        RPR.RPR_MIDI_Clear(take) # Clear any default notes

        midi_editor = RPR.RPR_MIDIEditor_GetActive()
        if not midi_editor: # If editor not open, open it for the first track
            if i == 0:
                RPR.RPR_Main_OnCommand(40868, 0) # Open MIDI editor (any item)
                midi_editor = RPR.RPR_MIDIEditor_GetActive()
        
        if midi_editor:
             # Ensure the MIDI editor is showing track colors if already open
             # This is a UI preference and not directly set by script in a simple way.
             # RPR.MIDIEditor_SetSetting_int(midi_editor, "Display: Color notes by", 3) # 3 for track color (approx, actual index varies by REAPER version)
             RPR.RPR_MIDIEditor_OnCommand(midi_editor, 40166) # Action: View: Color notes by track


        for note_pitch, start_beat, duration_beats, velocity in config["notes"]:
            start_pos = start_beat * (60.0 / bpm) # Convert beats to seconds
            end_pos = (start_beat + duration_beats) * (60.0 / bpm) # Convert beats to seconds
            RPR.MIDI_InsertNote(take, False, False, start_pos, end_pos, velocity, False, note_pitch, False)
        
        RPR.MIDI_Sort(take)
        RPR.MIDI_Commit(take)

        all_created_tracks_info.append(f"'{config['name']}' with {len(config['notes'])} notes")
    
    return f"Created tracks: {', '.join(all_created_tracks_info)} over {bars} bars at {bpm} BPM in {project_name}."


