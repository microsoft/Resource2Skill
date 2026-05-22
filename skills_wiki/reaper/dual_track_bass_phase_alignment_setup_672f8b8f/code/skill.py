def create_pattern(
    project_name: str = "Phase_Alignment_Setup",
    track_name: str = "Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Dual-Track Bass Phase Alignment Setup in REAPER.
    Generates a DI track and an Amp track with a simulated phase delay,
    providing native tools (JS: Time Adjustment) to fix the phase relationship.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated bass bus.
        bpm: Tempo in BPM.
        key: Root note (e.g., "E").
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created setup.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # E1 is MIDI note 28. C1 is 24.
    root_pitch = 24 + NOTE_MAP.get(key.capitalize(), 4)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks (Folder Hierarchy) ===
    # We will create: Bass Bus -> [Bass DI, Bass Amp]
    start_idx = RPR.RPR_CountTracks(0)
    
    # 2a. Insert Bus Track
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    bus_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bus_track, "P_NAME", f"{track_name} Bus", True)
    RPR.RPR_SetMediaTrackInfo_Value(bus_track, "I_FOLDERDEPTH", 1) # Start folder
    
    # 2b. Insert DI Track
    RPR.RPR_InsertTrackAtIndex(start_idx + 1, True)
    di_track = RPR.RPR_GetTrack(0, start_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(di_track, "P_NAME", f"{track_name} DI", True)
    RPR.RPR_SetMediaTrackInfo_Value(di_track, "I_FOLDERDEPTH", 0) # Inside folder
    
    # 2c. Insert Amp Track
    RPR.RPR_InsertTrackAtIndex(start_idx + 2, True)
    amp_track = RPR.RPR_GetTrack(0, start_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(amp_track, "P_NAME", f"{track_name} Amp", True)
    RPR.RPR_SetMediaTrackInfo_Value(amp_track, "I_FOLDERDEPTH", -1) # End folder

    # === Step 3: Function to generate driving MIDI pattern ===
    def generate_bass_midi(track):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        
        beats_per_bar = 4
        bar_len_sec = (60.0 / bpm) * beats_per_bar
        item_length = bar_len_sec * bars
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        for bar in range(bars):
            for beat in range(4):
                for sub in range(2): # 8th notes
                    # Groove: Skip the upbeat of beat 3
                    if beat == 2 and sub == 1: 
                        continue

                    # Calculate timings
                    start_sec = (bar * bar_len_sec) + (beat * (60.0 / bpm)) + (sub * (30.0 / bpm))
                    # Staccato lengths for clear transients (16th note length = 15.0 / bpm)
                    end_sec = start_sec + (15.0 / bpm)

                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)

                    # Occasional perfect 5th jump for melodic interest
                    pitch = root_pitch
                    if beat == 3 and sub == 1:
                        pitch = root_pitch + 7 

                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
        RPR.RPR_MIDI_Sort(take)
        return item

    # Add identical MIDI to both tracks
    generate_bass_midi(di_track)
    generate_bass_midi(amp_track)

    # === Step 4: Sound Design & FX Chains ===
    
    # 4a. DI Setup (Clean sub-heavy tone)
    RPR.RPR_TrackFX_AddByName(di_track, "ReaSynth", False, -1)
    # Set ReaSynth: Mix to purely Triangle for a solid DI sub-fundamental
    RPR.RPR_TrackFX_SetParam(di_track, 0, 1, 0.0)  # Square = 0
    RPR.RPR_TrackFX_SetParam(di_track, 0, 2, 0.0)  # Saw = 0
    RPR.RPR_TrackFX_SetParam(di_track, 0, 3, 1.0)  # Triangle = 1.0
    RPR.RPR_TrackFX_SetParam(di_track, 0, 4, 0.0)  # Attack = fast
    
    # 4b. Amp Setup (Gritty, distorted top-end tone)
    RPR.RPR_TrackFX_AddByName(amp_track, "ReaSynth", False, -1)
    # Set ReaSynth: Mix to Sawtooth for harmonic richness
    RPR.RPR_TrackFX_SetParam(amp_track, 0, 1, 0.0)  # Square = 0
    RPR.RPR_TrackFX_SetParam(amp_track, 0, 2, 1.0)  # Saw = 1.0
    RPR.RPR_TrackFX_SetParam(amp_track, 0, 3, 0.0)  # Triangle = 0
    
    # Add stock Distortion
    RPR.RPR_TrackFX_AddByName(amp_track, "JS: Distortion", False, -1)
    # Increase distortion gain slightly
    RPR.RPR_TrackFX_SetParam(amp_track, 1, 0, 6.0) 

    # 4c. The Phase Alignment Tool (JS: Time Adjustment Delay)
    time_adj_idx = RPR.RPR_TrackFX_AddByName(amp_track, "JS: Time Adjustment Delay", False, -1)
    
    # Simulate a "mic distance" delay of 3.5 milliseconds, which throws the low E perfectly out of phase.
    # Parameter 0 in JS Time Adjustment is "Delay Amount (ms)"
    # By default, we leave this intentionally misaligned at 3.5ms so the user/agent can adjust it to 0ms to fix it.
    RPR.RPR_TrackFX_SetParam(amp_track, time_adj_idx, 0, 3.5)

    return f"Created Bass Bus with DI and Amp tracks. The Amp track has a 3.5ms delay offset. Use 'JS: Time Adjustment' on the Amp track to phase-align them."
