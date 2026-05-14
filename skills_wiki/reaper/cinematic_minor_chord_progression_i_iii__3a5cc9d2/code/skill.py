def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Cinematic Minor Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a dramatic i - III - VI - V minor chord progression on a new track.
    Replicates the custom chord sequence demonstrated in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, D#, F).
        scale: Ignored internally as this specifically builds a minor progression.
        bars: Number of bars to generate (progression loops every 2 bars).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
    """
    import reaper_python as RPR

    # Base note mappings (Octave 3)
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}

    root_note = NOTE_MAP.get(key.upper(), 48)

    # Chord structure definitions (intervals from chord root)
    minor_triad = [0, 3, 7]
    major_triad = [0, 4, 7]

    # The i - III - VI - V Progression (Relative to Key Root)
    # Voicings are adjusted (offsets) to keep the chords close together on the keyboard
    progression = [
        {"name": "i",   "offset": 0,  "intervals": minor_triad}, # e.g., Cm  (C3, Eb3, G3)
        {"name": "III", "offset": 3,  "intervals": major_triad}, # e.g., Eb  (Eb3, G3, Bb3)
        {"name": "VI",  "offset": -4, "intervals": major_triad}, # e.g., Ab  (Ab2, C3, Eb3)
        {"name": "V",   "offset": -5, "intervals": major_triad}  # e.g., G   (G2, B2, D3)
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes ===
    beats_per_chord = 2.0  # Half note chords
    total_beats = bars * beats_per_bar
    total_chords = int(total_beats // beats_per_chord)

    notes_created = 0
    for c in range(total_chords):
        chord_data = progression[c % 4] # Loop the 4 chords
        
        start_qn = c * beats_per_chord
        end_qn = start_qn + beats_per_chord
        
        # Convert Quarter Notes to PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        # Add a tiny gap between chords for articulation
        end_ppq -= 20 
        
        for interval in chord_data["intervals"]:
            pitch = root_note + chord_data["offset"] + interval
            # Ensure pitch stays in valid MIDI range
            pitch = max(0, min(127, pitch)) 
            
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Synth & Reverb) ===
    # Add a basic synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume slightly to prevent clipping on block chords
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 0, 0.4) 

    # Add Reverb for cinematic space
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 0, 0.3) # Wet signal
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 1, 0.9) # Dry signal
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 2, 0.7) # Room size

    return f"Created '{track_name}' with {notes_created} notes (i-III-VI-V progression) over {bars} bars at {bpm} BPM in {key} minor."
