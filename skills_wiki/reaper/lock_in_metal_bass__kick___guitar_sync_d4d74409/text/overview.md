### 1. High-level Design Pattern Extraction

> **Skill Name**: Lock-In Metal Bass (Kick & Guitar Sync)

* **Core Musical Mechanism**: The defining characteristic of modern rock and metal bass programming is strict rhythmic alignment with the kick drum and the rhythm guitar's lowest string. The bass plays a pedal tone (usually the root note of the key) exactly when the kick hits. Long, sustained notes are used for heavy downbeats, while fast, staccato 16th notes are used for double-kick bursts. Octave jumps (+12 semitones) are strategically placed to match guitar flourishes or emphasize snare hits.
* **Why Use This Skill (Rationale)**: By locking the bass rhythm perfectly to the kick drum, you create a massive, unified low-end pulse. The kick provides the transient impact, while the bass provides the sustained tonal weight. Dropping the MIDI velocity slightly below maximum (e.g., from 127 to 110) prevents the virtual instrument from triggering overly harsh, artificial "pick attack" samples on every single note, resulting in a smoother, more realistic low end.
* **Overall Applicability**: This technique is foundational for Metalcore, Djent, Hard Rock, and Pop-Punk production, where the bass guitar acts more as a low-frequency extension of the rhythm guitar than an independent melodic voice.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes the rhythmic phrasing of a modern metal breakdown. It demonstrates how to combine legato downbeats with staccato 16th-note syncopation, octave jumps for variation, and humanized velocity scaling.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically anywhere from 100 to 160 BPM (the generated pattern defaults to 120 BPM for a standard mid-tempo groove).
  - **Rhythmic Grid**: A mix of 1/4 notes, 1/8 notes, and 1/16 notes.
  - **Durations**: Employs alternating staccato (choked) and legato (sustained) notes depending on the speed of the hits.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Root note pedal point (e.g., Drop C, C1/C2). 
  - **Voicings**: Single notes only. The pattern relies on moving between the fundamental root note and its perfect octave (+12 semitones) to simulate a bass player jumping from the open string to the 12th fret.
* **Step C: Sound Design & FX**
  - **Instrument**: While the tutorial uses DjinnBass (a specialized Kontakt/sampler library), this script builds a stock-plugin alternative using `ReaSynth` configured for a gritty, sub-heavy square/saw blend to emulate a distorted metal bass tone. 
  - **FX Chain**: `ReaSynth` for tone generation, followed by `ReaEQ` to shape the low end and tame harsh high frequencies.
* **Step D: Mix & Automation**
  - Velocity control is crucial here: the base velocity is capped around 110 (out of 127) to avoid the "machine gun" effect of max-velocity pick attacks.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic pattern | `RPR_MIDI_InsertNote` | Provides precise control over exact start times, staccato durations, and velocity variations. |
| Octave jumps | MIDI pitch manipulation | Computes the +12 semitone shift dynamically based on the input key. |
| Instrument Tone | `ReaSynth` + `ReaEQ` | Creates a self-contained, reproducible distorted bass tone using stock plugins, ensuring the script runs without requiring third-party libraries like DjinnBass. |

> **Feasibility Assessment**: 85% reproduction. The rhythmic theory, MIDI layout, octave jumps, and velocity tweaks perfectly match the tutorial's methodology. The only missing 15% is the hyper-realistic multi-sampled bass VST tone (DjinnBass), which is approximated here using ReaSynth.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lock-In Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create 'Lock-In Metal Bass' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Drops to octave 2 for bass.
        scale: Scale type (used for root note reference).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127). Set slightly below 127 to avoid harsh attacks.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root MIDI pitch for a bass (Octave 2)
    root_pitch = 24 + NOTE_MAP.get(key.capitalize(), 0) # e.g., C = 24 (C1)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    qn_len = 60.0 / bpm
    bar_length_sec = qn_len * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Define the "Kick Following" rhythm pattern for 1 bar (in quarter notes / beats)
    # Format: (start_beat, length_beats, pitch_offset, velocity_modifier)
    rhythm_pattern = [
        (0.0,  1.0,   0,  1.0),   # Beat 1: Legato quarter note
        (1.0,  0.5,   0,  0.95),  # Beat 2: Staccato 8th
        (1.5,  0.5,   0,  0.95),  # Beat 2&: Staccato 8th
        (2.0,  0.25,  0,  0.9),   # Beat 3: 16th burst
        (2.25, 0.25,  0,  0.9),   # Beat 3e: 16th burst
        (2.5,  0.25,  0,  0.9),   # Beat 3&: 16th burst
        (2.75, 0.25,  0,  0.9),   # Beat 3a: 16th burst
        (3.0,  0.5,   0,  1.0),   # Beat 4: Staccato 8th
        (3.5,  0.5,  12,  1.05)   # Beat 4&: Octave jump (+12 semitones) accent
    ]

    # Insert MIDI notes
    total_notes_created = 0
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        
        for note_def in rhythm_pattern:
            start_beat, length_beats, pitch_offset, vel_mod = note_def
            
            # Convert beats to time
            start_time = bar_start_time + (start_beat * qn_len)
            # Create a slight gap for staccato articulation unless it's the full quarter note
            actual_length = (length_beats * qn_len) * (0.85 if length_beats < 1.0 else 0.95)
            end_time = start_time + actual_length
            
            # Convert time to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = root_pitch + pitch_offset
            vel = int(min(127, max(1, velocity_base * vel_mod)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain for Bass Tone ===
    # 1. ReaSynth to generate the tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a gritty square/saw bass tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 1.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.8)    # Square mix (adds grit)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.5)    # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 10.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 100.0)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.8)    # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 50.0)   # Release
    
    # 2. ReaEQ to roll off harsh highs and boost the sub
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Band 1: Sub boost
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0)         # Type: Low Shelf
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 80.0)      # Freq: 80 Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 2, 3.0)       # Gain: +3 dB
    
    # Band 4: High Cut (to simulate a bass cab and hide ReaSynth's digital high-end)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 9, 2)         # Type: High Cut
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, 4000.0)   # Freq: 4000 Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 11, -12.0)    # Gain down

    return f"Created '{track_name}' with {total_notes_created} notes over {bars} bars at {bpm} BPM in Drop {key}"
```