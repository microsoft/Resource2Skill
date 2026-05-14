import reaper_python as RPR

# --- Helper functions ---
def get_midi_note_number(root_note_name, octave, semitone_offset=0):
    """Calculates MIDI note number from note name, octave, and offset."""
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    return NOTE_MAP[root_note_name] + (octave * 12) + semitone_offset

def add_midi_note_to_item(midi_take, start_time, duration, pitch, velocity=100):
    """Adds a MIDI note to a specified MIDI take."""
    midi_note_new = RPR.MIDI_InsertNote(midi_take, False, False, start_time, start_time + duration, velocity, pitch, 0)
    RPR.MIDI_SetNoteFlags(midi_take, midi_note_new, 1, 1, 0) # Select and update
    RPR.MIDI_SetNote(midi_take, midi_note_new, None, None, None, None, pitch, None, None)
    RPR.MIDI_SetNote(midi_take, midi_note_new, None, None, start_time, start_time + duration, None, velocity, None)
    return midi_note_new

def create_edm_dynamic_section(
    project_name: str = "EDM_House_Project",
    bpm: int = 120,
    key: str = "D", # D minor implied root for chords/melody
    scale: str = "minor",
    bars: int = 8, # Total bars for the section (e.g., intro + chorus)
    velocity_base: int = 100,
    include_melody: bool = True,
    apply_eq_sweep: bool = True,
    apply_sidechain: bool = True,
    **kwargs,
) -> str:
    """
    Creates an EDM-style dynamic section with melody, chords, bass, drums,
    filter sweep automation, and sidechain compression.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Will be interpreted as a minor key.
        scale: Scale type (minor).
        bars: Number of bars to generate for the section.
        velocity_base: Base MIDI velocity (0-127).
        include_melody: Whether to include the melody track.
        apply_eq_sweep: Whether to apply the low-pass filter sweep automation.
        apply_sidechain: Whether to apply sidechain compression.
        **kwargs: Additional overrides (not used in this specific implementation).

    Returns:
        Status string, e.g., "Created 'EDM Dynamic Section' with various tracks."
    """
    RPR.Undo_BeginBlock2(0) # Start an undo block

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Calculate bar length in seconds
    seconds_per_beat = 60.0 / bpm
    bar_length_beats = 4
    bar_length_seconds = seconds_per_beat * bar_length_beats

    # === Step 2: Create Tracks ===
    track_names = ["EDM Melody", "EDM Chords", "EDM Bass", "EDM Drums", "SC_Kick (Muted)"]
    tracks = {}
    for name in track_names:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track

    # Mute the Sidechain Kick track (volume to -inf)
    RPR.RPR_SetMediaTrackInfo_Value(tracks["SC_Kick (Muted)"], "D_VOL", 0.0) # 0.0 maps to -150dB

    # === Step 3: Create MIDI Items and Notes ===
    midi_data = {
        "EDM Melody": [],
        "EDM Chords": [],
        "EDM Bass": [],
        "EDM Drums": [],
        "SC_Kick (Muted)": [],
    }

    # Define the 2-bar progression loop based on D minor (D-C)
    # Melody notes (relative to MIDI 62 (D4))
    melody_pattern_1 = [
        (0.0, 1.0, get_midi_note_number(key, 4, 3)),   # F4 (D minor's 3rd)
        (1.0, 0.5, get_midi_note_number(key, 4, 7)),   # A4 (D minor's 5th)
        (1.5, 0.5, get_midi_note_number(key, 5, 0)),   # C5 (D minor's 7th)
        (2.0, 0.5, get_midi_note_number(key, 4, 7)),   # A4
        (2.5, 0.5, get_midi_note_number(key, 4, 5)),   # G4 (D minor's 4th)
        (3.0, 1.0, get_midi_note_number(key, 4, 3)),   # F4
    ] # Total 4 beats
    
    # Melody pattern 2 (relative to MIDI 62 (D4))
    melody_pattern_2 = [
        (0.0, 1.0, get_midi_note_number(key, 4, 2)),   # E4 (C major's 3rd)
        (1.0, 0.5, get_midi_note_number(key, 4, 5)),   # G4 (C major's 5th)
        (1.5, 0.5, get_midi_note_number(key, 4, 11)),  # B4 (C major's 7th, or B natural)
        (2.0, 0.5, get_midi_note_number(key, 4, 5)),   # G4
        (2.5, 0.5, get_midi_note_number(key, 4, 3)),   # F4 (C major's 4th, as passing)
        (3.0, 1.0, get_midi_note_number(key, 4, 2)),   # E4
    ] # Total 4 beats

    # Chords (D minor - C major progression)
    # D minor triad: root, m3, P5
    dm_triad = [get_midi_note_number(key, 3, 0), get_midi_note_number(key, 3, 3), get_midi_note_number(key, 3, 7)]
    # C major triad: root, M3, P5 (relative to C, which is 'key - 2' semitones)
    c_triad = [get_midi_note_number(key, 3, -2), get_midi_note_number(key, 3, 2), get_midi_note_number(key, 3, 5)]

    # Bass notes (roots of Dm, C)
    d_bass = get_midi_note_number(key, 2, 0)
    c_bass = get_midi_note_number(key, 2, -2)

    # Drum notes (General MIDI mapping)
    kick_note = 36 # C1
    snare_note = 38 # D1
    hihat_note = 42 # F#1

    current_time = 0.0
    for bar in range(bars):
        for beat_in_bar in range(4):
            # Drums
            midi_data["EDM Drums"].append((current_time + (beat_in_bar * seconds_per_beat), seconds_per_beat * 0.25, kick_note, velocity_base)) # Kick on every beat
            midi_data["SC_Kick (Muted)"].append((current_time + (beat_in_bar * seconds_per_beat), seconds_per_beat * 0.25, kick_note, velocity_base)) # SC Kick

            if beat_in_bar == 1 or beat_in_bar == 3: # Snare on beats 2 and 4
                midi_data["EDM Drums"].append((current_time + (beat_in_bar * seconds_per_beat), seconds_per_beat * 0.25, snare_note, velocity_base))
            
            # Hi-hat on every 1/8th note
            midi_data["EDM Drums"].append((current_time + (beat_in_bar * seconds_per_beat), seconds_per_beat * 0.25, hihat_note, velocity_base - 10))
            midi_data["EDM Drums"].append((current_time + (beat_in_bar * seconds_per_beat) + (seconds_per_beat * 0.5), seconds_per_beat * 0.25, hihat_note, velocity_base - 10))

        # Chords and Bass (2-bar loop)
        if bar % 2 == 0: # Dm chord for 2 beats, C chord for 2 beats
            # Dm chord
            for pitch in dm_triad:
                midi_data["EDM Chords"].append((current_time, seconds_per_beat * 2, pitch, velocity_base - 20))
            midi_data["EDM Bass"].append((current_time, seconds_per_beat * 2, d_bass, velocity_base))
            # C chord
            for pitch in c_triad:
                midi_data["EDM Chords"].append((current_time + (seconds_per_beat * 2), seconds_per_beat * 2, pitch, velocity_base - 20))
            midi_data["EDM Bass"].append((current_time + (seconds_per_beat * 2), seconds_per_beat * 2, c_bass, velocity_base))
        else: # Dm chord for 2 beats, C chord for 2 beats (repeat of pattern, but offset for full 4-bar loop visual)
            # Dm chord
            for pitch in dm_triad:
                midi_data["EDM Chords"].append((current_time, seconds_per_beat * 2, pitch, velocity_base - 20))
            midi_data["EDM Bass"].append((current_time, seconds_per_beat * 2, d_bass, velocity_base))
            # C chord
            for pitch in c_triad:
                midi_data["EDM Chords"].append((current_time + (seconds_per_beat * 2), seconds_per_beat * 2, pitch, velocity_base - 20))
            midi_data["EDM Bass"].append((current_time + (seconds_per_beat * 2), seconds_per_beat * 2, c_bass, velocity_base))
            
        # Melody (2-bar loop, follows chord changes)
        if include_melody:
            if bar % 2 == 0: # Dm context
                for start_offset, duration_beats, pitch in melody_pattern_1:
                    midi_data["EDM Melody"].append((current_time + (start_offset * seconds_per_beat), duration_beats * seconds_per_beat, pitch, velocity_base))
            else: # C Major context
                for start_offset, duration_beats, pitch in melody_pattern_2:
                    midi_data["EDM Melody"].append((current_time + (start_offset * seconds_per_beat), duration_beats * seconds_per_beat, pitch, velocity_base))


        current_time += bar_length_seconds

    # Create MIDI items and insert notes
    midi_takes = {}
    for name, track in tracks.items():
        if name != "EDM Drums" and name != "SC_Kick (Muted)" and name != "EDM Chords" and name != "EDM Melody" and name != "EDM Bass":
            continue # Only process tracks with MIDI data defined above

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_seconds * bars)
        take = RPR.RPR_GetActiveTake(item)
        if not take:
            take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_TakeFX_AddByName(take, "VSTi: ReaSynth (Cockos)", False, -1) # Default instrument

        midi_takes[name] = RPR.MIDI_AllocMidiTake(take)

        for note_start_time, note_duration, note_pitch, note_velocity in midi_data[name]:
            add_midi_note_to_item(midi_takes[name], note_start_time, note_duration, note_pitch, note_velocity)
        
        RPR.MIDI_Sort(midi_takes[name]) # Sort notes by start time
        RPR.MIDI_UpdateByTake(midi_takes[name], True, True) # Update take
        RPR.MIDI_FreeMidiTake(midi_takes[name]) # Free MIDI take

    # For drums, let's load ReaSamplOmatic5000 as it's common for drum kits
    RPR.RPR_TrackFX_AddByName(tracks["EDM Drums"], "VSTi: ReaSamplOmatic5000 (Cockos)", False, -1)
    RPR.RPR_TrackFX_AddByName(tracks["SC_Kick (Muted)"], "VSTi: ReaSamplOmatic5000 (Cockos)", False, -1)

    # === Step 4: Add FX Chains and Automation ===

    # EQ Filter Sweep on Melody and Chords
    if apply_eq_sweep:
        for track_name in ["EDM Melody", "EDM Chords"]:
            track = tracks[track_name]
            RPR.RPR_TrackFX_AddByName(track, "VST: ReaEQ (Cockos)", False, -1)
            fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1 # Index of ReaEQ

            # Enable Band 1 (low-pass filter)
            RPR.RPR_TrackFX_SetEQBandEnabled(track, fx_idx, 0, True) # Band 1 is first band in ReaEQ
            RPR.RPR_TrackFX_SetEQBandType(track, fx_idx, 0, 6) # Type 6 is Lowpass (6dB/oct)

            # Automate Band 1 Frequency (Parameter 0 of ReaEQ for Band 1 Freq)
            param_idx = 0 # Parameter ID for Band 1 Frequency
            envelope = RPR.RPR_GetTrackEnvelopeByName(track, f"FX {fx_idx+1}: ReaEQ (Cockos) VST: Band 1 Freq")
            if not envelope:
                envelope = RPR.RPR_CreateTrackEnvelope(track) # Create if not exists
                RPR.RPR_SetEnvelopeState(envelope, f"FX {fx_idx+1}: ReaEQ (Cockos) VST: Band 1 Freq 0") # Set name via state
            RPR.RPR_SetEnvelopeState(envelope, RPR.RPR_GetEnvelopeState(envelope).split('\n')[0] + " V 1") # Set visible
            
            RPR.RPR_DeleteEnvelopePointRange(envelope, 0.0, bar_length_seconds * bars) # Clear existing points

            # Add automation points for a linear sweep
            RPR.RPR_InsertEnvelopePoint(envelope, 0.0, 0.0, 0, 0, False, True) # Start closed (0.0 parameter value)
            RPR.RPR_InsertEnvelopePoint(envelope, bar_length_seconds * bars, 1.0, 0, 0, False, True) # End open (1.0 parameter value)
            RPR.RPR_SetEnvelopeState(envelope, RPR.RPR_GetEnvelopeState(envelope).replace("L 1", "L 3")) # Linear segment


    # Sidechain Compression setup
    if apply_sidechain:
        for track_name in ["EDM Melody", "EDM Chords", "EDM Bass"]:
            track = tracks[track_name]
            
            # Add ReaComp
            RPR.RPR_TrackFX_AddByName(track, "VST: ReaComp (Cockos)", False, -1)
            reacomp_fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1

            # Configure sidechain routing (send from SC_Kick to input 3/4 of current track)
            # Find the SC_Kick track's current channel mapping (source)
            sc_kick_track = tracks["SC_Kick (Muted)"]
            
            # Create a receive from the SC_Kick track to the current track
            # input 3 and 4 are for sidechain in ReaComp
            # RPR.RPR_CreateTrackSend(src_track, dest_track, flags)
            # flags: 0=send vol/pan, 1=MIDI, 2=post-fader, 3=pre-fader, 4=pre-FX, 5=post-FX
            send_idx = RPR.RPR_CreateTrackSend(sc_kick_track, track, 0) # Basic send
            
            # Set the destination channels for this send to 3 and 4 (sidechain input)
            # RPR_SetTrackSendInfo_Value(track, send_idx, parameter, value)
            # parameter "I_SRCCHAN": Source channel (1-16) for send (default 1)
            # parameter "I_DSTCHAN": Destination channel (1-16) for send (default 1)
            RPR.RPR_SetTrackSendInfo_Value(track, send_idx, "I_DSTCHAN", 3.0) # Set destination channels to 3/4
            RPR.RPR_SetTrackSendInfo_Value(track, send_idx, "D_VOL", 1.0) # Full volume send for sidechain trigger
            RPR.RPR_SetTrackSendInfo_Value(track, send_idx, "B_MUTE", 0.0) # Unmute send

            # Enable detector input for ReaComp (parameter 15)
            RPR.RPR_TrackFX_SetParam(track, reacomp_fx_idx, 15, 1.0) # Detector input to Aux L/R

            # Set ReaComp parameters for pumping
            RPR.RPR_TrackFX_SetParam(track, reacomp_fx_idx, 5, 0.4)  # Threshold: -20dB (0.0 to 1.0 -> -60 to 0)
            RPR.RPR_TrackFX_SetParam(track, reacomp_fx_idx, 6, 0.6)  # Ratio: 4:1 (0.0 to 1.0 -> 1:1 to 10:1)
            RPR.RPR_TrackFX_SetParam(track, reacomp_fx_idx, 3, 0.001) # Attack: very fast (~0.001s, 0.0 to 1.0 -> 0s to 1s)
            RPR.RPR_TrackFX_SetParam(track, reacomp_fx_idx, 4, 0.05)  # Release: medium (~0.15s, 0.0 to 1.0 -> 0s to 1s)

    RPR.Undo_EndBlock2(0, f"Created '{project_name}' EDM Dynamic Section", -1) # End undo block
    return f"Created '{project_name}' EDM Dynamic Section with {bars} bars. Melody: {include_melody}, EQ Sweep: {apply_eq_sweep}, Sidechain: {apply_sidechain}."

