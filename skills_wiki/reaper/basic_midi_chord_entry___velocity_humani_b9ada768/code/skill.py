import random
import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a foundational MIDI chord progression with velocity humanization.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
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
    }

    # Fallback to major if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_pitch_class = NOTE_MAP.get(key.upper(), 0)
    
    # Base octave (C3 = 48)
    base_octave = 48
    root_note = base_octave + root_pitch_class

    # Calculate the full diatonic scale over a couple of octaves
    diatonic_notes = []
    for oct_offset in [0, 12, 24]:
        for interval in scale_intervals:
            diatonic_notes.append(root_note + oct_offset + interval)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Chords & Humanize ===
    # Common progression (I - vi - IV - V or similar sequence based on available scale degrees)
    # Using scale degree indices (0-indexed)
    progression_degrees = [0, 5, 3, 4] if len(scale_intervals) >= 6 else [0, 0, 0, 0]
    
    notes_added = 0
    for bar in range(bars):
        # Repeat progression if bars > len(progression)
        degree_idx = progression_degrees[bar % len(progression_degrees)]
        
        # Build a basic triad + octave voicing
        # e.g., root, 3rd, 5th, octave
        chord_indices = [degree_idx, degree_idx + 2, degree_idx + 4, degree_idx + 7]
        
        start_sec = bar * bar_length_sec
        # Leave a tiny gap between chords
        end_sec = start_sec + bar_length_sec - 0.05 

        for idx in chord_indices:
            # Ensure we don't index out of bounds
            if idx < len(diatonic_notes):
                pitch = diatonic_notes[idx]
                
                # Humanization: randomize velocity (mimicking the CC editing in tutorial)
                # Keep root notes slightly louder, inner voices softer
                vol_offset = random.randint(-15, 5)
                # If it's the 3rd or 5th, make it slightly softer
                if idx in [degree_idx + 2, degree_idx + 4]:
                    vol_offset -= 10
                    
                vel = max(1, min(127, velocity_base + vol_offset))
                
                # Humanization: randomize timing slightly (strum effect)
                timing_offset_sec = random.uniform(0.0, 0.02)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + timing_offset_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                
                # Insert note
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)
                notes_added += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (ReaSynth) ===
    # To hear the result without external VSTs, use ReaSynth
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a softer, more pad/piano-like envelope
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.05) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.5)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} humanized MIDI notes over {bars} bars at {bpm} BPM in {key} {scale}."
