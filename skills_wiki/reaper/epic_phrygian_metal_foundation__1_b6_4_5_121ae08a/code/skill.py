def create_pattern(
    project_name: str = "FirstMetalSong",
    track_name: str = "Metal Foundation",
    bpm: int = 160,
    key: str = "E",
    scale: str = "phrygian",
    bars: int = 8,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates an Epic Phrygian Metal Foundation featuring a 4-track arrangement:
    Drums, Bass, and double-tracked hard-panned rhythm Guitars playing a 1-b6-4-5 progression.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated group of tracks.
        bpm: Tempo in BPM (Standard metal pace is 150-180).
        key: Root note (e.g., "E" is standard for metal).
        scale: Scale type (defaults to "phrygian" for that dark metal sound).
        bars: Number of bars to generate (should be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127). High for aggressive playing.
        **kwargs: Additional overrides.

    Returns:
        Status string indicating the created elements.
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10], # Metal staple
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    }

    # 1 - b6 - 4 - 5 relative to the scale indices
    # In Phrygian: index 0 (Root), index 5 (min 6th), index 3 (perf 4th), index 4 (perf 5th)
    progression_indices = [0, 5, 3, 4] 
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["phrygian"])
    base_note = NOTE_MAP.get(key.upper(), 4) # Default to E
    guitar_base_octave = 2 * 12 # E2 is MIDI 40
    bass_base_octave = 1 * 12   # E1 is MIDI 28

    # --- Set Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # --- Helper: Insert Track ---
    def add_track(name, pan=0.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        return track

    # --- Helper: Create MIDI Item ---
    def create_midi_item(track, length_sec):
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        return take

    # --- Helper: Insert MIDI Note ---
    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), "")

    # =========================================================================
    # 1. DRUMS TRACK (Center)
    # =========================================================================
    drum_track = add_track(f"{track_name} - Drums", pan=0.0)
    drum_take = create_midi_item(drum_track, total_length_sec)
    
    for bar in range(bars):
        for beat in range(4): # 4 quarter notes
            for sub in range(2): # 8th notes
                time_start = (bar * bar_length_sec) + (beat * 60.0 / bpm) + (sub * 30.0 / bpm)
                time_end = time_start + (30.0 / bpm) * 0.9 # Slightly detached
                
                # Snare on beats 2 and 4 (beat == 1 or beat == 3)
                if beat == 1 or beat == 3:
                    if sub == 0:
                        insert_note(drum_take, time_start, time_end, 38, velocity_base) # Snare
                else:
                    # Kicks on everything else for a driving rhythm
                    insert_note(drum_take, time_start, time_end, 36, velocity_base) # Kick
                
                # Hi-hat on all 8ths
                insert_note(drum_take, time_start, time_end, 42, velocity_base - 10) # Closed Hat
                
        # Crash on the 1st beat of every 4-bar phrase
        if bar % 4 == 0:
            insert_note(drum_take, bar * bar_length_sec, (bar * bar_length_sec) + 0.5, 49, velocity_base + 10)

    # =========================================================================
    # 2. BASS TRACK (Center)
    # =========================================================================
    bass_track = add_track(f"{track_name} - Bass", pan=0.0)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    bass_take = create_midi_item(bass_track, total_length_sec)

    # =========================================================================
    # 3. GUITAR TRACKS (Hard Left & Hard Right)
    # =========================================================================
    gtr_l_track = add_track(f"{track_name} - Guitar L", pan=-1.0)
    RPR.RPR_TrackFX_AddByName(gtr_l_track, "ReaSynth", False, -1)
    gtr_l_take = create_midi_item(gtr_l_track, total_length_sec)

    gtr_r_track = add_track(f"{track_name} - Guitar R", pan=1.0)
    RPR.RPR_TrackFX_AddByName(gtr_r_track, "ReaSynth", False, -1)
    gtr_r_take = create_midi_item(gtr_r_track, total_length_sec)

    # Generate the riffs
    for bar in range(bars):
        # Determine the chord root for this bar (loops every 4 bars)
        degree_idx = progression_indices[bar % 4]
        interval = scale_intervals[degree_idx]
        
        guitar_root = base_note + guitar_base_octave + interval
        bass_root = base_note + bass_base_octave + interval
        
        # 8th note chugs
        for beat in range(4):
            for sub in range(2):
                time_start = (bar * bar_length_sec) + (beat * 60.0 / bpm) + (sub * 30.0 / bpm)
                # Staccato gate (85%) for aggressive heavy metal chugging
                time_end = time_start + (30.0 / bpm) * 0.85 
                
                # Bass: Just the root note
                insert_note(bass_take, time_start, time_end, bass_root, velocity_base)
                
                # Guitars: Power Chords (Root, +7 Perfect Fifth, +12 Octave)
                for gtr_take in [gtr_l_take, gtr_r_take]:
                    insert_note(gtr_take, time_start, time_end, guitar_root, velocity_base)
                    insert_note(gtr_take, time_start, time_end, guitar_root + 7, velocity_base - 5)
                    insert_note(gtr_take, time_start, time_end, guitar_root + 12, velocity_base - 10)

    # Ensure MIDI items are updated in REAPER UI
    RPR.RPR_UpdateArrange()

    return f"Created Metal Foundation (Drums, Bass, 2x Panned Guitars) with a {scale} 1-b6-4-5 progression over {bars} bars at {bpm} BPM."
