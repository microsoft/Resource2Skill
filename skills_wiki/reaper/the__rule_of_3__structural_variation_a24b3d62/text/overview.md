### 1. High-level Design Pattern Extraction

> **Skill Name**: The "Rule of 3" Structural Variation

* **Core Musical Mechanism**: Overcoming listener fatigue through structured unpredictability. The technique involves playing a musical phrase once to introduce it, repeating it a second time to solidify the pattern in the listener's ear, and then intentionally breaking the pattern on the third iteration (by introducing a new chord progression or melody). 
* **Why Use This Skill (Rationale)**: The brain constantly seeks patterns. When a musical idea is played the first time, it's novel and interesting. The second time, the brain recognizes it, creating a sense of satisfaction and groove. By the third repetition, the brain has fully predicted the outcome and begins to tune it out. Subverting this expectation on the third iteration creates surprise and releases dopamine, effectively re-hooking the listener's attention.
* **Overall Applicability**: This is a macro-arrangement skill applicable to chord progressions, melodies, drum fills, and basslines across all genres (Pop, EDM, Hip-Hop, Classical). It is typically applied to 4-bar phrases to create dynamic 12-bar or 16-bar song sections.
* **Value Addition**: This skill transforms a static, amateur 4-bar loop into a compelling, professional musical journey. By encoding the deviation mathematically, the generated MIDI has built-in tension and release.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/4 and 1/8 notes.
  - **Macro-Structure**: 12 Bars total (Three 4-bar blocks).
  - **Repetitions**: Block 1 and Block 2 are identical (Idea A). Block 3 deviates halfway through (Idea B).

* **Step B: Pitch & Harmony**
  - **Progression A (Bars 1-8)**: A generic, universally pleasing progression. Using relative scale degrees: IV - V - iii - vi (in Major) or iv - v - III - VI (in Minor). 
  - **Progression B (Bars 9-12)**: The "Rule of 3" deviation. The first two bars start the same (IV - V) to trick the listener, but the last two bars deviate down to ii - I (in Major) or ii° - i (in Minor).
  - **Melody**: A generative, mathematically linked motif. For the first 10 bars, it plays a simple quarter/half note rhythm hitting the 5th and 7th intervals of the underlying chord. On the 11th and 12th bars, the rhythm accelerates into 1/8th notes to physically emphasize the break in the pattern.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` to serve as a clean placeholder for the chords and melody.
  - **FX Chain**: `ReaDelay` added after the synth to provide spatial depth and smooth over the transitions between the structural blocks.

* **Step D: Mix & Automation**
  - The chords are struck 15 MIDI velocity points lower than the melody to ensure the lead motif sits clearly on top of the harmony, preventing frequency masking.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| 12-bar Rule of 3 Structure | MIDI note insertion | Allows precise, programmatic control over the chords and melody to guarantee the pattern breaks on exactly the 9th bar. |
| Relative Diatonic Harmony | Scale degree math | By computing pitches using `(degree + interval) % scale_length`, the progression automatically adapts to *any* key or scale the user inputs. |
| Timbre & Tone | FX chain (ReaSynth + ReaDelay) | Provides a standalone, audible reproduction of the piano/synth concept shown in the tutorial without requiring third-party VSTs. |

> **Feasibility Assessment**: 100% reproducible. The tutorial teaches a conceptual arrangement rule. This code translates that conceptual rule into a concrete MIDI generation algorithm that executes the exact 3-iteration structure advocated in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Concept",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # The Rule of 3 fundamentally requires 12 bars (3 iterations of 4 bars)
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a 12-bar composition demonstrating the 'Rule of 3' in the current REAPER project.
    Plays an idea twice, then breaks the pattern halfway through the third repetition.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Forces 12 bars to properly demonstrate the structural concept.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
    """
    import reaper_python as RPR

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

    root_midi = NOTE_MAP.get(key.upper(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)

    def get_pitch(degree, octave):
        """Converts a scale degree into an absolute MIDI pitch."""
        oct_offset = degree // scale_len
        rem_deg = degree % scale_len
        # +1 because octave 3 is MIDI note 48 (C3)
        return root_midi + (octave + oct_offset + 1) * 12 + scale_intervals[rem_deg]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # Hardcoded to 12 to fulfill the 'Rule of 3' iterations
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    def insert_note(pitch, start_beat, length_beats, velocity):
        """Helper to insert quantized notes using project time calculation."""
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    # Note generation loop over 3 identical-length blocks
    notes_created = 0
    for block in range(3):
        # The core of the Rule of 3:
        # Blocks 0 and 1 play Progression A. Block 2 plays Progression B.
        # Prog A: generic IV-V-iii-vi. Prog B starts same, but resolves differently.
        prog = [3, 4, 2, 5] if block < 2 else [3, 4, 1, 0]

        for bar, chord_deg in enumerate(prog):
            global_bar = (block * 4) + bar
            start_beat = global_bar * 4

            # --- 1. Generate Underlying Harmony (Chords) ---
            # Root, 3rd, 5th intervals
            for interval in [0, 2, 4]:
                chord_pitch = get_pitch(chord_deg + interval, 3) 
                insert_note(chord_pitch, start_beat, 4.0, max(10, velocity_base - 15))
                notes_created += 1

            # --- 2. Generate Lead Melody ---
            if bar < 2 or block < 2:
                # MOTIF 1: Predictable, establishing pattern
                insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base)
                insert_note(get_pitch(chord_deg + 4, 4), start_beat + 1.0, 1.0, velocity_base)
                insert_note(get_pitch(chord_deg + 2, 4), start_beat + 2.0, 2.0, velocity_base)
                notes_created += 3
            else:
                # MOTIF 2: The "Rule of 3" deviation / pattern break
                # Speeds up rhythmically to 1/8th notes to emphasize the structural change
                if bar == 2:
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base + 10)
                    insert_note(get_pitch(chord_deg + 4, 4), start_beat + 1.0, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 1.5, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 0, 4), start_beat + 2.0, 2.0, velocity_base)
                    notes_created += 4
                elif bar == 3:
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 0.0, 1.0, velocity_base + 10)
                    insert_note(get_pitch(chord_deg + 0, 4), start_beat + 1.0, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 1, 4), start_beat + 1.5, 0.5, velocity_base)
                    insert_note(get_pitch(chord_deg + 2, 4), start_beat + 2.0, 2.0, max(10, velocity_base - 10))
                    notes_created += 4

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # Add a stock synth and delay to give the pattern atmosphere
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, 1)

    return f"Created '{track_name}' demonstrating Rule of 3 ({notes_created} notes over {total_bars} bars at {bpm} BPM in {key} {scale})"
```