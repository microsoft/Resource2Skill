def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Groovy Slap Bass",
    bpm: int = 105,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a humanized, syncopated slap bassline pattern with octaves and walk-ups.
    """
    import random
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a basic placeholder synth for the bass sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music Theory Setup
    # MIDI Octave 2 (36 = C2). Great range for bass.
    root_pitch = NOTE_MAP.get(key, 0) + 36 
    
    notes_added = 0

    def add_humanized_note(start_qn, length_qn, pitch, target_vel, is_slap=False):
        nonlocal notes_added
        
        # 1. Imitate Reality: Timing Offsets
        # Normal notes have slight swing, slaps are slightly laid back
        timing_offset = random.uniform(-0.015, 0.02) if not is_slap else random.uniform(0.005, 0.025)
        actual_start_qn = max(0.0, start_qn + timing_offset)
        
        # 2. Shorten for Slap Feel (staccato gaps)
        actual_length_qn = length_qn * random.uniform(0.7, 0.85)
        actual_end_qn = actual_start_qn + actual_length_qn

        # Convert QN to project time -> PPQ
        start_time = (actual_start_qn * 60.0) / bpm
        end_time = (actual_end_qn * 60.0) / bpm
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        # 3. Velocity Humanization
        # Slap notes trigger highest velocity layers, ghost notes are quiet
        vel_fluctuation = random.randint(-4, 4)
        actual_vel = max(1, min(127, int(target_vel + vel_fluctuation)))

        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, actual_vel, False)
        notes_added += 1

    # Generate Groove Pattern
    for bar in range(bars):
        bar_qn = bar * 4.0
        
        if bar % 2 == 0:
            # --- Pattern A: The Primary Groove ---
            # Strong downbeat root
            add_humanized_note(bar_qn + 0.0, 0.5, root_pitch, velocity_base)
            
            # Syncopated Octave "Slap" on the 1.75
            add_humanized_note(bar_qn + 1.75, 0.25, root_pitch + 12, 127, is_slap=True)
            
            # Second strong beat
            add_humanized_note(bar_qn + 2.5, 0.5, root_pitch, velocity_base - 5)
            
            # Syncopated Octave "Slap"
            add_humanized_note(bar_qn + 3.25, 0.25, root_pitch + 12, 120, is_slap=True)
            
            # Approach note back to root (Minor 7th / Whole step down)
            add_humanized_note(bar_qn + 3.75, 0.25, root_pitch - 2, 85)
            
        else:
            # --- Pattern B: The Walk-Up ---
            # Strong downbeat root
            add_humanized_note(bar_qn + 0.0, 0.5, root_pitch, velocity_base + 5)
            
            # Syncopated Octave "Slap"
            add_humanized_note(bar_qn + 1.5, 0.25, root_pitch + 12, 127, is_slap=True)
            
            # "Add some steps up to the root notes"
            # Walkup from the 4th degree below the root
            add_humanized_note(bar_qn + 2.5, 0.25, root_pitch - 5, 80)  # Perfect 4th below
            add_humanized_note(bar_qn + 3.0, 0.25, root_pitch - 4, 85)  # Major 3rd below
            add_humanized_note(bar_qn + 3.5, 0.25, root_pitch - 2, 95)  # Minor 7th / Step below
            
            # Final chromatic step right before the next downbeat
            add_humanized_note(bar_qn + 3.75, 0.25, root_pitch - 1, 105)

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} humanized notes (octaves, slaps, walk-ups) over {bars} bars at {bpm} BPM in {key} {scale}."
