def create_pattern(
    project_name: str = "TrapBeat_Template",
    track_name: str = "Trap Groove",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a 140BPM Half-Time Trap Drum Groove and an 808 bassline with 
    overlapping MIDI notes to trigger Portamento (glides) as shown in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (140 is standard for this style).
        key: Root note for the 808 bass (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
    """
    import reaper_python as RPR

    # --- Music Theory & MIDI Setup ---
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root note for 808 (Octave 2)
    root_pitch = 36 + NOTE_MAP.get(key.upper(), 0) # C2 is 36

    # General MIDI Drum Map
    KICK = 36
    SNARE = 38
    HAT = 42

    # --- Step 1: Project Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # PPQ (Pulses Per Quarter Note) usually 960 in REAPER
    PPQ = 960 
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def add_midi_track(name, is_drums=False):
        """Helper to create a track and a MIDI item."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def insert_note(take, start_beat, length_beats, pitch, vel):
        """Helper to insert a MIDI note using beat fractions."""
        start_ppq = int(start_beat * PPQ)
        end_ppq = int((start_beat + length_beats) * PPQ)
        # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # ==========================================
    # Step 2: Create Trap Drum Track
    # ==========================================
    drum_track, drum_take = add_midi_track(f"{track_name} Drums", is_drums=True)
    
    # Loop through bars to generate the drum pattern
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        
        # Kick Pattern: syncopated trap rhythm
        # Beats: 1, 1.75 (ah), 2.5 (and), 3.5 (and)
        insert_note(drum_take, bar_offset + 0.0, 0.25, KICK, velocity_base)
        insert_note(drum_take, bar_offset + 1.5, 0.25, KICK, velocity_base - 10)
        insert_note(drum_take, bar_offset + 2.0, 0.25, KICK, velocity_base)
        insert_note(drum_take, bar_offset + 3.5, 0.25, KICK, velocity_base - 10)
        
        # Snare/Clap Pattern: Half-time feel, strictly on Beat 3 (index 2.0)
        insert_note(drum_take, bar_offset + 2.0, 0.25, SNARE, velocity_base)
        
        # Hi-Hat Pattern: Continuous 8th notes (every 0.5 beats)
        for hat_step in range(8):
            hat_beat = bar_offset + (hat_step * 0.5)
            # Vary velocity slightly for groove
            hat_vel = velocity_base - 20 if hat_step % 2 == 0 else velocity_base - 35
            insert_note(drum_take, hat_beat, 0.25, HAT, hat_vel)
            
    RPR.RPR_MIDI_Sort(drum_take)

    # ==========================================
    # Step 3: Create 808 Glide Bass Track
    # ==========================================
    bass_track, bass_take = add_midi_track(f"{track_name} 808 Bass")
    
    for bar in range(bars):
        bar_offset = bar * beats_per_bar
        
        if bar % 2 == 0:
            # Standard downbeat 808
            insert_note(bass_take, bar_offset + 0.0, 1.5, root_pitch, velocity_base)
            insert_note(bass_take, bar_offset + 2.0, 1.0, root_pitch, velocity_base)
        else:
            # Turnaround bar with explicit overlapping notes for PORTAMENTO GLIDE
            # Base note plays from beat 0 to beat 1.5
            insert_note(bass_take, bar_offset + 0.0, 1.5, root_pitch, velocity_base)
            
            # The GLIDE Note: Triggers at 1.25, overlapping the previous note by 0.25 beats.
            # Jumps up an octave to force the synth to slide up.
            insert_note(bass_take, bar_offset + 1.25, 0.5, root_pitch + 12, velocity_base)
            
            # Lands back down
            insert_note(bass_take, bar_offset + 2.0, 1.0, root_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(bass_take)
    
    # Add a stock ReaSynth to the Bass track to provide immediate sub tone
    # It acts as a placeholder until the user loads an 808 sampler.
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a more 808-like sub sound (Triangle wave, lower cutoff)
    # Param 0: Volume, Param 1: Tuning, Param 2: Square mix, Param 6: Triangle mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.0) # Saw down
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 1.0) # Triangle up (subby)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 9, 0.5) # Release time

    return f"Created Trap Drums and 808 Bass tracks over {bars} bars at {bpm} BPM. Note: 808 track contains overlapping MIDI notes to trigger portamento/glides."
