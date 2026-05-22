### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Sweep & Tension Builder

* **Core Musical Mechanism**: The defining signature of this pattern is **parameter movement over time**—specifically, automating a synthesizer's high-frequency content (via an EQ filter sweep) alongside a sustained chord. This takes a static sound and gives it a distinct temporal trajectory (rising tension or fading energy).

* **Why Use This Skill (Rationale)**: In music theory and psychoacoustics, stationary sounds are perceived as lifeless or stagnant. By sweeping a filter (e.g., gradually increasing the cutoff frequency of a low-pass filter or high-shelf), we emulate an increase in acoustic energy and brightness. This exploits the psychological expectation of "opening up," making it a foundational technique for transitioning between sections, building anticipation before a drop, or creating dynamic, breathing pad sounds.

* **Overall Applicability**: This skill is essential for electronic music (EDM, house, synthwave), cinematic scoring (evolving drones), and modern pop (intro/outro fades). It shines when you need to bridge two sections of a song or create an evolving atmosphere behind a sparse arrangement. 

* **Value Addition**: Compared to a blank MIDI clip or a static synth track, this skill encodes the concept of *temporal modulation*. It automatically handles the complex routing of generating a track, inserting a synth, layering an EQ, extracting the specific automation envelope for the frequency band, and mathematically plotting the sweep curve perfectly across the duration of the musical phrase.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, dynamically adjustable (default 120 BPM).
  - **Rhythm**: Sustained whole notes tied across the entire specified duration (e.g., a 4-bar sustained chord). 
  - **Automation Timing**: A linear automation curve that spans exactly from the start of the item (Beat 1, Bar 1) to the very end of the item, ensuring the "swell" completes perfectly in time with the grid.

* **Step B: Pitch & Harmony**
  - **Harmony**: A lush, 4-note extended chord (Root, 3rd, 5th, 7th) to ensure a rich frequency spectrum. Without upper harmonics, a filter sweep is imperceptible; the 7th provides necessary high-frequency density for the sweep to act upon.
  - **Pitch Computation**: Calculated dynamically based on the requested key and scale.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` (stock REAPER synth) to generate a harmonically rich base tone.
  - **Effect**: `ReaEQ` (stock REAPER EQ).
  - **Parameter Routing**: The automation targets ReaEQ's Band 4 Frequency (Parameter Index 9). Sweeping this parameter creates the characteristic opening/closing filter effect.

* **Step D: Mix & Automation (if applicable)**
  - **Automation Envelope**: Utilizes the REAPER FX Envelope API to arm and draw points on the ReaEQ frequency parameter.
  - **Curve Shape**: Linear interpolation (Shape 0) between a muffled start state (normalized value `0.1`) and a bright, open end state (normalized value `0.9`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Lush Chord Generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides precise quantization, velocity control, and allows the chord to easily adapt to any BPM or duration. |
| Synth & EQ Chain | FX chain (`RPR_TrackFX_AddByName`) | Guarantees stock, native reproducibility without relying on 3rd-party VSTs or external samples. |
| Filter Sweep | FX Automation Envelope (`RPR_GetFXEnvelope` & `RPR_InsertEnvelopePoint`) | Directly implements the tutorial's core lesson ("Automate Anything"). Native API plotting is cleaner and mathematically perfect compared to mouse-drawn "Touch" mode automation. |

> **Feasibility Assessment**: 100% reproducible. The code uses purely stock REAPER plugins (ReaSynth, ReaEQ) and native ReaScript API functions to create the track, MIDI, effects, and exact automation envelope demonstrated conceptually in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Filter Sweep Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an automated filter sweep on a sustained synth chord.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the sweep and chord should last.
        velocity_base: Base MIDI velocity for the chord (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated elements.
    """
    import reaper_python as RPR

    # === Music Theory Dictionaries ===
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

    # === Step 1: Project Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Calculate timing
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    start_time = RPR.RPR_GetCursorPosition()
    
    # === Step 2: Track Creation ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: MIDI Item & Harmony Generation ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Construct a lush 4-note chord based on the scale (Root, 3rd, 5th, 7th)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_val = NOTE_MAP.get(key.capitalize(), 0)
    base_octave = 48 # C3
    
    chord_degrees = [0, 2, 4, 6] # 1st, 3rd, 5th, 7th of the scale
    chord_pitches = []
    
    for degree in chord_degrees:
        if degree < len(scale_intervals):
            pitch = base_octave + root_val + scale_intervals[degree]
        else:
            # Wrap around to the next octave if needed
            pitch = base_octave + root_val + scale_intervals[degree % len(scale_intervals)] + 12
        chord_pitches.append(pitch)

    # Insert MIDI notes (1 beat = 960 PPQ)
    start_ppq = 0
    end_ppq = int(bars * beats_per_bar * 960)
    
    for pitch in chord_pitches:
        # Note parameters: take, selected, muted, startppq, endppq, channel, pitch, velocity, noSort
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: FX Chain & Sound Design ===
    # Add Synthesizer
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Add EQ for the Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Parameter Automation ===
    # Automate ReaEQ Band 4 Frequency (Parameter Index 9)
    # The 'True' flag forces REAPER to create/arm the envelope if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    if env:
        # Envelope values are normalized 0.0 to 1.0. 
        # 0.1 is a muffled low frequency, 0.9 is a bright open high frequency.
        # Shape 0 = Linear transition
        
        # Point 1: Start of item (muffled)
        RPR.RPR_InsertEnvelopePoint(env, start_time, 0.1, 0, 0.0, False, True)
        
        # Point 2: End of item (open/bright)
        RPR.RPR_InsertEnvelopePoint(env, start_time + item_length, 0.9, 0, 0.0, False, True)
        
        # Sort envelope points to apply changes
        RPR.RPR_Envelope_Sort(env)

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' featuring an automated filter sweep over {bars} bars at {bpm} BPM in {key} {scale}."
```