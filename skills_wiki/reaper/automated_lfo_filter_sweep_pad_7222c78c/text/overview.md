# Automated LFO Filter Sweep Pad

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated LFO Filter Sweep Pad

* **Core Musical Mechanism**: The video tutorial focuses heavily on managing, viewing, and copying track automation and FX parameter modulation. The core musical pattern extracted here is the **Automated Filter Sweep**—a fundamental technique where a static chord progression is brought to life by programmatically drawing a low-frequency oscillator (LFO) curve directly into an FX parameter envelope (in this case, an EQ band's frequency).

* **Why Use This Skill (Rationale)**: Sustained pad chords can quickly become stagnant. By automating the filter cutoff (or EQ band frequency) to sweep up and down rhythmically, we introduce timbral motion and spectral tension/release. This simulates the "Parameter Modulation" tip shown in the video, but baked directly into an editable automation lane, allowing for precise structural control over the movement.

* **Overall Applicability**: Essential for ambient intros, transitions, and breakdown sections in electronic music, pop, and lo-fi. It provides a moving atmospheric bed that fills the frequency spectrum without clashing with lead elements.

* **Value Addition**: Instead of a static block of MIDI notes, this skill encodes harmony (a 4-bar diatonic progression), sound design (configuring a stock synthesizer for a pad sound), and mix automation (generating a sine-wave envelope over an EQ frequency parameter) into a single, cohesive musical element.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Whole notes (1 chord per bar).
  - **Tempo**: Inherits global BPM (defaults to 120).
  - **Movement**: The automation envelope follows a 2-bar sinusoidal cycle, peaking in brightness every other bar.

* **Step B: Pitch & Harmony**
  - Generates a 4-bar chord progression based on the input key and scale.
  - Minor/Dorian scales use the popular `i - VI - III - VII` progression.
  - Major scales use a pop-centric `I - IV - V - vi` progression.
  - Voicings are 4-note 7th chords built diatonically from the selected scale.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a slow-attack, slow-release sawtooth pad.
  - **Effect**: `ReaEQ`, acting as a filter.
  - **Modulation Target**: ReaEQ's Band 3 Frequency (Param Index 6).

* **Step D: Mix & Automation**
  - A programmatic sine-wave loop is calculated and inserted point-by-point into the "Freq-Band 3" automation envelope.
  - The envelope sweeps from roughly 200Hz (0.3 param value) up to ~5kHz (0.8 param value) to create a distinct "wah" or swelling motion.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Progression | MIDI note insertion | Allows calculation of diatonic 7th chords from the requested key/scale. |
| Pad Sound Design | FX Chain (ReaSynth) | Uses REAPER's stock synth to guarantee reproducibility without external VSTs. |
| Filter Sweep | `RPR_GetFXEnvelope` & `RPR_InsertEnvelopePoint` | Directly translates the video's core focus (automation lanes) into programmatic sine-wave LFO points on an EQ. |

> **Feasibility Assessment**: 100% reproduction of the core concept. While the video shows a human clicking and copying automation, this script replicates the end-result: a fully automated, moving FX parameter over a musical phrase.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sweeping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create an Automated LFO Filter Sweep Pad in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import math
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Diatonic Chords ===
    root_val = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0)) + 48 # Base octave C3
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Select progression based on scale flavor
    if "minor" in scale.lower() or "dorian" in scale.lower() or "blues" in scale.lower():
        progression = [0, 5, 2, 6] # i, VI, III, VII
    else:
        progression = [0, 3, 4, 5] # I, IV, V, vi

    notes_created = 0
    RPR.RPR_MIDI_DisableSort(take)
    
    for bar in range(bars):
        degree = progression[bar % len(progression)] % len(scale_intervals)
        
        # Build 4-note diatonic chord (root, 3rd, 5th, 7th)
        chord_notes = []
        for i in range(4):
            scale_idx = (degree + i * 2) % len(scale_intervals)
            octave_offset = (degree + i * 2) // len(scale_intervals)
            chord_notes.append(root_val + scale_intervals[scale_idx] + (12 * octave_offset))
            
        start_qndn = bar * beats_per_bar
        end_qndn = start_qndn + beats_per_bar
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qndn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qndn)
        
        for p in chord_notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (ReaSynth & ReaEQ) ===
    # Add ReaSynth for a basic pad tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 1.0) # Saw shape mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.2) # Slower attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.4) # Longer release
    
    # Add ReaEQ to act as our sweepable filter
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 3 Freq is parameter index 6. 
    # Create the automation envelope for this parameter.
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 6, True)
    
    # === Step 6: Generate Automation Points (LFO Sine Wave) ===
    points_per_bar = 8
    num_points = int(bars * points_per_bar)
    
    for i in range(num_points + 1):
        t = i * (item_length / num_points)
        # 1 complete sine cycle every 2 bars
        cycle_length_sec = bar_length_sec * 2
        phase = (t / cycle_length_sec) * math.pi * 2
        
        # Logarithmic param scale: 0.55 +/- 0.25 keeps it in the "musical" mid-range frequencies
        val = 0.55 + 0.25 * math.sin(phase)
        
        # Insert point (shape 0 = linear)
        RPR.RPR_InsertEnvelopePoint(env, t, val, 0, 0.0, False, True)
        
    RPR.RPR_Envelope_SortOrder(env)

    return f"Created '{track_name}' with {notes_created} notes and a sinusoidal ReaEQ automation envelope over {bars} bars."
```