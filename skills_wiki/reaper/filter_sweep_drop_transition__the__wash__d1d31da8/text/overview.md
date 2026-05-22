### 1. High-level Design Pattern Extraction

> **Skill Name**: Filter Sweep Drop Transition (The "Wash-Out" Effect)

* **Core Musical Mechanism**: Automating a low-pass filter (high-frequency cut) to gradually close over the final bar(s) of a verse or build-up, and then instantaneously snapping back to fully open exactly on the downbeat of the drop or chorus. 
* **Why Use This Skill (Rationale)**: This technique creates massive tension and release through spectral manipulation. By slowly sucking the high-frequency energy out of the track, the listener physically feels a sense of withdrawal and anticipation. When the filter snaps open on the downbeat, the sudden reintroduction of high frequencies psychoacoustically makes the new section feel exponentially wider, brighter, and more impactful than if the transition had no filter.
* **Overall Applicability**: Essential for beatmaking, EDM, and pop production. It is used to transition between low-energy and high-energy sections (e.g., Verse → Chorus, Build-up → Drop). It can be applied to individual synths, entire instrument buses, or even the master track.
* **Value Addition**: Compared to a blank MIDI clip or static audio, this skill encodes the concept of *automation-driven arrangement*. It teaches the agent how to manipulate FX parameters over time to create structural contrast, rather than just adding more notes.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Timing**: The transition occurs over a defined buildup period (usually 1 or 2 bars). 
  - **The "Snap"**: The most critical timing aspect is the envelope snapping from a closed state (e.g., 200Hz) back to an open state (e.g., 20kHz) in the few milliseconds exactly preceding the downbeat.

* **Step B: Pitch & Harmony**
  - Configurable to any key/scale.
  - To demonstrate the filter, the skill generates a 4-bar sustained diatonic chord progression (i - VI - III - VII in minor). Sustained harmonic content is required to make the filter sweep audible.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured to a bright saw wave to ensure rich high-frequency harmonics.
  - **Filter**: `ReaEQ`. Band 4 (High Shelf) is repurposed as a Low-Pass filter by setting its Gain to -inf (0.0 normalized). 
  - **Parameter Focus**: The Frequency of Band 4 (Parameter Index 9) is automated.

* **Step D: Mix & Automation**
  - **Envelope Shape**: A sawtooth/ramp-down automation curve.
  - Starts fully open (0.9 value).
  - Sweeps down over the final bar to a muffled state (0.2 value).
  - Instantly jumps back to fully open (0.9 value) exactly on the downbeat of the drop.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Content | MIDI note insertion | Generates a customizable chord progression so the filter has a wide-spectrum sound to act upon. |
| Sound Source | FX chain (`ReaSynth`) | Stock REAPER synth capable of generating a bright, harmonically rich saw wave. |
| Filter Transition | Automation envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Replicates the exact manual automation curve (ramp down, snap up) demonstrated in the tutorial using stock `ReaEQ`. |

> **Feasibility Assessment**: 100%. The code precisely replicates the tutorial's arrangement technique using native REAPER automation, the exact stock plugin (`ReaEQ`), and parameterized mathematical timing. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "FilterSweepTransition",
    track_name: str = "Synth Drop Bus",
    bpm: int = 120,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Filter Sweep Drop Transition in the current REAPER project.
    Generates a sustained chord progression, applies ReaSynth, and automates 
    a ReaEQ filter sweep that closes over the final bar and opens on the drop.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of buildup bars before the drop.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
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

    scale_degrees = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key, 0) + 48 # Base octave 3

    # Helper function to get MIDI notes from scale degrees
    def get_midi_note(root, scale_arr, degree, octave_offset=0):
        octave = degree // len(scale_arr)
        idx = degree % len(scale_arr)
        return root + scale_arr[idx] + (octave + octave_offset) * 12

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item with Sustained Chords ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_bars = bars + 1 # Add 1 extra bar for the "Drop"
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Diatonic progression indices (i7, VI7, III7, VII7)
    chords = [
        [0, 2, 4, 6], 
        [5, 7, 9, 11], 
        [2, 4, 6, 8], 
        [4, 6, 8, 10] 
    ]

    for bar in range(total_bars):
        chord = chords[bar % len(chords)]
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for degree in chord:
            note = get_midi_note(root_midi, scale_degrees, degree)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note), velocity_base, True)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments & FX ===
    # Add ReaSynth to generate a saw wave (rich in high frequencies to be filtered)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set ReaSynth Param 1 (Saw shape) to 1.0
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0)
    # Set ReaSynth volume down slightly
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.5)

    # Add ReaEQ for the Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # In ReaEQ: 
    # Param 9 = Band 4 Frequency (High Band)
    # Param 10 = Band 4 Gain. We set it to 0.0 (-inf dB) to convert the shelf into a hard cut.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 10, 0.0)

    # === Step 5: Automate Filter Sweep ===
    # Get the envelope for ReaEQ Param 9 (Band 4 Freq)
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 9, True)
    
    # Calculate automation timings
    sweep_start_time = (bars - 1) * bar_length_sec # Start closing 1 bar before drop
    drop_time = bars * bar_length_sec              # Exact moment of the drop
    
    # Insert automation points (shape 0 = linear)
    # RPR_InsertEnvelopePoint(envelope, time, value, shape, tension, selected, noSortIn)
    
    # 1. Start fully open (normalized 0.9 = approx 16kHz)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.9, 0, 0.0, False, True)
    
    # 2. Remain open until the sweep starts
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 0.9, 0, 0.0, False, True)
    
    # 3. Sweep down to heavily muffled (normalized 0.15 = approx 150Hz) right before drop
    RPR.RPR_InsertEnvelopePoint(env, drop_time - 0.02, 0.15, 0, 0.0, False, True) 
    
    # 4. Snap back to fully open EXACTLY on the downbeat of the drop
    RPR.RPR_InsertEnvelopePoint(env, drop_time, 0.9, 0, 0.0, False, True) 

    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with automated 1-bar filter sweep transition over {bars} buildup bars at {bpm} BPM in {key} {scale}."
```