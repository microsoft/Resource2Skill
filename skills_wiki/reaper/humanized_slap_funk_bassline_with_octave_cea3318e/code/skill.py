def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Slap Bass",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a groovy, humanized slap bass pattern with octave jumps and passing notes.
    """
    import reaper_python as RPR
    import random

    # === Music Theory & Scales ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10]
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper(), NOTE_MAP["E"])
    base_octave = 1 # Bass sits in octave 1 or 2 (E1 = MIDI 28)

    def get_midi_pitch(degree: int) -> int:
        """Calculate MIDI pitch for a given scale degree (0-indexed)."""
        octave_shift = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_val + ((base_octave + octave_shift + 1) * 12) + scale_intervals[idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define the Groove Pattern ===
    # Format: (beat_position, scale_degree, duration_in_beats, articulation)
    # Articulations: 'root' (steady), 'slap' (octave jump, staccato, loud), 'pass' (ghost note, quiet)
    
    # We define a 2-bar loop and repeat it
    two_bar_groove = [
        # Bar 1
        (0.0,  0, 0.75,  "root"), # Downbeat root
        (1.5,  7, 0.125, "slap"), # Beat 2 AND: Octave slap
        (2.5,  4, 0.5,   "root"), # Beat 3 AND: Fifth
        (3.75, 6, 0.125, "pass"), # Beat 4 'a': Flat 7th leading into next root
        
        # Bar 2
        (4.0,  0, 0.5,   "root"), # Downbeat root
        (4.75, 0, 0.125, "pass"), # Ghost root
        (5.5,  7, 0.125, "slap"), # Beat 2 AND: Octave slap
        (6.0,  2, 0.25,  "pass"), # Beat 3: Third
        (6.5,  3, 0.25,  "pass"), # Beat 3 AND: Fourth (walking up)
        (7.0,  4, 0.125, "slap"), # Beat 4: Fifth Slap
        (7.5,  7, 0.125, "slap"), # Beat 4 AND: Octave slap
    ]

    # === Step 5: Insert Humanized MIDI Notes ===
    total_notes = 0
    for bar in range(0, bars, 2):
        for beat_pos, degree, length_beats, art in two_bar_groove:
            
            # Stop if we exceed requested bars
            if bar + (beat_pos / 4.0) >= bars:
                break
                
            pitch = get_midi_pitch(degree)
            
            # Articulation processing
            if art == "root":
                vel = velocity_base
            elif art == "slap":
                vel = min(127, velocity_base + 30) # Hard hit for slap
            elif art == "pass":
                vel = max(1, velocity_base - 25)   # Ghost note / softer hit

            # HUMANIZATION: "Imitate reality, slightly offset your notes"
            # +/- up to 10 milliseconds of timing drift
            timing_drift_sec = random.uniform(-0.010, 0.010)
            # Anchor the very first downbeat perfectly
            if beat_pos == 0.0 and bar == 0:
                timing_drift_sec = 0.0
                
            # +/- up to 8 velocity levels of dynamic drift
            humanized_vel = int(max(1, min(127, vel + random.uniform(-8, 8))))

            # Calculate precise times
            base_time = (bar * bar_length_sec / 2) + (beat_pos * 60.0 / bpm)
            start_time = max(0.0, base_time + timing_drift_sec)
            end_time = start_time + (length_beats * 60.0 / bpm)
            
            # Convert to PPQ for REAPER MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, humanized_vel, True)
            total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Sound Design (ReaSynth & EQ) ===
    # Add ReaSynth to fake a bass pluck
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)    # Sawtooth mix (0)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.7)    # Square mix (hollow bass tone)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.15)   # Release (short for staccato feel)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)    # Portamento

    # Add ReaEQ to shape the bass (boost lows, cut mud, slight slap transient boost)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Low Shelf (Boost sub)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0.0)       # Type (Low Shelf)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 80.0)      # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 3.0)       # Gain (dB approx)
    # Band 4: High Shelf (Slap transient)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 3.0)       # Type (High Shelf)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 3500.0)   # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, 4.0)      # Gain (dB approx)

    return f"Created '{track_name}' with {total_notes} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
