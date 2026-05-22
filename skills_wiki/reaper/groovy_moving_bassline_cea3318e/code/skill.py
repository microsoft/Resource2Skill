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

def get_midi_note(root_key_str: str, scale_degree_idx: int, octave: int, scale_name: str = "major") -> int:
    """
    Calculates the MIDI note number for a given root, scale degree, and octave.
    scale_degree_idx is 0-indexed (0=root, 1=2nd, 2=3rd, etc. within the scale).
    Octave is standard MIDI numbering (e.g., C2 is MIDI note 36, C4 is 60).
    """
    root_midi = NOTE_MAP.get(root_key_str.upper())
    if root_midi is None:
        raise ValueError(f"Invalid root key: {root_key_str}")
    
    scale_intervals = SCALES.get(scale_name.lower())
    if scale_intervals is None:
        raise ValueError(f"Invalid scale name: {scale_name}")
        
    # Calculate the octave shift based on how many full scale cycles scale_degree_idx covers
    octave_shift_from_degree = (scale_degree_idx // len(scale_intervals)) * 12
    # Get the interval from the root within the current octave of the scale
    interval_from_root_within_octave = scale_intervals[scale_degree_idx % len(scale_intervals)]
    
    # MIDI note number: C0 = 12, C1 = 24, C2 = 36, C3 = 48, C4 = 60
    # Our `octave` parameter directly corresponds to the C-octave number (e.g., C2 means octave 2).
    # MIDI note 12 is C0. So, for octave `n`, the base MIDI note for C is `(n+1)*12`.
    midi_note = (octave + 1) * 12 + root_midi + interval_from_root_within_octave + octave_shift_from_degree
    
    # Ensure note is within valid MIDI range
    return min(127, max(0, midi_note))

def create_moving_bassline(
    project_name: str = "MyProject",
    track_name: str = "Groovy Bassline",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a moving bassline inspired by the tutorial, featuring rhythmic variation,
    steps, octave jumps, and subtle humanization.
    The bassline follows a I-IV-V-I chord progression within the specified key and scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this skill but for future expansion).

    Returns:
        Status string, e.g., "Created 'Groovy Bassline' with N notes over 4 bars at 120 BPM"
    """
    RPR.Undo_BeginBlock2(0) # Begin undo block
    
    # === Step 1: Set Tempo (if different from current project) ===
    # RPR.RPR_SetCurrentBPM(0, bpm, False) # This changes global project BPM, so it's commented out by default.
                                          # Use RPR_TimeMap_GetMeasuresAndBeatInfo and RPR_TimeMap_SetMeasureInfo 
                                          # for local tempo changes or if user intends global change.

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Configure ReaSynth for Bass Sound ===
    RPR.TrackFX_AddByName(track, "ReaSynth", False, -1)
    fx_idx = RPR.TrackFX_GetByName(track, "ReaSynth", False)
    if fx_idx != -1:
        # Oscillators: slightly detuned saws/squares for a richer bass tone
        RPR.TrackFX_SetParam(track, fx_idx, 0, 0.4)   # Waveform: between saw (0.25) and square (0.5)
        RPR.TrackFX_SetParam(track, fx_idx, 17, 0.05) # OSC2 Semi (slight detune)
        RPR.TrackFX_SetParam(track, fx_idx, 19, 0.8)  # OSC2 Volume (mix in a good amount)

        # ADSR for a plucky/slapped sound (fast attack, short decay, low sustain, medium release)
        RPR.TrackFX_SetParam(track, fx_idx, 1, 0.05)  # Attack (0-1)
        RPR.TrackFX_SetParam(track, fx_idx, 2, 0.2)   # Decay (0-1)
        RPR.TrackFX_SetParam(track, fx_idx, 3, 0.3)   # Sustain (0-1)
        RPR.TrackFX_SetParam(track, fx_idx, 4, 0.2)   # Release (0-1)

        # Filter for bass (low cutoff, medium resonance)
        RPR.TrackFX_SetParam(track, fx_idx, 7, 0.4)   # Filter Cutoff (0-1)
        RPR.TrackFX_SetParam(track, fx_idx, 8, 0.3)   # Filter Resonance (0-1)
        RPR.TrackFX_SetParam(track, fx_idx, 12, 0.05) # Portamento time (for subtle slides between notes)

    # Add ReaEQ and ReaComp for basic processing (no specific parameters set, but good practice)
    RPR.TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.TrackFX_AddByName(track, "ReaComp", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    _, _, _, current_bpm, _ = RPR.RPR_TimeMap_GetMeasuresAndBeatInfo(0, 0) # Get current project BPM
    bar_length_sec = (60.0 / current_bpm) * beats_per_bar # Use project BPM for item length
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", RPR.Time_GetProjectTime()) # Start at current project time
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.MIDI_CreateEx(0)) # Create new empty MIDI source
    
    # Refresh MIDI editor if open to reflect new item/take
    RPR.MIDIEditor_OnCommand(RPR.MIDIEditor_GetActive(), 40058) # Refresh active MIDI editor

    # Chord progression (I-IV-V-I degrees relative to the key's scale root)
    # Example: In C Major scale (degrees 0-6): C(0), D(1), E(2), F(3), G(4), A(5), B(6)
    # I=0 (C), IV=3 (F), V=4 (G)
    chord_roots_relative_degree_idx = [0, 3, 4, 0] 

    notes_inserted_count = 0
    for bar_i in range(bars):
        current_chord_root_degree_idx = chord_roots_relative_degree_idx[bar_i % len(chord_roots_relative_degree_idx)]
        
        # Beat 1: Root note, longer, strong velocity
        start_time_beat = bar_i * beats_per_bar
        end_time_beat = start_time_beat + 0.75 # A bit less than a full beat (dotted 1/8th) for punch
        
        # Humanize velocity and timing
        vel = min(127, max(0, velocity_base + random.randint(-10, 10)))
        timing_offset = random.uniform(-0.02, 0.02) # +/- 20ms in beats
        note_pitch = get_midi_note(key, current_chord_root_degree_idx, 2, scale) # Root, Octave 2
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 1.5 (1/8th after beat 1): 5th of current chord, shorter
        start_time_beat = bar_i * beats_per_bar + 0.5
        end_time_beat = start_time_beat + 0.25 # 1/8th note duration
        note_pitch = get_midi_note(key, (current_chord_root_degree_idx + 4) % len(SCALES[scale]), 2, scale) # 5th degree
        vel = min(127, max(0, velocity_base - 10 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 2: 6th of current chord, shorter
        start_time_beat = bar_i * beats_per_bar + 1.0
        end_time_beat = start_time_beat + 0.25
        note_pitch = get_midi_note(key, (current_chord_root_degree_idx + 5) % len(SCALES[scale]), 2, scale) # 6th degree
        vel = min(127, max(0, velocity_base - 5 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1
        
        # Beat 2.5 (1/8th after beat 2): Higher octave 'slap' note, very short
        start_time_beat = bar_i * beats_per_bar + 1.5
        end_time_beat = start_time_beat + 0.125 # 1/16th note duration
        note_pitch = get_midi_note(key, current_chord_root_degree_idx, 3, scale) # Root, Octave 3 (for slap feel)
        vel = min(127, max(0, velocity_base + 15 + random.randint(-10, 10))) # Higher velocity for slap
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 3: 3rd of current chord, shorter
        start_time_beat = bar_i * beats_per_bar + 2.0
        end_time_beat = start_time_beat + 0.25
        note_pitch = get_midi_note(key, (current_chord_root_degree_idx + 2) % len(SCALES[scale]), 2, scale) # 3rd degree
        vel = min(127, max(0, velocity_base - 5 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 3.5 (1/8th after beat 3): 2nd of current chord, shorter
        start_time_beat = bar_i * beats_per_bar + 2.5
        end_time_beat = start_time_beat + 0.25
        note_pitch = get_midi_note(key, (current_chord_root_degree_idx + 1) % len(SCALES[scale]), 2, scale) # 2nd degree
        vel = min(127, max(0, velocity_base - 10 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 4: Root note, shorter
        start_time_beat = bar_i * beats_per_bar + 3.0
        end_time_beat = start_time_beat + 0.25
        note_pitch = get_midi_note(key, current_chord_root_degree_idx, 2, scale) # Root
        vel = min(127, max(0, velocity_base - 5 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1

        # Beat 4.5 (1/8th after beat 4): Passing tone leading to next bar's root
        start_time_beat = bar_i * beats_per_bar + 3.5
        end_time_beat = start_time_beat + 0.25
        
        next_chord_root_degree_idx = chord_roots_relative_degree_idx[(bar_i + 1) % len(chord_roots_relative_degree_idx)]
        next_root_midi = get_midi_note(key, next_chord_root_degree_idx, 2, scale)

        # For the passing note, let's target the note a scale degree below the next root
        passing_degree_idx = (next_chord_root_degree_idx - 1 + len(SCALES[scale])) % len(SCALES[scale])
        note_pitch = get_midi_note(key, passing_degree_idx, 2, scale)
        
        # Special case for the very last note to create a more conclusive ending or a downward jump
        if bar_i == bars - 1:
            note_pitch = get_midi_note(key, 4, 1, scale) # Play the 5th down an octave for a strong ending
            end_time_beat = start_time_beat + 0.5 # Make it a bit longer
            
        vel = min(127, max(0, velocity_base - 15 + random.randint(-5, 5)))
        timing_offset = random.uniform(-0.01, 0.01)
        RPR.MIDI_InsertNote(take, False, False, start_time_beat + timing_offset, end_time_beat + timing_offset, vel, note_pitch, True)
        notes_inserted_count += 1


    RPR.MIDI_Sort(take) # Sort notes after insertion for good measure
    RPR.MIDI_MarkAllNotes(take, True) # Select all notes
    RPR.MIDI_SetRecentNoteLooped(take) # Loop the notes within the item (useful for repeating patterns)

    RPR.UpdateArrange() # Refresh REAPER UI
    RPR.Undo_EndBlock2(0, f"Created '{track_name}'", -1) # End undo block

    return f"Created '{track_name}' with {notes_inserted_count} notes over {bars} bars at {current_bpm} BPM"

