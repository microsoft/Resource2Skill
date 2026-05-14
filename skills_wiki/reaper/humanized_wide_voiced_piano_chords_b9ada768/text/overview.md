### 1. High-level Design Pattern Extraction

**Skill Name**: Humanized Wide-Voiced Piano Chords

* **Core Musical Mechanism**: The pattern centers on two essential MIDI programming techniques for realistic, full-sounding polyphonic instruments:
  1. **Wide Voicing**: Taking a standard closed triad (Root, 3rd, 5th) and dropping the root note down one or two octaves. 
  2. **Velocity Humanization & Ramping**: Applying a linear slope (crescendo) to MIDI velocities across a progression, while injecting subtle, randomized deviations in both timing and velocity to mimic human performance.

* **Why Use This Skill (Rationale)**: 
  - *Harmonic Spacing*: By default, drawing simple triads in a single octave sounds thin and muddy because the frequencies are clustered too closely together. Moving the root note down one or two octaves (as demonstrated in the tutorial) creates separation between the bass fundamental and the upper harmony, resulting in a much larger, more cinematic sound. 
  - *Psychoacoustics of Velocity*: A static velocity of 127 triggers the exact same synth/sampler layer on every hit, resulting in the dreaded "machine-gun effect." By ramping the velocities, you create dynamic movement (tension and release). Slight randomizations mimic the natural inconsistencies of human fingers striking physical keys.

* **Overall Applicability**: Essential for programming piano VSTs, lush synth pads, orchestral string sections, or any sustained polyphonic instrument in pop, lo-fi, EDM, and cinematic scoring.

* **Value Addition**: This skill moves beyond static, robotic block chords by automatically computing a diatonic progression, expanding the voicing into a massive 5-note stack (Root-24, Root-12, Root, 3rd, 5th), and applying humanized timing and velocity crescendos.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically 100-120 BPM.
  - **Grid**: Quarter notes (1/4), but played slightly staccato/detached (85% gate length).
  - **Humanization**: Each note is shifted off the perfect grid by a random value between -15ms and +15ms to create a looser, more organic feel.

* **Step B: Pitch & Harmony**
  - **Progression**: A standard 4-bar progression (I - V - vi - IV).
  - **Voicing Structure**: For every chord, the skill generates the Root, Major/Minor 3rd, and Perfect 5th. It then explicitly duplicates the root note down one octave (-12 semitones) and two octaves (-24 semitones) to anchor the low end.

* **Step C: Sound Design & FX**
  - **Instrument**: Uses REAPER's native `ReaSynth` as a lightweight placeholder for a Grand Piano VST. 
  - **Volume**: Track volume is lowered to avoid harsh clipping when playing 5-note chords.

* **Step D: Mix & Automation**
  - **Velocity Automation**: Simulates the MIDI Editor CC lane linear ramp. Velocity starts at 40% of the base value in bar 1 and swells to 100% by bar 4.
  - **Micro-dynamics**: Random velocity jitter (±12) is applied to individual notes within the chord so they don't strike with exact uniformity.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Wide Chord Voicings | MIDI Note Pitch Calculation | Programmatically drops the root note by 12 and 24 semitones to exactly replicate the tutorial's note dragging. |
| Humanized Performance | `random.uniform` & `random.randint` | Offsets `startppqpos`, `endppqpos`, and `vel` per note to break the mechanical grid. |
| Velocity Ramp (CC Lane) | Mathematical Progression | Calculates a linear ramp across the 4 bars to simulate drawing a velocity slope in the MIDI editor CC lane. |
| Instrument | `ReaSynth` FX | Provides a basic polyphonic sound source native to REAPER since external piano VSTs are not guaranteed. |

**Feasibility Assessment**: 100% reproducible. The code perfectly encapsulates the structural concepts of the MIDI editor shown in the tutorial (drawing notes, dropping octaves, adjusting velocities, and generating ramps) using native ReaScript functionality.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Humanized Wide-Voiced Chord Progression in the current REAPER project.
    """
    import reaper_python as RPR
    import random

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
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5) # Lower volume to prevent clipping

    # === Step 3: Add FX Chain (ReaSynth as placeholder) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Harmony Calculations
    base_note = NOTE_MAP.get(key.upper(), 0) + 60 # C4 = 60
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    
    def get_scale_note(degree):
        octave_shift = degree // len(scale_intervals)
        note_idx = degree % len(scale_intervals)
        return base_note + (octave_shift * 12) + scale_intervals[note_idx]

    # I - V - vi - IV progression
    progression = [0, 4, 5, 3]
    total_notes = 0
    
    # === Step 5: Generate Humanized MIDI ===
    for bar in range(bars):
        degree = progression[bar % len(progression)]
        
        # Calculate diatonic triad
        root = get_scale_note(degree)
        third = get_scale_note(degree + 2)
        fifth = get_scale_note(degree + 4)
        
        # Wide Voicing: Drop the root 1 and 2 octaves down
        notes = [root - 24, root - 12, root, third, fifth]
        
        # Generate quarter note chords
        for beat in range(4):
            start_time = (bar * beats_per_bar + beat) * (60.0 / bpm)
            end_time = start_time + (60.0 / bpm) * 0.85 # 85% gate length
            
            # Linear Velocity Ramp (Swell)
            progress = (bar * 4 + beat) / (bars * 4 - 1)
            target_vel = int(velocity_base * 0.4 + (velocity_base * 0.6 * progress))
            
            for pitch in notes:
                # Add micro-humanization to velocity and timing
                human_vel = max(1, min(127, target_vel + random.randint(-12, 12)))
                human_start = max(0.0, start_time + random.uniform(-0.015, 0.015))
                human_end = end_time + random.uniform(-0.015, 0.015)
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, human_start)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, human_end)
                
                # Insert note (noSort = True for performance, sorted at the end)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, human_vel, True)
                total_notes += 1

    # Apply all MIDI note insertions
    RPR.RPR_MIDI_Sort(take)
    
    return f"Created '{track_name}' with {total_notes} humanized wide-voiced notes over {bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist
- [x] Does the code compute MIDI pitches from key/scale?
- [x] Is it purely ADDITIVE?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings computed cleanly utilizing musical constraints?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect parameters (bpm, key, scale, bars)?
- [x] Does it avoid hardcoded external dependencies?