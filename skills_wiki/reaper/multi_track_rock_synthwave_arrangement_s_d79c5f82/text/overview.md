### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Synthwave Arrangement Skeleton

* **Core Musical Mechanism**: A layered, 4-part band arrangement consisting of Drums, Bass, Rhythm Guitar/Synth, and Lead Guitar/Synth. The defining signature is the vertical interlocking of these instruments: the Bass drives the harmonic root with 8th-note momentum, the Rhythm track sustains the full triad to provide midrange harmonic density, the Lead plays an arpeggiated motif an octave higher for melodic interest, and the Drums provide the 4/4 rhythmic backbone. 
* **Why Use This Skill (Rationale)**: This arrangement pattern exemplifies proper frequency bracketing and rhythmic stratification. By separating the musical elements across distinct octaves (Bass in the 1st/2nd octave, Rhythm in the 3rd/4th, Lead in the 5th) and distinct rhythmic subdivisions (steady 8th notes in the bass, whole-note sustains in the rhythm, syncopated 16ths/8ths in the lead), the mix avoids frequency masking. It's the standard formula for pop, rock, and synthwave because it guarantees a full, cohesive sonic spectrum.
* **Overall Applicability**: Building the initial foundation for a rock, metal, or synthwave track. It perfectly complements REAPER's multi-track MIDI editing workflow shown in the tutorial, providing the raw MIDI data needed to practice selecting and editing multiple concurrent instruments.
* **Value Addition**: Compared to a blank project, this skill automatically translates a single chord progression into a fully orchestrated 4-piece band arrangement, mapping out the correct voicings, rhythmic patterns, and track routings simultaneously.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically 100-130 BPM (Defaults to 120 BPM).
  - **Drums**: Standard rock beat. Kick on beats 1 and 3; Snare on beats 2 and 4. Hi-hats on straight 8th notes.
  - **Bass**: Driving 8th-note chugs (staccato length, ~80% of a half-beat).
  - **Rhythm**: Whole note chords held across the entire measure (legato).
  - **Lead**: 8th-note ascending/descending arpeggios.

* **Step B: Pitch & Harmony**
  - **Progression**: A standard four-bar progression using scale degrees I - vi - IV - V (or i - VI - iv - v depending on the scale). 
  - **Voicings**: 
    - Bass plays the root note dropped by one octave.
    - Rhythm plays root-position triads (Root, 3rd, 5th).
    - Lead arpeggiates the chord tones (Root, 3rd, 5th, 3rd) shifted up by one octave to stay clear of the rhythm section.

* **Step C: Sound Design & FX**
  - To ensure standalone reproducibility without requiring external sample libraries (like the Kontakt instances shown in the video), this skill uses REAPER's native `ReaSynth` on all 4 generated tracks to serve as a placeholder sound generator. 

* **Step D: Mix & Automation**
  - The elements are separated strictly by MIDI octaves, establishing a natural frequency mix without needing immediate EQ. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track layout | `RPR_InsertTrackAtIndex()` | Creates a realistic 4-piece band setup corresponding to the video's Bass, Rhythm, Lead, and Drums tracks. |
| Arrangement generation | `RPR_MIDI_InsertNote()` | Allows precise, parametric placement of kicks, snares, bass chugs, and arpeggios based on the input key and scale. |
| Sound generation | `RPR_TrackFX_AddByName()` | Instantiates native ReaSynth so the generated MIDI produces immediate audio feedback without external VSTis. |

