import reaper_python as RPR
import math

# Music theory lookup tables
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

def create_bittime_pluck_synth(
    project_name: str = "MyProject",
    track_name: str = "Bittime Pluck Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    octave_base: int = 3, # C3
    velocity_base: int = 100,
    note_duration_beats: float = 0.25, # Default to 16th note length (e.g., 0.25 beats for a 16th note)
    delay_mix: float = 0.3, # 0.0 to 1.0 (for wet/dry)
    comp_thresh: float = -20.0, # dB
    comp_ratio: float = 4.0, # ratio
    comp_attack_ms: float = 5.0, # ms
    comp_release_ms: float = 50.0, # ms
    **kwargs,
) -> str:
    """
    Create a synth track with a rhythmic arpeggiated pattern inspired by Bittime Generator,
    using ReaSynth for a pluck sound and ReaDelay/ReaComp for effects.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        octave_base: MIDI octave for the starting note (e.g., 3 for C3).
        velocity_base: Base MIDI velocity (0-127).
        note_duration_beats: Duration of each MIDI note in beats.
        delay_mix: Wet/dry mix for ReaDelay (0.0 to 1.0).
        comp_thresh: Threshold for ReaComp (dB).
        comp_ratio: Ratio for ReaComp.
        comp_attack_ms: Attack time for ReaComp (ms).
        comp_release_ms: Release time for ReaComp (ms).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Bittime Pluck Synth' with 32 notes over 4 bars at 120 BPM"
    """

    RPR.Undo_BeginBlock2(0) # Begin undo block

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item and Notes ===
    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    
    # Calculate MIDI root note (defaulting to C if key not found)
    root_midi = NOTE_MAP.get(key.upper(), 0) + (octave_base * 12)
    
    # Get scale degrees (defaulting to major scale if not found)
    scale_degrees = SCALES.get(scale.lower(), SCALES["major"])
    
    # Construct the arpeggiated pattern pitches: ascend the scale, then the root an octave higher.
    # e.g., for C major: C, D, E, F, G, A, B, C (octave higher)
    pitch_offsets_for_pattern = list(scale_degrees)
    if len(pitch_offsets_for_pattern) > 0:
        pitch_offsets_for_pattern.append(pitch_offsets_for_pattern[0] + 12)
    
    notes_per_cycle = len(pitch_offsets_for_pattern) # 8 notes for a full major scale + octave
    
    notes_to_add = []
    total_notes_added = 0

    for bar in range(bars):
        for i in range(notes_per_cycle):
            # Each note starts on an 8th note position: 0.0, 0.5, 1.0, 1.5, ...
            # The tutorial pattern has notes spaced at 8th note intervals
            position_beats = (bar * beats_per_bar) + (i * 0.5) 
            
            midi_offset = pitch_offsets_for_pattern[i]
            midi_pitch = root_midi + midi_offset
            
            duration_beats = note_duration_beats
            
            notes_to_add.append({
                "pitch": midi_pitch,
                "position": position_beats,
                "duration": duration_beats,
                "velocity": velocity_base
            })
            total_notes_added += 1

    # Add MIDI item
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats)
    take = RPR.RPR_AddTakeToMediaItem(item)
    RPR.RPR_SetMediaItemTake_Source(take, RPR.MIDI_CreateEx(0)) # Create empty MIDI source

    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.MIDI_SetItemExtents(midi_take, 0.0, item_length_beats) # Set MIDI item length

    # Insert MIDI notes
    for note_data in notes_to_add:
        RPR.MIDI_InsertNote(
            midi_take,
            False, # selected
            True,  # no_name (use pitch name for display)
            note_data["position"],
            note_data["position"] + note_data["duration"],
            note_data["pitch"],
            note_data["velocity"],
            False # no_loop
        )
    # Update MIDI editor if open
    # RPR.MIDIEditor_OnCommand(RPR.MIDIEditor_GetActive(), 40043) # Apply changes to MIDI editor (update notes)

    # === Step 3: Add FX Chain ===
    # ReaSynth (for pluck sound approximation)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    synth_fx_idx = RPR.RPR_TrackFX_GetByName(track, "ReaSynth (Cockos)", False)
    if synth_fx_idx != -1:
        # Oscillator 1 Waveform (param 0): 0.667 for Saw
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 0, 0.667) 
        # Oscillator 2 Waveform (param 1): 0.333 for Square
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 1, 0.333)
        # Oscillator 1 Volume (param 2)
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 2, 0.5) 
        # Oscillator 2 Volume (param 3)
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 3, 0.5) 

        # Amp Envelope: Attack, Decay, Sustain, Release for pluck
        # Attack (param 10): Very fast
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 10, 0.01) 
        # Decay (param 11): Short
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 11, 0.15) 
        # Sustain (param 12): No sustain
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 12, 0.0)  
        # Release (param 13): Short
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 13, 0.1)  

        # Filter: Low Pass, some cutoff, some resonance
        # Filter type (param 14): 0.0 for Low Pass
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 14, 0.0) 
        # Filter Cutoff (param 15): 0.4 (approx 8kHz)
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 15, 0.4) 
        # Filter Resonance (param 16): 0.2
        RPR.RPR_TrackFX_SetParam(track, synth_fx_idx, 16, 0.2) 

    # ReaDelay (for Reason Delay placeholder)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay (Cockos)", False, -1)
    delay_fx_idx = RPR.RPR_TrackFX_GetByName(track, "ReaDelay (Cockos)", False)
    if delay_fx_idx != -1:
        # Dry/Wet Mix (param 0: Dry, param 1: Wet)
        RPR.RPR_TrackFX_SetParam(track, delay_fx_idx, 0, 1.0 - delay_mix) 
        RPR.RPR_TrackFX_SetParam(track, delay_fx_idx, 1, delay_mix)       
        # Feedback (param 6): 50%
        RPR.RPR_TrackFX_SetParam(track, delay_fx_idx, 6, 0.5) 
        # Delay 1 Left (param 2) and Right (param 3) are normalized 0-1 values.
        # Max delay for ReaDelay is 20 seconds. 500ms = 0.5s.
        delay_time_norm = 0.5 / 20.0 
        RPR.RPR_TrackFX_SetParam(track, delay_fx_idx, 2, delay_time_norm) 
        RPR.RPR_TrackFX_SetParam(track, delay_fx_idx, 3, delay_time_norm)

    # ReaComp (for Reason Big Compressor placeholder)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp (Cockos)", False, -1)
    comp_fx_idx = RPR.RPR_TrackFX_GetByName(track, "ReaComp (Cockos)", False)
    if comp_fx_idx != -1:
        # Threshold (param 0): -100 to 0 dB, mapped to 0.0-1.0
        RPR.RPR_TrackFX_SetParam(track, comp_fx_idx, 0, (comp_thresh + 100.0) / 100.0) 
        # Ratio (param 1): 1:1 to 100:1. ReaComp's ratio knob is non-linear.
        # A simple linear approximation for 1:1 to 10:1:
        RPR.RPR_TrackFX_SetParam(track, comp_fx_idx, 1, min(comp_ratio / 10.0, 1.0)) 
        # Attack (param 2): 0.001ms to 2000ms, normalized 0.0-1.0
        RPR.RPR_TrackFX_SetParam(track, comp_fx_idx, 2, comp_attack_ms / 2000.0)
        # Release (param 3): 1ms to 5000ms, normalized 0.0-1.0
        RPR.RPR_TrackFX_SetParam(track, comp_fx_idx, 3, comp_release_ms / 5000.0)
        # Gain (param 5): -20dB to +20dB. Default 0.5 for 0dB.
        RPR.RPR_TrackFX_SetParam(track, comp_fx_idx, 5, 0.5)

    # ReaEQ (as seen in video, although later removed in tutorial - added as a placeholder)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ (Cockos)", False, -1)

    RPR.Undo_EndBlock2(0, f"Create {track_name} pattern", -1) # End undo block
    RPR.UpdateArrange() # Refresh REAPER UI

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM (approximated sound)"

