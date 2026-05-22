def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass Foundation",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates a humanized, syncopated slap bassline with octave jumps and scalar walk-ups.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard notes (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Lookups ===
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

    # Input validation
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Base octave for bass (usually octave 2 = MIDI notes 36-47)
    bass_octave_base = 36 
    
    def get_pitch(degree: int) -> int:
        """Calculate MIDI pitch based on scale degree (0 = root)"""
        scale_len = len(scale_intervals)
        oct_offset = degree // scale_len
        idx = degree % scale_len
        return bass_octave_base + root_pitch + scale_intervals[idx] + (oct_offset * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain for Bass Tone ===
    # ReaSynth for tone, ReaEQ to trim mud/harshness, ReaComp for punch
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # (Optional) Basic FX shaping could be done here via SetParam, 
    # but stock defaults with ReaSynth provide a usable starting sine/square tone.

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Define Groove Pattern ===
    # A 1-bar looping pattern representing the tutorial's rhythm
    # Dictionary maps beat position to (Scale Degree, Length in Beats, Velocity Offset)
    groove_pattern = [
        # Beat 0: Strong downbeat root
        {"beat": 0.0, "degree": 0,  "length": 0.5,   "vel_mod": 5},
        
        # Beat 1.5 (Syncopated upbeat): Octave Slap, very short, maximum velocity
        {"beat": 1.5, "degree": 7,  "length": 0.125, "vel_mod": 25}, 
        
        # Beat 2.0: Root again, standard length, slightly softer
        {"beat": 2.0, "degree": 0,  "length": 0.5,   "vel_mod": -5},
        
        # Beat 3.0: Walk-up step 1 (Scale degree -2 = 6th/7th below root), ghost note velocity
        {"beat": 3.0, "degree": -2, "length": 0.25,  "vel_mod": -25},
        
        # Beat 3.5: Walk-up step 2 (Scale degree -1 = 7th/lead tone), medium velocity leading into next bar
        {"beat": 3.5, "degree": -1, "length": 0.25,  "vel_mod": -15},
    ]

    # === Step 6: Insert Humanized MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        for note in groove_pattern:
            # 1. Pitch calculation
            pitch = get_pitch(note["degree"])
            
            # 2. Humanize timing (+/- 0.015 beats ~ 5-10ms)
            human_offset_beats = random.uniform(-0.015, 0.015)
            start_beat = bar_start_beat + note["beat"] + human_offset_beats
            end_beat = start_beat + note["length"]
            
            # Translate beats to project time
            start_proj_time = start_beat * sec_per_beat
            end_proj_time = end_beat * sec_per_beat
            
            # Ensure we don't place notes before 0.0
            if start_proj_time < 0:
                start_proj_time = 0.0
                
            # Translate project time to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_proj_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_proj_time)
            
            # 3. Humanize velocity
            base_v = velocity_base + note["vel_mod"]
            vel = int(base_v + random.uniform(-6, 6))
            vel = max(1, min(127, vel)) # Clamp 1-127
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
