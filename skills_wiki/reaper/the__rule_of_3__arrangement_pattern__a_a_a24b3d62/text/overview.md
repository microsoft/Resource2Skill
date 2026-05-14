### 1. High-level Design Pattern Extraction

> **Skill Name**: The "Rule of 3" Arrangement Pattern (A-A-A' Progression)

* **Core Musical Mechanism**: The psychological threshold of musical repetition. When a musical phrase (a chord progression or melody) is played the first time, it is intriguing. The second time, it reinforces the pattern in the listener's ear. By the third time, the brain begins to tune it out due to predictability ("too much of a good thing"). The core mechanism is a 3-phrase structure (A - A - A') where the 3rd iteration starts identically but introduces a structural deviation (turnaround, new chord, or melodic variation) to recapture listener attention.

* **Why Use This Skill (Rationale)**: This principle is deeply rooted in human cognitive processing and pattern recognition. A complete lack of repetition causes confusion, while excessive repetition causes fatigue. The "Rule of 3" perfectly balances familiarity and novelty. Musically, altering the end of the third phrase builds tension that often leads perfectly into a new song section (like a chorus or bridge). 

* **Overall Applicability**: This is a macro-compositional skill applicable to almost every genre. It is highly effective for 4-bar chord loops in pop, EDM drops, boom-bap drum variations (adding a fill on the 3rd or 4th bar), and vocal hook phrasing. 

* **Value Addition**: Compared to a blank MIDI clip or a simple looping item, this skill encodes professional arrangement structure. It demonstrates how to logically extend a 4-bar loop into a compelling 12-bar section that naturally holds attention without requiring complex sound design.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **BPM**: ~120 BPM (Versatile, adaptable to user input)
  - **Structure**: 12 bars total, divided into three 4-bar phrases.
  - **Rhythm Grid**: Sustained whole notes (chords) to clearly demonstrate the harmonic shift without rhythmic distraction.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Major (configurable)
  - **Phrase 1 & 2 (The Establishment)**: Uses the progression IV - V - vi - iii. (In C Major: F - G - Am - Em).
  - **Phrase 3 (The Deviation)**: Uses Option 2 from the tutorial ("start the same, go somewhere different"). It uses IV - V - ii - I. (In C Major: F - G - Dm - C). 
  - **Voicings**: Triads with a duplicated root note one octave below for bass presence.

* **Step C: Sound Design & FX**
  - **Instrument**: REAPER's native `ReaSynth`. 
  - **Timbre**: A basic warm pad/electric piano tone created by lowering the oscillator mix and tweaking the envelope.

* **Step D: Mix & Automation**
  - No complex automation needed; the focus is purely on the arrangement and harmonic deviation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rule of 3 Structure | Python Loop Logic | Allows us to systematically generate the A-A-A' phrase variations. |
| Harmony/Chords | MIDI note insertion | Perfect control over chord voicings, scale degrees, and exact timing. |
| Sound Design | FX chain (ReaSynth) | Uses stock REAPER plugins to guarantee reproducible audio playback. |

> **Feasibility Assessment**: 100% reproducible. The tutorial teaches a structural/compositional theory rather than a specific synth patch. We can perfectly model this "Rule of 3" deviation using a diatonic chord progression script.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, 
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create the 'Rule of 3' Progression pattern in REAPER.
    Generates a 12-bar sequence (three 4-bar phrases) demonstrating how to 
    deviate on the 3rd repetition to hold listener interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored here; strictly locked to 12 bars to demonstrate the 3x4 phrase rule.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    # Safe defaults
    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "major"
    
    root_pitch = NOTE_MAP[key] + 48 # Root at C3
    scale_intervals = SCALES[scale]
    
    # Helper to get diatonic pitches
    def get_scale_pitch(root, intervals, degree):
        octave = degree // len(intervals)
        note_idx = degree % len(intervals)
        return root + (octave * 12) + intervals[note_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # We strictly use 12 bars to demonstrate the Rule of 3 (4 bars x 3 iterations)
    total_bars = 12
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: The Rule of 3 Logic & Note Insertion ===
    # Phrase structure based on scale degrees (0-indexed). 
    # Example in Major: 3=IV, 4=V, 5=vi, 2=iii, 1=ii, 0=I
    phrases = [
        [3, 4, 5, 2], # Phrase 1: Standard loop (IV - V - vi - iii)
        [3, 4, 5, 2], # Phrase 2: Identical repetition to reinforce idea
        [3, 4, 1, 0]  # Phrase 3: The Deviation (IV - V - ii - I)
    ]

    ppq_per_quarter = 960
    ppq_per_bar = ppq_per_quarter * 4
    note_count = 0

    for phrase_idx, phrase_chords in enumerate(phrases):
        for bar_idx, chord_degree in enumerate(phrase_chords):
            # Calculate timing
            start_ppq = (phrase_idx * 4 + bar_idx) * ppq_per_bar
            end_ppq = start_ppq + ppq_per_bar - 120 # leave a slight gap between chords
            
            # Generate diatonic triad
            pitches = [
                get_scale_pitch(root_pitch, scale_intervals, chord_degree - 7), # Bass octave down
                get_scale_pitch(root_pitch, scale_intervals, chord_degree),     # Root
                get_scale_pitch(root_pitch, scale_intervals, chord_degree + 2), # 3rd
                get_scale_pitch(root_pitch, scale_intervals, chord_degree + 4), # 5th
            ]
            
            # Insert notes
            for pitch in pitches:
                pitch_clamped = max(0, min(127, pitch)) # Safety clamp
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_clamped, velocity_base, False)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Stock Instrument (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a soft electric piano/pad feel instead of harsh default sine
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)   # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.8)   # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.3)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4)   # Release

    return f"Created '{track_name}' showcasing the 'Rule of 3' (12 bars, 3 phrases). Deviated harmonically on phrase 3. Inserted {note_count} notes at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? (Bars intentionally overridden to 12 as this specific concept strictly requires a 3x repetition structure).
- [x] Does it avoid hardcoded file paths or external sample dependencies?