# High-level Design Pattern Extraction

> **Skill Name**: Viral R&B / Neo-Soul Bassline Formula

* **Core Musical Mechanism**: This pattern transforms a static, whole-note root bassline into a professional groove. It achieves this by introducing sixteenth-note syncopation (striking the off-beats at 2.5 and 3.5), jumping an octave to create a "bouncy" dynamic, and inserting a pentatonic passing shape (the Perfect 5th and Minor 7th) right before the end of the bar to voice-lead into the next chord transition.
* **Why Use This Skill (Rationale)**: A static bassline lacks momentum. The syncopation (playing on the "ands" of the beat) creates rhythmic interplay with the drum groove. The octave jumps provide necessary tonal variety without clashing with the foundational harmony. The use of the 5th and minor 7th as passing tones acts as a turnaround, pulling the listener forward and resolving strongly onto the downbeat of the subsequent bar.
* **Overall Applicability**: Ideal for R&B, Neo-Soul, Hip-Hop, Funk, and Lofi where the bass needs to drive the rhythmic pocket while maintaining a relatively simple harmonic foundation.
* **Value Addition**: This skill completely replaces flat, robotic MIDI clips with an idiomatic, genre-accurate rhythm and a built-in passing-tone vocabulary.

---

# Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 85 - 100 BPM (Default: 90)
  * **Time Signature**: 4/4
  * **Rhythm Grid**: 16th notes.
  * **Pattern**: 
    * Beat 1 (Downbeat): Quarter note length
    * Beat 2.5 (Off-beat / Syncopated): Eighth note length
    * Beat 3.5 (Off-beat / Syncopated): Eighth note length
    * Beat 4.0 (Downbeat): Eighth note length
    * Beat 4.5 (Off-beat): Eighth note length

* **Step B: Pitch & Harmony**
  * **Octave Range**: Sub/bass range (C2 - B2).
  * **Intervallic Formula (relative to current chord root)**:
    * Beat 1: Root
    * Beat 2.5: Octave (+12 semitones)
    * Beat 3.5: Root
    * Beat 4.0: Perfect 5th (+7 semitones)
    * Beat 4.5: Minor 7th (+10 semitones)

* **Step C: Sound Design & FX**
  * **Instrument**: ReaSynth
  * **Timbre**: A blend of Sine wave (for sub-frequency weight), Triangle wave (for warmth), and a small amount of Square wave (to add mid-range harmonics so the bass is audible on small speakers).
  * **Envelope**: Quick release time to ensure the syncopated notes remain "bouncy" and punchy without bleeding into each other.

* **Step D: Mix & Automation**
  * **Volume**: Reduced output to avoid clipping the master.
  * **Velocities**: Accented downbeats (100) with slightly pulled-back off-beats (85-95) to emphasize the groove.

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic syncopation & passing tones | MIDI note insertion | Gives absolute precision over timing, velocity, and dynamic offsets for the groove. |
| Pitch selection | Music Theory Arrays | Computes exact passing intervals dynamically based on scale and progression parameters. |
| Bass Timbre | FX chain (ReaSynth parameters) | Provides a clean, self-contained synth bass sound native to REAPER without requiring external VSTs. |

> **Feasibility Assessment**: 100% — The precise rhythmic grid, pitch intervallic logic, and foundational synthesizer settings demonstrated in the tutorial are fully reproducible using stock REAPER Python API functions.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Bass",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    progression: list = [4, 1], # Default scale degrees (iv -> i)
    **kwargs,
) -> str:
    """
    Create a 'Viral R&B/Neo-Soul Bassline Formula' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        progression: List of scale degrees to outline per bar (1-indexed).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Calculate Timing & Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }

    base_note = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    ppq_per_qn = 960

    # === Step 5: Insert MIDI Notes ===
    for bar in range(bars):
        bar_start_ppq = bar * ppq_per_qn * beats_per_bar
        chord_degree = progression[bar % len(progression)]
        
        # Calculate root pitch (Octave 2 for bass)
        deg_idx = (chord_degree - 1) % len(scale_intervals)
        octave_shift = (chord_degree - 1) // len(scale_intervals)
        semitones = scale_intervals[deg_idx]
        root_pitch = (2 + octave_shift + 1) * 12 + base_note + semitones

        # Formula Pattern: (start_qn, end_qn, pitch_offset, vel_offset)
        notes = [
            (0.0, 1.0, 0, 0),       # Beat 1: Root downbeat
            (1.5, 2.0, 12, -10),    # Beat 2.5: Octave jump syncopation
            (2.5, 3.0, 0, -5),      # Beat 3.5: Root syncopation
            (3.0, 3.5, 7, -15),     # Beat 4.0: Perfect 5th passing
            (3.5, 4.0, 10, -10),    # Beat 4.5: Minor 7th passing
        ]

        for start_qn, end_qn, pitch_offset, vel_offset in notes:
            start_ppq = int(bar_start_ppq + start_qn * ppq_per_qn)
            end_ppq = int(bar_start_ppq + end_qn * ppq_per_qn)
            pitch = max(0, min(127, root_pitch + pitch_offset))
            vel = max(1, min(127, velocity_base + vel_offset))
            
            # Insert note, deferring sort for performance
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Sort MIDI events after insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 6: Add Instrument FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a bouncy Neo-Soul Sub Bass
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.4)   # Volume (to prevent clipping)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.25)  # Square Mix (adds mid harmonics)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5)   # Triangle Mix (warmth)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.05)  # Quick Release (tightness)

    return f"Created '{track_name}' bassline over {bars} bars at {bpm} BPM in {key} {scale}"
```