# Legato Walking Bassline (Octave-Pumping Groove)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Legato Walking Bassline (Octave-Pumping Groove)

* **Core Musical Mechanism**: The defining signature of this pattern is the combination of **strict 1/16th note quantization** with **legato note durations**, deliberately interspersed with manual staccato breaks (rests). Melodically, it relies on octave leaps (Root to Octave) and walking movements targeting the 5th and minor 6th degrees. This mimics the physical constraints and groove of a real bass player walking across the fretboard.

* **Why Use This Skill (Rationale)**: When programming MIDI bass, gaps between notes often sound unnatural because a real bassist continuously slides or rolls their fingers between frets. By forcing the MIDI notes to be perfectly legato (the end of one note touching the start of the exact next note), you create a smooth, continuous low-end foundation. Muting (trimming the note early) is then used intentionally as a rhythmic device to create bounce and syncopation, while 16th-note fills at the end of the phrase provide a turnaround into the next bar.

* **Overall Applicability**: This is a universal bass programming technique perfect for rock, funk, neo-soul, and pop. The specific Root-Octave-5th-6th groove is a classic motif that establishes a driving rhythm while leaving space for a snare drum.

* **Value Addition**: A raw MIDI recording often sounds sloppy and disjointed. This skill encodes the post-recording editing techniques demonstrated in the tutorial: snapping note starts to a strict 16th grid, extending note lengths for a legato "fretless" feel, creating rhythmic space, and using scale degrees to build an authentic walking turnaround fill.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 80 BPM (standard mid-tempo groove).
  - **Grid**: 1/16th notes, straight (no swing).
  - **Note Durations**: Predominantly 1/8th notes played *legato* (lengths perfectly extended to 0.5 beats so they touch). Strategic 1/16th note gaps are carved out before strong beats to simulate fret muting. Fills utilize rapid 1/16th notes.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: E Minor (as demonstrated), but adaptable to any key.
  - **Progression**:
    - Bar 1: Root (low) → Octave (high) → 5th → minor 6th.
    - Bar 2: Root → Octave → 5th → 4th → minor 3rd → 2nd, leading into a 16th-note turnaround fill.
  - **Register**: Octave 1 and 2 (e.g., E1 and E2). 

* **Step C: Sound Design & FX**
  - **Instrument**: While the tutorial uses the 3rd-party *Ample Bass P Lite II* VST, the core tonal characteristic is a Fender Precision Bass (P-Bass).
  - **Recreation**: This can be approximated using REAPER's native `ReaSynth` blended with a square/saw wave and heavily lowpass-filtered using `ReaEQ` (high-cut around 800 Hz) to remove the synthetic high-end "buzz", focusing entirely on the warm fundamental frequencies.

* **Step D: Mix & Automation**
  - Bass tracks are typically kept dead-center in the pan. 
  - (Optional) Randomizing MIDI velocity slightly between 90-110 helps sell the "live player" illusion, especially on the fast 16th-note fills.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bassline Groove & Fills | MIDI note insertion | Allows precise 16th-note quantization and exact programmatic control over *legato* vs *staccato* note durations. |
| Scale/Key Adaptability | Python Scale Arrays | Ensures the walking bassline stays perfectly in key while performing its turnaround walk-downs. |
| Tone Generation | FX Chain (`ReaSynth` + `ReaEQ`) | Provides a guaranteed, out-of-the-box reproducible bass tone without relying on the user having the 3rd-party Ample Sound VST installed. |

