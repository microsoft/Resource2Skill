def create_pattern(
    project_name: str = "Synthwave_Project",
    track_name: str = "Retro",
    bpm: int = 105,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full 4-track Synthwave groove (Drums, Arp Bass, Pumping Pad, Looping Lead).
    It implements the cinematic minor-key progression and simulates sidechain compression.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper function to scaffold tracks safely
    def create_midi_track(name, item_length):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(trk)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return trk, take

    # Helper function for mathematically precise MIDI note placement
    def add_midi_note(take, start_sec, end_sec, pitch, vel):
        # 1 Quarter Note (beat) = 960 PPQ in default REAPER setups
        start_ppq = (start_sec * bpm / 60.0) * 960
        end_ppq = (end_sec * bpm / 60.0) * 960
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 2: Music Theory Calculations ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 11) # Defaults to B2

    # The signature Retrowave progression: i -> VImaj7 -> VII -> V7
    # Calculated as precise semitone offsets relative to the minor root
    progression = [
        [0, 3, 7],           # Bar 1: i (e.g., B minor)
        [-4, 0, 3, 7],       # Bar 2: VI maj7 (e.g., G Major 7)
        [-2, 2, 5],          # Bar 3: VII (e.g., A Major)
        [-5, -1, 2, 5]       # Bar 4: V7 (e.g., F# Dom 7)
    ]
    # Arp roots corresponding to the chords
    roots = [0, -4, -2, -5]

    bar_len = (60.0 / bpm) * 4
    total_len = bar_len * bars

    # === Step 3: Track Generation ===

    # TRACK 1: 4-on-the-floor Drums
    drum_trk, drum_take = create_midi_track(f"{track_name}_Drums", total_len)
    for b in range(bars * 4): # Loop over every beat
        beat_time = b * (60.0 / bpm)
        # Kick drum on every beat
        add_midi_note(drum_take, beat_time, beat_time + 0.1, 36, velocity_base + 10)
        # Snare drum on backbeats (2 and 4)
        if b % 4 in [1, 3]:
            add_midi_note(drum_take, beat_time, beat_time + 0.2, 38, velocity_base + 20)

    # TRACK 2: Driving 16th-Note Bass Arp
    bass_trk, bass_take = create_midi_track(f"{track_name}_BassArp", total_len)
    RPR.RPR_TrackFX_AddByName(bass_trk, "ReaSynth", False, -1)
    
    sixteenth_len = (60.0 / bpm) * 0.25
    for b in range(bars):
        bar_start = b * bar_len
        root_offset = roots[b % len(roots)]
        bass_pitch = root_midi + root_offset - 12 # Drop down 1 octave
        
        for i in range(16):
            note_start = bar_start + (i * sixteenth_len)
            # Add subtle velocity groove
            vel = velocity_base if i % 4 == 0 else velocity_base - 20
            add_midi_note(bass_take, note_start, note_start + sixteenth_len*0.8, bass_pitch, vel)

    # TRACK 3: Lush Pad with Sidechain Pumping Simulation
    pad_trk, pad_take = create_midi_track(f"{track_name}_LushPad", total_len)
    fx_idx = RPR.RPR_TrackFX_AddByName(pad_trk, "ReaSynth", False, -1)
    
    # Configure ReaSynth to swell on attack, simulating a compressor ducking
    RPR.RPR_TrackFX_SetParam(pad_trk, fx_idx, 2, 0.4) # Attack (Param 2) - Slow swell
    RPR.RPR_TrackFX_SetParam(pad_trk, fx_idx, 3, 0.5) # Release (Param 3) - Smooth fade
    RPR.RPR_TrackFX_SetParam(pad_trk, fx_idx, 5, 1.0) # Sawtooth mix (Param 5)
    
    RPR.RPR_TrackFX_AddByName(pad_trk, "ReaVerbate", False, -1) # Add Reverb

    for b in range(bars):
        bar_start = b * bar_len
        chord_offsets = progression[b % len(progression)]
        
        # Trigger chords on every downbeat to force the synth attack envelope to swell
        beat_len = (60.0 / bpm)
        for beat in range(4):
            beat_start = bar_start + (beat * beat_len)
            for offset in chord_offsets:
                pitch = root_midi + offset
                add_midi_note(pad_take, beat_start, beat_start + beat_len, pitch, velocity_base - 10)

    # TRACK 4: Looping 8th-Note Lead Melody
    lead_trk, lead_take = create_midi_track(f"{track_name}_Lead", total_len)
    RPR.RPR_TrackFX_AddByName(lead_trk, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(lead_trk, "ReaDelay", False, -1)

    # Repetitive synth motif (Root, Minor 3rd, Major 2nd, Perfect 5th)
    motif = [12, 15, 14, 7]
    eighth_len = (60.0 / bpm) * 0.5
    for b in range(bars):
        bar_start = b * bar_len
        for i in range(8):
            note_start = bar_start + (i * eighth_len)
            pitch = root_midi + motif[i % len(motif)] + 12 # Octave up
            add_midi_note(lead_take, note_start, note_start + eighth_len*0.8, pitch, velocity_base)

    return f"Created 4-Track Synthwave Pattern (Drums, Bass, Pad, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
