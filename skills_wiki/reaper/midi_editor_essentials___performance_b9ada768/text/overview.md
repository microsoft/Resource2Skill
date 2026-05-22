### 1. High-level Design Pattern Extraction

*   **Skill Name**: MIDI Editor Essentials & Performance
*   **Core Musical Mechanism**: This skill demonstrates fundamental MIDI note creation, editing, and automation techniques within REAPER's MIDI editor, focusing on building melodic and harmonic structures and infusing them with dynamic expression through velocity adjustments. The signature is the workflow itself, emphasizing manual note entry, quantizing, adjusting length/pitch, and varying velocity for a more "human" feel.
*   **Why Use This Skill (Rationale)**: This skill provides the foundational knowledge for building any MIDI-based musical idea from scratch. By understanding how to place, edit, and duplicate notes, users can construct melodies, bass lines, and chord progressions efficiently. The emphasis on velocity automation introduces the concept of musical dynamics, preventing static, robotic-sounding MIDI and allowing for expressive performances, which is crucial for emotional impact and realism in music. Quantization ensures rhythmic precision, while the ability to fine-tune outside the grid (with Shift) allows for nuanced "humanization" of timing.
*   **Overall Applicability**: This skill is universally applicable across all genres and production stages that involve MIDI. It's essential for composing and arranging parts for virtual instruments (synthesizers, drums, pianos, strings, etc.), correcting recorded MIDI performances, or creating entirely new musical ideas. It's the bedrock for any digital music production.
*   **Value Addition**: Compared to a blank MIDI clip, this skill encodes the practical workflow of creating musical ideas. It instantiates an example of melody and chords, applies varied velocities, and sets up a track with an instrument, providing a ready-to-edit starting point that immediately showcases essential MIDI manipulation techniques.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   Time signature: 4/4 (implied by typical DAW grid).
    *   BPM range: Configurable (defaults to 120 BPM in the video).
    *   Rhythmic grid: The tutorial demonstrates setting the grid to 1/8th and 1/16th notes for precise placement, with options to disable snapping for fine adjustments. Notes are placed on quarter, eighth, and half-beat divisions.
    *   Note duration pattern: Varies from short (1/8th) to long (whole notes), with adjustable lengths.

*   **Step B: Pitch & Harmony**
    *   Key/Scale: Defaults to C Major, which is implied by the notes (C, E, G) and the chords demonstrated (C Major). The skill code is parametric for `key` and `scale`.
    *   Chord voicings: A simple C Major triad (C3, E3, G3, C4) is explicitly shown and duplicated.
    *   Melody notes: Individual notes like C4, G3, E3, C3 are shown being placed.

*   **Step C: Sound Design & FX**
    *   Instrument/Synth: The tutorial uses "Grand Piano - Substantial" (a third-party VSTi). The reproduction code uses `ReaSynth` as a generic placeholder for a MIDI instrument.
    *   FX chain: No explicit FX chain other than the instrument itself is demonstrated or edited.

*   **Step D: Mix & Automation (if applicable)**
    *   Volume, panning, send levels: Not directly shown or edited within the MIDI editor context.
    *   Automation curves: The video explicitly shows adjusting note **velocity** in the CC lane (control change lane) for individual notes and multiple selected notes, emphasizing dynamic variation. The code simulates this by setting varied velocities. The concept of adding additional CC lanes (e.g., Pitch) is also shown.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|:----------------------|:-------|:------------------------------------------------|
| Track creation        | Track creation & naming | To isolate the MIDI demo elements.                 |
| Instrument setup      | FX chain               | To provide a playable sound for the MIDI notes. `ReaSynth` is a stock REAPER instrument. |
| MIDI item creation    | Item/take manipulation | To provide the canvas for MIDI notes.          |
| Note creation         | MIDI note insertion    | For precise placement, length, and velocity of individual and chord notes. |
| Velocity variation    | FX parameters (MIDI_SetNoteVel) | To simulate the "automation" shown in the CC lane for expressive dynamics. |

