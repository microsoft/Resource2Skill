def create_pattern(
    project_name: str = "Arrangement",
    track_name: str = "TrapBeat",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a complete 12-bar Trap Arrangement (Intro -> Drop -> Verse Breakdown).
    Features stutter builds, tension risers, 808 basslines, and half-time verse emulation.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (140 recommended for trap double-time).
        key: Root note (e.g., C, D#, F).
        scale: Scale type (minor, major, harmonic_minor, dorian).
        bars: Number of bars (generates 12 bars by default).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    # === Step 1: Setup Tempo & Music Theory ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_note = 48 + root_val # Anchored around C3
    
    # Progression: i - VI (minor) or I - IV (major)
    chord1_deg = [0, 2, 4]
    chord2_deg = [5, 7, 9] if scale != "major" else [3, 5, 7]
    
    # === Helper Functions ===
    def get_pitches(root_p, degrees):
        pitches = []
        for deg in degrees:
            oct_shift = deg // len(scale_intervals)
            idx = deg % len(scale_intervals)
            pitches.append(root_p + (oct_shift * 12) + scale_intervals[idx])
        return pitches
        
    def add_midi_item(track, start_beat, end_beat):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
        return RPR.RPR_GetActiveTake(item)
        
    def add_note(take, start_beat, end_beat, pitch, vel):
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    def add_cc(take, beat, cc_num, val):
        val = max(0, min(127, int(val)))
        time_sec = beat * (60.0 / bpm)
        ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)
        RPR.RPR_MIDI_InsertCC(take, False, False, ppq, 176, 0, cc_num, val)
        
    def make_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(tr, "ReaSynth", False, -1) # Default placeholder
        return tr

    # === Step 2: Track Creation ===
    tr_mel   = make_track(f"{track_name}_Melody")
    tr_kick  = make_track(f"{track_name}_Kick")
    tr_snare = make_track(f"{track_name}_Snare")
    tr_hat   = make_track(f"{track_name}_Hats")
    tr_808   = make_track(f"{track_name}_808")
    tr_riser = make_track(f"{track_name}_Riser_FX")
    
    # === Step 3: Melody Track (Chords & Stutters) ===
    take_mel = add_midi_item(tr_mel, 0, 48) # 12 Bars = 48 Beats
    
    def write_chord(take, sb, eb, root_p, degs, vel):
        for p in get_pitches(root_p, degs):
            add_note(take, sb, eb, p, vel)
            
    # Intro (Beats 0-16)
    write_chord(take_mel, 0, 8, base_note, chord1_deg, velocity_base)
    write_chord(take_mel, 8, 12, base_note, chord2_deg, velocity_base)
    # Stutter effect on Intro Bar 4
    write_chord(take_mel, 12, 14, base_note, chord2_deg, velocity_base)
    write_chord(take_mel, 14, 15, base_note, chord2_deg, velocity_base)
    write_chord(take_mel, 15, 16, base_note, chord2_deg, velocity_base)
    
    # Drop (Beats 16-32)
    write_chord(take_mel, 16, 24, base_note, chord1_deg, velocity_base+10)
    write_chord(take_mel, 24, 32, base_note, chord2_deg, velocity_base+10)
    
    # Verse / Breakdown (Beats 32-48) - Pitched down 1 octave to simulate HalfTime
    write_chord(take_mel, 32, 40, base_note - 12, chord1_deg, velocity_base-10)
    write_chord(take_mel, 40, 48, base_note - 12, chord2_deg, velocity_base-10)
    
    # === Step 4: Drums (Kick, Snare, Hats) ===
    take_k = add_midi_item(tr_kick, 0, 48)
    take_s = add_midi_item(tr_snare, 0, 48)
    take_h = add_midi_item(tr_hat, 0, 48)
    
    pitch_k, pitch_s, pitch_h = 36, 38, 42 # General MIDI C1, D1, F#1
    
    # Intro Build-up Fill (Beat 15)
    add_note(take_k, 15.0, 15.25, pitch_k, velocity_base)
    add_note(take_k, 15.5, 15.75, pitch_k, velocity_base)
    add_note(take_s, 15.75, 16.0, pitch_s, velocity_base+10)
    
    # Drop Drums (Beats 16-32)
    for b in [16, 24]:
        # Trap Kick Groove
        add_note(take_k, b+0.0, b+0.5, pitch_k, velocity_base+10)
        add_note(take_k, b+2.5, b+3.0, pitch_k, velocity_base+5)
        add_note(take_k, b+5.0, b+5.5, pitch_k, velocity_base+10)
        add_note(take_k, b+6.5, b+7.0, pitch_k, velocity_base+5)
        # Snare (Beats 3 and 7 in double time)
        add_note(take_s, b+2.0, b+2.5, pitch_s, velocity_base+10)
        add_note(take_s, b+6.0, b+6.5, pitch_s, velocity_base+10)
        # 1/8th Hats with 1/16th Roll
        for h in range(16):
            if h == 14: # Roll
                add_note(take_h, b + h*0.5, b + h*0.5 + 0.25, pitch_h, velocity_base)
                add_note(take_h, b + h*0.5 + 0.25, b + h*0.5 + 0.5, pitch_h, velocity_base)
            else:
                add_note(take_h, b + h*0.5, b + h*0.5 + 0.25, pitch_h, velocity_base if h%2==0 else velocity_base-20)
                
    # Verse Breakdown Drums (Beats 32-48) - Sparse Density
    for b in [32, 40]:
        add_note(take_k, b+0.0, b+0.5, pitch_k, velocity_base) # Kick only on the 1
        add_note(take_s, b+2.0, b+2.5, pitch_s, velocity_base-10)
        add_note(take_s, b+6.0, b+6.5, pitch_s, velocity_base-10)
        for h in range(8): # Slow 1/4 note hats
            add_note(take_h, b + h*1.0, b + h*1.0 + 0.25, pitch_h, velocity_base-15)

    # === Step 5: 808 Bass ===
    take_808 = add_midi_item(tr_808, 0, 48)
    
    # 808 ONLY plays during the Drop
    for b, deg in [(16, chord1_deg[0]), (24, chord2_deg[0])]:
        r808 = get_pitches(24, [deg])[0] # Anchor around C1 (24)
        if r808 > 29: r808 -= 12 # Clamp range for sub impact
        
        add_note(take_808, b+0.0, b+2.0, r808, velocity_base+10)
        add_note(take_808, b+2.5, b+4.0, r808, velocity_base)
        add_note(take_808, b+5.0, b+6.0, r808, velocity_base+10)
        add_note(take_808, b+6.5, b+8.0, r808, velocity_base)
        
    # === Step 6: FX Riser / Transition Sweeps ===
    take_riser = add_midi_item(tr_riser, 0, 48)
    
    # Ascending Arp Riser into Drop (Beats 8 to 16)
    for i in range(32):
        beat = 8 + i*0.25
        p = get_pitches(base_note + 12, [i % 14])[0] # Ascend scale
        add_note(take_riser, beat, beat+0.25, p, 90)
        add_cc(take_riser, beat, 7, int(127 * (i/31.0))) # CC7 Volume Fade In
        
    # Descending Arp Transition into Verse (Beats 24 to 32)
    for i in range(32):
        beat = 24 + i*0.25
        p = get_pitches(base_note + 12, [13 - (i % 14)])[0] # Descend scale
        add_note(take_riser, beat, beat+0.25, p, 90)
        add_cc(take_riser, beat, 7, int(127 * (1.0 - (i/31.0)))) # CC7 Volume Fade Out
        
    # === Step 7: Finalize ===
    for take in [take_mel, take_k, take_s, take_h, take_808, take_riser]:
        RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' Arrangement Toolkit: 12 bars (Intro->Drop->Verse) in {key} {scale} at {bpm} BPM."
