def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Epic Arrangement",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part Epic Rock/Synthwave arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    key_val = NOTE_MAP.get(key.capitalize(), 11) # Default to B

    # Define progressions based on scale
    if scale.lower() == "major":
        # Epic Major Progression: I - vi - IV - V
        chords = [
            [0, 4, 7],     # I (Root + 0, Major)
            [9, 12, 16],   # vi (Root + 9, Minor)
            [5, 9, 12],    # IV (Root + 5, Major)
            [7, 11, 14]    # V (Root + 7, Major)
        ]
    else:
        # Epic Minor Progression (From Video): i - VI - VII - v
        chords = [
            [0, 3, 7],     # i (Root + 0, Minor)
            [8, 12, 15],   # VI (Root + 8, Major)
            [10, 14, 17],  # VII (Root + 10, Major)
            [7, 10, 14]    # v (Root + 7, Minor)
        ]

    # Helper to convert RGB to REAPER native color
    def color_to_native(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    # Helper to add a note to a take
    def add_note(take, start_qn, end_qn, pitch, vel=100):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Helper to create a track with a MIDI item
    def setup_track(name, r, g, b, add_synth=True):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetTrackColor(track, color_to_native(r, g, b))
        
        if add_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", (60.0 / bpm) * 4 * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    tr_drums, tk_drums = setup_track(f"{track_name} - Drums", 75, 0, 130, add_synth=False)
    tr_bass, tk_bass   = setup_track(f"{track_name} - Bass", 128, 0, 128)
    tr_rhythm, tk_rhy  = setup_track(f"{track_name} - Rhythm", 255, 128, 0)
    tr_lead, tk_lead   = setup_track(f"{track_name} - Lead Arp", 255, 215, 0)

    # === Step 3: Populate MIDI Data ===
    for bar in range(bars):
        bar_qn = bar * 4  # 4 quarter notes per bar in 4/4
        chord = chords[bar % len(chords)]
        
        # --- Drums ---
        # Kick (36) on 1, 2-AND, 3
        add_note(tk_drums, bar_qn + 0.0, bar_qn + 0.25, 36, 110)
        add_note(tk_drums, bar_qn + 1.5, bar_qn + 1.75, 36, 100)
        add_note(tk_drums, bar_qn + 2.0, bar_qn + 2.25, 36, 110)
        
        # Snare (38) on 2 and 4
        add_note(tk_drums, bar_qn + 1.0, bar_qn + 1.25, 38, 115)
        add_note(tk_drums, bar_qn + 3.0, bar_qn + 3.25, 38, 115)
        
        # Hi-hat (42) straight 8ths
        for i in range(8):
            add_note(tk_drums, bar_qn + i*0.5, bar_qn + i*0.5 + 0.25, 42, 85 if i%2==0 else 70)
            
        # Crash (49) on the downbeat of bar 1 and every 4th bar
        if bar % 4 == 0:
            add_note(tk_drums, bar_qn, bar_qn + 0.5, 49, 120)

        # --- Bass ---
        # Driving 8th notes on the Root of the current chord
        root_note = key_val + 24 + chord[0] # Octave 2
        for i in range(8):
            add_note(tk_bass, bar_qn + i*0.5, bar_qn + i*0.5 + 0.45, root_note, 105)

        # --- Rhythm Guitar / Pads ---
        # Sustained whole notes for the triad
        for note in chord:
            pitch = key_val + 48 + note # Octave 4
            add_note(tk_rhy, bar_qn, bar_qn + 4.0, pitch, 90)

        # --- Lead Arp ---
        # Sweeping 8th note arpeggio: Root, 3rd, 5th, Octave, 5th, 3rd, Root, Lower 5th
        arp_intervals = [
            chord[0],          # Root
            chord[1],          # 3rd
            chord[2],          # 5th
            chord[0] + 12,     # Octave
            chord[2],          # 5th
            chord[1],          # 3rd
            chord[0],          # Root
            chord[2] - 12      # Lower 5th
        ]
        
        for i, interval in enumerate(arp_intervals):
            pitch = key_val + 60 + interval # Octave 5
            # Add dynamic velocity slope to the arpeggio
            vel = 80 + (i if i <= 3 else 7 - i) * 6 
            add_note(tk_lead, bar_qn + i*0.5, bar_qn + i*0.5 + 0.45, pitch, vel)

    # === Step 4: Finalize MIDI Data ===
    RPR.RPR_MIDI_Sort(tk_drums)
    RPR.RPR_MIDI_Sort(tk_bass)
    RPR.RPR_MIDI_Sort(tk_rhy)
    RPR.RPR_MIDI_Sort(tk_lead)

    return f"Created Epic 4-Track Arrangement '{track_name}' in {key} {scale} over {bars} bars at {bpm} BPM"
