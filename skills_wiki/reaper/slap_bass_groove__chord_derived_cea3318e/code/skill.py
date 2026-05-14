import reaper_python as RPR
import random

def create_slap_bass_groove(
    project_name: str = "SlapBassProject",
    main_bass_track_name: str = "Slap Bass Main",
    slap_bass_track_name: str = "Slap Bass Slap",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    main_velocity_base: int = 100,
    slap_velocity_base: int = 80,
    humanize_strength: float = 0.02, # Max +/- beats for timing, +/- velocity percent
    **kwargs,
) -> str:
    """
    Creates a slap bass groove with distinct main and slap bass sounds, derived from a chord progression.

    Args:
        project_name: Project identifier (for logging).
        main_bass_track_name: Name for the main bass track.
        slap_bass_track_name: Name for the slap bass track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        main_velocity_base: Base MIDI velocity for main bass notes (0-127).
        slap_velocity_base: Base MIDI velocity for slap notes (0-127).
        humanize_strength: Max random offset for timing (in beats) and velocity (as fraction of base).
        **kwargs: Additional overrides (not used in this skill but for compatibility).

    Returns:
        Status string describing what was created.
    """
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

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Must be one of {list(SCALES.keys())}"

    root_midi_offset = NOTE_MAP[key] # C0 is MIDI 0

    # Ensure REAPER is running
    if not RPR.RPR_GetProjectName(0, "", 0)[0]:
        RPR.RPR_ShowConsoleMsg("REAPER not running or project not loaded.\n")
        return "Error: REAPER not ready."

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_idx_main = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_main, True)
    track_main = RPR.RPR_GetTrack(0, track_idx_main)
    RPR.RPR_GetSetMediaTrackInfo_String(track_main, "P_NAME", main_bass_track_name, True)

    track_idx_slap = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx_slap, True)
    track_slap = RPR.RPR_GetTrack(0, track_idx_slap)
    RPR.RPR_GetSetMediaTrackInfo_String(track_slap, "P_NAME", slap_bass_track_name, True)

    # === Step 3: Add FX Chains (ReaSynth for both) ===
    # Main Bass ReaSynth config
    RPR.RPR_TrackFX_AddByName(track_main, "ReaSynth", False, -1)
    fx_main_idx = RPR.RPR_TrackFX_GetCount(track_main) - 1
    # Set waveform (0=sine, 1=saw, 2=square, 3=triangle)
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 15, 0.5) # Waveform to Sawtooth (0.5 for Saw)
    # Env: Attack, Decay, Sustain, Release
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 0, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 1, 0.2) # Decay
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 2, 0.7) # Sustain
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 3, 0.1) # Release
    # Filter
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 8, 0.0) # Filter type (0=LPF)
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 9, 0.35) # Cutoff (around 700Hz)
    RPR.RPR_TrackFX_SetParam(track_main, fx_main_idx, 10, 0.05) # Resonance

    # Slap Bass ReaSynth config
    RPR.RPR_TrackFX_AddByName(track_slap, "ReaSynth", False, -1)
    fx_slap_idx = RPR.RPR_TrackFX_GetCount(track_slap) - 1
    # Set waveform
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 15, 0.75) # Waveform to Triangle (0.75 for Triangle)
    # Env: Attack, Decay, Sustain, Release (very short for slap)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 0, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 1, 0.05) # Decay
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 2, 0.0) # Sustain
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 3, 0.01) # Release
    # Filter (highpass for brightness)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 8, 0.5) # Filter type (0.5 for HPF)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 9, 0.7) # Cutoff (around 1.5kHz)
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 10, 0.2) # Resonance
    RPR.RPR_TrackFX_SetParam(track_slap, fx_slap_idx, 16, 0.8) # Volume slightly lower

    # === Step 4: Create MIDI Items ===
    beats_per_bar = 4
    item_length_beats = beats_per_bar * bars
    item_main = RPR.RPR_AddMediaItemToTrack(track_main)
    RPR.RPR_SetMediaItemInfo_Value(item_main, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_main, "D_LENGTH", item_length_beats / beats_per_bar * (60.0 / bpm) * beats_per_bar) # Length in seconds
    take_main = RPR.RPR_GetActiveTake(item_main)
    RPR.RPR_MIDI_Clear(RPR.MIDI_SetItemExt(item_main, take_main, False)) # Clear existing MIDI

    item_slap = RPR.RPR_AddMediaItemToTrack(track_slap)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_slap, "D_LENGTH", item_length_beats / beats_per_bar * (60.0 / bpm) * beats_per_bar) # Length in seconds
    take_slap = RPR.RPR_GetActiveTake(item_slap)
    RPR.RPR_MIDI_Clear(RPR.MIDI_SetItemExt(item_slap, take_slap, False)) # Clear existing MIDI

    RPR.RPR_PreventUIRefresh(1) # Prevent UI refresh during note insertion

    # Define the chord progression roots relative to the key (0=I, 5=IV, 7=V) based on video example
    # Cmin, Fmaj, Gmaj, Cmin
    # Roots: C, F, G, C
    chord_roots_relative = [0, 5, 7, 0] # Intervals from the key's root
    
    # Octave for the main bassline
    base_octave = 2 # C2 (MIDI 36)

    notes_added_count = 0

    for bar in range(bars):
        current_bar_start_beat = bar * beats_per_bar
        chord_root_interval = chord_roots_relative[bar % len(chord_roots_relative)]
        current_root_midi = root_midi_offset + chord_root_interval + (base_octave * 12)

        # Helper to get the 5th of a given root, adjusted for desired octave
        def get_fifth(root_midi):
            # C major scale for intervals, then adjust octave to stay in bass range
            fifth = root_midi + 7 # interval of a perfect fifth
            if fifth > (base_octave + 1) * 12 + root_midi_offset + 5: # If too high, bring down an octave
                fifth -= 12
            return fifth

        current_fifth_midi = get_fifth(current_root_midi)

        # --- Main Bass Track Notes ---
        # Note 1: Root on Beat 1 (1/4 note duration)
        pos = current_bar_start_beat
        vel = max(1, min(127, main_velocity_base + random.randint(int(-main_velocity_base * humanize_strength), int(main_velocity_base * humanize_strength))))
        offset = (random.random() * 2 - 1) * humanize_strength
        RPR.RPR_MIDI_InsertNote(RPR.MIDI_SetItemExt(item_main, take_main, True), False, False, pos + offset, pos + offset + 1.0, 0, current_root_midi, vel, False)
        notes_added_count += 1

        # Note 2: Fifth on Beat 2 (1/8 note duration)
        pos = current_bar_start_beat + 2.0
        vel = max(1, min(127, main_velocity_base + random.randint(int(-main_velocity_base * humanize_strength), int(main_velocity_base * humanize_strength))))
        offset = (random.random() * 2 - 1) * humanize_strength
        RPR.RPR_MIDI_InsertNote(RPR.MIDI_SetItemExt(item_main, take_main, True), False, False, pos + offset, pos + offset + 0.5, 0, current_fifth_midi, vel, False)
        notes_added_count += 1

        # --- Slap Bass Track Notes ---
        # Slap 1: Root + 1 octave on Beat 1.5 (1/16 note duration, very short)
        pos = current_bar_start_beat + 1.5
        vel = max(1, min(127, slap_velocity_base + random.randint(int(-slap_velocity_base * humanize_strength), int(slap_velocity_base * humanize_strength))))
        offset = (random.random() * 2 - 1) * humanize_strength
        RPR.RPR_MIDI_InsertNote(RPR.MIDI_SetItemExt(item_slap, take_slap, True), False, False, pos + offset, pos + offset + 0.25, 0, current_root_midi + 12, vel, False)
        notes_added_count += 1

        # Slap 2: Root + 1 octave on Beat 2.5 (1/16 note duration, very short)
        pos = current_bar_start_beat + 2.5
        vel = max(1, min(127, slap_velocity_base + random.randint(int(-slap_velocity_base * humanize_strength), int(slap_velocity_base * humanize_strength))))
        offset = (random.random() * 2 - 1) * humanize_strength
        RPR.RPR_MIDI_InsertNote(RPR.MIDI_SetItemExt(item_slap, take_slap, True), False, False, pos + offset, pos + offset + 0.25, 0, current_root_midi + 12, vel, False)
        notes_added_count += 1

    RPR.RPR_MIDI_Sort(RPR.MIDI_SetItemExt(item_main, take_main, True))
    RPR.RPR_MIDI_Sort(RPR.MIDI_SetItemExt(item_slap, take_slap, True))
    RPR.RPR_UpdateArrange()
    RPR.RPR_PreventUIRefresh(-1) # Resume UI refresh

    return f"Created '{main_bass_track_name}' and '{slap_bass_track_name}' with {notes_added_count} notes over {bars} bars at {bpm} BPM."

