def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 115,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a Syncopated Slap Bassline Pattern with humanized timing and velocity.
    """
    import reaper_python as RPR
    import random

    # === Music Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate base MIDI pitch in the standard bass range (E1 - Eb2)
    base_octave = 24 # C1
    root_pitch = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 4) + base_octave
    if root_pitch < 28: # If lower than E1, push it up an octave to avoid extreme sub muddiness
        root_pitch += 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure ReaSynth for "Pluck/Slap" Articulation ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Param Indices: 0:Vol, 1:Tune, 2:Porta, 3:Square Mix, 4:Saw Mix, 7:Attack, 8:Decay, 9:Sustain, 10:Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)    # 0% Square
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 1.0)    # 100% Saw (bright harmonics for slap)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.0)    # Fast Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.06)   # Quick Decay for pluck feel
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.15)   # Low Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.05)  # Fast Release

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Define Groove Pattern ===
    # Format: (beat_position, pitch_offset, duration_beats, velocity_offset)
    # The pattern spans 2 bars (8 beats) to allow for a walk-up at the end of the phrase
    slap_pattern = [
        # --- Bar 1 ---
        (0.00,  0,  0.250,   0),  # Downbeat root
        (0.75,  0,  0.250, -10),  # Anticipation root (syncopated 16th)
        (1.25, 12,  0.100,  30),  # SLAP! (Octave, short duration, max velocity)
        (1.75, 12,  0.100,  25),  # SLAP!
        (2.50,  0,  0.250,   0),  # Root anchor
        (3.50,  5,  0.250, -10),  # Walk up (Perfect 4th)
        (3.75,  7,  0.250,  -5),  # Walk up (Perfect 5th)
        
        # --- Bar 2 ---
        (4.00,  0,  0.250,   5),  # Downbeat root
        (4.75, 12,  0.100,  30),  # SLAP!
        (5.50,  0,  0.250,  -5),  # Root anchor
        (6.25, 12,  0.100,  25),  # SLAP!
        (6.75,  7,  0.250,  -5),  # Anchor on the 5th
        (7.50, 10,  0.250,   0),  # Minor 7th passing note
        (7.75, 12,  0.100,  30)   # SLAP walk-up into next downbeat
    ]

    # === Step 6: Generate Humanized MIDI Data ===
    notes_created = 0
    
    for bar_pair in range(0, bars, 2):
        base_beat = bar_pair * beats_per_bar
        
        for beat_pos, p_offset, dur, v_offset in slap_pattern:
            if base_beat + beat_pos >= bars * beats_per_bar:
                continue # Stop if we exceed the requested number of bars
                
            # Apply Humanization (Timing and Velocity)
            time_shift = random.uniform(-0.015, 0.025) # Slight push/pull on the grid
            vel_shift = random.randint(-6, 6)
            
            start_beat = base_beat + beat_pos + time_shift
            end_beat = start_beat + dur
            
            # Ensure velocity stays within MIDI bounds
            final_vel = int(max(1, min(127, velocity_base + v_offset + vel_shift)))
            final_pitch = int(root_pitch + p_offset)
            
            # Convert beats to time, then to PPQ (Pulses Per Quarter Note)
            start_time = start_beat * (60.0 / bpm)
            end_time = end_beat * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Failsafe for extremely short notes after humanization
            if end_ppq <= start_ppq:
                end_ppq = start_ppq + 15
                
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, final_pitch, final_vel, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized groove notes over {bars} bars at {bpm} BPM."
