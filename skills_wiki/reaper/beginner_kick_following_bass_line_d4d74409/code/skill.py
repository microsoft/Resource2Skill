import reaper_python as RPR
import random

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Beginner Bass",
    bpm: int = 120,
    key: str = "C", # Root note (C, C#, D, ..., B)
    scale: str = "minor", # Not directly used for simple root-following, but good for context
    bars: int = 4,
    velocity_base: int = 110, # Adjusted from 127 as per tutorial suggestion
    bass_octave: int = 2, # Common bass starting octave (e.g., C2 is MIDI 36)
    note_length_factor: float = 0.9, # Multiplier for note duration (0.1 for very short, 1.0 for full sustain)
    octave_variation_chance: float = 0.25, # Probability (0.0-1.0) for a note to be placed an octave higher
    **kwargs,
) -> str:
    """
    Create a beginner bass line in the current REAPER project, primarily following kick drum hits.
    Mimics the basic programming techniques shown in the tutorial: kick-following rhythm,
    velocity adjustment, note length control, and octave variations.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        bass_octave: The octave for the root bass note (e.g., 2 for C2, 1 for C1).
        note_length_factor: Multiplier for note duration (0.1 for very short, 1.0 for full sustain).
        octave_variation_chance: Probability (0.0-1.0) for a note to be placed an octave higher.
        **kwargs: Additional overrides for parameters.

    Returns:
        Status string, e.g., "Created 'Beginner Bass' with 24 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Ensure key is valid
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}"

    # Use kwargs to override default parameters if provided
    velocity_base = kwargs.get('velocity_base', velocity_base)
    bass_octave = kwargs.get('bass_octave', bass_octave)
    note_length_factor = kwargs.get('note_length_factor', note_length_factor)
    octave_variation_chance = kwargs.get('octave_variation_chance', octave_variation_chance)

    # Validate parameters
    velocity_base = max(0, min(127, int(velocity_base)))
    bass_octave = max(-2, min(8, int(bass_octave))) # Reasonable octave range
    note_length_factor = max(0.1, min(1.0, float(note_length_factor)))
    octave_variation_chance = max(0.0, min(1.0, float(octave_variation_chance)))

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add ReaSynth for a Basic Bass Sound ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    
    fx_idx = RPR.RPR_TrackFX_GetFXByName(track, "ReaSynth", False)
    if fx_idx != -1:
        # Oscillator 1: Saw wave
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 1.0) # param 0: Osc 1 Waveform (0=sine, 1=saw, 2=pulse)
        
        # Filter: Lowpass, cutoff ~200-300Hz, resonance low
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 13, 0.0) # param 13: Filter Mode (0=LP, 1=BP, 2=HP)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 14, 0.25) # param 14: Filter Cutoff (0.0-1.0, approx 200-300Hz)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 15, 0.1) # param 15: Filter Resonance (0.0-1.0)
        
        # Amp Envelope (ADSR): basic bass setup
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 16, 0.0) # param 16: Attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 17, 0.2) # param 17: Decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 18, 0.8) # param 18: Sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 19, 0.2) # param 19: Release
        
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 12, 0.5) # param 12: Volume (reduce to avoid clipping)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4 # Assuming 4/4 time signature
    quarter_note_time = 60.0 / bpm
    bar_length_time = quarter_note_time * beats_per_bar
    item_length = bar_length_time * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    # Place item at current cursor position
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", RPR.RPR_GetCursorPosition())
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_GetMediaItemTake(item, 0) # Get first take
    
    # Initialize MIDI take
    RPR.RPR_MIDI_SetItemExtents(take, 0.0, item_length)
    RPR.RPR_MIDI_SetPPQPos_ProjTime(take, 0.0, RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION"))
    RPR.RPR_MIDI_DisableSort(take) # Performance optimization for bulk MIDI writes

    root_midi_note = NOTE_MAP[key] + (bass_octave * 12)
    notes_inserted = 0

    # Simple 1-bar kick-following pattern derived from video analysis
    # Rhythmic pattern in beats relative to start of bar:
    # Kick at 1/1 (quarter), 1.5 (eighth), 2.0 (eighth), 3/1 (quarter), 3.5 (eighth), 4.0 (eighth)
    rhythmic_pattern_beats = [
        (0.0, 1.0), # Beat 1, duration 1 quarter note
        (1.0, 0.5), # Beat 1.5, duration 1 eighth note
        (1.5, 0.5), # Beat 2, duration 1 eighth note
        (2.0, 1.0), # Beat 3, duration 1 quarter note
        (3.0, 0.5), # Beat 3.5, duration 1 eighth note
        (3.5, 0.5), # Beat 4, duration 1 eighth note
    ]
    
    for bar_offset in range(bars):
        for beat_pos_in_bar, duration_in_beats in rhythmic_pattern_beats:
            # Calculate absolute start time in seconds
            start_time_sec = (bar_offset * bar_length_time) + (beat_pos_in_bar * quarter_note_time)
            
            # Adjust note duration based on factor
            note_dur_beats = duration_in_beats * note_length_factor
            # Ensure a minimum duration for audibility and editing
            if note_dur_beats < 0.05: note_dur_beats = 0.05
            
            length_sec = note_dur_beats * quarter_note_time
            
            current_midi_note = root_midi_note
            if random.random() < octave_variation_chance:
                current_midi_note += 12 # Shift up an octave

            # Insert MIDI note (take, selected, muted, start_time, end_time, channel, pitch, velocity)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_time_sec, start_time_sec + length_sec, 0, current_midi_note, velocity_base, True)
            notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_MIDI_MarkAllNotes(take, False)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_inserted} notes over {bars} bars at {bpm} BPM"

