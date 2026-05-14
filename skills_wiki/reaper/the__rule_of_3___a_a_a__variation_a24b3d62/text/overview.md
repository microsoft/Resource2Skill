### 1. High-level Design Pattern Extraction

> **Skill Name**: The "Rule of 3" (A-A-A' Variation)

* **Core Musical Mechanism**: Structural repetition combined with a forced deviation. A musical phrase (like a chord progression or melody) is repeated exactly twice to establish familiarity. On the *third* iteration, the phrase begins the same way but diverges halfway through to introduce a new harmony or rhythmic cadence. 
* **Why Use This Skill (Rationale)**: This technique exploits psychoacoustics and cognitive processing. The first listen introduces the idea; the second listen reinforces it, giving the listener the satisfaction of recognizing the pattern. By the third iteration, the brain has "solved" the pattern and begins to tune out ("too much of a good thing"). Forcing a deviation precisely at this moment re-engages the listener's attention and seamlessly transitions the arrangement into the next section.
* **Overall Applicability**: Used universally across pop, electronic, and film composition for structuring 4-bar and 8-bar loops. It prevents loop fatigue in beat-making and creates natural "turnarounds" at the end of verses or build-ups.
* **Value Addition**: Transforms a static, copy-pasted MIDI loop into an evolving arrangement. It encodes the compositional knowledge of *when* to break a pattern, avoiding the amateur mistake of looping a 4-bar phrase endlessly.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4/4 time signature.
  - **Structure**: 12 bars total, broken into three 4-bar iterations.
  - **Rhythm**: Syncopated chord pulse. Chords trigger on beat 1, beat 2.5 (the "and" of 2), and beat 4. 

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (defaults to C Major).
  - **Theme A (Iterations 1 & 2)**: Diatonic chords IV - I - V - vi. 
  - **Theme A' (Iteration 3)**: Diatonic chords IV - I - ii - V. 
  - *Note how Iteration 3 starts identically (IV - I) to trick the listener into expecting the same loop, but diverges to a `ii - V` turnaround to create tension.*

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` configured to act as a plucky, electric piano-like tone.
  - **Parameters**: Fast attack (0.01), moderate decay/release (0.3), using a mix of saw and square waves to cut through the mix.

* **Step D: Mix & Automation**
  - Standard track volume staging. No complex automation is needed, as the interest is generated entirely by the harmonic structure.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **A-A-A' Progression** | MIDI note insertion | Allows for exact programmatic control over scale degrees and time placement to enforce the 3rd-iteration deviation. |
| **Diatonic Chords** | Python Math / Data structures | Encodes music theory dynamically so the Rule of 3 works in any key or scale passed by the agent. |
| **Piano/Synth Sound** | FX chain (ReaSynth) | Provides an immediate, self-contained audible representation of the chords without requiring external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly implements "Option 2" described in the tutorial (repeating a phrase twice, then altering the second half of the third repetition) using stock REAPER tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Keys",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' A-A-A' chord progression in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Length of the base phrase (default 4). Total length will be bars * 3.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Override default if unchanged to provide context
    if track_name == "Drums":
        track_name = "Rule of 3 Keys"

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

    # Generate a massive array of scale notes across 8 octaves to prevent bounds errors
    base_midi = NOTE_MAP.get(key, 0) + 24 # Start at C1 / Octave 1
    scale_intervals = SCALES.get(scale, SCALES["major"])
    all_scale_notes = []
    for oct in range(8):
        for interval in scale_intervals:
            all_scale_notes.append(base_midi + (oct * 12) + interval)

    def get_diatonic_chord(degree: int, num_notes: int = 3, offset_octave: int = 2) -> list:
        """Returns a list of MIDI pitches for a diatonic chord built on 'degree' (1-indexed)."""
        base_idx = (offset_octave * len(scale_intervals)) + (degree - 1)
        return [all_scale_notes[base_idx + i * 2] for i in range(num_notes)]

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: FX Chain (ReaSynth) ===
    # Using ReaSynth to mock up a plucky electric piano sound to demonstrate the chords
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.2)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.01) # Fast attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.3)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5)  # Release
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.3)  # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.7)  # Saw mix

    # === Step 3: Rule of 3 Logic & MIDI Generation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_iterations = 3
    total_bars = bars * total_iterations
    item_length = bar_length_sec * total_bars

    # Create MIDI Item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # Rhythmic syncopation: Beat 1, Beat 2.5 ("and" of 2), Beat 4
    rhythm_offsets = [0.0, 1.5, 3.0] 
    rhythm_durations = [1.0, 1.0, 0.5]

    for bar in range(total_bars):
        iteration = bar // bars
        bar_in_phrase = bar % bars

        # The Rule of 3 Concept: 
        # First 2 loops are identical. The 3rd loop deviates halfway.
        if iteration < 2:
            progression = [4, 1, 5, 6] # Familiar Theme A
        else:
            progression = [4, 1, 2, 5] # Theme A' (Diverges on the 3rd chord)

        # Map to the progression based on where we are in the phrase
        degree = progression[bar_in_phrase % len(progression)]
        chord_pitches = get_diatonic_chord(degree, num_notes=4, offset_octave=2)

        for off, dur in zip(rhythm_offsets, rhythm_durations):
            qn_start = (bar * beats_per_bar) + off
            qn_end = qn_start + dur
            
            start_time = qn_start * (60.0 / bpm)
            end_time = qn_end * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Insert chord notes
            for pitch in chord_pitches:
                # Add a tiny bit of humanization to velocities
                vel = min(127, max(1, int(velocity_base + (off * 5))))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating the Rule of 3 (A-A-A') over {total_bars} bars at {bpm} BPM."
```