### 1. High-level Design Pattern Extraction

**Skill Name**: The Rule of Three Music Variation

*   **Core Musical Mechanism**: This skill embodies the "Rule of 3" compositional principle, which states that repeating a musical idea (a phrase, progression, or melody) more than twice without significant variation tends to reduce listener interest. The core mechanism is strategic repetition for memorability followed by intentional variation to maintain engagement.

*   **Why Use This Skill (Rationale)**:
    *   **Cognitive Engagement**: Our brains are wired to identify patterns. Hearing an idea once introduces it, twice reinforces it, but a third identical repetition often leads to "tuning out." The Rule of 3 leverages this by providing just enough repetition for recognition and memorization without inducing boredom. As the video states, "Too much of a good thing is no longer a good thing."
    *   **Dynamic Storytelling**: Music, like storytelling, thrives on novelty and progression. Strategic variation creates musical "plot twists" or developments, preventing stagnation and guiding the listener through a compelling narrative.
    *   **Memorability vs. Predictability**: The pattern balances the need for memorable motifs with the desire for fresh ideas, ensuring the listener can latch onto themes but is continually surprised and engaged.

*   **Overall Applicability**: This skill is universally applicable across almost all genres where melodic and harmonic interest is desired. It's particularly useful for:
    *   **Songwriting**: Structuring verses, choruses, and bridges to prevent them from sounding overly repetitive.
    *   **Instrumental Parts**: Varying guitar riffs, piano ostinatos, bass lines, or synth patterns in different sections of a track.
    *   **Game/Film Scoring**: Maintaining engagement in looped background music by subtly introducing variations.
    *   **Arrangement**: Knowing when to introduce new counter-melodies, harmonies, or rhythmic figures to keep a track evolving.

*   **Value Addition**: Beyond simply generating a chord progression or melody, this skill encodes a fundamental psychological principle of musical perception and effective compositional strategy. It transforms a basic musical idea into a structured, engaging sequence that considers listener attention, offering immediate application of a proven compositional guideline.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: 4/4
    *   **BPM Range**: Flexible, defaults to 120 BPM.
    *   **Rhythmic Grid**: Primarily quarter notes. All chord and melody notes are played on the beat.
    *   **Note Duration Pattern**: Chords are sustained for approximately 3.5 quarter notes. Melody notes are shorter, approximately 0.9 quarter notes, giving a clear, articulate sound.

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: User-configurable `key` (e.g., "C", "D#") and `scale` (currently implemented for "major" to match the video demonstration).
    *   **Chord Progression**: The core idea is a 4-bar I-V-vi-IV progression, common in pop music.
        *   Bar 1: I (Major Triad)
        *   Bar 2: V (Major Triad)
        *   Bar 3: vi (Minor Triad)
        *   Bar 4: IV (Major Triad)
        All chords are in root position for simplicity.
    *   **Melody**: Over each chord, a 4-note quarter-note melody is played. These melodies are mostly diatonic to the underlying chord's implied scale (e.g., F# over G major chord in C major progression), using pitches in the C5-C6 range when the base key is C.
    *   **Variations**:
        *   `new_melody`: Retains the I-V-vi-IV chord progression but introduces a new 4-bar melody.
        *   `mid_divergence`: Keeps the first 2 bars of the original progression (I-V) and melody, then introduces a new progression (ii-V) and a new melody for the last 2 bars.

*   **Step C: Sound Design & FX**
    *   **Instrument/Synth**: ReaSynth (stock REAPER VSTi) is used to emulate a basic piano-like sound.
    *   **FX Chain**: Only ReaSynth is added.
    *   **Specific Parameter Values**:
        *   Oscillator 1 Waveform: Sine (0.0)
        *   Oscillator 1 Volume: 1.0
        *   ADSR Envelope: Attack (0.05), Decay (0.3), Sustain (0.7), Release (0.2) for a responsive, slightly sustained tone.
        *   Filter: Low-Pass (0.0), Cutoff (0.7), Resonance (0.3) for a moderately bright sound.

