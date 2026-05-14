### 1. High-level Design Pattern Extraction

> **Skill Name**: Kick-Locked Modern Rock/Metal Bass Programming

* **Core Musical Mechanism**: The foundation of modern rock, metal, and djent bass programming relies on locking the bass guitar's rhythm identically to the kick drum pattern. To prevent the sampled bass from sounding unnatural or "machine-gun-like," the MIDI velocity is purposefully reduced from maximum (127) to around 110. Finally, rhythmic repetition is broken up by jumping up a full octave (simulating a jump to the 12th fret on a bass guitar) during turnarounds or syncopated off-beats.
* **Why Use This Skill (Rationale)**: 
  * *Groove Theory*: In heavy guitar music, the kick drum and the bass guitar act as a single hybrid instrument. Locking their attacks creates a massive, unified low-end transient.
  * *Timbral Realism*: Sampled bass libraries (like DjinnBass or Eurobass) map maximum velocities (120-127) to aggressive, string-clacking "pop" articulations. While occasionally useful, leaving all notes at 127 creates overwhelming high-frequency harshness. Dropping the velocity to ~110 hits the "hard picking" articulation without triggering the harsh fret-clack.
  * *Variation*: Octave jumps provide melodic interest without disrupting the harmonic foundation (the root note), keeping the low-end anchored while moving the bass into a more audible mid-range frequency pocket momentarily.
* **Overall Applicability**: Essential for producing modern metal, metalcore, pop-punk, hard rock, and djent. It also serves as a fantastic baseline technique for programming synth basses in EDM and synthwave where the bass must duck or lock with the kick.
* **Value Addition**: Transforms a static, lifeless MIDI bass drone into a driving, aggressive groove that perfectly glues the drum kit to the rhythm guitars, while automatically applying velocity-based humanization/tone-taming.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo Range**: Typically 100 - 160 BPM.
  * **Rhythm Grid**: Mix of 1/8th notes and syncopated 1/16th notes.
  * **Note Duration**: Staccato notes (16th to 8th note lengths) with precise cutoffs to leave room for the snare drum and create "chug" pockets.
* **Step B: Pitch & Harmony**
  * **Key/Scale**: Rides the absolute root note of the scale (often down-tuned, e.g., Drop C -> C1 or C2).
  * **Voicings**: Single notes only.
  * **Variation**: The 12th-fret octave jump (+12 semitones) placed at the end of a phrase (e.g., the 'AND' of beat 4) to lead into the next measure.
* **Step C: Sound Design & FX**
  * **Instrument**: Typically a multi-sampled bass VSTi (DjinnBass, Submission Audio). For the stock reproduction, ReaSynth is used.
  * **Tone control**: The tone is primarily controlled *at the MIDI level* via the 110 velocity cap.
* **Step D: Mix & Automation**
  * Consistent, hard-hitting velocities (no soft ghost notes, just a flat ~110 for every hit) to emulate heavy pick attack.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Lock to Kick Rhythm | MIDI note insertion | Allows for exact replication of a syncopated rock drum groove timing. |
| Tone & Harshness Control | MIDI Velocity limit | The video explicitly solves "top end harshness" by capping MIDI velocity at 110. |
| Fretboard Jumps | MIDI Pitch calculation (+12) | Accurately simulates the player moving from the open string to the 12th fret. |

> **Feasibility Assessment**: 85% reproduction. The rhythmic placement, velocity trick, and octave variation are replicated perfectly. The remaining 15% relies on having a premium third-party bass library (like DjinnBass) installed, which we substitute with REAPER's native ReaSynth for guaranteed out-of-the-box execution. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a kick-locked, modern rock/metal bass MIDI pattern in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (mostly rides the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (110 removes harsh clack from bass VSTs).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Note map starting at octave 1 (common for modern metal/drop tunings)
    NOTE_MAP = {
        "C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
        "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
        "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35
    }
    
    root_note = NOTE_MAP.get(key.upper(), 24) # Default to C1

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_duration = 60.0 / bpm
    bar_length_sec = qn_duration * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Simulated modern metal Kick/Djent rhythm mapped relative to a 4-beat bar.
    # Format: (start_beat, end_beat, octave_offset)
    rhythm_pattern = [
        (0.0, 0.5, 0),    # Beat 1 (Downbeat)
        (0.75, 1.0, 0),   # Syncopated 16th before Beat 2
        (1.5, 2.0, 0),    # The 'AND' of Beat 2
        (2.5, 2.75, 0),   # The 'AND' of Beat 3
        (3.0, 3.25, 0),   # Beat 4 Downbeat
        (3.5, 4.0, 1),    # The 'AND' of Beat 4 -> 12th Fret Octave Jump (+1)
    ]

    # === Step 4: Insert MIDI Notes ===
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for hit in rhythm_pattern:
            start_time = (bar_start_beat + hit[0]) * qn_duration
            end_time = (bar_start_beat + hit[1]) * qn_duration
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Apply octave variation (simulating moving to the 12th fret)
            pitch = root_note + (hit[2] * 12)
            
            # Video core lesson: 110 velocity to remove sample harshness
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Placeholder FX ===
    # Adds ReaSynth to ensure the track makes sound out of the box. 
    # In a real scenario, the user would swap this for DjinnBass/Eurobass.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM. Velocity capped at {velocity_base} to prevent sample harshness."
```