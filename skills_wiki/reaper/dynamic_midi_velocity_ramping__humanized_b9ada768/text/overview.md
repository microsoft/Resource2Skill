### 1. High-level Design Pattern Extraction

**Skill Name**: Dynamic MIDI Velocity Ramping (Humanized Swell / Crescendo)

* **Core Musical Mechanism**: The tutorial extensively covers creating notes in the REAPER MIDI Editor and specifically highlights manipulating the CC (Control Change) Lane at the bottom to adjust **Velocity**. The defining production technique extracted here is generating a sequence of notes (like a chord progression or arpeggio) and dragging a linear ramp across the velocity values. This creates a gradual volume and timbral swell (crescendo).
* **Why Use This Skill (Rationale)**: Drawing in MIDI notes with a mouse defaults every note to a static velocity (usually 100 or 127). Musically, this sounds robotic and lifeless. Acoustic instruments (especially pianos, strings, and drums) naturally vary in dynamics. Ramping velocities across a phrase simulates the physical effort of a player digging into the keys harder over time, creating emotional tension and momentum leading into a new downbeat or section.
* **Overall Applicability**: This technique is essential for piano ballads, cinematic string swells, EDM build-ups (snare rolls), and humanizing static hi-hat or shaker loops.
* **Value Addition**: Instead of just plunking down a static C-major chord, this skill encodes diatonic chord theory (I-IV-vi-V progression) and applies mathematical interpolation to the MIDI note velocities, providing a pre-configured, instantly expressive "swell" pattern.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 BPM (default, adjustable).
  - **Grid/Rhythm**: 8th-note driving rhythm. A 4-bar loop where chords are played repeatedly in 8th notes (8 strikes per bar, 32 total strikes).
  - **Note Duration**: Slightly detached (80% of an 8th note) to emphasize the rhythmic attack and make the velocity changes clearly audible.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Major (parametric).
  - **Chord Progression**: Diatonic I - IV - vi - V.
  - **Voicing Algorithm**: Uses an index-based diatonic expansion function to ensure that no matter the key or scale chosen, the 1st, 3rd, and 5th of that specific scale degree are correctly calculated and mapped to proper octaves.
* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` (Stock REAPER plugin used as a reliable fallback for the "Grand Piano" VSTi shown in the tutorial, ensuring 100% reproducibility on any system).
* **Step D: Mix & Automation**
  - **Automation**: The velocity of the notes ramps mathematically from a starting base (e.g., 40, very soft) to an ending peak (e.g., 115, very loud) over the 4-bar duration.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Progression | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise calculation of diatonic intervals and timing. |
| Velocity Humanization | Mathematical Interpolation | Accurately reproduces the "drag a line across the velocity lane" action shown in the video by linearly scaling the `vel` parameter. |
| Sound Generation | FX chain (`ReaSynth`) | Provides an immediate, stock-native auditory representation of the MIDI dynamics without requiring third-party VSTs. |

> **Feasibility Assessment**: 100% reproducible. While the tutorial uses a specific 3rd-party "Grand Piano" VSTi, the core educational concept (MIDI editing, chord creation, and velocity ramping) is perfectly reproduced using REAPER's native MIDI API and ReaSynth.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano Velocity Swell",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 40,
    velocity_end: int = 115,
    **kwargs,
) -> str:
    """
    Create a driving 8th-note chord progression with a smooth velocity ramp (crescendo).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Starting MIDI velocity (0-127).
        velocity_end: Ending MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    if key not in NOTE_MAP or scale not in SCALES:
        return f"Error: Unsupported key '{key}' or scale '{scale}'"

    root_val = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # Helper function to get exact pitch for diatonic chords (handles octave wrap-around)
    def get_pitch(degree, root, intervals, octave=4):
        octave_offset = degree // len(intervals)
        scale_degree = degree % len(intervals)
        return (octave + octave_offset) * 12 + root + intervals[scale_degree]

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add Instrument (ReaSynth) ===
    # Using ReaSynth as a universally available stand-in for the Piano VST
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    quarter_note_length = 60.0 / bpm
    bar_length_sec = quarter_note_length * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create MIDI Item (returns media item pointer)
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 4: Generate Rhythmic Progression & Velocity Ramp ===
    # Progression: I - IV - vi - V (expressed in scale degrees: 0, 3, 5, 4)
    # Each chord is built using the root, 3rd, and 5th relative to that degree
    chords = [
        [0, 2, 4], # I
        [3, 5, 7], # IV
        [5, 7, 9], # vi
        [4, 6, 8]  # V
    ]

    eighth_note_len = quarter_note_length / 2.0
    note_duration = eighth_note_len * 0.8  # 80% length for a slightly plucked/staccato feel
    total_steps = bars * 8
    notes_created = 0

    for bar in range(bars):
        # Loop through the progression
        chord_degrees = chords[bar % len(chords)]
        
        for eighth in range(8):
            step = bar * 8 + eighth
            
            # Linear interpolation for the velocity ramp (Crescendo)
            ramp_progress = step / max(1, total_steps - 1)
            current_velocity = int(velocity_base + (velocity_end - velocity_base) * ramp_progress)
            
            # Ensure velocity bounds
            current_velocity = max(1, min(127, current_velocity))

            start_time = step * eighth_note_len
            end_time = start_time + note_duration

            # Convert time to PPQ (Pulses Per Quarter Note) for MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Insert notes for the chord
            for degree in chord_degrees:
                pitch = get_pitch(degree, root_val, scale_intervals, octave=4)
                # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, current_velocity, True)
                notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM. Velocity ramps from {velocity_base} to {velocity_end}."
```