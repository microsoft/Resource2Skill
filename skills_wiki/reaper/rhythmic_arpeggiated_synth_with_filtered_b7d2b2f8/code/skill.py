import reaper_python as RPR

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

def create_arpeggiated_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arpeggiated Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 80,
    arpeggio_pattern: list = [0, 2, 4, 7], # 0-indexed scale degrees (e.g., [0, 2, 4, 7] for 1st, 3rd, 5th, 8th)
    arpeggio_octaves_span: int = 2, # How many octaves the arpeggio pattern should span
    note_rhythm_division: int = 16, # 4 for quarter, 8 for eighth, 16 for sixteenth
    arpeggio_start_octave: int = 3, # Starting MIDI octave for the arpeggio
    **kwargs,
) -> str:
    """
    Create an arpeggiated synth pattern with delay, approximating the tutorial's concept.
    Note: Exact sound design and complex rhythmic modulation of proprietary VSTs
    (Massive X, Reason Beat Map, BLASS, BLASS Delay) cannot be reproduced with stock REAPER plugins.
    This skill provides a conceptual equivalent using ReaSynth and ReaDelay.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        arpeggio_pattern: List of 0-indexed scale degrees to arpeggiate (e.g., [0, 2, 4] for 1st, 3rd, 5th).
        arpeggio_octaves_span: How many octaves the arpeggio pattern should span.
        note_rhythm_division: Rhythmic division for each arpeggio note (e.g., 16 for 16th notes).
        arpeggio_start_octave: The starting MIDI octave for the arpeggio.
        **kwargs: Additional overrides (not used in this simplified version).

    Returns:
        Status string describing what was created.
    """
    RPR.Undo_BeginBlock2(0) # Begin an undo block

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    seconds_per_beat = 60.0 / bpm
    
    # Calculate note duration based on rhythm division
    note_duration_beats = beats_per_bar / note_rhythm_division # e.g., 4 beats/bar / 16 = 0.25 beats per 16th note

    item_length_beats = beats_per_bar * bars
    item_length_sec = item_length_beats * seconds_per_beat

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", RPR.RPR_GetPlayPosition()) # Start at current play position
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.MIDI_CreateNewMIDIItemInTake(take, 0), False)
    midi_take = RPR.RPR_GetMediaItemTake_Source(take)

    # Get notes in the scale to pick from for arpeggiation
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_midi_base = NOTE_MAP.get(key, 0)

    notes_created = 0
    current_beat_pos = 0.0

    # Generate arpeggio notes list
    arpeggio_notes_midi = []
    for octave_mult in range(arpeggio_octaves_span):
        for degree in arpeggio_pattern:
            effective_degree = degree % len(scale_intervals)
            # Adjust octave if the pattern degree itself implies an octave jump beyond the base scale
            octave_adjust_for_pattern = (degree // len(scale_intervals)) * 12 
            
            midi_note = root_midi_base + scale_intervals[effective_degree] \
                        + (arpeggio_start_octave + octave_mult) * 12 \
                        + octave_adjust_for_pattern
            arpeggio_notes_midi.append(midi_note)

    # Ensure notes are within a reasonable MIDI range (e.g., C2 to C7)
    arpeggio_notes_midi = [max(36, min(note, 96)) for note in arpeggio_notes_midi]

    pattern_index = 0
    while current_beat_pos < item_length_beats:
        if not arpeggio_notes_midi: # Prevent error if pattern is empty
            break

        midi_note_to_insert = arpeggio_notes_midi[pattern_index % len(arpeggio_notes_midi)]

        note_pos_sec = current_beat_pos * seconds_per_beat
        note_len_sec = note_duration_beats * seconds_per_beat * 0.9 # 90% duration for a slightly plucky sound

        RPR.MIDI_InsertNote(midi_take, False, False, note_pos_sec, note_pos_sec + note_len_sec, velocity_base, 0, midi_note_to_insert, True)
        notes_created += 1

        current_beat_pos += note_duration_beats
        pattern_index += 1

    RPR.MIDI_Sort(midi_take)
    RPR.MIDI_SetItemExtents(item, 0, 0) # Update item length from MIDI content

    # === Step 3: Add FX Chain (ReaSynth + ReaDelay) ===
    # ReaSynth (as a basic placeholder for Massive X)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    fx_synth_idx = RPR.RPR_TrackFX_GetByName(track, "ReaSynth (Cockos)", False)
    if fx_synth_idx != -1:
        # Set basic "pluck" parameters for ReaSynth (param indices: 0=Vol, 1=Att, 2=Dec, 3=Sus, 4=Rel, 5=Wave)
        RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 1, 0.05) # Attack (0.0 - 1.0)
        RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 2, 0.2)  # Decay (0.0 - 1.0)
        RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 3, 0.1)  # Sustain (0.0 - 1.0)
        RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 4, 0.1)  # Release (0.0 - 1.0)
        RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 5, 0.5)  # Waveform (0.0=Sine, 0.5=Saw, 1.0=Square)

    # ReaDelay (as a placeholder for BLASS Delay)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay (Cockos)", False, -1)
    fx_delay_idx = RPR.RPR_TrackFX_GetByName(track, "ReaDelay (Cockos)", False)
    if fx_delay_idx != -1:
        # Set parameters for Tap 1 of ReaDelay (common default setup for a filtered delay)
        # Parameter indices for ReaDelay can be complex; these are common approximations.
        RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 1, 0.5)  # Tap 1 Wet (mix)
        RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 2, 0.25) # Tap 1 Delay (e.g., 1/4 note if tempo-synced in plugin)
        RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 3, 0.4)  # Tap 1 Feedback
        RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 5, 0.7)  # Tap 1 Lowpass (filter cutoff)
        RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 6, 0.2)  # Tap 1 Highpass (filter cutoff)

    RPR.UpdateArrange()
    RPR.Undo_EndBlock2(0, f"Created '{track_name}' arpeggiated synth skill", -1)

    return f"Created '{track_name}' with {notes_created} arpeggiated notes over {bars} bars at {bpm} BPM with ReaSynth and ReaDelay (approximate sound)."

