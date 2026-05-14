def create_pattern(
    project_name: str = "Stadium Anthem",
    track_name: str = "Anthem",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Stadium Hip-Hop Anthem' featuring maximalist saw chords, frequency-split bass,
    and an evolving drum pattern in the current REAPER project.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Ensure valid scale fallback
    scale = scale.lower()
    if scale not in SCALES:
        scale = "minor"

    root_pitch = NOTE_MAP.get(key, 0) + 48 # Octave 4 for chords
    scale_intervals = SCALES[scale]

    # Helper function to get chord notes (triads) for a given scale degree (0-indexed)
    def get_chord(degree, root_offset=0):
        notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th of the chord
            idx = degree + i
            octave_shift = idx // len(scale_intervals)
            note_interval = scale_intervals[idx % len(scale_intervals)]
            notes.append(root_pitch + root_offset + note_interval + (octave_shift * 12))
        return notes

    # Triumphant Progression: i - VI - III - VII (0, 5, 2, 6 in 0-indexed minor)
    progression = [0, 5, 2, 6]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Helper to create a track with an item
    def create_track_with_item(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === TRACK 1: STADIUM KICKS ===
    kick_track, kick_take = create_track_with_item(f"{track_name} - Stadium Kicks")
    # Synthesize a basic kick with ReaSynth to make it audible (user should replace with drum sampler)
    fx_idx = RPR.RPR_TrackFX_AddByName(kick_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_track, fx_idx, 0, 0.0) # Saw mix 0
    RPR.RPR_TrackFX_SetParam(kick_track, fx_idx, 1, 0.0) # Square mix 0
    RPR.RPR_TrackFX_SetParam(kick_track, fx_idx, 5, 0.05) # Extra fast release
    
    kick_pitch = 36 # C2
    for b in range(bars):
        bar_start = b * bar_length_sec
        quarter_note = 60.0 / bpm
        eighth_note = quarter_note / 2.0
        
        if b < 2:
            # Bars 1-2: Four-on-the-floor stadium pulse
            for beat in range(4):
                start_time = bar_start + (beat * quarter_note)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time + 0.1)
                RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_pitch, velocity_base, False)
        else:
            # Bars 3-4: Syncopated Hip-Hop bounce transition (Hits on 1, 2.5, 3.5)
            hits = [0, 1.5, 2.5, 3.0]
            for h in hits:
                start_time = bar_start + (h * quarter_note)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(kick_take, start_time + 0.1)
                RPR.RPR_MIDI_InsertNote(kick_take, False, False, start_ppq, end_ppq, 0, kick_pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(kick_take)


    # === TRACK 2: SUB BASS (Pure Sine) ===
    sub_track, sub_take = create_track_with_item(f"{track_name} - Sub Bass (Sine)")
    fx_idx = RPR.RPR_TrackFX_AddByName(sub_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, fx_idx, 0, 0.0) # Saw mix 0
    RPR.RPR_TrackFX_SetParam(sub_track, fx_idx, 1, 0.0) # Square mix 0
    # Add EQ to filter out highs
    eq_idx = RPR.RPR_TrackFX_AddByName(sub_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(sub_track, eq_idx, 0, 0.0) # Low shelf/pass

    for b in range(bars):
        degree = progression[b % len(progression)]
        chord = get_chord(degree, root_offset=-24) # 2 Octaves down for sub
        sub_pitch = chord[0]
        
        start_time = b * bar_length_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(sub_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(sub_take, start_time + bar_length_sec - 0.05)
        
        RPR.RPR_MIDI_InsertNote(sub_take, False, False, start_ppq, end_ppq, 0, sub_pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(sub_take)


    # === TRACK 3: SYNTH BASS (Gritty Mid-Bass) ===
    bass_track, bass_take = create_track_with_item(f"{track_name} - Mid Bass (Gritty)")
    fx_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 0, 0.5) # Saw mix
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 1, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 4, 0.2) # Fast attack
    
    for b in range(bars):
        degree = progression[b % len(progression)]
        chord = get_chord(degree, root_offset=-12) # 1 Octave down for mid bass
        bass_pitch = chord[0]
        
        bar_start = b * bar_length_sec
        quarter_note = 60.0 / bpm
        
        # Rhythmic bounce mirroring the hip hop rhythm
        hits = [0, 0.75, 1.5, 2.5, 3.5]
        for h in hits:
            start_time = bar_start + (h * quarter_note)
            end_time = start_time + (quarter_note * 0.5) # staccato bounce
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(bass_take, end_time)
            RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base - 10, False)

    RPR.RPR_MIDI_Sort(bass_take)


    # === TRACK 4: ANTHEM CHORDS (Bright Saw) ===
    chord_track, chord_take = create_track_with_item(f"{track_name} - Anthem Chords")
    fx_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 0, 1.0) # Full Saw wave for stadium brightness
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 1, 0.3) # Slight Square
    RPR.RPR_TrackFX_SetParam(chord_track, fx_idx, 5, 0.8) # Longer release
    
    # Add wide reverb for the stadium feel
    verb_idx = RPR.RPR_TrackFX_AddByName(chord_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, verb_idx, 0, 0.8) # Room size
    RPR.RPR_TrackFX_SetParam(chord_track, verb_idx, 1, 0.5) # Dampening

    for b in range(bars):
        degree = progression[b % len(progression)]
        chord = get_chord(degree)
        
        bar_start = b * bar_length_sec
        quarter_note = 60.0 / bpm
        
        # Syncopated stadium stabs
        stabs = [
            (0, 1.5),         # Downbeat long stab
            (2.5, 1.0),       # Off-beat mid stab
            (4.0, 0.5)        # Pickup stab for the next bar
        ]
        
        for (beat_offset, duration_beats) in stabs:
            start_time = bar_start + (beat_offset * quarter_note)
            if start_time >= total_length_sec:
                continue
            
            end_time = min(start_time + (duration_beats * quarter_note), total_length_sec)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chord_take, end_time)
            
            for pitch in chord:
                RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
                
    RPR.RPR_MIDI_Sort(chord_take)

    RPR.RPR_UpdateArrange()

    return f"Created Stadium Anthem pattern '{track_name}' featuring 4 tracks (Kicks, Sub, Mid-Bass, Chords) over {bars} bars at {bpm} BPM in {key} {scale}."
