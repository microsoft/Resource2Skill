def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule_of_3_Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a musical demonstration of the "Rule of 3" in the current REAPER project.
    Generates three phrases (default 4 bars each, 12 bars total). Phrase 1 and 2 are identical. 
    Phrase 3 introduces harmonic variation and a climbing melodic crescendo to retain listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Length of the base phrase in bars (total generated length is bars * 3).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated sequence.
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Helper to calculate precise MIDI pitches based on scale degree
    def get_pitch(degree: int, base_octave: int) -> int:
        root_pitch = NOTE_MAP.get(key, 0)
        octave_offset = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        # +1 because Octave 4 starts at MIDI 60 (Middle C)
        return int(root_pitch + (base_octave + 1 + octave_offset) * 12 + scale_intervals[scale_degree])

    # === Step 1: Initialize Project Temp ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Additive Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add native plugins for immediate auditioning
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)

    # === Step 3: Math for Time and Length ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    total_bars = bars * 3
    item_length = bar_length_sec * total_bars
    
    # Create the media item
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(start_sec, end_sec, pitch, velocity):
        # Convert absolute seconds into MIDI PPQ for strict grid alignment
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        pitch = max(0, min(127, int(pitch)))
        velocity = max(1, min(127, int(velocity)))
        # pass True to noSort for batch speed; we'll sort at the end
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, True)

    # === Step 4: Rule of 3 Logic Execution ===
    
    # Diatonic scale degrees (0-indexed): I=0, ii=1, IV=3, V=4, vi=5
    prog_A = [0, 3, 5, 4]  # Phrase 1 & 2: I, IV, vi, V
    prog_B = [0, 3, 1, 4]  # Phrase 3: I, IV, ii, V (The Variation)
    
    chords_per_phrase = len(prog_A)
    beats_per_chord = (bars * beats_per_bar) / chords_per_phrase
    note_count = 0
    
    for phrase in range(3):
        is_phrase_B = (phrase == 2) # The 3rd repetition
        prog = prog_B if is_phrase_B else prog_A
        phrase_start_sec = phrase * bars * bar_length_sec
        
        for idx, root_deg in enumerate(prog):
            chord_start_sec = phrase_start_sec + idx * beats_per_chord * beat_len_sec
            chord_end_sec = chord_start_sec + (beats_per_chord - 0.2) * beat_len_sec
            
            # Stack fundamental thirds for chords
            chord_degrees = [root_deg, root_deg + 2, root_deg + 4]
            if is_phrase_B and idx == chords_per_phrase - 1:
                # Add the 7th scale degree to the final V chord for resolving tension
                chord_degrees.append(root_deg + 6) 
                
            # 1. Bass note layer
            insert_note(chord_start_sec, chord_end_sec, get_pitch(root_deg, 3), velocity_base - 10)
            note_count += 1
            
            # 2. Chord stack layer
            for deg in chord_degrees:
                insert_note(chord_start_sec, chord_end_sec, get_pitch(deg, 4), velocity_base - 20)
                note_count += 1
                
            # 3. Arpeggiated Melody layer
            # Apply the "Rule of 3" variation on the second half of the 3rd phrase
            is_variation = is_phrase_B and (idx >= chords_per_phrase / 2)
            num_8th_notes = int(beats_per_chord * 2)
            
            for i in range(num_8th_notes):
                note_start = chord_start_sec + i * 0.5 * beat_len_sec
                note_end = note_start + 0.4 * beat_len_sec
                
                if not is_variation:
                    # Expectation: Static, predictable looping arp
                    note_idx = i % len(chord_degrees)
                    pitch = get_pitch(chord_degrees[note_idx], 5)
                    vel = velocity_base if i % 2 == 0 else velocity_base - 15
                else:
                    # Variation: Subvert expectation by climbing octaves and crescendoing 
                    scale_len = len(scale_intervals)
                    octave_bump = i // len(chord_degrees)
                    deg = chord_degrees[i % len(chord_degrees)] + (octave_bump * scale_len)
                    pitch = get_pitch(deg, 5)
                    vel = velocity_base + (i * 2) # Crescendo effect
                
                insert_note(note_start, note_end, pitch, vel)
                note_count += 1

    # Cleanup and sort MIDI events
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {note_count} notes demonstrating the Rule of 3 (A-A-B variation) over {total_bars} bars at {bpm} BPM."
