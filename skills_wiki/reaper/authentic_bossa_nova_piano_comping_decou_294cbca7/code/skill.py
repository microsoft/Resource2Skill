def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bossa_Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create an Authentic Bossa Nova Piano Groove in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (should be even to fit the 2-bar phrase).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # --- Music Theory Lookup Tables ---
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

    # Helper to calculate extended scale degrees (e.g., 9ths, 11ths)
    def get_degree(deg, arr):
        octave_shift = deg // len(arr)
        idx = deg % len(arr)
        return arr[idx] + (12 * octave_shift)

    # --- Project & Track Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # --- MIDI Item Setup ---
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length = bars * beats_per_bar * sec_per_beat
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # --- Pitch Calculation ---
    base_note = 60 + NOTE_MAP.get(key, 0) # Middle C octave
    scale_arr = SCALES.get(scale, SCALES["minor"])
    
    # Bass left hand (Root and 5th, 2 octaves down)
    bass_root = base_note - 24 + get_degree(0, scale_arr)
    bass_5th  = base_note - 24 + get_degree(4, scale_arr)
    
    # Right hand jazz voicing (3rd, 5th, 7th, 9th)
    chord_pitches = [
        base_note + get_degree(2, scale_arr),
        base_note + get_degree(4, scale_arr),
        base_note + get_degree(6, scale_arr),
        base_note + get_degree(8, scale_arr)
    ]

    # --- Rhythm Arrays (Beat relative to bar start, Duration) ---
    bass_rhythm = [
        (0.0, 1.8),  # Beat 1
        (2.0, 1.8)   # Beat 3
    ]
    # Standard 2-bar Bossa syncopation (Clave)
    chord_rhythm_even = [
        (0.0, 1.0),  # Downbeat 1
        (1.5, 1.0),  # Upbeat 2
        (3.0, 1.0)   # Downbeat 4
    ]
    chord_rhythm_odd = [
        (0.5, 1.0),  # Upbeat 1
        (2.0, 1.0),  # Downbeat 3
        (3.5, 1.0)   # Upbeat 4
    ]

    # --- Helper function for inserting notes ---
    def insert_note(start_beat, duration_beats, pitch, velocity):
        start_sec = start_beat * sec_per_beat
        end_sec = (start_beat + duration_beats) * sec_per_beat
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        # Bounds check velocity
        vel = max(1, min(127, int(velocity)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, False)

    # --- Generate MIDI Events ---
    note_count = 0
    for b in range(bars):
        bar_start_beat = b * 4.0
        
        # Insert Bass Notes (Relaxed Half Notes)
        insert_note(bar_start_beat + bass_rhythm[0][0], bass_rhythm[0][1], bass_root, velocity_base - 5)
        insert_note(bar_start_beat + bass_rhythm[1][0], bass_rhythm[1][1], bass_5th, velocity_base - 5)
        note_count += 2
        
        # Insert Syncopated Chords
        active_chord_rhythm = chord_rhythm_even if (b % 2 == 0) else chord_rhythm_odd
        for beat_offset, duration in active_chord_rhythm:
            # Humanize velocity: upbeats (ending in .5) get slight accents
            is_upbeat = (beat_offset % 1.0) != 0.0
            vel = velocity_base + 12 if is_upbeat else velocity_base
            
            for pitch in chord_pitches:
                insert_note(bar_start_beat + beat_offset, duration, pitch, vel)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # --- FX Setup (ReaSynth for Electric Piano Tone) ---
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth to sound somewhat like a warm Rhodes/Wurlitzer
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.1)  # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.4)  # Square mix (warmth)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.01) # Fast attack
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.3)  # Medium decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.2)  # Low sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 7, 0.4)  # Natural release

    return f"Created Bossa Nova groove track '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