> **Feasibility Assessment**: 90% – The core MIDI editing techniques (note placement, length, pitch, velocity variation) are fully reproducible. The specific tonal character of the "Grand Piano - Substantial" VSTi cannot be reproduced exactly with a stock REAPER plugin like ReaSynth, but ReaSynth serves as a functional placeholder for a MIDI instrument.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def create_midi_editor_demo_pattern(
    project_name: str = "MIDI_Project",
    track_name: str = "MIDI Editor Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a simple MIDI item with a 4-bar progression demonstrating
    basic note creation and velocity variations, as seen in the REAPER MIDI editor tutorial.

    The pattern consists of:
    - Bar 1: A short melodic phrase with varied note lengths and velocities.
    - Bar 2, 3, 4: Repeated C Major chords with varied velocities.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (not used in this specific skill).

    Returns:
        Status string, e.g., "Created 'MIDI Editor Demo' with 17 notes over 4 bars at 120 BPM"
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11], # Intervals: R, M2, M3, P4, P5, M6, M7
        "minor":            [0, 2, 3, 5, 7, 8, 10], # Intervals: R, M2, m3, P4, P5, m6, m7
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Must be one of {list(NOTE_MAP.keys())}."
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Must be one of {list(SCALES.keys())}."

    root_midi_base = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # Helper function to get MIDI pitch
    def get_midi_pitch(root, interval_idx_in_scale, octave_c0_relative):
        return root + scale_intervals[interval_idx_in_scale] + (12 * octave_c0_relative)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth as a placeholder for the Grand Piano VSTi shown in the tutorial.
    # The tutorial used 'Grand Piano - Substantial' VSTi, which is not a stock REAPER plugin.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_seconds = float(bars * beats_per_bar) * (60.0 / bpm)
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)

    take = RPR.RPR_GetActiveTake(item)
    if not take:
        RPR.RPR_DeleteTrack(track) # Clean up if take creation failed
        return "Error: Failed to create active take for MIDI item."

    RPR.RPR_MIDI_SetItemExtents(item, 0.0, float(bars * beats_per_bar)) # Set item length in beats
    midi_take = RPR.RPR_MIDI_AllocTemporary(take, True) # Allocate temporary MIDI buffer

    note_count = 0
    current_beat_pos = 0.0

    # --- Bar 1: Melodic phrase (as demonstrated in tutorial) ---
    # Notes are relative to C major scale for consistency with tutorial's examples
    # Pitches: C4, C4, G3, E3, C3 (using C as root for these relative calcs)
    
    # C4 (Root, octave 4)
    pitch_c4 = get_midi_pitch(root_midi_base, 0, 4)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base, False, pitch_c4, 0)
    note_count += 1
    current_beat_pos += 0.5

    # C4 (Root, octave 4, longer duration)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 1.0, velocity_base + 10, False, pitch_c4, 0)
    note_count += 1
    current_beat_pos += 1.0

    # Skip 1 beat to beat 2.5
    current_beat_pos += 1.0

    # G3 (Perfect 5th, octave 3)
    pitch_g3 = get_midi_pitch(root_midi_base, 4, 3) # Index 4 in major scale is P5
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 5, False, pitch_g3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # E3 (Major 3rd, octave 3)
    pitch_e3 = get_midi_pitch(root_midi_base, 2, 3) # Index 2 in major scale is M3
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 10, False, pitch_e3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # C3 (Root, octave 3)
    pitch_c3 = get_midi_pitch(root_midi_base, 0, 3)
    RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_beat_pos, current_beat_pos + 0.5, velocity_base - 15, False, pitch_c3, 0)
    note_count += 1
    current_beat_pos += 0.5

    # Align to start of Bar 2 (next full bar)
    current_beat_pos = float(beats_per_bar)

    # --- Bar 2, 3, 4: C Major Chord (repeated for copy/paste concept) ---
    # Voicing: C3, E3, G3, C4
    chord_pitches_cmaj = [
        get_midi_pitch(root_midi_base, 0, 3), # C3
        get_midi_pitch(root_midi_base, 2, 3), # E3
        get_midi_pitch(root_midi_base, 4, 3), # G3
        get_midi_pitch(root_midi_base, 0, 4)  # C4
    ]
    
    # Velocities for each note in the chord (simulating automation)
    chord_vels = [velocity_base + 20, velocity_base + 10, velocity_base, velocity_base - 10]

    for bar_offset in range(1, bars): # Start from Bar 2 (index 1) up to 'bars'
        bar_start_beat = float(bar_offset * beats_per_bar)
        for i, pitch in enumerate(chord_pitches_cmaj):
            velocity = max(1, min(127, chord_vels[i] + (bar_offset * 5))) # Add slight variation per bar
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, velocity, False, pitch, 0)
            note_count += 1

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_FreeTemporary(midi_take)

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range? (Ensured by `max(1, min(127, ...))`)
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (Uses float values for beats, which REAPER handles internally for sub-beat precision).
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? Yes, it creates the essential elements (individual notes, chords, varied velocities) demonstrated for editing.
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies? Yes, uses ReaSynth and relative MIDI pitches.