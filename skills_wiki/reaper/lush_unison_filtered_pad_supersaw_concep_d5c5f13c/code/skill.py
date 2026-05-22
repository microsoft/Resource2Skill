def create_pattern(
    project_name: str = "Vital_Pad_Concept",
    track_name: str = "Lush Unison Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a lush, wide, modulated synth pad demonstrating Unison, Filtering, 
    and Spatial FX concepts, driven by a 4-bar extended chord progression.
    """
    import reaper_python as RPR
    import math

    # === Music Theory & Scales ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Use minor by default if unsupported scale is provided
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 48 # Start around C3

    def get_scale_degree_pitch(degree, root, intervals):
        """Returns the MIDI pitch for a given scale degree (0-indexed)."""
        octave = degree // 7
        scale_idx = degree % 7
        return root + (octave * 12) + intervals[scale_idx]

    # Chord Progression: i9 -> VImaj7 -> IIImaj7 -> v7
    # Expressed as scale degrees (0-indexed: 0=i, 5=VI, 2=III, 4=v)
    progression = [
        [0, 2, 4, 6, 8], # Root, 3rd, 5th, 7th, 9th (i9)
        [5, 7, 9, 11],   # (VImaj7)
        [2, 4, 6, 8],    # (IIImaj7)
        [4, 6, 8, 10]    # (v7)
    ]

    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert Chords
    for i, chord_degrees in enumerate(progression):
        start_time = i * bar_length_sec
        # Overlap notes slightly for lush ADSR release tails
        end_time = start_time + bar_length_sec + 0.5 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for idx, degree in enumerate(chord_degrees):
            pitch = get_scale_degree_pitch(degree, root_pitch, scale_intervals)
            
            # Spread voicings: drop the root down an octave, keep extensions high
            if idx == 0:
                pitch -= 12
                vel = velocity_base + 10 # Bass slightly harder
            else:
                vel = velocity_base - (idx * 5) # Softer as we go up
            
            # Ensure pitch is in valid MIDI range
            pitch = max(0, min(127, pitch))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (FX Chain) ===
    
    # 1. ReaSynth (Raw Sawtooth Wave + Slow Envelope)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.3)  # Attack (Slow for pad)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.8)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.6)  # Release (Long tail)
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 1.0)  # Sawtooth mix max
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.0)  # Square mix zero
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.5)  # Volume
    
    # 2. Chorus (Simulating Vital's Stereo Unison / Detune Spread)
    fx_chorus = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_chorus, 0, 4.0)   # Chorus length
    RPR.RPR_TrackFX_SetParam(track, fx_chorus, 1, 2.5)   # Number of voices
    RPR.RPR_TrackFX_SetParam(track, fx_chorus, 2, 0.8)   # Rate (Hz)
    RPR.RPR_TrackFX_SetParam(track, fx_chorus, 3, 0.5)   # Pitch Detune
    RPR.RPR_TrackFX_SetParam(track, fx_chorus, 4, -0.5)  # Stereo Phase
    
    # 3. ReaEQ (Lowpass Filter to tame harsh saw highs)
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 is usually a lowpass in default ReaEQ
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 9, 800.0) # Freq cut around 800Hz
    
    # 4. ReaDelay (Space)
    fx_delay = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 0, 0.0)   # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 13, -6.0) # Wet
    
    # 5. ReaVerbate (Lush Reverb)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.3)  # Wet
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.8)  # Dry
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.9)  # Room size (Huge)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 3, 0.5)  # Dampening

    # === Step 5: LFO Modulation (Automation) ===
    # Automate Track Volume to simulate an LFO opening and closing
    env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if not env:
        # Fallback to activating the envelope if not visible
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_VENV", 1) 
        env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    
    if env:
        lfo_rate_sec = (60.0 / bpm) # 1/4 note pulse
        points = int(item_length / (lfo_rate_sec / 2))
        
        for p in range(points):
            time_pos = p * (lfo_rate_sec / 2)
            # Sine wave simulation for LFO: oscillate volume between 50% and 100%
            val = 700 + (300 * math.sin(p * math.pi)) 
            # Convert to REAPER's volume scaling (roughly 0.0 to 1.0 for standard fader, up to 2.0)
            vol_val = val / 1000.0
            # Insert point: env, time, value, shape (0=linear, 1=square, 2=slow start/end), tension, selected, noSort
            RPR.RPR_InsertEnvelopePoint(env, time_pos, vol_val, 2, 0.0, False, True)
            
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' pad concept with Unison, Filter, LFO modulation, and lush extended chords in {key} {scale} at {bpm} BPM."
