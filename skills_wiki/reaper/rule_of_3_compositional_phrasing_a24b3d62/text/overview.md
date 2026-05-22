### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Compositional Phrasing

* **Core Musical Mechanism**: A tri-partite structural arrangement pattern that governs repetition. Instead of looping a 4-bar phrase infinitely, the pattern is structured as:
  1. **Idea (Bars 1-4)**: Introduce the melodic/harmonic phrase.
  2. **Reinforcement (Bars 5-8)**: Repeat the phrase identically to establish familiarity.
  3. **Departure (Bars 9-12)**: Begin the phrase identically (creating the expectation of a third repeat), but diverge halfway through to introduce novel harmonic and melodic material. 
* **Why Use This Skill (Rationale)**: This mechanism relies on psychoacoustics and listener attention span. The human brain craves pattern recognition (fulfilled by the first repeat) but quickly fatigues if stimulation becomes entirely predictable. By the third repetition, the brain begins tuning the pattern out ("too much of a good thing"). Diverging on the third repetition subverts expectation, rewarding the listener's attention and creating forward momentum in the song.
* **Overall Applicability**: Essential for transforming static 4-bar loops into dynamic 12-bar or 16-bar sections. Ideal for verse structures, intro buildups, drop variations, and general melodic phrasing across all genres (Pop, EDM, Hip-Hop, Orchestral).
* **Value Addition**: This skill injects high-level arrangement theory into a project. It prevents the "boring 4-bar loop syndrome" by encoding a programmatic awareness of musical expectation and variation over time.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4/4 time signature, scaling dynamically based on the requested bar count.
  - **Structure**: Divided into three equal segments. If 12 bars are requested, it creates three 4-bar phrases.
  - **Duration**: Chords play as whole notes (or scaled equivalents) on the downbeat. Melodies follow a driving staccato/legato rhythm (half/quarter note equivalents) to clearly articulate the underlying harmony.

* **Step B: Pitch & Harmony**
  - **Phrase A (Idea & Reinforcement)**: `I - IV - vi - V` (Scale degrees: 0, 3, 5, 4). Melody highlights the 3rd, 5th, and root of each chord (e.g., E, A, C, B in C Major).
  - **Phrase B (Departure)**: `I - IV - ii - V` (Scale degrees: 0, 3, 1, 4). The first half is identical to Phrase A. The second half drops to the `ii` chord instead of `vi`, with a totally different melodic contour that resolves down to the 5th degree.
  - *Note: This relative degree structure is mathematically robust and works cohesively in both Major and Minor scales.*

* **Step C: Sound Design & FX**
  - **Chords Track**: Uses `ReaSynth` configured with a triangle/sine hybrid (Param 8: 0.8) and soft attack/release envelopes to act as a supportive pad.
  - **Melody Track**: Uses `ReaSynth` configured as a sharp saw wave lead (Param 7: 0.7) with a fast attack and quick release to stand out against the pad.

* **Step D: Mix & Automation**
  - The melody track is mixed slightly louder than the chord track. Both are placed on independent tracks so an agent can easily swap the synths for external VSTs later.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Tri-partite Phrasing | Python looping and array mapping | Allows dynamic generation of the A-A-B phrase structure while gracefully stretching time to fit the requested bar count. |
| Harmony & Melody | `RPR_MIDI_InsertNote` with scale math | Encodes the relative interval logic (I-IV-vi-V vs I-IV-ii-V) perfectly into explicit MIDI pitches based on the key parameter. |
| Timbre separation | `RPR_TrackFX_AddByName` (ReaSynth) | Creates two distinct synthesizer patches (a soft triangle pad and a saw lead) entirely using stock REAPER tools. |

