import reaper_python as RPR

def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    intro_bars: int = 8,
    chorus_bars: int = 4,
    verse_bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates EDM intro, pumping chorus, and verse segments in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        intro_bars: Number of bars for the intro build-up segment.
        chorus_bars: Number of bars for the main chorus segment.
        verse_bars: Number of bars for the verse segment.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'EDM Pattern' with intro, chorus, and verse segments."
    """
    # Music theory lookup tables (C Major for this pattern)
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # MIDI note mappings for drum sounds (ReaSamplOmatic5000 defaults)
    DRUM_KICK = 36 # C1
    DRUM_SNARE = 38 # D1
    DRUM_HIHAT = 42 # F#1

    # Base MIDI note for C3 (Middle C is 60, C2 is 48, C1 is 36)
    root_midi = NOTE_MAP[key]

    # Helper to calculate absolute MIDI pitch
    def get_abs_midi(octave, semitones_from_C):
        return (octave * 12) + semitones_from_C

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_names = ["Piano Melody", "Piano Chords", "Bass", "Drums", "SD Kick Boost"]
    tracks = {}
    for name in track_names:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track
        
    # Mute "SD Kick Boost" track audio output (only used for sidechain trigger)
    RPR.RPR_SetMediaTrackInfo_Value(tracks["SD Kick Boost"], "D_VOL", 0.0)

    # === Step 3: Add Instruments (ReaSynth/ReaSamplOmatic5000) ===
    # Piano Melody
    RPR.RPR_TrackFX_AddByName(tracks["Piano Melody"], "ReaSynth", False, -1)
    # Piano Chords
    RPR.RPR_TrackFX_AddByName(tracks["Piano Chords"], "ReaSynth", False, -1)
    # Bass
    RPR.RPR_TrackFX_AddByName(tracks["Bass"], "ReaSynth", False, -1)
    # Drums (ReaSamplOmatic5000 - basic kit)
    RPR.RPR_TrackFX_AddByName(tracks["Drums"], "ReaSamplOmatic5000", False, -1)

    # === Step 4: Add FX (ReaEQ & ReaComp) and Sidechain Routing ===
    # Piano Chords: ReaEQ (Low-pass) and ReaComp (Sidechain)
    RPR.RPR_TrackFX_AddByName(tracks["Piano Chords"], "ReaEQ", False, -1)
    chords_eq_fx_idx = RPR.RPR_TrackFX_GetFXIdxByName(tracks["Piano Chords"], "ReaEQ", False)
    RPR.RPR_TrackFX_AddByName(tracks["Piano Chords"], "ReaComp", False, -1)
    chords_comp_fx_idx = RPR.RPR_TrackFX_GetFXIdxByName(tracks["Piano Chords"], "ReaComp", False)

    # Bass: ReaComp (Sidechain)
    RPR.RPR_TrackFX_AddByName(tracks["Bass"], "ReaComp", False, -1)
    bass_comp_fx_idx = RPR.RPR_TrackFX_GetFXIdxByName(tracks["Bass"], "ReaComp", False)

    # Sidechain Routing: SD Kick Boost -> Piano Chords/Bass (Aux 3/4)
    sd_kick_track_idx = RPR.RPR_GetMediaTrackInfo_Value(tracks["SD Kick Boost"], "T_INDEX")
    
    # Send from SD Kick Boost to Piano Chords (channels 1/2 to 3/4)
    RPR.RPR_CreateTrackSend(tracks["SD Kick Boost"], tracks["Piano Chords"])
    send_idx = RPR.RPR_GetTrackSendInfo_Set(tracks["SD Kick Boost"], tracks["Piano Chords"], 0, "I_SRCCHAN", 2) # Use channels 3/4 from source
    RPR.RPR_GetTrackSendInfo_Set(tracks["SD Kick Boost"], tracks["Piano Chords"], 0, "I_DSTCHAN", 2) # Use channels 3/4 as destination

    # Send from SD Kick Boost to Bass (channels 1/2 to 3/4)
    RPR.RPR_CreateTrackSend(tracks["SD Kick Boost"], tracks["Bass"])
    send_idx = RPR.RPR_GetTrackSendInfo_Set(tracks["SD Kick Boost"], tracks["Bass"], 0, "I_SRCCHAN", 2) # Use channels 3/4 from source
    RPR.RPR_GetTrackSendInfo_Set(tracks["SD Kick Boost"], tracks["Bass"], 0, "I_DSTCHAN", 2) # Use channels 3/4 as destination

    # Configure ReaComp for sidechain
    # Piano Chords ReaComp
    if chords_comp_fx_idx != -1:
        RPR.RPR_TrackFX_SetParam(tracks["Piano Chords"], chords_comp_fx_idx, 0, 0.4)  # Threshold (-20dB normalized to 0-1)
        RPR.RPR_TrackFX_SetParam(tracks["Piano Chords"], chords_comp_fx_idx, 2, 0.25) # Ratio (4:1 normalized to 0-1)
        RPR.RPR_TrackFX_SetParam(tracks["Piano Chords"], chords_comp_fx_idx, 3, 0.001/0.1) # Attack (0.001s normalized to 0-0.1s range)
        RPR.RPR_TrackFX_SetParam(tracks["Piano Chords"], chords_comp_fx_idx, 4, 0.1/1.0) # Release (0.1s normalized to 0-1s range)
        RPR.RPR_TrackFX_SetParam(tracks["Piano Chords"], chords_comp_fx_idx, 20, 1.0) # Wet (100%)
        # Set detector input to Aux (channels 3/4) - this often requires specific ReaComp presets or direct ReaScript FX parameter manipulation which is complex.
        # For simplicity, we assume the user might manually set "Detector Input: Auxiliary input L+R" in ReaComp.
        # There isn't a direct ReaScript function to select "Auxiliary Input" for ReaComp's detector.
        # This part might need manual adjustment or a custom JSFX.
        # For now, the routing is set up, implying sidechain readiness.

    # Bass ReaComp (similar settings)
    if bass_comp_fx_idx != -1:
        RPR.RPR_TrackFX_SetParam(tracks["Bass"], bass_comp_fx_idx, 0, 0.4)  # Threshold
        RPR.RPR_TrackFX_SetParam(tracks["Bass"], bass_comp_fx_idx, 2, 0.25) # Ratio
        RPR.RPR_TrackFX_SetParam(tracks["Bass"], bass_comp_fx_idx, 3, 0.001/0.1) # Attack
        RPR.RPR_TrackFX_SetParam(tracks["Bass"], bass_comp_fx_idx, 4, 0.1/1.0) # Release
        RPR.RPR_TrackFX_SetParam(tracks["Bass"], bass_comp_fx_idx, 20, 1.0) # Wet (100%)
        # Same note on manual "Detector Input: Auxiliary input L+R" setting.

    # === Step 5: Create MIDI Items and Notes ===
    beat_len = 60.0 / bpm
    quarter_note = beat_len
    eighth_note = quarter_note / 2

    # Chord progression: Cmaj7 - Gmaj - Amin - Fmaj (in C Major)
    chords_data = [
        ([get_abs_midi(3, root_midi + 0), get_abs_midi(3, root_midi + 4), get_abs_midi(3, root_midi + 7), get_abs_midi(3, root_midi + 11)], "Cmaj7"),
        ([get_abs_midi(3, root_midi + 7), get_abs_midi(3, root_midi + 11), get_abs_midi(4, root_midi + 2)], "Gmaj"),
        ([get_abs_midi(3, root_midi + 9), get_abs_midi(4, root_midi + 0), get_abs_midi(4, root_midi + 4)], "Amin"),
        ([get_abs_midi(3, root_midi + 5), get_abs_midi(3, root_midi + 9), get_abs_midi(4, root_midi + 0)], "Fmaj"),
    ]

    # Melody pattern (relative to C4, MIDI 60)
    melody_pattern = [
        # Cmaj7 part
        (get_abs_midi(4, root_midi + 7), 0.0, 0.25), (get_abs_midi(4, root_midi + 9), 0.25, 0.25), 
        (get_abs_midi(4, root_midi + 7), 0.5, 0.25), (get_abs_midi(4, root_midi + 11), 0.75, 0.25), 
        (get_abs_midi(5, root_midi + 0), 1.0, 0.25), (get_abs_midi(4, root_midi + 11), 1.25, 0.25), 
        (get_abs_midi(4, root_midi + 7), 1.5, 0.25), (get_abs_midi(4, root_midi + 9), 2.0, 0.25), 
        (get_abs_midi(4, root_midi + 7), 2.5, 0.25), (get_abs_midi(4, root_midi + 11), 2.75, 0.25),
        (get_abs_midi(5, root_midi + 0), 3.0, 0.25), (get_abs_midi(4, root_midi + 11), 3.25, 0.25), 
        (get_abs_midi(4, root_midi + 7), 3.5, 0.25),
    ]

    # Bass pattern (relative to C2, MIDI 36)
    bass_pattern = [
        # C part
        (get_abs_midi(2, root_midi + 0), 0.0, 0.5), (get_abs_midi(2, root_midi + 7), 0.5, 0.5), 
        (get_abs_midi(2, root_midi + 4), 1.0, 0.5), (get_abs_midi(2, root_midi + 7), 1.5, 0.5), 
        (get_abs_midi(2, root_midi + 0), 2.0, 0.5), (get_abs_midi(2, root_midi + 7), 2.5, 0.5), 
        (get_abs_midi(2, root_midi + 4), 3.0, 0.5), (get_abs_midi(2, root_midi + 7), 3.5, 0.5),
    ]

    # Drum pattern for 4 bars (kick, snare, hihat)
    drum_pattern = []
    for bar in range(4):
        # Kick on 1, 2, 3, 4
        drum_pattern.append((DRUM_KICK, bar * beats_per_bar, quarter_note))
        drum_pattern.append((DRUM_KICK, bar * beats_per_bar + 1.0, quarter_note))
        drum_pattern.append((DRUM_KICK, bar * beats_per_bar + 2.0, quarter_note))
        drum_pattern.append((DRUM_KICK, bar * beats_per_bar + 3.0, quarter_note))
        # Snare on 2 and 4
        drum_pattern.append((DRUM_SNARE, bar * beats_per_bar + 1.0, quarter_note))
        drum_pattern.append((DRUM_SNARE, bar * beats_per_bar + 3.0, quarter_note))
        # Hi-hats on 1/8ths
        for beat_pos in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            drum_pattern.append((DRUM_HIHAT, bar * beats_per_bar + beat_pos, eighth_note))
    
    # SD Kick Boost (ghost kick for sidechain)
    sd_kick_pattern = []
    for bar in range(intro_bars + chorus_bars + verse_bars): # Span across all segments
        for beat_pos in [0.0, 1.0, 2.0, 3.0]: # Every quarter note
            sd_kick_pattern.append((DRUM_KICK, bar * beats_per_bar + beat_pos, quarter_note))


    # Helper to create MIDI item and add notes
    def create_midi_item_with_notes(track, start_time, duration, notes_data, is_drum_track=False):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration)
        take = RPR.RPR_AddTakeToMediaItem(item)
        midi_take = RPR.RPR_MIDI_SetItemExtents(item, start_time, start_time + duration)
        
        RPR.RPR_MIDI_DisableMediaItemCallback(midi_take)
        RPR.RPR_MIDI_SetItemExtents(item, -1, -1) # Needed to prevent notes from being clipped at the end of the item.

        for note_info in notes_data:
            if is_drum_track:
                pitch, beat_start, beat_duration = note_info
            else:
                pitch_or_chord, beat_start, beat_duration = note_info
                
            if isinstance(pitch_or_chord, list): # For chords
                for pitch in pitch_or_chord:
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, beat_start * quarter_note, beat_duration * quarter_note, velocity_base, pitch, 0)
            else: # For single notes (melody, bass, drums)
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, beat_start * quarter_note, beat_duration * quarter_note, velocity_base, pitch_or_chord, 0)
        
        RPR.RPR_MIDI_Sort(midi_take)
        RPR.RPR_MIDI_Update(midi_take)
        RPR.RPR_MIDI_EnableMediaItemCallback(midi_take)
        return item
    
    # === Arrange Segments ===
    current_time = 0.0

    # INTRO SEGMENT (8 bars)
    # Bars 1-4: Piano Melody + Chords (filter sweep, gradual volume on chords)
    melody_item_intro1 = create_midi_item_with_notes(tracks["Piano Melody"], current_time, 4 * quarter_note * beats_per_bar, melody_pattern * 1)
    chords_item_intro1 = create_midi_item_with_notes(tracks["Piano Chords"], current_time, 4 * quarter_note * beats_per_bar, 
                                                     [(chords_data[i][0], i * beats_per_bar, beats_per_bar) for i in range(4)])
    
    # Automation for Piano Chords (Volume & EQ Filter) during intro
    chords_track_vol_env = RPR.RPR_GetTrackEnvelopeByName(tracks["Piano Chords"], "Volume")
    if not chords_track_vol_env: chords_track_vol_env = RPR.RPR_CreateTrackEnvelope(tracks["Piano Chords"])
    RPR.RPR_InsertEnvelopePoint(chords_track_vol_env, current_time, 0.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(chords_track_vol_env, current_time + 4 * quarter_note * beats_per_bar - quarter_note, 1.0, 0, 0, False, False, False)

    if chords_eq_fx_idx != -1:
        # ReaEQ Band 1 (Low-pass) parameter 12 (Frequency)
        # Parameter value range for frequency: 0.0 (20 Hz) to 1.0 (20000 Hz)
        eq_freq_env = RPR.RPR_TrackFX_GetEnvelope(tracks["Piano Chords"], chords_eq_fx_idx, 12, True)
        RPR.RPR_InsertEnvelopePoint(eq_freq_env, current_time, 0.02, 0, 0, False, False, False) # Start low (e.g., 100 Hz)
        RPR.RPR_InsertEnvelopePoint(eq_freq_env, current_time + intro_bars * quarter_note * beats_per_bar, 1.0, 0, 0, False, False, False) # End full open (20000 Hz)

    current_time += 4 * quarter_note * beats_per_bar

    # Bars 5-8: Bass joins (bass volume automation)
    bass_item_intro2 = create_midi_item_with_notes(tracks["Bass"], current_time, 4 * quarter_note * beats_per_bar, 
                                                    [(get_abs_midi(2, root_midi + chords_data[i % 4][0][0] - root_midi), j * 0.5, 0.4) 
                                                     for i in range(4) for j in range(8)]) # Simple root bass line
    
    bass_track_vol_env = RPR.RPR_GetTrackEnvelopeByName(tracks["Bass"], "Volume")
    if not bass_track_vol_env: bass_track_vol_env = RPR.RPR_CreateTrackEnvelope(tracks["Bass"])
    RPR.RPR_InsertEnvelopePoint(bass_track_vol_env, current_time, 0.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(bass_track_vol_env, current_time + 4 * quarter_note * beats_per_bar - quarter_note, 1.0, 0, 0, False, False, False)

    current_time += 4 * quarter_note * beats_per_bar

    # CHORUS SEGMENT (4 bars)
    # Full mix, pumping effect via sidechain on Chords and Bass. Filter open.
    melody_item_chorus = create_midi_item_with_notes(tracks["Piano Melody"], current_time, chorus_bars * quarter_note * beats_per_bar, melody_pattern * 1)
    chords_item_chorus = create_midi_item_with_notes(tracks["Piano Chords"], current_time, chorus_bars * quarter_note * beats_per_bar, 
                                                     [(chords_data[i % 4][0], i * beats_per_bar, beats_per_bar) for i in range(4)])
    bass_item_chorus = create_midi_item_with_notes(tracks["Bass"], current_time, chorus_bars * quarter_note * beats_per_bar, bass_pattern * 1)
    drums_item_chorus = create_midi_item_with_notes(tracks["Drums"], current_time, chorus_bars * quarter_note * beats_per_bar, drum_pattern, is_drum_track=True)
    sd_kick_item_chorus = create_midi_item_with_notes(tracks["SD Kick Boost"], current_time, chorus_bars * quarter_note * beats_per_bar, sd_kick_pattern, is_drum_track=True)

    # Enable sidechain for chorus (by removing volume automation that was used in intro, or set to 1.0)
    RPR.RPR_InsertEnvelopePoint(chords_track_vol_env, current_time, 1.0, 0, 0, False, False, False)
    RPR.RPR_InsertEnvelopePoint(bass_track_vol_env, current_time, 1.0, 0, 0, False, False, False)
    
    drums_track_vol_env = RPR.RPR_GetTrackEnvelopeByName(tracks["Drums"], "Volume")
    if not drums_track_vol_env: drums_track_vol_env = RPR.RPR_CreateTrackEnvelope(tracks["Drums"])
    RPR.RPR_InsertEnvelopePoint(drums_track_vol_env, current_time, 1.0, 0, 0, False, False, False)

    current_time += chorus_bars * quarter_note * beats_per_bar

    # VERSE SEGMENT (4 bars)
    # Chords + Bass, no melody/drums. Filter open, sidechain active.
    chords_item_verse = create_midi_item_with_notes(tracks["Piano Chords"], current_time, verse_bars * quarter_note * beats_per_bar, 
                                                    [(chords_data[i % 4][0], i * beats_per_bar, beats_per_bar) for i in range(4)])
    bass_item_verse = create_midi_item_with_notes(tracks["Bass"], current_time, verse_bars * quarter_note * beats_per_bar, bass_pattern * 1)
    sd_kick_item_verse = create_midi_item_with_notes(tracks["SD Kick Boost"], current_time, verse_bars * quarter_note * beats_per_bar, sd_kick_pattern, is_drum_track=True)
    
    current_time += verse_bars * quarter_note * beats_per_bar

    RPR.RPR_UpdateArrange()

    return f"Created 'EDM Pattern' with {intro_bars}-bar intro, {chorus_bars}-bar chorus, and {verse_bars}-bar verse segments at {bpm} BPM."

