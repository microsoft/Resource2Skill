def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Electro Pluck Chords",
    bpm: int = 128,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Electro-Pluck synth using ReaSynth and automated JS Filters.
    Mimics the "Envelope modulating Filter Cutoff" technique taught in the tutorial.
    """
    import reaper_python as RPR
    import math

    # === Music Theory Helpers ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_note = NOTE_MAP.get(key, 0) + 48 # Base octave C3 (48)

    # Progression degrees (1-based: I, VI, III, VII for minor / I, IV, vi, V for major)
    if scale.lower() == "minor":
        progression = [0, 5, 2, 6] # i, VI, III, VII
    else:
        progression = [0, 3, 5, 4] # I, IV, vi, V

    def get_chord_notes(degree_index):
        """Builds a triad based on the scale degree"""
        notes = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = degree_index + i
            octave_shift = idx // 7
            scale_idx = idx % 7
            note = root_note + scale_intervals[scale_idx] + (octave_shift * 12)
            notes.append(note)
        # Add an octave bass note for thickness
        notes.append(notes[0] - 12)
        return notes

    # === Step 1: Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item & Chords ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Rhythmic pattern: 1/8th note stabs (syncopated)
    # Define timing in beats (quarters)
    rhythm_pattern = [
        (0.0, 0.75),   # Beat 1, length 1/8.
        (1.0, 0.75),   # Beat 2, length 1/8.
        (2.5, 0.75),   # Beat 3.5 (syncopated), length 1/8
        (3.5, 0.25)    # Beat 4.5, fast pickup
    ]

    sec_per_beat = 60.0 / bpm
    total_notes_created = 0
    chord_start_times = [] # Keep track for our filter envelope automation later

    for bar in range(bars):
        chord_idx = bar % len(progression)
        chord_notes = get_chord_notes(progression[chord_idx])
        bar_offset_sec = bar * bar_length_sec

        for start_beat, length_beats in rhythm_pattern:
            start_sec = bar_offset_sec + (start_beat * sec_per_beat)
            end_sec = start_sec + (length_beats * sec_per_beat)
            
            # Save time for automation
            chord_start_times.append(start_sec)

            # Insert notes
            for note in chord_notes:
                # PPQ calculation (assuming 960 PPQ)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)
                total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Sound Design (FX Chain) ===
    # 1. ReaSynth: Raw waveform (Sawtooth/Square blend)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.7)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.8)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.01)  # Extra fast attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.05)  # Release

    # 2. JS Moog Filter: The subtractive element
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Moog 24dB/oct Filter", False, -1)
    RPR.RPR_TrackFX_SetParam(track, filter_idx, 1, 0.4) # Resonance (add some bite)
    
    # 3. ReaDelay: Space and width (imitating Unison)
    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, 0.0) # Tap 1 Vol
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 4, sec_per_beat * 0.75) # Length (dotted 8th)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 6, -0.8) # Pan Left
    # Add Tap 2
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 13, 0.0) # Tap 2 Vol
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 17, sec_per_beat * 0.5) # Length (8th)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 19, 0.8) # Pan Right
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 12, -12.0) # Wet mix

    # === Step 4: Automate the Filter Envelope ===
    # This simulates Serum's "Envelope to Filter Cutoff" shown in the tutorial.
    env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True) # Param 0 is Cutoff
    
    # Base filter state (closed)
    base_cutoff = 0.1 
    peak_cutoff = 0.85
    decay_time = 0.15 # 150ms decay (the "Pluck" shape)

    for t in chord_start_times:
        # Before strike: Closed
        RPR.RPR_InsertEnvelopePoint(env, t - 0.001, base_cutoff, 0, 0, False, True)
        # On strike: Instantly open (Fast Attack)
        RPR.RPR_InsertEnvelopePoint(env, t, peak_cutoff, 0, 0, False, True)
        # Decay: Quickly drop back down to base
        RPR.RPR_InsertEnvelopePoint(env, t + decay_time, base_cutoff, 0, 0, False, True)
    
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}': Subtractive Pluck with {total_notes_created} notes over {bars} bars at {bpm} BPM in {key} {scale}."
