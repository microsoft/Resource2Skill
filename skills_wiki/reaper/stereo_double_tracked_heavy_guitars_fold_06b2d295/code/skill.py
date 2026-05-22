def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Heavy Guitars",
    bpm: int = 170,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create Stereo Double-Tracked Heavy Guitars via Folder Routing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (ignored here, riff explicitly uses Phrygian/Blues intervals).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    # C2 as the base chug octave for metal
    root_pitch = NOTE_MAP.get(key, 0) + 36 

    # === Step 2: Create Folder Structure ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Parent Track (Amp Sim Bus)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    parent_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name + " Bus", True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1.0)
    
    # Child Take 1 (Hard Left)
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    child_l = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(child_l, "P_NAME", track_name + " L", True)
    RPR.RPR_SetMediaTrackInfo_Value(child_l, "I_FOLDERDEPTH", 0.0)
    RPR.RPR_SetMediaTrackInfo_Value(child_l, "D_PAN", -1.0) 
    
    # Child Take 2 (Hard Right)
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    child_r = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(child_r, "P_NAME", track_name + " R", True)
    RPR.RPR_SetMediaTrackInfo_Value(child_r, "I_FOLDERDEPTH", -1.0) # Closes the folder
    RPR.RPR_SetMediaTrackInfo_Value(child_r, "D_PAN", 1.0) 

    # === Step 3: Add FX Chains ===
    # Add Amp Sim placeholders to the Parent Track
    RPR.RPR_TrackFX_AddByName(parent_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaEQ", False, -1)
    
    # Add raw tone generators to the Child Tracks to simulate raw guitar DI
    for child in [child_l, child_r]:
        synth_idx = RPR.RPR_TrackFX_AddByName(child, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 0, 0.15) # Volume
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 2, 0.6)  # Add Square mix for grit
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 3, 0.8)  # Add Saw mix for brightness

    # === Step 4: Create MIDI Riff Pattern ===
    # Tuple format: (start_beat, length_beats, pitch_offset_from_root, is_power_chord)
    pattern = [
        (0.0, 0.25, 0, False), # 16th note palm mute
        (0.25, 0.25, 0, False),
        (0.5, 0.5, 3, True),   # 8th note minor 3rd power chord
        (1.0, 0.25, 0, False),
        (1.25, 0.25, 0, False),
        (1.5, 0.5, 5, True),   # 8th note Perfect 4th power chord
        (2.0, 0.25, 0, False),
        (2.25, 0.25, 0, False),
        (2.5, 0.5, 6, True),   # 8th note Diminished 5th power chord (Tritone)
        (3.0, 0.5, 0, False),  # 8th note palm mute
        (3.5, 0.5, 5, True),   # 8th note Perfect 4th power chord
    ]
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    def create_take_for_track(track, is_right_track):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for bar in range(bars):
            bar_offset = bar * beats_per_bar
            for p in pattern:
                start_beat, length_beats, pitch_offset, is_power_chord = p
                
                # Calculate absolute time in seconds
                start_time = (bar_offset + start_beat) * (60.0 / bpm)
                end_time = start_time + (length_beats * (60.0 / bpm))
                
                # The "Double Track" Magic: Humanize timing for the Right track 
                # This creates the stereo width (Haas effect) when panned
                if is_right_track:
                    start_time += random.uniform(0.005, 0.025)
                    end_time += random.uniform(0.005, 0.025)
                
                # Convert project time to MIDI PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Dynamic Velocity humanization
                vel = velocity_base if not is_power_chord else min(127, velocity_base + 20)
                if is_right_track:
                    vel = max(1, min(127, vel + random.randint(-12, 12)))
                else:
                    vel = max(1, min(127, vel + random.randint(-4, 4)))
                    
                base_note = root_pitch + pitch_offset
                notes_to_add = [base_note]
                
                if is_power_chord:
                    notes_to_add.append(base_note + 7) # Add Perfect 5th interval
                    
                for note in notes_to_add:
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note), int(vel), False)
                    
        RPR.RPR_MIDI_Sort(take)

    # Generate both "takes"
    create_take_for_track(child_l, False)
    create_take_for_track(child_r, True)

    return f"Created '{track_name} Bus' folder with hard-panned L/R simulated double-tracked guitars over {bars} bars at {bpm} BPM."
