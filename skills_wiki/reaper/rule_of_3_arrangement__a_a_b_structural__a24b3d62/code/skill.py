def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' arrangement (A-A-B structure) in REAPER.
    Generates 12 bars: 
      - Bars 1-4: Idea A
      - Bars 5-8: Idea A (Repeated)
      - Bars 9-12: Idea B (Variation)
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Helper to get MIDI pitch from scale degree (1-indexed, e.g., 1=root, 2=second)
    def get_pitch(degree, octave_offset=0):
        deg_zero = degree - 1
        octave_shift = deg_zero // 7
        scale_idx = deg_zero % 7
        return root_midi + (octave_shift * 12) + scale_intervals[scale_idx] + (octave_offset * 12)

    # === Step 1: Initialize Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    ticks_per_beat = 960  # Standard MIDI PPQ
    ticks_per_bar = ticks_per_beat * beats_per_bar

    # === Step 2: Create Tracks ===
    def setup_track(name, synth_volume=-12.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        # Add basic Synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 10**(synth_volume/20))
        return track

    chords_track = setup_track(f"{track_name}_Chords", -14.0)
    melody_track = setup_track(f"{track_name}_Melody", -10.0)

    # === Step 3: Create Items & Takes ===
    total_length_sec = (60.0 / bpm) * beats_per_bar * 12
    
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    
    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", total_length_sec)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)

    # === Step 4: Arrangement Logic (The Rule of 3) ===
    # A Section Progression: I - V - vi - IV
    progression_a = [1, 5, 6, 4] 
    # B Section Progression (Variation): ii - V - I - vi
    progression_b = [2, 5, 1, 6]

    note_count = 0

    def add_chord(take, degree, start_bar, duration_bars=1):
        nonlocal note_count
        start_ppq = start_bar * ticks_per_bar
        end_ppq = start_ppq + (duration_bars * ticks_per_bar) - 60 # slight gap
        
        # Triad voicing (Root, 3rd, 5th)
        notes = [get_pitch(degree, -1), get_pitch(degree + 2, -1), get_pitch(degree + 4, -1)]
        for p in notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base, False)
            note_count += 1

    def add_melody_a(take, start_bar):
        nonlocal note_count
        # Simple rhythmic motif introducing the theme
        # Plays on beats 1, 2.5, and 4
        ppq_base = start_bar * ticks_per_bar
        rhythms = [(0, 1), (1.5, 1), (3, 1)] # (beat_start, beat_duration)
        degrees = [1, 2, 3]
        
        for i, (b_start, b_dur) in enumerate(rhythms):
            s_ppq = ppq_base + int(b_start * ticks_per_beat)
            e_ppq = s_ppq + int(b_dur * ticks_per_beat) - 30
            RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, get_pitch(degrees[i], 1), velocity_base + 10, False)
            note_count += 1

    def add_melody_b(take, start_bar):
        nonlocal note_count
        # Contrast motif: faster rhythm, higher register to break the repetition
        # Plays 8th notes
        ppq_base = start_bar * ticks_per_bar
        rhythms = [(0, 0.5), (0.5, 0.5), (1, 0.5), (2, 1.5)]
        degrees = [5, 4, 3, 2]
        
        for i, (b_start, b_dur) in enumerate(rhythms):
            s_ppq = ppq_base + int(b_start * ticks_per_beat)
            e_ppq = s_ppq + int(b_dur * ticks_per_beat) - 30
            RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, get_pitch(degrees[i], 1), velocity_base + 15, False)
            note_count += 1

    # --- Generate the 12-Bar Form ---
    for bar in range(12):
        if bar < 4:
            # 1st Time: Introduce Idea A
            chord = progression_a[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_a(melody_take, bar)
            
        elif bar < 8:
            # 2nd Time: Reinforce Idea A (Exact Repeat)
            chord = progression_a[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_a(melody_take, bar)
            
        else:
            # 3rd Time: The "Rule of 3" Variation (Idea B)
            chord = progression_b[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_b(melody_take, bar)

    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(melody_take)

    return f"Created Rule of 3 Arrangement (A-A-B structure): {note_count} notes over 12 bars at {bpm} BPM in {key} {scale}."
