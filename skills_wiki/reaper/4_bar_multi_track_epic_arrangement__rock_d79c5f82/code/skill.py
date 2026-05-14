def create_pattern(
    project_name: str = "EpicArrangement",
    track_name: str = "Arrangement", # Used as a prefix
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Bar Multi-Track Epic Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Prefix for the created tracks (e.g. 'Arrangement_Bass').
        bpm: Tempo in BPM.
        key: Root note (e.g., 'B').
        scale: Scale type (forces the epic minor progression relative to the key).
        bars: Number of bars to generate (will loop the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave C3 = 48
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 11) # Default to B if not found

    # Progression: i - VI - III - VII (Relative to minor root)
    # Stored as semitone offsets from the root note to form the triads
    progression_intervals = [
        [0, 3, 7],     # i (Minor)
        [8, 12, 15],   # VI (Major built on minor 6th)
        [3, 7, 10],    # III (Major built on minor 3rd)
        [10, 14, 17]   # VII (Major built on minor 7th)
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Helper Functions ---
    def create_track(name, vol_db, use_synth=True):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 10**(vol_db/20.0))
        if use_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return track

    def create_midi_take(track, total_bars):
        item_length_sec = total_bars * 4.0 * (60.0 / bpm)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        return RPR.RPR_GetActiveTake(item)

    def add_note(take, start_qn, end_qn, pitch, vel):
        start_time = start_qn * (60.0 / bpm)
        end_time = end_qn * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- 1. Drums Track ---
    trk_drums = create_track("Drums", -6.0, use_synth=False)
    take_drums = create_midi_take(trk_drums, bars)
    
    for b in range(bars):
        bar_start_qn = b * 4.0
        # Kick (36) and Snare (38)
        for beat in range(4):
            if beat % 2 == 0: # Beats 1 & 3
                add_note(take_drums, bar_start_qn + beat, bar_start_qn + beat + 0.25, 36, velocity_base + 10)
            else:             # Beats 2 & 4
                add_note(take_drums, bar_start_qn + beat, bar_start_qn + beat + 0.25, 38, velocity_base + 10)
        
        # 8th note Hi-hats (42)
        for eighth in range(8):
            add_note(take_drums, bar_start_qn + (eighth * 0.5), bar_start_qn + (eighth * 0.5) + 0.25, 42, velocity_base - 10)
            
        # Crash (49) on downbeat of every 4th bar
        if b % 4 == 0:
            add_note(take_drums, bar_start_qn, bar_start_qn + 1.0, 49, velocity_base + 15)

    RPR.RPR_MIDI_Sort(take_drums)

    # --- 2. Bass Track ---
    trk_bass = create_track("Bass", -6.0)
    take_bass = create_midi_take(trk_bass, bars)
    
    for b in range(bars):
        bar_start_qn = b * 4.0
        chord_ivs = progression_intervals[b % 4]
        bass_pitch = root_midi + chord_ivs[0] - 24 # Down 2 octaves
        
        # Driving 8th notes
        for eighth in range(8):
            add_note(take_bass, bar_start_qn + (eighth * 0.5), bar_start_qn + (eighth * 0.5) + 0.4, bass_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(take_bass)

    # --- 3. Rhythm Chords Track ---
    trk_rhythm = create_track("Rhythm", -12.0)
    take_rhythm = create_midi_take(trk_rhythm, bars)
    
    for b in range(bars):
        bar_start_qn = b * 4.0
        chord_ivs = progression_intervals[b % 4]
        
        # Sustained whole notes for the chord triad
        for iv in chord_ivs:
            chord_pitch = root_midi + iv - 12 # Down 1 octave
            add_note(take_rhythm, bar_start_qn, bar_start_qn + 4.0, chord_pitch, velocity_base - 15)

    RPR.RPR_MIDI_Sort(take_rhythm)

    # --- 4. Lead Arpeggio Track ---
    trk_lead = create_track("Lead", -10.0)
    take_lead = create_midi_take(trk_lead, bars)
    
    for b in range(bars):
        bar_start_qn = b * 4.0
        chord_ivs = progression_intervals[b % 4]
        
        # Arpeggio pattern traversing chord tones: 5th -> 3rd -> Root -> 3rd
        arp_pattern = [2, 1, 0, 1, 2, 1, 0, 1] 
        
        for eighth in range(8):
            note_idx = arp_pattern[eighth]
            lead_pitch = root_midi + chord_ivs[note_idx] + 12 # Up 1 octave
            add_note(take_lead, bar_start_qn + (eighth * 0.5), bar_start_qn + (eighth * 0.5) + 0.4, lead_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track arrangement ('{track_name}') with Drums, Bass, Rhythm, and Lead over {bars} bars at {bpm} BPM in {key} minor."
