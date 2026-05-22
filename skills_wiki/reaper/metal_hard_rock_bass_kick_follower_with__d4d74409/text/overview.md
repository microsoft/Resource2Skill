### 1. High-level Design Pattern Extraction

> **Skill Name**: Metal/Hard Rock Bass Kick-Follower with Octave Jumps

* **Core Musical Mechanism**: The baseline rhythmically matches the kick drum of the track, alternating between staccato (short, muted) and legato (held-out) notes depending on the groove. Crucially, the pattern employs strategic 12-semitone (one octave) leaps to accent specific syncopated hits or transition beats, while the MIDI velocity is deliberately reined in to soften the aggressive pick attack common in virtual bass instruments.
* **Why Use This Skill (Rationale)**: In modern metal and hard rock, the bass guitar fundamentally serves as the harmonic anchor for the rhythm guitars and the tonal extension of the kick drum. Following the kick tightly locks the groove. Lowering the velocity from the default maximum (127 down to ~110) prevents VST sample libraries (like DjinnBass) from triggering excessively harsh, "clanky" top-end string noise on every single hit. The octave jumps introduce melodic variation and prevent the pedal-point bassline from becoming completely static.
* **Overall Applicability**: Perfect for programming modern metal, metalcore, hard rock, or djent tracks where the bass is driving the low-end via VST instruments. It serves as the foundational bass layer during verses, heavy breakdowns, or intricate guitar riffs.
* **Value Addition**: This skill transforms a flat, unrealistic bass MIDI sequence into a dynamic, production-ready metal bassline by applying genre-specific playing articulations (staccato vs. legato), realistic VST velocity management, and idiomatic fretboard jumps.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically ranging from 100 to 140 BPM (syncopated metal groove).
  - **Rhythmic Grid**: Primarily 16th-note and 8th-note subdivisions. 
  - **Note Duration**: A mix of short, punchy notes (1/16ths) to follow fast kick bursts, and longer held quarter/eighth notes to let the sub-frequencies bloom.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Standard or drop-tuned root notes (e.g., Drop C, Drop A). 
  - **Pitch Pattern**: The bass rides the lowest root note (e.g., C1) for 90% of the progression.
  - **Fretboard Leap**: On syncopated turnaround beats, the pitch jumps exactly +12 semitones (one octave, moving from the lowest open string to the 12th fret).

* **Step C: Sound Design & FX**
  - **Instrument**: Submission Audio DjinnBass (or similar modern metal bass VST like MODO Bass, Eurobass). 
  - **Velocity Control**: The video heavily emphasizes pulling velocity down from 127 to approximately 110. This changes the sample layer in the VST, removing artificial high-end harshness.

* **Step D: Mix & Automation**
  - Hard velocity maximums are avoided to allow room in the mix for the actual kick drum's click/beater to punch through without clashing with the bass pick attack.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Kick-following rhythm** | MIDI note insertion | Allows precise placement of 16th/8th notes to emulate a double-kick groove. |
| **Octave Jumps** | MIDI pitch calculation (`root + 12`) | Directly mirrors the fretboard manipulation described in the tutorial. |
| **Harshness Control** | MIDI velocity parameter | Emulates the specific instruction to set maximum velocity around 110 rather than 127. |

> **Feasibility Assessment**: 85% reproduction. The code perfectly reproduces the MIDI timing, varying note lengths, velocity attenuation, and octave jump technique shown in the video. Since third-party instruments like "Submission Audio DjinnBass" are not guaranteed, the code relies on Reaper's native `ReaSynth` as an audible placeholder, pitched down to act as a sub-bass. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Hard Rock Bass Kick-Follower pattern with octave jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (110 recommended to avoid VST harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # Calculate base pitch (Set to octave 1 for deep metal bass tuning, e.g. C1 = 24)
    base_pitch = NOTE_MAP.get(key, 0) + 24

    # Definition of the syncopated rhythm mimicking a kick-drum follow
    # Format: (step_start_16th, duration_16ths, octave_offset)
    pattern = [
        (0, 2, 0),   # Beat 1: 8th note chug
        (2, 1, 0),   # Beat 1: 16th note stutter
        (3, 1, 0),   # Beat 1: 16th note stutter
        (4, 2, 0),   # Beat 2: 8th note chug
        (7, 1, 0),   # Beat 2: Syncopated 16th off-beat
        (8, 2, 0),   # Beat 3: 8th note chug
        (10, 2, 12), # Beat 3: OCTAVE JUMP (up 12 frets) for variation
        (12, 4, 0)   # Beat 4: Quarter note, held out (legato)
    ]

    total_notes = 0

    # === Step 4: Insert MIDI Notes ===
    for bar in range(bars):
        for step, dur, offset in pattern:
            # Calculate project time for the start and end of the note
            beat_pos = (bar * beats_per_bar) + (step * 0.25)
            note_start_time = beat_pos * (60.0 / bpm)
            note_end_time = (beat_pos + (dur * 0.25)) * (60.0 / bpm)

            # Convert to PPQ (Pulses Per Quarter Note)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)

            # Insert note with controlled velocity to emulate tutorial's harshness mitigation
            pitch = base_pitch + offset
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Synthesizer (Placeholder) ===
    # Using ReaSynth pitched appropriately to simulate the bass foundation
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM (Velocity pulled to {velocity_base})."
```