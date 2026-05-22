### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Pop Arrangement Skeleton

* **Core Musical Mechanism**: This pattern generates a cohesive, 4-part rhythm section arrangement (Drums, Bass, Rhythm Chords, Arpeggiated Lead) utilizing standard functional diatonic harmony (e.g., I-V-vi-IV in major or i-VI-III-VII in minor). Beyond the notes themselves, the tracks are intentionally color-coded. In the tutorial, this multi-track layout and specific color-coding (`View -> Color notes by: Track`) is the core mechanism that makes single-window, multi-track MIDI editing visually decipherable and musically efficient.

* **Why Use This Skill (Rationale)**: Sonically, this encapsulates standard frequency separation: Bass holds down the root and low-end pulse, Rhythm Guitars/Synths provide midrange harmonic support via sustained power chords, the Lead occupies the higher frequency range with melodic 8th-note arpeggios, and the Drums provide the rhythmic grid. From a workflow perspective, rendering these four layers simultaneously with distinct colors gives the producer an immediate "sandbox" to practice multi-track orchestration and testing REAPER's advanced MIDI editor visibility/editability toggles.

* **Overall Applicability**: This is the quintessential starting point for rock, pop, synthwave, or orchestral templates. It establishes the rhythm section backbone, allowing producers to immediately focus on tweaking the groove, adjusting voicings, or designing synth patches without having to click in a 4-bar progression from scratch. 

* **Value Addition**: Compared to a blank MIDI clip, this skill encodes standard voice-leading, rhythm section roles, and diatonic scale math. It transforms a blank project into a fully harmonized, layered loop that is specifically optimized for multi-track visibility in REAPER's MIDI editor.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically 120 BPM.
  - **Drums**: Standard backbeat. Kick on 1 and 3 (with syncopated 16ths). Snare on 2 and 4. 8th note hi-hats. Crash on the downbeat of bar 1.
  - **Bass**: Straight pulsing 8th notes, emphasizing the root.
  - **Rhythm**: Whole notes or half notes (sustained chords) to establish the harmonic bed.
  - **Lead**: 8th-note ascending/descending arpeggios outlining the underlying chord shapes.

* **Step B: Pitch & Harmony**
  - **Harmony**: Uses a standard 4-chord progression. In minor, it defaults to the epic `i - VI - III - VII` progression. In major, it uses `I - V - vi - IV`. 
  - **Voicings**: Rhythm track uses 3-note triad/power chord voicings in the 3rd/4th octave. Lead uses single notes spread across the 4th and 5th octaves. Bass plays single root notes in the 1st/2nd octave.
  - All pitches are computed dynamically from the root key and scale arrays to ensure perfect diatonic compliance.

* **Step C: Sound Design & FX**
  - This script builds the foundational MIDI and color-codes the tracks (Magenta for Drums, Purple for Bass, Orange for Rhythm, Cyan for Lead) directly reflecting the tutorial's visual setup.
  - *Note: To hear the instruments, the user will route their preferred drum samplers and VST synths/guitars to these tracks.*

* **Step D: Mix & Automation**
  - Tracks are inserted sequentially and distinctly named to align with standard mixing console layouts (Drums -> Bass -> Rhythm -> Lead).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track layout | Track Insertion & Coloring | Matches tutorial's visual color-coding strategy for multi-track editing (`I_CUSTOMCOLOR`). |
| Harmonic progression | Programmatic Diatonic Math | Allows the pattern to dynamically adapt to any user-provided Key and Scale. |
| Notes & Rhythms | MIDI Note Insertion (`RPR_MIDI_InsertNote`) | Provides sample-accurate PPQ timing and precise velocity layering for all 4 distinct instruments. |

