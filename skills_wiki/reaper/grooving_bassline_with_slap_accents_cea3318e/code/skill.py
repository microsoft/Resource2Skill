import reaper_python as RPR
import random
import math

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


def get_midi_note(key: str, octave: int, scale_degree: int, scale: str) -> int:
    """
    Calculates the MIDI note number for a given key, octave, scale degree, and scale.
    """
    root_midi = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    if not scale_intervals:
        RPR.RPR_ShowConsoleMsg(f"Warning: Scale '{scale}' not found. Using major scale.\n")
        scale_intervals = SCALES["major"]

    # Ensure scale_degree is within the bounds of the scale, handling octaves
    octave_offset = scale_degree // len(scale_intervals)
    degree_in_scale = scale_degree % len(scale_intervals)
    
    interval = scale_intervals[degree_in_scale]
    midi_note = root_midi + (octave + octave_offset) * 12 + interval
    return midi_note


def create_grooving_bassline_with_slap(
    project_name: str = "MyProject",
    track_name: str = "Grooving Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    slap_velocity_boost: int = 30,
    humanize_timing: float = 0.005, # Max +/- seconds offset
    humanize_velocity: int = 15, # Max +/- velocity offset
    bass_octave: int = 2,
    slap_octave_offset: int = 1, # Slap note is 1 octave higher than main bass
    **kwargs,
) -> str:
    """
    Create a grooving bassline with slap accents in the current REAPER project,
    mimicking the techniques from the tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for main bass notes.
        slap_velocity_boost: Additional velocity for slap notes.
        humanize_timing: Max absolute timing offset in seconds.
        humanize_velocity: Max absolute velocity offset.
        bass_octave: MIDI octave for the main bassline (e.g., 2 for C2).
        slap_octave_offset: Octave difference for slap notes relative to main bass.
        **kwargs: Additional overrides (not used in this simplified version).

    Returns:
        Status string, e.g., "Created 'Grooving Bass' with X notes over 4 bars at 120 BPM"
    """

    # === Step 1: Set Tempo ===
    # Set the project BPM for accurate timing calculations.
    RPR.RPR_SetCurrentBPM(0, float(bpm), False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth + ReaEQ + ReaComp) ===
    # ReaSynth for a basic bass sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Basic ReaSynth patch: Sawtooth wave, adjust attack/decay for bass
    # Parameter IDs are determined empirically for ReaSynth, may vary slightly but these are common.
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.5) # Osc1 Wave: Sawtooth (0.0=Sine, 0.25=Square, 0.5=Saw, 0.75=Triangle)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5) # Osc1 Octave (0.5 is 0, 0 is -1, 1 is +1) -> default
    RPR.RPR_TrackFX_SetParam(track, 0, 11, 0.7) # Mix (Osc1/Osc2 balance, biased towards Osc1)
    
    # Filter for bass sound: low cutoff, some resonance
    RPR.RPR_TrackFX_SetParam(track, 0, 12, 0.25) # Filter Cutoff (lower for bass, 0-1 range)
    RPR.RPR_TrackFX_SetParam(track, 0, 13, 0.2) # Filter Resonance (0-1 range)
    RPR.RPR_TrackFX_SetParam(track, 0, 15, 0.5) # Filter Velocity (make it respond to velocity)

    # Amplifier Envelope for bass: moderate attack, decay, sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 16, 0.1) # Amp Attack (short but not too clicky)
    RPR.RPR_TrackFX_SetParam(track, 0, 17, 0.4) # Amp Decay (medium)
    RPR.RPR_TrackFX_SetParam(track, 0, 18, 0.7) # Amp Sustain (good sustain)
    RPR.RPR_TrackFX_SetParam(track, 0, 19, 0.3) # Amp Release (short)


    # ReaEQ for shaping
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: Low Shelf Boost (for bass warmth)
    RPR.RPR_TrackFX_SetParam(track, 1, 1, 1.0) # Band 1 On (0=off, 1=on)
    RPR.RPR_TrackFX_SetParam(track, 1, 2, 0.0) # Band 1 Type (0=LowShelf)
    RPR.RPR_TrackFX_SetParam(track, 1, 3, 60.0/20000.0) # Band 1 Freq (60 Hz, normalized 0-1)
    RPR.RPR_TrackFX_SetParam(track, 1, 4, 0.6) # Band 1 Gain (+6 dB, normalized 0-1 where 0.5 is 0dB)
    # Band 2: Mid Cut (to clear mud)
    RPR.RPR_TrackFX_SetParam(track, 1, 5, 1.0) # Band 2 On (0=off, 1=on)
    RPR.RPR_TrackFX_SetParam(track, 1, 6, 2.0/6.0) # Band 2 Type (2=Band)
    RPR.RPR_TrackFX_SetParam(track, 1, 7, 300.0/20000.0) # Band 2 Freq (300 Hz)
    RPR.RPR_TrackFX_SetParam(track, 1, 8, 0.4) # Band 2 Gain (-6 dB, normalized 0-1)

    # ReaComp for punch
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, 2, 0, 0.05) # Pre-comp (short)
    RPR.RPR_TrackFX_SetParam(track, 2, 1, 0.3)  # Attack (medium-fast)
    RPR.RPR_TrackFX_SetParam(track, 2, 2, 0.2)  # Release (medium-fast)
    RPR.RPR_TrackFX_SetParam(track, 2, 3, 0.4)  # Ratio (4:1, normalized 0-1 for 1:1 to 20:1)
    RPR.RPR_TrackFX_SetParam(track, 2, 4, 0.6)  # Threshold (-10 dB, normalized 0-1 for -60dB to 0dB)
    RPR.RPR_TrackFX_SetParam(track, 2, 10, 0.6) # Auto Gain (on, to compensate for compression)


    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", seconds_per_beat * beats_per_bar * bars)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, seconds_per_beat * beats_per_bar * bars)
    
    midi_take = RPR.RPR_MIDI_GetTake(take)
    if not midi_take:
        RPR.RPR_ShowConsoleMsg("Failed to get MIDI take. Ensure a valid take was created.\n")
        return f"Error creating MIDI item for '{track_name}'."
    
    RPR.RPR_MIDI_DisableGridSnap(midi_take) # Disable grid snap for humanization
    RPR.RPR_MIDI_BeginEdit(midi_take)
    
    notes_inserted = 0
    
    # Example chord progression roots (scale degrees for Cm - Ab - Bb - Cm in C minor scale)
    # C minor scale degrees: C(0), D(2), Eb(3), F(5), G(7), Ab(8), Bb(10)
    chord_roots_degrees = [0, 8, 10, 0] 
    
    # Define a grooving pattern using 16th notes
    # (relative_16th_onset, duration_16th, relative_scale_degree_from_root, note_type, velocity_mod_factor)
    # `relative_scale_degree_from_root`: 0=root, 3=minor third, 5=perfect fifth, 10=minor seventh, etc.
    # `note_type`: 'main_bass', 'passing_note', 'slap'

    # This pattern provides a basic loop demonstrating the concepts for one bar,
    # which is then adapted for the chord progression.
    base_bar_pattern = [
        # Pattern for 1 bar (16 x 16th notes)
        # Beat 1: Root (main, long)
        (0,  4, 0, 'main_bass', 1.0), 
        # Beat 1.5: Passing note (minor third from root)
        (6,  2, 3, 'passing_note', 0.8), 
        # Beat 2: Fifth (main)
        (8,  3, 5, 'main_bass', 0.9), 
        # Beat 2.75: Slap (octave above root, very short)
        (11, 1, 0, 'slap', 0.2), # relative_scale_degree 0 here means root, get_midi_note will add octave offset
        # Beat 3: Root (main, long)
        (12, 4, 0, 'main_bass', 1.0), 
        # Beat 4: Fifth (main, shorter for movement into next bar)
        (16-3, 3, 5, 'main_bass', 0.8), # End of bar 4th beat, leading into next
    ]

    for bar in range(bars):
        current_bar_start_time = bar * beats_per_bar * seconds_per_beat
        
        # Get the root scale degree for the current bar's chord
        current_root_scale_degree = chord_roots_degrees[bar % len(chord_roots_degrees)]

        for note_data in base_bar_pattern:
            start_16th, duration_16th, relative_scale_degree, note_type, note_length_factor = note_data
            
            # Calculate actual timing
            start_time = current_bar_start_time + start_16th * (seconds_per_beat / 4.0)
            end_time = start_time + duration_16th * (seconds_per_beat / 4.0) * note_length_factor

            # Apply humanization
            start_time += random.uniform(-humanize_timing, humanize_timing)
            # Ensure note does not start before current bar's beginning for first note in bar
            if start_16th == 0:
                 start_time = max(current_bar_start_time, start_time)
            
            # Calculate pitch
            final_midi_octave = bass_octave
            if note_type == 'slap':
                # Slap notes are an octave higher than the current bar's root
                final_midi_octave = bass_octave + slap_octave_offset
                # The relative_scale_degree for slap notes is interpreted as the root of the slap itself
                midi_note = get_midi_note(key, final_midi_octave, current_root_scale_degree + relative_scale_degree, scale)
            else:
                # Main bass and passing notes use the base_octave, relative to the current bar's root
                midi_note = get_midi_note(key, final_midi_octave, current_root_scale_degree + relative_scale_degree, scale)
            
            # Calculate velocity
            vel = velocity_base
            if note_type == 'slap':
                vel = min(127, velocity_base + slap_velocity_boost)
            
            vel += random.randint(-humanize_velocity, humanize_velocity)
            vel = max(1, min(127, vel)) # Clamp velocity to MIDI range

            # Insert note
            start_beat = start_time / seconds_per_beat
            end_beat = end_time / seconds_per_beat
            
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, start_beat, end_beat, 0, midi_note, vel, False)
            notes_inserted += 1

    RPR.RPR_MIDI_EndEdit(midi_take)
    RPR.RPR_UpdateArrange() # Refresh the arrange view to show the new item/notes

    return f"Created '{track_name}' with {notes_inserted} notes over {bars} bars at {bpm} BPM"
