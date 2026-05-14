### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock Band Arrangement Scaffold

* **Core Musical Mechanism**: A structured, 4-layer instrumental arrangement (Rhythm Guitar, Lead Guitar, Bass, and Drums) built using typical rock/metal ensemble roles. The pattern demonstrates interlocking frequency and rhythm bracketing: Rhythm guitars hold the mid-range harmony via sustained chords, the bass locks to the root notes with driving 8th-note momentum, the drums anchor the groove with a backbeat and crashes on the transitions, and a lead instrument provides high-frequency 16th-note melodic arpeggiations. 
* **Why Use This Skill (Rationale)**: This arrangement template works because it cleanly separates musical roles to prevent masking and crowding. Bass and Kick hold the low end; chords hold the midrange; hi-hats, cymbals, and lead arpeggios hold the highs. Furthermore, visually coloring these tracks (as demonstrated in the tutorial) allows for seamless multi-track MIDI editing in a single piano roll, a workflow crucial for ensuring ghost notes, bass roots, and kick drum hits align perfectly.
* **Overall Applicability**: Excellent as a starting scaffold for rock, metal, pop-punk, or synth-wave tracks. The color-coded tracks make it highly suited for producers who prefer composing multiple instruments simultaneously in a single MIDI editor window (a workflow heavily used by orchestral and band composers).
* **Value Addition**: Compared to a blank project, this skill automatically sets up a fully color-coded, 4-track band template and generates a cohesive 4-bar musical idea with proper part-writing, ready for the user to tweak and expand upon.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Grid**: 4/4 time, straight feel. 
  - **Drums**: Kick on beats 1, 2.5, and 3. Snare on the standard backbeat (2 and 4). 8th-note hi-hats.
  - **Bass**: Driving, continuous 8th notes.
  - **Rhythm Guitar**: Sustained whole-note triads (1 per bar).
  - **Lead Guitar**: Continuous 16th-note up/down arpeggio sequence.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Designed to work in any minor key (e.g., E minor).
  - **Progression**: i - VI - III - VII (A classic epic/rock four-chord loop, e.g., Em - C - G - D).
  - **Voicings**: Bass plays root notes in Octave 2. Rhythm Guitar plays root position triads in Octave 3. Lead plays a 4-note arpeggio (Root, 3rd, 5th, Octave) in Octave 4.

* **Step C: Sound Design & FX**
  - **Instruments**: Native `ReaSynth` is applied to all tracks to ensure immediate audibility without relying on external VSTs or sample libraries.
  - **Color Coding**: Tracks are strictly color-coded using REAPER's custom color API (Drums = Indigo, Bass = Purple, Rhythm = Orange, Lead = Pink) to visually separate them in the shared MIDI editor.

* **Step D: Mix & Automation**
  - Tracks are independent and left at unity gain to allow the user to easily route them to dedicated amp simulators, drum samplers, or bussing structures later.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Setup & Color Coding | `RPR_SetMediaTrackInfo_Value` | Crucial for the tutorial's multi-track shared MIDI editing workflow, cleanly identifying layers. |
| Item Generation | `RPR_CreateNewMIDIItemInProj` | Safely generates properly initialized MIDI items/takes spanning the requested duration. |
| Arrangement & Pitch | `RPR_MIDI_InsertNote` | Precise, programmatic insertion of drums, chords, basslines, and arpeggios using scale degree math. |

