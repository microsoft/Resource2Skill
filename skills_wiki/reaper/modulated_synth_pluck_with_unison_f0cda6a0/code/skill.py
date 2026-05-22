import math

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Modulated Pluck Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Modulated Synth Pluck with Unison and an LFO Filter Sweep.
    """
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

    import reaper_python as RPR

    # === Step 1: Tempo & Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    base_pitch = 48 + NOTE_MAP.get(key, 0) # Root note around C3
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Chords ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # 4-bar progression: i, VI, III, VII (represented by scale degrees 0, 5, 2, 6)
    progression_degrees = [0, 5, 2, 6] 
    
    # Rhythmic syncopation pattern (1/16th note grid intervals per bar)
    # Stabs on beats: 1, 2.5, 3.5, 4 (in 16th steps: 0, 6, 10, 12)
    rhythm_steps = [0, 6, 10, 12]
    step_duration_16th = bar_length_sec / 16.0
    note_length_sec = step_duration_16th * 1.5 # Short MIDI notes, tail handled by ADSR
    
    total_notes = 0
    for bar in range(bars):
        root_deg = progression_degrees[bar % len(progression_degrees)]
        bar_start_time = bar * bar_length_sec
        
        for step in rhythm_steps:
            start_time = bar_start_time + (step * step_duration_16th)
            end_time = start_time + note_length_sec
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Stack a 4-note 7th chord
            for note_idx in [0, 2, 4, 6]:
                deg = (root_deg + note_idx) % len(scale_intervals)
                octave_shift = (root_deg + note_idx) // len(scale_intervals)
                pitch = base_pitch + scale_intervals[deg] + (12 * octave_shift)
                
                # Alternate velocity slightly for humanization
                vel = velocity_base - (step % 3) * 10
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, max(1, min(127, vel)), True)
                total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Synthesizer & ADSR Configuration ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.5)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)  # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)  # Attack: 0ms (Instant Pluck)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.15) # Decay: 150ms (Fast drop)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.1)  # Sustain: 10% (Quiet hold)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.2)  # Release: 200ms
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 1.0)  # Saw mix: 100% (Harmonically rich)

    # === Step 5: Unison via Chorus ===
    chorus_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 0, 15.0) # Delay length (ms)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 1, 0.6)  # Rate (Hz)
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 2, 2.5)  # Depth
    RPR.RPR_TrackFX_SetParam(track, chorus_idx, 3, 0.7)  # Wet Mix

    # === Step 6: LFO Filter Sweep ===
    filter_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Resonant Lowpass Filter", False, -1)
    # Param 0 is Cutoff (Hz), Param 1 is Resonance (0-1)
    RPR.RPR_TrackFX_SetParam(track, filter_idx, 1, 0.4) # Add slight resonance for a "juicy" sweep
    
    # Automate the Cutoff parameter to simulate an LFO
    env = RPR.RPR_GetFXEnvelope(track, filter_idx, 0, True)
    
    # Generate an LFO sine wave matching 1 bar duration
    lfo_rate_bars = 1.0 
    points_per_bar = 16 # Resolution of the automation
    
    for i in range(int(bars * points_per_bar) + 1):
        t = i * (bar_length_sec / points_per_bar)
        # Sine wave mapped from -1 to +1
        lfo_phase = math.sin(2 * math.pi * (t / (bar_length_sec * lfo_rate_bars)))
        
        # Map LFO to Hz: Center ~1500Hz, Depth ~1200Hz -> Range: 300Hz to 2700Hz
        cutoff_hz = 1500 + (1200 * lfo_phase)
        
        # Insert Envelope Point (Linear shape = 0)
        RPR.RPR_InsertEnvelopePoint(env, t, cutoff_hz, 0, 0.0, False, True)
        
    RPR.RPR_Envelope_SortPoints(env)

    # === Step 7: Space / Reverb ===
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.15) # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.85) # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.6)  # Room size
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 4, 0.2)  # Highpass

    return f"Created '{track_name}' (Saw Pluck w/ LFO Filter & Unison) with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
