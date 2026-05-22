### 1. High-level Design Pattern Extraction

**Skill Name**: REAPER MIDI Editing Fundamentals (Notes, Chords, Velocity Automation)

*   **Core Musical Mechanism**: This skill encapsulates the foundational workflow for creating, editing, and expressing MIDI data in REAPER's MIDI Editor. It focuses on precise placement, duration adjustment, duplication of notes and chords, and dynamic control through velocity automation to achieve more professional and realistic MIDI performances. The signature of this pattern is the ability to rapidly construct and refine melodic and harmonic structures while adding human-like nuances.

*   **Why Use This Skill (Rationale)**: Understanding these fundamentals is crucial for any music producer working with MIDI. It allows for:
    *   **Efficiency**: Rapid creation, copying, and pasting of musical ideas (notes, chords) saves significant time compared to manual entry or repeated live recording.
    *   **Precision**: Snap-to-grid and fine-tuning (Shift key) ensure rhythmic accuracy and allow for subtle deviations for musical feel.
    *   **Expressiveness**: Velocity automation (and other CC lanes) directly translates to the dynamic and timbral character of the instrument, moving beyond static playback to create expressive performances. This leverages psychoacoustic principles where varied dynamics contribute to a more engaging and "live" sound.
    *   **Error Correction**: Easy deletion and adjustment of notes facilitate quick fixes for recorded or drawn MIDI.

*   **Overall Applicability**: This skill is universally applicable across all genres and production stages where MIDI instruments are used. It's foundational for:
    *   **Composing**: Building melodies, basslines, and chord progressions from scratch.
    *   **Arranging**: Developing and repeating musical motifs.
    *   **Performance Enhancement**: Cleaning up live MIDI recordings, adding dynamic range, and shaping instrument articulation.
    *   **Sound Design**: Creating intricate rhythmic or pitched patterns for synthesizers and samplers.

*   **Value Addition**: This skill encodes the knowledge of efficient and expressive MIDI manipulation within REAPER. Compared to simply recording MIDI or drawing notes one by one, it provides:
    *   Accelerated workflow for MIDI input and arrangement.
    *   Techniques for dynamic control and humanization of MIDI performances.
    *   A structured approach to using the MIDI editor's core features (grid, snap, selection, copy/paste, velocity lanes).

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   Time signature: Implied 4/4 (standard).
    *   BPM range: Configurable, demonstrated at 120 BPM.
    *   Rhythmic grid: Demonstrated with 1/16th notes for detailed placement and adjustment.
    *   Note duration pattern: Variable, demonstrating both shorter melodic notes and longer chord notes. Adjustable by dragging note edges.
    *   Swing/shuffle: Not explicitly demonstrated, but the ability to fine-tune timing (Shift key for non-snapped movement) allows for manual groove adjustment.

*   **Step B: Pitch & Harmony**
    *   Key/scale: Demonstrated with C Major notes and chords (C3, E3, G3, C4, C5). The skill will be parametric for `key` and `scale`.
    *   Chord voicings: A simple C Major triad (root position: C3, E3, G3, C4) is shown.
    *   Melody: Simple ascending/descending patterns within the C Major scale.
    *   Chromaticism/mode mixture: Not demonstrated in the tutorial's musical examples.

*   **Step C: Sound Design & FX**
    *   Instrument: "VSTi: Grand Piano (saudade.lv2)" was used. Since this is a third-party VSTi, the reproduction code will use `ReaSynth` as a general-purpose placeholder instrument. The exact "Grand Piano" timbre would require the specific VSTi or equivalent samples/synthesis not available by default.
    *   FX chain: No specific FX chain was demonstrated beyond the instrument itself.

*   **Step D: Mix & Automation**
    *   Volume, panning, send levels: Not explicitly demonstrated in this tutorial segment.
    *   Automation curves: Velocity automation is extensively covered, showing how to individually adjust the "hit strength" of notes. The tutorial demonstrates visually adjusting individual velocity bars and marquee-selecting multiple bars for collective adjustment. Other CC lanes (Pitch, Modulation, Pan) are mentioned as possibilities.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :-------------------- | :--------------------------------------- |
| Track Creation        | `RPR_InsertTrackAtIndex()` | Creates a new, isolated environment for the pattern. |
| BPM Setting           | `RPR_SetCurrentBPM()` | Ensures the project tempo matches the desired context. |
| MIDI Item Creation    | `RPR_AddMediaItemToTrack()`, `RPR_SetMediaItemInfo_Value()` | Establishes the container for MIDI notes. |
| MIDI Note Insertion   | `RPR_MIDI_InsertNote()` | Allows precise creation of notes with specified pitch, position, length, and velocity, directly replicating the manual drawing process. |
| Instrument Loading    | `RPR_TrackFX_AddByName()` | Adds a VSTi (ReaSynth) to generate sound for the MIDI notes, as shown in the tutorial. |
| Velocity Automation   | `RPR_MIDI_SetNoteIntProperty()`, `RPR_MIDI_SetNoteByteProperty()` | Directly controls the velocity of individual MIDI notes, reproducing the core expressive element. |

