def create_pattern(
    project_name: str = "Arrangement_Project",
    track_name: str = "Arrangement_Bus",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 20,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Subtractive Arrangement' demonstrating verse/chorus transitions
    in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Prefix for the generated stems.
        bpm: Tempo in BPM.
        key: Root note (e.g., 'C').
        scale: Scale type (e.g., 'minor').
        bars: Total arrangement length (default 20 to show all sections).
        velocity_base: Base MIDI velocity (0-127).
    """
    import reaper_python as RPR
    
    # === Step 1: Music Theory Data ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Normalize inputs
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # Start around C3
    
    # Helper: Build Diatonic Triads
    def get_chord(degree):
        notes = []
        for offset in [0, 2, 4]:
            idx = degree + offset
            octave = idx // 7
            scale_degree = idx % 7
            pitch = root_midi + (octave * 12) + scale_intervals[scale_degree]
            notes.append(pitch)
        return notes

    # Chord progression degrees: i - VI - III - VII (0-indexed: 0, 5, 2, 6)
    progression = [0, 5, 2, 6]

    # === Step 2: Setup REAPER Environment ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    
    def bar_to_sec(bar_num):
        return (bar_num - 1) * beats_per_bar * sec_per_beat

    # Helper: Track & MIDI Item creation
    def create_instrument_track(name, is_drum=False):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        # Add basic synth so it makes sound
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_to_sec(bars + 1))
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def add_note(take, pitch, start_bar, start_beat, length_beats, vel=100):
        start_sec = bar_to_sec(start_bar) + (start_beat - 1) * sec_per_beat
        end_sec = start_sec + (length_beats * sec_per_beat)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Create Tracks
    tk_chords = create_instrument_track("Chords")
    tk_lead = create_instrument_track("Lead")
    tk_bass = create_instrument_track("Bass")
    tk_kick = create_instrument_track("Kick", True)
    tk_snare = create_instrument_track("Snare", True)
    tk_hats = create_instrument_track("Hats", True)
    tk_riser = create_instrument_track("Riser")

    # === Step 3: Subtractive Arrangement Logic ===
    # Intro: 1-4 | Chorus: 5-12 | Verse 1A: 13-16 | Verse 1B: 17-20
    
    for bar in range(1, bars + 1):
        # 1. Progression Logic
        chord_idx = (bar - 1) % 4
        degree = progression[chord_idx]
        chord_notes = get_chord(degree)
        
        # Identify current section
        is_intro = (1 <= bar <= 4)
        is_chorus = (5 <= bar <= 12)
        is_verse_1a = (13 <= bar <= 16)
        is_verse_1b = (17 <= bar <= 20)
        
        # --- CHORDS (Plays everywhere to hold the track together) ---
        for note in chord_notes:
            add_note(tk_chords, note, bar, 1, 4, velocity_base - 20)
            
        # --- LEAD (Plays ONLY in Chorus, muted in verses for vocals) ---
        if is_chorus:
            # Simple rhythmic motif on the root and 5th
            add_note(tk_lead, root_midi + 12, bar, 1, 0.5, velocity_base)
            add_note(tk_lead, root_midi + 19, bar, 2.5, 0.5, velocity_base - 10)
            add_note(tk_lead, root_midi + 12, bar, 4, 1.0, velocity_base)

        # --- BASS (Muted in Intro and Verse 1A for contrast) ---
        if is_chorus or is_verse_1b:
            bass_note = chord_notes[0] - 12 # Octave down
            add_note(tk_bass, bass_note, bar, 1, 0.5, velocity_base + 10)
            add_note(tk_bass, bass_note, bar, 2.5, 1.0, velocity_base + 10)

        # --- DRUMS: KICK (Follows bass exactly) ---
        if is_chorus or is_verse_1b:
            add_note(tk_kick, 36, bar, 1, 0.5, velocity_base + 20)
            add_note(tk_kick, 36, bar, 2.5, 0.5, velocity_base + 10)

        # --- DRUMS: SNARE (Keeps time in Chorus and Verses) ---
        if is_chorus or is_verse_1a or is_verse_1b:
            add_note(tk_snare, 38, bar, 3, 0.5, velocity_base + 10)

        # --- DRUMS: HATS (Muted in Verse 1A. Transition stretch in Bar 20) ---
        if is_chorus or is_verse_1b:
            # Transition technique: "Half speed / stretched" pattern at the end of the verse
            step_size = 1.0 if bar == 20 else 0.5 
            
            beat = 1.0
            while beat <= 4.5:
                vel = velocity_base if (beat % 1 == 0) else velocity_base - 30
                add_note(tk_hats, 42, bar, beat, 0.25, vel)
                beat += step_size

        # --- RISER FX (Plays only at Bar 4, transitioning into the Chorus) ---
        if bar == 4:
            # Add a sustained high note
            add_note(tk_riser, root_midi + 24, bar, 1, 4, 100)
            
            # Automate MIDI CC 11 (Expression) for the swell effect
            start_sec = bar_to_sec(bar)
            end_sec = bar_to_sec(bar + 1)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk_riser, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(tk_riser, end_sec)
            
            cc_steps = 16
            for i in range(cc_steps + 1):
                cur_ppq = start_ppq + (end_ppq - start_ppq) * (i / cc_steps)
                # Exponential curve for smooth tension build
                val = int(127 * ((i / cc_steps) ** 2))
                RPR.RPR_MIDI_InsertCC(tk_riser, False, False, cur_ppq, 176, 0, 11, val)

    # Sort MIDI events for all takes
    for take in [tk_chords, tk_lead, tk_bass, tk_kick, tk_snare, tk_hats, tk_riser]:
        RPR.RPR_MIDI_Sort(take)

    return f"Created subtractive arrangement '{track_name}' spanning {bars} bars at {bpm} BPM in {key} {scale}. (Includes automated riser and half-time drum transition)."
