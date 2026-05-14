# Algorithmic Chord Arpeggiation (Random & Sequential)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Algorithmic Chord Arpeggiation (Random & Sequential)

* **Core Musical Mechanism**: The procedural breakdown of static block chords (where multiple notes play simultaneously) into sequential, rhythmic melodic lines. The tutorial demonstrates taking a I-vi-IV-V block chord progression and running custom scripts to distribute those chord tones across a 1/8th or 1/16th note grid, creating "Up", "Down", and "Random" arpeggio patterns.
* **Why Use This Skill (Rationale)**: Arpeggiation adds rhythmic drive and harmonic movement without cluttering the frequency spectrum. By separating chord tones in time, the listener still perceives the full underlying harmony (thanks to auditory memory and psychoacoustic grouping), but the arrangement gains kinetic energy. "Random" arpeggios in particular add a generative, unpredictable texture reminiscent of modular synthesizers or IDM (Intelligent Dance Music).
* **Overall Applicability**: Essential for synthwave basslines, trance/EDM lead plucks, cinematic ostinatos, and ambient generative textures. It is a fundamental technique to transform a basic harmonic sketch into a full arrangement.
* **Value Addition**: Instead of relying on external third-party scripts (like the "kawa" scripts in the video), this skill mathematically encodes music theory to natively generate diatonic 7th chords from a key/scale and dynamically algorithmically sequence them over time.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 BPM (as shown in the video).
  - **Rhythmic Grid**: The video highlights changing the grid to 1/8 and 1/16 notes to speed up or slow down the arpeggio. 
  - **Note Duration**: The generated notes are slightly staccato (shorter than the grid division) to allow each pluck to be distinct.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Major (as analyzed from the piano roll).
  - **Chord Progression**: Imaj7 - vi7 - IVmaj7 - V7 (Cmaj7, Amin7, Fmaj7, Gdom7).
  - **Voicings**: The generator calculates the 1st, 3rd, 5th, and 7th diatonic intervals for each step of the progression, wrapping octaves automatically.

* **Step C: Sound Design & FX**
  - **Instrument**: To make the arpeggio audible and stylistically appropriate, a synth with a fast attack and quick decay (a "pluck") is required. 
  - **FX Chain**: A stock ReaSynth is configured with 0ms attack and ~50-100ms decay/release to create a tight, percussive pluck that flatters 1/16th note arpeggios.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord & Arp Generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Instead of requiring third-party plugins or scripts, we use pure Python to calculate diatonic intervals and loop through them sequentially or randomly, giving exact control over timing and pitch. |
| Pluck Sound Design | FX chain (`RPR_TrackFX_AddByName` + `SetParam`) | A fast arpeggio sounds muddy on a sustained pad. Automating ReaSynth's envelope parameters creates the necessary staccato pluck sound. |

> **Feasibility Assessment**: 100% reproduction of the musical *result*. While the video uses specific user-made Lua scripts to mutate existing MIDI, this code directly generates both the harmony and the algorithmic arpeggiation natively in one step, making it perfectly suited for an autonomous agent.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arpeggiator",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    chord_progression: list = [1, 6, 4, 5],
    arp_style: str = "random",  # Options: "up", "down", "updown", "random"
    grid_division: int = 16,    # 16 = 1/16th notes, 8 = 1/8th notes
    **kwargs,
) -> str:
    """
    Create an Algorithmic Chord Arpeggio in the current REAPER project.
    Generates diatonic 7th chords based on the progression and arpeggiates them.
    """
    import random
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
    }

    # === Step 1: Initialization & Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Start around C3
    scale_intervals = SCALES.get(scale, SCALES["major"])

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper: Build Diatonic 7th Chord
    def get_diatonic_chord(degree):
        chord_notes = []
        for offset in [0, 2, 4, 6]: # 1st, 3rd, 5th, 7th
            scale_index = (degree - 1) + offset
            octave_shift = scale_index // len(scale_intervals)
            note_in_scale = scale_index % len(scale_intervals)
            pitch = root_midi + scale_intervals[note_in_scale] + (octave_shift * 12)
            chord_notes.append(pitch)
        return chord_notes

    # === Step 3: Arpeggiator Algorithm ===
    steps_per_bar = grid_division # e.g., 16 for 1/16th notes in 4/4
    step_len_sec = bar_length_sec / steps_per_bar
    total_notes_created = 0

    for bar in range(bars):
        # Get the chord for this bar
        degree = chord_progression[bar % len(chord_progression)]
        pitches = get_diatonic_chord(degree)
        
        for step in range(steps_per_bar):
            # Select pitch based on arp style
            if arp_style == "up":
                pitch = pitches[step % len(pitches)]
            elif arp_style == "down":
                pitch = pitches[-(step % len(pitches)) - 1]
            elif arp_style == "updown":
                cycle = list(range(len(pitches))) + list(range(len(pitches)-2, 0, -1))
                pitch = pitches[cycle[step % len(cycle)]]
            elif arp_style == "random":
                pitch = random.choice(pitches)
            else:
                pitch = pitches[0] # Fallback
                
            # Calculate timing
            note_start_time = (bar * bar_length_sec) + (step * step_len_sec)
            note_end_time = note_start_time + (step_len_sec * 0.8) # 80% gate for staccato feel
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_end_time)
            
            # Humanize velocity slightly
            vel = velocity_base + random.randint(-12, 12)
            vel = max(1, min(127, vel))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
            total_notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Sound Design (Plucky Synth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape the envelope for a fast arp pluck
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Attack (Fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.08)  # Decay (Short)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.0)   # Sustain (None)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.08)  # Release (Short)
    # Mix Saw and Square waves for rich harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.5)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.5)   # Saw mix

    return f"Created '{track_name}' with {total_notes_created} notes over {bars} bars at {bpm} BPM using '{arp_style}' style on a 1/{grid_division} grid."
```

#### 3c. Verification Checklist
- [x] Does the code compute MIDI pitches from key/scale? (Yes, using a custom diatonic math generator).
- [x] Is it purely ADDITIVE? (Yes, inserts new track/item/FX).
- [x] Does it set the track name? (Yes, "Arpeggiator" by default).
- [x] Are all velocity values in the 0-127 MIDI range? (Yes, clamped via `min()` and `max()`).
- [x] Are note timings quantized to the musical grid? (Yes, calculated precisely based on `step_len_sec`).
- [x] Does the function return a descriptive status string? (Yes).
- [x] Would someone listening say "yes, that is the pattern from the tutorial"? (Yes, it recreates the random/sequential arp generation).
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? (Yes).
- [x] Does it avoid hardcoded file paths or external dependencies? (Yes, relies only on native ReaSynth and internal math).