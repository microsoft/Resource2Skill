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

def get_midi_note_from_scale_degree(key: str, scale_type: str, degree: int, octave: int = 3) -> int:
    """Returns the MIDI note for a specific scale degree in a given octave."""
    root_midi = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale_type, SCALES["major"])
    
    if not scale_intervals:
        return root_midi + (octave * 12) # Fallback to root if scale not found

    # Adjust degree to wrap around scale
    # degree 1 is the root, so (degree - 1)
    degree_in_scale = (degree - 1) % len(scale_intervals)
    octave_offset = (degree - 1) // len(scale_intervals)

    return root_midi + (octave * 12) + scale_intervals[degree_in_scale] + (octave_offset * 12)


def humanize_velocity(base_velocity: int, strength: float) -> int:
    """Applies random deviation to a velocity value within a given strength."""
    deviation = int((random.random() * 2 - 1) * 127 * strength)
    new_velocity = base_velocity + deviation
    return max(1, min(127, new_velocity)) # Keep velocity within 1-127 range

def humanize_timing(beat_pos: float, beat_unit_duration: float, strength: float) -> float:
    """Applies random timing offset based on beat duration to a given position."""
    # beat_unit_duration could be 1.0 for a quarter note, 0.5 for an 8th etc.
    deviation = (random.random() * 2 - 1) * beat_unit_duration * strength
    return beat_pos + deviation


