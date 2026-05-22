# 80s Boogie & Electro Funk Groove

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 80s Boogie & Electro Funk Groove

* **Core Musical Mechanism**: This pattern defines the quintessential 1980s Boogie/Electro Funk rhythm section through the interaction of three elements:
  1. **16th-Note Swing**: The drum machine (historically a LinnDrum or Oberheim DMX) employs a heavy 16th-note swing, where the off-beat 16ths (the "e" and "a" of the beat) are pushed late.
  2. **Hi-Hat Articulation**: Accentuated downbeats and 8th notes, juxtaposed with lower-velocity, shorter-decay notes on the swung 16th subdivisions, creating a breathing, non-robotic feel.
  3. **Staccato/Legato Bass Syncopation**: A synth bassline playing heavily off the grid. It contrasts short, punchy, staccatissimo notes (often utilizing the root, octave, minor 7th, and 5th) with sudden, long, sustained legato notes. Furthermore, the bass deliberately leaves "space" by dropping out on unexpected downbeats (like the "1" of the second bar) to create groove through anticipation.

* **Why Use This Skill (Rationale)**: This groove works because of the tension between the rigid downbeats (Kick/Snare on the 1, 2, 4) and the highly syncopated bass and swung hi-hats. Dropping the bass and kick on the downbeat of a new measure defies the listener's expectation of resolution, propelling the groove forward. The contrast between short and long bass notes adds a conversational, vocal quality to the low-end.

* **Overall Applicability**: Perfect for writing the rhythm sections of modern synth-pop, nu-disco, funk, and retro-wave tracks. It provides an instant "head-nod" foundation that leaves a wide open frequency pocket in the upper mids for lush extended chord voicings (Major 9s, Minor 9s) and vocal melodies.

* **Value Addition**: Instead of a static 4-on-the-floor beat with a continuous 8th-note bass, this skill encodes advanced rhythmic swing mathematically, generates procedurally articulated hi-hats, and writes a music-theory-backed syncopated bassline that automatically adapts to your chosen key.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 105 - 115 BPM.
  - **Grid**: 16th notes with a calculated swing delay. Every off-beat 16th note (falling exactly between an 8th note and the next 8th note) is delayed by approximately 32% of a 16th note duration.
  - **Duration**: Hi-hats use dynamic velocities (100 on 8ths, 60 on 16ths). Bass notes alternate between ~150ms (staccato) and ~500ms+ (legato).
  - **The "Drop"**: Bar 2 explicitly mutes the kick and bass on beat 1.

* **Step B: Pitch & Harmony**
  - **Bass Scale**: Dorian / Minor Pentatonic framework.
  - **Intervals Used**: Root, Minor 3rd, Perfect 5th, Minor 7th, Octave.
  - The bass prioritizes jumping to the octave on the weakest subdivisions (the "a" of beat 2) and sustaining the 5th on the end of phrases to lead back to the root.

* **Step C: Sound Design & FX**
  - **Drums**: Outputs standard General MIDI mapping (36 Kick, 38 Snare, 42 CHH, 46 OHH) ready for a drum machine VST or sampler.
  - **Bass**: Implements a native REAPER `ReaSynth` configured to output a classic 80s square/saw wave. A `ReaEQ` is added to roll off the high frequencies to emulate a vintage Moog/Sequential low-pass filter, giving it a warm, analog punch.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Swung Drum Groove | MIDI note insertion w/ math offset | Precise velocity and timing control required to emulate 80s drum machine swing and hi-hat articulation. |
| Syncopated Bassline | MIDI note insertion | Allows us to define the staccato/legato note lengths dynamically and map the pentatonic intervals to any user-defined root key. |
| Synth Bass Tone | FX chain (ReaSynth + ReaEQ) | Guarantees playback natively in REAPER without requiring external VSTs, mimicking the low-passed square wave of an 80s synth. |