> **Feasibility Assessment**: 100% — The structural, harmonic, and compositional lessons taught in the video are fully translated into parametric MIDI logic and stock synthesizers.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3_Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a multi-track composition demonstrating the "Rule of 3" phrasing structure.
    Generates an Idea (A), a Reinforcement (A), and a Departure (B) sequence.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (Chords and Melody).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Total number of bars for the entire structure (defaults to 12).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # === Step 1: Music Theory Lookup Tables ===
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

    # === Step 2: Pitch & Time Math Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    root_val = NOTE_MAP.get(key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    def get_midi_note(degree, octave):
        """Converts a 0-indexed scale degree into an absolute MIDI pitch."""
        octave_shift = degree // len(scale_intervals)
        scale_degree = degree % len(scale_intervals)
        return root_val + scale_intervals[scale_degree] + (octave + octave_shift) * 12

    def get_triad(degree, octave):
        """Builds a root-position diatonic triad."""
        return [
            get_midi_note(degree, octave),
            get_midi_note(degree + 2, octave),
            get_midi_note(degree + 4, octave)
        ]

    # Calculate precise time scalings to stretch the pattern to the requested 'bars'
    total_bars = float(bars)
    phrase_bars = total_bars / 3.0       # Divide total bars into 3 equal phrases
    time_scale = phrase_bars / 4.0       # Scale factor relative to a standard 4-bar phrase template
    
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length_sec = beat_length * beats_per_bar
    item_length_sec = total_bars * bar_length_sec

    # === Step 3: Define Rule of 3 Musical Sequence ===
    # Phrase A: I - IV - vi - V
    phrase_a_chords = [0, 3, 5, 4] 
    phrase_a_melody = [
        # (relative_start_bar, relative_end_bar, scale_degree, octave)
        (0.0, 0.5, 2, 5), (0.5, 1.0, 2, 5),  # Bar 1 (over I)
        (1.0, 1.5, 5, 4), (1.5, 2.0, 5, 4),  # Bar 2 (over IV)
        (2.0, 2.5, 0, 5), (2.5, 3.0, 0, 5),  # Bar 3 (over vi)
        (3.0, 4.0, 6, 4),                    # Bar 4 (over V)
    ]
    
    # Phrase B (Departure): Starts identical to A, changes at Bar 3 to ii - V
    phrase_b_chords = [0, 3, 1, 4]
    phrase_b_melody = [
        (0.0, 0.5, 2, 5), (0.5, 1.0, 2, 5),  # Bar 1 (over I - Identical)
        (1.0, 1.5, 5, 4), (1.5, 2.0, 5, 4),  # Bar 2 (over IV - Identical)
        (2.0, 2.5, 3, 5), (2.5, 3.0, 3, 5),  # Bar 3 (over ii - DEPARTURE)
        (3.0, 4.0, 1, 5),                    # Bar 4 (over V - DEPARTURE)
    ]
    
    # The Tri-Partite Structure
    phrases = [
        (phrase_a_chords, phrase_a_melody), # 1: Idea
        (phrase_a_chords, phrase_a_melody), # 2: Reinforcement
        (phrase_b_chords, phrase_b_melody), # 3: Departure
    ]

    # === Step 4: Create Tracks and Synths ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Chords Track (Soft Triangle Pad)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    
    idx_chord = RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 8, 0.8) # Triangle mix
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 2, 0.1) # Attack
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 5, 0.3) # Release
    RPR.RPR_TrackFX_SetParam(track_chords, idx_chord, 0, 0.3) # Volume

    item_chords = RPR.RPR_CreateNewMIDIItemInProj(track_chords, 0.0, item_length_sec, False)
    take_chords = RPR.RPR_GetActiveTake(item_chords)

    # Melody Track (Sharp Saw Lead)
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_mel = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mel, "P_NAME", f"{track_name}_Melody", True)
    
    idx_mel = RPR.RPR_TrackFX_AddByName(track_mel, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 7, 0.7) # Saw mix
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 2, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 5, 0.1) # Release
    RPR.RPR_TrackFX_SetParam(track_mel, idx_mel, 0, 0.5) # Volume

    item_mel = RPR.RPR_CreateNewMIDIItemInProj(track_mel, 0.0, item_length_sec, False)
    take_mel = RPR.RPR_GetActiveTake(item_mel)

    # === Step 5: Inject MIDI Sequence ===
    for phrase_idx, (chords, melody) in enumerate(phrases):
        phrase_start_sec = phrase_idx * phrase_bars * bar_length_sec
        
        # Inject Chords
        for chord_idx, chord_deg in enumerate(chords):
            # Base template assumes 1 chord per bar
            rel_start_bar = chord_idx * 1.0
            rel_end_bar = (chord_idx + 1) * 1.0
            
            chord_start_sec = phrase_start_sec + (rel_start_bar * time_scale * bar_length_sec)
            chord_end_sec = phrase_start_sec + (rel_end_bar * time_scale * bar_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, chord_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, chord_end_sec)
            
            for pitch in get_triad(chord_deg, 4):  # Base Octave 4
                RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base * 0.75), True)
                
        # Inject Melody
        for (rel_start_bar, rel_end_bar, degree, octave) in melody:
            note_start_sec = phrase_start_sec + (rel_start_bar * time_scale * bar_length_sec)
            note_end_sec = phrase_start_sec + (rel_end_bar * time_scale * bar_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, note_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, note_end_sec)
            
            pitch = get_midi_note(degree, octave)
            RPR.RPR_MIDI_InsertNote(take_mel, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity_base), True)

    # Sort MIDI events
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_mel)

    return f"Created Rule of 3 Structural Arrangement ('{track_name}_Chords' & '{track_name}_Melody') over {bars} bars at {bpm} BPM in {key} {scale}."
```