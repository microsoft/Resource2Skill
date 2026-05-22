def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "FullBand",
    bpm: int = 120,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Part Full Band Scaffold (Drums, Bass, Chords, Lead) 
    to demonstrate multi-track MIDI arrangements.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the creation log.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (should be a multiple of 4).
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
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Fallbacks
    root_midi = NOTE_MAP.get(key, 2) + 48 # Default to Octave 4 (e.g., C4 = 48)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # 4-chord pop progression: 1, 5, 6, 4
    progression_degrees = [1, 5, 6, 4]

    # REAPER Custom Colors (R + 256*G + 65536*B | 0x1000000)
    COLOR_DRUMS = int(0x4B0082) | 0x1000000  # Indigo
    COLOR_BASS  = int(0x800080) | 0x1000000  # Purple
    COLOR_CHORD = int(0x008CFF) | 0x1000000  # Orange (BGR hex format -> FF8C00 is Orange)
    COLOR_LEAD  = int(0xFFB400) | 0x1000000  # Deep Blue (BGR)

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def get_chord_notes(degree, root_note, intervals):
        """Returns the MIDI notes for a triad based on the scale degree (1-indexed)."""
        idx1 = (degree - 1) % len(intervals)
        idx3 = (degree + 1) % len(intervals)
        idx5 = (degree + 3) % len(intervals)

        oct1 = (degree - 1) // len(intervals)
        oct3 = (degree + 1) // len(intervals)
        oct5 = (degree + 3) // len(intervals)

        n1 = root_note + intervals[idx1] + (oct1 * 12)
        n3 = root_note + intervals[idx3] + (oct3 * 12)
        n5 = root_note + intervals[idx5] + (oct5 * 12)
        return [n1, n3, n5]

    def insert_note(take, start_beat, end_beat, pitch, vel):
        """Helper to insert MIDI notes accurately via PPQ."""
        start_pos = (start_beat * 60.0 / bpm)
        end_pos = (end_beat * 60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    def create_track_with_item(name, color):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", color)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def setup_reasynth(track, vol, square, saw, tri):
        """Sets up native ReaSynth for sound design without external VSTs."""
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, vol)     # Vol
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, square)  # Square mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, saw)     # Saw mix
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, tri)     # Triangle mix

    # === Track 1: Drums ===
    track_drums, take_drums = create_track_with_item("MIDI Drums", COLOR_DRUMS)
    for b in range(bars):
        bar_start_beat = b * 4
        # Kick on 1 and 3
        insert_note(take_drums, bar_start_beat + 0.0, bar_start_beat + 0.5, 36, velocity_base)
        insert_note(take_drums, bar_start_beat + 2.0, bar_start_beat + 2.5, 36, velocity_base)
        # Snare on 2 and 4
        insert_note(take_drums, bar_start_beat + 1.0, bar_start_beat + 1.5, 38, velocity_base)
        insert_note(take_drums, bar_start_beat + 3.0, bar_start_beat + 3.5, 38, velocity_base)
        # 8th note High Hats
        for h in range(8):
            insert_note(take_drums, bar_start_beat + (h * 0.5), bar_start_beat + (h * 0.5) + 0.25, 42, velocity_base - 20)
        # Crash on downbeat of first bar
        if b % 4 == 0:
            insert_note(take_drums, bar_start_beat, bar_start_beat + 1.0, 49, velocity_base + 10)

    # === Track 2: Bass ===
    track_bass, take_bass = create_track_with_item("BASS", COLOR_BASS)
    setup_reasynth(track_bass, vol=0.5, square=0.0, saw=0.0, tri=0.8) # Sine/Tri for sub
    for b in range(bars):
        deg = progression_degrees[b % 4]
        chord = get_chord_notes(deg, root_midi, scale_intervals)
        bass_note = chord[0] - 24 # 2 octaves down
        bar_start_beat = b * 4
        insert_note(take_bass, bar_start_beat, bar_start_beat + 4.0, bass_note, velocity_base)

    # === Track 3: Rhythm Guitar (Chords) ===
    track_chords, take_chords = create_track_with_item("GTR RHY", COLOR_CHORD)
    setup_reasynth(track_chords, vol=0.15, square=0.0, saw=0.8, tri=0.0) # Saw for richness
    for b in range(bars):
        deg = progression_degrees[b % 4]
        chord = get_chord_notes(deg, root_midi, scale_intervals)
        bar_start_beat = b * 4
        for note in chord:
            insert_note(take_chords, bar_start_beat, bar_start_beat + 4.0, note - 12, velocity_base - 10)

    # === Track 4: Lead Guitar (Arpeggio) ===
    track_lead, take_lead = create_track_with_item("GTR LEAD", COLOR_LEAD)
    setup_reasynth(track_lead, vol=0.1, square=0.5, saw=0.5, tri=0.0) # Buzzy Square/Saw
    for b in range(bars):
        deg = progression_degrees[b % 4]
        chord = get_chord_notes(deg, root_midi, scale_intervals)
        bar_start_beat = b * 4
        
        # 8th note arpeggio pattern: Root, 3rd, 5th, 3rd, Root, 3rd, 5th, 3rd
        arp_pattern = [chord[0], chord[1], chord[2], chord[1], 
                       chord[0], chord[1], chord[2], chord[1]]
        
        for i, note in enumerate(arp_pattern):
            insert_note(take_lead, bar_start_beat + (i * 0.5), bar_start_beat + (i * 0.5) + 0.4, note + 12, velocity_base)

    # Sort MIDI events to ensure proper playback
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_lead)
    
    # Update timeline view
    RPR.RPR_UpdateArrange()

    return f"Created full band scaffold with 4 tracks (Drums, Bass, Chords, Lead) spanning {bars} bars in {key} {scale} at {bpm} BPM."
