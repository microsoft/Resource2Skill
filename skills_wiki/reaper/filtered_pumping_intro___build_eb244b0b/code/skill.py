def create_pattern(
    project_name: str = "EDM_Arrangement",
    track_name: str = "Pumping Filtered Build",
    bpm: int = 126,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an EDM Intro/Build sequence featuring sustained chords,
    a 4-on-the-floor simulated sidechain pump, and an opening low-pass filter sweep.
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Default to F minor if missing
    root_val = NOTE_MAP.get(key.capitalize(), 5)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Classic EDM Progression: i - VI - III - VII
    # Represented as scale degrees (0-indexed)
    progression = [0, 5, 2, 6] 

    # --- Step 1: Initialize Project & Track ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Set track color to an "EDM Orange/Red"
    RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", RPR.RPR_ColorToNative(255, 100, 50) | 0x1000000)

    # --- Step 2: Create Media Item & MIDI Take ---
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # --- Step 3: Insert Chords ---
    octave_base = 4
    notes_added = 0
    
    for bar in range(bars):
        # Loop the progression if bars > len(progression)
        degree = progression[bar % len(progression)]
        
        # Build a triad + octave bass
        chord_intervals = [
            degree, 
            (degree + 2) % 7, 
            (degree + 4) % 7
        ]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate literal MIDI notes
        for i, interval in enumerate(chord_intervals):
            octave_shift = (degree + (2*i if i>0 else 0)) // 7
            note_val = root_val + scale_intervals[interval] + ((octave_base + octave_shift) * 12)
            
            # Insert triad notes
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val, velocity_base, False)
            notes_added += 1
            
            # Add a bass note an octave lower for depth
            if i == 0:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val - 12, velocity_base + 10, False)
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # --- Step 4: Sound Design (ReaSynth) ---
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth to Sawtooth for a rich harmonic spectrum
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0) # Saw shape
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.5) # Square shape
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.8) # Release

    # --- Step 5: The "Filter Sweep" Automation ---
    # Add a Lowpass filter
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Lowpass", False, -1)
    # Get the envelope for Param 0 (Frequency) and create it if it doesn't exist
    filter_env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True)
    
    if filter_env:
        # Sweep from 10% (muffled) to 100% (fully open) over the entire duration
        RPR.RPR_InsertEnvelopePoint(filter_env, 0.0, 0.1, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(filter_env, total_length_sec, 1.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(filter_env)

    # --- Step 6: The "Sidechain Pump" Volume Automation ---
    # Show volume envelope
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if vol_env:
        # Loop through every beat (1/4 note) to create a pumping effect
        total_beats = bars * beats_per_bar
        for b in range(total_beats):
            beat_start = b * beat_length_sec
            pump_bottom = beat_start + 0.01
            pump_recover = beat_start + (beat_length_sec * 0.4) # Recovers slightly before next beat
            
            # Amplitude values (Reaper linear volume: 1.0 = 0dB, 0.25 = -12dB, 0.05 = -26dB)
            vol_ducked = 0.05 
            vol_full = 1.0
            
            # Beat Start (dip instantly)
            RPR.RPR_InsertEnvelopePoint(vol_env, beat_start, vol_full, 0, 0.0, False, True)
            RPR.RPR_InsertEnvelopePoint(vol_env, pump_bottom, vol_ducked, 2, 0.0, False, True) # 2 = Slow Start/End shape
            
            # Recover
            RPR.RPR_InsertEnvelopePoint(vol_env, pump_recover, vol_full, 0, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(vol_env)

    return f"Created '{track_name}' with {notes_added} chord notes, fake sidechain pump, and filter sweep over {bars} bars at {bpm} BPM."
