def create_pattern(
    project_name: str = "Pharrell_Groove",
    track_name: str = "Neptunes_Style",
    bpm: int = 96,
    key: str = "F",
    scale: str = "pentatonic_minor",
    bars: int = 2,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates a Pharrell/Neptunes-style inverted groove featuring repitched melodic percussion, 
    staccato rhythmic guitars, and sparse ear-candy placement.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (forces multiples of 2 for the loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    if scale not in SCALES:
        scale = "pentatonic_minor"
    
    root_val = NOTE_MAP.get(key.capitalize(), 5) # Default F
    scale_intervals = SCALES[scale]

    # Ensure bars is a multiple of 2 to allow the "sparse" event to happen at the end of the phrase
    bars = max(2, bars + (bars % 2))

    # Helper function to get midi pitch from scale degree
    def get_pitch(octave, degree):
        degree = degree % len(scale_intervals)
        octave_offset = (degree // len(scale_intervals)) * 12
        return (octave * 12) + root_val + scale_intervals[degree] + octave_offset

    # Helper function to add notes
    def add_midi_note(take, start_qn, duration_qn, pitch, vel):
        start_time = start_qn * (60.0 / bpm)
        end_time = (start_qn + duration_qn) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_count = RPR.RPR_CountTracks(0)

    # === Track 1: Melodic Percussion (Bass) ===
    # Represents repitched toms/claves acting as the bass groove
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    trk_perc = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_perc, "P_NAME", f"{track_name}_MelodicPerc", True)
    
    # Add ReaSynth (Sine wave to act as a subby tom)
    fx_perc = RPR.RPR_TrackFX_AddByName(trk_perc, "ReaSynth", False, -1)
    # Set to fast decay to make it percussive
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 1, 0.0)  # Square mix 0
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 2, 0.0)  # Saw mix 0
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 4, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 5, 0.1)  # Decay
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 6, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 7, 0.1)  # Release

    item_perc = RPR.RPR_AddMediaItemToTrack(trk_perc)
    RPR.RPR_SetMediaItemInfo_Value(item_perc, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_perc, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_perc = RPR.RPR_AddTakeToMediaItem(item_perc)

    # === Track 2: Dry Rhythmic "Guitar" ===
    # Very short, staccato off-beat syncopations
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    trk_gtr = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_gtr, "P_NAME", f"{track_name}_RhythmicGtr", True)
    RPR.RPR_SetMediaTrackInfo_Value(trk_gtr, "D_PAN", -0.5) # Pan Left for width
    
    fx_gtr = RPR.RPR_TrackFX_AddByName(trk_gtr, "ReaSynth", False, -1)
    # Saw wave, no sustain, mimicking a muted guitar pluck
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 1, 0.0)  # Square mix 0
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 2, 0.8)  # Saw mix up
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 4, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 5, 0.05) # Very short decay
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 6, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 7, 0.05) # Release

    item_gtr = RPR.RPR_AddMediaItemToTrack(trk_gtr)
    RPR.RPR_SetMediaItemInfo_Value(item_gtr, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_gtr, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_gtr = RPR.RPR_AddTakeToMediaItem(item_gtr)

    # === Track 3: Sparse Ear Candy ===
    # A distinct sound that hits only once per loop
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    trk_candy = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_candy, "P_NAME", f"{track_name}_EarCandy", True)
    RPR.RPR_SetMediaTrackInfo_Value(trk_candy, "D_PAN", 0.5) # Pan Right
    
    fx_candy = RPR.RPR_TrackFX_AddByName(trk_candy, "ReaSynth", False, -1)
    # Square wave for a distinct, synthetic contrast to the other sounds
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 1, 0.8)  # Square mix
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 2, 0.0)  # Saw mix
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 3, 0.2)  # Extra tuning for a bell-like feel

    item_candy = RPR.RPR_AddMediaItemToTrack(trk_candy)
    RPR.RPR_SetMediaItemInfo_Value(item_candy, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_candy, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_candy = RPR.RPR_AddTakeToMediaItem(item_candy)

    # === MIDI Generation Loop ===
    note_count = 0
    for b in range(0, bars, 2): # Iterate in 2-bar chunks
        bar_qn = b * 4
        
        # -- Melodic Percussion Groove (Bass, Octave 2 & 3) --
        # Syncopated 16th note pattern
        add_midi_note(take_perc, bar_qn + 0.00, 0.2, get_pitch(2, 0), velocity_base)      # Beat 1 (Root)
        add_midi_note(take_perc, bar_qn + 0.75, 0.2, get_pitch(2, 1), velocity_base - 10) # Beat 1.75 (m3)
        add_midi_note(take_perc, bar_qn + 1.50, 0.2, get_pitch(2, 2), velocity_base - 15) # Beat 2.5 (4th)
        add_midi_note(take_perc, bar_qn + 3.00, 0.2, get_pitch(2, 3), velocity_base)      # Beat 4 (5th)
        
        add_midi_note(take_perc, bar_qn + 4.00, 0.2, get_pitch(2, 0), velocity_base)      # Bar 2, Beat 1
        add_midi_note(take_perc, bar_qn + 5.25, 0.2, get_pitch(2, 4), velocity_base - 10) # Bar 2, Beat 2.25 (m7)
        add_midi_note(take_perc, bar_qn + 6.50, 0.2, get_pitch(3, 0), velocity_base)      # Bar 2, Beat 3.5 (Root + octave)
        note_count += 7

        # -- Rhythmic Guitar Groove (Octave 4) --
        # Extremely dry, staccato, 2-note bursts acting like percussion
        add_midi_note(take_gtr, bar_qn + 1.25, 0.1, get_pitch(4, 0), velocity_base - 5)   # Beat 2.25 (e)
        add_midi_note(take_gtr, bar_qn + 1.50, 0.1, get_pitch(4, 0), velocity_base - 5)   # Beat 2.5  (&)
        
        add_midi_note(take_gtr, bar_qn + 5.25, 0.1, get_pitch(4, 0), velocity_base - 5)   # Bar 2, Beat 2.25
        add_midi_note(take_gtr, bar_qn + 5.50, 0.1, get_pitch(4, 0), velocity_base - 5)   # Bar 2, Beat 2.5
        add_midi_note(take_gtr, bar_qn + 7.50, 0.1, get_pitch(4, 0), velocity_base - 10)  # Bar 2, Beat 4.5
        note_count += 5

        # -- Sparse Ear Candy (Octave 6) --
        # Only happens ONCE at the very end of the 2-bar phrase
        add_midi_note(take_candy, bar_qn + 7.75, 0.25, get_pitch(6, 4), velocity_base + 10) # Bar 2, Beat 4.75
        note_count += 1

    RPR.RPR_MIDI_Sort(take_perc)
    RPR.RPR_MIDI_Sort(take_gtr)
    RPR.RPR_MIDI_Sort(take_candy)
    RPR.RPR_UpdateArrange()

    return f"Created Pharrell-style arrangement: 3 tracks ('{track_name}'), {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
