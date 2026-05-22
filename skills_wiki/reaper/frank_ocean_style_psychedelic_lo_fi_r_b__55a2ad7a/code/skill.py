def create_pattern(
    project_name: str = "Frank_Ocean_Vibe",
    track_name: str = "LoFi_R&B",
    bpm: int = 85,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Frank Ocean-style Psychedelic Lo-Fi R&B Groove in REAPER.
    Generates a tape-wobbled electric piano chord progression, a Minimoog-style 
    syncopated bassline, and a sparse drum groove.
    """
    import reaper_python as RPR

    # === Music Theory & Scales ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }
    
    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper(), 5) # Default to F
    
    # Base octave for chords is C3 (MIDI 48)
    base_midi = 48 + root_val 

    # Generate a lookup list of diatonic notes across 5 octaves
    diatonic_notes = []
    for oct_mult in range(-2, 3): 
        for interval in scale_intervals:
            diatonic_notes.append(base_midi + interval + (oct_mult * 12))

    # Helper: get a diatonic 7th chord starting from a specific scale degree
    def get_diatonic_7th(degree, octave_offset=0):
        # degree is 0-indexed relative to the root base_midi
        zero_index = len(scale_intervals) * 2 # Center octave in our list
        start_idx = zero_index + degree + (octave_offset * len(scale_intervals))
        return [
            diatonic_notes[start_idx],       # Root
            diatonic_notes[start_idx + 2],   # 3rd
            diatonic_notes[start_idx + 4],   # 5th
            diatonic_notes[start_idx + 6]    # 7th
        ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    PPQ = 960 # Standard REAPER Pulses Per Quarter Note
    bar_len_sec = (60.0 / bpm) * 4
    total_len_sec = bar_len_sec * bars

    # Track tracking
    created_tracks = []

    # === Helper to create tracks and MIDI items ===
    def create_midi_track(name):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_len_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        created_tracks.append(track)
        return track, take

    # ==========================================
    # TRACK 1: Lo-Fi Tape Chords (Wurlitzer vibe)
    # ==========================================
    chords_track, chords_take = create_midi_track(f"{track_name}_Keys")
    
    # Progression: i7 -> v7 -> VImaj7 -> iv7
    chord_degrees = [0, 4, 5, 3] 

    for bar in range(bars):
        degree = chord_degrees[bar % len(chord_degrees)]
        chord_pitches = get_diatonic_7th(degree, octave_offset=0)
        
        start_ppq = int(bar * 4 * PPQ)
        end_ppq = int((bar * 4 + 3.8) * PPQ) # Slight legato gap
        
        for p in chord_pitches:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, p, velocity_base - 10, False)
    
    RPR.RPR_MIDI_Sort(chords_take)

    # FX Chain for Lo-Fi Chords
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(chords_track, "JS: Lo-Fi", False, -1)
    # Bitcrusher / Sample rate reduction
    RPR.RPR_TrackFX_SetParam(chords_track, 1, 0, 4000) # Param 0: Sample Rate -> 4000Hz as per video
    RPR.RPR_TrackFX_SetParam(chords_track, 1, 1, 12)   # Param 1: Bit Depth -> 12 bit
    
    # Tape wobble using JS: Chorus
    RPR.RPR_TrackFX_AddByName(chords_track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, 2, 0, 2.0)  # Delay length (wobble size)
    RPR.RPR_TrackFX_SetParam(chords_track, 2, 1, 0.5)  # Rate (slow wow)
    
    # Spacey Reverb
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(chords_track, 3, 0, 0.8) # Wet
    RPR.RPR_TrackFX_SetParam(chords_track, 3, 1, 0.2) # Dry
    RPR.RPR_TrackFX_SetParam(chords_track, 3, 2, 0.7) # Room size


    # ==========================================
    # TRACK 2: Minimoog-Style Bass
    # ==========================================
    bass_track, bass_take = create_midi_track(f"{track_name}_Bass")
    
    for bar in range(bars):
        degree = chord_degrees[bar % len(chord_degrees)]
        # Get the root note, drop it down 2 octaves for sub
        root_pitch = get_diatonic_7th(degree, octave_offset=-2)[0]
        
        # Syncopated Groove: 1 (long), 2-and-a (short), 3-and (mid)
        # Note 1: Beat 1
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, int((bar * 4) * PPQ), int((bar * 4 + 1.5) * PPQ), 0, root_pitch, velocity_base + 10, False)
        # Note 2: Beat 2.75 (syncopated 16th)
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, int((bar * 4 + 1.75) * PPQ), int((bar * 4 + 2.0) * PPQ), 0, root_pitch, velocity_base, False)
        # Note 3: Beat 2.5
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, int((bar * 4 + 2.5) * PPQ), int((bar * 4 + 3.0) * PPQ), 0, root_pitch, velocity_base - 5, False)
        # Note 4: Beat 4
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, int((bar * 4 + 3.0) * PPQ), int((bar * 4 + 3.5) * PPQ), 0, root_pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(bass_take)

    # FX Chain for Moog Bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Saturation (Decapitator alternative)
    RPR.RPR_TrackFX_AddByName(bass_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 0, 50.0) # Drive amount
    # Lowpass EQ to focus the sub
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)


    # ==========================================
    # TRACK 3: Sparse Groove Drums
    # ==========================================
    drum_track, drum_take = create_midi_track(f"{track_name}_Drums")
    
    KICK = 36
    SNARE = 38
    HAT = 42

    for bar in range(bars):
        base_beat = bar * 4
        
        # Kicks: Beat 1 and syncopated Beat 2.5
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, int(base_beat * PPQ), int((base_beat + 0.25) * PPQ), 9, KICK, velocity_base + 15, False)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, int((base_beat + 1.5) * PPQ), int((base_beat + 1.75) * PPQ), 9, KICK, velocity_base - 10, False)
        
        # Snare/Snap: Beat 2 and 4
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, int((base_beat + 1.0) * PPQ), int((base_beat + 1.25) * PPQ), 9, SNARE, velocity_base, False)
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, int((base_beat + 3.0) * PPQ), int((base_beat + 3.25) * PPQ), 9, SNARE, velocity_base + 5, False)

        # Sparse Hats: 8th notes, skipping beat 2 and 4 to leave room for the snare
        for h in [0.0, 0.5, 1.5, 2.0, 2.5, 3.5]:
            vel = velocity_base - 20 if h % 1.0 != 0 else velocity_base - 10
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, int((base_beat + h) * PPQ), int((base_beat + h + 0.125) * PPQ), 9, HAT, vel, False)

    RPR.RPR_MIDI_Sort(drum_take)
    
    # Reverb on drums (as seen in the tutorial for the kicks/snares)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, 0, 0, 0.15) # Keep wet low so it's subtle space

    return f"Created Frank Ocean Lo-Fi Groove: 3 tracks (Chords, Bass, Drums) over {bars} bars at {bpm} BPM in {key} {scale}."
