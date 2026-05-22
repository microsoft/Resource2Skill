### 1. High-level Design Pattern Extraction

> **Skill Name**: The Rule of Three (A-A-B Structural Variation)

* **Core Musical Mechanism**: Phrase repetition and controlled variation. The pattern introduces a 4-bar musical idea (A), repeats it exactly once to establish familiarity and hook the listener (A), and on the *third* iteration, introduces a contrasting idea (B) or a variation (A') to prevent cognitive boredom.
* **Why Use This Skill (Rationale)**: This principle leverages human psychoacoustics and attention span. The brain actively seeks and enjoys recognizing patterns (fulfilled by the first repetition), but quickly tunes out static loops (which happens if you play it a third time). By breaking the pattern exactly when the brain confidently expects another identical loop, you force the listener to re-engage and pay attention again.
* **Overall Applicability**: This is a universal composition guideline. It applies to arranging chord progressions, varying drum loops (e.g., adding a fill on the 3rd or 4th bar), vocal phrasing, and overarching song structures. It is the antidote to the "endless 4-bar loop" syndrome.
* **Value Addition**: Transforms a static 4-bar loop into a dynamic, evolving 12-bar musical statement. It encodes the knowledge of *macro-pacing*—giving an automated agent a reliable formula for maintaining listener interest over time.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Works at any tempo, typically in 4/4 time.
  - The macro-structure is 12 bars long, divided into three 4-bar blocks (Iterations 1, 2, and 3).
  - Iterations 1 and 2 use a sparse, relaxed rhythm (e.g., quarter and half notes) to establish the motif. Iteration 3 increases rhythmic density (eighth notes) to heighten the contrast.
* **Step B: Pitch & Harmony**
  - **Phrase A (Bars 1-8)**: A familiar, resolving progression: **I - V - vi - IV**.
  - **Phrase B (Bars 9-12)**: A departing progression that builds tension: **ii - vi - IV - V**.
  - The melody mirrors this by shifting from long, sustained interval jumps to quicker, stepwise descending lines in the 3rd iteration.
* **Step C: Sound Design & FX**
  - Instrument: `ReaSynth` (stock REAPER synth) to act as a clear, bell-like piano/synth stand-in.
  - FX: `ReaVerbate` is added to give the synth physical space, making the chords feel like a cohesive pad.
* **Step D: Mix & Automation (if applicable)**
  - No specific automation is required; the focus is entirely on the compositional arrangement and MIDI placement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| A-A-B Phrase Structure | MIDI note insertion | Provides precise control over chord voicings and melodic rhythm across the 12-bar timeline. |
| Synth Sound | FX chain (ReaSynth + ReaVerbate) | Ensures the pattern is immediately audible with a pleasant, sustained tone without requiring third-party VSTs. |

> **Feasibility Assessment**: 100% reproducible. The psychological concept taught in the tutorial is perfectly captured by programmatically generating the 3-part sequence as a self-contained MIDI item with stock instruments.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 'The Rule of Three (A-A-B Structural Variation)' in the current REAPER project.
    Generates a 12-bar progression demonstrating exact repetition followed by variation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Total bars (overridden to 12 internally to demonstrate the 3-part rule).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12  # Fixed to 12 bars to represent 3 iterations of 4 bars
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory calculations
    root_pitch = NOTE_MAP.get(key, 0) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_pitch(degree, octave_shift=0):
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_pitch + (octave + octave_shift) * 12 + scale_intervals[idx]

    def add_chord(bar, degree, length_beats):
        start_time = (bar * beats_per_bar) * (60.0 / bpm)
        end_time = start_time + length_beats * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Triad: Root, Third, Fifth
        for d in [degree, degree + 2, degree + 4]:
            pitch = get_pitch(d)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, max(1, velocity_base - 15), True)

    def add_melody_note(bar, beat, degree, length_beats):
        start_time = (bar * beats_per_bar + beat) * (60.0 / bpm)
        end_time = start_time + length_beats * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        pitch = get_pitch(degree, octave_shift=1) # Melody an octave up
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)

    # Define the 4-bar phrases (Chords in relative scale degrees: 0=I, 1=ii, 3=IV, 4=V, 5=vi)
    phrase_A_chords = [0, 4, 5, 3] # I - V - vi - IV
    phrase_A_melody = [
        [(0, 0, 1.5), (2, 2, 1.5)], # (beat, degree, duration_in_beats)
        [(0, 4, 1.5), (2, 2, 1.5)],
        [(0, 5, 1.5), (2, 4, 1.5)],
        [(0, 3, 1.5), (2, 0, 1.5)]
    ]

    phrase_B_chords = [1, 5, 3, 4] # ii - vi - IV - V (The variation)
    phrase_B_melody = [
        [(0, 1, 0.5), (1, 3, 0.5), (2, 5, 0.5), (3, 4, 0.5)], # Quicker, descending 8th notes
        [(0, 5, 0.5), (1, 7, 0.5), (2, 9, 0.5), (3, 8, 0.5)],
        [(0, 3, 0.5), (1, 5, 0.5), (2, 7, 0.5), (3, 5, 0.5)],
        [(0, 4, 0.5), (1, 6, 0.5), (2, 8, 0.5), (3, 7, 0.5)]
    ]

    # Iteration 1 (Bars 0-3): Introduce Phrase A
    for i in range(4):
        add_chord(i, phrase_A_chords[i], 3.8)
        for note in phrase_A_melody[i]:
            add_melody_note(i, note[0], note[1], note[2])
            
    # Iteration 2 (Bars 4-7): Repeat Phrase A to build familiarity
    for i in range(4):
        add_chord(i + 4, phrase_A_chords[i], 3.8)
        for note in phrase_A_melody[i]:
            add_melody_note(i + 4, note[0], note[1], note[2])

    # Iteration 3 (Bars 8-11): Switch to Phrase B (The Rule of 3 Variation)
    for i in range(4):
        add_chord(i + 8, phrase_B_chords[i], 3.8)
        for note in phrase_B_melody[i]:
            add_melody_note(i + 8, note[0], note[1], note[2])

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.15) # Wet level
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.90) # Dry level

    return f"Created '{track_name}' with a 12-bar A-A-B structural progression at {bpm} BPM in {key} {scale}."
```