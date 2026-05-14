def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Chopped Swell Transition",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 1,
    velocity_base: int = 100,
    chop_rate: int = 32,
    **kwargs,
) -> str:
    """
    Creates a Chopped Synth Swell Transition using overlapping Automation Items.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars for the main swell (tail will extend past this).
        velocity_base: Base MIDI velocity.
        chop_rate: The rhythmic division for the chop (default 32 for 32nd notes).
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # === Step 1: Initialize Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    tail_length = bar_length_sec * 0.5  # Half a bar for the chopped reverb tail

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Synth -> Chorus -> Reverb) ===
    # ReaSynth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 1.0)  # Waveform: Mix of Saw/Square
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5)  # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5)  # Release
    
    # Chorus
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 0, 15.0)  # Chorus depth
    
    # ReaVerbate (for the spatial tail)
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.5)  # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.5)  # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.8)  # Roomsize

    # === Step 4: Create MIDI Item & Chord ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    root = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start at C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Build a lush 9th chord spread voicing (Root, 5th, Octave+3rd, Octave+7th, Octave+9th)
    chord_degrees = [0, 4, 9, 13, 15] # 1st, 5th, 3rd(up), 7th(up), 9th(up)
    
    midi_notes = []
    for deg in chord_degrees:
        octave_offset = (deg // len(scale_intervals)) * 12
        scale_idx = deg % len(scale_intervals)
        pitch = root + octave_offset + scale_intervals[scale_idx]
        midi_notes.append(min(127, pitch))

    for pitch in midi_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, item_length * 960, 0, pitch, velocity_base, False)

    # === Step 5: Automate Volume with Overlapping Automation Items ===
    
    # Select track to guarantee action applies correctly
    RPR.RPR_SetOnlyTrackSelected(track)
    # Action 40406: Track: Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40406, 0)
    env_vol = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    # 5a. Automation Item 1: The Macro Swell
    ai_swell = RPR.RPR_InsertAutomationItem(env_vol, -1, 0.0, item_length)
    # Clear any default points in the AI
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_swell, "D_LFO_SHAPE", 0, True) # No LFO
    RPR.RPR_InsertEnvelopePointEx(env_vol, ai_swell, 0.0, 0.0, 0, 0, 0, True) # Start at -inf (0.0 amp)
    RPR.RPR_InsertEnvelopePointEx(env_vol, ai_swell, item_length, 1.0, 0, 0, 0, True) # Swell to 0dB (1.0 amp)
    RPR.RPR_Envelope_SortPointsEx(env_vol, ai_swell)

    # 5b. Automation Item 2: The Micro Rhythmic Chop (extends into the tail)
    # 1 beat = 1/4 note. LFO Period needs to be length of one chop_rate note in seconds.
    chop_period_sec = (60.0 / bpm) * (4.0 / chop_rate) 
    
    ai_chop = RPR.RPR_InsertAutomationItem(env_vol, -1, 0.0, item_length + tail_length)
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_chop, "D_UISEL", 1, True)
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_chop, "D_LFO_SHAPE", 1, True) # 1 = Square wave
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_chop, "D_LFO_PERIOD", chop_period_sec, True)
    
    # Unipolar negative LFO math: 
    # With Baseline = -0.5 and Amp = 0.5, a square wave swings from (-0.5 + 0.5) to (-0.5 - 0.5)
    # i.e., from 0.0 to -1.0. When summed with Swell, it perfectly gates it!
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_chop, "D_BASELINE", -0.5, True)
    RPR.RPR_GetSetAutomationItemInfo(env_vol, ai_chop, "D_AMPLITUDE", 0.5, True)

    return f"Created '{track_name}' with {len(midi_notes)}-note chord, swelled and chopped at 1/{chop_rate} notes over {bars} bars + tail at {bpm} BPM."
