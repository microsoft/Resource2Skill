import reaper_python as RPR
import random

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
CHORD_INTERVALS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "dom7": [0, 4, 7, 10],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
    "add9": [0, 4, 7, 14], # 14 is 9th (octave + 2nd)
}

def get_midi_pitch(root_note_midi: int, scale_index: int, scale_intervals: list, octave_offset: int = 0) -> int:
    """
    Calculates MIDI pitch from a root, scale degree index, and octave offset.
    The scale_index can extend beyond the length of scale_intervals to indicate higher octaves.
    """
    if not scale_intervals:
        return root_note_midi + (octave_offset * 12) 
    
    # Calculate base pitch in the root's octave by wrapping scale_index
    interval_value = scale_intervals[scale_index % len(scale_intervals)]
    
    # Adjust for octaves from the scale index wrap-around and explicit offset
    octave_from_interval_wrap = (scale_index // len(scale_intervals)) * 12
    
    return root_note_midi + interval_value + octave_from_interval_wrap + (octave_offset * 12)

def create_moving_bassline_groove(
    project_name: str = "MyProject",
    track_name_bass: str = "Groovy Bass",
    track_name_slap: str = "Slap Bass",
    track_name_chords: str = "Chord Ghosts",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    humanize_amount: float = 0.02, # Max +/- beat offset for humanization
    **kwargs,
) -> str:
    """
    Creates a moving bassline with slap elements and chord ghost notes,
    inspired by the "Moving Basslines" tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name_bass: Name for the main bass track.
        track_name_slap: Name for the slap bass track.
        track_name_chords: Name for the chord ghost notes track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        humanize_amount: Max +/- beat offset for humanization.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """

    # --- Input Validation and Setup ---
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Must be one of {list(SCALES.keys())}"

    root_midi_base = NOTE_MAP[key] + 60 # Default key root to C4 (MIDI 60) for consistency
    current_scale_intervals = SCALES[scale]
    
    # Define a common chord progression (e.g., I-V-vi-IV) based on the input scale
    if scale == "major":
        chord_progression_info = [ # (scale_degree_index_for_root, chord_type_string)
            (0, "major"), # I
            (4, "major"), # V
            (5, "minor"), # vi
            (3, "major"), # IV
        ]
    elif scale == "minor": # Common natural minor progression: i-VII-VI-v (can adjust V to major for harmonic minor)
        chord_progression_info = [
            (0, "minor"), # i
            (6, "major"), # VII
            (5, "major"), # VI
            (4, "minor"), # v
        ]
    else: # Fallback for other scales: use major triads at common scale degrees
        chord_progression_info = [
            (0, "major"), # I
            (4, "major"), # V
            (5, "major"), # vi
            (3, "major"), # IV
        ]

    # Translate scale degree indices into actual MIDI root notes for the chord progression
    chord_progression = []
    for deg_idx, c_type in chord_progression_info:
        midi_root = get_midi_pitch(root_midi_base, deg_idx, current_scale_intervals, 0)
        chord_progression.append((midi_root, c_type))

    # --- REAPER API Calls ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm

    created_info = []

    # --- 1. Create Track for Chord Ghost Notes ---
    track_idx_chords = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_chords, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx_chords)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", track_name_chords, True)
    RPR.RPR_SetMediaTrackInfo_Value(track_chords, "I_SHOWMIDIONLYINLINER", 1.0) # Show MIDI editor ghost notes
    RPR.RPR_SetTrackColor(track_chords, RPR.ColorToNative(0, 100, 200) | 0x1000000) # Blue color

    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", bars * beats_per_bar * seconds_per_beat)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)
    
    fx_idx_chord = RPR.RPR_TakeFX_AddByName(take_chords, "ReaSynth", False, -1)
    if fx_idx_chord != -1: # ReaSynth for a subtle pad sound for ghost notes
        RPR.RPR_TakeFX_SetParam(take_chords, fx_idx_chord, 13, 0.2) # Attack
        RPR.RPR_TakeFX_SetParam(take_chords, fx_idx_chord, 14, 0.8) # Decay
        RPR.RPR_TakeFX_SetParam(take_chords, fx_idx_chord, 15, 0.6) # Sustain
        RPR.RPR_TakeFX_SetParam(take_chords, fx_idx_chord, 16, 0.5) # Release
        RPR.RPR_TakeFX_SetParam(take_chords, fx_idx_chord, 0, 0.5) # Osc 1 Waveform (Triangle)

    midi_take_chords = RPR.RPR_MIDI_GetTake(take_chords)
    if not midi_take_chords: return "Error creating MIDI take for chords"
    
    chord_notes_count = 0
    for bar_idx in range(bars):
        chord_root_midi, chord_type = chord_progression[bar_idx % len(chord_progression)]
        chord_intervals = CHORD_INTERVALS.get(chord_type, CHORD_INTERVALS["major"])
        
        # Insert chord notes (usually C3/C4 range, one octave below the root_midi_base C4)
        chord_start_beat = bar_idx * beats_per_bar
        chord_duration_beats = beats_per_bar # Whole bar chord
        for interval in chord_intervals:
            pitch = chord_root_midi + interval - 12 # Place chords around C3 (MIDI 48)
            RPR.RPR_MIDI_InsertNote(midi_take_chords, False, False, chord_start_beat, chord_start_beat + chord_duration_beats, 0, True, pitch, velocity_base - 10, False)
            chord_notes_count += 1
    RPR.RPR_MIDI_Sort(midi_take_chords)
    RPR.RPR_MIDI_Commit(midi_take_chords)
    created_info.append(f"'{track_name_chords}' with {chord_notes_count} notes")


    # --- 2. Create Track for Main Bassline ---
    track_idx_bass = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_bass, True)
    track_bass = RPR.RPR_GetTrack(0, track_idx_bass)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", track_name_bass, True)
    RPR.RPR_SetTrackColor(track_bass, RPR.ColorToNative(150, 200, 50) | 0x1000000) # Green color

    fx_idx_bass = RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    if fx_idx_bass == -1: return "Error adding ReaSynth to bass track"
    
    # Set up ReaSynth for a basic warm bass (saw wave, low filter)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 0, 2.0) # Osc 1 Waveform: Saw
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 1, 0.0) # Osc 2 Waveform: Sine (off)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 4, 1.0) # Osc 1 Level
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 13, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 14, 0.4) # Decay
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 15, 0.7) # Sustain
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 16, 0.2) # Release
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 22, 0.1) # Filter Cutoff (low)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 23, 0.05) # Filter Resonance (low)
    RPR.RPR_TrackFX_SetParam(track_bass, fx_idx_bass, 24, 0.05) # Filter Env Amt (low)

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", bars * beats_per_bar * seconds_per_beat)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)
    midi_take_bass = RPR.RPR_MIDI_GetTake(take_bass)
    if not midi_take_bass: return "Error creating MIDI take for bass"

    bass_notes_count = 0
    # Bass pattern for one bar: combination of root and passing notes to create movement
    bass_pattern_relative_to_chord = [
        (0.0,  0.5, 0),   # Root (1/4 note) on beat 1
        (0.5,  0.25, 1),  # 2nd (1/8 note) on 1.5
        (0.75, 0.25, 0),  # Root (1/8 note) on 1.75
        (1.0,  0.5, 2),   # 3rd (1/4 note) on beat 2
        (1.5,  0.25, 4),  # 5th (1/8 note) on 2.5
        (1.75, 0.25, 3),  # 4th (1/8 note) on 2.75
        (2.0,  0.5, 2),   # 3rd (1/4 note) on beat 3
        (2.5,  0.25, 1),  # 2nd (1/8 note) on 3.5
        (2.75, 0.25, 0),  # Root (1/8 note) on 3.75
        (3.0,  0.5, 4),   # 5th (1/4 note) on beat 4
        (3.5,  0.5, 0),   # Root (1/4 note), leads to next bar on 4.5
    ]
    
    for bar_idx in range(bars):
        chord_root_midi, _ = chord_progression[bar_idx % len(chord_progression)]
        bass_root_midi_for_this_bar = chord_root_midi - 24 # Bass plays 2 octaves below chord root (e.g. C2 = MIDI 36)
        
        for beat_offset, duration, scale_degree_index in bass_pattern_relative_to_chord:
            note_start_beat = (bar_idx * beats_per_bar) + beat_offset
            pitch = get_midi_pitch(bass_root_midi_for_this_bar, scale_degree_index, current_scale_intervals)
            
            # Clamp pitch to a typical bass range (e.g., MIDI 24-50, G0 to F3)
            pitch = max(24, min(50, pitch)) 
            
            RPR.RPR_MIDI_InsertNote(midi_take_bass, False, False, note_start_beat, note_start_beat + duration, 0, True, pitch, velocity_base, False)
            bass_notes_count += 1
            
    RPR.RPR_MIDI_Sort(midi_take_bass)
    RPR.RPR_MIDI_Commit(midi_take_bass)
    created_info.append(f"'{track_name_bass}' with {bass_notes_count} notes")


    # --- 3. Create Track for Slap Bass ---
    track_idx_slap = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_slap, True)
    track_slap = RPR.RPR_GetTrack(0, track_idx_slap)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", track_name_slap, True)
    RPR.RPR_SetTrackColor(track_slap, RPR.ColorToNative(255, 150, 0) | 0x1000000) # Orange color

    fx_idx_slap = RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    if fx_idx_slap == -1: return "Error adding ReaSynth to slap track"
    
    # Set up ReaSynth for a percussive slap (square wave, short envelope, brighter filter)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 0, 3.0) # Osc 1 Waveform: Square
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 1, 0.0) # Osc 2 Waveform: Sine (off)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 4, 1.0) # Osc 1 Level
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 13, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 14, 0.08) # Decay (short)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 15, 0.0) # Sustain (off)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 16, 0.01) # Release (very short)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 22, 0.7) # Filter Cutoff (brighter)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 23, 0.3) # Filter Resonance (some twang)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_idx_slap, 24, 0.6) # Filter Env Amt (more snap)

    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", bars * beats_per_bar * seconds_per_beat)
    take_slap = RPR.RPR_AddTakeToMediaItem(item_slap)
    midi_take_slap = RPR.RPR_MIDI_GetTake(take_slap)
    if not midi_take_slap: return "Error creating MIDI take for slap bass"

    slap_notes_count = 0
    slap_note_duration_beats = 0.125 # Very short, 16th note
    for bar_idx in range(bars):
        chord_root_midi, _ = chord_progression[bar_idx % len(chord_progression)]
        slap_root_midi_for_this_bar = chord_root_midi # Slap often uses the same root as the main bass, but higher

        # Slap pattern: syncopated off-beats, higher octave
        slap_bar_pattern = [
            (0.5, 0, slap_note_duration_beats, 1), # Root +1 octave, after beat 1
            (1.5, 2, slap_note_duration_beats, 1), # 3rd +1 octave, after beat 2
            (2.5, 4, slap_note_duration_beats, 1), # 5th +1 octave, after beat 3
            (3.5, 0, slap_note_duration_beats, 1)  # Root +1 octave, after beat 4
        ]
        
        for beat_offset, scale_degree_index, duration, octave_shift in slap_bar_pattern:
            note_start_beat = (bar_idx * beats_per_bar) + beat_offset
            pitch = get_midi_pitch(slap_root_midi_for_this_bar, scale_degree_index, current_scale_intervals, octave_shift)
            
            # Clamp slap pitch to a higher range (e.g., MIDI 60-80, C4 to G5)
            pitch = max(60, min(80, pitch)) 
            
            RPR.RPR_MIDI_InsertNote(midi_take_slap, False, False, note_start_beat, note_start_beat + duration, 0, True, pitch, velocity_base + 15, False)
            slap_notes_count += 1
            
    RPR.RPR_MIDI_Sort(midi_take_slap)
    RPR.RPR_MIDI_Commit(midi_take_slap)
    created_info.append(f"'{track_name_slap}' with {slap_notes_count} notes")

    # --- 4. Humanization (Velocity and Timing) ---
    # Humanize main bass notes
    num_bass_notes_ptr = RPR.new_intp()
    RPR.RPR_MIDI_CountEvts(midi_take_bass, RPR.new_intp(), num_bass_notes_ptr, RPR.new_intp(), RPR.new_intp())
    num_bass_notes_val = num_bass_notes_ptr[0]
    for i in range(num_bass_notes_val):
        _, _, mute, start_beat, end_beat, chan, vel, pitch = RPR.RPR_MIDI_GetNote(midi_take_bass, i)
        
        new_vel = int(max(1, min(127, vel + random.randint(int(-velocity_base*0.1), int(velocity_base*0.1)))))
        timing_offset = random.uniform(-humanize_amount, humanize_amount)
        new_start_beat = start_beat + timing_offset
        new_end_beat = end_beat + timing_offset
        
        RPR.RPR_MIDI_SetNote(midi_take_bass, i, False, mute, new_start_beat, new_end_beat, chan, new_vel, pitch, False)
    RPR.RPR_MIDI_Commit(midi_take_bass)
    
    # Humanize slap bass notes
    num_slap_notes_ptr = RPR.new_intp()
    RPR.RPR_MIDI_CountEvts(midi_take_slap, RPR.new_intp(), num_slap_notes_ptr, RPR.new_intp(), RPR.new_intp())
    num_slap_notes_val = num_slap_notes_ptr[0]
    for i in range(num_slap_notes_val):
        _, _, mute, start_beat, end_beat, chan, vel, pitch = RPR.RPR_MIDI_GetNote(midi_take_slap, i)
        
        # More velocity variation for slap, slightly less timing deviation for perceived tightness
        new_vel = int(max(1, min(127, vel + random.randint(int(-velocity_base*0.15), int(velocity_base*0.15))))) 
        timing_offset = random.uniform(-humanize_amount*0.5, humanize_amount*0.5) 
        new_start_beat = start_beat + timing_offset
        new_end_beat = end_beat + timing_offset
        
        RPR.RPR_MIDI_SetNote(midi_take_slap, i, False, mute, new_start_beat, new_end_beat, chan, new_vel, pitch, False)
    RPR.RPR_MIDI_Commit(midi_take_slap)

    return f"Created base lines: {', '.join(created_info)} over {bars} bars at {bpm} BPM."

