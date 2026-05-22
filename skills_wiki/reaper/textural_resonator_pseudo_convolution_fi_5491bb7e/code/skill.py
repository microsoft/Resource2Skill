def create_pattern(
    project_name: str = "Creative_Convolution",
    track_name: str = "Textural Resonator (Comb IR)",
    bpm: int = 110,
    key: str = "D",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Textural Resonator track that simulates creative Foley convolution 
    using cascaded micro-delays (comb filters) and short transient MIDI bursts.
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

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Step 2: Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Step 3: Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Resolve scale and root
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Generate wide voicings to feed a broad frequency spectrum into the resonator
    chord_degrees = [
        [0, 2, 4],  # i
        [3, 5, 7],  # iv
        [4, 6, 8],  # v
        [0, 2, 4]   # i
    ]

    def get_midi_note(degree_idx, octave):
        # Handle wrap-around for degrees larger than scale length
        scale_len = len(scale_intervals)
        octave_offset = degree_idx // scale_len
        rem_degree = degree_idx % scale_len
        return root_val + scale_intervals[rem_degree] + (octave + octave_offset) * 12

    # Rhythm: Syncopated sparse hits. We use EXTREMELY short notes (0.05 beats)
    # This creates the "transient ping" needed to excite the comb filters.
    rhythm_pattern = [0.0, 1.5, 2.75, 3.5] 
    note_length_beats = 0.05 
    note_count = 0

    for bar in range(bars):
        chord_idx = bar % len(chord_degrees)
        current_chord = chord_degrees[chord_idx]
        bar_start_beat = bar * beats_per_bar

        for beat_offset in rhythm_pattern:
            start_pos = (bar_start_beat + beat_offset) * (60.0 / bpm)
            end_pos = start_pos + (note_length_beats * (60.0 / bpm))

            # Build a wide 4-note chord
            for i, degree in enumerate(current_chord):
                # Spread notes across octaves (e.g. Bass, Mid, High)
                octave = 3 if i == 0 else (4 if i == 1 else 5)
                note = get_midi_note(degree, octave)
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_pos, end_pos, 
                    1, note, velocity_base, False
                )
                note_count += 1
            
            # Add an extra high "sparkle" note to excite high-frequency reflections
            high_note = get_midi_note(current_chord[0], 6)
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_pos, end_pos, 
                1, high_note, int(velocity_base * 0.8), False
            )
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # Step 4: Setup FX Chain
    
    # 4A. Transient Sound Source (ReaSynth)
    # Serves as the raw, dry acoustic strike.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 4B. The Pseudo-Convolution Imprint (Cascaded Micro-Delays)
    # These act as a fixed, complex comb filter, mathematically identical 
    # to a physical object's acoustic fingerprint.
    
    delays = [
        {"ms": 7.0,  "fbk": 65.0,  "mix": 60.0},  # Sharp metallic resonance
        {"ms": 11.0, "fbk": -50.0, "mix": 70.0},  # Phase cancellation hollow
        {"ms": 19.0, "fbk": 55.0,  "mix": 50.0},  # Lower mid body
        {"ms": 29.0, "fbk": -45.0, "mix": 40.0},  # Wood/plastic flutter
    ]

    for d in delays:
        delay_idx = RPR.RPR_TrackFX_AddByName(track, "JS: delay", False, -1)
        # JS: delay standard parameters: 0:Delay(ms), 1:Feedback(%), 2:Mix(%)
        RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, d["ms"])
        RPR.RPR_TrackFX_SetParam(track, delay_idx, 1, d["fbk"])
        RPR.RPR_TrackFX_SetParam(track, delay_idx, 2, d["mix"])

    return f"Created '{track_name}' with {note_count} transient triggers over {bars} bars at {bpm} BPM, routed through a 4-stage pseudo-convolution resonator."
