def create_pattern(
    project_name: str = "Jungle_Project",
    track_name: str = "Jungle_Scaffold",
    bpm: int = 165,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 90s Jungle arrangement scaffold (Drums, Staccato Bass, Ethereal Pads) in REAPER.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (160-170 recommended for Jungle).
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.upper(), 5) # Default F
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def insert_midi_item_with_notes(track, name, notes_data, is_pad=False):
        """Helper to create an item, take, and insert precise MIDI notes via time-to-PPQ."""
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_GetSetMediaItemInfo_String(item, "P_NOTES", name, True)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        # Extend pad item length slightly to accommodate overlapping tails
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec + (bar_length_sec if is_pad else 0))
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for note in notes_data:
            start_beat, duration_beats, pitch, vel = note
            start_time = (60.0 / bpm) * start_beat
            end_time = start_time + ((60.0 / bpm) * duration_beats)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
            
        RPR.RPR_MIDI_Sort(take)
        return item

    # ==========================================
    # TRACK 1: JUNGLE DRUM BREAK (MIDI Proxy)
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name}_Break_MIDI", True)
    
    drum_notes = []
    # Standard GM Map: 36 Kick, 38 Snare, 42 Closed Hat
    for b in range(bars):
        offset = b * 4
        # Kick Pattern: Syncopated
        drum_notes.append((offset + 0.0, 0.25, 36, velocity_base))       # Beat 1
        drum_notes.append((offset + 1.5, 0.25, 36, velocity_base - 10))  # Beat 2 "and"
        drum_notes.append((offset + 2.75, 0.25, 36, velocity_base - 20)) # Beat 3 "a"
        
        # Snare Pattern: Core hits + ghost notes
        drum_notes.append((offset + 1.0, 0.25, 38, velocity_base + 10))  # Beat 2
        drum_notes.append((offset + 3.0, 0.25, 38, velocity_base + 10))  # Beat 4
        # Ghost snares mimicking chopped break fills
        drum_notes.append((offset + 1.75, 0.125, 38, velocity_base - 40)) 
        drum_notes.append((offset + 3.5, 0.125, 38, velocity_base - 30))
        drum_notes.append((offset + 3.75, 0.125, 38, velocity_base - 40))
        
        # Hi-Hats: Rapid 8ths and 16ths
        for i in range(16):
            hat_pos = offset + (i * 0.25)
            # Skip hats exactly where main snare hits to leave room
            if hat_pos not in [offset + 1.0, offset + 3.0]:
                drum_notes.append((hat_pos, 0.125, 42, velocity_base - 25 if i % 2 != 0 else velocity_base - 10))

    insert_midi_item_with_notes(drum_track, "Jungle Break", drum_notes)

    # ==========================================
    # TRACK 2: STACCATO DREAD BASS
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_DreadBass", True)
    
    # Add a stock synth for the sub bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    # Tune ReaSynth down to act as a sub
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.0) # Volume lower
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.0) # Tuning
    
    bass_notes = []
    bass_root = 24 + root_val # Sub octave (MIDI C1/C2 range)
    bass_fifth = bass_root + 7
    
    for b in range(bars):
        offset = b * 4
        # Tutorial note: "cut off the tail ends of the base notes slightly... adds extra bounce"
        # We use a very short duration (0.15 beats) for a staccato 16th note feel.
        staccato_dur = 0.15 
        
        bass_notes.append((offset + 0.0, staccato_dur, bass_root, velocity_base)) 
        bass_notes.append((offset + 1.5, staccato_dur, bass_root, velocity_base))
        bass_notes.append((offset + 2.5, staccato_dur, bass_fifth, velocity_base - 10))
        bass_notes.append((offset + 3.75, staccato_dur, bass_root, velocity_base))

    insert_midi_item_with_notes(bass_track, "Staccato Bass", bass_notes)

    # ==========================================
    # TRACK 3: ETHEREAL AMBIENT PADS
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    pad_track = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(pad_track, "P_NAME", f"{track_name}_EtherealPad", True)
    
    # Add Synth and Reverb for "dreamlike" atmosphere
    RPR.RPR_TrackFX_AddByName(pad_track, "ReaSynth", False, -1)
    reverb_idx = RPR.RPR_TrackFX_AddByName(pad_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(pad_track, reverb_idx, 0, 0.8) # Wet mix high
    RPR.RPR_TrackFX_SetParam(pad_track, reverb_idx, 1, 0.9) # Room size large
    RPR.RPR_SetMediaTrackInfo_Value(pad_track, "D_VOL", 0.5) # Lower track volume
    
    pad_notes = []
    # Base octave for pads
    pad_base = 48 + root_val 
    
    # Create overlapping chords (min7 or maj7 depending on scale)
    # The tutorial explicitly mentions letting pads overlap into the next chord
    for b in range(bars):
        offset = b * 4
        # Chord 1 (Root chord) - spans 4.5 beats to overlap into the next bar
        overlap_dur = 4.5 
        
        chord_root = pad_base
        chord_third = pad_base + scale_intervals[2]
        chord_fifth = pad_base + scale_intervals[4]
        chord_seventh = pad_base + scale_intervals[6]
        
        # Alternate between the i chord and the iv or VI chord for movement
        if b % 2 != 0:
            chord_root = pad_base + scale_intervals[3] # 4th degree
            chord_third = chord_root + (scale_intervals[5] - scale_intervals[3])
            chord_fifth = chord_root + (scale_intervals[0] + 12 - scale_intervals[3])
            chord_seventh = chord_root + (scale_intervals[2] + 12 - scale_intervals[3])
            
        pad_notes.append((offset, overlap_dur, chord_root, velocity_base - 30))
        pad_notes.append((offset, overlap_dur, chord_third, velocity_base - 30))
        pad_notes.append((offset, overlap_dur, chord_fifth, velocity_base - 30))
        pad_notes.append((offset, overlap_dur, chord_seventh, velocity_base - 30))

    insert_midi_item_with_notes(pad_track, "Ethereal Pad", pad_notes, is_pad=True)

    return f"Created Jungle Scaffold (Break, Bass, Pads) across 3 tracks for {bars} bars at {bpm} BPM in {key} {scale}."