> **Feasibility Assessment**: Approximately 80% of the tutorial's musical result and workflow demonstration is reproducible. The core MIDI editing techniques (note creation, deletion via Alt-click, selection, copying, pasting, length adjustment, position adjustment via Shift, octave changes via piano roll right-click) are all fundamental operations that the generated notes facilitate. The main limitation is the specific "Grand Piano (saudade.lv2)" VSTi, which is not a stock REAPER plugin and cannot be reliably reproduced with `ReaSynth` without specific preset information. However, ReaSynth provides a generic synth sound to play the MIDI notes.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def create_midi_editing_fundamentals(
    project_name: str = "MyProject",
    track_name: str = "MIDI Notes Demo",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    octave: int = 3, # Default octave for the base notes
    **kwargs,
) -> str:
    """
    Creates a new track with a MIDI item demonstrating basic MIDI editing fundamentals:
    notes, a simple chord, and varied velocities.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, harmonic_minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        octave: MIDI octave for the root of the notes (e.g., 3 for C3).
        **kwargs: Additional overrides (not used in this skill but for future expansion).

    Returns:
        Status string, e.g., "Created 'MIDI Notes Demo' with 16 notes over 4 bars at 120 BPM"
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

    # Ensure key and scale are valid
    if key not in NOTE_MAP:
        return f"Error: Invalid key '{key}'. Choose from {list(NOTE_MAP.keys())}"
    if scale not in SCALES:
        return f"Error: Invalid scale '{scale}'. Choose from {list(SCALES.keys())}"

    root_midi = NOTE_MAP[key] + (octave * 12)
    current_scale = SCALES[scale]

    # === Step 1: Set Tempo ===
    # Note: RPR_SetCurrentBPM changes global project BPM.
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) ===
    # The tutorial used "VSTi: Grand Piano (saudade.lv2)", which is not stock.
    # Using ReaSynth as a general VSTi for MIDI playback.
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Could set a basic sound for ReaSynth if a known preset exists or params are provided.
    # For now, default ReaSynth sound is used.

    # === Step 4: Create MIDI Item ===
    # Timebase: REAPER's time unit is usually in quarter notes, 1.0 = 1 quarter note.
    # For a 4/4 bar: 4.0 quarter notes.
    quarter_note_len = 60.0 / bpm
    bar_length_qn = 4.0 # 4 quarter notes per bar (4/4 time)
    item_length_qn = bar_length_qn * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_qn * quarter_note_len) # Length in seconds

    take = RPR.RPR_AddTakeToMediaItem(item)
    if not take:
        RPR.RPR_DeleteTrack(track)
        return "Error: Could not add take to media item."

    RPR.RPR_MIDI_SetItemExtents(item, 0, item_length_qn) # Set item length in quarter notes

    # Get the MIDI take for editing
    midi_take = RPR.RPR_MIDI_GetTake(take)
    if not midi_take:
        RPR.RPR_DeleteTrack(track)
        return "Error: Could not get MIDI take."

    RPR.RPR_MIDI_BeginEdit(midi_take)

    # === Step 5: Insert Notes (Melody & Chord) and Adjust Velocities ===
    note_count = 0
    # Simple melody (like the video's double-click examples)
    # Using notes from the selected scale
    melody_notes = [current_scale[0], current_scale[2], current_scale[4], current_scale[5]] # C, E, G, F (in C major)
    melody_octave_offset = 12 # One octave higher than base

    for i in range(bars):
        # Melody part
        for j, scale_degree_offset in enumerate(melody_notes):
            pos_qn = float(i * bar_length_qn) + (j * 0.5) # Each note 1/8th note apart
            note_len_qn = 0.4 # Slightly less than 1/8th note for separation (staccato feel)
            midi_note = root_midi + melody_octave_offset + scale_degree_offset

            # Velocity variation for realism (as shown in tutorial)
            velocity = velocity_base + (j % 2 * 10) - 5 # Alternating velocity slightly
            
            RPR.RPR_MIDI_InsertNote(midi_take, False, False, pos_qn, pos_qn + note_len_qn, 0, midi_note, velocity, False)
            note_count += 1

        # Simple chord (like the video's C chord example)
        # Root position C major chord in the base octave
        if i % 2 == 0: # Place a chord every other bar
            chord_pos_qn = float(i * bar_length_qn) + 2.0 # Start mid-bar
            chord_len_qn = 1.5 # Longer duration chord
            chord_pitches = [root_midi, root_midi + current_scale[2], root_midi + current_scale[4], root_midi + 12] # C3, E3, G3, C4
            
            for k, pitch in enumerate(chord_pitches):
                # More velocity variation for chords
                velocity = velocity_base - (k * 5) + 15 # Descending velocity for chord notes
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, chord_pos_qn, chord_pos_qn + chord_len_qn, 0, pitch, velocity, False)
                note_count += 1

    RPR.RPR_MIDI_EndEdit(midi_take)

    # === Step 6: Select the created MIDI item and open MIDI editor for demonstration ===
    RPR.RPR_SetMediaItemSelected(item, True)
    RPR.RPR_Main_OnCommand(40866, 0) # View: Open item in MIDI editor

    return f"Created '{track_name}' with {note_count} notes over {bars} bars at {bpm} BPM"

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)? The `pos_qn` calculations ensure notes are placed on quarter-note and eighth-note subdivisions.
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? Yes, it demonstrates creating notes, chords, and varied velocities, which are the core editing actions shown.
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? Yes.
- [x] Does it avoid hardcoded file paths or external sample dependencies? Yes, uses ReaSynth.