def create_pattern(
    project_name: str = "DungeonSynth",
    track_name: str = "DS_Motif",
    bpm: int = 85,
    key: str = "C",
    scale: str = "phrygian",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a Dungeon Synth A-B-A-C melody and polyrhythmic plucked ostinato.
    """
    import reaper_python as RPR

    # === Music Theory Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Normalize inputs
    root_midi = NOTE_MAP.get(key.capitalize(), 0)
    scale_name = scale.lower()
    if scale_name not in SCALES:
        scale_name = "phrygian"
    scale_intervals = SCALES[scale_name]

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Create Tracks ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Melody Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    melody_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(melody_track, "P_NAME", track_name + "_Flute_Melody", True)
    
    # Ostinato Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    ostinato_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(ostinato_track, "P_NAME", track_name + "_Lute_Ostinato", True)

    # === FX Chains ===
    # Flute Sound
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 2, 0.4)  # Square mix
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 3, 0.6)  # Saw mix
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 4, 0.15) # Attack (slow)
    RPR.RPR_TrackFX_SetParam(melody_track, 0, 7, 0.4)  # Release (smooth tail)
    
    RPR.RPR_TrackFX_AddByName(melody_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(melody_track, 1, 0, 0.7)  # Wet
    RPR.RPR_TrackFX_SetParam(melody_track, 1, 1, 0.4)  # Dry
    RPR.RPR_TrackFX_SetParam(melody_track, 1, 2, 0.9)  # Roomsize (huge)

    # Lute Sound
    RPR.RPR_TrackFX_AddByName(ostinato_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 0, 0.6)  # Volume
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 2, 0.8)  # Square mix
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 3, 0.0)  # Saw mix
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 4, 0.0)  # Attack (instant)
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 5, 0.15) # Decay (snappy)
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 6, 0.0)  # Sustain (none)
    RPR.RPR_TrackFX_SetParam(ostinato_track, 0, 7, 0.1)  # Release (short)

    # === MIDI Generation ===
    beats_per_bar = 4
    bar_sec = (60.0 / bpm) * beats_per_bar
    total_sec = bar_sec * bars

    # Create Items
    mel_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(mel_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(mel_item, "D_LENGTH", total_sec)
    mel_take = RPR.RPR_AddTakeToMediaItem(mel_item)

    ost_item = RPR.RPR_AddMediaItemToTrack(ostinato_track)
    RPR.RPR_SetMediaItemInfo_Value(ost_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(ost_item, "D_LENGTH", total_sec)
    ost_take = RPR.RPR_AddTakeToMediaItem(ost_item)

    def insert_note(take, item, pitch, pos_beats, len_beats, vel):
        item_start = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")
        start_time = item_start + (pos_beats * (60.0 / bpm))
        end_time = start_time + (len_beats * (60.0 / bpm))
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    def get_pitch(degree, octave):
        scale_len = len(scale_intervals)
        semitone = scale_intervals[degree % scale_len] + (degree // scale_len) * 12
        return root_midi + (octave * 12) + semitone

    # Structure: A (0,3,2) -> B (0,4,3) -> A (0,3,2) -> C (0,5,4)
    motifs = [
        [0, 3, 2], # Bar A: Root, 4th, 3rd
        [0, 4, 3], # Bar B: Root, 5th, 4th
        [0, 3, 2], # Bar A: Root, 4th, 3rd
        [0, 5, 4]  # Bar C: Root, 6th, 5th
    ]

    # Populate MIDI
    for b in range(bars):
        bar_motif = motifs[b % 4]
        bar_start_beat = b * 4.0
        
        # 1. Main Melody (Octave 5)
        insert_note(mel_take, mel_item, get_pitch(bar_motif[0], 5), bar_start_beat + 0.0, 2.0, velocity_base)
        insert_note(mel_take, mel_item, get_pitch(bar_motif[1], 5), bar_start_beat + 2.0, 1.0, velocity_base - 10)
        insert_note(mel_take, mel_item, get_pitch(bar_motif[2], 5), bar_start_beat + 3.0, 1.0, velocity_base - 15)
        
        # 2. Polyrhythmic Ostinato (Octave 4) 
        # Groups of 3 + 3 + 2 mapped over 8th notes (0.5 beats each)
        ost_pitches = [
            bar_motif[0], bar_motif[1], bar_motif[2], # Group 1 (3 notes)
            bar_motif[0], bar_motif[1], bar_motif[2], # Group 2 (3 notes)
            bar_motif[0], bar_motif[1]                # Group 3 (2 notes)
        ]
        
        for i, deg in enumerate(ost_pitches):
            p = get_pitch(deg, 4)
            # Accent the first note of each polyrhythmic group
            accent_offset = 0 if (i == 0 or i == 3 or i == 6) else 15
            vel = max(1, velocity_base - 10 - accent_offset)
            insert_note(ost_take, ost_item, p, bar_start_beat + (i * 0.5), 0.4, vel)

    RPR.RPR_MIDI_Sort(mel_take)
    RPR.RPR_MIDI_Sort(ost_take)

    return f"Created '{track_name}' (Flute & Lute) generating {bars} bars of A-B-A-C motif at {bpm} BPM in {key} {scale_name}."
