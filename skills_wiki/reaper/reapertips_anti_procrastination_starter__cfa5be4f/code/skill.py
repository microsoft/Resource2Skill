def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Template_Generated",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Reapertips-style Anti-Procrastination Starter Template.
    Generates a color-coded track layout and a starter rhythmic foundation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (unused here, uses strict layout names).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) for the bass pulse.
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate for the foundation loop.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory & Input Mapping ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_offset = NOTE_MAP.get(key.capitalize(), 0)
    kick_pitch = 36 # Standard GM Kick
    bass_pitch = 36 + root_offset # Root note in bass octave

    # REAPER Custom Color Helper (BGR + OS Flag)
    def make_color(r, g, b):
        return (r + (g << 8) + (b << 16)) | 0x1000000

    # Layout matches the tutorial's screen at 02:18
    layout_config = [
        {"name": "Drums", "color": make_color(200, 50, 50), "is_midi": True},
        {"name": "GTRs CLN", "color": make_color(50, 200, 200), "is_midi": False},
        {"name": "GTRs RHY", "color": make_color(200, 50, 200), "is_midi": False},
        {"name": "BASS", "color": make_color(50, 50, 200), "is_midi": True},
        {"name": "VOX", "color": make_color(200, 150, 50), "is_midi": False},
        {"name": "FX", "color": make_color(100, 100, 100), "is_midi": False}
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    start_idx = RPR.RPR_CountTracks(0)
    created_tracks = []

    # === Step 2: Build Track Layout & Colors ===
    for i, t_info in enumerate(layout_config):
        idx = start_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Set Name and Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])
        created_tracks.append(track)

    # === Step 3: Populate Foundation Groove ===
    # A) Drums (Track 0 in our new array)
    drum_track = created_tracks[0]
    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drum_track, 0.0, total_length_sec, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)
    
    # 4-on-the-floor kick
    for b in range(bars * beats_per_bar):
        start_ppq = b * 960
        end_ppq = start_ppq + 240 # 16th note duration
        RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, kick_pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(drum_take)

    # B) Bass (Track 3 in our new array)
    bass_track = created_tracks[3]
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1) # Audibility
    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_track, 0.0, total_length_sec, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)

    # 1/8th note driving bass pulse
    for b in range(bars * beats_per_bar * 2):
        start_ppq = b * 480
        end_ppq = start_ppq + 400 # Slightly staccato to keep it punchy
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base - 15, False)
    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created {len(layout_config)} color-coded starter tracks with a {bars}-bar {key} foundation groove at {bpm} BPM."