> **Feasibility Assessment**: 85% — The MIDI groove, legato editing technique, and turnaround fills are reproduced exactly as taught. The 15% difference is the lack of the Ample Sound VST (which provides hyper-realistic fret buzz and slide samples). A lowpassed ReaSynth is used as a highly functional native stand-in.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Walking Legato Bass",
    bpm: int = 80,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Legato Walking Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (must be > 0).
        velocity_base: Base MIDI velocity (0-127).
    
    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

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

    # Ensure inputs are valid
    if key not in NOTE_MAP:
        key = "E"
    if scale not in SCALES:
        scale = "minor"
    
    root_val = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    
    # Base octave for Bass is usually octave 1 or 2. We'll use C1 = 24.
    octave_offset = 24 

    def get_midi_pitch(degree: int, oct_shift: int = 0) -> int:
        """Get MIDI pitch for a given scale degree (0-based) and octave shift."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        pitch = root_val + scale_intervals[idx] + ((octave + oct_shift) * 12) + octave_offset
        return min(max(pitch, 0), 127)

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

    # Define the 2-bar Legato Walking Bass groove (Beat Start, Degree, Length in Beats, Octave Shift)
    # The length intentionally leaves exact 16th note (0.25) gaps in certain places for the "trimmed" fret mute feel.
    groove_pattern = [
        # --- BAR 1 ---
        (0.0, 0, 0.5, 0),   # Beat 1: Root (legato)
        (0.5, 0, 0.5, 1),   # Beat 1.5: Octave jump (legato)
        (1.0, 4, 0.5, 0),   # Beat 2: 5th (legato)
        (1.5, 5, 1.25, 0),  # Beat 2.5: Minor 6th (sustained, leaves a 0.25 16th-note gap before next beat!)
        (3.0, 4, 0.5, 0),   # Beat 4: 5th (legato)
        (3.5, 0, 0.5, 1),   # Beat 4.5: Octave jump (legato)
        
        # --- BAR 2 (Walkdown & Fill) ---
        (4.0, 0, 0.5, 0),   # Beat 1: Root (legato)
        (4.5, 0, 0.5, 1),   # Beat 1.5: Octave jump (legato)
        (5.0, 4, 0.5, 0),   # Beat 2: 5th (legato)
        (5.5, 3, 0.5, 0),   # Beat 2.5: 4th (walk down)
        (6.0, 2, 0.5, 0),   # Beat 3: 3rd (walk down)
        (6.5, 1, 0.5, 0),   # Beat 3.5: 2nd (walk down)
        
        # 16th note turnaround fill (staccato / fast)
        (7.0, 0, 0.25, 0),  # Beat 4.0
        (7.25, 1, 0.25, 0), # Beat 4.25
        (7.50, 2, 0.25, 0), # Beat 4.5
        (7.75, 4, 0.25, 0), # Beat 4.75
    ]

    # Populate MIDI Item
    note_count = 0
    pattern_length_beats = 8.0 # 2 bars
    
    for bar_pair in range((bars + 1) // 2): # Loop the 2-bar pattern to fill requested bars
        beat_offset = bar_pair * pattern_length_beats
        
        for start_b, degree, len_b, oct_shift in groove_pattern:
            abs_start_beat = beat_offset + start_b
            abs_end_beat = abs_start_beat + len_b
            
            # Stop if we exceed the total requested bars
            if abs_start_beat >= bars * beats_per_bar:
                continue
                
            # Clamp the last note so it doesn't bleed past the item
            if abs_end_beat > bars * beats_per_bar:
                abs_end_beat = bars * beats_per_bar

            # Calculate absolute project time and PPQ
            start_time = abs_start_beat * (60.0 / bpm)
            end_time = abs_end_beat * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = get_midi_pitch(degree, oct_shift)
            
            # Slight velocity humanization for the "live" feel
            vel = max(1, min(127, velocity_base + random.randint(-8, 5)))
            # Accent the downbeats slightly
            if start_b % 1.0 == 0:
                vel = min(127, vel + 10)
                
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (Stock Bass Tone Substitute) ===
    # Using ReaSynth to act as our DI Bass
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a warm bass tone (less saw, more pulse/sine, fast attack)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Vol
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.01)   # Attack (punchy)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.8)    # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 0.6)    # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 5, 0.1)    # Release (tight)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 6, 0.7)    # Square mix (adds P-bass growl)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 7, 0.1)    # Saw mix
    
    # Add ReaEQ to drastically lowpass the synth and boost the sub fundamental
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # Band 1: Sub boost
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 0, 0)         # Type: Low Shelf
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 1, 60.0)      # Freq: 60Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 2, 4.0)       # Gain: +4dB
    
    # Band 4: High Cut (removes synthetic top end to mimic flatwound strings)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 9, 5)         # Type: High Cut / Low Pass
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 10, 800.0)    # Freq: 800Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 11, 0.0)      # Gain: 0

    return f"Created '{track_name}' with {note_count} legato/quantized notes over {bars} bars at {bpm} BPM in {key} {scale}."
```