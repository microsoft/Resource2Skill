# Period Form Syncopated Melody Generator

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Period Form Syncopated Melody Generator 

* **Core Musical Mechanism**: This pattern generates a "Question & Answer" melody using the classic **Period Form** (Statement → Variation → Repetition → Resolution). It enforces musical coherence by adhering to a specific scale (e.g., Dorian), creates groove via 16th-note syncopation, balances melodic contour by alternating small steps with larger leaps, and prevents robotic stiffness through velocity dynamics and timing humanization (off-grid shifting).
* **Why Use This Skill (Rationale)**: A melody sticking perfectly to the grid with flat velocity and random pitches feels robotic and aimless. This skill encodes classical melodic phrasing. The "Question" creates harmonic/rhythmic tension by landing on a non-tonic scale degree or syncopated off-beat, and the "Answer" provides psychoacoustic satisfaction by resolving down to the tonic on a strong downbeat. Humanizing the timing mimics a live keyboard player's natural pocket.
* **Overall Applicability**: Ideal for generating lead hooks, vocal topline mockups, or plucky synth arpeggios in Pop, EDM, Lo-Fi, and Hip-Hop. 
* **Value Addition**: Replaces arbitrary MIDI note clicking with a structured, 4-bar algorithmic composition engine. It encodes fundamental music theory (scale degrees, resolution, syncopation, phrasing structure) directly into reproducible data.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/4 and 1/8th notes for stability, dotted with 1/16th note syncopations for interest (e.g., placing notes on the `1.0`, `1.5`, `2.25`, and `3.0` beats).
  - **Structure**: 4-bar phrase blocks. Bars 1, 2, and 3 use active, staccato rhythmic syncopation. Bar 4 uses longer, sustained legato notes to signal the end of the phrase.
  - **Humanization**: Notes are shifted off the absolute grid by +/- 5 to 15 milliseconds to simulate human timing.

* **Step B: Pitch & Harmony**
  - **Scale**: Parameterized (Major, Minor, Dorian, Pentatonic, etc.). The tutorial specifically highlights the Dorian mode.
  - **Contour**: Alternates between chordal skips (Root → 3rd → 5th) and step-wise motion (5th → 4th). 
  - **Phrasing**: 
    - *Statement (Bar 1)*: Establishes motif.
    - *Variation (Bar 2)*: Shifts the motif up a diatonic 3rd to create "Question" tension.
    - *Repetition (Bar 3)*: Anchors the listener.
    - *Resolution (Bar 4)*: Steps down linearly (4th → 2nd → Root) to close the "Answer".

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` to provide an immediate, clear synth tone to hear the melody.
  - **Effects**: `ReaDelay` added to give the melody space and enhance the syncopated rhythm via rhythmic echoes.

* **Step D: Mix & Automation**
  - **Dynamics**: Velocity variation is applied musically. Downbeats get higher velocities (~105), syncopated off-beats get slightly lower velocities (~90), and random humanization (+/- 8) is layered on top.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Period Form Phrasing | Algorithmic MIDI Note Insertion | Allows precise mapping of scale degrees (Statement/Variation/Resolution) over a 4-bar loop. |
| Syncopation & Humanization | Time-math calculations | Floating-point time offsets (+/- ms) and velocity math recreate the "off-grid" feel explicitly requested. |
| Synth & Space | FX Chain (ReaSynth + ReaDelay) | Ensures the melody is immediately audible with an appropriate lead tone, matching the tutorial's clarity. |

> **Feasibility Assessment**: 100%. The core of the tutorial is the MIDI composition theory (Period form, Dorian scale, syncopation, humanization). All of these are entirely reproducible via the REAPER Python API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Period Form Lead",
    bpm: int = 110,
    key: str = "C",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a memorable, syncopated melody using Period Form (Statement, Variation, Repetition, Resolution).
    Humanizes timing and velocity as per tutorial instructions.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (generates in 4-bar phrases).
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
    
    # Root midi note mapping (Octave 5)
    root_midi = NOTE_MAP.get(key.capitalize(), 0) + 60
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_scale_note(degree: int) -> int:
        """Converts a 0-indexed scale degree to an absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return root_midi + (octave_shift * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track Additively ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} ({key} {scale})", True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beats_per_sec = bpm / 60.0
    bar_length_sec = beats_per_bar / beats_per_sec
    item_length = bar_length_sec * bars
    
    # Safely create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    note_count = 0
    
    # === Step 4: Algorithmic Period-Form Melody Generation ===
    for bar in range(bars):
        bar_type = bar % 4
        base_beat = bar * beats_per_bar
        
        # Define the musical phrase for this specific bar
        phrase_notes = [] # Format: (start_beat, end_beat, scale_degree, dynamic_accent)
        
        if bar_type == 0 or bar_type == 2:
            # Statement / Repetition: Establishes motif with syncopation
            phrase_notes.append((0.0, 0.5, 0, 10))    # Downbeat (Root)
            phrase_notes.append((1.5, 2.0, 2, 0))     # Upbeat (3rd)
            phrase_notes.append((2.25, 2.75, 4, 5))   # Syncopated 16th (5th)
            phrase_notes.append((3.0, 3.75, 3, -5))   # Step down (4th)
            
        elif bar_type == 1:
            # Variation / Contrasting Idea: Shifts melody up for "Question" tension
            phrase_notes.append((0.0, 0.5, 2, 10))    # (3rd)
            phrase_notes.append((1.5, 2.0, 4, 0))     # (5th)
            phrase_notes.append((2.25, 2.75, 6, 5))   # (7th)
            phrase_notes.append((3.0, 3.75, 5, -5))   # (6th)
            
        elif bar_type == 3:
            # Resolution: Drops syncopation, steps down to Tonic for "Answer"
            phrase_notes.append((0.0, 1.0, 3, 10))    # (4th)
            phrase_notes.append((1.0, 2.0, 1, 5))     # (2nd)
            phrase_notes.append((2.0, 4.0, 0, -10))   # Resolves to Root and holds
            
        # Process and insert the notes
        for note_data in phrase_notes:
            start_b, end_b, degree, accent = note_data
            
            # Humanize timing (+/- 15ms shift off the grid)
            human_shift_start = random.uniform(-0.015, 0.015)
            human_shift_end = random.uniform(-0.015, 0.015)
            
            start_time = ((base_beat + start_b) / beats_per_sec) + human_shift_start
            end_time = ((base_beat + end_b) / beats_per_sec) + human_shift_end
            
            # Ensure time doesn't fall below 0
            start_time = max(0.0, start_time)
            end_time = max(0.05, end_time)
            
            # Calculate PPQ (Pulses Per Quarter Note) for REAPER MIDI API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Humanize velocity
            human_vel = random.randint(-8, 8)
            final_vel = int(max(1, min(127, velocity_base + accent + human_vel)))
            
            # Get specific pitch from scale mapping
            pitch = get_scale_note(degree)
            
            # Insert Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, final_vel, False)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument & FX ===
    # Add a synthesizer to make the melody audible
    fx_synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Set a nice plucky square/saw sound
    RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 0, 0.5)  # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 2, 0.3)  # Pulse width
    RPR.RPR_TrackFX_SetParam(track, fx_synth_idx, 3, 0.8)  # Saw character
    
    # Add Delay to accentuate the syncopation
    fx_delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_delay_idx, 0, 0.1) # Dry/Wet balance

    return f"Created '{track_name}' with {note_count} humanized notes over {bars} bars (Period Form) at {bpm} BPM in {key} {scale}."
```