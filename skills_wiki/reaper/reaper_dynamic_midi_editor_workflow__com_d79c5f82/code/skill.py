import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a multi-instrument MIDI composition demonstrating the dynamic REAPER MIDI editor workflow.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., individual track velocities).

    Returns:
        Status string, e.g., "Created 'Drums' with 32 notes over 4 bars at 120 BPM"
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
    # Drum map for ReaSamplOmatic5000 (standard GM map for drums)
    DRUM_MAP = {
        "kick": 36, "snare": 38, "hi_hat_closed": 42, "hi_hat_open": 46, "crash": 49
    }

    # Ensure scale exists
    if scale not in SCALES:
        return f"Error: Scale '{scale}' not found."

    # Get root MIDI value
    root_midi = NOTE_MAP.get(key, 0) + 48 # Base C4 for melodies/chords

    # Get scale degrees
    current_scale = SCALES[scale]

    def get_midi_note(degree, octave_offset=0):
        if 0 <= degree < len(current_scale):
            return root_midi + current_scale[degree] + (octave_offset * 12)
        return root_midi + (degree * 1) + (octave_offset * 12) # Fallback if degree out of bounds

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_names = ["DRUMS", "BASS", "GTR RHY", "GTR LEAD"]
    tracks = {}
    for name in track_names:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track

        # Add basic FX (ReaEQ, ReaComp)
        RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
        RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)

    # === Step 3: Create MIDI Items and insert notes ===
    beats_per_bar = 4
    quarter_note_len = 60.0 / bpm
    item_length_beats = beats_per_bar * bars
    item_length_sec = quarter_note_len * item_length_beats

    notes_inserted_count = 0

    # --- DRUMS ---
    drum_track = tracks["DRUMS"]
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    RPR.RPR_MIDI_SetItemExt(drum_take, "", 0, 0, 0, 0) # Clear existing MIDI

    # Add ReaSamplOmatic5000 and load dummy samples (user to replace)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
    # Configure ReaSamplOmatic5000 for multiple samples if needed, but for now, just for kicks/snares
    # Note: Loading actual samples via script is complex and depends on file paths.
    # User will need to manually load desired drum samples into ReaSamplOmatic5000.

    midi_events = RPR.MIDI_GetAllEvts(drum_take, "") # For older versions of Reaper, need to pass True to enable editing
    RPR.MIDI_SetItemExt(drum_take, midi_events, len(midi_events), 0, 0, 0)
    
    # Drum pattern (Kick on 1 & 3, Snare on 2 & 4, Hi-hat 1/8ths)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        # Kick
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat, bar_start_beat + quarter_note_len, 0, DRUM_MAP["kick"], kwargs.get("kick_velocity", velocity_base + 10), False)
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + 2*quarter_note_len, bar_start_beat + 3*quarter_note_len, 0, DRUM_MAP["kick"], kwargs.get("kick_velocity", velocity_base + 10), False)
        # Snare
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + quarter_note_len, bar_start_beat + 2*quarter_note_len, 0, DRUM_MAP["snare"], kwargs.get("snare_velocity", velocity_base), False)
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + 3*quarter_note_len, bar_start_beat + 4*quarter_note_len, 0, DRUM_MAP["snare"], kwargs.get("snare_velocity", velocity_base), False)
        # Hi-hat (1/8th notes)
        for i in range(8):
            RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + i * quarter_note_len / 2, bar_start_beat + (i+0.5) * quarter_note_len / 2, 0, DRUM_MAP["hi_hat_closed"], kwargs.get("hi_hat_velocity", velocity_base - 20), False)
        notes_inserted_count += 12 # 2 kick, 2 snare, 8 hi-hat per bar

    RPR.MIDI_Sort(drum_take)
    RPR.MIDI_CommitItem(drum_take)

    # --- GUITAR RHYTHM (Chords) ---
    gtr_rhy_track = tracks["GTR RHY"]
    gtr_rhy_item = RPR.RPR_AddMediaItemToTrack(gtr_rhy_track)
    RPR.RPR_SetMediaItemInfo_Value(gtr_rhy_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(gtr_rhy_item, "D_LENGTH", item_length_sec)
    gtr_rhy_take = RPR.RPR_AddTakeToMediaItem(gtr_rhy_item)
    RPR.RPR_MIDI_SetItemExt(gtr_rhy_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(gtr_rhy_track, "ReaSynth", False, -1)
    
    # Chord progression: Gm, Cm, Dm, EbM
    chords_progression = [
        [get_midi_note(0, 0), get_midi_note(2, 0), get_midi_note(4, 0)], # Gm (0, 2, 4 in G minor)
        [get_midi_note(3, 0), get_midi_note(5, 0), get_midi_note(7, 0)], # Cm (root of C, which is 3rd degree of G minor, + minor 3rd (Eb=5), perfect 5th (G=7))
        [get_midi_note(4, 0), get_midi_note(6, 0), get_midi_note(8, 0)], # Dm (root of D, which is 4th degree of G minor, + minor 3rd (F=6), perfect 5th (A=8))
        [get_midi_note(5, 0), get_midi_note(7, 0), get_midi_note(9, 0)], # EbM (root of Eb, which is 5th degree of G minor, + major 3rd (G=7), perfect 5th (Bb=9))
    ]
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        current_chord_notes = chords_progression[bar % len(chords_progression)]
        for note_midi in current_chord_notes:
            RPR.MIDI_InsertNote(gtr_rhy_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, 0, note_midi, kwargs.get("chord_velocity", velocity_base - 10), False)
            notes_inserted_count += 1
    RPR.MIDI_Sort(gtr_rhy_take)
    RPR.MIDI_CommitItem(gtr_rhy_take)

    # --- BASS ---
    bass_track = tracks["BASS"]
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    RPR.RPR_MIDI_SetItemExt(bass_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1) # Use ReaSynth for bass
    
    # Bass follows root notes of chords, one octave lower
    bass_roots = [get_midi_note(0, -1), get_midi_note(3, -1), get_midi_note(4, -1), get_midi_note(5, -1)]
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        root_midi = bass_roots[bar % len(bass_roots)]
        RPR.MIDI_InsertNote(bass_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, 0, root_midi, kwargs.get("bass_velocity", velocity_base + 5), False)
        notes_inserted_count += 1
    RPR.MIDI_Sort(bass_take)
    RPR.MIDI_CommitItem(bass_take)

    # --- GUITAR LEAD ---
    gtr_lead_track = tracks["GTR LEAD"]
    gtr_lead_item = RPR.RPR_AddMediaItemToTrack(gtr_lead_track)
    RPR.RPR_SetMediaItemInfo_Value(gtr_lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(gtr_lead_item, "D_LENGTH", item_length_sec)
    gtr_lead_take = RPR.RPR_AddTakeToMediaItem(gtr_lead_item)
    RPR.RPR_MIDI_SetItemExt(gtr_lead_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(gtr_lead_track, "ReaSynth", False, -1) # Use ReaSynth for lead

    # Simple arpeggiated lead line (G minor pentatonic over Gm, Cm, Dm, EbM)
    lead_pattern_beats = quarter_note_len / 2 # 1/8th notes
    lead_notes = [
        (get_midi_note(0, 1), 0), (get_midi_note(3, 1), 1), (get_midi_note(5, 1), 2), (get_midi_note(7, 1), 3), # Gm arpeggio
        (get_midi_note(3, 1), 4), (get_midi_note(5, 1), 5), (get_midi_note(7, 1), 6), (get_midi_note(8, 1), 7), # Cm arpeggio
        (get_midi_note(4, 1), 8), (get_midi_note(6, 1), 9), (get_midi_note(8, 1), 10), (get_midi_note(10, 1), 11), # Dm arpeggio
        (get_midi_note(5, 1), 12), (get_midi_note(7, 1), 13), (get_midi_note(9, 1), 14), (get_midi_note(11, 1), 15), # EbM arpeggio
    ]
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for note_midi_offset, beat_offset in lead_notes:
            RPR.MIDI_InsertNote(gtr_lead_take, False, False, bar_start_beat + beat_offset * lead_pattern_beats, bar_start_beat + (beat_offset + 0.5) * lead_pattern_beats, 0, note_midi_offset, kwargs.get("lead_velocity", velocity_base + 20), False)
            notes_inserted_count += 1
    RPR.MIDI_Sort(gtr_lead_take)
    RPR.MIDI_CommitItem(gtr_lead_take)

    RPR.RPR_UpdateArrange()

    return f"Created '{', '.join(track_names)}' tracks with {notes_inserted_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."

