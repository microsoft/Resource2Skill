def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo Soul Rhodes",
    bpm: int = 85,
    key: str = "D#",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 75,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul Extended Chord Progression in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (80-95 recommended for Neo-Soul).
        key: Root note (e.g., "D#", "Eb", "C").
        scale: Scale type (defaults to minor for this specific progression).
        bars: Number of bars (generates an 8-bar loop with a sus4 turnaround).
        velocity_base: Base MIDI velocity (kept low for soft Rhodes tone).
        
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Define Harmony & Voicings ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key.upper(), 3) # Default to D#
    base_octave = 48 # C3
    tonic = base_octave + root_val

    # Neo-Soul minor voicings mapped by semitone intervals relative to the tonic
    # i m9 -> ii m7 -> III maj7 -> v m9 (turnaround 1) -> V 9sus4 (turnaround 2)
    chords = [
        [0, 3, 7, 10, 14],          # i m9
        [2, 5, 9, 12],              # ii m7 (borrowed dorian/passing)
        [3, 7, 10, 14],             # bIII maj7
        [7, 10, 14, 17, 21],        # v m9
        [0, 3, 7, 10, 14],          # i m9
        [2, 5, 9, 12],              # ii m7
        [3, 7, 10, 14],             # bIII maj7
        [7, 12, 14, 17, 21]         # V 9sus4 (Neo-Soul turnaround)
    ]

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    PPQ_PER_QUARTER = 960
    PPQ_PER_BAR = PPQ_PER_QUARTER * 4
    
    note_count = 0
    
    # Loop through the progression
    for bar in range(bars):
        chord_idx = bar % len(chords)
        chord_intervals = chords[chord_idx]
        
        # Calculate timing
        start_ppq = int(bar * PPQ_PER_BAR)
        end_ppq = int(start_ppq + PPQ_PER_BAR - 60) # slight gap at end of bar
        
        # Insert notes with humanized "strum" (lower notes slightly earlier)
        for i, interval in enumerate(chord_intervals):
            pitch = tonic + interval
            
            # Keep highest notes in a reasonable melody range (drop down if too high)
            while pitch > 76:
                pitch -= 12
                
            # Strum effect: offset each note start time by a few ticks
            strum_offset = i * 15 
            note_start = start_ppq + strum_offset
            
            # Humanize velocity
            vel = velocity_base + random.randint(-5, 5)
            # Make top note slightly louder for melody emphasis
            if i == len(chord_intervals) - 1:
                vel += 8
                
            RPR.RPR_MIDI_InsertNote(take, False, False, note_start, end_ppq, 0, pitch, vel, True)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Rhodes EP Emulation) ===
    # 1. ReaSynth for base tone (Soft Triangle/Sine mix)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set Triangle wave volume to high, others to 0
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Volume mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.8)   # Triangle mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 1.0)   # Sine mix
    # ADSR Envelope (Soft attack, long decay)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.02)  # Attack 
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.5)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.5)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.3)   # Release

    # 2. JS Tremolo for classic electric piano modulation
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 0, 2.5)    # Frequency (Hz)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 1, -6.0)   # Amount (dB)

    # 3. ReaEQ for Vintage Muffling (Lowpass)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 to Lowpass to cut digital highs
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 1)       # Band 4 Type: Lowpass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 13, 2000)    # Freq: 2kHz
    # Band 2 boost low-mids for warmth
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 5, 250)      # Freq: 250Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 6, 3.0)      # Gain: +3dB

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}"
