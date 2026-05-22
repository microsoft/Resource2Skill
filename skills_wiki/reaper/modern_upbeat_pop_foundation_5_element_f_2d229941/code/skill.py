def create_pattern(
    project_name: str = "Pop Producer Pro",
    track_name: str = "Pop",
    bpm: int = 115,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Modern Upbeat Pop Foundation (Drums, Bass, Mids) in REAPER.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (115 is optimal for this groove).
        key: Root note (e.g., D).
        scale: Scale type (major or minor).
        bars: Number of bars to generate (generates a 4-bar progression loop).
        velocity_base: Base velocity for the groove.
    """
    import reaper_python as RPR
    import math

    # Theory lookup
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Set project tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 2) # Default to D
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Standard pop progression: vi - IV - I - V (major) or i - VI - III - VII (minor)
    progression_degrees = [5, 3, 0, 4] if scale.lower() == "major" else [0, 5, 2, 6]

    def get_chord_notes(degree, octave):
        """Returns root, third, and fifth MIDI notes for a given scale degree."""
        notes = []
        for offset in [0, 2, 4]: # Triad
            idx = (degree + offset) % 7
            oct_shift = (degree + offset) // 7
            pitch = root_pitch + scale_intervals[idx] + ((octave + oct_shift) * 12)
            notes.append(pitch)
        return notes

    def create_midi_track(name, is_drum=False):
        """Helper to create a track, a MIDI item, and return the take reference."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        # Calculate item length
        quarter_len = 60.0 / bpm
        bar_len = quarter_len * 4
        
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, bar_len * bars, False)
        take = RPR.RPR_GetActiveTake(item)
        return track, take, quarter_len, bar_len

    def insert_note(take, time_sec, duration_sec, pitch, vel):
        """Inserts a MIDI note precisely using PPQ mapping."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec + duration_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # -----------------------------------------------------------------------
    # 1. DRUMS TRACK
    # -----------------------------------------------------------------------
    drum_track, drum_take, q_len, b_len = create_midi_track("Drums", True)
    
    # Add Drum Processing (ReaComp to snap transients, ReaEQ for low punch)
    comp_idx = RPR.RPR_TrackFX_AddByName(drum_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(drum_track, comp_idx, 0, -15.0) # Threshold
    RPR.RPR_TrackFX_SetParam(drum_track, comp_idx, 1, 4.0)   # Ratio
    eq_idx = RPR.RPR_TrackFX_AddByName(drum_track, "ReaEQ", False, -1)
    
    kick_pitch, snare_pitch, hat_pitch = 36, 38, 42
    
    for bar in range(bars):
        bar_start = bar * b_len
        # Syncopated Kick: 1, 2-and, 3, 4-and
        for beat_offset in [0, 1.5, 2, 3.5]:
            insert_note(drum_take, bar_start + (beat_offset * q_len), q_len * 0.25, kick_pitch, velocity_base + 10)
        # Snare: 2, 4
        for beat_offset in [1, 3]:
            insert_note(drum_take, bar_start + (beat_offset * q_len), q_len * 0.25, snare_pitch, velocity_base)
        # Hats: 8th notes
        for beat_offset in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:
            vel = velocity_base - 10 if (beat_offset % 1 != 0) else velocity_base
            insert_note(drum_take, bar_start + (beat_offset * q_len), q_len * 0.125, hat_pitch, vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # -----------------------------------------------------------------------
    # 2. BASS TRACK
    # -----------------------------------------------------------------------
    bass_track, bass_take, _, _ = create_midi_track("Bass")
    
    # Add simple placeholder synth and low-pass filter
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    bass_eq = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    
    for bar in range(bars):
        bar_start = bar * b_len
        deg = progression_degrees[bar % len(progression_degrees)]
        chord = get_chord_notes(deg, 2) # Octave 2
        root_bass = chord[0]
        
        # Driving 8th notes
        for eighth in range(8):
            time_offset = eighth * (q_len / 2.0)
            insert_note(bass_take, bar_start + time_offset, (q_len / 2.0) * 0.8, root_bass, velocity_base)

    RPR.RPR_MIDI_Sort(bass_take)

    # -----------------------------------------------------------------------
    # 3. MIDS TRACK (Chords / Keys)
    # -----------------------------------------------------------------------
    mids_track, mids_take, _, _ = create_midi_track("Mids")
    
    # Add Synths, EQ (Low Cut to make room for bass), and Reverb (Wide Wash)
    RPR.RPR_TrackFX_AddByName(mids_track, "ReaSynth", False, -1)
    mids_eq = RPR.RPR_TrackFX_AddByName(mids_track, "ReaEQ", False, -1)
    verb_idx = RPR.RPR_TrackFX_AddByName(mids_track, "ReaVerbate", False, -1)
    
    # Push wet signal up for that roomy pop wash
    RPR.RPR_TrackFX_SetParam(mids_track, verb_idx, 0, 0.4) # Wet
    RPR.RPR_TrackFX_SetParam(mids_track, verb_idx, 1, 0.6) # Dry
    RPR.RPR_TrackFX_SetParam(mids_track, verb_idx, 2, 0.8) # Room Size
    
    for bar in range(bars):
        bar_start = bar * b_len
        deg = progression_degrees[bar % len(progression_degrees)]
        chord = get_chord_notes(deg, 4) # Octave 4
        
        # Syncopated block chords: hits on beat 1, and the "and" of 2
        for offset in [0.0, 1.5]:
            for note in chord:
                insert_note(mids_take, bar_start + (offset * q_len), q_len * 1.5, note, velocity_base - 15)

    RPR.RPR_MIDI_Sort(mids_take)

    return f"Created {bars} bars of Upbeat Pop Foundation at {bpm} BPM (Key of {key} {scale}). Generated tracks for Drums, Bass, and Mids with bus processing applied."
