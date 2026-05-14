def create_pattern(
    project_name: str = "BossaNova",
    track_name: str = "Bossa",
    bpm: int = 80,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Bossa Nova Groove & Harmony scaffold in the current REAPER project.
    Generates 4 tracks: Drums, Bass, Chords, and Lead Synth.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    base_note = NOTE_MAP.get(key.upper() if len(key) == 1 else key.capitalize(), 0) + 48 # Root at C3

    # Define diatonic 9th chord voicings based on the scale feeling
    if scale.lower() == "major":
        # I maj9, ii min9, vi min9, V 13
        chords = [
            [0, 4, 7, 11, 14],     
            [2, 5, 9, 12, 16],     
            [-3, 0, 4, 7, 11],     
            [7, 11, 14, 17, 21]    
        ]
    else:
        # i min9, iv min9, VII maj9, III maj9 (Classic minor Bossa progression)
        chords = [
            [0, 3, 7, 10, 14],     
            [-7, -4, 0, 3, 7],     
            [-2, 2, 5, 9, 12],     
            [3, 7, 10, 14, 17]     
        ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * 4
    # Extend item length slightly so reverb tails and turnaround lead licks ring out
    item_length_sec = (bar_length_sec * bars) + (beat_len_sec * 2)

    # Helper function to create a track with a MIDI item
    def create_track_with_midi(name, index_offset):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        return track, take

    # Helper function to insert notes into a take
    def add_midi_notes(take, notes_list):
        # notes_list format: (step_16th, pitch, duration_16ths, velocity)
        for step, pitch, dur, vel in notes_list:
            start_sec = step * (beat_len_sec / 4.0)
            end_sec = start_sec + (dur * (beat_len_sec / 4.0))
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        RPR.RPR_MIDI_Sort(take)

    # === Step 2: Generate Sequences ===
    drum_notes = []
    bass_notes = []
    chord_notes = []
    lead_notes = []

    for bar in range(bars):
        bar_offset = bar * 16
        chord_idx = bar % 4
        
        # --- DRUMS ---
        # Kick drum (Anticipated groove)
        drum_notes.extend([
            (bar_offset + 0, 36, 2, 100),
            (bar_offset + 6, 36, 2, 90),
            (bar_offset + 8, 36, 2, 100),
            (bar_offset + 14, 36, 2, 90),
        ])
        # Rimshot Clave
        clave_steps = [0, 6, 12] if bar % 2 == 0 else [2, 8, 14]
        for step in clave_steps:
            drum_notes.append((bar_offset + step, 37, 2, 110))
        # Ride Cymbal
        for step in range(0, 16, 2):
            vel = 80 if step % 4 == 0 else 60
            drum_notes.append((bar_offset + step, 51, 1, vel))

        # --- BASS ---
        root_pitch = base_note + chords[chord_idx][0] - 12
        fifth_pitch = base_note + chords[chord_idx][2] - 12
        bass_notes.extend([
            (bar_offset + 0, root_pitch, 5, 110),
            (bar_offset + 6, root_pitch, 2, 90),
            (bar_offset + 8, fifth_pitch, 5, 100),
            (bar_offset + 14, root_pitch, 2, 90),
        ])

        # --- CHORDS ---
        voicings = [base_note + offset for offset in chords[chord_idx]]
        for step in clave_steps:
            for i, pitch in enumerate(voicings):
                # Strum the chord slightly (0.15 16th-notes per string)
                roll = i * 0.15 
                chord_notes.append((bar_offset + step + roll, pitch, 4, 85 - (i*2)))

        # --- LEAD SYNTH ---
        # Descending pentatonic lick at the end of every 2 bars
        if bar % 2 == 1:
            octave = base_note + 12
            if scale.lower() == "major":
                lick = [(8, 9), (10, 7), (12, 4), (14, 2), (16, 0)] # Maj pentatonic
            else:
                lick = [(8, 10), (10, 7), (12, 5), (14, 3), (16, 0)] # Min pentatonic
            
            for step_offset, interval in lick:
                dur = 6.0 if step_offset == 16 else 1.5
                lead_notes.append((bar_offset + step_offset, octave + interval, dur, 100))


    # === Step 3: Create Tracks & Inject MIDI ===
    trk_drums, take_drums = create_track_with_midi("Drums", 0)
    add_midi_notes(take_drums, drum_notes)

    trk_bass, take_bass = create_track_with_midi("Bass", 1)
    add_midi_notes(take_bass, bass_notes)
    RPR.RPR_TrackFX_AddByName(trk_bass, "ReaSynth", False, -1)

    trk_chords, take_chords = create_track_with_midi("Keys", 2)
    add_midi_notes(take_chords, chord_notes)
    RPR.RPR_TrackFX_AddByName(trk_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(trk_chords, "ReaVerbate", False, -1)

    trk_lead, take_lead = create_track_with_midi("Lead", 3)
    add_midi_notes(take_lead, lead_notes)
    RPR.RPR_TrackFX_AddByName(trk_lead, "ReaSynth", False, -1)
    # Add EQ to create a resonant peak simulating the "Meow" brass synth
    eq_idx = RPR.RPR_TrackFX_AddByName(trk_lead, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(trk_lead, "ReaDelay", False, -1)

    return f"Created Bossa Nova ensemble ({bars} bars) in {key} {scale} at {bpm} BPM."
