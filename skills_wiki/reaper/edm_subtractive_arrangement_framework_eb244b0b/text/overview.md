### 1. High-level Design Pattern Extraction

> **Skill Name**: EDM Subtractive Arrangement Framework

* **Core Musical Mechanism**: **Subtractive Arrangement**. The tutorial demonstrates a fundamental electronic music workflow: building a dense, energetic "Drop" or "Chorus" loop first (with Chords, Melody, Bass, and Drums hitting together), and then stretching it across the timeline by *selectively subtracting elements* to create an Intro, Build, and Verse. 
* **Why Use This Skill (Rationale)**: This technique guarantees that the track sounds cohesive because all sections are derived from the exact same harmonic and rhythmic DNA. By managing *when* elements are introduced (e.g., withholding the bassline during the intro, teasing the drums during the build, muting the melody during the verse), the producer controls the listener's energy expectations, creating the tension-and-release necessary for dance music.
* **Overall Applicability**: Essential for turning a static 8-bar loop into a full song structure in genres like House, Trance, Future Bass, or Pop. 
* **Value Addition**: Instead of generating a single loop, this skill encodes song *macro-structure*. It automatically arrays your musical ideas across the timeline, mapping out an industry-standard 24-bar progression (Intro → Build → Verse → Drop) and even sets up a routing-ready "Ghost Kick" track for sidechain pumping.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 128 BPM (Standard House/EDM).
  - **Time Signature**: 4/4.
  - **Structure Grid**: 4-bar blocks (16 beats). 
    - Bars 1-4: Intro
    - Bars 5-8: Build/Pre-Chorus
    - Bars 9-16: Verse (8 bars)
    - Bars 17-24: Drop/Chorus (8 bars)

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (defaults to C minor).
  - **Progression**: A standard dance progression `i - VI - III - VII` is used as the base DNA. 
  - **Parts generated**: 
    - *Chords*: Triads playing sustained whole notes.
    - *Melody*: Syncopated lead line.
    - *Bass*: Root notes following the chords.

* **Step C: Sound Design & FX**
  - Standard tracks are created: `Chords`, `Melody`, `Bass`, and `Drums`.
  - A 5th utility track `Ghost Kick (Sidechain)` is created. Its Master/Parent send is disabled (`B_MAINSEND = 0`). This replicates the tutorial's step for setting up an invisible kick that plays during the Build and Verse to trigger a pumping compressor effect on the chords/bass without making an audible kick drum sound.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arrangement Macro-Structure | `RPR_AddMediaItemToTrack` | Allows placing specific 4-bar blocks of MIDI at exact timeline coordinates. |
| Harmonic/Rhythmic Content | `RPR_MIDI_InsertNote` | Computes diatonic MIDI notes and velocity dynamics without relying on external samples. |
| Sidechain Prep | `RPR_SetMediaTrackInfo_Value` | Disabling master send on a duplicated kick track safely preps the session for sidechain routing. |