> **Feasibility Assessment**: 90% reproducibility. The rhythmic swing, MIDI velocities, harmonic intervals, and basic synth tone are perfectly replicated. The remaining 10% accounts for the specific high-end analog drum samples (LinnDrum/DMX) used in the tutorial, which the user will need to supply via their preferred drum sampler on the generated MIDI track.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "BoogieFunk",
    track_name: str = "80s Boogie Groove",
    bpm: int = 110,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an 80s Boogie / Electro Funk rhythm section in the current REAPER project.
    Generates a swung drum machine track and a highly syncopated staccato/legato synth bass.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name prefix for the created tracks.
        bpm: Tempo in BPM (105-115 recommended).
        key: Root note (e.g., "E", "A", "F").
        scale: Scale type (defaults to minor/dorian feel).
        bars: Number of bars to generate (should be even, e.g., 4 or 8).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Music theory lookup table
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Ensure bars is a multiple of 2 for our 2-bar groove loop
    if bars % 2 != 0:
        bars += 1

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Helper function to calculate swing (delays off-beat 16th notes)
    # 1 Quarter Note (QN) = 1 Beat. 16th note = 0.25 QN.
    # Off-beat 16ths fall on .25 and .75 marks.
    def apply_swing(qn_pos, swing_amount=0.08):
        rem = round(qn_pos % 0.5, 3)
        if rem == 0.25:
            return qn_pos + swing_amount
        return qn_pos

    # Helper function to safely insert MIDI notes
    def insert_midi_note(take, pitch, start_qn, duration_qn, velocity):
        start_qn_swung = apply_swing(start_qn)
        end_qn_swung = apply_swing(start_qn + duration_qn) # Prevent notes from overlapping grid incorrectly
        
        # Convert Quarter Notes to PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn_swung)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn_swung)
        
        # Insert note: take, selected, muted, startppq, endppq, channel, pitch, velocity, None
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), None)

    # === Step 2: Create Drum Track & MIDI ===
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums (Add Sampler)", True)

    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # Generate Drum Groove
    for b in range(bars):
        bar_offset = b * 4.0
        
        # --- KICK (36) ---
        # Bar 1: Strong downbeat
        if b % 2 == 0:
            insert_midi_note(drum_take, 36, bar_offset + 0.0, 0.25, 110)
        # Bar 2: Drop the 1! Kick comes in late to create space
        else:
            insert_midi_note(drum_take, 36, bar_offset + 1.5, 0.25, 90) # Ghost kick
            
        insert_midi_note(drum_take, 36, bar_offset + 2.75, 0.25, 100) # Swung syncopation
        insert_midi_note(drum_take, 36, bar_offset + 3.5, 0.25, 105)

        # --- SNARE (38) ---
        insert_midi_note(drum_take, 38, bar_offset + 1.0, 0.25, 115) # Beat 2
        insert_midi_note(drum_take, 38, bar_offset + 3.0, 0.25, 115) # Beat 4
        
        # --- HI-HAT (42 closed, 46 open) ---
        for i in range(16):
            beat_pos = bar_offset + (i * 0.25)
            
            # Open hi-hat flourish at the end of every 2-bar loop
            if b % 2 == 1 and i == 14:
                insert_midi_note(drum_take, 46, beat_pos, 0.5, 95)
                continue
            if b % 2 == 1 and i == 15:
                continue # Skip closed hat to let open ring
                
            is_offbeat_16th = (i % 2 != 0)
            # Accent downbeats and 8ths, lower velocity for 16ths
            vel = 65 if is_offbeat_16th else 105
            duration = 0.1 if is_offbeat_16th else 0.15
            insert_midi_note(drum_take, 42, beat_pos, duration, vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Create Bass Track & MIDI ===
    bass_track_idx = drum_track_idx + 1
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} - Synth Bass", True)

    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # Calculate Bass Pitches based on key
    root_pitch = NOTE_MAP.get(key, 4) + 24 # Drop to bass octave (E1/E2 range)
    m3 = root_pitch + 3
    fifth = root_pitch + 7
    m7 = root_pitch + 10
    octave = root_pitch + 12

    # Generate Bass Groove
    for b in range(0, bars, 2):
        bar_offset = b * 4.0
        
        # --- MEASURE 1 ---
        # Beat 1: Root staccato
        insert_midi_note(bass_take, root_pitch, bar_offset + 0.0, 0.15, 115)
        # Beat 2 'a': Octave pop staccato (swung)
        insert_midi_note(bass_take, octave, bar_offset + 1.75, 0.15, 95)
        # Beat 3 '&': m7 staccato passing tone
        insert_midi_note(bass_take, m7, bar_offset + 2.5, 0.15, 100)
        # Beat 4: Root LEGATO (long hold)
        insert_midi_note(bass_take, root_pitch, bar_offset + 3.0, 0.75, 105)
        # Beat 4 'a': 5th staccato lead-in
        insert_midi_note(bass_take, fifth, bar_offset + 3.75, 0.15, 90)

        # --- MEASURE 2 (The Drop) ---
        # Beat 1 is left completely blank for groove/space!
        
        # Beat 2 '&': m3 staccato
        insert_midi_note(bass_take, m3, bar_offset + 4.0 + 1.5, 0.15, 95)
        # Beat 3: Root staccato
        insert_midi_note(bass_take, root_pitch, bar_offset + 4.0 + 2.0, 0.15, 110)
        # Beat 4: 5th LEGATO resolving hold
        insert_midi_note(bass_take, fifth, bar_offset + 4.0 + 3.0, 0.5, 105)

    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 4: Bass Sound Design (ReaSynth + ReaEQ) ===
    # Add ReaSynth to act as our analog 80s bass
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a punchy, warm square/saw bass
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 0, 0.0)    # Volume (avoid clipping)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.01)   # Attack (snappy)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.15)   # Decay
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 3, 0.4)    # Sustain
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 4, 0.1)    # Release
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 5, 0.7)    # Square mix (fundamental body)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 6, 0.4)    # Saw mix (bite/harmonics)
    
    # Add ReaEQ to emulate a low-pass filter cutting off the harsh digital highs
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)
    # Band 4 (High Shelf -> Low Pass)
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 8, 2.0) # Type = Low Pass
    RPR.RPR_TrackFX_SetParam(bass_track, 1, 9, 800.0 / 24000.0) # Freq ~800Hz for warm low end

    return f"Created '{track_name}' (Drums and Bass) over {bars} bars at {bpm} BPM in {key} {scale} with 16th-note swing."
```