import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a basic rock groove with synchronized MIDI for drums, bass, rhythm guitar, and lead.

    This skill demonstrates a multi-instrument MIDI arrangement, including:
    - A 4-bar rock chord progression (Am-G-C-F or similar)
    - Synchronized drum beat (kick, snare, hi-hats)
    - Bass line following chord roots
    - Rhythm guitar playing power chords
    - Lead guitar playing a simple arpeggiated melody

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (minimum 4 for full progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Drums', 'Bass', 'Rhythm Guitar', 'Lead Guitar' with MIDI notes."
    """

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
    
    # Drum MIDI Notes (General MIDI Standard)
    KICK = 36 # C1
    SNARE = 38 # D1
    CLOSED_HIHAT = 42 # F#1
    CRASH = 49 # C#2

    # Basic rock progression (Am - G - C - F) relative to the chosen key's root
    # Chord progression roots (scale degrees in chosen scale)
    # Using scale degrees: 0 (tonic), 5 (dominant), 3 (subtonic), 4 (mediant) for A minor (Am-G-C-F-ish)
    CHORD_PROGRESSION_SCALE_DEGREES = [0, 5, 3, 4] 
    
    # Ensure a minimum of 4 bars for the progression to loop correctly
    actual_bars = max(4, bars)

    RPR.Undo_BeginBlock2(0) # Begin undo block
    
    try:
        # === Step 1: Set Tempo ===
        RPR.RPR_SetCurrentBPM(0, bpm, False)

        # === Step 2 & 3: Create Tracks & MIDI Items ===
        track_names = ["MIDI Drums", "MIDI Bass", "GTR RHY", "GTR LEAD"]
        tracks = []
        midi_items = []
        for name in track_names:
            track_idx = RPR.RPR_CountTracks(0)
            RPR.RPR_InsertTrackAtIndex(track_idx, True)
            track = RPR.RPR_GetTrack(0, track_idx)
            RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
            tracks.append(track)

            # Create MIDI item for 4 bars, set to loop
            item = RPR.RPR_AddMediaItemToTrack(track)
            RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
            RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", 4.0 * 4.0) # 4 beats per bar, 4 bars
            RPR.RPR_SetMediaItemInfo_Value(item, "B_LOOPSRC", 1.0) # Loop source
            midi_items.append(item)

            take = RPR.RPR_AddTakeToMediaItem(item)
            if not take:
                RPR.RPR_ShowConsoleMsg("Failed to add take to media item. Skipping MIDI insertion for this track.\n")
                continue
            # Ensure it's a blank MIDI take for note insertion
            RPR.RPR_MIDI_SetItemExt(take, "", 0, 0, 0)
            
            # Activate the take for MIDI editing
            RPR.RPR_SetMediaItemTakeInfo_Value(take, "I_ACTIVE", 1)


        # Function to get absolute MIDI note from root, scale degree, and octave
        def get_midi_note(base_key_root: int, scale_degree: int, octave: int = 3) -> int:
            if scale not in SCALES:
                RPR.RPR_ShowConsoleMsg(f"Scale '{scale}' not found. Using major scale fallback.\n")
                scale_intervals = SCALES["major"] # Fallback
            else:
                scale_intervals = SCALES[scale]
            
            # Calculate root of the current chord based on project key and scale degree
            chord_root_midi = base_key_root + scale_intervals[scale_degree % len(scale_intervals)]
            
            # Map scale degree to interval within that specific chord's scale
            # For simplicity, we are using the project's scale intervals for arpeggio building
            # You might want specific chord intervals for richer harmony
            
            return chord_root_midi + (octave * 12)

        # Get the MIDI root of the project's key (e.g., A for A minor)
        project_key_root_midi = NOTE_MAP[key]

        # Loop through each bar to insert MIDI notes
        for bar in range(actual_bars):
            # Calculate the root of the current chord in the progression
            current_chord_scale_degree = CHORD_PROGRESSION_SCALE_DEGREES[bar % len(CHORD_PROGRESSION_SCALE_DEGREES)]
            current_chord_root_midi = get_midi_note(project_key_root_midi, current_chord_scale_degree, 0) # Base octave for chord root calc

            # --- Drums (Track 0) ---
            midi_take_drums = RPR.RPR_GetActiveTake(midi_items[0])
            if midi_take_drums:
                # Kick (on 1, 1.5, 3, 3.5)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0, 0.25, velocity_base + 10, True, KICK, True)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + 1.5, 0.25, velocity_base + 5, True, KICK, True)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + 2.0, 0.25, velocity_base + 10, True, KICK, True)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + 3.5, 0.25, velocity_base + 5, True, KICK, True)

                # Snare (on 2 and 4)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + 1.0, 0.25, velocity_base + 15, True, SNARE, True)
                RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + 3.0, 0.25, velocity_base + 15, True, SNARE, True)

                # Closed Hi-Hat (every 8th note)
                for beat_offset in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
                    RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0 + beat_offset, 0.25, velocity_base - 10, True, CLOSED_HIHAT, True)
                
                # Crash on the first beat of the first bar
                if bar == 0:
                     RPR.RPR_MIDI_InsertNote(midi_take_drums, False, False, bar * 4.0, 1.0, velocity_base + 20, True, CRASH, True)

            # --- Bass (Track 1) ---
            midi_take_bass = RPR.RPR_GetActiveTake(midi_items[1])
            if midi_take_bass:
                bass_root_note = get_midi_note(current_chord_root_midi, 0, 2) # Octave 2
                RPR.RPR_MIDI_InsertNote(midi_take_bass, False, False, bar * 4.0, 4.0, velocity_base + 5, True, bass_root_note, True) # Full bar sustained root

            # --- Rhythm Guitar (Track 2) ---
            midi_take_rhy = RPR.RPR_GetActiveTake(midi_items[2])
            if midi_take_rhy:
                # Power chord: Root, 5th, Octave
                rhy_root_note = get_midi_note(current_chord_root_midi, 0, 3) # Octave 3
                rhy_5th_note = rhy_root_note + 7
                rhy_octave_note = get_midi_note(current_chord_root_midi, 0, 4) # Octave 4

                # Strummed power chords on beats 1 and 3 (quarter notes)
                for beat_start in [0.0, 2.0]:
                    # Root
                    RPR.RPR_MIDI_InsertNote(midi_take_rhy, False, False, bar * 4.0 + beat_start, 0.5, velocity_base + 10, True, rhy_root_note, True)
                    # 5th (slightly offset for strumming effect)
                    RPR.RPR_MIDI_InsertNote(midi_take_rhy, False, False, bar * 4.0 + beat_start + 0.05, 0.5, velocity_base + 10, True, rhy_5th_note, True)
                    # Octave (slightly more offset)
                    RPR.RPR_MIDI_InsertNote(midi_take_rhy, False, False, bar * 4.0 + beat_start + 0.1, 0.5, velocity_base + 10, True, rhy_octave_note, True)

            # --- Lead Guitar (Track 3) ---
            midi_take_lead = RPR.RPR_GetActiveTake(midi_items[3])
            if midi_take_lead:
                # Simple arpeggiated line from the chord
                # Arpeggio pattern over a bar (8th notes): Root, 2nd, 3rd, 5th, 3rd, 2nd, Root (octave up), 2nd (octave up)
                arpeggio_pattern_degrees = [0, 1, 2, 4, 2, 1, 0, 1] 
                
                for i, scale_degree_offset in enumerate(arpeggio_pattern_degrees):
                    note_time = bar * 4.0 + (i * 0.5) # Every 8th note
                    
                    # Adjust octave for lead melody
                    octave_offset = 0
                    if i >= 6: # Last two notes an octave higher for melodic climb
                        octave_offset = 1 
                        
                    lead_note = get_midi_note(current_chord_root_midi, scale_degree_offset, 4 + octave_offset) # Octave 4/5
                    
                    RPR.RPR_MIDI_InsertNote(midi_take_lead, False, False, note_time, 0.5, velocity_base + 10, True, lead_note, True)


        # === Step 4: Add FX Chain (Basic ReaSynth/ReaSamplOmatic5000) ===
        # Drums: ReaSamplOmatic5000
        RPR.RPR_TrackFX_AddByName(tracks[0], "ReaSamplOmatic5000", False, -1)
        
        # Bass, Rhythm Guitar, Lead Guitar: ReaSynth
        RPR.RPR_TrackFX_AddByName(tracks[1], "ReaSynth", False, -1)
        RPR.RPR_TrackFX_AddByName(tracks[2], "ReaSynth", False, -1)
        RPR.RPR_TrackFX_AddByName(tracks[3], "ReaSynth", False, -1)
        
        # Basic Panning for guitars
        RPR.RPR_SetMediaTrackInfo_Value(tracks[2], "D_PAN", -0.3) # Rhythm Left
        RPR.RPR_SetMediaTrackInfo_Value(tracks[3], "D_PAN", 0.3) # Lead Right

        return f"Created '{', '.join(track_names)}' with MIDI notes for a {actual_bars}-bar rock groove at {bpm} BPM."

    except Exception as e:
        RPR.RPR_ShowConsoleMsg(f"Error creating pattern: {e}\n")
        return f"Error creating pattern: {e}"

    finally:
        RPR.Undo_EndBlock2(0, "Create Multi-Instrument MIDI Arrangement", -1)

