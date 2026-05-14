def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arpeggiator",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    chord_progression: list = [1, 6, 4, 5],
    arp_style: str = "random",  # Options: "up", "down", "updown", "random"
    grid_division: int = 16,    # 16 = 1/16th notes, 8 = 1/8th notes
    **kwargs,
) -> str:
    """
    Create an Algorithmic Chord Arpeggio in the current REAPER project.
    Generates diatonic 7th chords based on the progression and arpeggiates them.
    """
    import random
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
    }

    # === Step 1: Initialization & Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Start around C3
    scale_intervals = SCALES.get(scale, SCALES["major"])

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper: Build Diatonic 7th Chord
    def get_diatonic_chord(degree):
        chord_notes = []
        for offset in [0, 2, 4, 6]: # 1st, 3rd, 5th, 7th
            scale_index = (degree - 1) + offset
            octave_shift = scale_index // len(scale_intervals)
            note_in_scale = scale_index % len(scale_intervals)
            pitch = root_midi + scale_intervals[note_in_scale] + (octave_shift * 12)
            chord_notes.append(pitch)
        return chord_notes

    # === Step 3: Arpeggiator Algorithm ===
    steps_per_bar = grid_division # e.g., 16 for 1/16th notes in 4/4
    step_len_sec = bar_length_sec / steps_per_bar
    total_notes_created = 0

    for bar in range(bars):
        # Get the chord for this bar
        degree = chord_progression[bar % len(chord_progression)]
        pitches = get_diatonic_chord(degree)
        
        for step in range(steps_per_bar):
            # Select pitch based on arp style
            if arp_style == "up":
                pitch = pitches[step % len(pitches)]
            elif arp_style == "down":
                pitch = pitches[-(step % len(pitches)) - 1]
            elif arp_style == "updown":
                cycle = list(range(len(pitches))) + list(range(len(pitches)-2, 0, -1))
                pitch = pitches[cycle[step % len(cycle)]]
            elif arp_style == "random":
                pitch = random.choice(pitches)
            else:
                pitch = pitches[0] # Fallback
                
            # Calculate timing
            note_start_time = (bar * bar_length_sec) + (step * step_len_sec)
            note_end_time = note_start_time + (step_len_sec * 0.8) # 80% gate for staccato feel
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
            
            # Humanize velocity slightly
            vel = velocity_base + random.randint(-12, 12)
            vel = max(1, min(127, vel))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (Plucky Synth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the envelope for a fast arp pluck
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.08)  # Decay (Short)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.0)   # Sustain (None)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.08)  # Release (Short)
    # Mix Saw and Square waves for rich harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.5)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.5)   # Saw mix

    return f"Created '{track_name}' with {total_notes_created} notes over {bars} bars at {bpm} BPM using '{arp_style}' style on a 1/{grid_division} grid."
