# Foundational MIDI Track & Channel Strip Setup

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Foundational MIDI Track & Channel Strip Setup

* **Core Musical Mechanism**: The tutorial demonstrates the foundational workflow for music production in a DAW: establishing a MIDI instrument track, creating a MIDI region, and immediately applying a basic "channel strip" (a Low-Pass EQ to tame harsh high frequencies, and a Compressor to control dynamics). While the video draws random notes to demonstrate the piano roll, this skill encodes a functional, foundational 4-bar chord progression (I - V - vi - IV) to provide immediate musical utility alongside the mix setup.
* **Why Use This Skill (Rationale)**: Unprocessed digital synths and virtual instruments often contain excessive high-frequency content and inconsistent dynamics. By habitually adding a low-pass filter (or high-shelf cut) and a baseline compressor (as demonstrated with ReaEQ and ReaComp), you immediately "seat" the instrument better in the mix, leaving room for vocals, cymbals, and other high-frequency elements.
* **Overall Applicability**: This is the universal starting point for any MIDI-based harmonic element—pianos, pads, synth leads, or strings. It is the blank canvas setup required before detailed composition and mixing can occur.
* **Value Addition**: Instead of a completely empty project, this skill provides a mix-ready starting point. It generates a mathematically correct chord progression mapped to your chosen key/scale, automatically loads a synthesizer, and configures the essential mixing plugins (EQ and Compression) to save setup time.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: 4/4 time, default 120 BPM.
  - **Rhythm**: Block chords playing on the downbeat of each bar (whole notes).
  - **Duration**: 4 bars (one chord per bar).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (Defaults to C Major).
  - **Progression**: Classic Pop/Rock I - V - vi - IV progression.
  - **Voicing**: Root position triads constructed dynamically based on the selected scale's intervals.

* **Step C: Sound Design & FX**
  - **Instrument**: ReaSynth (used as a stock substitute for the third-party Piano VST shown in the video).
  - **EQ (ReaEQ)**: Taming high frequencies (simulating the low-pass filter shown). Band 4 (High) gain is reduced to smooth out the digital harshness.
  - **Compression (ReaComp)**: Basic dynamic control. Ratio set to 3:1, Threshold lowered to catch peaks.

* **Step D: Mix & Automation**
  - **Volume**: Track volume is initialized to -6.0 dB to ensure proper gain staging and prevent master bus clipping.
  - **Panning**: Center.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Creation | `RPR_InsertTrackAtIndex` | Safely adds a new track without overwriting existing project elements. |
| Harmony Generation | `RPR_MIDI_InsertNote` | Allows precise, programmatic creation of a chord progression based on music theory data. |
| FX Chain | `RPR_TrackFX_AddByName` | Loads stock REAPER plugins (ReaSynth, ReaEQ, ReaComp) to replicate the tutorial's mixing chain. |
| Mix Tweaking | `RPR_TrackFX_SetParam` | Sets specific EQ cuts and Compression thresholds to mirror the tutorial's mixing moves. |

> **Feasibility Assessment**: 90%. The structural workflow, MIDI integration, and mixing chain are perfectly reproduced. Because standard REAPER does not include a native Grand Piano VST, `ReaSynth` is used as the sound generator, which produces a simpler electronic tone rather than an acoustic piano.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano/Synth Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Foundational MIDI Track & Channel Strip Setup in REAPER.
    
    Generates a 4-bar block chord progression with a pre-configured 
    synthesizer, EQ, and Compressor chain.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (4 is recommended for the progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    # Ensure valid key and scale
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    octave_base = 48 # C3
    root_midi = octave_base + root_val

    # Helper function to get a MIDI note for a specific scale degree (0-indexed)
    def get_scale_note(degree):
        octave_shift = degree // 7
        interval = scale_intervals[degree % 7]
        return root_midi + (octave_shift * 12) + interval

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Gain stage: Set track volume to -6dB (approx 0.5 in REAPER's amplitude scale)
    vol_amp = 10 ** (-6.0 / 20.0)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol_amp)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Define a basic progression: I - V - vi - IV (degrees 0, 4, 5, 3)
    progression = [0, 4, 5, 3]
    
    total_notes_inserted = 0
    
    # Insert chords
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Build a triad (root, third, fifth relative to the scale degree)
        chord_degrees = [degree, degree + 2, degree + 4]
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec - 0.05 # slight gap between chords
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for chord_degree in chord_degrees:
            pitch = get_scale_note(chord_degree)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), False)
            total_notes_inserted += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    
    # 1. Virtual Instrument (ReaSynth)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a softer, more pad/piano-like attack and decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.2)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.4)   # Release

    # 2. Equalization (ReaEQ)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Tame the high frequencies (simulating the Low-Pass from tutorial)
    # Band 4 (High Shelf) Gain is Param 10. Cut by -8dB.
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 10, -8.0) 

    # 3. Compression (ReaComp)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Param 0: Threshold (-12 dB)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -12.0)
    # Param 1: Ratio (3.0 : 1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 3.0)
    # Param 2: Attack (10 ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 10.0)
    # Param 3: Release (100 ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 100.0)

    return f"Created '{track_name}' with {total_notes_inserted} notes (I-V-vi-IV progression) over {bars} bars at {bpm} BPM in {key} {scale}. Loaded ReaSynth + EQ + Comp."
```