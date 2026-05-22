### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Layered Arrangement Scaffold (Rock / Synthwave)

* **Core Musical Mechanism**: This pattern establishes a cohesive, four-part interlocking arrangement. It systematically assigns distinct musical roles—a driving 8th-note root bassline, a foundational block-chord rhythm track, a flowing arpeggiated lead, and a backbeat drum groove. By keeping all melodic and harmonic elements mathematically locked to the same diatonic scale degrees, the layers interact perfectly without clashing.
* **Why Use This Skill (Rationale)**: This structure relies on the principle of *frequency and rhythmic slotting*. The bass anchors the low end with straight 8th notes, emphasizing root motion. The rhythm track fills the mid-range with sustained harmony. The lead track occupies the upper-mid frequencies with an active, syncopated or continuous 8th/16th-note rhythm, providing melodic contour. The kick and snare anchor the strong beats, giving the progression forward momentum. 
* **Overall Applicability**: This is a universal scaffold for producing the core loop (the "drop" or "chorus") of rock, synthwave, pop, or orchestral music. It gives producers an immediate, thick-sounding structural bed to build upon.
* **Value Addition**: Instead of manually programming a chord progression and then painstakingly copying the roots to a bass track and splitting the chords into an arpeggio, this skill encodes the harmonic relationships (Roots -> Triads -> Arpeggios) automatically across multiple tracks. It establishes a perfectly synchronized multi-track MIDI bed ready for synth/instrument assignments.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Time Signature**: 120 BPM (adjustable), 4/4 time.
  - **Grid/Divisions**: Driving 8th-note grid. 
  - **Rhythm Patterns**: 
    - *Drums*: Kick on beats 1, 2.5, and 3; Snare on beats 2 and 4; Hi-hats on straight 8th notes.
    - *Bass*: Pumping, straight 8th notes (legato or slightly staccato).
    - *Rhythm*: Sustained whole notes lasting the entire bar.
    - *Lead*: 8th-note up-and-down arpeggios (root, third, fifth, third).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Configurable (defaults to C minor).
  - **Progression**: Classic dramatic pop/rock progression: `i - VI - iv - v` (e.g., in C minor: Cm, Ab, Fm, Gm).
  - **Voicings**: Diatonic root-position triads built by stacking thirds within the selected scale. Bass plays 2 octaves below the rhythm track; Lead plays 1 octave above.

* **Step C: Sound Design & FX**
  - While the script generates the pure MIDI data, standard practice for this arrangement involves routing the tracks to respective Virtual Instruments (e.g., a sampler for drums, a subtractive synth for the bass, a pad/rhythm synth for the chords, and a plucky synth for the lead).

* **Step D: Mix & Automation**
  - Elements are separated into distinct tracks ("Drums", "Bass", "Rhythm", "Lead") allowing the producer to utilize REAPER's multi-track MIDI editor feature (as shown in the tutorial) to visualize how the ghost notes of the chords align with the bass and lead melodies.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Architecture | `RPR_InsertTrackAtIndex` | Safely and additively builds a multi-track folder/grouping structure without destroying the user's project. |
| Harmonic/Melodic Sync | Algorithmic MIDI Generation | Computes diatonic thirds mathematically (`degree`, `degree+2`, `degree+4`) ensuring the Bass, Rhythm, and Lead tracks are perfectly harmonized in any chosen key/scale. |
| Drum Programming | `RPR_MIDI_InsertNote` | Precise placement of Kick (36), Snare (38), and Hi-Hat (42) to establish the driving groove demonstrated in the tutorial. |