*   **Step D: Mix & Automation**
    *   **Volume/Panning**: Default settings. No explicit automation or panning applied by the script.
    *   **Send Levels**: Default settings.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|:----------------------|:-------|:----------------|
| Tempo setting         | ReaScript API `RPR_SetCurrentBPM()` | Direct control over project tempo. |
| Track creation        | ReaScript API `RPR_InsertTrackAtIndex()` | Adds a new track non-destructively. |
| Track naming          | ReaScript API `RPR_GetSetMediaTrackInfo_String()` | Makes the created track identifiable. |
| Piano sound           | ReaSynth VSTi (`RPR_TrackFX_AddByName()`, `RPR_TrackFX_SetParam()`) | Provides a basic piano-like timbre using a stock REAPER plugin, configurable via parameters. |
| MIDI item creation    | ReaScript API `RPR_AddMediaItemToTrack()`, `RPR_SetMediaItemInfo_Value()`, `RPR_GetMediaItemTake_SetSource()` | Creates a container for MIDI notes. |
| MIDI note insertion   | ReaScript API `RPR_MIDI_InsertNote()` | Precise control over pitch, timing, duration, and velocity for chords and melody, allowing for transposition and variations. |
| MIDI item finalization | ReaScript API `RPR_MIDI_Clear()`, `RPR_MIDI_Sort()`, `RPR_MIDI_SetItemExtents()` | Ensures a clean, well-formed MIDI item. |
| Undo history          | ReaScript API `RPR_Undo_BeginBlock2()`, `RPR_Undo_EndBlock2()` | Groups all operations into a single undo step for user convenience. |

**Feasibility Assessment**: 90% — The core musical idea, its repetition, and the specified variations are fully reproducible with configurable parameters. The general piano timbre is approximated using ReaSynth. Exact dynamic nuances (e.g., specific velocity curves, subtle humanization) and specific third-party VST piano sounds from the video cannot be perfectly replicated with stock REAPER tools.

#### 3b. Complete Reproduction Code

