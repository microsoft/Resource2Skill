### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Pop-Punk / Rock Arrangement (I-V-vi-IV Stack)

* **Core Musical Mechanism**: This pattern represents the quintessential modern rock / pop-punk full band arrangement. It features a high-energy 160 BPM syncopated drum groove (kick on beats 1, 2.5, and 3), a driving 8th-note bassline mirroring the roots, dense 8th-note power chords on the rhythm guitar, and an alternating 8th-note ostinato lead melody (pedaling the root and third of the underlying chords). 
* **Why Use This Skill (Rationale)**: The I-V-vi-IV progression is one of the most powerful and recognizable harmonic structures in modern music. Stacking an 8th-note straight rhythm across the bass and rhythm guitars creates a "wall of sound" and extreme forward momentum. The syncopated kick drum adds groove against the straight 8th notes, while the high-octave lead guitar ostinato provides melodic interest without cluttering the mid-range power chords.
* **Overall Applicability**: Perfect for choruses, intros, and drops in rock, pop-punk, emo, and alternative metal genres. It serves as a foundational "band-in-a-box" scaffolding that producers can swap with real amp sims, bass VSTs, and drum samplers.
* **Value Addition**: Transforms an empty project into a fully arranged, 4-part polyphonic rock section. It mathematically encodes voice leading for power chords, bass octave placements, and complementary drum groove timing all synced to a single harmonic progression.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo & Signature**: ~160 BPM, 4/4 time.
  - **Grid**: Strict 1/8th note driving pulse for Bass, Rhythm Guitar, and Lead Guitar. 
  - **Drum Groove**: Kick on 1, 2.5 (syncopated off-beat), and 3. Snare firmly planted on 2 and 4. Hi-hats play constant 8th notes. A crash cymbal accents the downbeat of the 1st bar.
  - **Note Durations**: Guitars and bass use slightly shortened durations (0.40 - 0.45 beats instead of a full 0.5) to emulate the aggressive, staccato "chugging" playing style.

* **Step B: Pitch & Harmony**
  - **Progression**: I - V - vi - IV (e.g., in D Major: D5 - A5 - B5 - G5).
  - **Bass**: Plays the root notes strictly in the 1st/2nd octave. 
  - **Rhythm Guitars**: Root-5th-Octave power chords mapped to the 2nd/3rd octave, automatically adjusting contour to drop the V and vi chords down for a heavier sound.
  - **Lead Guitar**: An alternating 8th-note ostinato playing the root and the 3rd of the active chord, transposed up two octaves (C5/C6 range) to cut through the mix.

* **Step C: Sound Design & FX**
  - **Instruments**: To ensure immediate playback, a stock `ReaSynth` instance is loaded on every track.
  - **Track Coloring**: Mirrors the visual organization shown in the tutorial (Drums = Magenta, Bass = Blue, Rhythm = Orange, Lead = Teal) to optimize workflow in REAPER's multi-track MIDI editor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-Track Architecture | Track Creation & Coloring | Prepares the exact workspace needed for the multi-track MIDI editing workflow shown in the video. |
| Rock Band Arrangement | MIDI note insertion | Allows precise, algorithmic construction of drum patterns, power chords, and melodies tied to global scale parameters. |
| Audibility | FX chain (ReaSynth) | Adds native REAPER synths to the generated MIDI tracks so the arrangement can be previewed immediately. |