> **Feasibility Assessment**: 100% reproducible for the structural and MIDI elements. The tutorial relies on specific VST synths and audio samples which we safely abstract away into labeled MIDI tracks and stock `ReaSynth` placeholders, allowing the user to map their preferred sounds.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 128,
    key: str = "C",
    scale: str = "minor",
    bars: int = 24, # Total arrangement length
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an EDM Subtractive Arrangement in the current REAPER project.
    Generates a full 24-bar structure (Intro, Build, Verse, Drop) from a unified chord progression.
    """
    import reaper_python as RPR

    # --- Music Theory & Initialization ---
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
    
    root_val = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    root_pitch = 60 + root_val # C4 base
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])

    def get_pitch(degree, octave=0):
        scale_len = len(scale_intervals)
        oct_offset = (degree // scale_len) + octave
        note_idx = degree % scale_len
        return root_pitch + (oct_offset * 12) + scale_intervals[note_idx]

    # --- Setup Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar

    # --- Track Creation ---
    track_names = ["Chords", "Melody", "Bass", "Drums", "Ghost Kick (Sidechain)"]
    tracks = {}
    for name in track_names:
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track
        
        # Add a basic synth so melodic tracks aren't silent
        if name in ["Chords", "Melody", "Bass"]:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            
        # Mute the output of the Ghost Kick track (for sidechain pumping logic)
        if name == "Ghost Kick (Sidechain)":
            RPR.RPR_SetMediaTrackInfo_Value(track, "B_MAINSEND", 0.0)

    # --- Generate 4-Bar Loop DNA ---
    chord_degrees = [0, 5, 2, 6] # i - VI - III - VII
    
    notes_chords = []
    notes_bass = []
    notes_melody = []
    notes_drums = []
    notes_ghost_kick = []
    notes_build_drums = []

    for bar in range(4):
        deg = chord_degrees[bar]
        start_b = bar * 4
        
        # Bass (Whole notes, -2 octaves)
        notes_bass.append((get_pitch(deg, -2), start_b, start_b + 4, 110))
        
        # Chords (Triads, -1 octave)
        for offset in [0, 2, 4]:
            notes_chords.append((get_pitch(deg + offset, -1), start_b, start_b + 4, 85))
            
        # Melody (Syncopated rhythm)
        notes_melody.append((get_pitch(deg, 0), start_b, start_b + 0.5, 95))
        notes_melody.append((get_pitch(deg + 2, 0), start_b + 0.5, start_b + 1.5, 80))
        notes_melody.append((get_pitch(deg + 4, 0), start_b + 1.5, start_b + 2.5, 85))
        notes_melody.append((get_pitch(deg + 2, 0), start_b + 2.5, start_b + 4, 90))

        # Drums (4-on-the-floor + snares + hihats)
        for beat in range(4):
            kick_b = start_b + beat
            notes_drums.append((36, kick_b, kick_b + 0.25, 120)) # Kick
            notes_ghost_kick.append((36, kick_b, kick_b + 0.25, 120)) # Ghost Kick
            if beat % 2 == 1:
                notes_drums.append((38, kick_b, kick_b + 0.25, 110)) # Snare
            notes_drums.append((42, kick_b + 0.5, kick_b + 0.75, 95)) # Hihat offbeat
            
            # Build Drums (Just kicks, plus a snare roll on the 4th bar)
            notes_build_drums.append((36, kick_b, kick_b + 0.25, 100))
            if bar == 3: # 4th bar snare roll
                notes_build_drums.append((38, kick_b, kick_b + 0.25, 80 + (beat * 10)))
                if beat >= 2: # 8th notes at the end
                    notes_build_drums.append((38, kick_b + 0.5, kick_b + 0.75, 95 + (beat * 5)))

    # --- Helper to instantiate MIDI blocks ---
    def insert_block(track, start_bar, length_bars, note_data, is_drum=False):
        start_sec = start_bar * bar_length
        duration_sec = length_bars * bar_length
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_sec)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for pitch, s_beat, e_beat, vel in note_data:
            n_start_sec = start_sec + (s_beat * beat_length)
            n_end_sec = start_sec + (e_beat * beat_length)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end_sec)
            chan = 9 if is_drum else 0
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)
        RPR.RPR_MIDI_Sort(take)

    # --- Timeline Subtractive Arrangement Mapping ---
    
    # 1. Intro (Bars 1-4) - Chords + Melody only
    insert_block(tracks["Chords"], 0, 4, notes_chords)
    insert_block(tracks["Melody"], 0, 4, notes_melody)
    insert_block(tracks["Ghost Kick (Sidechain)"], 0, 4, notes_ghost_kick, True) # Invisible pump

    # 2. Build (Bars 5-8) - Add building drums
    insert_block(tracks["Chords"], 4, 4, notes_chords)
    insert_block(tracks["Melody"], 4, 4, notes_melody)
    insert_block(tracks["Drums"], 4, 4, notes_build_drums, True)

    # 3. Verse (Bars 9-16) - Bass enters, Drums full, Melody removed
    for iter in range(2):
        start = 8 + (iter * 4)
        insert_block(tracks["Chords"], start, 4, notes_chords)
        insert_block(tracks["Bass"], start, 4, notes_bass)
        insert_block(tracks["Drums"], start, 4, notes_drums, True)
        insert_block(tracks["Ghost Kick (Sidechain)"], start, 4, notes_ghost_kick, True)

    # 4. Drop (Bars 17-24) - ALL Elements combined
    for iter in range(2):
        start = 16 + (iter * 4)
        insert_block(tracks["Chords"], start, 4, notes_chords)
        insert_block(tracks["Melody"], start, 4, notes_melody)
        insert_block(tracks["Bass"], start, 4, notes_bass)
        insert_block(tracks["Drums"], start, 4, notes_drums, True)
        insert_block(tracks["Ghost Kick (Sidechain)"], start, 4, notes_ghost_kick, True)

    return f"Created EDM Subtractive Arrangement (Intro, Build, Verse, Drop) over 24 bars at {bpm} BPM in {key} {scale}."
```