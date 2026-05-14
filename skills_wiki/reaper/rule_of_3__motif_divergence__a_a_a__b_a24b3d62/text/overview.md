### 1. High-level Design Pattern Extraction

> **Skill Name**: "Rule of 3" Motif Divergence (A-A-A'-B)

* **Core Musical Mechanism**: A structural compositional framework for repeating musical ideas (melodies, chord progressions, or drum grooves). A motif is played twice identically to establish a pattern. On the third repetition, the motif begins identically but *deviates halfway through*, leading into an entirely different concluding fourth phrase.
* **Why Use This Skill (Rationale)**: This technique exploits how the human brain processes musical information. The 1st pass intrigues the listener; the 2nd pass reinforces the pattern. By the 3rd pass, the brain begins to tune it out ("too much of a good thing is no longer a good thing"). Deviating halfway through the 3rd iteration recaptures attention by introducing novelty *exactly* when the listener expects pure predictability. 
* **Overall Applicability**: This is a universal phrasing technique. It applies to writing lead melodies, structuring 4-chord progressions, placing drum fills (e.g., standard beat for 3 bars, fill at the end of the 4th), and arranging song sections across all genres.
* **Value Addition**: Transforms a static, boring 1-bar loop into a dynamic, narrative 4-bar (or 8-bar) phrase. It encodes high-level songwriting structure into raw MIDI generation.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - The script dynamically divides the total length (`bars`) into 4 equal phrasing "units". 
  - Unit 1 & 2 (Idea A): Straight 1/4 and 1/8 note syncopations.
  - Unit 3 (Idea A'): Mirrors the rhythm of Idea A, but alters the timing/notes in the second half.
  - Unit 4 (Idea B): Uses steady 1/4 notes to provide rhythmic resolution.
* **Step B: Pitch & Harmony**
  - **Harmony**: Uses a diatonic progression backing the melody.
    - Units 1 & 2: `i` chord (degrees 0, 2, 4)
    - Unit 3: `i` chord moving to `VI` chord (degrees 5, 7, 9)
    - Unit 4: `iv` chord (degrees 3, 5, 7) to `v` chord (degrees 4, 6, 8)
  - **Melody**: 
    - Idea A: Ascends from the Root (degrees 0, 2, 3, 4).
    - Idea A': Ascends from the Root but diverges upward (degrees 0, 2, 3, 5, 6).
    - Idea B: Resolves downward (degrees 3, 2, 4, 6).
* **Step C: Sound Design & FX**
  - Uses `ReaSynth` with a blend of sine and saw waves to support both the polyphonic chords and the melody.
  - Uses `ReaDelay` to add basic spatial width to the synth.
* **Step D: Mix & Automation**
  - Velocity mapping is used to accent downbeats and de-accent passing 1/8th notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| A-A-A'-B Phrasing | `RPR_MIDI_InsertNote` | Precise programmatic placement of notes allows us to dynamically stretch the 4-part structure over any requested bar length. |
| Scale/Key adherence | Lookup Tables & Modulo Math | Ensures the melodic divergence remains perfectly diatonic regardless of the user's requested key or scale. |
| Audibility | `RPR_TrackFX_AddByName` | Instantiates `ReaSynth` and `ReaDelay` so the structural concept is immediately audible without needing third-party VSTs. |

> **Feasibility Assessment**: 100%. Because the tutorial teaches a *compositional framework* rather than a specific sound design trick, we can fully replicate the lesson by generating MIDI that strictly obeys the rule.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Motif",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a musical phrase demonstrating the "Rule of 3" (A-A-A'-B structure).

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Total number of bars for the phrase (dynamically divided into 4 units).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 4, 4, True)
    RPR.RPR_UpdateTimeline()

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar
    item_length = sec_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
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

    # Normalize key and scale
    clean_key = key.upper() if len(key) == 1 else key[0].upper() + key[1:].upper()
    root_val = NOTE_MAP.get(clean_key, 0)
    intervals = SCALES.get(scale.lower(), SCALES["minor"])
    scale_len = len(intervals)

    def get_note(deg, oct_offset=0):
        octave_shift = deg // scale_len
        scale_deg = deg % scale_len
        return root_val + intervals[scale_deg] + (4 + oct_offset + octave_shift) * 12

    item_pos = RPR.RPR_GetMediaItemInfo_Value(item, "D_POSITION")

    def insert_note_bar(start_bar, duration_bar, pitch, velocity):
        """Helper to insert MIDI notes using bar-based musical timing."""
        start_sec = start_bar * sec_per_bar
        dur_sec = duration_bar * sec_per_bar
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_pos + start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_pos + start_sec + dur_sec)
        p = max(0, min(127, int(pitch)))
        v = max(1, min(127, int(velocity)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, v, False)

    def insert_chord(start_bar, duration_bar, degrees, oct_offset=-1, velocity=70):
        """Helper to stack scale degrees into a polyphonic chord."""
        for deg in degrees:
            insert_note_bar(start_bar, duration_bar, get_note(deg, oct_offset), velocity)

    # === GENERATE RULE OF 3 PHRASING ===
    # The structure divides the requested 'bars' into 4 equal phrasing units
    unit = bars / 4.0

    # Idea A (Unit 1) - Establishes the motif
    insert_chord(0.0 * unit, 1.0 * unit, [0, 2, 4], oct_offset=-1, velocity=65) # i chord
    insert_note_bar(0.0 * unit, 0.25 * unit, get_note(0), velocity_base)
    insert_note_bar(0.25 * unit, 0.125 * unit, get_note(2), velocity_base - 15)
    insert_note_bar(0.375 * unit, 0.125 * unit, get_note(3), velocity_base - 15)
    insert_note_bar(0.5 * unit, 0.25 * unit, get_note(4), velocity_base)

    # Idea A (Unit 2) - Exact Repeat (Reinforces the motif)
    insert_chord(1.0 * unit, 1.0 * unit, [0, 2, 4], oct_offset=-1, velocity=65) # i chord
    insert_note_bar(1.0 * unit, 0.25 * unit, get_note(0), velocity_base)
    insert_note_bar(1.25 * unit, 0.125 * unit, get_note(2), velocity_base - 15)
    insert_note_bar(1.375 * unit, 0.125 * unit, get_note(3), velocity_base - 15)
    insert_note_bar(1.5 * unit, 0.25 * unit, get_note(4), velocity_base)

    # Idea A' (Unit 3) - Rule of 3 Divergence (Starts same, diverges halfway)
    insert_chord(2.0 * unit, 0.5 * unit, [0, 2, 4], oct_offset=-1, velocity=65) # i chord
    insert_chord(2.5 * unit, 0.5 * unit, [5, 7, 9], oct_offset=-1, velocity=65) # VI chord (Harmonic Divergence)
    insert_note_bar(2.0 * unit, 0.25 * unit, get_note(0), velocity_base)
    insert_note_bar(2.25 * unit, 0.125 * unit, get_note(2), velocity_base - 15)
    insert_note_bar(2.375 * unit, 0.125 * unit, get_note(3), velocity_base - 15)
    insert_note_bar(2.5 * unit, 0.25 * unit, get_note(5), velocity_base + 10) # Melodic Divergence
    insert_note_bar(2.75 * unit, 0.25 * unit, get_note(6), velocity_base + 10)

    # Idea B (Unit 4) - Completely Different (Phrase Resolution)
    insert_chord(3.0 * unit, 0.5 * unit, [3, 5, 7], oct_offset=-1, velocity=65) # iv chord
    insert_chord(3.5 * unit, 0.5 * unit, [4, 6, 8], oct_offset=-1, velocity=65) # v chord
    insert_note_bar(3.0 * unit, 0.25 * unit, get_note(3), velocity_base)
    insert_note_bar(3.25 * unit, 0.25 * unit, get_note(2), velocity_base - 10)
    insert_note_bar(3.5 * unit, 0.25 * unit, get_note(4), velocity_base)
    insert_note_bar(3.75 * unit, 0.25 * unit, get_note(6), velocity_base - 10)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument & FX ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Blend in Saw wave for harmonic richness over the chords
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.5) 
    
    # Add stock delay to give the synth spatial presence
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)

    return f"Created '{track_name}' demonstrating Rule of 3 (A-A-A'-B) over {bars} bars in {clean_key} {scale} at {bpm} BPM"
```