def create_evolving_bassline_groove(
    project_name: str = "MyProject",
    track_name: str = "Evolving Bass",
    slap_track_name: str = "Bass Slaps",
    ghost_track_name: str = "Chord Progression (Ghost)",
    bpm: int = 120, # BPM is used for internal timing calculations if needed, but not to set global project BPM
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    humanize_strength: float = 0.05, # Max 5% timing/velocity deviation (0.0 to 1.0)
    **kwargs,
) -> str:
    """
    Creates an evolving bassline from root notes, adds rhythmic complexity, 
    passing tones, and incorporates distinct "slap" notes on separate tracks.
    Also applies humanization.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the main bass track.
        slap_track_name: Name for the bass slap accent track.
        ghost_track_name: Name for the ghost chord progression track.
        bpm: Tempo in BPM (used for internal rhythm calculation context).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        humanize_strength: Maximum percentage deviation for velocity and timing (0.0 to 1.0).
        **kwargs: Additional overrides (not used in this specific function but for future expansion).

    Returns:
        Status string describing what was created.
    """
    RPR.Undo_BeginBlock2(0) # Begin an undo block

    # === Step 1: Create Tracks ===
    track_count_start = RPR.RPR_CountTracks(0)
    
    # Main Bass Track
    RPR.RPR_InsertTrackAtIndex(track_count_start, True)
    main_bass_track = RPR.RPR_GetTrack(0, track_count_start)
    RPR.RPR_GetSetMediaTrackInfo_String(main_bass_track, "P_NAME", track_name, True)
    
    # Bass Slap Track
    RPR.RPR_InsertTrackAtIndex(track_count_start + 1, True)
    slap_bass_track = RPR.RPR_GetTrack(0, track_count_start + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(slap_bass_track, "P_NAME", slap_track_name, True)
    
    # Ghost Chords Track (optional, for reference)
    RPR.RPR_InsertTrackAtIndex(track_count_start + 2, True)
    ghost_chords_track = RPR.RPR_GetTrack(0, track_count_start + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(ghost_chords_track, "P_NAME", ghost_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(ghost_chords_track, "I_SOLO", 0) # Mute ghost track by default
    RPR.RPR_SetMediaTrackInfo_Value(ghost_chords_track, "I_MUTE", 1) # Mute ghost track by default


    # === Step 2: Setup Instruments (ReaSynth) ===
    # Main Bass (ReaSynth) - slightly sustained, low-mid focused
    RPR.RPR_TrackFX_AddByName(main_bass_track, "ReaSynth (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 0, 1.0) # Osc 1 Waveform (Saw)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 2, 0.4) # Osc 1 Level
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 4, 0.0) # Attack (fast)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 5, 0.4) # Decay (medium)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 6, 0.5) # Sustain (medium)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 7, 0.3) # Release (short)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 17, 0.3) # Filter Cutoff (lowpass)
    RPR.RPR_TrackFX_SetParam(main_bass_track, 0, 18, 0.5) # Filter Resonance

    # Slap Bass (ReaSynth) - very short, percussive, higher pitch
    RPR.RPR_TrackFX_AddByName(slap_bass_track, "ReaSynth (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 0, 2.0) # Osc 1 Waveform (Square)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 2, 0.5) # Osc 1 Level
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 4, 0.0) # Attack (fastest)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 5, 0.05) # Decay (very short)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 6, 0.0) # Sustain (zero)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 7, 0.05) # Release (very short)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 17, 0.8) # Filter Cutoff (bright)
    RPR.RPR_TrackFX_SetParam(slap_bass_track, 0, 18, 0.8) # Filter Resonance


    # === Step 3: Define Chord Progression & MIDI Item Setup ===
    beats_per_bar = 4
    bar_length_beats = float(beats_per_bar) 
    
    # Example chord progression (I-vi-IV-V in C Major)
    chord_progression_roots = [
        get_midi_note_from_scale_degree(key, scale, 1, 3), # I (root octave 3)
        get_midi_note_from_scale_degree(key, scale, 6, 3), # vi (root octave 3)
        get_midi_note_from_scale_degree(key, scale, 4, 3), # IV (root octave 3)
        get_midi_note_from_scale_degree(key, scale, 5, 3), # V (root octave 3)
    ]
    
    # Chords for ghost notes (full triads, higher octave for clarity)
    chord_voicings = [
        [get_midi_note_from_scale_degree(key, scale, 1, 4), get_midi_note_from_scale_degree(key, scale, 3, 4), get_midi_note_from_scale_degree(key, scale, 5, 4)], # I chord
        [get_midi_note_from_scale_degree(key, scale, 6, 3), get_midi_note_from_scale_degree(key, scale, 1, 4), get_midi_note_from_scale_degree(key, scale, 3, 4)], # vi chord (inversion/voicing for flow)
        [get_midi_note_from_scale_degree(key, scale, 4, 3), get_midi_note_from_scale_degree(key, scale, 6, 3), get_midi_note_from_scale_degree(key, scale, 1, 4)], # IV chord (inversion/voicing for flow)
        [get_midi_note_from_scale_degree(key, scale, 5, 3), get_midi_note_from_scale_degree(key, scale, 7, 3), get_midi_note_from_scale_degree(key, scale, 2, 4)], # V chord (inversion/voicing for flow)
    ]

    midi_notes_total = 0

    # Create MIDI Items
    main_bass_item = RPR.RPR_AddMediaItemToTrack(main_bass_track)
    RPR.RPR_SetMediaItemInfo_Value(main_bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(main_bass_item, "D_LENGTH", bar_length_beats * bars)
    main_bass_take = RPR.RPR_AddTakeToMediaItem(main_bass_item)
    RPR.RPR_MIDI_SetItemExtents(main_bass_item, 0.0, bar_length_beats * bars) # Set item to be MIDI
    RPR.MIDI_SetOpen(main_bass_take, True) # Open MIDI editor for the take

    slap_bass_item = RPR.RPR_AddMediaItemToTrack(slap_bass_track)
    RPR.RPR_SetMediaItemInfo_Value(slap_bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(slap_bass_item, "D_LENGTH", bar_length_beats * bars)
    slap_bass_take = RPR.RPR_AddTakeToMediaItem(slap_bass_item)
    RPR.RPR_MIDI_SetItemExtents(slap_bass_item, 0.0, bar_length_beats * bars) # Set item to be MIDI
    RPR.MIDI_SetOpen(slap_bass_take, True)

    ghost_chords_item = RPR.RPR_AddMediaItemToTrack(ghost_chords_track)
    RPR.RPR_SetMediaItemInfo_Value(ghost_chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(ghost_chords_item, "D_LENGTH", bar_length_beats * bars)
    ghost_chords_take = RPR.RPR_AddTakeToMediaItem(ghost_chords_item)
    RPR.RPR_MIDI_SetItemExtents(ghost_chords_item, 0.0, bar_length_beats * bars) # Set item to be MIDI
    RPR.MIDI_SetOpen(ghost_chords_take, True)


    # === Step 4: Generate MIDI Notes ===
    for bar in range(bars):
        current_root_midi = chord_progression_roots[bar % len(chord_progression_roots)]
        current_voicing = chord_voicings[bar % len(chord_voicings)]
        bar_start_beat = bar * bar_length_beats

        # Add ghost chord for reference
        for note_pitch in current_voicing:
            ghost_velocity = humanize_velocity(int(velocity_base * 0.4), humanize_strength)
            RPR.MIDI_InsertNote(ghost_chords_take, False, False, 
                                humanize_timing(bar_start_beat, 1.0, humanize_strength), # 1.0 is duration of a quarter note
                                bar_start_beat + bar_length_beats, # Full bar duration
                                ghost_velocity, note_pitch, False)
            midi_notes_total += 1

        # Bassline Pattern for each bar
        # Note durations are expressed in beats (e.g., 1.0 for quarter, 0.5 for eighth, 0.25 for 16th)
        
        # Beat 1: Root note (slightly shorter than a full beat)
        RPR.MIDI_InsertNote(main_bass_take, False, False, 
                            humanize_timing(bar_start_beat, 1.0, humanize_strength), 
                            bar_start_beat + 0.8, # 0.8 beat duration for a grooving quarter note
                            humanize_velocity(velocity_base + 10, humanize_strength), 
                            current_root_midi, False)
        midi_notes_total += 1

        if bar % 2 == 0: # Pattern for even bars (more complex, walking bass feel)
            # Beat 2: Fifth, shorter
            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 1.0, 0.5, humanize_strength), 
                                bar_start_beat + 1.0 + 0.4, # 0.4 beat duration (short 8th)
                                humanize_velocity(velocity_base, humanize_strength), 
                                current_root_midi + 7, False) # Perfect 5th
            midi_notes_total += 1

            # Beat 2.5 (& of 2): Slap (on the upbeat)
            slap_pitch_mid = get_midi_note_from_scale_degree(key, scale, 3, 4) # e.g., 3rd scale degree, octave 4 (E4 in C major)
            RPR.MIDI_InsertNote(slap_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 1.5, 0.25, humanize_strength), 
                                bar_start_beat + 1.5 + 0.1, # Very short, percussive
                                humanize_velocity(velocity_base + 30, humanize_strength), # Higher velocity for slap
                                slap_pitch_mid, False)
            midi_notes_total += 1

            # Beat 3: Scale step (e.g., 2nd degree)
            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 2.0, 0.75, humanize_strength), 
                                bar_start_beat + 2.0 + 0.7, # 0.7 beat duration
                                humanize_velocity(velocity_base, humanize_strength), 
                                get_midi_note_from_scale_degree(key, scale, 2, 3), # 2nd degree in root octave
                                False)
            midi_notes_total += 1
            
            # Beat 4: Passing note leading to next root
            next_root_midi = chord_progression_roots[(bar + 1) % len(chord_progression_roots)]
            # Simple passing note logic: try to step towards the next root
            passing_note = current_root_midi # Default to root if no clear step
            if next_root_midi > current_root_midi and next_root_midi - current_root_midi <= 7: # Ascending, within an octave
                passing_note = get_midi_note_from_scale_degree(key, scale, 7, 3) # Use 7th scale degree
            elif next_root_midi < current_root_midi and current_root_midi - next_root_midi <= 7: # Descending
                passing_note = get_midi_note_from_scale_degree(key, scale, 5, 3) - 1 # Chromatic lower neighbor to 5th

            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 3.0, 1.0, humanize_strength), 
                                bar_start_beat + 3.0 + 0.8, # 0.8 beat duration
                                humanize_velocity(velocity_base + 5, humanize_strength), 
                                passing_note, False)
            midi_notes_total += 1

        else: # Pattern for odd bars (more simple, rhythmic focus)
            # Beat 2: Root note, syncopated (1/4 beat after beat 2)
            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 1.25, 0.5, humanize_strength), 
                                bar_start_beat + 1.25 + 0.4, # 0.4 beat duration
                                humanize_velocity(velocity_base - 10, humanize_strength), 
                                current_root_midi, False)
            midi_notes_total += 1

            # Beat 3: Octave up or fifth
            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 2.0, 0.75, humanize_strength), 
                                bar_start_beat + 2.0 + 0.7, # 0.7 beat duration
                                humanize_velocity(velocity_base + 5, humanize_strength), 
                                current_root_midi + 12, False) # Octave up from root
            midi_notes_total += 1

            # Beat 3.5 (& of 3): Slap (on the upbeat)
            slap_pitch_high = get_midi_note_from_scale_degree(key, scale, 5, 4) # e.g., 5th scale degree, octave 4 (G4 in C major)
            RPR.MIDI_InsertNote(slap_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 2.5, 0.25, humanize_strength), 
                                bar_start_beat + 2.5 + 0.1, # Very short, percussive
                                humanize_velocity(velocity_base + 30, humanize_strength), # Higher velocity for slap
                                slap_pitch_high, False)
            midi_notes_total += 1

            # Beat 4: Root for next bar
            RPR.MIDI_InsertNote(main_bass_take, False, False, 
                                humanize_timing(bar_start_beat + 3.0, 1.0, humanize_strength), 
                                bar_start_beat + 3.0 + 0.8, # 0.8 beat duration
                                humanize_velocity(velocity_base + 5, humanize_strength), 
                                current_root_midi, False)
            midi_notes_total += 1

    # Close MIDI editors to commit changes
    RPR.MIDI_SetOpen(main_bass_take, False)
    RPR.MIDI_SetOpen(slap_bass_take, False)
    RPR.MIDI_SetOpen(ghost_chords_take, False)
    
    RPR.UpdateArrange()
    RPR.Undo_EndBlock2(0, "Create Evolving Bassline Groove", -1) # End undo block

    return f"Created '{track_name}', '{slap_track_name}', and '{ghost_track_name}' with {midi_notes_total} notes over {bars} bars."

