def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Modern Metal Bass Programming' pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc. - though this pattern heavily relies on the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for standard chugs (accents will be louder).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length_sec = sec_per_beat * beats_per_bar * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # Calculate root note in MIDI. 
    # Metal bass typically sits very low. We use Octave 1 (MIDI 24 for C1).
    root_midi = 24 + NOTE_MAP.get(key, 0)
    
    # Velocity mapping: 
    # Accents trigger hard picking layers, base velocity triggers slightly softer chugs to avoid harshness.
    accent_vel = min(127, velocity_base + 17)
    chug_vel = min(127, velocity_base)

    # Define a syncopated 1-bar metal riff.
    # Format: (beat_start, length_in_beats, pitch_offset, velocity)
    pattern = [
        # Beat 1: Aggressive downbeat, followed by tight chugs
        (0.00, 0.25,  0, accent_vel),
        (0.25, 0.25,  0, chug_vel),
        (0.50, 0.25,  0, chug_vel),
        # Upbeat octave jump
        (0.75, 0.25, 12, accent_vel), 

        # Beat 2: Slower chugging
        (1.00, 0.50,  0, chug_vel),
        (1.50, 0.25,  0, chug_vel),
        (1.75, 0.25,  0, chug_vel),

        # Beat 3: Sustained heavy accent (letting the note ring out)
        (2.00, 1.00,  0, accent_vel),

        # Beat 4: Sustained octave accent leading back into tight chugs
        (3.00, 0.50, 12, accent_vel),
        (3.50, 0.25,  0, chug_vel),
        (3.75, 0.25,  0, chug_vel),
    ]

    total_notes = 0
    # Loop the pattern over the requested number of bars
    for bar in range(bars):
        bar_start_sec = bar * beats_per_bar * sec_per_beat
        for note in pattern:
            beat_start, beat_len, pitch_offset, vel = note
            
            start_sec = bar_start_sec + (beat_start * sec_per_beat)
            end_sec = start_sec + (beat_len * sec_per_beat)
            
            # Convert project time in seconds to MIDI PPQ (Pulses Per Quarter Note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            pitch = min(127, max(0, root_midi + pitch_offset))
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes += 1
            
    # Sort the MIDI data to finalize event timings
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a stock synth to act as the bass guitar
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a slightly thicker low end
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.6) # Volume to prevent clipping
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0) # Tuning (0 semitones)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.3) # Attack 
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.5) # Decay
    
    # Add native JS Distortion to give it the necessary metal "clank" and aggression
    dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
    if dist_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 1.5) # Gain (Drive)
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 2, 0.8) # Hardness
        
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM."
