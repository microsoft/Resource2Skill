def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SlapBass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Multi-Timbral Humanized Slap Bass Groove in the current REAPER project.
    Creates two tracks (Main and Slap) to handle different articulations, 
    populating them with a syncopated 16th-note groove.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Setup ===
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

    base_note = NOTE_MAP.get(key.upper(), 4) # Default E
    # Shift base to a good bass register (e.g., E1 = 28 or E2 = 40)
    base_midi = base_note + 24 if base_note > 5 else base_note + 36
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(scale_intervals)

    def get_pitch(degree, oct_shift=0):
        """Convert a scale degree (e.g., 0=root, 4=fifth, -1=seventh of lower octave) to MIDI pitch."""
        octaves = degree // scale_len
        rem_degree = degree % scale_len
        return base_midi + scale_intervals[rem_degree] + (octaves * 12) + (oct_shift * 12)

    # === Setup Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Create Tracks ===
    def setup_bass_track(name_suffix, is_slap):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} {name_suffix}", True)
        
        # Add stock synth
        synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        if is_slap:
            # Slap Bass: Brighter, square wave mix, fast decay
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.6)   # Vol
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Attack (fast)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.15)  # Decay (fast)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)   # Sustain (none)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.1)   # Release (fast)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.5)   # Square mix (bite)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.2)   # Saw mix
        else:
            # Main Bass: Warm, round, slightly filtered
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.8)   # Vol
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.02)  # Attack (slightly softer)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4)   # Decay (longer)
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.3)   # Sustain
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.2)   # Release
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0)   # Square mix
            RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.2)   # Saw mix
            
        return track

    track_main = setup_bass_track("Main", is_slap=False)
    track_slap = setup_bass_track("Slap", is_slap=True)

    # === Create Media Items & Takes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    def create_take_on_track(track):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        return RPR.RPR_AddTakeToMediaItem(item)

    take_main = create_take_on_track(track_main)
    take_slap = create_take_on_track(track_slap)

    # === Generate Pattern ===
    sixteenth_sec = (60.0 / bpm) / 4.0

    # Pattern definition: (16th_step, degree, dur_16ths, is_slap, vel_mod)
    # This emulates the tutorial: roots, octaves(slaps), and passing notes
    groove_pattern = [
        (0,  0, 1.5, False, 1.0),   # 1
        (2,  0, 1.0, False, 0.85),  # 1 &
        (5,  0, 0.8, True,  1.1),   # 2 e (Slap Octave)
        (7,  4, 0.8, False, 0.7),   # 2 a (Ghost Fifth)
        (8,  0, 1.5, False, 0.95),  # 3
        (10, 0, 1.0, False, 0.8),   # 3 &
        (13,-1, 0.8, False, 0.85),  # 4 e (Leading tone, e.g., minor 7th)
        (15, 0, 0.8, True,  1.1),   # 4 a (Slap Octave)
    ]

    notes_created = 0
    
    # Loop over bars
    for bar in range(bars):
        bar_offset = bar * bar_length_sec
        
        # Add slight variation per bar for scale degrees
        alt_pattern = bar % 2 != 0 

        for step, degree, dur, is_slap, vel_mod in groove_pattern:
            
            # Alternative passing note on odd bars for movement
            if alt_pattern and step == 13:
                degree = 4 # jump to fifth instead of 7th
                
            pitch = get_pitch(degree, oct_shift=1 if is_slap else 0)
            
            # Humanization: Timing offset and velocity jitter
            timing_humanize = random.uniform(-0.005, 0.015) 
            vel_humanize = random.randint(-8, 8)
            
            start_pos = bar_offset + (step * sixteenth_sec) + timing_humanize
            # Keep start_pos strictly >= 0
            start_pos = max(0.0, start_pos)
            end_pos = start_pos + (dur * sixteenth_sec * random.uniform(0.9, 1.0))
            
            velocity = int(velocity_base * vel_mod) + vel_humanize
            velocity = max(1, min(127, velocity))

            target_take = take_slap if is_slap else take_main
            
            RPR.RPR_MIDI_InsertNote(
                target_take, False, False,
                RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, start_pos),
                RPR.RPR_MIDI_GetPPQPosFromProjTime(target_take, end_pos),
                0, pitch, velocity, True
            )
            notes_created += 1

    # Sort MIDI items to finalize
    RPR.RPR_MIDI_Sort(take_main)
    RPR.RPR_MIDI_Sort(take_slap)

    return f"Created Multi-Timbral Slap Bass Groove ('{track_name} Main/Slap') with {notes_created} notes over {bars} bars at {bpm} BPM in {key} {scale}."
