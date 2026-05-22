def create_pattern(
    project_name: str = "KanyeStyleGroove",
    track_name: str = "Distorted_Groove",
    bpm: int = 88,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Kanye-style distorted monotone groove with offset looping.
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

    # Helper function to insert MIDI notes
    def insert_note(take, start_time, duration, pitch, vel=100):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    quarter_note = 60.0 / bpm
    eighth_note = quarter_note / 2.0
    sixteenth_note = quarter_note / 4.0
    bar_length = quarter_note * 4
    total_length = bar_length * bars

    root_pitch = NOTE_MAP.get(key.capitalize(), 4)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Octave offsets
    bass_octave = 36 # C2 range
    melody_octave = 60 # C4 range
    
    notes_created = 0

    # ==========================================
    # TRACK 1: Monotone Distorted Bass
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name}_MonoBass", True)
    
    # FX: ReaSynth + JS Saturation
    bass_synth = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 0, 0.5) # Square mix
    RPR.RPR_TrackFX_SetParam(bass_track, bass_synth, 1, 0.5) # Saw mix
    
    bass_dist = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Saturation", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, bass_dist, 0, 100.0) # 100% Amount for extreme drive

    # MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    
    bass_pitch = bass_octave + root_pitch

    for bar in range(bars):
        bar_start = bar * bar_length
        # Syncopated monotone pattern
        insert_note(bass_take, bar_start, quarter_note, bass_pitch, velocity_base)
        insert_note(bass_take, bar_start + quarter_note + eighth_note, eighth_note, bass_pitch, velocity_base - 10)
        insert_note(bass_take, bar_start + (quarter_note * 2) + sixteenth_note, eighth_note, bass_pitch, velocity_base)
        insert_note(bass_take, bar_start + (quarter_note * 3), eighth_note, bass_pitch, velocity_base - 15)
        notes_created += 4

    RPR.RPR_MIDI_Sort(bass_take)

    # ==========================================
    # TRACK 2: Zero-Tail Abrasive Percussion
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    perc_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(perc_track, "P_NAME", f"{track_name}_AbrasivePerc", True)
    
    # FX: ReaSynth (Noise) + JS Distortion
    perc_synth = RPR.RPR_TrackFX_AddByName(perc_track, "ReaSynth", False, -1)
    # Zero out standard oscillators
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 0, 0.0) # Square
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 1, 0.0) # Saw
    # Max noise
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 4, 1.0) # Noise mix
    # ADSR for "Zero Tail"
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 6, 0.0) # Attack = 0
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 7, 0.1) # Decay = short
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 8, 0.0) # Sustain = 0
    RPR.RPR_TrackFX_SetParam(perc_track, perc_synth, 9, 0.0) # Release = 0
    
    perc_dist = RPR.RPR_TrackFX_AddByName(perc_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(perc_track, perc_dist, 0, 15.0) # Heavy Gain
    
    perc_item = RPR.RPR_AddMediaItemToTrack(perc_track)
    RPR.RPR_SetMediaItemInfo_Value(perc_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(perc_item, "D_LENGTH", total_length)
    perc_take = RPR.RPR_AddTakeToMediaItem(perc_item)

    for bar in range(bars):
        bar_start = bar * bar_length
        # Upfront percussive hits on 2 and 4, plus syncopations
        insert_note(perc_take, bar_start + quarter_note, sixteenth_note, 60, velocity_base)
        insert_note(perc_take, bar_start + quarter_note + eighth_note + sixteenth_note, sixteenth_note, 60, velocity_base - 20)
        insert_note(perc_take, bar_start + (quarter_note * 3), sixteenth_note, 60, velocity_base)
        notes_created += 3

    RPR.RPR_MIDI_Sort(perc_take)

    # ==========================================
    # TRACK 3: "Hiding the Seam" Offset Loop
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    loop_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(loop_track, "P_NAME", f"{track_name}_OffsetChops", True)
    
    loop_synth = RPR.RPR_TrackFX_AddByName(loop_track, "ReaSynth", False, -1)
    
    loop_item = RPR.RPR_AddMediaItemToTrack(loop_track)
    RPR.RPR_SetMediaItemInfo_Value(loop_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(loop_item, "D_LENGTH", total_length)
    loop_take = RPR.RPR_AddTakeToMediaItem(loop_item)

    # Simple 3-chop sequence representing a sample
    chop_1_pitch = melody_octave + root_pitch
    chop_2_pitch = melody_octave + root_pitch + scale_intervals[2] # 3rd degree
    chop_3_pitch = melody_octave + root_pitch + scale_intervals[4] # 5th degree

    for bar in range(bars):
        bar_start = bar * bar_length
        
        # Chop 1 & 2 are consistent
        insert_note(loop_take, bar_start, quarter_note, chop_1_pitch, velocity_base - 10)
        insert_note(loop_take, bar_start + quarter_note, quarter_note, chop_2_pitch, velocity_base - 15)
        
        # "Hiding the Seam" Logic:
        if bar == bars - 1:
            # On the final bar, shift the 3rd chop later by an 8th note to break the predictability
            offset = eighth_note
            insert_note(loop_take, bar_start + (quarter_note * 2) + offset, quarter_note, chop_3_pitch, velocity_base)
        else:
            # Normal placement for standard bars
            insert_note(loop_take, bar_start + (quarter_note * 2), quarter_note, chop_3_pitch, velocity_base)
            
        notes_created += 3

    RPR.RPR_MIDI_Sort(loop_take)

    return f"Created {track_name} groove with {notes_created} notes across 3 tracks (Mono Bass, Zero-Tail Perc, Offset Chops) over {bars} bars at {bpm} BPM."
