def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # A full demonstration requires 12 bars (3x 4-bar phrases)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 12-bar 'Rule of 3' compositional pattern in the current REAPER project.
    It plays a 4-bar idea twice, and varies it on the 3rd repetition.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (loops the 12-bar structure to fit).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add native Synth and Reverb for a piano/pad-like tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    
    # Attenuate volume to avoid clipping from thick polyphonic chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Setup MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Music Theory Data ===
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
    
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)
    
    def get_pitch(degree, octave):
        """Calculates exact MIDI pitch from a diatonic scale degree."""
        oct_shift = degree // scale_len
        scale_deg = degree % scale_len
        return root_val + (octave + 1 + oct_shift) * 12 + scale_intervals[scale_deg]

    def insert_note(pitch, start_time, end_time, vel):
        """Helper to safely insert a MIDI note."""
        pitch = max(0, min(127, int(pitch)))
        vel = max(0, min(127, int(vel)))
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 5: Generate "Rule of 3" Structural Progression ===
    # 0-indexed scale degrees mapping to diatonic chords
    base_progression = [
        0, 4, 5, 3,  # Bars 1-4 (Phrase 1 - The Idea)
        0, 4, 5, 3,  # Bars 5-8 (Phrase 2 - The Exact Repetition)
        0, 4, 1, 4   # Bars 9-12(Phrase 3 - Starts same, turns around to ii-V)
    ]
    
    for bar in range(bars):
        chord_deg = base_progression[bar % 12]
        bar_start = bar * bar_length_sec
        
        # 1. Bass Note (Whole note, Octave 2)
        bass_pitch = get_pitch(chord_deg, 2)
        insert_note(bass_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 10)
        
        # 2. Block Chord Left Hand (Root, 3rd, 5th in Octave 3)
        root_pitch = get_pitch(chord_deg, 3)
        third_pitch = get_pitch(chord_deg + 2, 3)
        fifth_pitch = get_pitch(chord_deg + 4, 3)
        
        if bar % 12 == 11:
            # Bar 12 (Final turnaround variation): 
            # Ditch the arpeggio, play a dramatic held block chord to create tension/resolution 
            insert_note(root_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            insert_note(third_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            insert_note(fifth_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            # Add top melody resolution note
            insert_note(get_pitch(chord_deg + scale_len, 3), bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 10)
            
        else:
            # Regular Bars (1-11): 
            # Play standard LH block chord...
            insert_note(root_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            insert_note(third_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            insert_note(fifth_pitch, bar_start, bar_start + bar_length_sec * 0.95, velocity_base - 15)
            
            # ...and overlay the Right Hand driving 8th-note Arpeggio (3rd, 5th, Octave, 5th)
            eighth_sec = bar_length_sec / 8.0
            arp_degrees = [chord_deg + 2, chord_deg + 4, chord_deg + scale_len, chord_deg + 4]
            
            for i in range(8):
                deg = arp_degrees[i % 4]
                note_pitch = get_pitch(deg, 4)
                note_start = bar_start + i * eighth_sec
                note_end = note_start + eighth_sec * 0.85 # Slight detach/staccato
                
                # Accent the downbeats slightly
                current_vel = velocity_base if i % 2 == 0 else velocity_base - 15
                insert_note(note_pitch, note_start, note_end, current_vel)

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' applying the 'Rule of 3' structure over {bars} bars at {bpm} BPM."
