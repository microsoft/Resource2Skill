### 1. High-level Design Pattern Extraction

> **Skill Name**: Kick-Locked Metal Bass Line

* **Core Musical Mechanism**: In modern metal, djent, and hard rock, the bass guitar's primary rhythmic function is to strictly follow (or "lock into") the kick drum pattern. Pitch-wise, it acts as a pedal point—matching the lowest note of the rhythm guitar (often an open string like Drop C or Drop A). To add variation and mimic the physical movement on a bass fretboard, the pattern occasionally jumps up an octave (representing a jump to the 12th fret) during turnaround fills.
* **Why Use This Skill (Rationale)**: Locking the bass MIDI precisely to the kick drum rhythm creates a massive, unified low-end block. If the bass and kick are playing different syncopations, the low end becomes muddy and loses impact. Additionally, lowering the base MIDI velocity slightly (from 127 down to ~110) prevents virtual bass instruments (like DjinnBass, Eurobass) from triggering harsh, unnatural "fret buzz" round-robins on every single hit.
* **Overall Applicability**: This pattern is essential for metalcore, djent, hard rock, and any genre relying heavily on aggressive, syncopated guitar riffs paired with double-kick drumming.
* **Value Addition**: Compared to a basic quantized bassline, this skill encodes the specific syncopated rhythm matrix of a metal groove, applies the realistic staccato note lengths required for aggressive picking, handles the octave-jump articulation, and optimizes the MIDI velocity for amp-sim VSTs.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 16th notes.
  - **Pattern**: A highly syncopated 16th-note sequence mapping directly to a typical double-kick drum groove. 
  - **Duration**: Staccato notes (e.g., ~0.15 beats) so the virtual string mutes properly between rapid hits, creating "chug" separation.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Defined by the root note of the track (acts as a pedal point).
  - **Voicing**: Single notes in the lowest possible register (typically MIDI note 24 to 36, corresponding to C1-C2).
  - **Movement**: The sequence mostly repeats the root note, with specific +12 semitone jumps to mimic popping/accenting the 12th fret, a staple move in modern metal bass parts.
* **Step C: Sound Design & FX**
  - **Velocity**: Capped at ~110. The tutorial explicitly emphasizes bringing default 127 velocities down to ~110 to remove the top-end harshness inherent to maximum-velocity multi-sampled bass VSTs.
* **Step D: Mix & Automation**
  - Generally routed to a bass amp sim or split into a low-passed sub bus and a distorted top bus (omitted in this MIDI-generation script to maintain broad compatibility).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Kick-locked Rhythm | MIDI note insertion on 16th grid | Allows precise, programmed syncopation matching a drum layout. |
| Pitch & Octave Jumps | MIDI `pitch` manipulation | Dynamically computes the lowest bass string pitch and +12 semitone jumps based on the key parameter. |
| Reduced Top-End Harshness | Velocity parameter reduction | The tutorial explicitly lowers the velocity parameter from 127 to 110 inside the MIDI editor to sweeten the tone. |

> **Feasibility Assessment**: 100% reproducible for the MIDI sequence. The exact bass tone requires an external virtual instrument (like DjinnBass), so the code sets up the perfect, mix-ready MIDI sequence on a new track waiting for the user's preferred VST to be loaded. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Lowered from 127 as specified in the tutorial to tame string harshness
    **kwargs,
) -> str:
    """
    Create a Kick-Locked Metal Bass Line in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), optimized to 110 for virtual bass.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Note map parsing for calculating the lowest root pedal point
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Establish root pitch class. Metal bass is usually in Octave 1 (MIDI 24 for C1)
    root_pitch_class = NOTE_MAP.get(key.capitalize(), 0)
    base_pitch = 24 + root_pitch_class 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track Additively ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Place item at current edit cursor
    pos = RPR.RPR_GetCursorPosition()
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", pos)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 4: Insert Syncopated MIDI Notes ===
    # Rhythm Matrix (16th notes): 
    # 1 = Root hit (Follows Kick)
    # 2 = Octave jump (+12st) on turnaround (12th fret mimic)
    # 0 = Rest
    rhythm_16ths = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 2, 0, 1, 0]
    
    note_count = 0
    
    for bar in range(bars):
        for i, hit_type in enumerate(rhythm_16ths):
            if hit_type != 0:
                # Calculate timing in beats relative to start
                beat_offset = (bar * beats_per_bar) + (i * 0.25)
                proj_start = pos + (beat_offset * 60.0 / bpm)
                
                # Use a staccato note length (0.15 beats instead of full 0.25) to allow for string muting
                note_len_beats = 0.15
                proj_end = proj_start + (note_len_beats * 60.0 / bpm)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_start)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, proj_end)
                
                # Determine pitch
                pitch = base_pitch
                if hit_type == 2:
                    pitch += 12  # Jump an octave up
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, velocity_base, False
                )
                note_count += 1

    # Sort MIDI events to finalize the item
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} syncopated notes over {bars} bars at {bpm} BPM. Note: Add your preferred Bass VST to this track."
```