> **Feasibility Assessment**: 100% reproduction of the MIDI composition logic and multi-track workflow scaffold demonstrated. The user will simply need to assign their preferred VST instruments to the generated tracks to hear the specific synth/orchestral timbres.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arrangement Scaffold",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Track Layered Arrangement Scaffold (Drums, Bass, Rhythm, Lead)
    in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_note = NOTE_MAP.get(key, 0) + 48  # Set base to octave 3 (e.g., C3 = 48)

    def get_pitch(degree, octave_offset=0):
        """Convert a scale degree (0-indexed) to an absolute MIDI pitch."""
        octaves = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        return base_note + (octaves + octave_offset) * 12 + scale_intervals[scale_idx]

    # Progression: i - VI - iv - v (diatonic degrees: 0, 5, 3, 4)
    progression = [0, 5, 3, 4] 
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def get_proj_time(beat):
        """Convert beats to project time based on BPM."""
        return (60.0 / bpm) * beat

    def add_note(take, start_beat, end_beat, pitch, vel, item_start_time):
        """Helper to insert a MIDI note using project beats."""
        start_time = item_start_time + get_proj_time(start_beat)
        end_time = item_start_time + get_proj_time(end_beat)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Step 2 & 3: Create Tracks & MIDI Data ===
    tracks_info = [
        {"name": f"{track_name} - Drums", "role": "drums"},
        {"name": f"{track_name} - Bass", "role": "bass"},
        {"name": f"{track_name} - Rhythm", "role": "rhythm"},
        {"name": f"{track_name} - Lead", "role": "lead"},
    ]

    beats_per_bar = 4
    item_length_sec = get_proj_time(bars * beats_per_bar)

    for info in tracks_info:
        # Create Track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", info["name"], True)
        
        # Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        item_start = 0.0
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", item_start)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Populate MIDI Notes based on role
        for bar in range(bars):
            bar_start_beat = bar * beats_per_bar
            chord_degree = progression[bar % len(progression)]
            
            # Diatonic Triad: Root, Third, Fifth
            chord = [chord_degree, chord_degree + 2, chord_degree + 4]

            if info["role"] == "drums":
                # Standard Drum mapping: Kick=36, Snare=38, Hat=42
                kick, snare, hat = 36, 38, 42
                # Kick on 1, 2.5, 3
                add_note(take, bar_start_beat + 0.0, bar_start_beat + 0.5, kick, velocity_base, item_start)
                add_note(take, bar_start_beat + 1.5, bar_start_beat + 2.0, kick, velocity_base - 10, item_start)
                add_note(take, bar_start_beat + 2.0, bar_start_beat + 2.5, kick, velocity_base, item_start)
                # Snare on 2, 4
                add_note(take, bar_start_beat + 1.0, bar_start_beat + 1.5, snare, velocity_base + 5, item_start)
                add_note(take, bar_start_beat + 3.0, bar_start_beat + 3.5, snare, velocity_base + 5, item_start)
                # 8th note Hats
                for i in range(8):
                    hat_vel = velocity_base if i % 2 == 0 else velocity_base - 20
                    add_note(take, bar_start_beat + (i * 0.5), bar_start_beat + (i * 0.5) + 0.25, hat, hat_vel, item_start)

            elif info["role"] == "bass":
                # Pumping 8th notes on the root, 2 octaves down
                bass_pitch = get_pitch(chord[0], -2)
                for i in range(8):
                    start = bar_start_beat + (i * 0.5)
                    add_note(take, start, start + 0.45, bass_pitch, velocity_base, item_start)

            elif info["role"] == "rhythm":
                # Sustained diatonic triad
                for note_degree in chord:
                    rhythm_pitch = get_pitch(note_degree, 0)
                    add_note(take, bar_start_beat, bar_start_beat + 4.0, rhythm_pitch, velocity_base - 15, item_start)

            elif info["role"] == "lead":
                # Up/down arpeggio: Root, 3rd, 5th, 3rd (1 octave up)
                arp_pattern = [0, 1, 2, 1, 0, 1, 2, 1] 
                for i, pattern_idx in enumerate(arp_pattern):
                    lead_pitch = get_pitch(chord[pattern_idx], 1)
                    start = bar_start_beat + (i * 0.5)
                    add_note(take, start, start + 0.4, lead_pitch, velocity_base + 10, item_start)

        # Sort MIDI events to ensure they play back correctly
        RPR.RPR_MIDI_Sort(take)

    # Optional: Set track colors, folder structure, etc., could go here

    return f"Created 4-track layered scaffold ('{track_name}') spanning {bars} bars in {key} {scale} at {bpm} BPM."
```