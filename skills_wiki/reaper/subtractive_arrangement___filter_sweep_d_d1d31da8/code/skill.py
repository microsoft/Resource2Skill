def create_pattern(
    project_name: str = "ArrangementTutorial",
    track_name_prefix: str = "Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Locked to 8 to demonstrate Verse (4 bars) -> Chorus (4 bars)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a subtractive arrangement transition (Verse to Chorus) with a Filter Sweep drop.
    """
    import reaper_python as RPR
    import math

    # Theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    # Validate/Force parameters for this specific technique
    bars = 8 # Force 8 bars to show the 4-bar verse into 4-bar chorus transition
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_pitch = NOTE_MAP.get(key, 0) + 48  # C3

    # Timings
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4
    total_len = bar_len * bars

    # === Helper Functions ===
    def insert_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    def create_midi_item(track, length):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    def get_scale_pitch(degree, octave_offset=0):
        octaves = degree // 7
        scale_degree = degree % 7
        return root_pitch + (octaves + octave_offset) * 12 + scale_intervals[scale_degree]

    # === TRACK 1: Subtractive Drums ===
    drum_track = insert_track(f"{track_name_prefix} - Drums")
    drum_item, drum_take = create_midi_item(drum_track, total_len)

    # Insert drum pattern (1/8 hats, 2/4 snares, kicks only in bars 5-8)
    for b in range(bars):
        bar_start = b * bar_len
        
        # Hi-Hats (every 1/8 note)
        for i in range(8):
            pos = bar_start + (i * beat_len * 0.5)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                  pos, pos + (beat_len * 0.25), 
                                  1, 42, velocity_base - 20, False)
        
        # Snare (beats 2 and 4)
        for beat in [1, 3]:
            pos = bar_start + (beat * beat_len)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                  pos, pos + (beat_len * 0.5), 
                                  1, 38, velocity_base, False)
        
        # Kick (Subtractive arrangement: Kicks ONLY play in Chorus, Bars 5-8)
        if b >= 4:  # 0-indexed, so 4 is the 5th bar
            kick_beats = [0, 1.5, 2.5] # syncopated trap/pop kick rhythm
            for beat in kick_beats:
                pos = bar_start + (beat * beat_len)
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, 
                                      pos, pos + (beat_len * 0.5), 
                                      1, 36, velocity_base + 10, False)
                
    RPR.RPR_MIDI_Sort(drum_take)

    # === TRACK 2: Instrument & Filter Sweep Drop ===
    inst_track = insert_track(f"{track_name_prefix} - Chords")
    RPR.RPR_SetMediaTrackInfo_Value(inst_track, "D_VOL", 0.4) # lower volume so synth isn't harsh
    inst_item, inst_take = create_midi_item(inst_track, total_len)

    # Add 4-bar chord progression (i - VI - III - VII) repeated twice
    chord_progression_degrees = [
        [0, 2, 4],     # i
        [5, 0, 2],     # VI (inverted)
        [2, 4, 6],     # III
        [4, 6, 1]      # VII
    ]

    for b in range(bars):
        bar_start = b * bar_len
        chord_idx = b % 4
        chord_notes = chord_progression_degrees[chord_idx]
        
        for degree in chord_notes:
            pitch = get_scale_pitch(degree, 0)
            RPR.RPR_MIDI_InsertNote(inst_take, False, False,
                                  bar_start, bar_start + bar_len - 0.05,
                                  1, pitch, velocity_base - 10, False)
            
    RPR.RPR_MIDI_Sort(inst_take)

    # Add Instruments & FX
    RPR.RPR_TrackFX_AddByName(inst_track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(inst_track, "ReaEQ", False, -1)
    
    # Configure ReaEQ to act as a lowpass on Band 4
    # Param 10 is Band 4 Gain. We set it to 0.0 (roughly -inf) to cut all highs above the frequency
    RPR.RPR_TrackFX_SetParam(inst_track, eq_idx, 10, 0.0) 
    
    # Get Envelope for Band 4 Frequency (Param 9)
    env = RPR.RPR_GetFXEnvelope(inst_track, eq_idx, 9, True)
    
    # Create the Tension Sweep and Drop automation!
    # Shape 0 = Linear transition
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0, False, True) # Start completely open
    
    sweep_start_time = bar_len * 2.5 # Start sweeping halfway through bar 3
    sweep_end_time = bar_len * 4.0 - 0.05 # Reaches lowest point right before the drop
    drop_time = bar_len * 4.0 # Instant snap back open at Bar 5
    
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, sweep_end_time, 0.25, 0, 0, False, True) # Muffled/Filtered down
    RPR.RPR_InsertEnvelopePoint(env, drop_time, 1.0, 0, 0, False, True) # DROP! fully open
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created subtractive arrangement over {bars} bars. Verse (Bars 1-4) omits kick and features a lowpass filter riser, resolving instantly at the Chorus drop (Bar 5)."
