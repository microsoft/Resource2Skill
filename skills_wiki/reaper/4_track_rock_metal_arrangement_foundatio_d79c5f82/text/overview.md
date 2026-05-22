### 1. High-level Design Pattern Extraction

> **Skill Name**: 4-Track Rock/Metal Arrangement Foundation

* **Core Musical Mechanism**: This pattern establishes a dense, multi-instrument "wall of sound" by interlocking four distinct musical layers: a driving 8th-note root-bass, sustained power chords (rhythm guitar), a syncopated drum backbeat, and an arpeggiated/syncopated lead melody. The mechanism relies on frequency and rhythmic separation—the bass holds the constant rhythmic pulse, the rhythm guitar fills the harmonic midrange with sustained notes, the drums provide the foundational transient groove, and the lead dances over the top.
* **Why Use This Skill (Rationale)**: Arranging multiple MIDI instruments can quickly become muddy. This workflow pattern encodes the quintessential rock/metal/pop-punk arrangement strategy. By strictly assigning rhythmic roles (8th notes to bass/hi-hats, whole notes to rhythm harmony, backbeat to snare), it maximizes sonic impact without frequency masking. The use of "split notes to grid" (8th notes) for the bass creates the iconic driving, chugging momentum.
* **Overall Applicability**: Perfect for generating the core foundation of rock, metal, pop-punk, or cinematic action tracks. It instantly provides a cohesive verse or chorus backing track that you can swap with premium VSTs (like Kontakt guitars or GetGood Drums).
* **Value Addition**: Compared to a blank project, this skill automatically orchestrates a complete 4-part arrangement based on a user-defined key and scale, handling the MIDI routing, chord voice-leading, and rhythmic interlocking across multiple synchronized tracks.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically 120-140 BPM.
  - **Grid**: Strict 8th-note grid drive.
  - **Bass**: Continuous 8th notes (0.5 beats each).
  - **Rhythm Guitar**: Sustained whole notes (4 beats) or half notes.
  - **Drums**: Kick on 1, 1.5, 2.5. Snare on 2 and 4. Hi-hats driving on every 8th note.
  - **Lead**: Syncopated 8th/16th notes or arpeggios floating over the barline.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Computes a standard 1-6-4-5 progression (I-vi-IV-V in major, i-VI-iv-v in minor) using scale lookups.
  - **Bass**: Root note of the current chord, dropped 2 octaves (`Root - 24`).
  - **Rhythm Guitar**: Power chords (Root, Perfect 5th, Octave) dropped 1 octave (`Root - 12`).
  - **Lead Guitar**: Arpeggiates the chord tones + 1 octave (`Root + 12`, `Third + 12`, `Fifth + 12`).

* **Step C: Sound Design & FX**
  - **Drums**: Standard General MIDI map (Kick: 36, Snare: 38, Hat: 42). 
  - **Tonal Instruments**: Basic instances of `ReaSynth` are loaded so the arrangement is immediately audible, separated by octave ranges. 

* **Step D: Mix & Automation**
  - **Panning**: Bass and Drums center, Rhythm Guitar panned slightly left, Lead Guitar panned slightly right to clear the center channel.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track Orchestration | `RPR_InsertTrackAtIndex()` & `RPR_AddMediaItemToTrack()` | Generates 4 distinct, identifiable tracks mirroring the tutorial's layout. |
| Rhythmic & Harmonic Generation | `RPR_MIDI_InsertNote()` with Theory Math | Translates the selected key/scale into exact MIDI notes across 4 tracks with precise timing relationships. |
| Initial Sound Generation | `RPR_TrackFX_AddByName("ReaSynth")` | Ensures the user hears the composition immediately without needing external premium VSTs. |

