import reaper_python as RPR
import random

def get_scale_midi_notes(root_note_name: str, scale_name: str, octave: int):
    """
    Calculates MIDI notes for a given root, scale, and octave.
    """
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    root_midi = NOTE_MAP.get(root_note_name, 0) + (octave * 12)
    scale_intervals = SCALES.get(scale_name, SCALES["minor"])

    # Returns the intervals from the root, not absolute MIDI notes
    return [root_midi + interval for interval in scale_intervals]

def create_retro_synth_arpeggiated_bassline(
    project_name: str = "MyProject",
    track_name: str = "Retro Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    octave: int = 3, # C3 as root for bassline
    **kwargs,
) -> str:
    """
    Create a retro synth arpeggiated bassline using Massive X and a pattern inspired by Beat Map.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        octave: MIDI octave for the root note (e.g., 3 for C3).
        **kwargs: Additional overrides for future extensions.

    Returns:
        Status string, e.g., "Created 'Retro Bass' with 40 notes over 4 bars at 120 BPM."
    """
    RPR.RPR_PreventUIRefresh(1)
    RPR.RPR_Undo_BeginBlock2(0) # Begin undo block

    try:
        # === Step 1: Set Tempo ===
        # Using CSurf_OnMidiChange for global BPM change as SetProjectBPMChange is internal CF_
        # This will set the project tempo and update the tempo envelope.
        RPR.RPR_CSurf_OnMidiChange(0, 0x50, int(bpm * 2), 0) # 0x50 is for tempo, value is BPM*2 (0-255)

        # === Step 2: Create Track ===
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
        RPR.RPR_TrackList_AdjustWindows(False) # Adjust track view

        # === Step 3: Add Massive X VSTi and preset ===
        massive_x_loaded = False
        # Try common VST names for Massive X
        if RPR.RPR_TrackFX_AddByName(track, "VSTi: Massive X (Native Instruments)", False, -1):
            massive_x_loaded = True
        elif RPR.RPR_TrackFX_AddByName(track, "VSTi: Massive X", False, -1): # Fallback
            massive_x_loaded = True
        
        if not massive_x_loaded:
            return "Failed to load Massive X. Please ensure it is installed as 'Massive X (Native Instruments)' or 'Massive X'."

        fx_idx = RPR.RPR_TrackFX_GetCount(track) - 1
        if fx_idx >= 0:
            preset_name = "Retro Pitch"
            # Attempt to set the preset. This requires the exact preset name.
            # RPR_TrackFX_SetPreset does not always confirm success, but it's the standard method.
            RPR.RPR_TrackFX_SetPreset(track, fx_idx, preset_name)
            
            # Verify if the preset was actually set (optional, as there's no direct API to get current preset name easily)
            # RPR.RPR_ShowConsoleMsg(f"Attempted to load Massive X preset: '{preset_name}'\n")
        else:
            RPR.RPR_ShowConsoleMsg("Error: Massive X FX not found after adding it.\n")
            return "Error: Massive X FX not found after adding it."


        # === Step 4: Create MIDI Item ===
        beats_per_bar = 4
        
        # Get current project time in seconds to place item at current cursor
        cursor_pos = RPR.RPR_GetCursorPosition()
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", cursor_pos)
        
        # Calculate item length in seconds
        seconds_per_beat = 60.0 / bpm
        item_length_beats = bars * beats_per_bar
        item_length_seconds = item_length_beats * seconds_per_beat
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)

        take = RPR.RPR_GetActiveTake(item)
        if not take:
            take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Ensure the take has a MIDI source
        RPR.RPR_SetMediaItemTake_Source(take, RPR.RPR_MIDI_CreateNewMIDIItemInTake(take, 0))
        
        midi_take = RPR.RPR_GetMediaItemTake_Source(take)
        if not midi_take or not RPR.RPR_TakeIsMIDI(midi_take):
            return "Failed to create MIDI source for item."

        # === Step 5: Insert MIDI Notes (Clockwork Bassline Pattern) ===
        # Define the 1-bar pattern using scale degree indices and octave shifts.
        # Example for C minor (C, D, Eb, F, G, Ab, Bb):
        # (0,0) -> C3 (root)
        # (2,0) -> Eb3 (3rd degree of minor scale, in base octave)
        # (4,0) -> G3 (5th degree of minor scale, in base octave)
        # (0,1) -> C4 (0th degree, shifted up one octave)

        pattern_steps = [
            # Beat 1: Root, 5th
            {"beat_offset": 0.00,  "scale_degree_idx": 0, "octave_shift": 0}, # 1st 16th
            {"beat_offset": 0.50,  "scale_degree_idx": 4, "octave_shift": 0}, # 3rd 16th

            # Beat 2: Root, minor 3rd, octave (root)
            {"beat_offset": 1.00,  "scale_degree_idx": 0, "octave_shift": 0}, # 1st 16th
            {"beat_offset": 1.25,  "scale_degree_idx": 2, "octave_shift": 0}, # 2nd 16th
            {"beat_offset": 1.75,  "scale_degree_idx": 0, "octave_shift": 1}, # 4th 16th

            # Beat 3: Root, 5th
            {"beat_offset": 2.00,  "scale_degree_idx": 0, "octave_shift": 0}, # 1st 16th
            {"beat_offset": 2.50,  "scale_degree_idx": 4, "octave_shift": 0}, # 3rd 16th

            # Beat 4: Root, minor 3rd, octave (root)
            {"beat_offset": 3.00,  "scale_degree_idx": 0, "octave_shift": 0}, # 1st 16th
            {"beat_offset": 3.25,  "scale_degree_idx": 2, "octave_shift": 0}, # 2nd 16th
            {"beat_offset": 3.75,  "scale_degree_idx": 0, "octave_shift": 1}, # 4th 16th
        ]

        note_duration_16th = 0.25 # in beats (for staccato feel)
        total_notes_added = 0
        
        # Get the actual MIDI notes for the specified key, scale, and base octave
        # We need the intervals from the root, not the absolute MIDI notes here.
        # So we adapt the helper function or define internal scale intervals.
        root_midi_base = get_scale_midi_notes(key, "major", octave)[0] # Get absolute MIDI for the root in base octave
        
        # Get scale intervals (0-11 semitones from root)
        NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
        SCALES = {
            "major":            [0, 2, 4, 5, 7, 9, 11],
            "minor":            [0, 2, 3, 5, 7, 8, 10], # Natural minor
            "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
            "dorian":           [0, 2, 3, 5, 7, 9, 10],
            "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
            "pentatonic_major": [0, 2, 4, 7, 9],
            "pentatonic_minor": [0, 3, 5, 7, 10],
            "blues":            [0, 3, 5, 6, 7, 10],
        }
        scale_intervals_semitones = SCALES.get(scale, SCALES["minor"])

        for bar in range(bars):
            for step in pattern_steps:
                beat_pos = (bar * beats_per_bar) + step["beat_offset"]
                
                # Calculate the pitch based on root_midi_base, scale degree interval, and octave shift
                scale_degree_interval = scale_intervals_semitones[step["scale_degree_idx"] % len(scale_intervals_semitones)]
                pitch = root_midi_base + scale_degree_interval + (step["octave_shift"] * 12)
                
                # Clamp velocity to MIDI range (0-127)
                velocity = max(20, min(127, velocity_base + random.randint(-5, 5))) # Add slight velocity variation

                # Insert note
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, beat_pos, beat_pos + note_duration_16th,
                                        0, pitch, velocity, True)
                total_notes_added += 1

        RPR.RPR_MIDI_Sort(midi_take) # Sort notes after insertion for good measure
        # RPR_MIDI_SetItemExtents is automatically handled by MIDI_InsertNote if last parameter is True,
        # but calling it manually here ensures the item's visual length reflects the notes.
        # However, RPR_SetMediaItemInfo_Value("D_LENGTH") sets the item length, not notes.
        # If the item length is longer than the notes, it will loop empty space.
        # If the item length is shorter than notes, it will cut off.
        # We set D_LENGTH based on bars, so notes should fit within this.
        RPR.RPR_UpdateArrange() # Update arrangement view
        
        return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM."

    finally:
        RPR.RPR_Undo_EndBlock2(0, "Create Retro Synth Arpeggiated Bassline", True) # End undo block
        RPR.RPR_PreventUIRefresh(-1)


