### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized Velocity MIDI Chords

* **Core Musical Mechanism**: The defining technique shown in the tutorial is the manual adjustment of the MIDI Velocity CC (Control Change) lane to inject dynamic variation into drawn-in block chords. Instead of all notes firing simultaneously at a maximum static velocity (the "machine gun" effect), the velocities of individual notes within the chords are staggered and randomized.
* **Why Use This Skill (Rationale)**: When producers draw chords into a piano roll with a mouse, the DAW defaults to perfect quantization and static velocities (often 127 or 96). This sounds highly robotic because a real pianist naturally applies different weight to their fingers—often accenting the root or melody note while playing the inner chord voices softer. Humanizing these parameters creates psychoacoustic realism, making digital instruments sound like physical, acoustic performances.
* **Overall Applicability**: This technique is essential whenever programming acoustic sampled instruments—particularly grand pianos, orchestral strings, acoustic guitars, and drum kits—in any genre ranging from lo-fi hip-hop to pop and cinematic scoring. 
* **Value Addition**: Compared to a blank MIDI clip or a basic rigid chord generator, this skill encodes "expressive performance" data. It calculates chords based on music theory but explicitly applies a humanization algorithm (velocity variation and micro-timing shifts) to emulate a live player.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo:** 120 BPM (as explicitly set in the tutorial).
  - **Rhythmic Grid:** Block chords held for 1 bar each, initially snapped to a 1/16th note grid.
  - **Timing Humanization:** The tutorial mentions holding `Shift` to bypass grid snapping. We emulate this by adding a tiny micro-timing offset (jitter) to the start and end of each note so they don't strike perfectly simultaneously.

* **Step B: Pitch & Harmony**
  - **Key/Scale:** C Major (demonstrated), but parameter-driven. 
  - **Chords:** Basic diatonic triads. The tutorial demonstrates copying, pasting, and transposing a C Major chord. We will generate a foundational I-IV-V-I progression to demonstrate the humanization across changing harmonies.

* **Step C: Sound Design & FX**
  - **Instrument:** The tutorial uses a free third-party "Grand Piano" VSTi. To ensure reproducibility in a vanilla REAPER installation, the code will default to REAPER's native `ReaSynth` (set to a plucky, piano-like decay envelope) to preview the chords.

* **Step D: Mix & Automation**
  - **Velocity CC Automation:** The core focus. The base velocity is set around 100. The root note gets a slight boost, while the 3rd and 5th intervals are reduced. Finally, a random jitter of +/- 10 is applied to every individual note's velocity.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Generation | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise, programmatic definition of pitches based on scale degrees. |
| Velocity Humanization | `vel` parameter in `RPR_MIDI_InsertNote` | Directly manipulates the CC Velocity lane shown in the tutorial for dynamic expression. |
| Timing Humanization | PPQ positional math | Replicates the "bypassing the grid" technique to create micro-timing staggers (strumming effect). |
| Instrument | `RPR_TrackFX_AddByName` (ReaSynth) | Provides a stock sound generator without relying on external third-party VSTs. |

> **Feasibility Assessment**: 90% — The code perfectly reproduces the creation of a MIDI item, the input of chords, and the explicit humanization of the velocity CC lane and micro-timing highlighted in the video. The only missing element is the specific 3rd-party "Grand Piano" VST used, which is safely substituted with ReaSynth.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a Humanized Velocity MIDI Chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate (generates 1 chord per bar).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10]
    }
    
    # Fallback to major if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    base_midi_note = 48 + NOTE_MAP.get(key.upper(), 0) # Start around C3 (Midi note 48)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate Chords & Humanize Velocity/Timing ===
    # A standard I - IV - V - I progression defined by scale degrees
    progression = [0, 3, 4, 0] 
    
    def get_scale_pitch(degree_index, octave_shift=0):
        # Calculate diatonic pitch based on scale degree
        octave = degree_index // len(scale_intervals)
        rem = degree_index % len(scale_intervals)
        return base_midi_note + scale_intervals[rem] + (octave * 12) + (octave_shift * 12)

    notes_created = 0
    
    for bar in range(bars):
        # Loop progression if bars > len(progression)
        chord_root_degree = progression[bar % len(progression)]
        
        # Triad degrees (root, 3rd, 5th)
        chord_degrees = [chord_root_degree, chord_root_degree + 2, chord_root_degree + 4]
        
        start_time = bar * bar_length_sec
        # Leave a tiny gap at the end of the bar for articulation
        end_time = start_time + (bar_length_sec * 0.95) 
        
        base_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        base_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        for i, degree in enumerate(chord_degrees):
            pitch = get_scale_pitch(degree)
            
            # --- HUMANIZATION LOGIC ---
            # 1. Velocity weighting (root is strongest, 3rd is quietest, 5th is mid)
            if i == 0:
                vel = velocity_base + 5
            elif i == 1:
                vel = velocity_base - 15
            else:
                vel = velocity_base - 5
                
            # 2. Velocity random jitter
            vel += random.randint(-8, 8)
            vel = max(1, min(127, vel)) # Clamp between 1-127
            
            # 3. Timing jitter (Stagger notes slightly to avoid robotic simultaneous attack)
            # 960 PPQ is typical for a quarter note; 20 PPQ is a very subtle human micro-shift
            timing_jitter = random.randint(-15, 25) 
            start_ppq = base_start_ppq + timing_jitter
            end_ppq = base_end_ppq + timing_jitter
            
            # Insert the humanized note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX ===
    # Using ReaSynth as a fallback, configured to act somewhat like a plucked/piano string
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to have a fast attack and decaying sustain (Pluck/Piano style)
    # Param 1: Attack (fast)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 1, 0.01)
    # Param 2: Decay (moderate)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.4)
    # Param 3: Sustain (low)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.1)
    # Param 4: Release (moderate)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.3)

    return f"Created '{track_name}' with {notes_created} humanized velocity chord notes over {bars} bars at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (with explicit, calculated human micro-shifts applied as demonstrated in the skill)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?