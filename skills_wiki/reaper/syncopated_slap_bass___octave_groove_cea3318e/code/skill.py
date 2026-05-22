def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Slap Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Syncopated Slap Bass groove in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (90-115 recommended for this groove).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (e.g., minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # === Music Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Base octave for a bassline (MIDI note 24 is C1)
    BASE_OCTAVE = 1
    root_pitch = NOTE_MAP.get(key, 4) + (BASE_OCTAVE * 12)
    octave_pitch = root_pitch + 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Define the Slap Groove Pattern ===
    # Each dictionary represents a note. 
    # pos_16th = Position in 16th notes (0.0 to 15.0 per bar)
    # len_16th = Length in 16th notes (e.g., 0.5 is a 32nd note for a sharp slap)
    # is_slap = Boolean. True = Octave up, shorter, louder.
    # is_ghost = Boolean. True = Softer rhythm filler.
    groove_pattern = [
        {"pos_16th": 0.0,  "len_16th": 1.0, "is_slap": False, "is_ghost": False},
        {"pos_16th": 1.5,  "len_16th": 0.5, "is_slap": False, "is_ghost": True},  # Ghost on "e"
        {"pos_16th": 2.5,  "len_16th": 1.0, "is_slap": False, "is_ghost": False}, # Syncopation
        {"pos_16th": 4.0,  "len_16th": 1.5, "is_slap": False, "is_ghost": False}, # Beat 2
        {"pos_16th": 7.0,  "len_16th": 0.5, "is_slap": True,  "is_ghost": False}, # Slap on "a"
        {"pos_16th": 8.5,  "len_16th": 0.5, "is_slap": False, "is_ghost": True},  # Ghost on "e" of 3
        {"pos_16th": 10.0, "len_16th": 0.5, "is_slap": True,  "is_ghost": False}, # Slap on "&" of 3
        {"pos_16th": 12.0, "len_16th": 1.0, "is_slap": False, "is_ghost": False}, # Beat 4
        {"pos_16th": 14.0, "len_16th": 0.5, "is_slap": True,  "is_ghost": False}, # Slap on "&" of 4
        {"pos_16th": 15.0, "len_16th": 0.5, "is_slap": False, "is_ghost": True},  # Ghost on "a" of 4
    ]

    # Standard REAPER MIDI PPQ is 960 per quarter note. 16th note = 240 PPQ.
    PPQ_PER_16TH = 240
    TOTAL_BARS = bars
    notes_created = 0

    # Humanization limits
    MAX_TIMING_OFFSET = 15  # Ticks
    MAX_VELOCITY_OFFSET = 7 # Velocity points

    for bar in range(TOTAL_BARS):
        bar_start_ppq = bar * 16 * PPQ_PER_16TH
        
        for note in groove_pattern:
            # Determine base parameters
            is_slap = note["is_slap"]
            is_ghost = note["is_ghost"]
            
            # Pitch
            pitch = octave_pitch if is_slap else root_pitch
            
            # Velocity mapping based on note type
            if is_slap:
                base_vel = min(127, velocity_base + 20)
            elif is_ghost:
                base_vel = max(10, velocity_base - 35)
            else:
                base_vel = velocity_base
                
            # Apply Humanization (Velocity)
            vel = base_vel + random.randint(-MAX_VELOCITY_OFFSET, MAX_VELOCITY_OFFSET)
            vel = max(1, min(127, vel))
            
            # Apply Humanization (Timing Offset)
            timing_offset = random.randint(-MAX_TIMING_OFFSET, MAX_TIMING_OFFSET)
            # Ensure the first note of the item doesn't fall before 0
            if bar == 0 and note["pos_16th"] == 0:
                timing_offset = max(0, timing_offset)
                
            start_ppq = int(bar_start_ppq + (note["pos_16th"] * PPQ_PER_16TH) + timing_offset)
            end_ppq = int(start_ppq + (note["len_16th"] * PPQ_PER_16TH))
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            notes_created += 1

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain for Bass Tone ===
    # Add native synth and EQ to approximate the bass sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # We leave ReaSynth at defaults which has a fairly sharp attack natively.
    # A complete VSTi instrument (like Trilian) would normally be loaded here for production-ready slaps.

    return f"Created '{track_name}' with {notes_created} humanized slap bass notes over {bars} bars at {bpm} BPM in {key} {scale}."
