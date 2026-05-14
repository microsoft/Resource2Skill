### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized MIDI Chord Programming

* **Core Musical Mechanism**: Creating structured MIDI chords and manually varying their individual velocities to remove the "robotic" feel of perfectly programmed MIDI. The tutorial highlights using the CC lane (velocity lane) to draw dynamic shapes, ensuring notes are not "maxed out" uniformly.
* **Why Use This Skill (Rationale)**: Acoustic instruments—like the Grand Piano used in the tutorial—respond drastically to velocity, changing not just volume but timbral brightness. Static, uniform velocities sound synthetic and unnatural. Varying velocities creates groove, highlights certain voices within a chord (e.g., making the top note sing louder), and mimics the physical nuance of human fingers hitting keys at slightly different strengths.
* **Overall Applicability**: Essential for any programmed acoustic instrument (keys, strings, drums) in genres ranging from pop to hip-hop to orchestral music. It acts as the foundational step for bridging the gap between "electronic sequencing" and "musical performance."
* **Value Addition**: Transforms blocky, lifeless MIDI input into a dynamic, musical performance by encoding the concept of human expression through deterministic velocity variation.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time at 120 BPM.
  - **Grid**: Chords are placed squarely on the downbeats using "Snap to Grid", occupying most of the bar but leaving a slight gap before the next chord to simulate articulation.
* **Step B: Pitch & Harmony**
  - **Key & Scale**: Parameterized (defaults to C Major).
  - **Harmony**: A standard four-bar progression (I - V - vi - IV) utilizing root position and inverted voicings generated dynamically via scale degrees.
* **Step C: Sound Design & FX**
  - **Instrument**: Grand Piano VST. (We will substitute this with REAPER's stock `ReaSynth` to ensure the script executes safely without third-party dependencies).
* **Step D: Mix & Automation**
  - **Velocity Automation**: Instead of static velocities (e.g., all 127), a patterned offset is applied to each note to emulate the manual CC lane adjustments shown in the tutorial.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides precise, programmatic control over individual note pitch, timing, and velocity. |
| Humanized Dynamics | Mathematical velocity offset | Reproduces the tutorial's manual CC lane adjustments deterministically. |
| Instrument Sound | FX chain (`ReaSynth`) | Provides a guaranteed, self-contained stock sound source so the MIDI notes can be heard. |

> **Feasibility Assessment**: 90% — The specific third-party "Grand Piano" VST cannot be guaranteed on every user's machine and is substituted with ReaSynth. However, the core skill—MIDI grid placement, chord theory generation, and velocity humanization—is 100% faithfully reproduced.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create Humanized MIDI Chord Programming in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity before humanization offsets (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument ===
    # Using stock ReaSynth as a placeholder for the piano VST to guarantee execution
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    start_time = 0.0
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Music Theory & Note Logic ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Define a standard I - V - vi - IV progression using scale degrees (0-indexed)
    progression_degrees = [
        [0, 2, 4], # I
        [4, 6, 8], # V  (Note: 8 wraps to the 2nd degree of the next octave)
        [5, 7, 9], # vi
        [3, 5, 7]  # IV
    ]
    
    scale_intervals = SCALES.get(scale, SCALES["major"])
    root_val = NOTE_MAP.get(key, 0)
    octave_base = 48 # Start around C3

    def get_midi_pitch(degree):
        """Converts a scale degree into an absolute MIDI pitch."""
        octave_offset = degree // 7
        scale_degree = degree % 7
        return octave_base + root_val + scale_intervals[scale_degree] + (octave_offset * 12)

    # Deterministic array of velocity offsets to simulate the manual CC lane humanization shown in tutorial
    velocity_offsets = [12, -8, 4, -15, 6, -2, 10, -5]
    notes_created = 0

    # === Step 6: Insert Notes ===
    for bar in range(bars):
        chord_idx = bar % len(progression_degrees)
        chord = progression_degrees[chord_idx]
        
        # Calculate timing in Quarter Notes (QN)
        start_qn = bar * beats_per_bar
        # End slightly early (0.15 QN gap) so chords don't bleed into each other
        end_qn = start_qn + beats_per_bar - 0.15 
        
        # Convert QN to Pulses Per Quarter Note (PPQ) for accurate grid placement
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        for degree in chord:
            pitch = get_midi_pitch(degree)
            
            # Apply deterministic velocity humanization
            offset = velocity_offsets[notes_created % len(velocity_offsets)]
            humanized_velocity = velocity_base + offset
            
            # Clamp velocity between valid MIDI bounds (1-127)
            humanized_velocity = max(1, min(127, int(humanized_velocity)))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, humanized_velocity, False)
            notes_created += 1

    # Finalize MIDI editing state
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized notes over {bars} bars at {bpm} BPM in {key} {scale}."
```