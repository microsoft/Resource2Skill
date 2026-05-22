### 1. High-level Design Pattern Extraction

> **Skill Name**: Neo-Soul/R&B Bassline Construction (Root, Octave, 5th, Passing Tone)

* **Core Musical Mechanism**: The foundational technique of building an R&B/Neo-Soul bassline by starting with long, anchored root notes, then injecting rhythmic energy using syncopated octave jumps. Once the root and octave framework is established, diatonic passing tones (most notably the minor 7th and the perfect 5th) are inserted on the offbeats to create smooth, melodic voice-leading into the next chord change.
* **Why Use This Skill (Rationale)**: This formula works because it perfectly balances harmonic stability with rhythmic groove. The low root establishes the chord, the octave jump adds rhythmic bounce without changing the harmonic function (avoiding clashes), and the passing tones (minor 7th / perfect 5th) act as melodic glue. Placing these passing notes on syncopated subdivisions (like the "and" of beat 3 or 4) creates a "push" or "pull" feeling that characterizes the groove of modern R&B, Gospel, and Hip-Hop.
* **Overall Applicability**: Essential for Neo-Soul, R&B, Gospel, Hip-Hop, and Lofi. It serves as the primary engine for moving a progression forward without overly dense harmony. 
* **Value Addition**: Replaces static, robotic quarter-note basslines with a dynamic, syncopated, voice-led groove. It encodes the specific "Root -> Syncopated Octave -> Passing Tone" heuristic that professional session bassists use to build parts on the fly.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically around 80-100 BPM (90 BPM used here).
  - **Rhythmic Grid**: Syncopated 8th and 16th notes.
  - **Duration Pattern**: 
    - Beat 1.0: Root (Low) — Long duration (sustains for 1.5 beats).
    - Beat 2.5 (the "and" of 2, or beat 3 pickup): Root (High/Octave) — Short duration (0.5 beats).
    - Beat 3.5 (the "and" of 4): Passing Tone — Short duration (0.5 beats), leading directly into the next bar.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: F Minor (Video demonstrates F minor to C minor, which is a i -> v progression in F minor).
  - **Voicing Structure**: 
    - Note 1: `Root`
    - Note 2: `Root + 12` (Octave up)
    - Note 3: Alternating between `Root + 10` (Minor 7th) and `Root + 7` (Perfect 5th).
  - **Range Enforcement**: Roots are constrained strictly to MIDI Octave 1 (notes 24-35) to keep the bass heavy.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth`.
  - **Timbre**: Deep, muted tone resembling a vintage bass guitar or Moog sub-bass. Achieved by mixing Triangle (1.0) and Sine (1.0) waves with zero Saw/Square, creating a naturally filtered, warm low-end without harsh upper harmonics.
  - **Envelope**: Fast attack (10ms) for punch, medium decay, and a relatively tight release (100ms) so syncopated notes don't bleed into each other.

* **Step D: Mix & Automation**
  - Volume reduced to -6dB (0.5 parameter value) to prevent low-end clipping. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| R&B Syncopated Rhythm | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise placement on off-beats (e.g., 2.5 and 3.5 QN) to capture the Neo-Soul groove. |
| Pitch/Voice Leading | Python music theory logic | Dynamically calculates diatonic passing tones (minor 7ths and perfect 5ths) relative to the chord root. |
| Deep Bass Timbre | FX Chain (`ReaSynth` parameter tweaking) | Mixing Sine and Triangle waves natively produces the muffled, sub-heavy tone heard in the video without needing external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The melodic formula, the syncopated rhythm, and the deep, warm synthesis tone can be perfectly recreated using REAPER's native MIDI and ReaSynth features.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Neo Soul Project",
    track_name: str = "Neo-Soul Bass",
    bpm: int = 90,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul/R&B bassline featuring root anchors, octave jumps, and passing tones.

    Args:
        project_name: Project identifier.
        track_name: Name for the created bass track.
        bpm: Tempo in BPM.
        key: Root note (e.g., "F").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Optional 'chord_progression' list (1-indexed scale degrees).

    Returns:
        Status string describing the generated bassline track.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    # Default to the i -> v progression shown in the video (Fm -> Cm)
    chord_progression = kwargs.get("chord_progression", [1, 5])
    
    # Format key strictly
    key_formatted = key[0].upper() + key[1:].lower() if len(key) > 1 else key.upper()
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Deep Neo-Soul Tone) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth: Sine/Triangle mix for warm low end, tight release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume (-6dB)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5)   # Tuning (Center)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)   # Square (Off)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Saw (Off)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 1.0)   # Triangle (Full)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)   # Extra Sine (Full)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.01)  # Attack (Fast, punchy)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.3)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.7)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.1)   # Release (Tight for syncopation)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_qn = bars * beats_per_bar
    item_length_sec = RPR.RPR_TimeMap2_QNToTime(0, total_qn)
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Neo-Soul MIDI Pattern ===
    note_count = 0
    
    for i in range(bars):
        chord_idx = i % len(chord_progression)
        degree = chord_progression[chord_idx]
        
        # Calculate root note in scale
        degree_zero_indexed = (degree - 1) % len(scale_intervals)
        octave_offset = (degree - 1) // len(scale_intervals)
        
        # Force bass notes into Octave 1 (MIDI 24-35)
        base_midi = NOTE_MAP.get(key_formatted, 0) + 24 
        root_midi = base_midi + scale_intervals[degree_zero_indexed] + (octave_offset * 12)
        
        while root_midi >= 36:
            root_midi -= 12
        while root_midi < 24:
            root_midi += 12

        notes_to_add = []
        
        # Pattern structure per bar:
        # 1. Beat 1 (0.0): Heavy foundational root note
        notes_to_add.append((0.0, 1.5, root_midi, velocity_base))
        
        # 2. Beat 3 'and' (2.5): Syncopated octave jump
        notes_to_add.append((2.5, 0.5, root_midi + 12, int(velocity_base * 0.85)))
        
        # 3. Beat 4 'and' (3.5): Voice-leading passing tone into next bar
        if i % 2 == 0:
            passing_midi = root_midi + 10  # Minor 7th (creates tension)
        else:
            passing_midi = root_midi + 7   # Perfect 5th (solidifies harmony)
            
        notes_to_add.append((3.5, 0.5, passing_midi, int(velocity_base * 0.80)))
        
        # Insert notes into MIDI take
        for start_beat, duration_beats, pitch, vel in notes_to_add:
            start_qn = (i * beats_per_bar) + start_beat
            end_qn = start_qn + duration_beats
            
            start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} syncopated bass notes over {bars} bars at {bpm} BPM."
```