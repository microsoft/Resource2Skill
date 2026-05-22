### 1. High-level Design Pattern Extraction

**Skill Name**: Syncopated Diatonic Chord Progression (Notation-Ready)

* **Core Musical Mechanism**: The tutorial demonstrates recording a syncopated, rhythmic chord progression (I - IV - V) via MIDI and then utilizing REAPER's built-in **Musical Notation Editor** (Score Editor) to automatically transcribe the raw performance into standard sheet music. The core mechanism is using precise MIDI quantization and diatonic harmony so that the resulting score is clean and readable.
* **Why Use This Skill (Rationale)**: The I-IV-V progression is the foundational backbone of Western popular music (Rock, Pop, Blues, Gospel). Applying a syncopated rhythm (hitting chords on the upbeats/off-beats) creates forward momentum and groove. By generating this precisely on the grid, it allows producers to instantly visualize the harmony in REAPER's notation view, bridging the gap between piano roll MIDI editing and classical music theory.
* **Overall Applicability**: Useful for starting a new composition, creating a backing track for vocal or solo practice, or generating structural chord beds for pop/rock tracks. It also serves as a perfect test case for exporting sheet music to session musicians.
* **Value Addition**: Instead of manually clicking in chords, this skill procedurally generates a functionally sound, syncopated chord progression based on user-defined keys and scales, ready to be viewed as sheet music.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Grid/Feel**: 16th-note syncopation. The chords don't just land on the downbeats; they anticipate the beats (e.g., hitting on the "and" of 2, or the "ah" of 1).
  - **Duration**: Staccato to medium-length block chords.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (Default: C Major).
  - **Progression**: I - IV - V - IV (e.g., C major, F major, G major, F major).
  - **Voicing**: Root position triads built procedurally from scale degrees.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` to provide an immediate auditory representation of the "Keyboard" track seen in the tutorial.

* **Step D: Mix & Automation**
  - Standard centered panning and default volume to ensure clear playback.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Chords | `RPR_MIDI_InsertNote()` | Allows precise, programmatic placement of syncopated notes on the grid. |
| Harmonic Structure | Scale Degree Math | Calculates correct MIDI pitches dynamically based on the requested key and scale. |
| Sound Generation | `RPR_TrackFX_AddByName()` | Adds ReaSynth so the generated MIDI produces sound immediately without needing external VSTs. |

**Feasibility Assessment**: 100% reproduction of the core musical concept. The script will generate the rhythmic chord progression. *Note: To see the visual result highlighted in the video, the user simply needs to double-click the generated MIDI item and press `Alt+4` (or `View -> Mode: musical notation`) to see the auto-transcribed sheet music.*

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Keyboard (Notation Demo)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a syncopated I-IV-V chord progression on a new track.
    Open the resulting MIDI item and press Alt+4 to view it in REAPER's Notation mode.
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
    }

    # Validate inputs
    root_val = NOTE_MAP.get(key.upper() if len(key) == 1 else key.capitalize(), 0)
    intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Base octave for chords
    base_octave = 4 
    root_midi = (base_octave + 1) * 12 + root_val

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for basic sound
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth slightly to sound more like an electric piano (less harsh)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) # Saw shape down
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Triangle shape up
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3) # Release time

    # Create MIDI Item
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define the syncopated rhythm pattern for a bar (start_beat, duration_beats)
    rhythm_pattern = [
        (0.0,  0.5),   # Beat 1 (eighth note)
        (0.75, 0.25),  # "ah" of 1 (sixteenth note)
        (1.5,  0.5),   # "and" of 2 (eighth note syncopation)
        (2.5,  0.5),   # "and" of 3 (eighth note syncopation)
        (3.5,  0.5)    # "and" of 4 (eighth note syncopation)
    ]

    # Define harmonic progression by scale degrees (0-indexed)
    # I = degrees 0, 2, 4
    # IV = degrees 3, 5, 7
    # V = degrees 4, 6, 8
    progression = [
        [0, 2, 4], # Bar 1: I chord
        [3, 5, 7], # Bar 2: IV chord
        [4, 6, 8], # Bar 3: V chord
        [3, 5, 7], # Bar 4: IV chord
    ]

    def get_midi_note(degree_idx):
        """Helper to safely calculate MIDI pitch from a scale degree index, handling octave wrapping."""
        octave_shift = degree_idx // len(intervals)
        scale_idx = degree_idx % len(intervals)
        return root_midi + (octave_shift * 12) + intervals[scale_idx]

    # Generate notes
    notes_added = 0
    ticks_per_quarter = 960 # REAPER default PPQ
    
    RPR.RPR_MIDI_DisableSort(take)
    
    for bar_idx in range(bars):
        # Loop the 4-bar progression if 'bars' > 4
        chord_degrees = progression[bar_idx % len(progression)]
        
        for start_beat, dur_beats in rhythm_pattern:
            # Calculate absolute tick positions
            start_ppq = (bar_idx * beats_per_bar + start_beat) * ticks_per_quarter
            end_ppq = start_ppq + (dur_beats * ticks_per_quarter)
            
            # Slight velocity variation for humanization
            vel = velocity_base
            if start_beat != 0.0:
                vel = max(10, velocity_base - 15) # Syncopated notes slightly quieter

            # Insert notes for the chord
            for degree in chord_degrees:
                pitch = get_midi_note(degree)
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, vel, False
                )
                notes_added += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes over {bars} bars at {bpm} BPM. Open MIDI item and use View -> Mode: musical notation."
```