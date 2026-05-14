# Bossa Nova Rhythm & Bass Groove

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Bossa Nova Rhythm & Bass Groove

* **Core Musical Mechanism**: The defining characteristic of this pattern is the polyrhythmic interplay between a steady, syncopated drum groove and an anchoring root-fifth bassline. The foundation relies on a 2-bar "Bossa Clave" played on a rimshot or actual claves (a 3-2 rhythm), layered over straight 8th-note hi-hats and a kick drum that anticipates beats 3 and 1. The bass rigidly locks into the kick drum's rhythm, oscillating between the root note and the perfect fifth. 
* **Why Use This Skill (Rationale)**: Bossa Nova grooves are fundamentally built on *syncopation* and *tension/release* against a rigid grid. The "anticipation" of the downbeat (the kick and bass playing on the "and" of 2, and the "and" of 4) creates a forward-pulling, relaxed momentum. Humanization (varying velocities and not strictly hard-quantizing) is critical so the loop feels laid-back rather than robotic. 
* **Overall Applicability**: This arrangement is perfect for relaxing chill-out, lo-fi hip-hop, ambient pop, or jazz-fusion tracks. It serves as an excellent rhythmic bed when you need movement without aggressive energy. 
* **Value Addition**: This skill encodes the specific, often misunderstood 3-2 Bossa Clave timing and perfectly pairs it with the correct syncopated root-fifth bass movement, replacing the trial-and-error of programming authentic Brazilian syncopation.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: Typically 70-90 BPM (Default: 80 BPM). 
  - **Grid Divisions**: Straight 8th notes (no swing/shuffle).
  - **Pattern Length**: 2 bars (repeating).
  - **Rhythmic Signatures**:
    - **Kick**: Plays on beat 1, the "and" of 2, beat 3, and the "and" of 4.
    - **Hi-hat**: Plays straight 8th notes.
    - **Clave/Rimshot (3-2 Pattern)**: 
      - Bar 1: Beat 1, the "and" of 2, beat 4.
      - Bar 2: The "and" of 1, beat 3.

* **Step B: Pitch & Harmony**
  - **Drums**: General MIDI mapping — Kick (36), Rimshot/Clave (37), Closed Hi-hat (42).
  - **Bass**: Locks strictly to the kick drum rhythm.
    - Beats 1 & 2&: Root Note (e.g., C2).
    - Beats 3 & 4&: Perfect Fifth (e.g., G2, exactly 7 semitones above the root).

* **Step C: Sound Design & FX**
  - **Drums**: A dry, acoustic drum kit works best. The snare must be a rimshot or replaced with a wooden clave. 
  - **Bass**: An acoustic upright bass, or a deep, filtered sine/triangle wave synth bass. 
  - **Humanization**: Velocities emphasize the downbeats. The off-beat 8th notes are played significantly softer to create a natural, swaying dynamic.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bossa Clave & Drum Groove | MIDI note insertion | Requires exact control over the 2-bar syncopated rhythm and velocity humanization. |
| Bassline Harmony | MIDI note insertion | Computes the Root and perfect 5th dynamically based on the requested musical key. |
| Bass Instrument | FX chain (ReaSynth) | Provides a standalone, audible sub-bass without relying on external VST sample libraries. |

> **Feasibility Assessment**: 100% reproducible. The script precisely encodes the 2-bar drum clave, the root-fifth bassline locking to the kick syncopation, and adds velocity variations to simulate the humanized feel emphasized in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bossa Groove",
    bpm: int = 80,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a traditional Bossa Nova drum and bass groove in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (70-90 recommended).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (should be even, as the clave is a 2-bar loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Bass pitches (Root and Perfect 5th)
    root_pitch = NOTE_MAP.get(key.capitalize(), 0) + 36  # Octave 2
    fifth_pitch = root_pitch + 7 # Perfect 5th

    # Ensure bars is an even number to complete the 2-bar clave cycle
    if bars % 2 != 0:
        bars += 1

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Helper function to insert MIDI ===
    def insert_note(take, item_pos, pitch, start_beat, length_beats, velocity):
        sec_per_beat = 60.0 / bpm
        start_sec = start_beat * sec_per_beat
        end_sec = (start_beat + length_beats) * sec_per_beat
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_pos + start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_pos + end_sec)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    # === Step 2: Create Drums Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} Drums", True)

    # Create Drum MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)

    # === Step 3: Create Bass Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    bass_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} Bass", True)

    # Add ReaSynth for an immediate audible deep bass tone
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    # === Step 4: Generate MIDI Patterns ===
    for b in range(bars):
        bar_offset = b * beats_per_bar
        
        # 1. Straight 8th-note Hi-hats (Note 42)
        # Humanized: Downbeats are louder, upbeats are softer
        for i in range(8):
            beat_pos = bar_offset + (i * 0.5)
            hh_vel = velocity_base if i % 2 == 0 else velocity_base - 25
            insert_note(drum_take, 0.0, 42, beat_pos, 0.25, hh_vel)

        # 2. Syncopated Kick Drum (Note 36)
        # Plays on 1, 2&, 3, 4&
        insert_note(drum_take, 0.0, 36, bar_offset + 0.0, 0.5, velocity_base + 10)
        insert_note(drum_take, 0.0, 36, bar_offset + 1.5, 0.5, velocity_base - 10)
        insert_note(drum_take, 0.0, 36, bar_offset + 2.0, 0.5, velocity_base + 10)
        insert_note(drum_take, 0.0, 36, bar_offset + 3.5, 0.5, velocity_base - 10)

        # 3. Clave / Rimshot (Note 37) -> 3-2 Bossa Clave Pattern over 2 bars
        if b % 2 == 0:
            # Bar 1: Beats 1, 2&, 4
            insert_note(drum_take, 0.0, 37, bar_offset + 0.0, 0.5, velocity_base)
            insert_note(drum_take, 0.0, 37, bar_offset + 1.5, 0.5, velocity_base - 5)
            insert_note(drum_take, 0.0, 37, bar_offset + 3.0, 0.5, velocity_base + 5)
        else:
            # Bar 2: Beats 1&, 3
            insert_note(drum_take, 0.0, 37, bar_offset + 0.5, 0.5, velocity_base - 5)
            insert_note(drum_take, 0.0, 37, bar_offset + 2.0, 0.5, velocity_base + 10)

        # 4. Bass Line -> Locks exactly to the Kick rhythm, oscillating 1 and 5
        # Note lengths are humanized (longer on downbeats, staccato on syncopated upbeats)
        insert_note(bass_take, 0.0, root_pitch, bar_offset + 0.0, 1.4, velocity_base)
        insert_note(bass_take, 0.0, root_pitch, bar_offset + 1.5, 0.4, velocity_base - 15)
        insert_note(bass_take, 0.0, fifth_pitch, bar_offset + 2.0, 1.4, velocity_base)
        insert_note(bass_take, 0.0, fifth_pitch, bar_offset + 3.5, 0.4, velocity_base - 15)

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(drum_take)
    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created '{track_name}' (Drums and Bass) over {bars} bars at {bpm} BPM in {key}."
```