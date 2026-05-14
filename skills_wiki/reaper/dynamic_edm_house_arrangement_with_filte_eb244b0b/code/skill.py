import reaper_python as RPR
import math

def create_edm_arrangement_pattern(
    project_name: str = "EDM House",
    bpm: int = 120,
    key: str = "A", # Base key for transposition, video uses A minor progression
    scale: str = "minor", # Scale type that broadly fits the progression
    bars: int = 16, # Total bars for the example (e.g., 4 intro + 4 pumping + 8 chorus)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a dynamic EDM House arrangement pattern with filter and sidechain automation.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note for transposition (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.). Used for harmonic context,
               but progression intervals are fixed for this specific pattern.
        bars: Number of bars to generate for the entire arrangement.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # MIDI note patterns (relative to C0=0), transcribed from video
    # Progression: Fmaj, Gmaj, Amin, Gmaj (repeated)
    
    # Piano Melody Pattern (4 bars, then repeats)
    # Notes are relative to A0 (MIDI 21) which is the tonic of A minor for this progression
    # The notes in the video are fixed, so we calculate an offset based on the requested key
    reference_key_midi = NOTE_MAP["A"] + 3*12 # A3 (MIDI 57) as typical lower chord note root in video
    key_offset = (NOTE_MAP[key.upper()] + 3*12) - reference_key_midi

    piano_melody_pattern = [
        # Bar 1 (over Fmaj)
        {"note": 60 + key_offset, "start": 0.0, "duration": 0.5}, # C4
        {"note": 67 + key_offset, "start": 0.5, "duration": 0.5}, # G4
        {"note": 65 + key_offset, "start": 1.0, "duration": 0.5}, # F4
        {"note": 67 + key_offset, "start": 1.5, "duration": 0.5}, # G4
        # Bar 2 (over Gmaj)
        {"note": 60 + key_offset, "start": 2.0, "duration": 0.5}, # C4
        {"note": 67 + key_offset, "start": 2.5, "duration": 0.5}, # G4
        {"note": 65 + key_offset, "start": 3.0, "duration": 0.5}, # F4
        {"note": 67 + key_offset, "start": 3.5, "duration": 0.5}, # G4
        # Bar 3 (over Amin)
        {"note": 69 + key_offset, "start": 4.0, "duration": 0.5}, # A4
        {"note": 64 + key_offset, "start": 4.5, "duration": 0.5}, # E4
        {"note": 60 + key_offset, "start": 5.0, "duration": 0.5}, # C4
        {"note": 64 + key_offset, "start": 5.5, "duration": 0.5}, # E4
        # Bar 4 (over Gmaj)
        {"note": 67 + key_offset, "start": 6.0, "duration": 0.5}, # G4
        {"note": 62 + key_offset, "start": 6.5, "duration": 0.5}, # D4
        {"note": 59 + key_offset, "start": 7.0, "duration": 0.5}, # B3
        {"note": 62 + key_offset, "start": 7.5, "duration": 0.5}, # D4
    ]

    # Piano Chords Pattern (4 bars, then repeats)
    piano_chords_pattern = [
        # Bar 1 (Fmaj)
        {"notes": [53 + key_offset, 57 + key_offset, 60 + key_offset], "start": 0.0, "duration": 4.0}, # F3, A3, C4
        # Bar 2 (Gmaj)
        {"notes": [55 + key_offset, 59 + key_offset, 62 + key_offset], "start": 4.0, "duration": 4.0}, # G3, B3, D4
        # Bar 3 (Amin)
        {"notes": [57 + key_offset, 60 + key_offset, 64 + key_offset], "start": 8.0, "duration": 4.0}, # A3, C4, E4
        # Bar 4 (Gmaj)
        {"notes": [55 + key_offset, 59 + key_offset, 62 + key_offset], "start": 12.0, "duration": 4.0}, # G3, B3, D4
    ]
    
    # Bass Pattern (4 bars, then repeats)
    bass_pattern = [
        # Bar 1 (F)
        {"note": 41 + key_offset, "start": 0.0, "duration": 0.25}, {"note": 41 + key_offset, "start": 0.5, "duration": 0.25},
        {"note": 41 + key_offset, "start": 1.0, "duration": 0.25}, {"note": 41 + key_offset, "start": 1.5, "duration": 0.25},
        {"note": 41 + key_offset, "start": 2.0, "duration": 0.25}, {"note": 41 + key_offset, "start": 2.5, "duration": 0.25},
        {"note": 41 + key_offset, "start": 3.0, "duration": 0.25}, {"note": 41 + key_offset, "start": 3.5, "duration": 0.25},
        # Bar 2 (G)
        {"note": 43 + key_offset, "start": 4.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 4.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 5.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 5.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 6.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 6.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 7.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 7.5, "duration": 0.25},
        # Bar 3 (A)
        {"note": 45 + key_offset, "start": 8.0, "duration": 0.25}, {"note": 45 + key_offset, "start": 8.5, "duration": 0.25},
        {"note": 45 + key_offset, "start": 9.0, "duration": 0.25}, {"note": 45 + key_offset, "start": 9.5, "duration": 0.25},
        {"note": 45 + key_offset, "start": 10.0, "duration": 0.25}, {"note": 45 + key_offset, "start": 10.5, "duration": 0.25},
        {"note": 45 + key_offset, "start": 11.0, "duration": 0.25}, {"note": 45 + key_offset, "start": 11.5, "duration": 0.25},
        # Bar 4 (G)
        {"note": 43 + key_offset, "start": 12.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 12.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 13.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 13.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 14.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 14.5, "duration": 0.25},
        {"note": 43 + key_offset, "start": 15.0, "duration": 0.25}, {"note": 43 + key_offset, "start": 15.5, "duration": 0.25},
    ]

    # Drum Pattern (C1 = Kick, D1 = Snare, F#1 = Closed Hat, A#1 = Open Hat)
    drum_pattern_main = [
        # Kick (C1/36) - every 8th note
        {"note": 36, "start": 0.0, "duration": 0.25}, {"note": 36, "start": 0.5, "duration": 0.25},
        {"note": 36, "start": 1.0, "duration": 0.25}, {"note": 36, "start": 1.5, "duration": 0.25},
        {"note": 36, "start": 2.0, "duration": 0.25}, {"note": 36, "start": 2.5, "duration": 0.25},
        {"note": 36, "start": 3.0, "duration": 0.25}, {"note": 36, "start": 3.5, "duration": 0.25},
        # Snare (D1/38) - on 2 & 4
        {"note": 38, "start": 1.0, "duration": 0.25}, {"note": 38, "start": 3.0, "duration": 0.25},
        # Closed Hi-Hat (F#1/42) - every 8th note
        {"note": 42, "start": 0.0, "duration": 0.25, "velocity": int(velocity_base * 0.7)}, {"note": 42, "start": 0.5, "duration": 0.25, "velocity": int(velocity_base * 0.7)},
        {"note": 42, "start": 1.0, "duration": 0.25, "velocity": int(velocity_base * 0.7)}, {"note": 42, "start": 1.5, "duration": 0.25, "velocity": int(velocity_base * 0.7)},
        {"note": 42, "start": 2.0, "duration": 0.25, "velocity": int(velocity_base * 0.7)}, {"note": 42, "start": 2.5, "duration": 0.25, "velocity": int(velocity_base * 0.7)},
        {"note": 42, "start": 3.0, "duration": 0.25, "velocity": int(velocity_base * 0.7)}, {"note": 42, "start": 3.5, "duration": 0.25, "velocity": int(velocity_base * 0.7)},
        # Open Hi-Hat (A#1/46) - on 1 & 3
        {"note": 46, "start": 0.0, "duration": 0.5, "velocity": int(velocity_base * 0.8)},
        {"note": 46, "start": 2.0, "duration": 0.5, "velocity": int(velocity_base * 0.8)},
    ]

    # Sidechain Kick Boost Pattern (4-on-the-floor)
    sd_kick_pattern = [
        {"note": 36, "start": 0.0, "duration": 0.25},
        {"note": 36, "start": 1.0, "duration": 0.25},
        {"note": 36, "start": 2.0, "duration": 0.25},
        {"note": 36, "start": 3.0, "duration": 0.25},
    ]

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    track_names = ["Piano Melody", "Piano Chords", "Bass", "SD Kick Boost", "Drums"]
    tracks = []
    midi_items = []
    
    # Create tracks and initial MIDI items
    for i, name in enumerate(track_names):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks.append(track)
        
        # Create MIDI item for the length of the requested bars
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * (60.0 / bpm) * 4) # 4 beats per bar
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_MIDI_SetItemExtents(item, 0.0, bars * 4.0) # Set MIDI item length in beats
        midi_items.append(item)

        # Add ReaSynth for melodic/harmonic tracks
        if "Piano" in name or "Bass" in name:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        # Add ReaSamplOmatic5000 for drum tracks
        elif "Drums" in name or "Kick Boost" in name:
            RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)

    # Populate MIDI items
    RPR.Undo_BeginBlock()

    # Helper function to add notes
    def add_notes_to_midi_item(midi_item, pattern, num_bars, base_velocity):
        take = RPR.RPR_GetActiveTake(midi_item)
        if not take: return
        RPR.MIDI_SetItemExtents(midi_item, 0.0, num_bars * 4.0)
        
        midi_editor = RPR.MIDIEditor_Create(midi_item)
        RPR.MIDIEditor_OnCommand(midi_editor, 40530) # Clear existing MIDI notes
        
        for bar_offset in range(num_bars):
            for note_data in pattern:
                if "notes" in note_data: # For chords
                    for pitch in note_data["notes"]:
                        RPR.MIDI_InsertNote(take, False, False, 
                                            note_data["start"] + bar_offset * 4.0, 
                                            note_data["start"] + bar_offset * 4.0 + note_data["duration"], 
                                            False, pitch, note_data.get("velocity", base_velocity))
                else: # For single notes
                    RPR.MIDI_InsertNote(take, False, False, 
                                        note_data["start"] + bar_offset * 4.0, 
                                        note_data["start"] + bar_offset * 4.0 + note_data["duration"], 
                                        False, note_data["note"], note_data.get("velocity", base_velocity))
        RPR.MIDIEditor_Destroy(midi_editor)
        RPR.MIDI_Sort(take)
        RPR.MIDI_MarkAllNotes(take, True) # Select all notes
        RPR.MIDI_SetAllNotesVel(take, True, True, velocity_base) # Set velocities if not specified

    # Add notes to respective tracks
    add_notes_to_midi_item(midi_items[0], piano_melody_pattern, bars, velocity_base)
    add_notes_to_midi_item(midi_items[1], piano_chords_pattern, bars, velocity_base)
    add_notes_to_midi_item(midi_items[2], bass_pattern, bars, velocity_base)
    add_notes_to_midi_item(midi_items[4], drum_pattern_main, bars, velocity_base)
    add_notes_to_midi_item(midi_items[3], sd_kick_pattern, bars, velocity_base) # SD Kick Boost

    # Mute SD Kick Boost track
    RPR.RPR_SetMediaTrackInfo_Value(tracks[3], "B_MUTE", 1.0) 

    # --- Apply FX and Automation ---

    # Get FX IDs
    reacomp_guid = RPR.AddTrackFX(tracks[1], "ReaComp", 0) # Add ReaComp to Piano Chords
    reacomp_chords_idx = RPR.TrackFX_GetFXIdxByGUID(tracks[1], reacomp_guid)
    RPR.AddTrackFX(tracks[2], "ReaComp", 0) # Add ReaComp to Bass
    reacomp_bass_idx = RPR.TrackFX_GetFXIdxByGUID(tracks[2], reacomp_guid) # Will be same GUID if added to multiple tracks

    # Add ReaEQ to Piano Chords for filter sweep
    RPR.AddTrackFX(tracks[1], "ReaEQ", 0)
    # Get ReaEQ index (usually 0 if first FX, but good to find by name)
    reareq_chords_idx = -1
    for i in range(RPR.TrackFX_GetCount(tracks[1])):
        retval, name, guid = RPR.TrackFX_GetFXName(tracks[1], i, "", 1024)
        if "ReaEQ" in name:
            reareq_chords_idx = i
            break
    
    if reareq_chords_idx != -1:
        # Enable Band 1 (Low Pass), set type, and get Cutoff Freq parameter index
        # ReaEQ parameters: 0-Enable, 1-Type, 2-Freq, 3-Gain, 4-Q, ... for each band
        # Band 1 is LowPass by default. To set type to LowPass (if not default): param 1 to 2 (Low Shelf=1, Low Pass=2, Band=3...)
        RPR.TrackFX_SetParam(tracks[1], reareq_chords_idx, 1, 2.0/6.0) # Band 1 Type: Lowpass (val=2) out of 6 options (0-6)
        
        # Automation for ReaEQ Low Pass Filter Cutoff (Band 1 Freq is Param 2)
        # Parameter index for Band 1 Freq: 2. Need to ensure Band 1 is active & Low Pass.
        
        # Get parameter ID for ReaEQ Band 1 Frequency
        eq_freq_param = -1
        for p_idx in range(RPR.TrackFX_GetNumParams(tracks[1], reareq_chords_idx)):
            retval, name, minval, maxval, midval = RPR.TrackFX_GetParamInfo(tracks[1], reareq_chords_idx, p_idx, "", 1024)
            if "Band 1 Freq" in name: # ReaEQ param names might vary slightly by version/language
                eq_freq_param = p_idx
                break
        
        if eq_freq_param != -1:
            RPR.BR_TrackFX_SetFocused(tracks[1], reareq_chords_idx) # Focus FX for envelope creation
            RPR.TrackFX_SetParam(tracks[1], reareq_chords_idx, eq_freq_param, 200.0/20000.0) # Set initial freq to 200Hz (0.01)
            
            envelope = RPR.TrackFX_GetEnvelope(tracks[1], reareq_chords_idx, eq_freq_param, True)
            if envelope:
                RPR.SetTrackEnvelopeState(envelope, "V 0.0") # Set automation lane visible
                
                # Clear existing points
                RPR.DeleteEnvelopePointRange(envelope, 0.0, 4.0 * (60.0 / bpm) * 4) # Clear points for first 4 bars (intro duration)
                
                # Add automation points for filter sweep (first 4 bars)
                # Cutoff from ~200Hz to ~18000Hz (normalized 0-1 range)
                RPR.InsertEnvelopePoint(envelope, 0.0, 200.0/20000.0, 0, 0, False, True)  # Start: 200 Hz
                RPR.InsertEnvelopePoint(envelope, 4.0 * (60.0 / bpm) * 4, 18000.0/20000.0, 0, 0, False, True) # End: 18000 Hz
        else:
            RPR.ShowConsoleMsg("Could not find ReaEQ Band 1 Freq parameter.\n")
    else:
        RPR.ShowConsoleMsg("Could not find ReaEQ FX on Piano Chords track.\n")

    # Sidechain Routing (SD Kick Boost -> Piano Chords & Bass)
    sd_kick_track = tracks[3]
    
    # Send from SD Kick Boost to Piano Chords
    send_idx_chords = RPR.CreateTrackSend(sd_kick_track, tracks[1])
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_chords, "I_SRCCHAN", 0) # Send from 1/2
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_chords, "I_DSTCHAN", 2) # To channels 3/4 (Aux L/R)
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_chords, "D_VOL", 1.0) # Full volume send
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_chords, "B_MUTE", 0) # Unmute send

    # Send from SD Kick Boost to Bass
    send_idx_bass = RPR.CreateTrackSend(sd_kick_track, tracks[2])
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_bass, "I_SRCCHAN", 0)
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_bass, "I_DSTCHAN", 2)
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_bass, "D_VOL", 1.0)
    RPR.SetTrackSendInfo_Value(sd_kick_track, 0, send_idx_bass, "B_MUTE", 0)

    # Configure ReaComp for sidechain (on Piano Chords and Bass)
    # Common ReaComp parameter IDs:
    # 0=Enable, 1=Threshold, 2=Ratio, 3=Attack, 4=Release, 5=Gain, 9=Detector Input L, 10=Detector Input R
    # (These can vary slightly, but 9/10 are common for detector input)
    
    # ReaComp on Piano Chords
    reacomp_chords = RPR.TrackFX_GetFX(tracks[1], reacomp_chords_idx)
    if reacomp_chords:
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 1, 0.4) # Threshold (~-20dB)
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 2, 0.5) # Ratio (4:1)
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 3, 0.01/1000.0) # Attack (0.01ms)
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 4, 150.0/1000.0) # Release (150ms)
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 5, 0.5) # Auto Gain
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 9, 1.0) # Detector input L (Aux L)
        RPR.TrackFX_SetParam(tracks[1], reacomp_chords_idx, 10, 1.0) # Detector input R (Aux R)
    
    # ReaComp on Bass
    reacomp_bass = RPR.TrackFX_GetFX(tracks[2], reacomp_bass_idx)
    if reacomp_bass:
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 1, 0.4) # Threshold (~-20dB)
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 2, 0.5) # Ratio (4:1)
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 3, 0.01/1000.0) # Attack (0.01ms)
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 4, 150.0/1000.0) # Release (150ms)
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 5, 0.5) # Auto Gain
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 9, 1.0) # Detector input L (Aux L)
        RPR.TrackFX_SetParam(tracks[2], reacomp_bass_idx, 10, 1.0) # Detector input R (Aux R)

    RPR.Undo_EndBlock(project_name + " - Create EDM House Arrangement", -1)
    RPR.UpdateArrange()

    return f"Created EDM House Arrangement with {len(track_names)} tracks over {bars} bars at {bpm} BPM."

