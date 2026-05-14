def create_pattern(
    project_name: str = "Chipmunk_Soul",
    track_name: str = "Soul_Chop_Group",
    bpm: int = 88,
    key: str = "F",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 'Chipmunk Soul' style Boom-Bap beat in REAPER.
    Generates a synthesized 'vinyl sample' (chords + high lead), a boom-bap drum break, and a Motown bassline.
    """
    import reaper_python as RPR

    # --- Music Theory & Tuning Setup ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Default to major for that uplifting soulful Kanye vibe
    if scale not in SCALES:
        scale = "major"
        
    root_midi = 48 + NOTE_MAP.get(key, 5) # Base octave 4 (e.g., F3)
    scale_intervals = SCALES[scale]
    
    def get_scale_note(degree_zero_indexed, octave_offset=0):
        octaves = degree_zero_indexed // 7
        scale_degree = degree_zero_indexed % 7
        return root_midi + (octaves + octave_offset) * 12 + scale_intervals[scale_degree]

    # --- Helper: Create Track & MIDI Item ---
    def create_track_with_midi(name, bars, bpm):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_length_sec * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def add_note(take, start_beat, duration_beats, pitch, vel, bpm):
        sec_per_beat = 60.0 / bpm
        start_time = start_beat * sec_per_beat
        end_time = start_time + (duration_beats * sec_per_beat)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- 1. Setup Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # --- 2. DRUMS TRACK (Boom-Bap Groove) ---
    drums_track, drums_take = create_track_with_midi(f"{track_name}_Drums", bars, bpm)
    
    # 2-bar drum pattern looped
    # Kick: 1, 2.75 (a of 2), 3.5 (and of 3)
    # Snare: 2, 4
    # Hats: swung 8ths
    for b in range(bars):
        bar_offset = b * 4.0
        
        # Kick (MIDI 36)
        add_note(drums_take, bar_offset + 0.0, 0.25, 36, velocity_base + 10, bpm)
        if b % 2 == 0:
            add_note(drums_take, bar_offset + 1.75, 0.25, 36, velocity_base - 10, bpm)
            add_note(drums_take, bar_offset + 2.5, 0.25, 36, velocity_base, bpm)
        else:
            add_note(drums_take, bar_offset + 2.0, 0.25, 36, velocity_base, bpm) # variation
            add_note(drums_take, bar_offset + 3.5, 0.25, 36, velocity_base - 10, bpm)

        # Snare (MIDI 38)
        add_note(drums_take, bar_offset + 1.0, 0.25, 38, velocity_base + 15, bpm)
        add_note(drums_take, bar_offset + 3.0, 0.25, 38, velocity_base + 15, bpm)
        
        # Hats (MIDI 42) - 8th notes with slight swing/velocity humanization
        for i in range(8):
            hat_pos = bar_offset + (i * 0.5)
            # Add micro-swing to offbeats
            if i % 2 != 0:
                hat_pos += 0.03
                vel = velocity_base - 25
            else:
                vel = velocity_base - 5
            add_note(drums_take, hat_pos, 0.1, 42, vel, bpm)

    # --- 3. BASS TRACK (Motown/James Jamerson style) ---
    bass_track, bass_take = create_track_with_midi(f"{track_name}_Bass", bars, bpm)
    # Add ReaSynth for a warm sine/triangle bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.0) # Saw down
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.5) # Triangle up
    
    # Bass rhythm follows the kick
    chord_roots = [0, 5, 1, 4] # I, vi, ii, V (0-indexed: 0=I, 5=vi, 1=ii, 4=V)
    for b in range(bars):
        bar_offset = b * 4.0
        root = get_scale_note(chord_roots[b % 4], -2) # Down 2 octaves
        
        # Staccato notes following kick pattern
        add_note(bass_take, bar_offset + 0.0, 0.2, root, velocity_base, bpm)
        if b % 2 == 0:
            add_note(bass_take, bar_offset + 1.75, 0.15, root, velocity_base - 10, bpm)
            add_note(bass_take, bar_offset + 2.5, 0.2, root, velocity_base, bpm)
        else:
            add_note(bass_take, bar_offset + 2.0, 0.2, root, velocity_base, bpm)
            add_note(bass_take, bar_offset + 3.5, 0.15, root, velocity_base - 10, bpm)


    # --- 4. "SAMPLED" CHOP TRACK (Soul Chords + EQ) ---
    chop_track, chop_take = create_track_with_midi(f"{track_name}_SoulSample", bars, bpm)
    RPR.RPR_TrackFX_AddByName(chop_track, "ReaSynth", False, -1)
    # Add a bandpass filter using ReaEQ to make it sound like a vintage sample
    eq_idx = RPR.RPR_TrackFX_AddByName(chop_track, "ReaEQ", False, -1)
    # Band 1: Highpass around 300Hz (clears mud for our bass)
    RPR.RPR_TrackFX_SetParam(chop_track, eq_idx, 0, 0) # Highpass type
    RPR.RPR_TrackFX_SetParam(chop_track, eq_idx, 1, 300.0) # Freq
    # Band 4: Lowpass around 4000Hz (removes modern sizzle)
    RPR.RPR_TrackFX_SetParam(chop_track, eq_idx, 9, 1) # Lowpass type
    RPR.RPR_TrackFX_SetParam(chop_track, eq_idx, 10, 4000.0) # Freq

    # Chords: Imaj7, vi7, ii7, V7 (Soul classic)
    # E.g., Fmaj7, Dm7, Gm7, C7
    chords = [
        [0, 2, 4, 6], # Imaj7
        [5, 7, 9, 11], # vi7
        [1, 3, 5, 7], # ii7
        [4, 6, 8, 10], # V7
    ]
    
    for b in range(bars):
        bar_offset = b * 4.0
        chord_degrees = chords[b % 4]
        
        # We "chop" the sample by re-triggering the chord on the 1, 2.5, 3.5 
        # (This mimics re-triggering an MPC pad)
        hits = [0.0, 1.5, 2.5, 3.5]
        for hit in hits:
            for deg in chord_degrees:
                pitch = get_scale_note(deg, 0)
                # Short, choppy lengths
                add_note(chop_take, bar_offset + hit, 0.4, pitch, velocity_base - 20, bpm)

    # --- 5. "CHIPMUNK" VOCAL LEAD ---
    # High-pitched synth to emulate the formant-shifted vocal
    vocal_track, vocal_take = create_track_with_midi(f"{track_name}_ChipmunkLead", bars, bpm)
    RPR.RPR_TrackFX_AddByName(vocal_track, "ReaSynth", False, -1)
    # Smooth sine wave, portamento enabled for vocal glides
    RPR.RPR_TrackFX_SetParam(vocal_track, 0, 6, 0.2) # Portamento/Glide
    
    # High register pentatonic riff
    lead_riff = [
        (0.0, 0.5, 4), (0.75, 0.25, 2), (1.5, 1.0, 0),
        (2.5, 0.25, 0), (2.75, 0.25, 2), (3.0, 0.75, 4)
    ]
    
    for b in range(bars):
        bar_offset = b * 4.0
        # Play different degrees based on the chord to stay harmonious
        chord_root = chords[b % 4][0]
        for pos, dur, deg in lead_riff:
            # Note is +2 octaves to sound "Chipmunked"
            pitch = get_scale_note(chord_root + deg, 2)
            add_note(vocal_take, bar_offset + pos, dur, pitch, velocity_base, bpm)

    # Force MIDI sort
    RPR.RPR_MIDI_Sort(drums_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(chop_take)
    RPR.RPR_MIDI_Sort(vocal_take)

    return f"Created 'Chipmunk Soul' pattern: Generated {bars} bars at {bpm} BPM in {key} {scale}. Vinyl-EQ'd sample chords, high-pitch portamento lead, syncopated Motown bass, and Boom-Bap drum break."
