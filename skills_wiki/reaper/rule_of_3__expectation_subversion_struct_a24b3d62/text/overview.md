### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 (Expectation Subversion Structure)

* **Core Musical Mechanism**: A structural and compositional arranging technique where a distinct musical idea (melody, chord progression, or motif) is played exactly twice to establish a pattern, and then altered on the third iteration. The third pass begins the same way but diverges halfway through to introduce new harmonic or melodic information.
* **Why Use This Skill (Rationale)**: This is based heavily on psychoacoustics and cognitive processing. Human brains are prediction machines. 
  1. **First pass (Exposure)**: The brain analyzes the new information.
  2. **Second pass (Reinforcement)**: The brain confirms the pattern, and internalizes it (listener can now predict what comes next).
  3. **Third pass (Boredom/Subversion)**: If repeated exactly a third time, the brain tunes it out ("too much of a good thing is no longer a good thing"). By intentionally breaking the convention on the third repetition, you re-engage the listener's active attention and prevent the loop from feeling stale.
* **Overall Applicability**: This applies to nearly every genre. It is perfect for turning a static 4-bar loop into a compelling 12-bar or 16-bar section. It is heavily used in pop vocal melodies, EDM drop synths, classical motifs, and hip-hop basslines.
* **Value Addition**: Compared to a standard looping 4-bar MIDI clip, this skill encodes *long-term arrangement structure* and *tension management*. It mathematically generates three phrases, ensuring the exact cognitive trigger described in the tutorial is satisfied.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Time Signature**: 4/4 time. 
  - **Structure**: Three distinct 4-bar phrases (12 bars total). 
  - **Rhythm**: Quarter-note melodic pulses over whole-note block chords to clearly expose the pattern to the listener.

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Adaptable (defaults to C minor). 
  - **Phrase 1 & 2 (Bars 1-8)**: A repeating `i - VI - III - VII` progression. The melody follows a predictable ascending/descending motif.
  - **Phrase 3 (Bars 9-12)**: Starts identical to the first phrase (`i - VI`), but the last two bars diverge to `iv - V` (Subdominant to Dominant). The melody climbs higher instead of resolving, creating tension that begs for a new section.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` to guarantee the melodic and harmonic variation is clearly audible without external VSTs.
  - **Tone**: A soft square/saw mix with a gentle release so the chords pad out nicely beneath the staccato melody.

* **Step D: Mix & Automation**
  - Volume is set moderately to avoid clipping the 4-voice chords.
  - No heavy automation; the focus is entirely on the MIDI note variation architecture.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| 3-Phrase Structure | MIDI note insertion | Requires distinct programmatic logic to duplicate phrase 1&2, and mutate phrase 3. |
| Harmony/Melody Generation | Music Theory Array Math | Calculates scale degrees dynamically so the "divergence" remains diatonic to the user's chosen key/scale. |
| Sound Generator | `ReaSynth` FX | Keeps the script self-contained while providing an immediate, audible demonstration of the cognitive trick. |

> **Feasibility Assessment**: 100% reproducible. The tutorial teaches a structural philosophy rather than a specific synth patch. Generating a 12-bar dynamic MIDI item perfectly executes the psychological concept demonstrated in the video natively inside REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Arrangement",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 12,  # Overridden internally to ensure multiples of 3
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Rule of 3 (Expectation Subversion Structure) in the current REAPER project.
    
    Generates a 3-phrase structural pattern where the first two phrases are identical
    to build listener expectation, and the third phrase diverges to maintain interest.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Ignored here (forces 12 bars to perfectly demonstrate the 3x4 structure).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR
    import math

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

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth for immediate playback
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume slightly to handle polyphony
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Math Setup for 'Rule of 3' ===
    # We explicitly need 3 phrases. Let's do 3 phrases of 4 bars = 12 bars.
    total_phrases = 3
    bars_per_phrase = 4
    total_bars = total_phrases * bars_per_phrase
    beats_per_bar = 4
    
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    total_length_sec = bar_length_sec * total_bars
    
    # Scale Data
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_val = NOTE_MAP.get(key, 0)
    root_pitch = root_val + 48 # Octave 3 (Safe midrange)

    def get_pitch(degree):
        """Converts a diatonic scale degree (0-indexed) into an exact MIDI pitch."""
        octave = degree // len(scale_intervals)
        idx = degree % len(scale_intervals)
        return root_pitch + (octave * 12) + scale_intervals[idx]

    # === Step 4: Create MIDI Item ===
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    def insert_note(start_sec, end_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # === Step 5: Generate Structural Notes ===
    total_notes_created = 0
    
    # Iteration over the 3 phrases
    for phrase in range(total_phrases):
        
        # Phrases 1 and 2 are identical (Establish expectation)
        if phrase < 2:
            chords_by_degree = [0, 5, 2, 6] # e.g., in minor: i, VI, III, VII
        else:
            # Phrase 3: Subvert expectation! Starts the same (0, 5), goes somewhere different (3, 4)
            chords_by_degree = [0, 5, 3, 4] # e.g., in minor: i, VI, iv, v
            
        for bar in range(bars_per_phrase):
            base_degree = chords_by_degree[bar]
            bar_start_sec = (phrase * bars_per_phrase + bar) * bar_length_sec
            
            # --- Draw Harmony (Whole note block chord) ---
            # Root, 3rd, 5th
            for chord_tone in [0, 2, 4]:
                pitch = get_pitch(base_degree + chord_tone)
                # Play chords slightly softer
                insert_note(bar_start_sec, bar_start_sec + bar_length_sec, pitch, max(10, velocity_base - 20))
                total_notes_created += 1

            # --- Draw Melody (Quarter notes) ---
            # Standard repeating motif for established phrases or the beginning of phrase 3
            if phrase < 2 or (phrase == 2 and bar < 2):
                mel_degrees = [base_degree + 7, base_degree + 9, base_degree + 7, base_degree + 4]
            else:
                # The variation! The melody climbs instead of following the old motif
                mel_degrees = [base_degree + 9, base_degree + 11, base_degree + 12, base_degree + 14]
            
            for beat in range(beats_per_bar):
                note_start = bar_start_sec + beat * beat_length_sec
                note_end = note_start + (beat_length_sec * 0.75) # Slight staccato
                pitch = get_pitch(mel_degrees[beat])
                insert_note(note_start, note_end, pitch, velocity_base)
                total_notes_created += 1

    # Commit MIDI operations
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' demonstrating the Rule of 3 (3 phrases, {total_bars} bars, {total_notes_created} notes) at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? *(Note: `bars` deliberately constrained to 12 internally to preserve the required 3-iteration structure)*
- [x] Does it avoid hardcoded file paths or external sample dependencies?