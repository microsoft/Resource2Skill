def create_pattern(
    project_name: str = "MultiTrackBand",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Rock/Metal Band arrangement (Drums, Bass, Rhythm, Lead)
    in the current REAPER project following a classic i-VI-III-VII progression.
    """
    import reaper_python as RPR

    # --- Music Theory & Settings ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key.capitalize(), 11) # Default to B
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Progression: i - VI - III - VII (Relative indices in the scale)
    progression_indices = [0, 5, 2, 6] 

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Helper function to get absolute MIDI pitch
    def get_chord_tones(degree_idx, octave):
        # degree_idx is 0-indexed relative to the scale
        scale_degree = degree_idx % 7
        octave_offset = degree_idx // 7
        root = root_val + scale_intervals[scale_degree] + (12 * (octave + octave_offset))
        
        # Build triad (1, 3, 5)
        third_idx = (degree_idx + 2) % 7
        third_oct_offset = (degree_idx + 2) // 7
        third = root_val + scale_intervals[third_idx] + (12 * (octave + third_oct_offset))
        
        fifth_idx = (degree_idx + 4) % 7
        fifth_oct_offset = (degree_idx + 4) // 7
        fifth = root_val + scale_intervals[fifth_idx] + (12 * (octave + fifth_oct_offset))
        
        return [root, third, fifth]

    # --- Track Definitions ---
    # Colors encoded using OS-native color formats (R|G|B)
    def rgb_to_native(r, g, b):
        return r + (g << 8) + (b << 16) | 0x1000000

    tracks_config = [
        {"name": "Drums", "color": rgb_to_native(50, 150, 255), "role": "drums"},
        {"name": "Bass", "color": rgb_to_native(150, 50, 255), "role": "bass"},
        {"name": "GTR Rhy", "color": rgb_to_native(255, 150, 50), "role": "rhythm"},
        {"name": "GTR Lead", "color": rgb_to_native(50, 255, 150), "role": "lead"},
    ]

    track_count = RPR.RPR_CountTracks(0)
    
    for i, config in enumerate(tracks_config):
        track_idx = track_count + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Set Track Properties
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", config["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", config["color"])
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Turn down to avoid master clip
        
        # Add basic Synth for tonal tracks
        if config["role"] != "drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Create Item & Take
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # --- Generate MIDI based on Role ---
        for bar in range(bars):
            chord_idx = progression_indices[bar % len(progression_indices)]
            bar_start_time = bar * bar_length_sec
            
            if config["role"] == "drums":
                # Standard rock backbeat
                eighth_sec = (60.0 / bpm) / 2.0
                for e in range(8):
                    beat_pos = bar_start_time + (e * eighth_sec)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos + (eighth_sec * 0.8))
                    
                    # Hi-hat on every 8th note
                    hat_vel = velocity_base if e % 2 == 0 else velocity_base - 20
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, 42, hat_vel, False)
                    
                    # Kick on 1 and 3 (0 and 4 in 8th notes) + syncopated kick on 8th note before 3
                    if e in [0, 3, 4]:
                        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, 36, velocity_base, False)
                    
                    # Snare on 2 and 4 (2 and 6 in 8th notes)
                    if e in [2, 6]:
                        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, 38, velocity_base, False)
                        
            elif config["role"] == "bass":
                # Driving 8th notes on the root (Octave 2)
                chord_tones = get_chord_tones(chord_idx, 2)
                root_note = chord_tones[0]
                eighth_sec = (60.0 / bpm) / 2.0
                
                for e in range(8):
                    beat_pos = bar_start_time + (e * eighth_sec)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos + (eighth_sec * 0.9))
                    vel = velocity_base if e % 2 == 0 else velocity_base - 15
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_note, vel, False)

            elif config["role"] == "rhythm":
                # Sustained chords (Octave 3)
                chord_tones = get_chord_tones(chord_idx, 3)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time + bar_length_sec - 0.05)
                
                for note in chord_tones:
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base - 10, False)

            elif config["role"] == "lead":
                # Arpeggios 2 octaves up (Octave 5)
                chord_tones = get_chord_tones(chord_idx, 5)
                arp_pattern = [chord_tones[0], chord_tones[1], chord_tones[2], chord_tones[0] + 12] # Upward arp
                eighth_sec = (60.0 / bpm) / 2.0
                
                for e in range(8):
                    note = arp_pattern[e % len(arp_pattern)]
                    beat_pos = bar_start_time + (e * eighth_sec)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_pos + (eighth_sec * 0.8))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base + 5, False)

        RPR.RPR_MIDI_Sort(take)

    RPR.RPR_UpdateArrange()
    return f"Created 4-track Band Arrangement (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
