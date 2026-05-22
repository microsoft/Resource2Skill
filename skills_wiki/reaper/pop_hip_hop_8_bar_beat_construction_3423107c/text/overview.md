# Pop/Hip-Hop 8-Bar Beat Construction

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pop/Hip-Hop 8-Bar Beat Construction

* **Core Musical Mechanism**: The pattern is built on two foundational pillars: 
  1. A classic, looping 4-chord diatonic progression (IV - I - V - vi).
  2. A standard 16-step drum sequence featuring a syncopated kick (on beat 1 and beat 3 "and"), a backbeat snare (beats 2 and 4), and driving 16th-note hi-hats with strictly alternating velocities.

* **Why Use This Skill (Rationale)**: The IV - I - V - vi progression is ubiquitous in modern commercial music because it provides a satisfying balance of tension and resolution, naturally looping back on itself without ever feeling definitively "finished." For the rhythm, placing the second kick drum on an off-beat (the 16th-note syncopation of the 3 "and") gives the beat its distinct hip-hop bounce. Furthermore, drawing alternating loud/soft velocities on the hi-hats prevents the sequence from sounding robotic—a critical humanization technique explicitly demonstrated in the tutorial.

* **Overall Applicability**: This is the quintessential foundational loop for modern Pop, Hip-Hop, R&B, and Trap tracks. It works perfectly as a main verse or chorus backing groove. 

* **Value Addition**: This skill completely abstracts away the manual labor of piano-roll drawing and step-sequencing. It computationally encodes the relationship between diatonic harmony (building valid chords based on any key/scale) and humanized drum programming.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: 120 - 130 BPM (The tutorial uses 128 BPM).
  - **Grid**: 4/4 time signature, quantized to 16th notes.
  - **Drum Pattern**:
    - Kick: Beat 1 (Step 0) and Beat 3.5 (Step 10).
    - Snare: Beat 2 (Step 4) and Beat 4 (Step 12).
    - Hats: Continuous 16th notes (Steps 0 through 15) with dynamic velocity ramps (alternating loud and soft).

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Dynamically adapts (defaults to C Major).
  - **Progression**: IV - I - V - vi (Scale degrees 3, 0, 4, 5).
  - **Voicing**: Root position triads.

* **Step C: Sound Design & FX**
  - **Chords**: Uses `ReaSynth` as a lightweight stock replacement for the Spitfire Audio piano used in the video.
  - **Drums**: Outputs to standard General MIDI drum mapping (Kick = 36, Snare = 38, Closed Hat = 42).

* **Step D: Mix & Automation (if applicable)**
  - Hi-hats explicitly use automated/programmed velocity shifts (100 for downbeats, 70 for off-beats) to simulate the manual velocity dragging shown in the tutorial.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Chord Progression** | MIDI note insertion + Pitch Calculation | Replicates the manual piano roll drawing from the tutorial while adding procedural scale-awareness so it works in any key. |
| **Drum Sequence** | MIDI note insertion | Directly translates the 16-step grid sequencing (shown via the JS Megababy plugin) into explicit, mathematically placed MIDI events for precise timing and velocity control. |
| **Instrumentation** | FX Chain (ReaSynth) | Ensures the generated chords are immediately audible using REAPER's stock toolset, avoiding third-party VST dependencies. |

