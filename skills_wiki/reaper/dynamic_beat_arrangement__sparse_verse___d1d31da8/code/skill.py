def create_pattern(
    project_name: str = "Wodzu Arrangement",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16, # Fixed to 16 to demonstrate the specific Intro/Chorus/Verse structure
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a dynamic Hip-Hop/Trap arrangement structure (Intro, Chorus, Sparse Verse) 
    featuring white-noise risers and filter-sweep transitions.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
    }

    # Setup project timing
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4.0

    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Deriving basic pitches for placeholder arrangement
    root_bass = root_val + 36 # C2
    chord_notes = [root_val + 48, root_val + 48 + scale_intervals[2], root_val + 48 + scale_intervals[4]] # Triad
    lead_notes = [root_val + 72, root_val + 72 + scale_intervals[2], root_val + 72 + scale_intervals[4]] # Arp notes

    # --- Helper: Insert Track ---
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    # --- Helper: Insert MIDI Note ---
    def insert_note(take, start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # --- Helper: Create MIDI Item with Grid logic ---
    def create_midi_item(track, start_bar, end_bar, pattern_type):
        start_sec = start_bar * bar_len
        end_sec = end_bar * bar_len
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_sec)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", end_sec - start_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Populate based on pattern type
        num_bars = end_bar - start_bar
        for b in range(num_bars):
            bar_start = start_sec + (b * bar_len)
            
            if pattern_type == "chords":
                for note in chord_notes:
                    insert_note(take, bar_start, bar_start + bar_len, note, velocity_base - 20)
            
            elif pattern_type == "lead":
                for i, note in enumerate(lead_notes * 2): # 8th note run
                    n_start = bar_start + (i * beat_len * 0.5)
                    insert_note(take, n_start, n_start + (beat_len * 0.25), note, velocity_base)
            
            elif pattern_type == "bass":
                # Boom bap / Trap sparse sub bass
                insert_note(take, bar_start, bar_start + (beat_len * 1.5), root_bass, velocity_base)
                insert_note(take, bar_start + (beat_len * 2.5), bar_start + (beat_len * 3.5), root_bass, velocity_base)

            elif pattern_type == "drums_full":
                # Kick (36), Snare (38), Hat (42)
                insert_note(take, bar_start, bar_start + 0.1, 36, velocity_base) # Kick 1
                insert_note(take, bar_start + (beat_len * 2.5), bar_start + (beat_len * 2.5) + 0.1, 36, velocity_base) # Kick syncopated
                insert_note(take, bar_start + beat_len, bar_start + beat_len + 0.1, 38, velocity_base) # Snare 2
                insert_note(take, bar_start + (beat_len*3), bar_start + (beat_len*3) + 0.1, 38, velocity_base) # Snare 4
                for i in range(8): # 8th note hats
                    insert_note(take, bar_start + (i * beat_len * 0.5), bar_start + (i * beat_len * 0.5) + 0.05, 42, velocity_base - 15)

            elif pattern_type == "drums_sparse":
                # Verse A (Subtraction): NO Kicks, NO Hats. Just snare on 2 and 4 to keep the core time.
                insert_note(take, bar_start + beat_len, bar_start + beat_len + 0.1, 38, velocity_base - 10) 
                insert_note(take, bar_start + (beat_len*3), bar_start + (beat_len*3) + 0.1, 38, velocity_base - 10) 

            elif pattern_type == "riser_midi":
                # Hold a single C4 note to trigger the noise synth
                insert_note(take, bar_start, bar_start + bar_len, 60, velocity_base)

        RPR.RPR_MIDI_Sort(take)
        return item

    # ==========================================
    # 1. CREATE TRACKS & ARRANGEMENT BLOCKS
    # ==========================================
    
    # Track 1: Chords (Plays throughout)
    tr_chords = add_track("Chords_Bus")
    RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    create_midi_item(tr_chords, 0, 16, "chords")

    # Track 2: Lead (Only in Chorus)
    tr_lead = add_track("Lead_Melody")
    RPR.RPR_TrackFX_AddByName(tr_lead, "ReaSynth", False, -1)
    create_midi_item(tr_lead, 4, 8, "lead")    # Chorus 1
    # Notice it is omitted from bars 8-16 (The Verse) to leave room for vocals

    # Track 3: Drums
    tr_drums = add_track("Drums")
    create_midi_item(tr_drums, 4, 8, "drums_full")     # Chorus 1
    create_midi_item(tr_drums, 8, 12, "drums_sparse")  # Verse A (Sparse)
    create_midi_item(tr_drums, 12, 16, "drums_full")   # Verse B (Build back up)

    # Track 4: Bass
    tr_bass = add_track("Sub_Bass")
    RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)
    create_midi_item(tr_bass, 4, 8, "bass")    # Chorus 1
    # Omitted from 8-12 (Verse A)
    create_midi_item(tr_bass, 12, 16, "bass")  # Verse B
    
    # ==========================================
    # 2. FX TRANSITIONS & AUTOMATION
    # ==========================================

    # --- A. The Noise Riser ---
    tr_riser = add_track("Noise_Riser_FX")
    fx_synth = RPR.RPR_TrackFX_AddByName(tr_riser, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_riser, fx_synth, 1, 0.0) # Saw mix = 0
    RPR.RPR_TrackFX_SetParamNormalized(tr_riser, fx_synth, 5, 1.0) # Noise mix = 1
    
    fx_verb = RPR.RPR_TrackFX_AddByName(tr_riser, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(tr_riser, fx_verb, 1, 0.9) # Huge Room Size
    RPR.RPR_TrackFX_SetParamNormalized(tr_riser, fx_verb, 4, 0.6) # Wet mix

    # Riser runs for 1 bar before each Chorus
    create_midi_item(tr_riser, 3, 4, "riser_midi")
    create_midi_item(tr_riser, 15, 16, "riser_midi")

    # Automate Riser Volume (Fade in)
    RPR.RPR_SetMediaTrackInfo_Value(tr_riser, "I_AUTOMODE", 1) # Read mode
    env_vol = RPR.RPR_GetTrackEnvelopeByName(tr_riser, "Volume")
    
    # Points for Riser 1 (Bar 3 to 4)
    time_b3 = 3 * bar_len
    time_b4 = 4 * bar_len
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b3, 0.0, 0, 0, False, True)       # -inf dB
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b4, 1.0, 0, 0, False, True)       # 0 dB
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b4 + 0.01, 0.0, 0, 0, False, True)# Instant cut

    # Points for Riser 2 (Bar 15 to 16)
    time_b15 = 15 * bar_len
    time_b16 = 16 * bar_len
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b15, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b16, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_vol, time_b16 + 0.01, 0.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortDsts(env_vol)

    # --- B. The "Sawtooth" Filter Sweep on Chords ---
    # Adds an EQ to the chords and violently pulls down high frequencies 1 beat before the chorus
    eq_idx = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaEQ", False, -1)
    
    # Param 10 in ReaEQ is Band 4 Gain. We will drop the high shelf gain to emulate the filter drop.
    env_filt = RPR.RPR_GetFXEnvelope(tr_chords, eq_idx, 10, True) 
    
    if env_filt:
        # Neutral state
        RPR.RPR_InsertEnvelopePoint(env_filt, 0, 0.5, 0, 0, False, True) # 0.5 normalized = 0dB
        
        # At Bar 15, Beat 3 (Starts pulling down)
        sweep_start = time_b15 + (beat_len * 2)
        RPR.RPR_InsertEnvelopePoint(env_filt, sweep_start, 0.5, 0, 0, False, True)
        
        # Right before Bar 16 (Suffocated / Low passed)
        sweep_bottom = time_b16 - 0.05
        RPR.RPR_InsertEnvelopePoint(env_filt, sweep_bottom, 0.0, 0, 0, False, True) # 0.0 = -24dB cutoff
        
        # Downbeat of Bar 16 (Explodes back open)
        RPR.RPR_InsertEnvelopePoint(env_filt, time_b16, 0.5, 0, 0, False, True)
        RPR.RPR_Envelope_SortDsts(env_filt)

    RPR.RPR_UpdateTimeline()
    RPR.RPR_TrackList_AdjustWindows(False)

    return f"Created Dynamic Arrangement ({bars} bars at {bpm} BPM) featuring Intro, Chorus, Verse A (Sparse), Verse B, Risers, and Filter transitions."
