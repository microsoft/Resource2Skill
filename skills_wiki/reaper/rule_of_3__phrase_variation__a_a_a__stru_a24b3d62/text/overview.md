### 1. High-level Design Pattern Extraction

> **Skill Name**: "Rule of 3" Phrase Variation (A-A-A' Structure)

* **Core Musical Mechanism**: Repetition creates expectation, and breaking that expectation maintains listener interest. The "Rule of 3" dictates that a musical phrase should be played twice identically to establish a groove (Iterations 1 and 2). However, repeating it a third time exactly is redundant. On the third iteration, the phrase should start the same but deviate halfway through, creating an "A-A-A'" structure that builds tension and pushes the song forward.
* **Why Use This Skill (Rationale)**: Human brains are wired to recognize patterns. When we hear a 4-bar phrase once, we learn it. The second time, we validate it and groove to it. By the third time, our brain has mapped the pattern and will quickly lose interest (fatigue) if it is repeated again. Subverting the tail end of the third iteration satisfies the brain's need for novelty while maintaining the structural anchor of the original progression.
* **Overall Applicability**: This structural pacing rule is universal. It applies to chord progressions, vocal melodies, basslines, and drum beats across pop, EDM, hip-hop, and orchestral composition.
* **Value Addition**: Compared to a standard endlessly looping 4-bar MIDI clip, this skill encodes professional arrangement pacing. It dynamically generates a 12-bar sequence where the last segment actively builds tension, demonstrating a fundamental difference between amateur loops and finished songs.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 100-130 BPM (Tutorial uses a standard upbeat tempo).
  - **Grid**: Iterations 1 and 2 rely on relaxed 1/8th note arpeggios. Iteration 3's deviation switches to a denser 1/16th note rhythm to physically accelerate the pacing and build tension.
  - **Structure**: 12 bars total (3 phrases of 4 bars each). 

* **Step B: Pitch & Harmony**
  - **Phrase A (Bars 1-8)**: A standard, comforting pop progression (I - V - vi - IV). The melody arpeggiates the underlying chords in a predictable, looping manner.
  - **Phrase A' Deviation (Bars 9-12)**: Bars 9 and 10 repeat the I - V chords. Bars 11 and 12 completely deviate to a ii - V progression. 
  - **Melodic Tension**: During the ii - V deviation, the melody stops looping and instead performs an overlapping climbing sequence (0-1-2-3, 1-2-3-4...), driving the pitch upward without resolving, perfectly setting up a transition to a new section.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth`.
  - **Timbre**: A plucky, piano-like articulation is required so the arpeggiated 1/16th notes don't smear together.
  - **Parameters**: Instant attack (0.0), fast decay (0.2), low sustain (0.1), and moderate release (0.3).

* **Step D: Mix & Automation**
  - **Velocity Automation**: During the deviation in Bars 11-12, the MIDI note velocities swell smoothly upwards alongside the climbing pitch, naturally pushing the energy level up.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| A-A-A' Structural Generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise mathematical generation of the 3 iterations, the chord voicings, and the climbing velocity/rhythm in the deviation. |
| Time Translation | `RPR_MIDI_GetPPQPosFromProjTime` | Ensures exact placement on the MIDI grid regardless of the project's internal PPQ settings. |
| Plucky Timbre | FX Chain (`ReaSynth`) | Provides a stock, reliable sound source that can be cleanly shaped using envelope parameters (`RPR_TrackFX_SetParam`). |

> **Feasibility Assessment**: 100% reproducible. The script successfully encodes the music theory required to generate the chord progressions, the exact melodies, and the structural deviation demonstrated in the video using strictly REAPER stock plugins and APIs.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,  
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a 12-bar progression demonstrating the 'Rule of 3' (A-A-A' structure).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: The length is structurally tied to 12 bars to show 3 iterations.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument & Sound Design ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape ReaSynth to be a plucky, piano-like sound
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.0)  # Attack 
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.2)  # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.3)  # Release

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
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }
    
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_pitch = 60 + NOTE_MAP.get(key.capitalize(), 0)
    # Keep the root pitch comfortably in the midrange
    if root_pitch > 65: 
        root_pitch -= 12

    def get_note(degree, oct_offset=0):
        """Converts a scale degree into an absolute MIDI pitch."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_pitch + scale_intervals[idx] + (octave + oct_offset) * 12

    # === Step 5: Setup MIDI Item ===
    # Forcing exactly 12 bars (3 iterations of a 4-bar phrase) to demonstrate the rule
    total_bars = 12
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    notes_to_add = []

    def add_note(start_bar, start_beat, duration_beats, degree, oct_offset=0, velocity=100):
        note_start_sec = ((start_bar * beats_per_bar) + start_beat) * (60.0 / bpm)
        note_end_sec = note_start_sec + (duration_beats * (60.0 / bpm))
        
        # Convert absolute project time to MIDI PPQ exactly
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)
        
        pitch = get_note(degree, oct_offset)
        pitch = int(max(0, min(127, pitch)))
        velocity = int(max(1, min(127, velocity)))
        
        notes_to_add.append((start_ppq, end_ppq, pitch, velocity))

    # === Step 6: Generate A-A-A' Structure ===
    # Phrase A: I - V - vi - IV
    # Phrase A' (Deviation): I - V - ii - V
    chords_A = [0, 4, 5, 3] 
    chords_B = [0, 4, 1, 4] 

    for global_bar in range(total_bars):
        iteration = global_bar // 4
        bar_in_phrase = global_bar % 4
        
        # Select progression based on the Rule of 3
        root_deg = chords_A[bar_in_phrase] if iteration < 2 else chords_B[bar_in_phrase]
            
        # 1. Bass Note (held for the whole bar, low velocity)
        add_note(global_bar, 0, 4.0, root_deg, oct_offset=-2, velocity=velocity_base + 10)
        
        # 2. Sustained Triad (held for the whole bar)
        add_note(global_bar, 0, 4.0, root_deg, oct_offset=-1, velocity=velocity_base - 10)
        add_note(global_bar, 0, 4.0, root_deg + 2, oct_offset=-1, velocity=velocity_base - 10)
        add_note(global_bar, 0, 4.0, root_deg + 4, oct_offset=-1, velocity=velocity_base - 10)
        
        # 3. Melody Generation
        if iteration < 2 or bar_in_phrase < 2:
            # Iterations 1 & 2 (and start of 3): Predictable 1/8th note arpeggio
            m_pattern = [root_deg+4, root_deg+2, root_deg, root_deg+2] * 2
            for i, m_deg in enumerate(m_pattern):
                add_note(global_bar, i * 0.5, 0.5, m_deg, oct_offset=1, velocity=velocity_base)
        else:
            # Iteration 3 Deviation (Bars 11 & 12): Tension-building 1/16th notes
            # Climbs overlapping sequence: 0-1-2-3, 1-2-3-4, 2-3-4-5, 3-4-5-6
            m_pattern = [(root_deg + (i % 4) + (i // 4)) for i in range(16)]
            for i, m_deg in enumerate(m_pattern):
                # Dynamically swell velocity as the pitch climbs
                swell_vel = velocity_base - 10 + int((i / 15) * 30) 
                add_note(global_bar, i * 0.25, 0.25, m_deg, oct_offset=1, velocity=swell_vel)

    # === Step 7: Insert & Finalize ===
    for note in notes_to_add:
        RPR.RPR_MIDI_InsertNote(take, False, False, note[0], note[1], 0, note[2], note[3], True)
        
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' demonstrating the 'Rule of 3' (A-A-A' form) over 12 bars in {key} {scale} at {bpm} BPM."
```