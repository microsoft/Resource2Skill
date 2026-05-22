# Complementary Frequency Puzzling (EQ Masking Relief)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Complementary Frequency Puzzling (EQ Masking Relief)

* **Core Musical Mechanism**: The defining technique shown in this tutorial is using Equalization (EQ) not to alter a single sound's tone in isolation, but to "fit sounds together like a puzzle." Specifically, the creator addresses frequency masking by carving out defined spaces for different instruments: placing a High-Pass filter on mid/high-frequency instruments (like pianos/synths) and a Low-Pass filter on low-frequency instruments (like bass). 

* **Why Use This Skill (Rationale)**: When multiple instruments contain energy in the same frequency range (e.g., both a piano and a bass pushing 150-300Hz), they clash. Psychoacoustically, this creates a "muddy" or "boomy" mix where neither instrument has clarity. By carving a rigid boundary line (a crossover point, often between 150Hz and 300Hz), the fundamental weight of the bass is preserved, and the clarity/texture of the chords can cut through effortlessly without fighting for headroom.

* **Overall Applicability**: This is a mandatory foundational step in mixing nearly every modern music genre—ranging from EDM and hip-hop to pop and rock. It is particularly crucial when dealing with thick synth layers, wide pianos, or heavily distorted basslines that possess aggressive harmonics.

* **Value Addition**: Compared to just throwing MIDI loops together, this skill encodes the actual mixing geometry required to make a track sound professional. It automatically establishes a balanced low-end/mid-range relationship out of the box.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM:** Variable (typically 100-130 for the demonstrated styles).
  - **Rhythm:** Block chords and foundational bass notes played simultaneously. This overlapping rhythm explicitly forces the frequencies to clash, making the EQ cuts functionally necessary.
  - **Grid:** 1 bar per chord/bass note to provide a sustained test for frequency masking.

* **Step B: Pitch & Harmony**
  - **Harmony:** A standard progression (I - V - vi - IV) demonstrating harmonic stacking.
  - **Bass:** Root notes living entirely in Octave 2 (sub/bass frequencies).
  - **Chords:** Root position triads living in Octave 4 (mid/high frequencies).

* **Step C: Sound Design & FX**
  - **Instrument:** Simple subtractive synthesis (e.g., ReaSynth saw/square waves) to generate a rich harmonic spectrum that naturally clashes.
  - **EQ Strategy:** 
    - *Bass Track:* Low-Pass filter applied at ~300Hz to remove harsh upper-harmonics and strictly reserve the low-end.
    - *Chords Track:* High-Pass filter applied at ~300Hz to remove unnecessary low-end rumble that would mask the bass.

* **Step D: Mix & Automation**
  - Static EQ cuts are established. In the tutorial, the creator manually sweeps to find these clash points; we will procedurally assign a clean crossover frequency (300Hz) to automate the puzzle-fitting process.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Instrument separation | Track creation & Routing | Required to process the bass and chords with independent EQ chains. |
| Harmony / Clash generation | MIDI note insertion | Generating overlapping MIDI notes ensures we have sustained sound energy to demonstrate the EQ puzzle technique. |
| "Puzzle Fitting" EQ | JSFX (`JS: Filters/highpass` & `lowpass`) | REAPER's stock JSFX filters take exact un-normalized Hz values, allowing us to precisely set the mathematical crossover point (300Hz) reliably across all REAPER installations without VST UI limitations. |

> **Feasibility Assessment**: 100% reproducible for the core concept. While the specific third-party VSTs (Serum, Kontakt guitars) shown in the video are not used, the underlying physics of frequency masking and the REAPER-native application of high-pass/low-pass filters are perfectly reconstructed using native tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EQ_Puzzle",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates two tracks (Bass and Chords) demonstrating the complementary EQ "puzzle" technique.
    Applies a Lowpass filter to the Bass and a Highpass filter to the Chords at a shared crossover frequency.
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

    base_note = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    # Helper function to compute pitch dynamically from scale degrees
    def get_pitch(degree, oct):
        scale_len = len(scale_intervals)
        oct_offset = degree // scale_len
        idx = degree % scale_len
        return base_note + (oct + oct_offset) * 12 + scale_intervals[idx]

    # === Step 1: Initialize Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Core I-V-vi-IV (0-indexed degrees: 0, 4, 5, 3)
    progression = [0, 4, 5, 3]

    # === Step 2: Create Bass Track (The Low-End Puzzle Piece) ===
    idx_bass = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_bass, True)
    track_bass = RPR.RPR_GetTrack(0, idx_bass)
    RPR.RPR_GetSetMediaTrackInfo_String(track_bass, "P_NAME", f"{track_name}_Bass", True)

    # Setup Bass Sound & FX
    RPR.RPR_TrackFX_AddByName(track_bass, "ReaSynth", False, -1)
    bass_eq = RPR.RPR_TrackFX_AddByName(track_bass, "JS: Filters/lowpass", False, -1)
    # Param 0 in JS: Filters/lowpass is cutoff frequency in Hz
    RPR.RPR_TrackFX_SetParam(track_bass, bass_eq, 0, 300.0) 

    item_bass = RPR.RPR_AddMediaItemToTrack(track_bass)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_bass, "D_LENGTH", total_length_sec)
    take_bass = RPR.RPR_AddTakeToMediaItem(item_bass)

    # === Step 3: Create Chords Track (The High-End Puzzle Piece) ===
    idx_chords = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_chords, True)
    track_chords = RPR.RPR_GetTrack(0, idx_chords)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)

    # Setup Chords Sound & FX
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    chord_eq = RPR.RPR_TrackFX_AddByName(track_chords, "JS: Filters/highpass", False, -1)
    # Param 0 in JS: Filters/highpass is cutoff frequency in Hz
    RPR.RPR_TrackFX_SetParam(track_chords, chord_eq, 0, 300.0)

    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", total_length_sec)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)

    # === Step 4: Generate Complementary MIDI ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        start_sec = bar * bar_length_sec
        end_sec = start_sec + bar_length_sec

        # Convert timing to PPQ for both takes
        start_ppq_b = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, start_sec)
        end_ppq_b   = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_bass, end_sec)
        start_ppq_c = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, start_sec)
        end_ppq_c   = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, end_sec)

        # 4a. Insert Bass Note (Octave 2)
        b_pitch = get_pitch(degree, 2)
        RPR.RPR_MIDI_InsertNote(take_bass, False, False, start_ppq_b, end_ppq_b, 0, b_pitch, velocity_base, True)

        # 4b. Insert Chord Notes (Root, 3rd, 5th in Octave 4)
        chord_pitches = [
            get_pitch(degree, 4),
            get_pitch(degree + 2, 4),
            get_pitch(degree + 4, 4)
        ]
        
        for p in chord_pitches:
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq_c, end_ppq_c, 0, p, int(velocity_base * 0.8), True)

    # === Step 5: Finalize & Sort ===
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_UpdateArrange()

    return f"Created Bass (Lowpass @ 300Hz) and Chords (Highpass @ 300Hz) tracks over {bars} bars at {bpm} BPM."
```