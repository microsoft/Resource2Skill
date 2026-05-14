def create_pattern(
    project_name: str = "SoulTheory",
    track_name: str = "R&B Sample",
    bpm: int = 88,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a layered Neo-Soul / R&B sample loop (Keys, Motown Bass, Strings) 
    using the signature VImaj7 -> vm7 progression.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (88 is ideal for this genre).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (defaults to minor for this progression).
        bars: Number of bars to generate (must be even for the 2-bar progression).
        velocity_base: Base MIDI velocity (0-127).
    """
    import reaper_python as RPR

    # Setup tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Music theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate roots for VI and v in a minor scale
    base_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # e.g., C3 = 48
    vi_root = base_midi + 8 # VI root (e.g., Ab in C minor)
    v_root = base_midi + 7  # v root (e.g., G in C minor)
    
    # 7th Chord Voicings (Root, 3rd, 5th, 7th)
    # VI is a Major 7th chord
    vi_maj7_chord = [vi_root, vi_root + 4, vi_root + 7, vi_root + 11]
    # v is a Minor 7th chord
    v_min7_chord = [v_root, v_root + 3, v_root + 7, v_root + 10]

    beats_per_bar = 4
    qn_length = 60.0 / bpm
    bar_length_sec = qn_length * beats_per_bar
    item_length = bar_length_sec * bars

    def create_layer(name, pan, synth_params, fx_names):
        """Helper to create a track, set up basic routing/FX, and return its take."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} - {name}", True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)

        # Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Add FX
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        for param_idx, value in synth_params.items():
            RPR.RPR_TrackFX_SetParam(track, fx_idx, param_idx, value)
            
        for fx in fx_names:
            RPR.RPR_TrackFX_AddByName(track, fx, False, -1)

        return take

    # --- SYNTH PARAMETER MAP (ReaSynth) ---
    # 1: Vol, 2: Square mix, 3: Saw mix, 4: Triangle mix
    # 6: Attack, 7: Decay, 8: Sustain, 9: Release

    # 1. CREATE KEYS (Electric Piano/Pad vibe)
    keys_params = {1: 0.1, 2: 0.4, 4: 0.8, 6: 0.05, 8: 0.8, 9: 0.4}
    take_keys = create_layer("Keys", -0.15, keys_params, ["ReaVerbate"])

    # 2. CREATE BASS (Motown Sub vibe)
    bass_params = {1: 0.2, 2: 0.0, 3: 0.0, 4: 1.0, 6: 0.01, 8: 1.0, 9: 0.1}
    take_bass = create_layer("Motown Bass", 0.0, bass_params, [])

    # 3. CREATE STRINGS (Slow attack, high sustain)
    strings_params = {1: 0.05, 2: 0.0, 3: 1.0, 4: 0.0, 6: 0.8, 8: 1.0, 9: 1.0}
    take_strings = create_layer("Strings", 0.15, strings_params, ["ReaVerbate"])

    # --- POPULATE MIDI ---
    for bar in range(bars):
        is_even_bar = (bar % 2 == 0)
        chord = vi_maj7_chord if is_even_bar else v_min7_chord
        bass_note = (vi_root if is_even_bar else v_root) - 24 # Drop 2 octaves
        string_note = chord[3] + 12 # Top note of the chord, up 1 octave

        bar_start_beat = bar * beats_per_bar
        
        # Keys: Whole note chords (held for full bar)
        start_time = bar_start_beat * qn_length
        end_time = (bar_start_beat + 4.0) * qn_length
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_keys, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_keys, end_time)
        
        for note in chord:
            RPR.RPR_MIDI_InsertNote(take_keys, False, False, start_ppq, end_ppq, 0, int(note), velocity_base - 10, False)

        # Strings: Whole note melody line
        start_ppq_str = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_strings, start_time)
        end_ppq_str = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_strings, end_time)
        RPR.RPR_MIDI_InsertNote(take_strings, False, False, start_ppq_str, end_ppq_str, 0, int(string_note), velocity_base - 15, False)

        # Bass: Motown Syncopated Rhythm
        # Hit 1: Beat 1 (Duration: 1.5 beats)
        # Hit 2: Beat 2.5 (Duration: 0.5 beats)
        # Hit 3: Beat 3 (Duration: 1 beat)
        bass_rhythm = [
            (0.0, 1.5, velocity_base),
            (1.5, 2.0, velocity_base - 15), # Ghost note/bounce
            (2.0, 3.5, velocity_base)
        ]
        
        for b_start, b_end, vel in bass_rhythm:
            b_start_time = (bar_start_beat + b_start) * qn_length
            b_end_time = (bar_start_beat + b_end) * qn_length
            b_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, b_start_time)
            b_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, b_end_time)
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, b_start_ppq, b_end_ppq, 0, int(bass_note), int(vel), False)

    # Sort MIDI to finalize
    RPR.RPR_MIDI_Sort(take_keys)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_strings)

    return f"Created R&B Sample loop '{track_name}' in {key} {scale} over {bars} bars at {bpm} BPM with Keys, Motown Bass, and Strings."
