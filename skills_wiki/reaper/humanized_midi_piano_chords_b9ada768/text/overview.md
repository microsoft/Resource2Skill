### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized MIDI Piano Chords

* **Core Musical Mechanism**: The defining technique demonstrated in this tutorial is the application of **variable note velocities** to a sequenced MIDI chord progression. Instead of leaving all notes at a uniform default maximum velocity (the "machine-gun" effect), velocities are randomized/adjusted to simulate the natural dynamic variations of a human playing a physical instrument.
* **Why Use This Skill (Rationale)**: When producing acoustic instruments like a Grand Piano via MIDI, uniform velocities sound highly unnatural. A real pianist never strikes every key with the exact same force. Furthermore, lower velocities on most piano VSTs don't just reduce the volume; they trigger entirely different, softer sample layers with fewer high-frequency harmonics. Varying the velocity (humanization) adds groove, dynamic expression, and psychoacoustic realism.
* **Overall Applicability**: This technique is essential anytime you sequence acoustic instruments (pianos, strings, drums, guitars) or want to add a "human feel" (groove) to electronic chord progressions, particularly in genres like lo-fi hip hop, neo-soul, deep house, and pop.
* **Value Addition**: Compared to a basic block-chord MIDI item, this skill encodes the music theory of a diatonic chord progression (I-vi-IV-V) combined with algorithmic performance humanization, bridging the gap between raw sheet music and a realistic performance.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM**: Tutorial uses 120 BPM.
  - **Grid/Timing**: 1 bar per chord. Notes span almost the entire bar but leave a slight staccato gap at the end to emulate releasing the keys before the next strike.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (defaults to C Major).
  - **Chords**: Demonstrates building basic triads. We will implement a full 4-bar progression (I - vi - IV - V) using scale degrees to ensure the chords are always diatonic to the chosen key.
* **Step C: Sound Design & FX**
  - **Instrument**: The tutorial uses a specific 3rd-party "Grand Piano" VSTi. To ensure reproducibility without external dependencies, we will substitute this with REAPER's stock `ReaSynth`, parameterized to have a softer, piano-like decay envelope.
* **Step D: Mix & Automation**
  - **Velocity CC Lane**: Velocities are varied for every single note. In the code, we will algorithmically apply a randomized offset (e.g., ±15) to a base velocity of 90.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Progression | `RPR_MIDI_InsertNote` | Allows exact control over pitch, timing, and crucially, the velocity of every individual note. |
| Velocity Humanization | Python `random.randint()` | Algorithmically mimics the manual dragging of the velocity CC lane shown in the tutorial. |
| Piano Sound | `RPR_TrackFX_AddByName` (ReaSynth) | Provides a guaranteed stock REAPER fallback since the specific Grand Piano VSTi from the tutorial may not be installed. |

> **Feasibility Assessment**: 90% — The precise tonal characteristics of the "Grand Piano" VST cannot be perfectly replicated with stock REAPER plugins, but the core lesson (MIDI drawing, chord duplication, and velocity humanization) is reproduced 100% via the ReaScript API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    humanize_amt: int = 20,
    **kwargs,
) -> str:
    """
    Create a 'Humanized MIDI Piano Chords' sequence in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        humanize_amt: Maximum random ± offset applied to velocity to simulate human playing.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR
    import random

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
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Stock Instrument (ReaSynth as Piano Placeholder) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth parameters for a softer, plucky piano-like envelope
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Attack: 0
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3)  # Decay: ~30%
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1)  # Sustain: low
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release: moderate

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Humanized Chord Progression ===
    # Diatonic progression: I - vi - IV - V (represented as scale degrees, 0-indexed)
    progression = [
        [0, 2, 4], # I
        [5, 7, 2], # vi (last note wrapped to octave below if desired, but 2 maps up naturally)
        [3, 5, 0], # IV
        [4, 6, 1]  # V
    ]

    scale_intervals = SCALES.get(scale, SCALES["major"])
    root_midi = 60 + NOTE_MAP.get(key, 0) # Base octave C4
    
    notes_created = 0

    for bar in range(bars):
        chord_idx = bar % len(progression)
        chord_degrees = progression[chord_idx]

        # Calculate time positions (leaving a 10% gap at the end for realistic key release)
        start_time = bar * bar_length_sec
        end_time = start_time + (bar_length_sec * 0.9)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        for degree in chord_degrees:
            # Map scale degree to exact MIDI note pitch
            octave_shift = degree // len(scale_intervals)
            scale_idx = degree % len(scale_intervals)
            note_pitch = root_midi + scale_intervals[scale_idx] + (octave_shift * 12)

            # --- Core Technique: Velocity Humanization ---
            # Randomize velocity around the base to avoid the "machine gun" effect
            random_offset = random.randint(-humanize_amt, humanize_amt)
            vel = max(1, min(127, velocity_base + random_offset))

            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_pitch, vel, False)
            notes_created += 1

    # Finalize MIDI to ensure it displays correctly
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} humanized velocity notes over {bars} bars at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range? (Checked by `max(1, min(127, ...))`)
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, varying velocity in MIDI chords is the main applied lesson).
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies? (Uses `ReaSynth`).