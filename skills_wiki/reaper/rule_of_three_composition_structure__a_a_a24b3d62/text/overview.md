### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of Three Composition Structure (A-A-A')

* **Core Musical Mechanism**: The "Rule of Three" is a structural and psychological pattern in music composition. It dictates that a musical phrase or idea should be repeated exactly once to establish familiarity and reinforce the pattern (Iterations 1 and 2). However, on the third iteration, the brain habituates and begins to lose interest. To capture attention, the third iteration must introduce a variation (either a completely new idea "B", or a variation of the original idea "A'"). 

* **Why Use This Skill (Rationale)**: Human brains are pattern-matching engines. Hearing an idea once introduces it. Hearing it twice establishes a pattern, which feels satisfying. Hearing it a third time exactly the same way causes the brain to tune out, as it has already successfully predicted the outcome. Diverging on the third repetition (e.g., starting the same but changing the chord progression at the end) breaks the expectation, releasing dopamine and re-engaging the listener. 

* **Overall Applicability**: This applies to nearly all linear music production: programming drum loop variations, writing chord progressions, structuring melodies, and arranging song sections (e.g., Verse 1, Verse 2, Pre-Chorus). 

* **Value Addition**: Compared to a looped 4-bar MIDI clip, this skill creates a dynamic 12-bar macro-structure. It encodes the psychology of listener expectation by automatically generating the necessary turnaround/variation on the third repetition, preventing a track from feeling repetitive or amateurish.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / Grid**: 4/4 time, quantized to the beat.
  - **Structure**: 12 bars total, broken into three 4-bar phrases.
  - **Note Durations**: Whole notes for the bass root, accompanied by pulsing half-notes for the upper chord voicings to maintain rhythmic momentum.

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Parametric (Defaults to C Major).
  - **Phrase 1 & 2 (Idea A)**: A descending/resolving diatonic progression. Using 0-indexed scale degrees: IV - V - vi - iii (Degrees 3, 4, 5, 2). 
  - **Phrase 3 (Idea A')**: Starts identical to Idea A to build the expectation of a third loop, but diverges in the last two bars into a turnaround: IV - V - ii - V (Degrees 3, 4, 1, 4).
  - **Voicing**: Root in the bass (2 octaves down), standard root-position triads in the right hand (root, 3rd, 5th of the chord).

* **Step C: Sound Design & FX**
  - **Instrument**: REAPER's stock `ReaSynth`.
  - **Timbre**: Configured to act as a soft electric piano/pad. Saw wave mix is turned down to create a pure sine/triangle-like tone, preventing harshness while clearly demonstrating the harmonic structure.

* **Step D: Mix & Automation**
  - **Volume**: ReaSynth output normalized to 0.3 (-10dB) to leave headroom. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rule of Three Structure | MIDI note insertion | Allows us to explicitly program the A-A-A' variation over 12 bars using music theory logic. |
| Harmonic Progression | Scale/Degree Math | Calculates specific intervals dynamically so the pattern works in any key/scale passed to the function. |
| Sound Source | FX Chain (`ReaSynth`) | Provides a clean, stock-REAPER audio source to instantly audition the structural turnaround without requiring third-party VSTs. |

> **Feasibility Assessment**: 100% of the *compositional principle* taught in the video is reproduced. The specific sampled piano VST the creator used is substituted with a stock ReaSynth soft pad to ensure zero external dependencies, while the exact chord progression variation technique is perfectly replicated via MIDI.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "RuleOfThree",
    track_name: str = "Rule Of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of Three' A-A-A' chord progression structure in the current REAPER project.
    
    Demonstrates the psychological composition rule:
    - Bars 1-4: Idea A (IV - V - vi - iii)
    - Bars 5-8: Idea A (Repeated for reinforcement)
    - Bars 9-12: Idea A' (Starts same, diverges to ii - V turnaround)

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars. Defaults to 12. If > 12, loops the A-A-A' structure.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
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

    import reaper_python as RPR

    # Safety checks
    if key not in NOTE_MAP:
        key = "C"
    if scale not in SCALES:
        scale = "major"
        
    current_scale = SCALES[scale]
    root_midi = NOTE_MAP[key] + 60  # Middle octave (e.g., C4)
    
    # Enforce minimum of 12 bars to properly demonstrate the rule of 3
    total_bars = max(12, bars)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) ===
    # Add ReaSynth and make it a soft sine/pad tone
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.3)  # Volume lower
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 1, 0.0)  # Saw mix to 0 (pure sine)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.5)  # Attack up slightly
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.6)  # Release up slightly

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to get scale pitches dynamically
    def get_scale_pitch(root, scale_arr, degree):
        octave_offset = degree // len(scale_arr)
        scale_degree = degree % len(scale_arr)
        return int(root + (octave_offset * 12) + scale_arr[scale_degree])

    note_count = 0

    # === Step 5: Generate Structural Notes ===
    for bar in range(total_bars):
        # Determine where we are in the 12-bar (A-A-A') cycle
        phase = (bar // 4) % 3  # 0: Idea A, 1: Idea A (repeat), 2: Idea A' (variation)
        bar_in_phrase = bar % 4
        
        if phase == 0 or phase == 1:
            # Idea A: IV - V - vi - iii
            chord_deg = [3, 4, 5, 2][bar_in_phrase]
        else:
            # Idea A': IV - V - ii - V (Variation/Turnaround)
            chord_deg = [3, 4, 1, 4][bar_in_phrase]

        bar_start_beat = bar * 4

        # 1. Add sustained bass note (2 octaves down)
        start_time = bar_start_beat * (60.0 / bpm)
        end_time = (bar_start_beat + 4) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

        bass_pitch = get_scale_pitch(root_midi, current_scale, chord_deg - 14) 
        
        # Keep pitch within safe MIDI bounds
        bass_pitch = max(0, min(127, bass_pitch))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, True)
        note_count += 1

        # 2. Add pulsing chord in the right hand (two half-notes per bar)
        for half in range(2):
            h_start = (bar_start_beat + half * 2) * (60.0 / bpm)
            h_end = (bar_start_beat + half * 2 + 1.8) * (60.0 / bpm)  # 1.8 leaves a slight rhythmic gap
            h_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, h_start)
            h_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, h_end)

            # Insert Root, 3rd, and 5th of the chord
            for interval in [0, 2, 4]:
                chord_pitch = get_scale_pitch(root_midi, current_scale, chord_deg - 7 + interval)
                chord_pitch = max(0, min(127, chord_pitch))
                
                # Make the chord hits slightly softer than the bass
                RPR.RPR_MIDI_InsertNote(take, False, False, h_start_ppq, h_end_ppq, 0, chord_pitch, velocity_base - 15, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating Rule of 3. Generated {note_count} notes over {total_bars} bars at {bpm} BPM in {key} {scale}."
```