> **Feasibility Assessment**: 85%. The musical logic, harmony, timing, and humanized velocities are reproduced with 100% accuracy. The missing 15% is simply the tonal difference between REAPER's stock `ReaSynth`/General MIDI and the specific third-party Spitfire Piano and Sitala drum sampler plugins the user loads in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "PopBeat",
    bpm: int = 128,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pop/Hip-Hop 8-Bar Beat Construction (Chords + Drums) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (128 used in tutorial).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (distributes 4 chords evenly across these bars).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    root_val = NOTE_MAP.get(key, 0)
    root_midi = 48 + root_val  # Base octave C3 = 48
    scale_intervals = SCALES.get(scale, SCALES["major"])

    # Generate a diatonic scale array across multiple octaves
    scale_notes = []
    for oct in range(-1, 4): 
        for interval in scale_intervals:
            scale_notes.append(root_midi + interval + (oct * 12))

    def get_chord_from_scale(degree, num_notes=3):
        """Constructs a root position triad by stacking thirds in the generated scale."""
        base_idx = len(scale_intervals) # Points to the root_midi in the 0th octave
        chord = []
        for i in range(num_notes):
            chord.append(scale_notes[base_idx + degree + (i * 2)])
        return chord

    # Target Progression: IV - I - V - vi (0-indexed scale degrees: 3, 0, 4, 5)
    progression_degrees = [3, 0, 4, 5]
    
    # Timing Setup
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4.0
    item_length = bar_len * bars

    # ==========================================
    # === Step 2: Create Chords Track & MIDI ===
    # ==========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    chords_track_idx = RPR.RPR_CountTracks(0) - 1
    chords_track = RPR.RPR_GetTrack(0, chords_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(chords_track, "P_NAME", f"{track_name} Chords", True)

    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", item_length)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    # Add audible synth to chords track
    RPR.RPR_TrackFX_AddByName(chords_track, "ReaSynth", False, -1)

    # Calculate duration of each chord so they perfectly stretch to fit the `bars` parameter
    chord_len_sec = (bars / len(progression_degrees)) * bar_len
    chord_note_count = 0

    for i, degree in enumerate(progression_degrees):
        chord_notes = get_chord_from_scale(degree, 3)
        start_time = i * chord_len_sec
        end_time = start_time + chord_len_sec - 0.05 # Leave a slight gap for articulation
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        for pitch in chord_notes:
            # Drop velocity slightly for softer pads/chords
            vel = int(velocity_base * 0.8)
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            chord_note_count += 1

    RPR.RPR_MIDI_Sort(chords_take)

    # =========================================
    # === Step 3: Create Drums Track & MIDI ===
    # =========================================
    RPR.RPR_InsertTrackAtIndex(RPR.RPR_CountTracks(0), True)
    drums_track_idx = RPR.RPR_CountTracks(0) - 1
    drums_track = RPR.RPR_GetTrack(0, drums_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drums_track, "P_NAME", f"{track_name} Drums", True)

    drums_item = RPR.RPR_AddMediaItemToTrack(drums_track)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drums_item, "D_LENGTH", item_length)
    drums_take = RPR.RPR_AddTakeToMediaItem(drums_item)

    # General MIDI standard map
    KICK = 36
    SNARE = 38
    HIHAT = 42

    sixteenth_len = beat_len / 4.0
    drum_note_count = 0

    for b in range(bars):
        bar_start = b * bar_len
        
        # Syncopated Kick: Beat 1 (Step 0) and Beat 3.5 (Step 10)
        for step in [0, 10]:
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, KICK, velocity_base, False)
            drum_note_count += 1
            
        # Backbeat Snare: Beat 2 (Step 4) and Beat 4 (Step 12)
        for step in [4, 12]:
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, SNARE, velocity_base, False)
            drum_note_count += 1
            
        # Continuous Hi-Hats with Humanized Alternating Velocity
        for step in range(16):
            start_time = bar_start + (step * sixteenth_len)
            end_time = start_time + sixteenth_len - 0.01
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, end_time)
            
            # Accent downbeats/eighths, soften sixteenth off-beats
            vel = velocity_base if (step % 2 == 0) else int(velocity_base * 0.7)
            RPR.RPR_MIDI_InsertNote(drums_take, False, False, start_ppq, end_ppq, 0, HIHAT, vel, False)
            drum_note_count += 1

    RPR.RPR_MIDI_Sort(drums_take)

    return f"Created Pop/Hip-Hop Beat over {bars} bars at {bpm} BPM. Generated {chord_note_count} chord notes and {drum_note_count} drum hits."
```