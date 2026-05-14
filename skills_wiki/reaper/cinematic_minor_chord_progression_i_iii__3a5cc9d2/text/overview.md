# Cinematic Minor Chord Progression (i - III - VI - V)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Minor Chord Progression (i - III - VI - V)

* **Core Musical Mechanism**: This pattern replicates the defining musical output of the tutorial's custom MIDI chord mapping: a powerful, four-chord minor key progression (Cm - Eb - Ab - G). It features diatonic movement through the minor scale (i, III, VI) before creating strong harmonic tension with a major dominant (V) chord that pulls relentlessly back to the tonic (i).

* **Why Use This Skill (Rationale)**: The inclusion of the major V chord (G major in the key of C minor) instead of the natural minor v chord (G minor) introduces the leading tone (B natural), creating a half-step resolution (B -> C) that makes the return home to the root feel incredibly satisfying. The movement from VI (Ab) to V (G) also creates dramatic descending half-step motion in the bass. This is a foundational concept in functional harmony used to evoke drama, triumph, or melancholy.

* **Overall Applicability**: This progression is a staple in cinematic orchestral music, pop anthems, trap/hip-hop, and deep house. It provides an immediate emotional foundation for a track, perfect for an intro pad, a dramatic chorus, or a driving bassline structure.

* **Value Addition**: Instead of manually plotting out complex chord voicings and ensuring correct voice leading, this skill automatically generates the full harmonic progression with tight, keyboard-style voicings (using inversions for the VI and V chords to minimize awkward jumping). It translates the tutorial's "one-finger chord" setup into an instantly usable MIDI item.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **BPM Range**: 90 - 130 BPM (flexible)
  - **Grid/Duration**: 2 beats (half note) per chord, creating a steady, foundational rhythmic pulse that loops cleanly every 2 bars.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Natural Minor (with a harmonic minor tweak on the V chord)
  - **Progression**: i - III - VI - V
  - **Specific Voicings (relative to C minor)**:
    - **Cm (i)**: C3, Eb3, G3 (Root position)
    - **Eb (III)**: Eb3, G3, Bb3 (Root position)
    - **Ab (VI)**: Ab2, C3, Eb3 (First inversion, dropped an octave for smoother voice leading from Eb)
    - **G (V)**: G2, B2, D3 (Root position, dropped an octave, featuring the major 3rd 'B' for harmonic tension)

* **Step C: Sound Design & FX**
  - **Instrument**: Native `ReaSynth` configured as a basic synth pad.
  - **FX Chain**: `ReaSynth` -> `ReaVerbate`
  - **ReaVerbate Settings**: Room size expanded (70%), Wet signal mixed at 30% to provide a lush, spacious tail appropriate for dramatic chords.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Progression | MIDI note insertion | Allows precise generation of chord voicings, inversions, and note durations without relying on external VST generators like "Chordz" (which are not native to REAPER). |
| Synth Tone | FX Chain (ReaSynth) | Provides a reliable, stock REAPER polyphonic sound source to immediately hear the chords. |
| Spatial depth | FX Chain (ReaVerbate) | Enhances the dramatic, cinematic feel of the chords without needing 3rd party reverbs. |

> **Feasibility Assessment**: 100% reproducible. While the tutorial specifically focuses on setting up a 3rd party VST (`Chordz`) to map these chords to single keys, we bypass the plugin entirely and script the *musical result* (the actual chord progression and voicings) directly into REAPER using native MIDI generation. This achieves the exact same auditory result with zero external dependencies.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Cinematic Minor Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a dramatic i - III - VI - V minor chord progression on a new track.
    Replicates the custom chord sequence demonstrated in the tutorial.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., C, D#, F).
        scale: Ignored internally as this specifically builds a minor progression.
        bars: Number of bars to generate (progression loops every 2 bars).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
    """
    import reaper_python as RPR

    # Base note mappings (Octave 3)
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}

    root_note = NOTE_MAP.get(key.upper(), 48)

    # Chord structure definitions (intervals from chord root)
    minor_triad = [0, 3, 7]
    major_triad = [0, 4, 7]

    # The i - III - VI - V Progression (Relative to Key Root)
    # Voicings are adjusted (offsets) to keep the chords close together on the keyboard
    progression = [
        {"name": "i",   "offset": 0,  "intervals": minor_triad}, # e.g., Cm  (C3, Eb3, G3)
        {"name": "III", "offset": 3,  "intervals": major_triad}, # e.g., Eb  (Eb3, G3, Bb3)
        {"name": "VI",  "offset": -4, "intervals": major_triad}, # e.g., Ab  (Ab2, C3, Eb3)
        {"name": "V",   "offset": -5, "intervals": major_triad}  # e.g., G   (G2, B2, D3)
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes ===
    beats_per_chord = 2.0  # Half note chords
    total_beats = bars * beats_per_bar
    total_chords = int(total_beats // beats_per_chord)

    notes_created = 0
    for c in range(total_chords):
        chord_data = progression[c % 4] # Loop the 4 chords
        
        start_qn = c * beats_per_chord
        end_qn = start_qn + beats_per_chord
        
        # Convert Quarter Notes to PPQ (Pulses Per Quarter Note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        # Add a tiny gap between chords for articulation
        end_ppq -= 20 
        
        for interval in chord_data["intervals"]:
            pitch = root_note + chord_data["offset"] + interval
            # Ensure pitch stays in valid MIDI range
            pitch = max(0, min(127, pitch)) 
            
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Synth & Reverb) ===
    # Add a basic synth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume slightly to prevent clipping on block chords
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 0, 0.4) 

    # Add Reverb for cinematic space
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 0, 0.3) # Wet signal
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 1, 0.9) # Dry signal
    RPR.RPR_TrackFX_SetParamNormalized(track, 1, 2, 0.7) # Room size

    return f"Created '{track_name}' with {notes_created} notes (i-III-VI-V progression) over {bars} bars at {bpm} BPM in {key} minor."
```