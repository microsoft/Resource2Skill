# Asymmetrical Waveform Correction & Headroom Recovery

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetrical Waveform Correction & Headroom Recovery

* **Core Musical Mechanism**: Utilizing a phase rotator (all-pass filter) or a linear phase EQ to realign the phase relationship of harmonics within a sound. This corrects asymmetrical (lopsided) waveforms without altering the perceived frequency balance or tone.
* **Why Use This Skill (Rationale)**: Asymmetrical waveforms naturally occur in analog synthesizers, brass instruments, and vocal recordings due to high concentrations of even-order harmonics (2nd, 4th, etc.) combining constructively on one side of the zero-crossing. Additionally, standard "minimum phase" EQs introduce phase shifts in the low frequencies that can cause previously symmetrical waveforms to become lopsided. This eats up digital headroom, meaning your track will clip the mix bus sooner. Rotating the phase redistributes the peak energy symmetrically, allowing you to turn the track up significantly louder before hitting 0 dBFS.
* **Overall Applicability**: Essential for mixing heavy synth basses, sub-basses, brass sections, and voiceovers. It is particularly crucial in EDM, hip-hop, and pop where maximizing low-end loudness and limiting headroom is a priority. 
* **Value Addition**: Compared to just dropping in an EQ or limiter (which would squarify and distort the lopsided peaks), this encoded knowledge preserves the exact sound of the instrument while mathematically optimizing its shape for the digital mixing environment. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Driving 1/8th note pattern, standard in synthwave, electro, or pop. 
  - **Duration**: Slightly staccato (e.g., 80% gate length) to allow the waveform to breathe and clearly show the peak levels between hits.
* **Step B: Pitch & Harmony**
  - **Register**: Deep bass register (C1 to C2 range, roughly 30-60 Hz) where asymmetric peaks and DC offset cause the most headroom damage.
  - **Pattern**: Emphasizes the root note of the chosen scale with octave jumps on the weak beats to trigger varying harmonic responses.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` (providing the raw waveforms).
  - **Standard EQ Risk**: A standard low-shelf or high-pass (like `ReaEQ`) is known to tilt the phase and create lopsided waveforms.
  - **The Fix (FX Chain)**: `JS: Phase Rotator` is inserted at the end of the chain. Adjusting it by 10 to 15 degrees shifts the fundamental and harmonics just enough to mirror the top and bottom peaks, reclaiming lost headroom.
* **Step D: Mix & Automation**
  - The limiter/compressor threshold can now be pushed deeper because the peaks are evenly distributed.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Driving Bass Rhythm | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides the raw, consistent sub-bass signal required to demonstrate and manage headroom. |
| The Asymmetry Fix | FX Chain (`JS: Phase Rotator`) | Directly replicates the tutorial's methodology of applying an all-pass filter to rotate the phase and center the waveform's peak energy. |
| Tone Generation | FX Chain (`ReaSynth` -> `ReaEQ`) | Creates the bass tone and simulates the phase-shifting conditions of standard minimum-phase EQ processing. |

> **Feasibility Assessment**: 100%. The code dynamically generates a synth bassline and applies the exact REAPER-native tools (JS Phase Rotator) demonstrated in the tutorial to correct potential waveform asymmetry.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Phase_Corrected_Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a driving synth bass track equipped with a Phase Rotator to 
    correct asymmetrical waveforms and maximize digital headroom.

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
    import reaper_python as RPR

    # === Music Theory & Pitch Logic ===
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
    
    # Calculate root MIDI note (register: C1-C2 for sub bass)
    root_val = NOTE_MAP.get(key, 0)
    base_midi_note = 24 + root_val # 24 is C1
    scale_intervals = SCALES.get(scale, SCALES["minor"])

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
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate 1/8th Note Driving Bassline ===
    notes_added = 0
    total_eighth_notes = bars * 8
    eighth_note_len = bar_length_sec / 8.0
    
    for i in range(total_eighth_notes):
        start_time = i * eighth_note_len
        # Staccato feel (80% gate length)
        end_time = start_time + (eighth_note_len * 0.8) 
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Pitch pattern: Root note mostly, jump up an octave on every 4th 8th-note
        pitch = base_midi_note
        if (i + 1) % 4 == 0:
            pitch += 12 # Octave jump
            
        # Slight velocity humanization
        vel = velocity_base if i % 2 == 0 else max(10, velocity_base - 15)

        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    # 1. Tone Generation (ReaSynth)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Standard EQ (ReaEQ) - High Pass filtering which typically shifts phase in low end
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # 3. THE FIX: Phase Rotator to realign harmonics and correct asymmetry
    rotator_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Phase Rotator", False, -1)
    
    # Set JS: Phase Rotator Phase Adjustment to ~11 degrees as demonstrated in the tutorial
    # Parameter 0 is Phase Adjustment (deg)
    RPR.RPR_TrackFX_SetParam(track, rotator_idx, 0, 11.0)

    return f"Created '{track_name}' with {notes_added} driving bass notes over {bars} bars. JS Phase Rotator applied to maximize headroom."
```