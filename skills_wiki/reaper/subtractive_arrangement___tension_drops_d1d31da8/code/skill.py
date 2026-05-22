def create_subtractive_arrangement(
    project_name: str = "Arrangement_Tutorial",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    total_bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full Chorus-to-Verse arrangement demonstrating Subtractive Arrangement.
    Bars 1-4: Chorus (Full beat, chords, lead melody).
    Bars 5-8: Verse (First kick dropped, lead deleted, hats removed for first half).
    
    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, F#).
        scale: Scale type (major, minor, harmonic_minor).
        total_bars: Must be at least 4 to hear the transition (default 8).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # --- Music Theory & Constants ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Helper to get MIDI pitch from scale degree
    def get_pitch(degree, octave=4):
        deg_idx = degree % len(scale_intervals)
        oct_shift = degree // len(scale_intervals)
        return root_val + scale_intervals[deg_idx] + ((octave + oct_shift) * 12)

    # --- Setup Project ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_len_sec = beat_len_sec * beats_per_bar
    
    chorus_bars = total_bars // 2
    verse_bars = total_bars - chorus_bars

    # Helper: Create track with MIDI item
    def create_track_with_midi(name, bars):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * bar_len_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # --- 1. DRUMS TRACK ---
    # GM Drum Map: Kick=36, Snare=38, Hat=42
    drum_track, drum_take = create_track_with_midi("Drums (Subtractive)", total_bars)
    
    for bar in range(total_bars):
        is_verse = bar >= chorus_bars
        bar_in_section = bar - chorus_bars if is_verse else bar
        bar_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, bar * bar_len_sec)
        beat_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, beat_len_sec) - RPR.RPR_MIDI_GetPPQPosFromProjTime(drum_take, 0)
        
        # KICK DRUM
        kick_rhythms = [0, 2.5] # Beats
        for beat in kick_rhythms:
            # THE "DROP" TECHNIQUE: Delete the first kick of the Verse
            if is_verse and bar_in_section == 0 and beat == 0:
                continue 
                
            start = bar_start_ppq + (beat * beat_ppq)
            end = start + (beat_ppq * 0.25)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start, end, 0, 36, velocity_base, False)
            
        # SNARE DRUM
        for beat in [1, 3]: # Beats 2 and 4 (0-indexed 1 and 3)
            start = bar_start_ppq + (beat * beat_ppq)
            end = start + (beat_ppq * 0.25)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start, end, 0, 38, velocity_base, False)
            
        # HI-HATS
        # TECHNIQUE: Delete hats for the first half of the verse to build contrast
        play_hats = True
        if is_verse and bar_in_section < (verse_bars / 2):
            play_hats = False
            
        if play_hats:
            for eighth in range(8):
                start = bar_start_ppq + (eighth * beat_ppq * 0.5)
                end = start + (beat_ppq * 0.25)
                # Slight velocity humanization
                vel = velocity_base if eighth % 2 == 0 else velocity_base - 20
                RPR.RPR_MIDI_InsertNote(drum_take, False, False, start, end, 0, 42, vel, False)

    # --- 2. CHORDS TRACK ---
    chord_track, chord_take = create_track_with_midi("Chords (Foundation)", total_bars)
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    
    # Simple i - VI progression
    chord_prog = [
        [0, 2, 4], # i
        [5, 7, 9], # VI
    ]
    
    for bar in range(total_bars):
        chord = chord_prog[bar % len(chord_prog)]
        start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, bar * bar_len_sec)
        end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, (bar + 1) * bar_len_sec)
        
        for degree in chord:
            pitch = get_pitch(degree, octave=4)
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start, end, 0, pitch, int(velocity_base*0.7), False)

    # --- 3. LEAD SYNTH TRACK ---
    lead_track, lead_take = create_track_with_midi("Lead (Subtractive)", total_bars)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)
    
    for bar in range(total_bars):
        is_verse = bar >= chorus_bars
        # TECHNIQUE: Delete the lead entirely during the verse to leave room for vocals
        if is_verse:
            continue
            
        bar_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(lead_take, bar * bar_len_sec)
        beat_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(lead_take, beat_len_sec) - RPR.RPR_MIDI_GetPPQPosFromProjTime(lead_take, 0)
        
        # Simple 2-note motif
        for i, beat in enumerate([0, 1.5, 3]):
            start = bar_start_ppq + (beat * beat_ppq)
            end = start + (beat_ppq * 0.5)
            pitch = get_pitch(0 if i%2==0 else 2, octave=5)
            RPR.RPR_MIDI_InsertNote(lead_take, False, False, start, end, 0, pitch, velocity_base, False)

    # --- 4. RISER/TRANSITION FX TRACK ---
    # Simulate the "Riser" transition shown in the video right before the Verse
    riser_track, riser_take = create_track_with_midi("Transition Riser", total_bars)
    RPR.RPR_TrackFX_AddByName(riser_track, "ReaSynth", False, -1)
    
    # We place one long note in the bar immediately preceding the Verse
    riser_bar = chorus_bars - 1
    start_time = riser_bar * bar_len_sec
    end_time = (riser_bar + 1) * bar_len_sec
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, start_time)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, end_time)
    
    pitch = get_pitch(0, octave=3)
    RPR.RPR_MIDI_InsertNote(riser_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    # Add volume automation to swell the riser (Technique: Transition dynamics)
    RPR.RPR_SetMediaTrackInfo_Value(riser_track, "D_VOL", 1.0)
    env = RPR.RPR_GetTrackEnvelopeByName(riser_track, "Volume")
    if not env:
        # Fallback if envelope isn't visible by default, force create it by adding an FX param env
        # Actually in ReaScript, track volume envelope can be selected/inserted via chunk, 
        # but to keep it perfectly safe across setups, we will automate track volume via API chunk or just leave the MIDI.
        # Alternatively, we can use MIDI expression (CC 11) for the swell! This is much safer.
        pass
        
    # Safer Volume Swell via MIDI CC 11 (Expression)
    steps = 16
    for i in range(steps):
        cc_time = start_ppq + (end_ppq - start_ppq) * (i / steps)
        # Parabolic swell curve (i/steps)^2
        val = int(127 * ((i / steps) ** 2))
        RPR.RPR_MIDI_InsertCC(riser_take, False, False, cc_time, 176, 0, 11, val)

    # Finalize all MIDI
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(lead_take)
    RPR.RPR_MIDI_Sort(riser_take)
    RPR.RPR_UpdateArrange()

    return f"Created Subtractive Arrangement ({total_bars} bars, Chorus->Verse drop) at {bpm} BPM in {key} {scale}."