> **Feasibility Assessment**: 100% of the *musical arrangement logic* is reproduced. The specific third-party guitar and drum VSTis (Kontakt, GGD) shown in the video cannot be invoked stock, so native `ReaSynth` is used as a functional acoustic placeholder.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock_Arrangement",
    bpm: int = 120,
    key: str = "D",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a layered 4-track Rock/Synthwave arrangement (Drums, Bass, Rhythm, Lead).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (will loop the 4-chord progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory setup (Octave 2 base for chord roots)
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}
    
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

    root_midi = NOTE_MAP.get(key, 50) # Defaults to D
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_scale_note(degree, root, intervals):
        """Returns the exact MIDI note for a given scale degree (0-indexed)."""
        octave = degree // len(intervals)
        note = degree % len(intervals)
        return root + (octave * 12) + intervals[note]

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Timing math
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    bar_len = beat_len * beats_per_bar
    total_len = bar_len * bars

    def create_instrument_track(name):
        """Creates a track, adds a basic synth, and creates an empty MIDI item."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)

        # Add basic stock synth so it produces sound immediately
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_len)
        take = RPR.RPR_AddTakeToMediaItem(item)

        return take

    def insert_note(take, start_sec, end_sec, pitch, vel):
        """Helper to insert a MIDI note using project seconds."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        # noSort=True for performance; we will sort at the very end
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # Initialize the 4 tracks
    take_drums = create_instrument_track(f"{track_name}_Drums")
    take_bass = create_instrument_track(f"{track_name}_Bass")
    take_rhythm = create_instrument_track(f"{track_name}_Rhythm")
    take_lead = create_instrument_track(f"{track_name}_Lead")

    # Standard progression sequence (e.g. i - VI - iv - v)
    progression_degrees = [0, 5, 3, 4]
    notes_count = 0

    for i in range(bars):
        bar_start = i * bar_len
        chord_degree = progression_degrees[i % len(progression_degrees)]

        # --- 1. DRUMS (Standard Rock Beat) ---
        # Kick (36) on beats 1 and 3
        insert_note(take_drums, bar_start, bar_start + 0.2, 36, velocity_base)
        insert_note(take_drums, bar_start + 2*beat_len, bar_start + 2*beat_len + 0.2, 36, velocity_base)
        # Snare (38) on beats 2 and 4
        insert_note(take_drums, bar_start + beat_len, bar_start + beat_len + 0.2, 38, velocity_base)
        insert_note(take_drums, bar_start + 3*beat_len, bar_start + 3*beat_len + 0.2, 38, velocity_base)
        # Hi-Hats (42) on straight 8th notes
        for j in range(8):
            hat_start = bar_start + j * (beat_len / 2)
            insert_note(take_drums, hat_start, hat_start + 0.1, 42, velocity_base - 20)
        # Crash (49) on beat 1 of the very first measure
        if i == 0:
            insert_note(take_drums, bar_start, bar_start + 0.5, 49, velocity_base + 10)
        notes_count += 13

        # --- HARMONY CALCULATION ---
        n1 = get_scale_note(chord_degree, root_midi, scale_intervals)
        n3 = get_scale_note(chord_degree + 2, root_midi, scale_intervals)
        n5 = get_scale_note(chord_degree + 4, root_midi, scale_intervals)

        # --- 2. BASS (Driving 8th notes, drop 1 octave) ---
        bass_note = n1 - 12
        for j in range(8):
            b_start = bar_start + j * (beat_len / 2)
            b_end = b_start + (beat_len / 2) * 0.85 # Staccato separation
            insert_note(take_bass, b_start, b_end, bass_note, velocity_base)
            notes_count += 1

        # --- 3. RHYTHM GUITAR/SYNTH (Sustained Triads) ---
        insert_note(take_rhythm, bar_start, bar_start + bar_len, n1, velocity_base - 10)
        insert_note(take_rhythm, bar_start, bar_start + bar_len, n3, velocity_base - 10)
        insert_note(take_rhythm, bar_start, bar_start + bar_len, n5, velocity_base - 10)
        notes_count += 3

        # --- 4. LEAD GUITAR/SYNTH (8th note arpeggios, up 1 octave) ---
        arp_sequence = [n1 + 12, n3 + 12, n5 + 12, n3 + 12]
        for j in range(8):
            arp_note = arp_sequence[j % 4]
            l_start = bar_start + j * (beat_len / 2)
            l_end = l_start + (beat_len / 2) * 0.8
            insert_note(take_lead, l_start, l_end, arp_note, velocity_base)
            notes_count += 1

    # Finalize and sort MIDI events on all takes
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_rhythm)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track arrangement '{track_name}' (4 tracks) with {notes_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```