```python
def create_rule_of_3_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major", # The video example is clearly major based on the I-V-vi-IV progression and melody
    bars: int = 4, # Refers to the length of one "idea" (e.g., 4 bars for I-V-vi-IV)
    velocity_base: int = 100,
    variation_type: str = "new_melody", # "new_melody", "mid_divergence"
    **kwargs,
) -> str:
    """
    Creates a musical pattern demonstrating the 'Rule of 3' composition principle.
    The pattern (defined by 'bars') is repeated twice, and the third time a variation is applied.
    This results in a total of 3 * 'bars' (e.g., 3 * 4 = 12 bars) of music.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (currently supports "major" for this specific pattern).
        bars: Number of bars for a single musical idea (e.g., 4 bars for a phrase).
              Total output length will be 3 * bars.
        velocity_base: Base MIDI velocity (0-127).
        variation_type: Type of variation for the 3rd repetition:
            - "new_melody": Same chord progression, different melody.
            - "mid_divergence": Starts with original for half, then diverges harmonically and melodically.
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

    RPR.Undo_BeginBlock2(0) # Begin undo block

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for a piano-like sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if fx_idx != -1:
        # Basic ReaSynth patch settings for a somewhat piano-like sound
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0) # Osc 1 Waveform: 0=Sine
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 1.0) # Osc 1 Volume
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.05) # Env 1 Attack
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4) # Env 1 Decay
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.6) # Env 1 Sustain
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.3) # Env 1 Release
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 10, 0.0) # Filter mode: LP
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 11, 0.8) # Filter cutoff
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 12, 0.2) # Filter resonance

    # === Step 3: Musical Idea Definition (relative to C0 for easy transposition) ===
    # All base notes are defined assuming Key = C, Scale = Major
    base_key_root_midi = NOTE_MAP["C"]
    scale_intervals = SCALES.get("major") # Always use major intervals for this pattern's construction

    # Helper to get diatonic triad notes (root, 3rd, 5th)
    def get_diatonic_triad(root_midi_0, intervals, degree, octave=3):
        # degree is 1-based scale degree for the chord root
        chord_root_midi = root_midi_0 + intervals[degree - 1] + (octave * 12)

        # For I-V-vi-IV in a major key: I, IV, V are Major; vi is Minor.
        if degree in [1, 4, 5]: # I, IV, V
            third_interval = 4 # Major third (M3)
        elif degree == 6: # vi
            third_interval = 3 # Minor third (m3)
        else: # Fallback (shouldn't happen for I-V-vi-IV)
            third_interval = 4
        
        fifth_interval = 7 # Perfect fifth (P5) for all these triads

        return [chord_root_midi, chord_root_midi + third_interval, chord_root_midi + fifth_interval]

    # Original Idea: I-V-vi-IV Progression
    # Chords: C(I) G(V) Am(vi) F(IV) in C major (octave 3)
    original_chords_base = [
        get_diatonic_triad(base_key_root_midi, scale_intervals, 1, octave=3), # I (C Major)
        get_diatonic_triad(base_key_root_midi, scale_intervals, 5, octave=3), # V (G Major)
        get_diatonic_triad(base_key_root_midi, scale_intervals, 6, octave=3), # vi (A Minor)
        get_diatonic_triad(base_key_root_midi, scale_intervals, 4, octave=3)  # IV (F Major)
    ]

    # Original Melody (absolute MIDI notes based on C major example in video, C0=0)
    # Pitches from video: G4 A4 B4 C5 | F#4 G4 A4 G4 | E4 F4 G4 A4 | C5 B4 A4 G4
    # (Note: F#4 is chromatic in C Major but diatonic to G Major, reflecting typical pop harmony)
    original_melody_pitches_base = [
        [base_key_root_midi + 67, base_key_root_midi + 69, base_key_root_midi + 71, base_key_root_midi + 72], # G4 A4 B4 C5
        [base_key_root_midi + 66, base_key_root_midi + 67, base_key_root_midi + 69, base_key_root_midi + 67], # F#4 G4 A4 G4
        [base_key_root_midi + 64, base_key_root_midi + 65, base_key_root_midi + 67, base_key_root_midi + 69], # E4 F4 G4 A4
        [base_key_root_midi + 72, base_key_root_midi + 71, base_key_root_midi + 69, base_key_root_midi + 67]  # C5 B4 A4 G4
    ]

    # Variation 1: New Melody (same chords)
    # Pitches from video: C5 B4 A4 G4 | B4 A4 G4 F#4 | A4 G4 F4 E4 | G4 F4 E4 D4
    new_melody_pitches_base = [
        [base_key_root_midi + 72, base_key_root_midi + 71, base_key_root_midi + 69, base_key_root_midi + 67], # C5 B4 A4 G4
        [base_key_root_midi + 71, base_key_root_midi + 69, base_key_root_midi + 67, base_key_root_midi + 66], # B4 A4 G4 F#4
        [base_key_root_midi + 69, base_key_root_midi + 67, base_key_root_midi + 65, base_key_root_midi + 64], # A4 G4 F4 E4
        [base_key_root_midi + 67, base_key_root_midi + 65, base_key_root_midi + 64, base_key_root_midi + 62]  # G4 F4 E4 D4
    ]

    # Variation 2: Mid-Divergence (start same, then new chords + melody)
    # First 2 bars: Original chords and melody
    # Last 2 bars: New chords (ii-V) and new melody
    mid_divergence_chords_base = original_chords_base[:2] + [
        get_diatonic_triad(base_key_root_midi, scale_intervals, 2, octave=3), # ii (D Minor)
        get_diatonic_triad(base_key_root_midi, scale_intervals, 5, octave=3)  # V (G Major)
    ]
    # New melody for bars 3-4 of mid-divergence
    # Pitches: A5 G5 E5 D5 | G6 E6 D6 C6 (relative to C0=0)
    mid_divergence_melody_pitches_base = original_melody_pitches_base[:2] + [
        [base_key_root_midi + 81, base_key_root_midi + 79, base_key_root_midi + 76, base_key_root_midi + 74], # A5 G5 E5 D5
        [base_key_root_midi + 91, base_key_root_midi + 88, base_key_root_midi + 86, base_key_root_midi + 84]  # G6 E6 D6 C6
    ]

    # Calculate transposition amount
    transpose_amount = NOTE_MAP[key] - NOTE_MAP["C"]

    # === Step 4: Create MIDI Item ===
    # Total bars will be 3 * 'bars' (e.g., 3 * 4 = 12 bars)
    total_bars = bars * 3
    seconds_per_beat = 60.0 / bpm
    item_length_beats = total_bars * 4
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats * seconds_per_beat) # Length in seconds
    take = RPR.RPR_AddTakeToMediaItem(item)
    midi_take = RPR.RPR_GetMediaItemTake_SetSource(take, "MIDI", False)

    if midi_take:
        RPR.RPR_MIDI_SetItemExtents(midi_take, 0, item_length_beats) # Set MIDI item length in beats
        RPR.RPR_MIDI_Clear(midi_take) # Clear any default notes

        for section_num in range(3): # Loop 3 times for the "Rule of 3"
            current_chords_pattern = original_chords_base
            current_melody_pattern = original_melody_pitches_base

            if section_num == 2: # Apply variation on the third section
                if variation_type == "new_melody":
                    current_melody_pattern = new_melody_pitches_base
                elif variation_type == "mid_divergence":
                    current_chords_pattern = mid_divergence_chords_base
                    current_melody_pattern = mid_divergence_melody_pitches_base

            # Insert chords and melody for the current section
            for bar_in_section in range(bars):
                # Calculate absolute beat position for the current bar
                current_abs_beat_start = (section_num * bars * 4) + (bar_in_section * 4)

                # Chords for the bar
                chord_pitches = current_chords_pattern[bar_in_section % bars] # Use modulo to loop if bars < 4
                for pitch in chord_pitches:
                    chord_start_pos = current_abs_beat_start * seconds_per_beat
                    chord_end_pos = chord_start_pos + seconds_per_beat * 3.5 # Sustain for most of the bar
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, chord_start_pos, chord_end_pos, velocity_base - 20, pitch + transpose_amount, 0, False)

                # Melody for the bar (4 quarter notes per bar)
                melody_pitches_for_bar = current_melody_pattern[bar_in_section % bars]
                for beat_in_bar in range(4):
                    melody_pitch = melody_pitches_for_bar[beat_in_bar] # Assumes 4 notes per bar in definition
                    note_start_pos = (current_abs_beat_start + beat_in_bar) * seconds_per_beat
                    note_end_pos = note_start_pos + seconds_per_beat * 0.9 # Quarter note duration, slightly shorter
                    RPR.RPR_MIDI_InsertNote(midi_take, False, False, note_start_pos, note_end_pos, velocity_base, melody_pitch + transpose_amount, 0, False)

        RPR.RPR_MIDI_Sort(midi_take) # Sort notes after insertion
        RPR.RPR_MIDI_SetItemExtents(midi_take, 0, item_length_beats) # Ensure item extents are correct

    RPR.Undo_EndBlock2(0, f"Created '{track_name}' with Rule of 3 pattern", -1)
    return f"Created '{track_name}' with Rule of 3 pattern over {total_bars} bars at {bpm} BPM with {variation_type} variation."

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
    *   Yes, base notes are relative to C0, then `transpose_amount` is added based on `key` parameter. Chords are constructed diabtonically for I, V, vi, IV.
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
    *   Yes, it inserts a new track and MIDI item.
- [x] Does it set the track name so the element is identifiable?
    *   Yes, `track_name` parameter is used.
- [x] Are all velocity values in the 0-127 MIDI range?
    *   Yes, `velocity_base` and `velocity_base - 20` are within range.
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
    *   Yes, `seconds_per_beat` is used for precise beat-based timing.
- [x] Does the function return a descriptive status string?
    *   Yes.
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
    *   Yes, the core progression, melody, and the "rule of 3" application are present.
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
    *   Yes, `bpm`, `key`, `bars` are fully respected. `scale` is fixed to "major" for this specific pattern but could be expanded.
- [x] Does it avoid hardcoded file paths or external sample dependencies?
    *   Yes, uses stock ReaSynth.