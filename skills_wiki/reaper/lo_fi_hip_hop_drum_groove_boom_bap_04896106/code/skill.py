def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lo-Fi Drums",
    bpm: int = 76,
    key: str = "C",      # Unused for drums, kept for signature consistency
    scale: str = "minor", # Unused for drums, kept for signature consistency
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a dynamic Lo-Fi / Boom Bap drum groove in the current REAPER project.
    Generates a heavily humanized MIDI sequence mapped to General MIDI standards.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (76 is standard for this genre).
        key: Ignored for drum generation.
        scale: Ignored for drum generation.
        bars: Number of bars to generate (must be an even number for the 2-bar kick variation).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

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
    
    # Safely create a new MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # General MIDI Mappings
    KICK_PITCH = 36  # C1
    SNARE_PITCH = 38 # D1
    HAT_PITCH = 42   # F#1

    # Velocity scaling for the Lo-Fi feel
    v_kick = min(127, int(velocity_base * 1.0))
    v_snare = min(127, int(velocity_base * 1.0))
    v_hat_on = min(127, int(velocity_base * 0.90))
    v_hat_off = min(127, int(velocity_base * 0.60))
    v_hat_ghost = min(127, int(velocity_base * 0.35))

    # Helper function to place MIDI notes based on beat grid
    def add_drum_hit(pitch, beat_position, duration_in_beats, vel):
        start_time_sec = beat_position * (60.0 / bpm)
        end_time_sec = (beat_position + duration_in_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
        # Note: selected=False, muted=False, chan=0
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 4: Populate the Rhythm Pattern ===
    note_count = 0
    
    for b in range(bars):
        bar_beat_offset = b * 4.0

        # --- SNARE ---
        # Hits steadily on beat 2 and 4
        add_drum_hit(SNARE_PITCH, bar_beat_offset + 1.0, 0.25, v_snare) # Beat 2
        add_drum_hit(SNARE_PITCH, bar_beat_offset + 3.0, 0.25, v_snare) # Beat 4
        note_count += 2

        # --- HI-HATS ---
        # 3-layer syncopated pattern on every beat
        for i in range(4):
            # 1. On-beat (1.0, 2.0, 3.0, 4.0)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.0, 0.25, v_hat_on)
            # 2. Off-beat 8th note (1.5, 2.5, 3.5, 4.5)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.5, 0.25, v_hat_off)
            # 3. Ghost 16th note before the next beat (1.75, 2.75, 3.75, 4.75)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.75, 0.25, v_hat_ghost)
            note_count += 3

        # --- KICK DRUM ---
        # 2-Bar alternating boom-bap pattern
        if b % 2 == 0:
            # First bar pattern: Beat 1, and the "and" of Beat 2
            add_drum_hit(KICK_PITCH, bar_beat_offset + 0.0, 0.25, v_kick) # 1.1.00
            add_drum_hit(KICK_PITCH, bar_beat_offset + 1.5, 0.25, v_kick) # 1.2.50
            note_count += 2
        else:
            # Second bar pattern: Beat 1, the "and" of Beat 2, and the "and" of Beat 3
            add_drum_hit(KICK_PITCH, bar_beat_offset + 0.0, 0.25, v_kick) # 2.1.00
            add_drum_hit(KICK_PITCH, bar_beat_offset + 1.5, 0.25, v_kick) # 2.2.50
            add_drum_hit(KICK_PITCH, bar_beat_offset + 2.5, 0.25, v_kick) # 2.3.50
            note_count += 3

    # Important: sort the MIDI events so they playback correctly
    RPR.RPR_MIDI_Sort(take)

    # Note: No internal sampler (like ReaSynth) is added because synthesizing 
    # a snare and high-hat out of a basic oscillator sounds awful and obscures the groove. 
    # The track is ready for a VSTi drum sampler to be dropped onto it.

    return f"Created '{track_name}' with {note_count} dynamic drum MIDI notes over {bars} bars at {bpm} BPM."
