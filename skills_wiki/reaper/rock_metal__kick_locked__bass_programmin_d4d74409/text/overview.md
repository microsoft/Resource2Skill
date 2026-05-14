### 1. High-level Design Pattern Extraction

> **Skill Name**: Rock/Metal "Kick-Locked" Bass Programming

* **Core Musical Mechanism**: The defining characteristic of this pattern is rhythmically locking the bass MIDI notes exactly to the syncopated hits of the kick drum. The bass primarily rides the root note (pedal point) in the lowest register to act as an anchor, and uses strategic +12 semitone (octave) jumps or follows the guitar's melodic fills to introduce variation. Note velocities are intentionally clamped slightly below maximum (e.g., 110 instead of 127) to avoid triggering the harshest, most "clanky" sample layers on every single hit.
* **Why Use This Skill (Rationale)**: In heavy music genres, the bass guitar's primary function is to glue the drum kit to the rhythm guitars. Locking the bass rhythmically to the kick drum creates a massive, unified low-end pulse (often referred to as the "machine gun" effect in metalcore or djent). Backing off the velocity to ~110 prevents dynamic fatigue and allows the top-end of the bass to sit better in the mix, leaving the absolute maximum velocities only for the hardest accents. Octave jumps (simulating jumping to the 12th fret on the lowest string) add immediate rhythmic bounce and ear candy without cluttering the harmonic progression.
* **Overall Applicability**: Essential for hard rock, metalcore, djent, punk, and any heavy genre where the bass needs to support an aggressive rhythm section.
* **Value Addition**: This skill transforms a static bass sequence into a dynamic, genre-appropriate groove by encoding specific genre rules: syncopated staccato durations, kick-locking, velocity management for sample-based VSTs, and idiomatic fretboard jumps.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/8th and 1/16th note syncopations simulating a double-kick drum pattern.
  - **Durations**: A mix of tight, staccato 16th notes (chugs) and slightly longer 8th notes to let the bass ring out on downbeats.
  - **Velocity**: Capped at 110 (out of 127) to maintain punch while reducing top-end sample harshness.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Root note pedal point (e.g., Drop C, so C1 or C2 depending on the octave mapping).
  - **Movement**: Primarily static on the root note. Variation is introduced via +12 semitone (octave) leaps, mimicking a common metal bass trope of jumping from the open string to the 12th fret.

* **Step C: Sound Design & FX**
  - **Instrument**: A multi-sampled Bass VST (Submission Audio DjinnBass, Moto Bass, etc.). *For the REAPER reproduction, we will synthesize a heavy bass using ReaSynth with a mix of saw/square waves and a low-pass filter.*
  - **Processing**: High compression, slight distortion/saturation to make it cut through the mix.

* **Step D: Mix & Automation**
  - Consistent volume, heavily compressed to maintain an even low-end floor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| "Following the kick" rhythm | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise placement of staccato and legato syncopations to emulate a metal kick pattern. |
| "Velocity at 110" | MIDI note velocity | Matches the tutorial's exact instruction to pull back from 127 to tame the sample harshness. |
| "12th Fret / Octave jumps" | Pitch manipulation (+12 semitones) | Emulates the fretboard jump demonstrated in the video for variation. |
| Bass Tone | FX chain (ReaSynth + ReaComp) | Provides a thick, stock-plugin stand-in for the third-party bass VSTs mentioned in the tutorial. |

> **Feasibility Assessment**: 90% — The precise rhythmic concept, velocity control, and octave-jump variations are reproduced perfectly. The exact timbre of DjinnBass cannot be replicated with stock REAPER synths, but the provided ReaSynth/ReaComp chain provides a functional placeholder that demonstrates the heavy bass concept.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "HeavyProject",
    track_name: str = "Kick-Locked Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Specifically lowered from 127 per tutorial
    **kwargs,
) -> str:
    """
    Create a Rock/Metal Kick-Locked Bass pattern in the current REAPER project.
    """
    import reaper_python as RPR
    
    # === Step 1: Initialize Theory & Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Root note mapped to the 2nd octave (e.g., Drop C tuning equivalent range)
    root_midi = 36 + NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Add FX Chain for Heavy Bass (Stock Placeholder) ===
    # Add a synth to act as the bass
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Volume (lower to avoid clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.5)    # Square mix (adds grit)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.5)    # Saw mix (adds bite)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 0.1)    # Attack tight
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, 0.1)    # Decay short for chugs
    
    # Add compression to flatten the dynamic range (essential for modern metal bass)
    fx_comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 0, -20.0)   # Threshold
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 1, 8.0)     # Ratio 8:1
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 2, 2.0)     # Attack 2ms
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 3, 50.0)    # Release 50ms
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Enable MIDI item to accept inserted notes
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 5: Define Rhythmic Pattern & Insert Notes ===
    # A typical metalcore syncopated "kick" pattern (positions in beats)
    # Format: (beat_position, duration_in_beats, is_octave_jump)
    base_pattern = [
        (0.0,  0.25, False), # Chug
        (0.5,  0.25, False), # Chug
        (1.25, 0.25, False), # Syncopated hit
        (1.5,  0.25, False), # Syncopated hit
        (2.0,  0.50, False), # Held note (let ring)
        (2.75, 0.25, False), # Pickup
        (3.0,  0.25, False), # Hit
        (3.5,  0.25, False)  # Hit
    ]
    
    # Define an alternate bar with the "12th fret" octave jump variation mentioned in tutorial
    fill_pattern = [
        (0.0,  0.25, False), 
        (0.5,  0.25, False), 
        (1.25, 0.25, False), 
        (1.5,  0.25, False), 
        (2.0,  0.50, False), 
        (3.0,  0.25, True),  # OCTAVE JUMP!
        (3.5,  0.25, True)   # OCTAVE JUMP!
    ]

    total_notes = 0
    
    # Generate notes across all requested bars
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        # Use fill pattern on every 2nd bar (e.g., bar index 1, 3, 5)
        current_pattern = fill_pattern if (bar % 2 == 1) else base_pattern
        
        for pos_beats, dur_beats, octave_jump in current_pattern:
            # Calculate absolute time in seconds
            note_start_sec = bar_start_time + (pos_beats * (60.0 / bpm))
            note_end_sec = note_start_sec + (dur_beats * (60.0 / bpm))
            
            # Convert time to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
            
            # Pitch logic: Root note, or Root + 12 for octave jumps
            pitch = root_midi + 12 if octave_jump else root_midi
            
            # Add note (not sorted immediately for performance)
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), int(velocity_base), True
            )
            total_notes += 1

    # Finalize MIDI by sorting the inserted notes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes} kick-locked notes (velocity {velocity_base}) over {bars} bars at {bpm} BPM in {key}."
```