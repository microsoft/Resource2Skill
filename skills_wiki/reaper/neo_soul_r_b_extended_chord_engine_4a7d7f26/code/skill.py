def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Rhodes",
    bpm: int = 85,
    key: str = "Eb",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul / R&B extended chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and pattern.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Rhodes Emulation) ===
    # 3.1 ReaSynth for the electric piano tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)   # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.8)   # Triangle mix (Main Rhodes body)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.3)   # Extra sine (Warmth)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.02)  # Soft Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.6)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.4)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.8)   # Long Release
    
    # 3.2 JS: Tremolo for Suitcase stereo panning vibe
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 0, 2.5)    # Frequency (Hz)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 1, -12.0)  # Amount (dB)

    # 3.3 ReaVerbate for space
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.15)   # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 1.0)    # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.5)    # Room Size

    # === Step 4: Music Theory & Voicing Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    tonic_pitch = NOTE_MAP.get(key.capitalize(), 0) + 36 # C2 Base octave
    
    # Define Progression based on scale (2-bar loop)
    progression = []
    if scale.lower() in ["major", "mixolydian", "pentatonic_major"]:
        # ii9 - V13 - Imaj9 - vi11
        progression = [
            {"root_offset": 2, "voicing": [0, 15, 19, 22, 26]},  # ii9
            {"root_offset": 7, "voicing": [0, 10, 16, 21, 26]},  # V13
            {"root_offset": 0, "voicing": [0, 14, 19, 23, 26]},  # Imaj9
            {"root_offset": 9, "voicing": [0, 15, 19, 22, 29]},  # vi11
        ]
    else:
        # Minor Context: i9 - iv9 - v7b9 - bVImaj9
        progression = [
            {"root_offset": 0, "voicing": [0, 15, 19, 22, 26]},  # i9
            {"root_offset": 5, "voicing": [0, 15, 19, 22, 26]},  # iv9
            {"root_offset": 7, "voicing": [0, 16, 19, 22, 25]},  # v7b9
            {"root_offset": 8, "voicing": [0, 14, 19, 23, 26]},  # bVImaj9
        ]

    # === Step 5: Create MIDI Item ===
    beats_per_bar = 4
    item_length_qn = bars * beats_per_bar
    item_length_sec = (60.0 / bpm) * item_length_qn
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 6: Insert Syncopated Chord Events ===
    note_count = 0
    
    # Loop over the requested number of bars
    for bar in range(bars):
        qn_offset = bar * 4.0
        
        # Decide which two chords to play based on even/odd bar
        if bar % 2 == 0:
            chords_to_play = [
                (progression[0], qn_offset + 0.0, 2.25),  # Downbeat, holds into beat 3
                (progression[1], qn_offset + 2.5, 1.25)   # Pushed on "and" of 3
            ]
        else:
            chords_to_play = [
                (progression[2], qn_offset + 0.0, 2.25),
                (progression[3], qn_offset + 2.5, 1.25)
            ]
            
        for chord_data, start_qn, length_qn in chords_to_play:
            root_note = tonic_pitch + chord_data["root_offset"]
            
            # Insert each note in the chord stack
            for i, interval in enumerate(chord_data["voicing"]):
                pitch = root_note + interval
                if pitch > 127: pitch = 127
                
                # Humanize velocity (accents the top melody note slightly)
                vel_shift = random.randint(-12, 5)
                if i == len(chord_data["voicing"]) - 1:
                    vel_shift += 10 # Emphasize top extension
                vel = max(1, min(127, velocity_base + vel_shift))
                
                # Strum effect (15ms delay per note upward)
                strum_offset_qn = i * 0.02
                note_start_qn = start_qn + strum_offset_qn
                note_end_qn = note_start_qn + length_qn - 0.1 # Slight gap before next chord
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_end_qn)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} lush extended notes over {bars} bars at {bpm} BPM in {key} {scale}."