> **Feasibility Assessment**: 100% reproducible for the MIDI arrangement and composition strategy shown in the tutorial. The code constructs the exact 4-track layout and generates an arrangement replicating the creator's workflow demonstration.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrackArrangement",
    track_name: str = "Rock Foundation",
    bpm: int = 130,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Metal Arrangement Foundation in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_pitch = NOTE_MAP.get(key, 2) + 60 # Default to middle octave (e.g., C4 = 60)

    # 1-6-4-5 progression indices (0-indexed scale degrees)
    progression_indices = [0, 5, 3, 4]

    # === Helper Function for MIDI Note Insertion ===
    def insert_note(take, pitch, vel, start_beat, end_beat):
        # Convert beats to time based on BPM (assuming start at 0.0)
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        # Convert time to PPQ
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 1: Set Project Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    item_length_sec = total_beats * (60.0 / bpm)

    # Define track roles
    roles = [
        {"name": f"{track_name} - Drums", "pan": 0.0, "synth": False},
        {"name": f"{track_name} - Bass", "pan": 0.0, "synth": True},
        {"name": f"{track_name} - Rhythm GTR", "pan": -0.5, "synth": True},
        {"name": f"{track_name} - Lead GTR", "pan": 0.5, "synth": True}
    ]

    tracks_created = []

    # === Step 2: Generate Tracks & Items ===
    for role in roles:
        # Create track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", role["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", role["pan"])
        
        # Add basic synth if tonal
        if role["synth"]:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        # === Generate MIDI Content ===
        if "Drums" in role["name"]:
            # GM Drum Map: 36=Kick, 38=Snare, 42=Closed Hat
            for b in range(bars):
                bar_start = b * beats_per_bar
                # Kick pattern
                insert_note(take, 36, velocity_base, bar_start + 0.0, bar_start + 0.25)
                insert_note(take, 36, velocity_base - 10, bar_start + 1.5, bar_start + 1.75)
                insert_note(take, 36, velocity_base, bar_start + 2.5, bar_start + 2.75)
                
                # Snare pattern
                insert_note(take, 38, velocity_base + 10, bar_start + 1.0, bar_start + 1.25)
                insert_note(take, 38, velocity_base + 10, bar_start + 3.0, bar_start + 3.25)
                
                # Hi-hat 8th notes
                for hat in range(8):
                    vel = velocity_base if hat % 2 == 0 else velocity_base - 20
                    insert_note(take, 42, vel, bar_start + (hat * 0.5), bar_start + (hat * 0.5) + 0.25)

        elif "Bass" in role["name"]:
            for b in range(bars):
                bar_start = b * beats_per_bar
                deg_idx = progression_indices[b % len(progression_indices)]
                chord_root = root_pitch + scale_intervals[deg_idx]
                bass_pitch = chord_root - 24 # Drop 2 octaves
                
                # Driving 8th notes
                for eighth in range(8):
                    beat_pos = bar_start + (eighth * 0.5)
                    insert_note(take, bass_pitch, velocity_base, beat_pos, beat_pos + 0.45) # 0.45 for slight staccato separation

        elif "Rhythm GTR" in role["name"]:
            for b in range(bars):
                bar_start = b * beats_per_bar
                deg_idx = progression_indices[b % len(progression_indices)]
                chord_root = root_pitch + scale_intervals[deg_idx]
                gtr_root = chord_root - 12 # Drop 1 octave
                
                # Power chords: Root, Fifth (+7), Octave (+12)
                insert_note(take, gtr_root, velocity_base - 10, bar_start, bar_start + beats_per_bar)
                insert_note(take, gtr_root + 7, velocity_base - 15, bar_start, bar_start + beats_per_bar)
                insert_note(take, gtr_root + 12, velocity_base - 10, bar_start, bar_start + beats_per_bar)

        elif "Lead GTR" in role["name"]:
            for b in range(bars):
                bar_start = b * beats_per_bar
                deg_idx = progression_indices[b % len(progression_indices)]
                chord_root = root_pitch + scale_intervals[deg_idx]
                lead_root = chord_root + 12 # Up 1 octave
                
                # 3rd interval logic based on scale degree (Major or Minor 3rd)
                # To keep it simple, we compute the relative 3rd in the scale
                third_idx = (deg_idx + 2) % len(scale_intervals)
                third_pitch = root_pitch + scale_intervals[third_idx] + 12
                if third_idx < deg_idx: # Crossed octave
                    third_pitch += 12
                
                fifth_pitch = lead_root + 7
                
                # Simple syncopated arpeggio
                insert_note(take, lead_root, velocity_base, bar_start + 0.0, bar_start + 0.5)
                insert_note(take, third_pitch, velocity_base - 10, bar_start + 0.75, bar_start + 1.25)
                insert_note(take, fifth_pitch, velocity_base, bar_start + 1.5, bar_start + 2.5)
                insert_note(take, third_pitch, velocity_base - 5, bar_start + 3.0, bar_start + 3.5)

        # Apply and sort MIDI notes for the take
        RPR.RPR_MIDI_Sort(take)
        tracks_created.append(role["name"])

    return f"Created 4-track arrangement ({', '.join(tracks_created)}) spanning {bars} bars at {bpm} BPM in {key} {scale}."
```