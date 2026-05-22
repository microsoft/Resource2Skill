def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "LofiArrangement",
    bpm: int = 85,
    key: str = "C",
    scale: str = "major",
    bars: int = 32,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Additive Lo-Fi Beat Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (70-90 recommended for lo-fi).
        key: Root note (e.g., "C", "F#").
        scale: Scale type (e.g., "major", "minor").
        bars: Total number of bars to generate (32 recommended to hear full evolution).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
    }

    root_offset = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def get_pitch(degree: int, base_octave: int = 4) -> int:
        """Calculate MIDI pitch for a given scale degree (0-indexed)."""
        octave = degree // 7
        deg = degree % 7
        return (base_octave * 12) + root_offset + scale_intervals[deg] + (octave * 12)

    def create_track_with_item(name: str, total_bars: int):
        """Creates a track and an empty MIDI item spanning the total duration."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)

        bar_len_sec = (60.0 / bpm) * 4  # 4 beats per bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_bars * bar_len_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    # Step 2: Create Tracks
    takes = {
        "Chords": create_track_with_item(f"{track_name}_Chords", bars),
        "Kick": create_track_with_item(f"{track_name}_Kick", bars),
        "Snare": create_track_with_item(f"{track_name}_Snare", bars),
        "Hats": create_track_with_item(f"{track_name}_Hats", bars),
        "Bass": create_track_with_item(f"{track_name}_Bass", bars),
        "Lead": create_track_with_item(f"{track_name}_Lead", bars),
        "Piano": create_track_with_item(f"{track_name}_Piano", bars)
    }

    def add_note(take, start_beat: float, end_beat: float, pitch: int, vel: float):
        """Helper to insert a note using beats relative to the project start."""
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Clamp velocity
        v = max(1, min(127, int(vel)))
        p = max(0, min(127, int(pitch)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, v, True)

    # Step 3: Generative Arrangement Logic
    # 4-bar descending progression: IV -> iii -> ii -> I (Scale degrees 3, 2, 1, 0)
    progression = [3, 2, 1, 0] 

    for b in range(0, bars, 4):
        # Arrangement structure checks based on bar blocks
        is_intro = (b < 4)
        is_build = (b >= 4 and b < 8)
        is_groove_a = (b >= 8 and b < 16)
        is_groove_b = (b >= 16 and b < 24)
        is_b_sect = (b >= 24 and b < 32)

        # Iterate through the 4 bars in the current block
        for bar_offset in range(4):
            global_bar = b + bar_offset
            if global_bar >= bars:
                break
                
            start_b = global_bar * 4 # Beat index
            chord_deg = progression[bar_offset % len(progression)]

            # 1. Chords (Always active) - Diatonic 7th chords
            add_note(takes["Chords"], start_b, start_b + 4, get_pitch(chord_deg, 4), velocity_base * 0.8)
            add_note(takes["Chords"], start_b, start_b + 4, get_pitch(chord_deg + 2, 4), velocity_base * 0.7)
            add_note(takes["Chords"], start_b, start_b + 4, get_pitch(chord_deg + 4, 4), velocity_base * 0.7)
            add_note(takes["Chords"], start_b, start_b + 4, get_pitch(chord_deg + 6, 4), velocity_base * 0.7)

            # 2. Kick (Always active) - Syncopated Lofi rhythm
            add_note(takes["Kick"], start_b + 0.0, start_b + 0.5, 36, velocity_base)
            add_note(takes["Kick"], start_b + 1.5, start_b + 2.0, 36, velocity_base * 0.85)
            add_note(takes["Kick"], start_b + 2.5, start_b + 3.0, 36, velocity_base * 0.75)

            # 3. Snare & Hats (Introduced after Intro)
            if not is_intro:
                # Snare on 2 and 4
                add_note(takes["Snare"], start_b + 1.0, start_b + 1.5, 38, velocity_base)
                add_note(takes["Snare"], start_b + 3.0, start_b + 3.5, 38, velocity_base)

                # 8th note hi-hats with velocity variation for groove
                for i in range(8):
                    hat_vel = velocity_base if i % 2 == 0 else velocity_base * 0.55
                    add_note(takes["Hats"], start_b + (i * 0.5), start_b + (i * 0.5) + 0.2, 42, hat_vel)

            # 4. Bass (Introduced in Groove sections) - Follows Kick rhythm
            if is_groove_a or is_groove_b or is_b_sect:
                bass_pitch = get_pitch(chord_deg, 2) # Root note, Octave 2
                add_note(takes["Bass"], start_b + 0.0, start_b + 1.0, bass_pitch, velocity_base * 0.9)
                add_note(takes["Bass"], start_b + 1.5, start_b + 2.0, bass_pitch, velocity_base * 0.8)
                add_note(takes["Bass"], start_b + 2.5, start_b + 3.5, bass_pitch, velocity_base * 0.9)

            # 5. Lead Synth (Introduced in Groove B)
            if is_groove_b:
                add_note(takes["Lead"], start_b + 0.0, start_b + 0.5, get_pitch(chord_deg + 7, 5), velocity_base)
                add_note(takes["Lead"], start_b + 1.0, start_b + 1.5, get_pitch(chord_deg + 9, 5), velocity_base * 0.8)
                add_note(takes["Lead"], start_b + 2.5, start_b + 3.0, get_pitch(chord_deg + 7, 5), velocity_base * 0.9)

            # 6. Piano Counter-Melody (Swapped in for B-Section)
            if is_b_sect:
                add_note(takes["Piano"], start_b + 0.0, start_b + 0.5, get_pitch(chord_deg + 7, 5), velocity_base)
                add_note(takes["Piano"], start_b + 0.5, start_b + 1.0, get_pitch(chord_deg + 9, 5), velocity_base * 0.8)
                add_note(takes["Piano"], start_b + 1.0, start_b + 1.5, get_pitch(chord_deg + 11, 5), velocity_base * 0.9)
                add_note(takes["Piano"], start_b + 1.5, start_b + 2.0, get_pitch(chord_deg + 9, 5), velocity_base * 0.7)

    # Step 4: Finalize MIDI Takes
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created full additive arrangement across 7 tracks over {bars} bars at {bpm} BPM."