> **Feasibility Assessment**: 100% reproducible for the MIDI content, track layout, and visual color-coding demonstrated. The specific virtual guitar/drum VSTs shown in the video (e.g., Kontakt, GetGood Drums) are third-party and cannot be natively spawned with audio, so the code focuses entirely on the high-value MIDI orchestration and REAPER layout.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrack_Workflow",
    track_name: str = "Arrangement",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Pop Arrangement Skeleton (Drums, Bass, Rhythm, Lead).
    Optimized with custom track colors for REAPER's multi-track MIDI editor.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks (unused, overridden internally).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major or minor).
        bars: Number of bars to generate (must be multiple of 4 for the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_val = NOTE_MAP.get(key, 11)  # Default B
    scale_arr = SCALES.get(scale, SCALES["minor"])
    
    # Standard progressions: minor (i, VI, III, VII), major (I, V, vi, IV)
    if scale == "minor":
        prog_degrees = [0, 5, 2, 6] 
    else:
        prog_degrees = [0, 4, 5, 3]

    # Calculate exact chord notes (Root, Third, Fifth) based on scale degrees
    chords = []
    for deg in prog_degrees:
        r = (root_val + scale_arr[deg]) % 12
        t_deg = (deg + 2) % 7
        t_oct = 12 if (deg + 2) >= 7 else 0
        t = (root_val + scale_arr[t_deg] + t_oct) % 12
        f_deg = (deg + 4) % 7
        f_oct = 12 if (deg + 4) >= 7 else 0
        f = (root_val + scale_arr[f_deg] + f_oct) % 12
        chords.append((r, t, f))

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Timing calculations
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars
    
    track_definitions = [
        {"name": "01 DRUMS", "color": 0x1000000 | (128 << 16) | (0 << 8) | 255},  # Magenta
        {"name": "02 BASS", "color": 0x1000000 | (255 << 16) | (0 << 8) | 128},   # Purple
        {"name": "03 RHYTHM", "color": 0x1000000 | (0 << 16) | (128 << 8) | 255}, # Orange
        {"name": "04 LEAD", "color": 0x1000000 | (255 << 16) | (255 << 8) | 0}    # Cyan
    ]

    created_tracks = 0
    start_track_idx = RPR.RPR_CountTracks(0)

    for i, t_def in enumerate(track_definitions):
        # Create Track
        idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        
        # Naming and Coloring
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_def["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_def["color"])
        
        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # Populate MIDI based on track role
        for bar in range(bars):
            bar_start_time = bar * bar_len
            chord_idx = bar % 4
            r, t, f = chords[chord_idx]
            
            # --- DRUMS ---
            if i == 0:
                # Kick (1, 2.5, 3)
                for b_offset in [0.0, 1.5, 2.0]:
                    t_pos = bar_start_time + (b_offset * beat_len)
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos + (beat_len/2))
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 36, velocity_base, False)
                # Snare (2, 4)
                for b_offset in [1.0, 3.0]:
                    t_pos = bar_start_time + (b_offset * beat_len)
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos + (beat_len/2))
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 38, velocity_base, False)
                # Hi-Hats (8th notes)
                for eighth in range(8):
                    t_pos = bar_start_time + (eighth * (beat_len/2))
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos + (beat_len/4))
                    vel = velocity_base if eighth % 2 == 0 else int(velocity_base * 0.7)
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 42, vel, False)
                # Crash (Bar 1, Beat 1 only)
                if bar % 4 == 0:
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time + beat_len)
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, 49, velocity_base+10, False)

            # --- BASS ---
            elif i == 1:
                # 8th note pulsing root notes, 1st octave (Root + 24)
                bass_pitch = r + 24
                # Adjust if pitch drops too low
                if bass_pitch < 28: bass_pitch += 12 
                for eighth in range(8):
                    t_pos = bar_start_time + (eighth * (beat_len/2))
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos + (beat_len/2 * 0.8)) # slightly staccato
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, bass_pitch, velocity_base, False)

            # --- RHYTHM GUITAR/SYNTH ---
            elif i == 2:
                # Whole note sustained chords in 3rd/4th octave
                ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
                ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time + bar_len)
                base_oct = 48
                for p in [r, t, f]:
                    pitch = p + base_oct
                    # Keep voicings tight
                    if pitch > 64: pitch -= 12
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, pitch, velocity_base-10, False)

            # --- LEAD GUITAR/SYNTH ---
            elif i == 3:
                # Ascending/Descending 8th note arpeggios
                arp_pattern = [r, t, f, t, r, f, t, r]
                base_oct = 60
                for eighth in range(8):
                    t_pos = bar_start_time + (eighth * (beat_len/2))
                    ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos)
                    ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_pos + (beat_len/2 * 0.9))
                    pitch = arp_pattern[eighth] + base_oct
                    if pitch < 60: pitch += 12
                    RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, pitch, velocity_base+5, False)
                    
        # Sort MIDI events after insertion
        RPR.RPR_MIDI_Sort(take)
        created_tracks += 1

    RPR.RPR_UpdateArrange()
    return f"Created 4-track layered arrangement skeleton over {bars} bars in {key} {scale} at {bpm} BPM."
```