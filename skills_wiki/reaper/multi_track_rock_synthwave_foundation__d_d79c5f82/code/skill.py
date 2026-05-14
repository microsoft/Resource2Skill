def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Band_Foundation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Rock/Synthwave arrangement (Drums, Bass, Rhythm, Lead).
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    # Setup base pitch and scale
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_pitch(degree, octave):
        """Convert a scale degree (0-indexed) to an absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[scale_idx] + (octave + octave_shift) * 12

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    total_length_sec = bar_sec * bars
    
    # i - VI - III - VII progression (relative scale degrees)
    progression = [0, 5, 2, 4] 

    def create_layer(name, add_synth=True, color=0):
        """Helper to create a track and a blank MIDI take."""
        track_idx = RPR.RPR_GetNumTracks()
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        if add_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        return take
        
    def add_note(take, start_beat, duration_beats, pitch, vel, chan=0):
        start_time = start_beat * beat_sec
        end_time = (start_beat + duration_beats) * beat_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        # take, selected, muted, startppq, endppq, chan, pitch, vel, noSort
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    # --- 1. DRUMS LAYER ---
    take_drums = create_layer("Drums", add_synth=False)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Crash on first bar
        if bar == 0:
            add_note(take_drums, bar_start_beat, 1.0, 49, velocity_base + 10, chan=9)
            
        # Kick (1 and 3) & Snare (2 and 4)
        for beat in range(4):
            if beat % 2 == 0: # Beats 1, 3 (0-indexed 0, 2)
                add_note(take_drums, bar_start_beat + beat, 0.5, 36, velocity_base + 10, chan=9)
            else:             # Beats 2, 4 (0-indexed 1, 3)
                add_note(take_drums, bar_start_beat + beat, 0.5, 38, velocity_base + 5, chan=9)
                
        # 8th Note Hi-Hats
        for eighth in range(8):
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 20 # Accent downbeats
            add_note(take_drums, bar_start_beat + (eighth * 0.5), 0.25, 42, vel, chan=9)
            
    RPR.RPR_MIDI_Sort(take_drums)

    # --- 2. BASS LAYER ---
    take_bass = create_layer("Bass", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        bass_pitch = get_pitch(chord_root, 2) # Octave 2
        
        # 8th note driving pulses
        for eighth in range(8):
            add_note(take_bass, bar_start_beat + (eighth * 0.5), 0.45, bass_pitch, velocity_base)
            
    RPR.RPR_MIDI_Sort(take_bass)

    # --- 3. RHYTHM LAYER (Chords) ---
    take_rhythm = create_layer("Rhythm", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        
        # Triad degrees (Root, 3rd, 5th)
        chord_degrees = [chord_root, chord_root + 2, chord_root + 4]
        for deg in chord_degrees:
            pitch = get_pitch(deg, 4) # Octave 4
            add_note(take_rhythm, bar_start_beat, 3.9, pitch, velocity_base - 15)
            
    RPR.RPR_MIDI_Sort(take_rhythm)

    # --- 4. LEAD LAYER (Arpeggios) ---
    take_lead = create_layer("Lead", add_synth=True)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        chord_root = progression[bar % len(progression)]
        
        # Arpeggio pattern (Root, 3rd, 5th, Octave)
        arp_degrees = [chord_root, chord_root + 2, chord_root + 4, chord_root + 7]
        
        # 16th note arpeggiator
        for sixteenth in range(16):
            deg = arp_degrees[sixteenth % 4]
            pitch = get_pitch(deg, 5) # Octave 5
            add_note(take_lead, bar_start_beat + (sixteenth * 0.25), 0.2, pitch, velocity_base - 5)

    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track Foundation ({bars} bars) at {bpm} BPM in {key} {scale}."
