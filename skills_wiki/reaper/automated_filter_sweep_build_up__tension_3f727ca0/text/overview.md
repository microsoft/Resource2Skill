### 1. High-level Design Pattern Extraction

> **Skill Name**: Automated Filter Sweep Build-up (Tension Generator)

* **Core Musical Mechanism**: The core pattern here is **Automation over Time**—specifically, automating the cutoff frequency of a filter across multiple bars. In the tutorial, this is demonstrated as drawing an envelope to sweep the Low Pass/High Pass frequency of ReaEQ. This creates a gradual change in timbre that builds kinetic energy before a drop or transition.
* **Why Use This Skill (Rationale)**: Filter sweeps play on the psychoacoustic principle of "tension and release." By slowly removing frequencies (e.g., sweeping a high-pass filter up to remove the fundamental bass, thinning out the sound), you create a sense of anticipation. When the filter suddenly resets or the next section of the song begins, the return of the full frequency spectrum hits the listener with maximum impact. 
* **Overall Applicability**: This is a mandatory technique for electronic music, pop transitions, and cinematic build-ups. It is typically applied to synth pads, full drum busses, or riser effects over 4 to 8 bars right before the chorus or drop.
* **Value Addition**: Compared to static MIDI, this skill encodes the concept of *macro-movement*. It introduces REAPER's FX Envelope API (`RPR_GetFXEnvelope`), demonstrating how to programmatically draw automation curves (linear, bezier) to breathe life and movement into otherwise static synthesizers.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Timing**: A single, sustained chord held over the entire specified duration (e.g., 4 bars).
  - **Automation Timing**: The envelope starts at bar 1 (value 0.0) and continuously interpolates to the end of the item (value 0.7), creating a smooth 4-bar swell.

* **Step B: Pitch & Harmony**
  - **Harmony**: A lush 9th chord (Root, 3rd, 5th, 7th, 9th) built from the user's selected key and scale. This provides a wide, thick frequency spectrum, ensuring the filter has plenty of harmonic material to sweep through.

* **Step C: Sound Design & FX**
  - **Sound Source**: `ReaSynth`. The default sine wave is mixed out (0.0) and the Sawtooth wave is maxed (1.0) to provide rich upper harmonics.
  - **Filter / EQ**: `ReaEQ`. Band 1 is manipulated to act as a high-pass filter by dropping its gain to `-inf` (normalized `0.0`). 

* **Step D: Mix & Automation (The Core Technique)**
  - **Envelope**: An automation envelope is generated for ReaEQ Band 1 Frequency (Parameter `0`).
  - **Curve**: The envelope uses an exponential/bezier shape (Shape `5`) to sweep the frequency from 20Hz up to roughly 2kHz, progressively thinning out the pad.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Sound Generation** | MIDI Note Insertion + `ReaSynth` | A static sawtooth 9th chord provides the ideal dense harmonic bed for a filter sweep. |
| **Filter Setup** | `ReaEQ` (Param 1 Gain = 0.0) | By setting Band 1's gain to zero, it behaves exactly like a High-Pass filter, cutting all frequencies below its cutoff point. |
| **The Sweep** | Automation Envelope (`RPR_GetFXEnvelope`) | Matches the tutorial's exact method of drawing envelopes to automate FX parameters over time. |

> **Feasibility Assessment**: 100% reproducible. By hooking directly into REAPER's native `ReaEQ` parameter indices and the Track Envelope API, we can programmatically generate the exact automation curves Kenny Gioia demonstrates manually in the video.

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
    Creates an Automated Filter Sweep Build-up using ReaSynth and ReaEQ.
    Demonstrates programmatic envelope automation (High-pass wash effect).

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Duration of the sweep build-up.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define 9th chords to ensure a thick frequency spectrum for the filter
    CHORD_INTERVALS = {
        "major": [0, 4, 7, 11, 14], # Maj9
        "minor": [0, 3, 7, 10, 14], # Min9
        "dorian": [0, 3, 7, 10, 14],
        "mixolydian": [0, 4, 7, 10, 14]
    }
    intervals = CHORD_INTERVALS.get(scale.lower(), CHORD_INTERVALS["minor"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert sustained 9th chord
    root_midi = 48 + NOTE_MAP.get(key.capitalize(), 0) # Start around C3
    end_ppq = bars * beats_per_bar * 960 # 960 PPQ per quarter note
    
    for interval in intervals:
        note = root_midi + interval
        # Insert note lasting the entire duration of the item
        RPR.RPR_MIDI_InsertNote(take, False, False, 0, end_ppq, 0, note, velocity_base, True)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (ReaSynth) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # To make a filter sweep audible, we need harmonics. A pure sine wave cannot be filtered well.
    # Set Sine volume to 0.0 (Param 0) and Sawtooth volume to 1.0 (Param 1)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 1.0)
    # Increase attack slightly to avoid clicks (Param 4)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.1)

    # === Step 5: Add ReaEQ and Setup High-Pass Automation ===
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # By default, ReaEQ Band 1 is a Low Shelf. 
    # If we set its Gain (Param 1) to -inf (Normalized 0.0), it acts like a High-Pass filter.
    RPR.RPR_TrackFX_SetParamNormalized(track, eq_idx, 1, 0.0)
    
    # Get the envelope for ReaEQ Band 1 Frequency (Param 0)
    # create=True ensures the envelope lane is created if it doesn't exist
    env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)

    # Insert automation points for the sweep
    # Param 0 Normalized values: 0.0 is ~20Hz, 0.5 is ~1kHz, 1.0 is ~24kHz
    # We sweep from 0.0 to 0.65 to thin out the sound over time (a classic riser wash-out)
    
    # Start point at time 0.0, value 0.0, shape 5 (bezier curve for natural build)
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 0.0, 5, 0.2, False, True)
    
    # End point at the end of the item, value 0.65 (~3kHz), shape 0 (linear)
    RPR.RPR_InsertEnvelopePoint(env, item_length_sec, 0.65, 0, 0.0, False, True)
    
    # Sort envelope points to apply changes
    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}': {bars}-bar automated High-Pass filter sweep on a {key} {scale} 9th chord at {bpm} BPM."
```