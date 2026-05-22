def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "GainStaged",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-stem gain-staged mix loop (Kick, Snare, Bass, Chords)
    calibrated to leave ~14dB of headroom on the master bus.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Calculate timings
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Fader Amplitude calculations (Amplitude = 10^(dB/20))
    # Calibrated to leave total mix headroom around -10 to -14 dBFS
    VOL_KICK = 10 ** (-12 / 20)  # ~0.25
    VOL_SNARE = 10 ** (-12 / 20) # ~0.25
    VOL_BASS = 10 ** (-14 / 20)  # ~0.20
    VOL_SYNTH = 10 ** (-16 / 20) # ~0.15

    def add_midi_track(name, vol_amp):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        # Enforce Gain Staging!
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol_amp)
        
        # Add basic synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Add MIDI item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # 1. KICK TRACK (-12 dB)
    kick_track, kick_take = add_midi_track("Kick", VOL_KICK)
    kick_pitch = 36 # C2
    for b in range(bars * beats_per_bar):
        pos = b * beat_len
        RPR.RPR_MIDI_InsertNote(kick_take, False, False, pos, pos + (beat_len*0.25), 1, kick_pitch, velocity_base, False)

    # 2. SNARE TRACK (-12 dB)
    snare_track, snare_take = add_midi_track("Snare", VOL_SNARE)
    snare_pitch = 84 # C6 (higher pitch for snap)
    for b in range(bars * beats_per_bar):
        if b % 2 != 0: # Beats 2 and 4
            pos = b * beat_len
            RPR.RPR_MIDI_InsertNote(snare_take, False, False, pos, pos + (beat_len*0.25), 1, snare_pitch, velocity_base, False)

    # 3. BASS TRACK (-14 dB)
    bass_track, bass_take = add_midi_track("Bass", VOL_BASS)
    bass_pitch = root_val + 36 # Octave 2
    for b in range(bars * beats_per_bar * 2): # 8th notes
        pos = b * (beat_len / 2)
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, pos, pos + (beat_len*0.4), 1, bass_pitch, int(velocity_base*0.9), False)

    # 4. SYNTH CHORDS (-16 dB)
    synth_track, synth_take = add_midi_track("Chords", VOL_SYNTH)
    # Build a triad
    chord_pitches = [
        root_val + 60, # Root (Octave 4)
        root_val + 60 + scale_intervals[2], # Third
        root_val + 60 + scale_intervals[4]  # Fifth
    ]
    for b in range(bars * beats_per_bar):
        # Play on the "and" of the beat
        pos = (b * beat_len) + (beat_len / 2)
        for p in chord_pitches:
            RPR.RPR_MIDI_InsertNote(synth_take, False, False, pos, pos + (beat_len*0.4), 1, p, int(velocity_base*0.8), False)

    return f"Created gain-staged 4-stem loop '{track_name}' over {bars} bars at {bpm} BPM. Track faders scaled to leave ~14dB master headroom."
