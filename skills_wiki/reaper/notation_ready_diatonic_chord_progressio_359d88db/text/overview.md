### 1. High-level Design Pattern Extraction

**Skill Name**: Notation-Ready Diatonic Chord Progression

* **Core Musical Mechanism**: A highly quantized, descending diatonic chord progression (i - VII - VI - VII) designed specifically to render cleanly in standard musical notation/sheet music views. It utilizes a recognizable rhythmic syncopation (a half note followed by two quarter notes) that standard notation engines easily parse without generating cluttered tie or slur artifacts.
* **Why Use This Skill (Rationale)**: The tutorial focuses on REAPER's ability to instantly transcribe MIDI into its Musical Notation mode (Alt+4). For standard notation to be readable, MIDI data must align mathematically to the grid. This pattern encodes clear harmonic voice leading and strict metric subdivisions (1/2 and 1/4 notes), making it the perfect test case or backing track for sheet music extraction.
* **Overall Applicability**: This skill is highly applicable when generating backing keyboard tracks, creating sheet music for session musicians, or producing structured pop/classical chord foundations that are easily readable in the score editor. 
* **Value Addition**: Transforms a blank track into an instantly recognizable, notation-ready minor progression with smooth diatonic octave shifting and a synthesized timbre, explicitly demonstrating REAPER's transcription capabilities.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Rhythm Grid**: The pattern repeats every bar. Beat 1 features a half note (duration of 2 beats). Beats 3 and 4 feature quarter notes (duration of 1 beat each).
  - **Quantization**: Strictly quantized to ensure maximum readability in notation mode.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (Defaults to A minor, mirroring the tutorial's piano roll notes).
  - **Chord Progression**: i -> VII -> VI -> VII (e.g., Am -> G -> F -> G).
  - **Voicing**: Root position triads. The algorithm dynamically calculates negative scale degrees (VII and VI) and automatically shifts them down an octave, ensuring smooth, natural voice leading rather than jagged jumps.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` virtual instrument.
  - **FX Parameters**: Adjusted to sound like a digital Electric Piano/Organ hybrid. Mixes in Saw (0.5) and Square (0.2) waves, with a fast Attack (0.01) and moderate Release (0.3).

* **Step D: Mix & Automation**
  - Volume is set to a safe standard (0.7) within the ReaSynth plugin to prevent clipping.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track & Item Creation | `RPR_CreateNewMIDIItemInProj` | Automatically creates a container for notes at the current cursor position. |
| Harmonic Rhythm | `RPR_MIDI_InsertNote` | Precise start/end PPQ lengths ensure the MIDI displays as clean half/quarter notes in the notation editor. |
| Sound Design | `RPR_TrackFX_AddByName` / `SetParam` | Uses REAPER's native ReaSynth to emulate the "Keyboard" track heard in the tutorial. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly reproduces the style of MIDI input required to make REAPER's Musical Notation view shine, using native Python REAPER API functions.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard",
    bpm: int = 120,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a notation-ready diatonic chord progression in the current REAPER project.

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
        Status string describing what was created.
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
    qn_length = 60.0 / bpm
    bar_length = qn_length * 4
    
    start_pos = RPR.RPR_GetCursorPosition()
    end_pos = start_pos + (bar_length * bars)
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, start_pos, end_pos, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Notation-Ready MIDI ===
    formatted_key = key.capitalize()
    root_val = NOTE_MAP.get(formatted_key, 9) # Default to A
    root_midi = root_val + 48 # Octave 3 for keyboard voicing
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_diatonic_triad(degree):
        chord = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            scale_idx = degree + i
            # Handle negative indices cleanly for octave shifting
            octave_shift = scale_idx // len(scale_intervals)
            rem_idx = scale_idx % len(scale_intervals)
            note = root_midi + scale_intervals[rem_idx] + (octave_shift * 12)
            chord.append(note)
        return chord
        
    # Progression degrees: i - VII - VI - VII
    progression = [0, -1, -2, -1]
    
    notes_created = 0
    for bar_idx in range(bars):
        degree = progression[bar_idx % len(progression)]
        chord = get_diatonic_triad(degree)
        
        bar_start = start_pos + (bar_idx * bar_length)
        
        # Rhythm Grid: Half note (beats 1-3), Quarter note (beat 3), Quarter note (beat 4)
        rhythms = [
            (0, 2),       
            (2, 3),       
            (3, 4)        
        ]
        
        for qn_start, qn_end in rhythms:
            t_start = bar_start + (qn_start * qn_length)
            t_end = bar_start + (qn_end * qn_length)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, t_end)
            
            for note in chord:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, True)
                notes_created += 1
                
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Synthesizer FX Chain ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for an EPiano tone
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2)  # Square wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5)  # Saw wave mix
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.01) # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, 0, 10, 0.3) # Release (Moderate)

    return f"Created '{track_name}' with {notes_created} perfectly-quantized notes over {bars} bars at {bpm} BPM (Notation Ready)"
```