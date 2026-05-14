def create_pattern(
    project_name: str = "RNB_Project",
    track_name: str = "RNB_Foundation",
    bpm: int = 95,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a lush R&B Neo-Soul foundation featuring diatonic 7th chords, 
    a separate sub-bass layer, and a humanized drum groove.
    
    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo (defaults to 95 for R&B bounce).
        key: Root note (e.g., "E").
        scale: Scale type (e.g., "minor").
        bars: Number of bars for the progression (defaults to 4).
        velocity_base: Base velocity for chords/bass.
    """
    import reaper_python as RPR
    import random

    # 1. Music Theory Dictionaries
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
    }

    root_midi = NOTE_MAP.get(key.capitalize(), 4) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Common R&B progression (scale degrees, 0-indexed): i7 - v7 - VImaj7 - iv7
    progression = [0, 4, 5, 3] 

    def get_diatonic_7th_chord(degree, root_midi, scale_intervals):
        """Builds a 1-3-5-7 chord diatonic to the selected scale."""
        chord = []
        for offset in [0, 2, 4, 6]:
            idx = degree + offset
            octave_shift = idx // len(scale_intervals)
            note_idx = idx % len(scale_intervals)
            pitch = root_midi + scale_intervals[note_idx] + (octave_shift * 12)
            chord.append(pitch)
        return chord

    # 2. Setup Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Track creation helper
    def create_track_with_midi(name, bars, bpm):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # Calculate PPQ (Pulses Per Quarter Note)
    # REAPER default is usually 960 PPQ
    qn_per_bar = 4
    ppq = 960 
    ppq_per_bar = qn_per_bar * ppq

    # ==========================================
    # TRACK 1: EP CHORDS (7ths)
    # ==========================================
    chord_track, chord_take = create_track_with_midi(f"{track_name}_EP_Chords", bars, bpm)
    
    # Setup FX for Dark EP Tone
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaSynth", False, -1)
    # Reduce Saw, Increase Square for hollow EP sound
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 1, 0.0) # Saw mix
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 2, 0.8) # Square mix
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 6, 0.5) # Attack
    RPR.RPR_TrackFX_SetParam(chord_track, 0, 9, 0.6) # Release
    
    # Add Lowpass Filter
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, 1, 0, 0) # Band 1 Type (High Cut)
    RPR.RPR_TrackFX_SetParam(chord_track, 1, 1, 0.3) # Freq (Lowpass around 800Hz)
    
    # Add Reverb
    RPR.RPR_TrackFX_AddByName(chord_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(chord_track, 2, 0, 0.2) # Wet mix
    RPR.RPR_TrackFX_SetParam(chord_track, 2, 1, 0.8) # Room size
    
    RPR.RPR_SetMediaTrackInfo_Value(chord_track, "D_VOL", 0.6) # Lower volume

    # Insert Chord MIDI
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        chord = get_diatonic_7th_chord(degree, root_midi, scale_intervals)
        
        start_ppq = bar * ppq_per_bar
        end_ppq = start_ppq + ppq_per_bar - 10 # Slight gap for legato playing
        
        for pitch in chord:
            RPR.RPR_MIDI_InsertNote(chord_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base - 10, True)

    # ==========================================
    # TRACK 2: SUB BASS (Roots)
    # ==========================================
    bass_track, bass_take = create_track_with_midi(f"{track_name}_Sub_Bass", bars, bpm)
    
    # Setup FX for pure Sub
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.0) # Saw mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.0) # Square mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.0) # Triangle mix (pure sine remains)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.1) # Fast attack
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 9, 0.4) # Tight release

    # Insert Bass MIDI (Root notes dropped 1 octave)
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        root_pitch = get_diatonic_7th_chord(degree, root_midi, scale_intervals)[0] - 12
        
        start_ppq = bar * ppq_per_bar
        end_ppq = start_ppq + ppq_per_bar
        
        RPR.RPR_MIDI_InsertNote(bass_take, False, False, start_ppq, end_ppq, 0, root_pitch, velocity_base + 10, True)

    # ==========================================
    # TRACK 3: R&B DRUMS (Hats & Claps)
    # ==========================================
    drum_track, drum_take = create_track_with_midi(f"{track_name}_Drums", bars, bpm)
    
    clap_pitch = 39 # D1 (Standard GM Clap)
    hat_pitch = 42  # F#1 (Standard GM Closed Hat)
    
    for bar in range(bars):
        bar_start_ppq = bar * ppq_per_bar
        
        # Claps on beats 2 and 4
        for beat in [1, 3]: # 0-indexed: beat 1 is 2nd beat, beat 3 is 4th beat
            start_ppq = bar_start_ppq + (beat * ppq)
            end_ppq = start_ppq + int(ppq * 0.25)
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, clap_pitch, 110, True)
            
        # Humanized 1/8th note Hi-Hats
        for eighth in range(8):
            start_ppq = bar_start_ppq + int(eighth * (ppq / 2))
            end_ppq = start_ppq + int((ppq / 2) * 0.8) # Slight staccato
            
            # Randomized velocity mimicking human strum/feel (68 to 92 as per tutorial)
            humanized_vel = random.randint(68, 92)
            
            # Emphasize downbeats slightly more
            if eighth % 2 == 0:
                humanized_vel = min(127, humanized_vel + 15)
                
            RPR.RPR_MIDI_InsertNote(drum_take, False, False, start_ppq, end_ppq, 0, hat_pitch, humanized_vel, True)

    # Sort MIDI to ensure everything plays correctly
    RPR.RPR_MIDI_Sort(chord_take)
    RPR.RPR_MIDI_Sort(bass_take)
    RPR.RPR_MIDI_Sort(drum_take)

    # Update UI
    RPR.RPR_UpdateArrange()

    return f"Created R&B Neo-Soul Foundation: 3 tracks (Chords, Sub, Drums) over {bars} bars at {bpm} BPM in {key} {scale}."
