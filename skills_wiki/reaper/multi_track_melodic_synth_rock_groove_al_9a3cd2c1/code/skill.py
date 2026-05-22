def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 160,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Track Melodic Synth-Rock Groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM (150-170 recommended for double-kick style).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks.
    """
    import reaper_python as RPR

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

    bpm = int(bpm)
    bars = int(bars)
    
    # Sync project tempo to our driving rhythm
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    root_midi = NOTE_MAP.get(key, 9) + 60 # Default around C4/A4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard i - VI - III - VII pop-punk/metalcore progression degrees
    progression = [0, 5, 2, 6]
    
    # Start generation at the user's current play/edit cursor
    cursor_pos = RPR.RPR_GetCursorPosition()

    def get_chord(degree, root_pitch, scale_int):
        """Builds a diatonic root-position triad for a given scale degree."""
        notes = []
        chord_root_octave = degree // len(scale_int)
        chord_root_deg = degree % len(scale_int)
        # Absolute pitch of the chord's root note
        base_pitch = root_pitch + scale_int[chord_root_deg] + (chord_root_octave * 12)
        
        # Build 1st, 3rd, 5th relative to the chord's position in the scale
        for i in [0, 2, 4]:
            abs_deg = degree + i
            octave = abs_deg // len(scale_int)
            deg = abs_deg % len(scale_int)
            pitch = root_pitch + scale_int[deg] + (octave * 12)
            notes.append(pitch)
        return notes

    def create_midi_track(name: str, notes_list: list, synth_type: str = None):
        """Helper to create a track, MIDI item, populate notes, and setup FX."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item_length = bars * 4 * (60.0 / bpm)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, cursor_pos, cursor_pos + item_length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # Insert Notes
        for n in notes_list:
            start_time = cursor_pos + n["start"] * (60.0 / bpm)
            end_time = cursor_pos + n["end"] * (60.0 / bpm)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = max(0, min(127, int(n["pitch"])))
            vel = max(1, min(127, int(n["vel"])))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            
        RPR.RPR_MIDI_Sort(take)
        
        # Setup Instrument/Timbre
        if synth_type == "pad":
            fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 3, 1.0) # Full Saw
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 6, 0.2) # Slow Attack
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 9, 0.4) # Lush Release
        elif synth_type == "bass":
            fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 2, 0.8) # Square for grit
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 3, 0.5) # Saw
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 8, 0.8) # High Sustain
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 9, 0.1) # Fast Release
        elif synth_type == "lead":
            fx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 3, 0.5) # Saw
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 4, 0.8) # Triangle for pluck tone
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 7, 0.15) # Fast Decay
            RPR.RPR_TrackFX_SetParamNormalized(track, fx, 8, 0.1) # Low Sustain
            RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
            
        return track

    # --- 1. Generate Synth Chords ---
    chord_notes = []
    for b in range(bars):
        chord_degree = progression[b % len(progression)]
        chord = get_chord(chord_degree, root_midi, scale_intervals)
        for pitch in chord:
            chord_notes.append({"start": b * 4, "end": b * 4 + 4, "pitch": pitch, "vel": velocity_base - 10})
    
    create_midi_track(f"Synth Chords ({key} {scale})", chord_notes, "pad")

    # --- 2. Generate Driving Bass ---
    bass_notes = []
    bass_root = root_midi - 24 # Drop 2 octaves
    for b in range(bars):
        chord_degree = progression[b % len(progression)]
        abs_deg = chord_degree
        octave = abs_deg // len(scale_intervals)
        deg = abs_deg % len(scale_intervals)
        bass_pitch = bass_root + scale_intervals[deg] + (octave * 12)
        
        # 8th note driving rhythm
        for step in range(8):
            start = b * 4 + step * 0.5
            end = start + 0.45 # Slight gap to accentuate the rhythmic drive
            bass_notes.append({"start": start, "end": end, "pitch": bass_pitch, "vel": velocity_base})
            
    create_midi_track("Driving Bass", bass_notes, "bass")

    # --- 3. Generate Double Kick Drums ---
    drum_notes = []
    for b in range(bars):
        # Crash on beat 1
        drum_notes.append({"start": b * 4, "end": b * 4 + 0.5, "pitch": 49, "vel": velocity_base})
        # Snare on beats 2 and 4
        drum_notes.append({"start": b * 4 + 1, "end": b * 4 + 1.25, "pitch": 38, "vel": velocity_base})
        drum_notes.append({"start": b * 4 + 3, "end": b * 4 + 3.25, "pitch": 38, "vel": velocity_base})
        # Unrelenting 16th note double kick
        for step in range(16):
            start = b * 4 + step * 0.25
            end = start + 0.125
            # Accentuate the downbeats
            vel = velocity_base if step % 4 == 0 else velocity_base - 15
            drum_notes.append({"start": start, "end": end, "pitch": 36, "vel": vel})
            
    create_midi_track("Double Kick Drums (GM)", drum_notes, None)

    # --- 4. Generate Polyrhythmic Arpeggio Lead ---
    lead_notes = []
    lead_root = root_midi + 12 # Up 1 octave
    arp_pattern = [0, 1, 2, 3, 2, 1] # 6-step up-and-down sweep
    
    for b in range(bars):
        chord_degree = progression[b % len(progression)]
        chord = get_chord(chord_degree, lead_root, scale_intervals)
        arp_pitches = chord + [chord[0] + 12] # Root, 3rd, 5th, Octave
        
        # Loop 6-step array over a 16-step grid
        for step in range(16):
            idx = arp_pattern[step % len(arp_pattern)]
            pitch = arp_pitches[idx]
            start = b * 4 + step * 0.25
            end = start + 0.2
            lead_notes.append({"start": start, "end": end, "pitch": pitch, "vel": velocity_base})
            
    create_midi_track("Arp Lead (Polyrhythm)", lead_notes, "lead")

    return f"Created multi-track Synth-Rock arrangement (Chords, Bass, Drums, Arp) spanning {bars} bars at {bpm} BPM in {key} {scale}."
