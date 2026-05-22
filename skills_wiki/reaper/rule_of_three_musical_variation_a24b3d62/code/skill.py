import reaper_python as RPR
import math

# Music theory lookup tables (global for easy access within the script)
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
    "add9": [0, 4, 7, 14], # add9 is major chord + major 9th
}

def get_midi_note(root_key, scale_name, degree, base_octave):
    root_midi_offset = NOTE_MAP[root_key]
    scale_intervals = SCALES[scale_name.lower()]

    # Calculate absolute degree considering scale length and octave
    num_scale_degrees = len(scale_intervals)
    octave_shift = degree // num_scale_degrees
    degree_in_octave = degree % num_scale_degrees

    midi_note = root_midi_offset + (base_octave + octave_shift) * 12 + scale_intervals[degree_in_octave]
    return midi_note

def add_midi_notes_to_item(midi_take, start_time_beats, notes_midi, duration_beats, velocity):
    for note_midi in notes_midi:
        RPR.MIDI_InsertNote(midi_take, False, False, start_time_beats, start_time_beats + duration_beats, 0, note_midi, velocity, False)

def create_rule_of_three_demo(
    project_name: str = "RuleOfThreeDemo",
    track_name: str = "Piano Demo",
    bpm: int = 120,
    key: str = "G",
    scale: str = "major",
    demonstrations: int = 1, # Number of times to play the full (Original + Var1 + Var2) sequence
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a musical demonstration of the "Rule of Three" in REAPER.
    This includes an original 4-bar phrase, a 4-bar phrase with a new melody,
    and a 4-bar phrase that changes midway through.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        demonstrations: Number of times to repeat the full demo sequence (Original + Var1 + Var2).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this skill but for composability).

    Returns:
        Status string, e.g., "Created 'Piano Demo' with 3 sections x 1 demonstration at 120 BPM"
    """
    RPR.Undo_BeginBlock2(0) # Begin undo block

    # === Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, float(bpm), False)

    # === Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Add ReaSynth FX ===
    RPR.TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    # Configure ReaSynth for a basic pluck/pad sound (approximate piano)
    # Oscillator 1 (Saw), Amp Env: Attack (0.05), Decay (0.5), Sustain (0.0), Release (0.2)
    RPR.TrackFX_SetParam(track, 0, 0, 0.5) # OSC1 Waveform (Saw is ~0.5)
    RPR.TrackFX_SetParam(track, 0, 3, 0.05) # Amp Env Attack
    RPR.TrackFX_SetParam(track, 0, 4, 0.5)  # Amp Env Decay
    RPR.TrackFX_SetParam(track, 0, 5, 0.0)  # Amp Env Sustain
    RPR.TrackFX_SetParam(track, 0, 6, 0.2)  # Amp Env Release

    beats_per_bar = 4
    item_length_bars = 4 # Each phrase is 4 bars long
    item_length_beats = item_length_bars * beats_per_bar

    total_notes_added = 0
    start_beat_offset = 0

    for demo_num in range(demonstrations):
        # --- Section 1: Original Phrase (4 bars) ---
        item_original = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item_original, "D_POSITION", start_beat_offset)
        RPR.RPR_SetMediaItemInfo_Value(item_original, "D_LENGTH", item_length_beats)
        take_original = RPR.RPR_AddTakeToMediaItem(item_original)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take_original, "P_NAME", f"Original Phrase {demo_num+1}", True)
        RPR.RPR_MIDI_SetItemExtents(item_original, 0, 0) # Ensure MIDI item length matches source

        midi_take_original = RPR.MIDI_SetItemTake(item_original, take_original)
        RPR.MIDI_SetItemExtents(item_original, 0.0, item_length_beats) # Set MIDI item length

        # Chords: Gmaj - Cmaj - Gmaj - Dmaj (in G Major)
        # Melody: B4 A4 G4 | C5 D5 E5 | G5 F#5 E5 | D5 C5 B4
        
        # Bar 1 (G Major)
        chord_root_midi = get_midi_note(key, scale, 0, 3) # G3
        add_midi_notes_to_item(midi_take_original, 0, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_original, 0, [get_midi_note(key, scale, 2, 4)], 1, velocity_base) # B4 (q)
        add_midi_notes_to_item(midi_take_original, 1, [get_midi_note(key, scale, 1, 4)], 1, velocity_base) # A4 (q)
        add_midi_notes_to_item(midi_take_original, 2, [get_midi_note(key, scale, 0, 4)], 2, velocity_base) # G4 (h)

        # Bar 2 (C Major)
        chord_root_midi = get_midi_note(key, scale, 3, 3) # C3
        add_midi_notes_to_item(midi_take_original, 4, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_original, 4, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5 (q)
        add_midi_notes_to_item(midi_take_original, 5, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5 (q)
        add_midi_notes_to_item(midi_take_original, 6, [get_midi_note(key, scale, 5, 4)], 2, velocity_base) # E5 (h)

        # Bar 3 (G Major)
        chord_root_midi = get_midi_note(key, scale, 0, 3) # G3
        add_midi_notes_to_item(midi_take_original, 8, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_original, 8, [get_midi_note(key, scale, 7, 4)], 1, velocity_base) # G5 (q)
        add_midi_notes_to_item(midi_take_original, 9, [get_midi_note(key, scale, 6, 4)], 1, velocity_base) # F#5 (q) - 7th degree of G major scale is F#, using degree 6 (scale index 6)
        add_midi_notes_to_item(midi_take_original, 10, [get_midi_note(key, scale, 5, 4)], 2, velocity_base) # E5 (h)

        # Bar 4 (D Major)
        chord_root_midi = get_midi_note(key, scale, 4, 3) # D3
        add_midi_notes_to_item(midi_take_original, 12, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_original, 12, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5 (q)
        add_midi_notes_to_item(midi_take_original, 13, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5 (q)
        add_midi_notes_to_item(midi_take_original, 14, [get_midi_note(key, scale, 2, 4)], 2, velocity_base) # B4 (h)
        
        RPR.MIDI_Sort(midi_take_original)
        RPR.MIDI_Compress(midi_take_original)
        total_notes_added += RPR.MIDI_CountEvts(midi_take_original)[0]
        RPR.MIDI_FreeCommand(midi_take_original)
        start_beat_offset += item_length_beats


        # --- Section 2: New Melody, Same Chords (4 bars) ---
        item_var1 = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item_var1, "D_POSITION", start_beat_offset)
        RPR.RPR_SetMediaItemInfo_Value(item_var1, "D_LENGTH", item_length_beats)
        take_var1 = RPR.RPR_AddTakeToMediaItem(item_var1)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take_var1, "P_NAME", f"New Melody Variation {demo_num+1}", True)
        RPR.RPR_MIDI_SetItemExtents(item_var1, 0, 0) # Ensure MIDI item length matches source

        midi_take_var1 = RPR.MIDI_SetItemTake(item_var1, take_var1)
        RPR.MIDI_SetItemExtents(item_var1, 0.0, item_length_beats)

        # Chords: Same as original
        # Melody: G5 E5 D5 C5 | D5 E5 F#5 G5 | E5 D5 C5 B4 | A4 G4 F#4 E4 (all quarter notes)

        # Bar 1 (G Major)
        chord_root_midi = get_midi_note(key, scale, 0, 3) # G3
        add_midi_notes_to_item(midi_take_var1, 0, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var1, 0, [get_midi_note(key, scale, 7, 4)], 1, velocity_base) # G5
        add_midi_notes_to_item(midi_take_var1, 1, [get_midi_note(key, scale, 5, 4)], 1, velocity_base) # E5
        add_midi_notes_to_item(midi_take_var1, 2, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5
        add_midi_notes_to_item(midi_take_var1, 3, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5

        # Bar 2 (C Major)
        chord_root_midi = get_midi_note(key, scale, 3, 3) # C3
        add_midi_notes_to_item(midi_take_var1, 4, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var1, 4, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5
        add_midi_notes_to_item(midi_take_var1, 5, [get_midi_note(key, scale, 5, 4)], 1, velocity_base) # E5
        add_midi_notes_to_item(midi_take_var1, 6, [get_midi_note(key, scale, 6, 4)], 1, velocity_base) # F#5
        add_midi_notes_to_item(midi_take_var1, 7, [get_midi_note(key, scale, 7, 4)], 1, velocity_base) # G5

        # Bar 3 (G Major)
        chord_root_midi = get_midi_note(key, scale, 0, 3) # G3
        add_midi_notes_to_item(midi_take_var1, 8, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var1, 8, [get_midi_note(key, scale, 5, 4)], 1, velocity_base) # E5
        add_midi_notes_to_item(midi_take_var1, 9, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5
        add_midi_notes_to_item(midi_take_var1, 10, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5
        add_midi_notes_to_item(midi_take_var1, 11, [get_midi_note(key, scale, 2, 4)], 1, velocity_base) # B4

        # Bar 4 (D Major)
        chord_root_midi = get_midi_note(key, scale, 4, 3) # D3
        add_midi_notes_to_item(midi_take_var1, 12, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var1, 12, [get_midi_note(key, scale, 1, 4)], 1, velocity_base) # A4
        add_midi_notes_to_item(midi_take_var1, 13, [get_midi_note(key, scale, 0, 4)], 1, velocity_base) # G4
        add_midi_notes_to_item(midi_take_var1, 14, [get_midi_note(key, scale, 6, 3)], 1, velocity_base) # F#4
        add_midi_notes_to_item(midi_take_var1, 15, [get_midi_note(key, scale, 5, 3)], 1, velocity_base) # E4

        RPR.MIDI_Sort(midi_take_var1)
        RPR.MIDI_Compress(midi_take_var1)
        total_notes_added += RPR.MIDI_CountEvts(midi_take_var1)[0]
        RPR.MIDI_FreeCommand(midi_take_var1)
        start_beat_offset += item_length_beats


        # --- Section 3: Same Start, Different Midway (4 bars) ---
        item_var2 = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item_var2, "D_POSITION", start_beat_offset)
        RPR.RPR_SetMediaItemInfo_Value(item_var2, "D_LENGTH", item_length_beats)
        take_var2 = RPR.RPR_AddTakeToMediaItem(item_var2)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take_var2, "P_NAME", f"Different Midway Variation {demo_num+1}", True)
        RPR.RPR_MIDI_SetItemExtents(item_var2, 0, 0) # Ensure MIDI item length matches source

        midi_take_var2 = RPR.MIDI_SetItemTake(item_var2, take_var2)
        RPR.MIDI_SetItemExtents(item_var2, 0.0, item_length_beats)

        # Bars 1-2: Same as original
        # Bar 1 (G Major)
        chord_root_midi = get_midi_note(key, scale, 0, 3) # G3
        add_midi_notes_to_item(midi_take_var2, 0, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var2, 0, [get_midi_note(key, scale, 2, 4)], 1, velocity_base) # B4 (q)
        add_midi_notes_to_item(midi_take_var2, 1, [get_midi_note(key, scale, 1, 4)], 1, velocity_base) # A4 (q)
        add_midi_notes_to_item(midi_take_var2, 2, [get_midi_note(key, scale, 0, 4)], 2, velocity_base) # G4 (h)

        # Bar 2 (C Major)
        chord_root_midi = get_midi_note(key, scale, 3, 3) # C3
        add_midi_notes_to_item(midi_take_var2, 4, get_chord_notes(chord_root_midi, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var2, 4, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5 (q)
        add_midi_notes_to_item(midi_take_var2, 5, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5 (q)
        add_midi_notes_to_item(midi_take_var2, 6, [get_midi_note(key, scale, 5, 4)], 2, velocity_base) # E5 (h)

        # Bars 3-4: Different progression & melody (Am - Fmaj)
        # Bar 3 (A minor)
        chord_root_midi_am = get_midi_note(key, "minor", 1, 3) # A3 (ii chord from Gmaj key, using minor scale intervals relative to A)
        add_midi_notes_to_item(midi_take_var2, 8, get_chord_notes(chord_root_midi_am, "minor"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var2, 8, [get_midi_note(key, scale, 5, 4)], 1, velocity_base) # E5 (q)
        add_midi_notes_to_item(midi_take_var2, 9, [get_midi_note(key, scale, 6, 4)], 1, velocity_base) # F5 (q) - technically F in G Major scale is F#, but using F for Am)
        add_midi_notes_to_item(midi_take_var2, 10, [get_midi_note(key, scale, 7, 4)], 2, velocity_base) # G5 (h)

        # Bar 4 (F Major)
        chord_root_midi_fmaj = get_midi_note(key, "major", -2, 3) # F3 (VIb in G, but using major scale intervals relative to F)
        add_midi_notes_to_item(midi_take_var2, 12, get_chord_notes(chord_root_midi_fmaj, "major"), 4, velocity_base - 10)
        add_midi_notes_to_item(midi_take_var2, 12, [get_midi_note(key, scale, 3, 4)], 1, velocity_base) # C5 (q)
        add_midi_notes_to_item(midi_take_var2, 13, [get_midi_note(key, scale, 4, 4)], 1, velocity_base) # D5 (q)
        add_midi_notes_to_item(midi_take_var2, 14, [get_midi_note(key, scale, 5, 4)], 2, velocity_base) # E5 (h)

        RPR.MIDI_Sort(midi_take_var2)
        RPR.MIDI_Compress(midi_take_var2)
        total_notes_added += RPR.MIDI_CountEvts(midi_take_var2)[0]
        RPR.MIDI_FreeCommand(midi_take_var2)
        start_beat_offset += item_length_beats
    
    RPR.Undo_EndBlock2(0, f"Created Rule of Three Demo ({demonstrations} sets)", -1)
    
    total_bars = demonstrations * (item_length_bars * 3)
    return f"Created '{track_name}' with {total_notes_added} notes over {total_bars} bars, with {demonstrations} full demonstrations at {bpm} BPM."

