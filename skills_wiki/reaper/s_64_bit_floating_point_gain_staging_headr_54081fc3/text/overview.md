# 64-Bit Floating-Point Gain Staging (Headroom Demonstration)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 64-Bit Floating-Point Gain Staging (Headroom Demonstration)

* **Core Musical Mechanism**: Utilizing the virtually infinite headroom of a modern DAW's 64-bit floating-point audio engine. By routing an audio signal through a massive gain boost (+100 dB) that severely exceeds 0 dBFS, and subsequently applying an equivalent gain reduction (-100 dB) before the signal reaches the hardware output, the audio is perfectly reconstructed without digital clipping or data loss.
* **Why Use This Skill (Rationale)**: This demystifies digital gain staging. In analog hardware (or fixed-point systems), hitting the "red" permanently destroys the waveform, creating harsh harmonic distortion. In REAPER's 64-bit float environment, the internal channels have over +1500 dB of headroom. Understanding this liberates the mixing process—you don't need to micro-manage every single plugin's input/output meters, so long as the final Master Fader (which goes to your fixed-point DAC/speakers) does not clip.
* **Overall Applicability**: Essential for routing, bussing, and mixing in modern DAWs. This allows producers to fearlessly push EQs, synths, and saturators on individual tracks or folders, knowing they can simply turn down the group bus or master fader to achieve a clean, undistorted final mix.
* **Value Addition**: Compared to standard mixing advice, this encodes the technical truth of modern digital audio. It proves that internal clipping is a visual myth in DAWs (excluding analog-modeled plugins that enforce artificial input ceilings) and provides a programmatic sandbox to prove the math.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: A single, continuous sustained chord.
  - **Duration**: Fills the specified number of bars entirely to allow the user to clearly hear the clean, sustained tone despite the internal clipping.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Dynamic based on input parameters.
  - **Voicing**: A fundamental root position triad (Root, 3rd, 5th) derived from the selected scale.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` to generate a pure, clean digital tone.
  - **FX 1 (The Overload)**: `JS: Volume Adjustment` applying an extreme **+100 dB** boost. At this stage, the REAPER track meter will hit +100 dB and the internal signal is mathematically astronomical.
  - **FX 2 (The Recovery)**: A second `JS: Volume Adjustment` applying a reciprocal **-100 dB** cut. The 64-bit math seamlessly divides the signal back to its original amplitude, outputting a perfectly clean synth chord to the master.
* **Step D: Mix & Automation**
  - No automation curves are needed; the static massive gain offset perfectly demonstrates the architecture's headroom.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Audio Source | MIDI note insertion + ReaSynth | Generates a clean, consistent tone from parameter-derived chords to make distortion (or lack thereof) obvious. |
| Gain Overload | FX parameter manipulation (`TrackFX_SetParam`) | Using `JS: Volume Adjustment` guarantees we can apply absurd gain boosts (+100dB) programmatically. |
| Gain Recovery | FX parameter manipulation (`TrackFX_SetParam`) | A second identical plugin perfectly mirrors the tutorial's method of nullifying the internal clipping. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly recreates the tutorial's primary demonstration: driving a signal impossibly loud internally and rescuing it losslessly before the final output.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Float_Headroom_Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create 64-Bit Floating-Point Gain Staging in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Float_Headroom_Demo' demonstrating +100dB floating point recovery."
    """
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

    import reaper_python as RPR

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

    # Calculate Triad Pitches based on parameters
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    octave_base = 60 # C4
    
    chord_notes = [
        octave_base + root_val + scale_intervals[0], # Root
        octave_base + root_val + scale_intervals[2], # 3rd
        octave_base + root_val + scale_intervals[4]  # 5th
    ]

    # Insert sustained MIDI notes
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)
    
    for note in chord_notes:
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, False)

    # === Step 4: Add FX Chain ===
    
    # 1. Clean Sound Generator
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Extreme Overload: +100 dB Boost (Would permanently distort a fixed-point system)
    boost_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    # Param 0 in JS: Volume Adjustment is 'Adjustment (dB)'
    RPR.RPR_TrackFX_SetParam(track, boost_idx, 0, 100.0)
    
    # 3. Floating Point Recovery: -100 dB Cut (Perfectly restores the clean signal)
    cut_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    RPR.RPR_TrackFX_SetParam(track, cut_idx, 0, -100.0)

    return f"Created '{track_name}' demonstrating floating-point headroom: +100dB internal clip followed by -100dB perfect recovery."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?