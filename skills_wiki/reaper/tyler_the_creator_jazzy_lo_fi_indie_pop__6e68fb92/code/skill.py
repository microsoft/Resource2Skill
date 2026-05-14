def create_pattern(
    project_name: str = "FlowerBoy_Era",
    track_name: str = "Indie_Vibe",
    bpm: int = 90,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Tyler/Mac DeMarco style jazzy lo-fi arrangement in the current REAPER project.
    Generates Diatonic 7th chords, a groovy bassline, and boom-bap drums with heavy chorus FX.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    try:
        RPR.RPR_SetCurrentBPM(0, bpm, True)
    except AttributeError:
        # Fallback if SetCurrentBPM is unavailable in the specific Reaper version
        pass

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

    root_midi = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Timing calculations
    PPQ = 960 # Standard REAPER Pulses Per Quarter note
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    def get_diatonic_note(degree, base_midi):
        """Calculates exact MIDI pitch for a given scale degree."""
        octave = degree // len(scale_intervals)
        rem = degree % len(scale_intervals)
        return base_midi + scale_intervals[rem] + (12 * octave)

    def create_track_with_midi(name_suffix):
        """Helper to create a track, item, and take safely."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name_suffix}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === Step 2: Create Tracks and Takes ===
    chords_track, chords_take = create_track_with_midi("Woozy_Chords")
    bass_track, bass_take = create_track_with_midi("Groove_Bass")
    drums_track, drums_take = create_track_with_midi("LoFi_Drums")

    # === Step 3: Populate MIDI Data ===
    # Progression: IV - iii - ii - I (degrees 3, 2, 1, 0 zero-indexed)
    progression = [3, 2, 1, 0] 

    for b in range(bars):
        chord_degree = progression[b % len(progression)]
        bar_ppq_start = b * beats_per_bar * PPQ

        # 1. Chords (7th chords)
        chord_base_midi = root_midi + 60 # C4 baseline
        for offset in [0, 2, 4, 6]: # Root, 3rd, 5th, 7th
            pitch = get_diatonic_note(chord_degree + offset, chord_base_midi)
            start_ppq = bar_ppq_start
            end_ppq = start_ppq + (beats_per_bar * PPQ) # Sustains for full bar
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 15, False)

        # 2. Bass (Syncopated groove)
        bass_base_midi = root_midi + 36 # C2 baseline
        bass_pitch = get_diatonic_note(chord_degree, bass_base_midi)
        
        # Rhythm offsets in beats: (start_beat, duration_in_beats)
        bass_groove = [(0.0, 1.0), (1.5, 1.0), (2.75, 0.25), (3.0, 1.0)]
        for start_beat, dur_beat in bass_groove:
            start_ppq = int(bar_ppq_start + (start_beat * PPQ))
            end_ppq = int(start_ppq + (dur_beat * PPQ))
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, False)

        # 3. Drums (Boom-bap)
        # Kick (MIDI 36)
        for kb in [0.0, 1.5, 2.5]:
            start_ppq = int(bar_ppq_start + (kb * PPQ))
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 240, 0, 36, velocity_base, False)
        # Snare (MIDI 38)
        for sb in [1.0, 3.0]:
            start_ppq = int(bar_ppq_start + (sb * PPQ))
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 240, 0, 38, velocity_base + 10, False)
        # Hi-hat (MIDI 42)
        for hb in range(8): # Every 8th note
            start_ppq = int(bar_ppq_start + (hb * 0.5 * PPQ))
            vel = velocity_base if hb % 2 == 0 else velocity_base - 20 # Accent downbeats
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, start_ppq + 120, 0, 42, vel, False)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drums_take)

    # === Step 4: Apply Sound Design (FX Chains) ===
    
    # Chords FX (Synth Keys + Tape Warble + Lo-fi EQ)
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, 0, 1, 0.4) # Sawtooth mix
    RPR.RPR_TrackFX_SetParam(chords_track, 0, 2, 0.6) # Triangle mix
    
    # "Mac DeMarco ass effects" - Heavy Chorus for pitch vibrato
    RPR.RPR_TrackFX_AddByName(chords_track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, 1, 1, 1.5) # Rate (Slow)
    RPR.RPR_TrackFX_SetParam(chords_track, 1, 2, 7.0) # Depth (Deep tape wow)
    RPR.RPR_TrackFX_SetParam(chords_track, 1, 3, 1.0) # Wet mix
    
    # Lo-fi filter
    RPR.RPR_TrackFX_AddByName(chords_track, "JS: 3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, 2, 0, -15.0) # Cut Lows
    RPR.RPR_TrackFX_SetParam(chords_track, 2, 2, -15.0) # Cut Highs

    # Bass FX (Subby Triangle)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 1.0) # Pure Triangle
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.0) # No Saw
    RPR.RPR_TrackFX_AddByName(bass_track, "JS: 3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 2, -24.0) # Roll off all highs

    # Drums FX (Placeholder synth hit so MIDI generates audible ticks)
    RPR.RPR_TrackFX_AddByName(drums_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(drums_track, 0, 3, 0.0) # No sustain
    RPR.RPR_TrackFX_SetParam(drums_track, 0, 4, 0.05) # Plucky release
    RPR.RPR_TrackFX_AddByName(drums_track, "JS: 3-Band EQ", False, -1)
    RPR.RPR_TrackFX_SetParam(drums_track, 1, 2, -10.0) # Cut harsh highs

    return f"Created Flower Boy style arrangement across 3 tracks (Chords, Bass, Drums) for {bars} bars at {bpm} BPM."
