def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Hi-Hats",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Expressive Humanized Drum Groove in the current REAPER project.
    Simulates painting 16th notes, selecting odd/even patterns for velocity
    accents, and applying the 'H' humanize shortcut.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused dynamically here, as we map to GM Drums).
        scale: Scale type (unused dynamically here, as we map to GM Drums).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (humanize_amt, drum_note).

    Returns:
        Status string describing the created element.
    """
    import reaper_python as RPR
    import random

    # General MIDI Drum Map (as discussed in the tutorial)
    GM_DRUMS = {
        "Kick": 36,
        "Snare": 38,
        "Closed_Hat": 42,
        "Pedal_Hat": 44,
        "Open_Hat": 46,
        "Crash": 49,
        "Ride": 51
    }
    
    # Allow kwargs to override target drum, default to Closed Hat
    drum_note = kwargs.get("drum_note", GM_DRUMS["Closed_Hat"])
    humanize_amt = kwargs.get("humanize_amt", 0.015) # Max seconds to shift timing

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI for the take
    RPR.RPR_MIDI_InsertNote(take, False, False, 0, 10, 0, drum_note, 1, False)
    RPR.RPR_MIDI_DeleteNote(take, 0) # Hack to initialize MIDI data structure

    # === Step 4: Generate Pattern (16th notes) ===
    sixteenth_length_sec = beat_length_sec / 4.0
    notes_created = 0
    
    for bar in range(bars):
        for step in range(16): # 16 sixteenth notes per bar
            
            # --- The "Select Odd/Even Pattern" Velocity Trick ---
            # Replicates dragging mousewheel on specific selected patterns
            if step % 4 == 0:
                # Downbeats (1, 2, 3, 4) - Accent
                vel = velocity_base + 15
            elif step % 4 == 2:
                # Upbeats ("and") - Standard
                vel = velocity_base
            else:
                # Offbeats ("e", "a") - Ghost notes
                vel = velocity_base - 25
                
            # --- The "Humanize ('H')" Trick ---
            # Randomize velocity slightly (+/- 6)
            vel = int(vel + random.uniform(-6, 6))
            vel = max(1, min(127, vel)) # Clamp 1-127
            
            # Calculate rigid grid time
            exact_start_sec = (bar * bar_length_sec) + (step * sixteenth_length_sec)
            exact_end_sec = exact_start_sec + (sixteenth_length_sec * 0.8) # Staccato notes
            
            # Randomize timing slightly
            time_shift = random.uniform(-humanize_amt, humanize_amt)
            start_sec = max(0.0, exact_start_sec + time_shift)
            end_sec = start_sec + (sixteenth_length_sec * 0.8)

            # Convert seconds to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

            # Insert the note
            # Signature: take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, drum_note, vel, False)
            notes_created += 1

    # Sort MIDI data after batch insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (Make it audible) ===
    # Add ReaSynth to simulate a hi-hat/tick since we don't know what VSTs the user has
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    if fx_idx != -1:
        # Parameter mapping for ReaSynth (approximate for a percussive hat)
        # 0: Volume, 1: Tuning, 2: Attack, 3: Decay, 4: Sustain, 5: Release, 6: Square mix, etc.
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)    # Attack: 0ms
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.05)   # Decay: very short
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)    # Sustain: 0%
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.05)   # Release: very short
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.8)    # Pitch: High

    return f"Created '{track_name}' with {notes_created} humanized hi-hat notes over {bars} bars at {bpm} BPM."
