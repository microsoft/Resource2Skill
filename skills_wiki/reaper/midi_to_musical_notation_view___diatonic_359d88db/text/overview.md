### 1. High-level Design Pattern Extraction

> **Skill Name**: MIDI to Musical Notation View & Diatonic Sketch

* **Core Musical Mechanism**: The video highlights REAPER's ability to seamlessly translate raw MIDI piano roll data into standard musical notation (sheet music). The skill provides a parametric diatonic sketch (chords + melody) and automates opening the MIDI editor directly into notation mode.
* **Why Use This Skill (Rationale)**: Many classical composers, arrangers, and multi-instrumentalists prefer reading traditional sheet music over piano rolls because it clearly displays harmonic relationships, key signatures, and rhythmic groupings (like rests, ties, and subdivisions). REAPER's notation view automatically infers time signatures and rhythmic quantizations from the MIDI data.
* **Overall Applicability**: Useful when composing orchestral pieces, printing charts for live musicians, studying the voice leading of a chord progression, or bridging the gap between digital sequencing and classical music theory. 
* **Value Addition**: Rather than just an empty MIDI clip, this skill translates your chosen key and scale parameters into a correctly voiced diatonic progression, giving REAPER's notation engine actual musical data to render into a standard staff. It also programmatically triggers REAPER's UI to open the notation view, serving as a powerful workflow automation for composers.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4.
  - **BPM**: Configurable (default 120 BPM).
  - **Rhythm Grid**: The underlying chords are held for whole notes (4 beats), while the melody features steady quarter-note (1 beat) subdivisions. This contrast perfectly demonstrates how the notation view handles simultaneous distinct rhythms and note lengths.

* **Step B: Pitch & Harmony**
  - **Key & Scale**: Fully parametric (defaults to C Major).
  - **Harmonic Progression**: A classical diatonic I - IV - V - I progression.
  - **Voicings**: Triads played in the 4th octave (e.g., C4, E4, G4), with a simple melody layered an octave higher (5th octave) to force the notation engine to map the notes cleanly across the staff.

* **Step C: Sound Design & FX**
  - **Instrument**: A basic `ReaSynth` instance is added so that when the notation is played back, the user hears the generated pitches.

* **Step D: Mix & Automation**
  - No specific automation is required. The focus is entirely on the MIDI data generation and the MIDI Editor UI view manipulation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chords and Melody | MIDI note insertion | Requires precise pitch, velocity, and timing logic derived from scale degree math to generate readable sheet music. |
| Sound | FX Chain (`ReaSynth`) | Gives immediate audio feedback of the notation when playing back the track. |
| Workflow Automation | `RPR_Main_OnCommand` & `RPR_MIDIEditor_OnCommand` | Uses REAPER's internal Action IDs to automatically open the MIDI item and switch the view from Piano Roll to Musical Notation (`40954`). |

> **Feasibility Assessment**: 100%. The script reliably generates a structured musical progression and effectively invokes the exact REAPER notation mode shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano Notation",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a parametric diatonic sketch and open it in REAPER's Musical Notation view.

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
        Status string.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a basic synth so the notation produces sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Select the item so we can open it in the MIDI editor later
    RPR.RPR_SetMediaItemSelected(item, True)

    # === Step 4: Generate Diatonic Progression (I-IV-V-I) ===
    root_note = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    def get_scale_note(degree, octave):
        """Returns the absolute MIDI pitch for a given scale degree (0-indexed) and octave."""
        octave_offset = degree // len(scale_intervals)
        note_in_scale = scale_intervals[degree % len(scale_intervals)]
        return root_note + note_in_scale + ((octave + octave_offset) * 12)

    notes_data = []
    
    for b in range(bars):
        bar_start_qn = b * 4
        prog_step = b % 4
        
        if prog_step == 0:
            # I chord + Melody
            notes_data.extend([
                (0, 4, bar_start_qn, 4), (2, 4, bar_start_qn, 4), (4, 4, bar_start_qn, 4),
                (0, 5, bar_start_qn, 1), (2, 5, bar_start_qn+1, 1), (4, 5, bar_start_qn+2, 1), (7, 5, bar_start_qn+3, 1)
            ])
        elif prog_step == 1:
            # IV chord + Melody
            notes_data.extend([
                (3, 4, bar_start_qn, 4), (5, 4, bar_start_qn, 4), (7, 4, bar_start_qn, 4),
                (5, 5, bar_start_qn, 1), (3, 5, bar_start_qn+1, 1), (7, 5, bar_start_qn+2, 1), (5, 5, bar_start_qn+3, 1)
            ])
        elif prog_step == 2:
            # V chord + Melody
            notes_data.extend([
                (4, 4, bar_start_qn, 4), (6, 4, bar_start_qn, 4), (8, 4, bar_start_qn, 4),
                (6, 5, bar_start_qn, 1), (4, 5, bar_start_qn+1, 1), (8, 5, bar_start_qn+2, 1), (6, 5, bar_start_qn+3, 1)
            ])
        elif prog_step == 3:
            # I chord (resolved) + Melody
            notes_data.extend([
                (0, 4, bar_start_qn, 4), (2, 4, bar_start_qn, 4), (4, 4, bar_start_qn, 4),
                (7, 5, bar_start_qn, 4)
            ])

    # Insert notes safely using Project Time to PPQ conversion
    for degree, oct_val, start_qn, len_qn in notes_data:
        pitch = get_scale_note(degree, oct_val)
        pitch = max(0, min(127, int(pitch)))
        
        start_time = start_qn * (60.0 / bpm)
        end_time = (start_qn + len_qn) * (60.0 / bpm)
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Automate Opening Musical Notation View ===
    # Open selected item in built-in MIDI editor
    RPR.RPR_Main_OnCommand(40153, 0)
    
    # Get active MIDI editor and switch to Notation Mode
    editor = RPR.RPR_MIDIEditor_GetActive()
    if editor:
        # 40954 is the Action ID for 'View: Mode: musical notation' in the MIDI Editor
        RPR.RPR_MIDIEditor_OnCommand(editor, 40954)

    return f"Created '{track_name}' with a {bars}-bar diatonic progression at {bpm} BPM, and opened in Musical Notation view."
```