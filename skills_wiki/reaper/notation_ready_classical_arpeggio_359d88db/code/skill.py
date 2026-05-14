def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Notation-Ready Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a strictly quantized, notation-friendly classical arpeggio progression.
    Double-click the generated MIDI item and press Alt+4 to view the clean sheet music.

    Args:
        project_name: Project identifier
        track_name: Name for the created track
        bpm: Tempo in BPM
        key: Root note (C, C#, D, etc.)
        scale: Scale type (major, minor, etc.)
        bars: Number of bars (generates arps, ending on a whole note chord)
        velocity_base: Base MIDI velocity

    Returns:
        Status string
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }

    # === Step 1: Initialize Track and Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Music Theory Logic ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_note(octave, degree):
        """Calculates exact MIDI pitch from a scale degree, allowing negative/overflow degrees for inversions."""
        octave_shift = int(degree // len(scale_intervals))
        safe_degree = int(degree % len(scale_intervals))
        return root_val + (octave + octave_shift + 1) * 12 + scale_intervals[safe_degree]

    # Classical Arpeggio Patterns based on scale degrees (I, IV(inv), V(inv))
    arp_patterns = [
        [0, 2, 4, 7, 4, 2, 0, 2],    # I chord
        [0, 3, 5, 7, 5, 3, 0, 3],    # IV chord (2nd inversion shape)
        [-1, 1, 4, 6, 4, 1, -1, 1]   # V chord (1st inversion shape)
    ]

    # === Step 4: Insert MIDI Notes ===
    ppq = 960  # Default ticks per quarter note
    note_count = 0
    
    for bar in range(bars):
        if bar < bars - 1:
            # 8th note arpeggios
            pattern = arp_patterns[bar % len(arp_patterns)]
            for eighth in range(8):
                start_ppq = int((bar * 4 * ppq) + eighth * (ppq / 2))
                end_ppq = int(start_ppq + (ppq / 2) - 10) # slightly detached for clean notation ties
                pitch = get_note(4, pattern[eighth % len(pattern)])
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                note_count += 1
        else:
            # Final resolving whole note chord (I)
            start_ppq = int(bar * 4 * ppq)
            end_ppq = int(start_ppq + (4 * ppq) - 10)
            for degree in [0, 2, 4]:
                pitch = get_note(4, degree)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(velocity_base * 0.8), False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX (ReaSynth Soft Pad) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.3)  # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5)  # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 1.0)  # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.7)  # Decay

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} quantized notes over {bars} bars at {bpm} BPM. Open in MIDI editor and press Alt+4 for Notation view."
