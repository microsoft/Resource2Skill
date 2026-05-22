### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Arrangement (A-A-B Structural Variation)

* **Core Musical Mechanism**: The "Rule of 3" states that a musical idea (a melody, chord progression, or motif) should be introduced, repeated once to build familiarity (reinforcement), and then fundamentally altered or replaced on the third repetition to prevent listener fatigue. Structurally, this creates an **A-A-B** or **A-A-A'** phrase architecture.
* **Why Use This Skill (Rationale)**: The brain is a pattern-recognition machine. The first time we hear an idea, it peaks interest. The second time, we experience the pleasure of recognizing the pattern. By the third time, the brain automatically begins to "tune it out" because it is no longer novel. By introducing a variation precisely when the brain expects another identical loop, you re-capture attention and create musical momentum. 
* **Overall Applicability**: This applies everywhere: 4-bar chord loops in pop/hip-hop (where the 3rd 4-bar phrase breaks the loop), EDM drop synths, hi-hat triplet fills, and vocal phrasing. 
* **Value Addition**: Instead of a static, looping 8-bar or 16-bar block that drags on, this skill generates a dynamic 12-bar phrase that autonomously shifts harmony and melody right at the critical moment of listener fatigue, encoding professional arrangement structure natively.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Time Signature**: 4/4
  * **Pacing**: 4-bar phrases.
  * **Structure**: 
    * Bars 1-4 (Iteration 1: Introduce Idea A)
    * Bars 5-8 (Iteration 2: Reinforce Idea A)
    * Bars 9-12 (Iteration 3: Diverge to Idea B - The "Rule of 3" pivot)
* **Step B: Pitch & Harmony**
  * **Section A (Bars 1-8)**: A recognizable, looping progression. For example, a classic I - V - vi - IV progression.
  * **Section B (Bars 9-12)**: A contrasting progression that creates tension or moves to a different tonal center. For example, ii - V - I - vi, alongside a completely different, more active melody.
* **Step C: Sound Design & FX**
  * Uses synthesized keys or pads. In a stock DAW context, simple subtractive synthesis (ReaSynth) can effectively demonstrate the melodic and harmonic shifts.
* **Step D: Mix & Automation**
  * A slight jump in velocity or velocity variation on the B section helps emphasize the change in the arrangement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **A-A-B Form Logic** | Python Control Flow | Allows us to loop Section A twice, then branch into a separate Section B function/loop mathematically. |
| **Chord/Melody Generation** | MIDI Note Insertion (`RPR_MIDI_InsertNote`) | Provides exact control over scale degrees, voicing inversions, and rhythmic phrasing for the variations. |
| **Sound Generation** | FX Chain (`ReaSynth`) | Native REAPER instrument, guarantees the agent and user will hear the tonal shift without needing external sample libraries. |

> **Feasibility Assessment**: 100% reproducible. The compositional "Rule of 3" is an arrangement concept that perfectly translates to MIDI logic and DAW timeline population.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "RuleOf3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' arrangement (A-A-B structure) in REAPER.
    Generates 12 bars: 
      - Bars 1-4: Idea A
      - Bars 5-8: Idea A (Repeated)
      - Bars 9-12: Idea B (Variation)
    """
    import reaper_python as RPR

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0) + 48 # Octave 4
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    # Helper to get MIDI pitch from scale degree (1-indexed, e.g., 1=root, 2=second)
    def get_pitch(degree, octave_offset=0):
        deg_zero = degree - 1
        octave_shift = deg_zero // 7
        scale_idx = deg_zero % 7
        return root_midi + (octave_shift * 12) + scale_intervals[scale_idx] + (octave_offset * 12)

    # === Step 1: Initialize Project ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    ticks_per_beat = 960  # Standard MIDI PPQ
    ticks_per_bar = ticks_per_beat * beats_per_bar

    # === Step 2: Create Tracks ===
    def setup_track(name, synth_volume=-12.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        # Add basic Synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 10**(synth_volume/20))
        return track

    chords_track = setup_track(f"{track_name}_Chords", -14.0)
    melody_track = setup_track(f"{track_name}_Melody", -10.0)

    # === Step 3: Create Items & Takes ===
    total_length_sec = (60.0 / bpm) * beats_per_bar * 12
    
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)
    
    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", total_length_sec)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)

    # === Step 4: Arrangement Logic (The Rule of 3) ===
    # A Section Progression: I - V - vi - IV
    progression_a = [1, 5, 6, 4] 
    # B Section Progression (Variation): ii - V - I - vi
    progression_b = [2, 5, 1, 6]

    note_count = 0

    def add_chord(take, degree, start_bar, duration_bars=1):
        nonlocal note_count
        start_ppq = start_bar * ticks_per_bar
        end_ppq = start_ppq + (duration_bars * ticks_per_bar) - 60 # slight gap
        
        # Triad voicing (Root, 3rd, 5th)
        notes = [get_pitch(degree, -1), get_pitch(degree + 2, -1), get_pitch(degree + 4, -1)]
        for p in notes:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base, False)
            note_count += 1

    def add_melody_a(take, start_bar):
        nonlocal note_count
        # Simple rhythmic motif introducing the theme
        # Plays on beats 1, 2.5, and 4
        ppq_base = start_bar * ticks_per_bar
        rhythms = [(0, 1), (1.5, 1), (3, 1)] # (beat_start, beat_duration)
        degrees = [1, 2, 3]
        
        for i, (b_start, b_dur) in enumerate(rhythms):
            s_ppq = ppq_base + int(b_start * ticks_per_beat)
            e_ppq = s_ppq + int(b_dur * ticks_per_beat) - 30
            RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, get_pitch(degrees[i], 1), velocity_base + 10, False)
            note_count += 1

    def add_melody_b(take, start_bar):
        nonlocal note_count
        # Contrast motif: faster rhythm, higher register to break the repetition
        # Plays 8th notes
        ppq_base = start_bar * ticks_per_bar
        rhythms = [(0, 0.5), (0.5, 0.5), (1, 0.5), (2, 1.5)]
        degrees = [5, 4, 3, 2]
        
        for i, (b_start, b_dur) in enumerate(rhythms):
            s_ppq = ppq_base + int(b_start * ticks_per_beat)
            e_ppq = s_ppq + int(b_dur * ticks_per_beat) - 30
            RPR.RPR_MIDI_InsertNote(take, False, False, s_ppq, e_ppq, 0, get_pitch(degrees[i], 1), velocity_base + 15, False)
            note_count += 1

    # --- Generate the 12-Bar Form ---
    for bar in range(12):
        if bar < 4:
            # 1st Time: Introduce Idea A
            chord = progression_a[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_a(melody_take, bar)
            
        elif bar < 8:
            # 2nd Time: Reinforce Idea A (Exact Repeat)
            chord = progression_a[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_a(melody_take, bar)
            
        else:
            # 3rd Time: The "Rule of 3" Variation (Idea B)
            chord = progression_b[bar % 4]
            add_chord(chords_take, chord, bar)
            add_melody_b(melody_take, bar)

    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(melody_take)

    return f"Created Rule of 3 Arrangement (A-A-B structure): {note_count} notes over 12 bars at {bpm} BPM in {key} {scale}."
```