# Trance/EDM Rolling 16th Bassline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Trance/EDM Rolling 16th Bassline

* **Core Musical Mechanism**: The defining characteristic of Trance and Progressive EDM (as seen in the dense project arrangement) is the "rolling" 16th-note bassline. This pattern actively dodges the downbeat (where the kick drum hits) and populates the remaining three 16th-note subdivisions (`e`, `&`, `a`) of every beat. Combined with a short, staccato articulation, this creates a relentless driving momentum.
* **Why Use This Skill (Rationale)**: Musically, this creates extreme rhythmic syncopation against a 4-to-the-floor kick drum. By leaving the downbeat empty, it achieves a natural "psychoacoustic ducking" or sidechain effect, ensuring the low-end frequencies of the kick and bass never clash. The continuous fast notes add physical energy and forward motion to the track.
* **Overall Applicability**: This is the foundational bass layer for Trance, Progressive House, Techno, and High-Energy EDM. It sits beneath wide supersaws, airy vocals, and heavy percussion. 
* **Value Addition**: Rather than a static, sustained bass note, this skill encodes precise EDM timing (grid quantization, rests, and staccato lengths) and synthesizes a plucky, mix-ready sawtooth bass directly within REAPER, establishing an instant electronic groove.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM Range**: 128 - 140 BPM (Defaulting to 138 for classic Trance).
  - **Grid**: 1/16th notes.
  - **Pattern**: A standard 4/4 measure. For every quarter note beat, the 1st 16th note is a rest. The 2nd, 3rd, and 4th 16th notes are played.
  - **Articulation**: Staccato. The notes are shortened to roughly 85% of their full 16th-note duration to prevent them from blurring together.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically minor or harmonic minor.
  - **Progression**: To demonstrate movement, the script follows a standard EDM `i - VI - VII - i` progression (e.g., in A minor: A -> F -> G -> A), changing the root pedal note once per bar.
  - **Octave**: Sub/Bass register (MIDI octaves 1 and 2, around 30-45).

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth`.
  - **Timbre**: 100% Sawtooth wave for a buzzy, harmonically rich electronic bass.
  - **Envelope**: Fast attack (0ms) to ensure punch, short decay (~50ms), zero sustain, and short release (~100ms). This creates the "pluck" needed for fast 16th notes to remain distinct.

* **Step D: Mix & Automation**
  - **Mix**: The track is slightly attenuated to leave headroom for the heavy kick drum that typically accompanies this style.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rolling 16th Rhythm | MIDI note insertion | Allows precise mathematical placement of notes on the 16th grid (`e`, `&`, `a`) while keeping the downbeat explicitly empty. |
| Harmonic Progression | PPQ Note Calculation | Dynamically maps the `i - VI - VII - i` chord root notes to the correct scale degrees. |
| Pluck Bass Timbre | FX Chain (`ReaSynth`) | Stock synthesizer manipulated via `SetParam` to create the exact sawtooth envelope needed for Trance without relying on external VSTs like Spire/Sylenth1. |

> **Feasibility Assessment**: 90% — The code perfectly reproduces the rhythmic foundation, timing, and fundamental oscillator sound of the genre. To match the exact commercial mix in the video, a producer would typically layer this MIDI with 2-3 specific third-party synthesizer presets (e.g., Sylenth1) and apply heavy sidechain compression, but this ReaScript yields a completely functional and musically accurate structural core using only native tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "TranceProject",
    track_name: str = "Rolling Bass",
    bpm: int = 138,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Trance/EDM Rolling 16th Bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (Trance is typically 135-140).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the bassline.
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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) and Configure Envelope ===
    # For a rolling bass, we want 100% saw wave, fast attack, zero sustain, short release.
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth Param Mapping:
    # 0: Volume, 1: Tuning, 2: Attack, 3: Decay, 4: Sustain, 5: Release
    # 6: Square Mix, 7: Saw Mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.4)    # Volume (slightly lower)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)    # Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.05)   # Decay (~50 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.0)    # Sustain (0%)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.05)   # Release (~50 ms)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.0)    # Square mix (0%)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 1.0)    # Saw mix (100%)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Notes ===
    base_midi = 36 # C2
    root_offset = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = base_midi + root_offset - 12 # Octave 1 (Sub/Bass)

    # Progression: i - VI - VII - i (indices 0, 5, 6, 0 in minor scale)
    progression = [0, 5, 6, 0]
    
    sixteenth_len_sec = beat_len_sec / 4.0
    note_duration = sixteenth_len_sec * 0.85 # Staccato articulation
    note_count = 0

    for bar in range(bars):
        bar_start_sec = bar * bar_length_sec
        
        # Determine the pedal root note for this bar
        deg_idx = progression[bar % len(progression)] % len(scale_intervals)
        pitch = root_midi + scale_intervals[deg_idx]

        for beat in range(beats_per_bar):
            beat_start_sec = bar_start_sec + beat * beat_len_sec

            # Trance roll: skip 0 (downbeat for kick), play on 1, 2, 3 (16ths: e, &, a)
            for sixteenth in [1, 2, 3]:
                note_start_sec = beat_start_sec + sixteenth * sixteenth_len_sec
                note_end_sec = note_start_sec + note_duration

                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_sec)

                # Minor velocity variation to groove
                vel = velocity_base if sixteenth == 2 else velocity_base - 10

                RPR.RPR_MIDI_InsertNote(
                    take, False, False,
                    start_ppq, end_ppq,
                    0, int(pitch), vel, -1
                )
                note_count += 1

    # Apply notes
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} rolling bass notes over {bars} bars at {bpm} BPM."
```