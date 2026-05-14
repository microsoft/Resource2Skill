### 1. High-level Design Pattern Extraction

> **Skill Name**: "Rule of 3" Arrangement Pattern (A-A-A' Form)

* **Core Musical Mechanism**: Structural and harmonic variation on the third repetition of a musical phrase. Instead of looping a 4-bar block endlessly, the first two iterations (A) establish a recognizable thematic motif and chord progression. The third iteration (A') begins exactly like the first two to "bait" the listener's expectation, but deviates halfway through with a new chord progression and melody contour. 

* **Why Use This Skill (Rationale)**: This technique exploits human psychoacoustics and pattern recognition. When an audience hears a phrase once, it piques their interest. A second repetition reinforces the idea and establishes a groove. By the third repetition, the brain has successfully predicted the pattern and begins to tune out ("habituation"). By introducing a structural variation (the A' section) exactly when the brain expects a perfect repeat, you break the habituation loop, recapturing attention and propelling the track forward into the next song section.

* **Overall Applicability**: Essential for moving from a "loop-based" production mindset into full song arrangement. This works in almost all modern genres—EDM, Hip-Hop, Pop, and Cinematic music. It is especially powerful for transitioning from a verse into a pre-chorus, or keeping a long 8-bar / 16-bar loop interesting.

* **Value Addition**: Compared to pasting a static 4-bar MIDI clip multiple times, this skill encodes narrative arrangement. It automatically generates 12 bars of music, handling the mathematical logic of the "bait and switch" to ensure your track remains dynamic.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 4/4 time signature, generated in a 12-bar macro block.
  - **Macro Structure**: Three phrases of 4 bars each (Bars 1-4, 5-8, 9-12).
  - **Melodic Rhythm**: The standard motif uses a syncopated 8th-note bounce on beat 2. The variation motif switches to straight, descending quarter notes to definitively signal a structural change.

* **Step B: Pitch & Harmony**
  - Uses dynamic scale degree mapping to work in any key/scale.
  - **A Section Chords (Phrases 1 & 2)**: I - V - vi - IV (Scale degrees 0, 4, 5, 3).
  - **A' Section Chords (Phrase 3 Variation)**: I - V - ii - V (Scale degrees 0, 4, 1, 4). The first two bars match the A section, but the final two pivot to create tension.
  - **Melody**: Arpeggiated chord tones with the root, third, fifth, and octave, following the underlying harmony.

* **Step C: Sound Design & FX**
  - **Chords Track**: Uses stock `ReaSynth` to create a foundational polyphonic pad.
  - **Melody Track**: Uses `ReaSynth` routed into `ReaDelay` to create a thematic lead that occupies a distinct spatial and rhythmic pocket from the chords.

* **Step D: Mix & Automation**
  - Volumes are managed via MIDI velocity. The pad notes are offset to be softer (`velocity_base - 20`), allowing the lead melody's downbeats (`velocity_base`) to cut through the mix clearly.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rule of 3 Arrangement | Algorithmic MIDI insertion | Allows mathematically perfect generation of the A-A-A' macro structure across dynamically selected keys and scales. |
| Thematic Lead / Pad Separation | Dual Track Creation | Creates an arrangement that is immediately audible and mixable, mirroring standard pop production routing. |
| Synth & Delay Setup | Stock FX Chains (`ReaSynth`, `ReaDelay`) | Guarantees self-contained reproducibility without requiring external VSTs or sample packs. |

> **Feasibility Assessment**: 100% reproduction of the musical theory and arrangement concept. The specific synth patches used in the video's piano roll are approximated using stock REAPER instruments, perfectly preserving the structural lesson.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOfThree",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 12-bar 'Rule of 3' arrangement (A-A-A' form) in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (minimum 12 recommended to hear the effect).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Rooted at octave 3

    def get_scale_note(degree, octave_offset=0):
        octave = degree // len(scale_intervals) + octave_offset
        idx = degree % len(scale_intervals)
        return root_midi + (octave * 12) + scale_intervals[idx]

    def clamp_vel(v):
        return max(1, min(127, int(v)))

    # Setup Timing
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    total_length_sec = bars * bar_length

    # Create Tracks
    track_idx = RPR.RPR_CountTracks(0)
    
    # 1. Chords Track
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_chords = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_chords, "P_NAME", f"{track_name}_Chords", True)
    item_chords = RPR.RPR_AddMediaItemToTrack(track_chords)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_chords, "D_LENGTH", total_length_sec)
    take_chords = RPR.RPR_AddTakeToMediaItem(item_chords)
    RPR.RPR_TrackFX_AddByName(track_chords, "ReaSynth", False, -1)

    # 2. Melody Track
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    track_mel = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(track_mel, "P_NAME", f"{track_name}_Melody", True)
    item_mel = RPR.RPR_AddMediaItemToTrack(track_mel)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_mel, "D_LENGTH", total_length_sec)
    take_mel = RPR.RPR_AddTakeToMediaItem(item_mel)
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_AddByName(track_mel, "ReaDelay", False, -1)

    # Progression Degrees (0-indexed)
    A_chords = [0, 4, 5, 3]        # I, V, vi, IV
    A_prime_chords = [0, 4, 1, 4]  # I, V, ii, V (The "Bait and Switch")

    chord_notes_list = []
    mel_notes_list = []

    # Generate Arrangement
    for bar in range(bars):
        phrase_idx = bar // 4
        bar_in_phrase = bar % 4

        # Rule of 3 Logic: On every 3rd phrase, vary the second half of the progression
        is_variation = (phrase_idx % 3 == 2) and (bar_in_phrase >= 2)
        chord_degree = A_prime_chords[bar_in_phrase] if is_variation else A_chords[bar_in_phrase]
        bar_start_time = bar * bar_length

        # Create Chords (Whole Notes)
        c_root = get_scale_note(chord_degree, 0)
        c_third = get_scale_note(chord_degree + 2, 0)
        c_fifth = get_scale_note(chord_degree + 4, 0)
        c_vel = clamp_vel(velocity_base - 20)
        
        chord_notes_list.extend([
            (bar_start_time, bar_start_time + bar_length, c_root, c_vel),
            (bar_start_time, bar_start_time + bar_length, c_third, c_vel),
            (bar_start_time, bar_start_time + bar_length, c_fifth, c_vel)
        ])

        # Create Melody
        if is_variation:
            # A' Melody: Straight descending quarter notes to signal a change
            m_data = [
                (0.0, 1.0, get_scale_note(chord_degree + 7, 1), clamp_vel(velocity_base)),
                (1.0, 2.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base)),
                (2.0, 3.0, get_scale_note(chord_degree + 2, 1), clamp_vel(velocity_base)),
                (3.0, 4.0, get_scale_note(chord_degree, 1),     clamp_vel(velocity_base))
            ]
        else:
            # A Melody: Syncopated 8th note bounce motif
            m_data = [
                (0.0, 1.0, get_scale_note(chord_degree, 1),     clamp_vel(velocity_base)),
                (1.0, 1.5, get_scale_note(chord_degree + 2, 1), clamp_vel(velocity_base - 15)),
                (1.5, 2.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base - 15)),
                (2.0, 3.0, get_scale_note(chord_degree + 7, 1), clamp_vel(velocity_base)),
                (3.0, 4.0, get_scale_note(chord_degree + 4, 1), clamp_vel(velocity_base - 10))
            ]

        for b_start, b_end, pitch, vel in m_data:
            start_sec = bar_start_time + (b_start * beat_length)
            end_sec = bar_start_time + (b_end * beat_length)
            mel_notes_list.append((start_sec, end_sec, pitch, vel))

    # Insert notes into REAPER items
    for start_sec, end_sec, pitch, vel in chord_notes_list:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_chords, end_sec)
        RPR.RPR_MIDI_InsertNote(take_chords, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    for start_sec, end_sec, pitch, vel in mel_notes_list:
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take_mel, end_sec)
        RPR.RPR_MIDI_InsertNote(take_mel, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_mel)

    return f"Created 'Rule of 3' arrangement across {bars} bars on tracks '{track_name}_Chords' and '{track_name}_Melody' in {key} {scale} at {bpm} BPM."
```