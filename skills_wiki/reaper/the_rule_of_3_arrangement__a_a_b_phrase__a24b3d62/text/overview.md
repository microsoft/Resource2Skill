### 1. High-level Design Pattern Extraction

> **Skill Name**: The Rule of 3 Arrangement (A-A-B Phrase Structure)

* **Core Musical Mechanism**: This pattern leverages a fundamental compositional framework consisting of Repetition and Variation. A specific musical idea (Phrase A) is established, repeated exactly once to build expectation and confirm the pattern, and then intentionally altered, subverted, or completely changed on the third iteration (Phrase B).
* **Why Use This Skill (Rationale)**: Human brains are highly efficient pattern-matching machines. One iteration of a melody is an occurrence; two iterations establish a recognizable pattern. By the third iteration, the brain anticipates the repetition and begins to drop its active listening state (what the instructor describes as "tuning it out"). Introducing a harmonic or melodic shift right at the moment of expected repetition forces the listener to re-engage, providing a spike of dopamine and sustaining their attention. As the tutorial notes: "Too much of a good thing is no longer a good thing."
* **Overall Applicability**: This psychoacoustic principle applies universally across arrangement, beatmaking, and songwriting. It dictates drum fill placements (3 bars of groove, 1 bar of fill), vocal phrasing, and macro song structures (e.g., repeating a 4-bar chord progression twice, then going somewhere different for the final 4 bars of a verse).
* **Value Addition**: Compared to looping a 4-bar MIDI clip endlessly, this skill explicitly encodes structural progression and listener psychology into the arrangement, transforming a static "loop" into a forward-moving song section.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Structure**: A macro-block evenly divided into three sections (Phrase A1, Phrase A2, Phrase B). In standard pop context, this is usually 12 bars (3 phrases of 4 bars), but it geometrically scales to fit any block length.
  - **Articulation**: Chords are played with slight syncopation or an 80% legato gate to feel like a live performance rather than a static block, allowing the harmonic rhythm to breathe.
* **Step B: Pitch & Harmony**
  - **Phrase A (The Establishment & Reinforcement)**: Uses a standard functional progression. Represented here via scale degrees I - V - vi - IV (0, 4, 5, 3). This plays twice.
  - **Phrase B (The Subversion)**: Shifts the harmonic center to subvert expectations. Represented here by starting on the relative minor or subdominant: vi - IV - ii - V (5, 3, 1, 4), forcing the ear to re-evaluate the tonal center.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured to act as an electric piano/keyboard (the instrument played in the video tutorial).
  - **Envelope**: Fast attack (0.01), medium decay (0.3), low sustain (0.2) to create a plucky, rhythmic transient that highlights chord changes clearly without creating muddy overlap.
* **Step D: Mix & Automation (if applicable)**
  - Track volume is set naturally, utilizing lower octaves for bass reinforcement and higher octaves for triad voicings to ensure frequency balance across the chords.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| A-A-B Structure | MIDI Note Insertion & Algorithmic generation | Enables programmatic splitting of any `bars` duration into three distinct harmonic phrases. |
| Harmonic Logic | Scale Degree Lookup Tables | Computes precise MIDI pitches from dynamic `key` and `scale` inputs instead of hardcoding the tutorial's exact C-Major piano chords. |
| Sound Design | `ReaSynth` FX Chain Configuration | Native REAPER synth; tweaking the ADSR envelope replicates the plucky, keyboard-like tone from the video without relying on external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The script captures the core *structural teaching* of the video (the Rule of 3) by dynamically generating an A-A-B chord sequence over whatever timeframe the user requests, using only built-in REAPER tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Creates a musical block demonstrating the 'Rule of 3' (A-A-B repetition/variation structure).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total number of bars to generate (will be divided into 3 phrases).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    # Validate inputs
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "major"
    
    root_midi = 48 + NOTE_MAP[key] # C3 Base
    scale_intervals = SCALES[scale]

    # Helper to calculate correct MIDI pitch based on scale degree
    def get_pitch(degree, octave_offset=0):
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_midi + (octave + octave_offset) * 12 + scale_intervals[idx]

    def get_triad(degree):
        # 1-3-5 chord voicings based on the active scale
        return [get_pitch(degree), get_pitch(degree+2), get_pitch(degree+4)]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth and configure as a plucky keys/piano sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.01) # Fast attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Medium decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.2)  # Low sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.4)  # Release

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Apply the "Rule of 3" Composition Logic ===
    # 12-chord macro sequence that executes the Rule of 3
    # Phrase A1 (Pattern Intro), Phrase A2 (Pattern Confirmed), Phrase B (The Subversion)
    macro_progression = [
        0, 4, 5, 3,  # Phrase A1 (e.g. I, V, vi, IV)
        0, 4, 5, 3,  # Phrase A2 (Repeats exact same idea)
        5, 3, 1, 4   # Phrase B  (Rule of 3 subversion: vi, IV, ii, V)
    ]
    
    total_chords = len(macro_progression)
    beats_per_chord = (bars * beats_per_bar) / float(total_chords)
    PPQ = 960  # Default pulses per quarter note in REAPER

    for i, degree in enumerate(macro_progression):
        start_beat = i * beats_per_chord
        # Make chords play for 80% of the duration so it breathes (legato envelope)
        end_beat = start_beat + (beats_per_chord * 0.8)

        start_tick = int(start_beat * PPQ)
        end_tick = int(end_beat * PPQ)

        notes = get_triad(degree)
        bass_pitch = get_pitch(degree, -1) # Add a solid root bass note

        # Insert Bass Note
        RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, bass_pitch, velocity_base + 10, False)
        
        # Insert Triad Notes
        for pitch in notes:
            # Humanize velocity slightly across chord stack
            vel = max(1, min(127, velocity_base - (pitch % 5)))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_tick, end_tick, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-B structure) with 12 chords over {bars} bars at {bpm} BPM in {key} {scale}."
```