> **Feasibility Assessment**: 100% reproducible for the MIDI, harmonic architecture, and workflow setup. Timbral reproduction (the actual sound of distorted guitars and acoustic drums) relies on placeholder synths, as third-party amp sims (like Neural DSP or Kontakt) are not native to REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "PopPunkArrangement",
    track_name: str = "Rock Band",
    bpm: int = 160,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a 4-track Rock/Pop-Punk arrangement (Drums, Bass, Rhythm, Lead)
    in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (160 is ideal for this genre).
        key: Root note (e.g., "D").
        scale: Scale type (e.g., "major").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Validate scale and key
    key_offset = NOTE_MAP.get(key, 2)  # Default to D
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    # Extend scale to 3 octaves to prevent out-of-bounds index lookups
    ext_scale = scale_intervals + [x + 12 for x in scale_intervals] + [x + 24 for x in scale_intervals]
    
    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # REAPER API Colors (R | G<<8 | B<<16 | 0x1000000)
    col_magenta = 255 | (0 << 8) | (255 << 16) | 0x1000000
    col_blue    = 0 | (100 << 8) | (255 << 16) | 0x1000000
    col_orange  = 255 | (128 << 8) | (0 << 16) | 0x1000000
    col_teal    = 0 | (255 << 8) | (255 << 16) | 0x1000000

    tracks_config = [
        {"name": f"{track_name} - Drums", "color": col_magenta},
        {"name": f"{track_name} - Bass",  "color": col_blue},
        {"name": f"{track_name} - Rhy",   "color": col_orange},
        {"name": f"{track_name} - Lead",  "color": col_teal}
    ]

    takes = []
    
    # Track & MIDI Item creation helper
    for config in tracks_config:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Naming & Coloring
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", config["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", config["color"])
        
        # Add basic Synth so it makes sound
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        # Create Media Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        item_length_sec = (60.0 / bpm) * 4 * bars
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes.append(take)

    drum_take, bass_take, rhy_take, lead_take = takes

    # Note Insertion Helper
    def add_note(take, pitch, start_beat, end_beat, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    total_notes_added = 0

    # Musical Data Generation Loop
    # Standard rock contour degrees: I (mid), V (low), vi (low), IV (low)
    # Using array indices of the extended scale: 7=I, 4=V, 5=vi, 3=IV
    contour_degrees = [7, 4, 5, 3] 

    for b in range(bars):
        bar_start_beat = b * 4
        base_deg = contour_degrees[b % 4]
        
        # Pre-calculate interval pitches for this bar
        root_interval = ext_scale[base_deg]
        third_interval = ext_scale[base_deg + 2]
        
        bass_root = 24 + key_offset + root_interval    # Octave 1/2
        rhy_root  = 36 + key_offset + root_interval    # Octave 2/3
        lead_root = 60 + key_offset + root_interval    # Octave 4/5
        lead_3rd  = 60 + key_offset + third_interval   # Octave 4/5

        # Beat-level generation (8th notes)
        for half_beat in range(8):
            beat_pos = bar_start_beat + (half_beat * 0.5)
            
            # --- 1. DRUMS ---
            # Crash on first downbeat of the section
            if b == 0 and half_beat == 0:
                add_note(drum_take, 49, beat_pos, beat_pos + 0.5, velocity_base + 10)
                total_notes_added += 1
            
            # Hi-hat (constant 8th notes, alternating velocity)
            hh_vel = velocity_base if half_beat % 2 == 0 else velocity_base - 20
            add_note(drum_take, 42, beat_pos, beat_pos + 0.25, hh_vel)
            total_notes_added += 1

            # Kick (Beats 1, 2.5, 3) mapped to half_beats 0, 3, 4
            if half_beat in [0, 3, 4]:
                add_note(drum_take, 36, beat_pos, beat_pos + 0.25, velocity_base + 10)
                total_notes_added += 1
            
            # Snare (Beats 2, 4) mapped to half_beats 2, 6
            if half_beat in [2, 6]:
                add_note(drum_take, 38, beat_pos, beat_pos + 0.25, velocity_base + 15)
                total_notes_added += 1

            # --- 2. BASS ---
            # Driving 8th notes (slightly detached length = 0.45)
            add_note(bass_take, bass_root, beat_pos, beat_pos + 0.45, velocity_base)
            total_notes_added += 1

            # --- 3. RHYTHM GUITAR (Power Chords) ---
            # Root, Fifth (+7), Octave (+12). Shorter duration for "chugging" = 0.40
            add_note(rhy_take, rhy_root,      beat_pos, beat_pos + 0.40, velocity_base)
            add_note(rhy_take, rhy_root + 7,  beat_pos, beat_pos + 0.40, velocity_base)
            add_note(rhy_take, rhy_root + 12, beat_pos, beat_pos + 0.40, velocity_base)
            total_notes_added += 3

            # --- 4. LEAD GUITAR ---
            # Alternating ostinato (Root, Third, Root, Third...)
            lead_pitch = lead_root if half_beat % 2 == 0 else lead_3rd
            add_note(lead_take, lead_pitch, beat_pos, beat_pos + 0.45, velocity_base)
            total_notes_added += 1

    # Commit all MIDI changes
    for take in takes:
        RPR.RPR_MIDI_Sort(take)

    return f"Created {len(tracks_config)} tracks with {total_notes_added} stacked MIDI notes over {bars} bars at {bpm} BPM in {key} {scale}."
```