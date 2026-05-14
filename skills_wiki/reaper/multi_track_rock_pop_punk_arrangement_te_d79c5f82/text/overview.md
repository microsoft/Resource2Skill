### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Pop-Punk Arrangement Template

* **Core Musical Mechanism**: This pattern represents a cohesive 4-piece band arrangement (Drums, Bass, Rhythm Guitar, Lead Guitar) functioning together. The rhythm section is driven by an 8th-note interlocking groove between the bass root notes and hi-hats. The harmonic foundation is laid by sustained chords in the mid-register (Rhythm Guitar), leaving the upper register open for arpeggiated melodic motifs (Lead Guitar).
* **Why Use This Skill (Rationale)**: This workflow demonstrates perfect frequency and rhythmic separation. By assigning strict roles—Bass holding the low-end root, Rhythm holding the mid-range harmony, Drums anchoring the 1 and 3 (kick) and 2 and 4 (snare), and Lead providing top-end motion—you prevent frequency masking and create an instantly recognizable, driving rock feel. 
* **Overall Applicability**: Ideal for rock, pop-punk, alternative, and metal tracks. It serves as an excellent starting point/scaffold for a song's chorus or high-energy verse. 
* **Value Addition**: Compared to an empty project, this skill encodes music theory (diatonic chord generation across multiple octaves) and arrangement theory (orchestrating different instruments to specific registers and rhythmic subdivisions) into a single deployable template.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time signature: 4/4
  * BPM range: 120 - 160+ (driving tempo)
  * Grid: 1/8th note drive. Bass plays constant 8th notes, Drums play 8th-note hi-hats, Lead plays 8th-note arpeggios. 
  * Syncopation: The kick drum hits on the 1, the "and" of 2 (1.5 beats), and the "and" of 3 (2.5 beats) to create a pushing rock groove.
* **Step B: Pitch & Harmony**
  * Key/Scale: Fully parametric (defaults to minor).
  * Progression: Uses a classic 4-chord diatonic loop (I - V - vi - IV in major, or i - v - VI - iv relative to the chosen scale).
  * Voicings:
    * Bass: Root note, 1 octave below middle C.
    * Rhythm: Root position triads (Root, 3rd, 5th), middle C register.
    * Lead: Arpeggiated sequence (Root-3rd-5th-3rd), 1 octave above Rhythm.
* **Step C: Sound Design & FX**
  * The tutorial relies heavily on premium Kontakt libraries (e.g., GetGood Drums, Solemn Tones bass/guitars) which cannot be instantiated natively without the user owning them.
  * *Implementation*: The script generates strictly named MIDI tracks ready for the user to drop their preferred VSTs onto.
* **Step D: Mix & Automation**
  * MIDI velocities are humanized manually (downbeat hi-hats are accented, offbeats are softer).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track composition | Track Creation & MIDI Insertion | The tutorial is about visualizing and writing 4 distinct MIDI parts simultaneously. We recreate the exact musical output of that workflow. |
| Harmonic generation | Array Indexing over Scales | Ensures that no matter what Key or Scale is passed in, the Bass, Chords, and Arpeggios are perfectly locked to diatonic scale degrees without hardcoding notes. |
| Humanized Drums | Velocity parameterization | Simulates a drummer's natural accents by setting downbeat 8th-notes to velocity 100 and offbeat 8th-notes to 80. |

> **Feasibility Assessment**: 100% of the core musical and MIDI arrangement logic is reproduced. The code does not spawn the specific third-party sample libraries used in the video (as those are premium plugins), but provides perfectly labeled and structured MIDI tracks ready for playback.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Arrangement",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Pop-Punk Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored, track names are hardcoded to band roles).
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Build Diatonic Multi-Octave Scale ===
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_val = NOTE_MAP.get(key, 0)
    
    full_scale = []
    # Build array from C-2 to C8
    for oct in range(-2, 8):
        for interval in scale_intervals:
            full_scale.append(root_val + oct * 12 + interval)

    # Find the index of the root note in octave 3 (base MIDI 48)
    base_idx = 0
    while full_scale[base_idx] < 48:
        base_idx += 1

    # === Step 3: Create Tracks & Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length_sec = bar_length_sec * bars
    
    band_tracks = ["Drums", "Bass", "Rhythm Guitar", "Lead Guitar"]
    takes = {}

    for name in band_tracks:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        takes[name] = take

    # Helper function to insert notes accurately
    def insert_note(take, beat_pos, beat_len, pitch, vel):
        pos_sec = beat_pos * (60.0 / bpm)
        end_sec = (beat_pos + beat_len) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Standard progression: 1 - 5 - 6 - 4 (scale degrees relative to root)
    progression = [0, 4, 5, 3] 

    # === Step 4: Populate MIDI Notes ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        bar_beat = bar * 4.0

        # --- 1. RHYTHM GUITAR ---
        # Sustained triad block chords (Root, 3rd, 5th of current scale degree)
        for note_offset in [0, 2, 4]:
            pitch = full_scale[base_idx + degree + note_offset]
            insert_note(takes["Rhythm Guitar"], bar_beat, 4.0, pitch, velocity_base - 10)

        # --- 2. BASS ---
        # Driving 8th notes, 1 octave down (-7 scale degrees)
        bass_base = base_idx - 7 + degree
        bass_pitch = full_scale[bass_base]
        for eighth in range(8):
            insert_note(takes["Bass"], bar_beat + eighth * 0.5, 0.45, bass_pitch, velocity_base)

        # --- 3. LEAD GUITAR ---
        # Arpeggio pattern (Root, 3rd, 5th, 3rd), 1 octave up (+7 scale degrees)
        lead_base = base_idx + 7 + degree
        arp_offsets = [0, 2, 4, 2, 0, 2, 4, 2]
        for eighth in range(8):
            pitch = full_scale[lead_base + arp_offsets[eighth]]
            insert_note(takes["Lead Guitar"], bar_beat + eighth * 0.5, 0.45, pitch, velocity_base - 15)

        # --- 4. DRUMS ---
        # Kick (36) on 1, 2-and, 3-and (Syncopated Rock Groove)
        insert_note(takes["Drums"], bar_beat + 0.0, 0.25, 36, velocity_base + 10)
        insert_note(takes["Drums"], bar_beat + 1.5, 0.25, 36, velocity_base)
        insert_note(takes["Drums"], bar_beat + 2.5, 0.25, 36, velocity_base)

        # Snare (38) strictly on 2 and 4
        insert_note(takes["Drums"], bar_beat + 1.0, 0.25, 38, velocity_base + 15)
        insert_note(takes["Drums"], bar_beat + 3.0, 0.25, 38, velocity_base + 15)

        # Hi-hat (42) riding straight 8th notes with alternating velocities
        for eighth in range(8):
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 20
            insert_note(takes["Drums"], bar_beat + eighth * 0.5, 0.2, 42, vel)

        # Crash (49) on the downbeat of the 1st bar of every 4-bar phrase
        if bar % 4 == 0:
            insert_note(takes["Drums"], bar_beat + 0.0, 0.5, 49, velocity_base + 20)

    # Sort all MIDI items to ensure proper playback
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track rock arrangement ({bars} bars, {key} {scale}, {bpm} BPM) with dynamic routing roles."
```