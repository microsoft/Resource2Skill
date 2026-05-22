### 1. High-level Design Pattern Extraction

> **Skill Name**: Velocity-Humanized MIDI Chords

* **Core Musical Mechanism**: The defining technique of this pattern is breaking the "robotic" feel of rigid, snapped-to-grid MIDI sequences by intentionally manipulating note lengths and explicitly varying the MIDI velocities (the "how hard the key is struck" parameter in the CC lane). Instead of drawing block chords where every note plays at a maximum velocity of 127, this pattern applies dynamic variation across the rhythm, emphasizing downbeats and softening syncopated offbeats or inner chord voices.
* **Why Use This Skill (Rationale)**: In music theory and live performance, players naturally accent certain beats (usually beats 1 and 3 in a 4/4 time signature) and play passing chords or offbeats softer. Furthermore, within a single chord, the root and melody notes are often struck slightly harder than the inner harmony notes. This variation creates a psychoacoustic sense of "groove" and realism, mimicking the physical constraints and emotional expression of a real pianist. 
* **Overall Applicability**: This technique is universally necessary for any genre that relies on virtual acoustic instruments (pianos, strings, Rhodes, acoustic drums). It is particularly vital for lo-fi hip hop, neo-soul, R&B, and cinematic orchestral arrangements where static, fully-velocity-maxed MIDI tracks instantly sound amateurish and fatiguing to the ear.
* **Value Addition**: Compared to a blank MIDI clip or a simple block chord loop, this skill encodes dynamic groove. It automates the tedious process of clicking and dragging individual velocity stalks by generating a progression with a pre-programmed "humanized" velocity curve (strong downbeats, softer offbeats, and varied inner-voice intensities).

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically around 90-120 BPM.
  - **Rhythm**: A syncopated comping rhythm (e.g., dotted-quarter, eighth, half note) that leaves space for velocity dynamics. 
  - **Note Duration**: Slightly detached (legato with a tiny gap) to mimic the sustain pedal releasing and repressing, preventing MIDI overlapping artifacts.

* **Step B: Pitch & Harmony**
  - **Key & Scale**: Configurable (e.g., C Major).
  - **Progression**: A fundamental I - V - vi - IV progression (or similar depending on the scale).
  - **Voicings**: Basic triads (root, third, fifth), with the root note usually given a slightly higher velocity base than the third and fifth to anchor the harmony.

* **Step C: Sound Design & FX**
  - **Instrument**: In the tutorial, a Grand Piano VST is used. For native reproducibility, we will instantiate `ReaSynth` as a placeholder to generate a tone, tuned to have a softer attack and decay to simulate a key strike.
  - **FX**: Native instrument plugin generation. 

* **Step D: Mix & Automation**
  - **Automation (CC Lane)**: The tutorial focuses entirely on the CC velocity lane at the bottom of the MIDI editor. This script mathematically mimics the "dragging down" of the CC lane stalks for offbeats.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track & Item Creation | `RPR_CreateNewMIDIItemInProj` | Safely initializes a valid MIDI take ready for note data compared to empty audio items. |
| Pitch Generation | Scale array indexing | Ensures chords are perfectly in-key regardless of the user's chosen root or scale. |
| Humanized Velocity | `RPR_MIDI_InsertNote` parameters | Explicitly controls the dynamic level of each specific note in the CC lane, matching the core lesson of the tutorial. |
| Instrument Setup | `RPR_TrackFX_AddByName` (ReaSynth) | Provides immediate audio feedback without relying on external, potentially missing VSTs (like the Grand Piano shown). |

> **Feasibility Assessment**: 100% reproducible. While the user's specific third-party "Grand Piano" VST is not standard, the native structural technique (humanized MIDI generation and track routing) is fully implementable via the ReaScript API using stock resources.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Velocity-Humanized MIDI Chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Data ===
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
    
    scale_degrees = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Start at C3 (MIDI 48)

    # Function to get pitch safe-wrapping the scale
    def get_pitch_in_scale(degree_index):
        octave_shift = degree_index // len(scale_degrees)
        scale_note = scale_degrees[degree_index % len(scale_degrees)]
        return root_midi + (octave_shift * 12) + scale_note

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth as Piano Placeholder) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more "piano-like" plucky envelope
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0) # Saw shape down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0) # Pulse shape down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0) # Attack time short
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Decay time
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.2) # Sustain level low
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.4) # Release time

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Generate Humanized Chord Progression ===
    # Progression degrees (0-indexed): I, V, vi, IV
    progression = [0, 4, 5, 3] 
    
    notes_added = 0
    for bar in range(bars):
        # Repeat progression if bars > 4
        chord_root_idx = progression[bar % len(progression)]
        
        # Chord notes (Root, 3rd, 5th)
        chord_degrees = [chord_root_idx, chord_root_idx + 2, chord_root_idx + 4]
        
        # Rhythm Pattern within the bar (Beat times: [start_beat, length_beats])
        # A syncopated comping rhythm demonstrating velocity changes
        rhythm_hits = [
            (0.0, 1.4), # Downbeat: Strong
            (1.5, 0.4), # Syncopated offbeat: Weak
            (2.0, 1.9)  # Beat 3: Medium
        ]
        
        # Velocity profile corresponding to the rhythm hits
        vel_profile = [
            velocity_base,           # Accent downbeat
            int(velocity_base * 0.7), # Soften offbeat
            int(velocity_base * 0.85) # Medium sustain
        ]

        for hit_idx, (start_b, len_b) in enumerate(rhythm_hits):
            start_time = (bar * bar_length_sec) + (start_b * beat_length_sec)
            end_time = start_time + (len_b * beat_length_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            base_hit_vel = vel_profile[hit_idx]
            
            for voice_idx, degree in enumerate(chord_degrees):
                pitch = get_pitch_in_scale(degree)
                
                # Humanize: Inner voices (3rd, 5th) are played slightly softer than the root
                voice_vel_adjustment = 0 if voice_idx == 0 else -10
                final_vel = max(1, min(127, base_hit_vel + voice_vel_adjustment))
                
                RPR.RPR_MIDI_InsertNote(
                    take, False, False, 
                    start_ppq, end_ppq, 
                    0, pitch, final_vel, True
                )
                notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_added} dynamically varied notes over {bars} bars at {bpm} BPM in {key} {scale}"
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?