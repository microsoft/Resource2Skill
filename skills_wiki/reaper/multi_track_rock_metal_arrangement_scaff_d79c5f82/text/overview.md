### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Metal Arrangement Scaffold

* **Core Musical Mechanism**: This pattern encodes a foundational multi-instrument rock arrangement. It relies on a synchronized 8th-note rhythmic drive across the bass and rhythm guitar tracks, locked to a standard backbeat drum groove with a syncopated kick. Harmonically, it algorithmically generates a 4-chord diatonic progression (e.g., i-VI-III-VII in minor) to create a cohesive backdrop for a lead melody.
* **Why Use This Skill (Rationale)**: The power of a rock/metal mix comes from "frequency stratification" and rhythmic locking. By placing the bass an octave below the rhythm guitars, and having both chug identical 8th-note rhythms locked to the kick drum's syncopations, you create a massive, unified wall of sound. The lead guitar then sits in the upper midrange, clear of the rhythmic dense low-end.
* **Overall Applicability**: Ideal for laying down a quick, heavy backing track, auditioning multi-out virtual instruments (like drum samplers and guitar amp sims), or establishing the structural foundation of a rock, metal, or alternative track.
* **Value Addition**: Instead of manually plotting out four separate tracks and risking harmonic or rhythmic clashes, this skill instantly generates mathematically perfect, scale-locked diatonic triads and synchronized grooves across four distinct instruments.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo:** Standard driving tempo around 120 BPM.
  - **Grid:** Rhythmic foundation is built on straight 8th notes (chugs).
  - **Drums:** Kick on beat 1, beat 3, and the "and" of beat 3 (syncopation). Snare on beats 2 and 4. Constant 8th-note hi-hats with alternating velocities to simulate stick dynamics.
* **Step B: Pitch & Harmony**
  - **Progression:** Follows a classic 4-bar loop. In a minor key, it uses degrees i, VI, III, VII. In major, I, vi, IV, V.
  - **Voicings:** Rhythm guitars play diatonic triads (or power chords) generated relative to the current scale degree. Bass plays the root note of the current chord, dropped two octaves.
  - **Lead:** A simple quarter-note arpeggio (Root, 3rd, 5th, 3rd) outlining the current chord in a higher register.
* **Step C: Sound Design & FX**
  - The script prepares the MIDI data perfectly partitioned on four tracks (`Drums`, `Bass`, `Rhythm`, `Lead`). Users can then drop their preferred VSTis (e.g., Kontakt, EZDrummer, Amp Sims) onto these tracks.
* **Step D: Mix & Automation**
  - Tracks are separated to allow individual panning (e.g., hard-panning rhythm guitars if duplicated) and EQing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track Orchestration | `RPR_InsertTrackAtIndex` & `RPR_AddMediaItemToTrack` | Creates the separated stems needed for the multi-instrument workflow demonstrated. |
| Drum, Bass, Guitar Parts | `RPR_MIDI_InsertNote` | Provides exact control over pitch, velocity, and timing to lock the rhythm section together. |
| Harmonic Generation | Algorithmic Scale Lookup | Allows the 4-track arrangement to adapt dynamically to any user-provided key and scale. |

> **Feasibility Assessment**: 100% of the MIDI composition pattern is reproducible. The tutorial uses third-party VST instruments (like Kontakt) for the sound source, which cannot be guaranteed on the target machine, so the code generates the pure MIDI arrangement ready for the user's instruments.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RockBand",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 'Multi-Track Rock/Metal Arrangement Scaffold' in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

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

    # Set project tempo
    RPR.RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, bpm, 4, 4, True)

    root_val = NOTE_MAP.get(key, 11) # Default to B
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # Determine progression based on scale flavor
    if "minor" in scale:
        progression = [0, 5, 2, 6] # i, VI, III, VII
    else:
        progression = [0, 5, 3, 4] # I, vi, IV, V

    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    def add_note(take, start_time, duration, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        pitch = max(0, min(127, int(pitch)))
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    def get_pitch_for_idx(idx, base_octave):
        octave_shift = idx // len(scale_intervals)
        scale_deg = idx % len(scale_intervals)
        return root_val + scale_intervals[scale_deg] + ((base_octave + octave_shift) * 12)

    def get_chord_pitches(degree, base_octave):
        return [
            get_pitch_for_idx(degree, base_octave),
            get_pitch_for_idx(degree + 2, base_octave),
            get_pitch_for_idx(degree + 4, base_octave)
        ]

    tracks_to_create = [
        {"name": f"{track_name} Drums", "type": "drums"},
        {"name": f"{track_name} Bass", "type": "bass"},
        {"name": f"{track_name} Rhythm", "type": "rhythm"},
        {"name": f"{track_name} Lead", "type": "lead"},
    ]

    total_notes = 0

    for track_info in tracks_to_create:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_info["name"], True)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bars * bar_len)
        take = RPR.RPR_AddTakeToMediaItem(item)

        t_type = track_info["type"]

        for b in range(bars):
            start_of_bar = b * bar_len
            deg = progression[b % len(progression)]
            
            if t_type == "drums":
                # Driving Rock Kick
                for pos in [0.0, 2.0, 2.5]:
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.5, 36, velocity_base)
                    total_notes += 1
                # Snare
                for pos in [1.0, 3.0]:
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.5, 38, velocity_base)
                    total_notes += 1
                # 8th note Hi-hats with velocity dynamics
                for pos_idx in range(8):
                    pos = pos_idx * 0.5
                    vel = velocity_base if pos_idx % 2 == 0 else velocity_base - 20
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.25, 42, vel)
                    total_notes += 1
                # Crash on the downbeat of the loop
                if b == 0:
                    add_note(take, start_of_bar, beat_len, 49, velocity_base + 10)
                    total_notes += 1

            elif t_type == "bass":
                # Root notes, octave 2, chugging 8th notes
                root_pitch = get_pitch_for_idx(deg, 2)
                for i in range(8):
                    pos = i * 0.5
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.45, root_pitch, velocity_base)
                    total_notes += 1

            elif t_type == "rhythm":
                # Triad block chords, octave 3, chugging 8th notes
                pitches = get_chord_pitches(deg, 3)
                for i in range(8):
                    pos = i * 0.5
                    for p in pitches:
                        add_note(take, start_of_bar + pos * beat_len, beat_len * 0.4, p, velocity_base - 10)
                        total_notes += 1

            elif t_type == "lead":
                # Arpeggiated melody, octave 5, quarter notes
                pitches = get_chord_pitches(deg, 5)
                arp_pattern = [pitches[0], pitches[1], pitches[2], pitches[1]]
                for i in range(4):
                    pos = i * 1.0 
                    add_note(take, start_of_bar + pos * beat_len, beat_len * 0.8, arp_pattern[i], velocity_base)
                    total_notes += 1

        RPR.RPR_MIDI_Sort(take)

    return f"Created {len(tracks_to_create)} tracks ({track_name} group) with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```