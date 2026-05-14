### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic "Humanized" MIDI Chord Progression

* **Core Musical Mechanism**: The defining characteristic of this pattern is **velocity variance and ramping** within a block chord progression. Instead of static, uniform, perfectly quantized velocity levels (e.g., all 127), the skill intentionally voices chords so the root note is struck harder than the third and fifth. It also incorporates a macroscopic velocity crescendo across the progression, mimicking a human player building emotional intensity over time.
* **Why Use This Skill (Rationale)**: Static velocities instantly give away a programmed, "robotic" sequence. Real pianists inherently play with nuanced dynamics: they anchor the harmony by playing the root note with more force, while internal harmony notes (like the third) are played slightly softer. Furthermore, drawing an upward or downward slope in the MIDI CC velocity lane (as highlighted in the tutorial) creates musical tension and release, guiding the listener's ear through a phrasing arc. 
* **Overall Applicability**: Essential for any genre that relies on virtual acoustic instruments (pianos, electric keys, string ensembles) such as Pop, Neo-Soul, R&B, and Cinematic Ambient music. It provides a highly realistic, organic foundation before applying further processing.
* **Value Addition**: Compared to a blank MIDI clip, this skill automatically translates raw chord degrees into properly voiced triads, injects algorithmic humanization (root emphasis), and applies an automated velocity envelope curve—all while staying strictly within your requested key and scale.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: 4/4, typically 120 BPM (adjustable).
  - **Rhythm**: Whole-note chord blocks (1 chord per bar) with a slight legato gap (90% of the bar length) to allow the release envelope of the synth to breathe before the next chord strikes.
* **Step B: Pitch & Harmony**
  - **Progression**: A classic 4-bar pop progression: **I - V - vi - IV** (Degrees 0, 4, 5, 3).
  - **Voicing**: Root position triads.
* **Step C: Sound Design & FX**
  - **Instrument**: Uses REAPER's native `ReaSynth` configured to act as a placeholder electric piano/pluck (fast attack, medium decay, lower sustain). 
* **Step D: Mix & Automation**
  - **Micro-dynamics (Internal Voicing)**: Root note = 100% target velocity, Third = 80%, Fifth = 85%.
  - **Macro-dynamics (Phrase Crescendo)**: The overall velocity of the chords scales up from 70% in Bar 1 to 100% in Bar 4, programmatically recreating the "draw a ramp in the velocity lane" technique demonstrated in the video.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Structure | `RPR_MIDI_InsertNote` | Precise pitch assignment based on a music theory lookup table to translate degrees into exact MIDI notes. |
| Humanized Dynamics | Parametric math | Calculates individual note velocities (root emphasis) and a linear crescendo ramp. |
| Placeholder Instrument | `RPR_TrackFX_AddByName` (ReaSynth) | Ensures the item makes sound natively without relying on external VSTs like the Grand Piano shown in the tutorial. |

> **Feasibility Assessment**: 90% reproducibility. The core MIDI editing, quantizing, and velocity ramping concepts are perfectly reproduced. The only missing element is the specific third-party Grand Piano VST, which is safely replaced with a molded stock ReaSynth. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Humanized MIDI Chord Progression with dynamic velocity ramping.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (loops the I-V-vi-IV progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
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

    # === Step 1: Set Tempo and Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Set up Instrument (ReaSynth) ===
    # Using ReaSynth as a stand-in for the Piano, tweaked for a plucky decay
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth standard param indices: 4=Attack, 5=Decay, 6=Sustain, 7=Release
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.02)  # Fast attack
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.35)  # Plucky decay
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.20)  # Low sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.50)  # Gentle release

    # === Step 3: Setup MIDI Item ===
    beats_per_bar = 4
    bar_len_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_len_sec * bars
    start_time = 0.0

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to compute MIDI pitches
    def get_pitch(degree, octave=4):
        scale_arr = SCALES.get(scale, SCALES["major"])
        oct_shift = degree // len(scale_arr)
        idx = degree % len(scale_arr)
        # MIDI base: C4 is 60 (Standard)
        return NOTE_MAP[key] + (octave + 1) * 12 + (oct_shift * 12) + scale_arr[idx]

    # === Step 4: Insert Notes (I - V - vi - IV) ===
    progression = [0, 4, 5, 3] # Scale degrees for the standard progression
    notes_added = 0

    for i in range(bars):
        bar_start_sec = start_time + (i * bar_len_sec)
        
        # Make the note length 90% of a bar so it leaves a short rest before the next chord
        note_start_sec = bar_start_sec
        note_end_sec = bar_start_sec + (bar_len_sec * 0.90)

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)

        degree = progression[i % len(progression)]

        # --- Macro Velocity Ramp (Crescendo across the bars) ---
        # Starts at 70% force, ramps to 100% force by the last bar
        bar_crescendo_multiplier = 0.7 + (0.3 * (i / max(1, bars - 1)))

        # Triad construction (Root, Third, Fifth)
        for chord_idx, offset in enumerate([0, 2, 4]):
            pitch = get_pitch(degree + offset, octave=4)

            # --- Micro Velocity Humanization (Per-note variance) ---
            if chord_idx == 0:
                note_vel = velocity_base              # Root is anchored strongly
            elif chord_idx == 1:
                note_vel = int(velocity_base * 0.80)  # Third is played softly
            else:
                note_vel = int(velocity_base * 0.85)  # Fifth is medium

            # Combine macro ramp and micro humanization
            final_vel = int(note_vel * bar_crescendo_multiplier)
            final_vel = max(1, min(127, final_vel))

            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, False)
            notes_added += 1

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} humanized chord notes over {bars} bars at {bpm} BPM in {key} {scale}."
```