> **Feasibility Assessment**: 100% reproducible for the MIDI arrangement, logic, and workflow color-coding setup. Stock `ReaSynth` is used as a placeholder sound generator instead of the user's specific third-party sample libraries.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockBand", # Not strictly used as 4 distinct tracks are generated
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-layer color-coded Rock Arrangement Scaffold in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Unused here (creates 4 specific role tracks).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    root_note = NOTE_MAP.get(key, 4)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # === Helpers ===
    def get_note(degree, octave):
        """Convert a scale degree (0-indexed) into an absolute MIDI note."""
        octave_offset = degree // len(scale_intervals)
        scale_deg = degree % len(scale_intervals)
        return root_note + scale_intervals[scale_deg] + (octave + octave_offset) * 12

    def add_note(take, pitch, start_beat, length_beats, velocity=velocity_base):
        """Insert a MIDI note safely using PPQ position."""
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    def get_color_int(r, g, b):
        """Convert RGB to REAPER custom color int."""
        return r | (g << 8) | (b << 16) | 0x1000000

    def create_colored_track(name, r, g, b):
        """Create a track, apply color, attach ReaSynth, and return an initialized MIDI take."""
        t_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(t_idx, True)
        track = RPR.RPR_GetTrack(0, t_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", get_color_int(r, g, b))
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        start_time = 0.0
        end_time = bars * 4 * (60.0 / bpm)
        item = RPR.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
        take = RPR.RPR_GetActiveTake(item)
        return take

    # === Initialization ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    # The classic epic rock progression: i - VI - III - VII
    progression = [0, 5, 2, 6] 

    # === Track 1: Drums ===
    drum_take = create_colored_track("MIDI Drums", 75, 0, 130) # Indigo
    for bar in range(bars):
        for b in range(4):
            abs_b = bar * 4 + b
            
            # Hats & Crashes
            if bar == 0 and b == 0:
                add_note(drum_take, 49, abs_b, 0.25) # Crash on downbeat of bar 1
            else:
                add_note(drum_take, 42, abs_b, 0.25) # Closed Hat
            add_note(drum_take, 42, abs_b + 0.5, 0.25) # Off-beat Hat
            
            # Kick (1, 2.5, 3)
            if b == 0 or b == 2:
                add_note(drum_take, 36, abs_b, 0.25)
            if b == 1:
                add_note(drum_take, 36, abs_b + 0.5, 0.25)
                
            # Snare (2, 4)
            if b == 1 or b == 3:
                add_note(drum_take, 38, abs_b, 0.25)
    RPR.RPR_MIDI_Sort(drum_take)

    # === Track 2: Bass ===
    bass_take = create_colored_track("BASS", 128, 0, 128) # Purple
    for bar in range(bars):
        chord_degree = progression[bar % len(progression)]
        bass_note = get_note(chord_degree, 2) # Octave 2
        
        # Driving 8th notes
        for i in range(8):
            abs_b = bar * 4 + i * 0.5
            add_note(bass_take, bass_note, abs_b, 0.4) 
    RPR.RPR_MIDI_Sort(bass_take)

    # === Track 3: Rhythm Guitar ===
    rhy_take = create_colored_track("GTR RHY", 255, 165, 0) # Orange
    for bar in range(bars):
        chord_degree = progression[bar % len(progression)]
        notes = [
            get_note(chord_degree, 3),      # Root
            get_note(chord_degree + 2, 3),  # 3rd
            get_note(chord_degree + 4, 3)   # 5th
        ]
        abs_b = bar * 4
        
        # Whole note chord swell
        for note in notes:
            add_note(rhy_take, note, abs_b, 4.0)
    RPR.RPR_MIDI_Sort(rhy_take)

    # === Track 4: Lead Guitar ===
    lead_take = create_colored_track("GTR LEAD", 255, 105, 180) # Pink
    for bar in range(bars):
        chord_degree = progression[bar % len(progression)]
        notes = [
            get_note(chord_degree, 4),
            get_note(chord_degree + 2, 4),
            get_note(chord_degree + 4, 4),
            get_note(chord_degree + 7, 4) # Root octave up
        ]
        
        # 16th note up/down sequence
        arp_pattern = [0, 1, 2, 3, 2, 1] 
        for i in range(16):
            note_idx = arp_pattern[i % len(arp_pattern)]
            note = notes[note_idx]
            abs_b = bar * 4 + i * 0.25
            add_note(lead_take, note, abs_b, 0.2)
    RPR.RPR_MIDI_Sort(lead_take)

    return f"Created Multi-Track Rock Scaffold with 4 colored tracks over {bars} bars at {bpm} BPM in {key} {scale}."
```