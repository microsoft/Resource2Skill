# Pharrell/Neptunes: Pharrell-Style Inverted Groove (Melodic Percussion & Sparse Arrangement)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pharrell-Style Inverted Groove (Melodic Percussion & Sparse Arrangement)

* **Core Musical Mechanism**: This pattern flips conventional arrangement on its head through three distinct techniques:
  1. **Sparse Ear Candy**: Instead of looping a unique "cool" sound constantly (like traditional boom-bap), highly recognizable/strange sounds are used extremely sparsely (e.g., once every 2 or 4 bars) to make them feel "special" and contextualized.
  2. **Percussion as Melody**: Rhythmic, non-tonal sounds (like claves, toms, or woodblocks) are repitched to act as the primary melodic or bass element.
  3. **Melody as Percussion**: Conventionally melodic/harmonic instruments (like guitars or synths) are used rhythmically. They play highly syncopated, staccato (very short), 2-3 note patterns with little to no reverb (extremely "dry"), acting more like a hi-hat than a lead instrument.

* **Why Use This Skill (Rationale)**: This creates an incredibly bouncy, infectious groove that leaves immense sonic space for a vocalist. By making the percussion melodic and the melody percussive, it disrupts listener expectations. The extreme dryness (lack of reverb) makes the track feel intimate and aggressive ("in your face"), while the sparse "ear candy" exploits psychoacoustics by rewarding the listener periodically rather than fatiguing them with a constant loop.

* **Overall Applicability**: Hip-hop, Pop, Funk, R&B, and modern beat-making. Ideal for verses where you need to maintain high energy but leave a massive pocket for a lead vocal or rapper. 

* **Value Addition**: This skill encodes an advanced arrangement philosophy, showing how to create movement and interest without adding *more* elements, but rather by altering the function and frequency of *existing* elements.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Typically 90-105 BPM (classic early 2000s Neptunes bounce).
  - **Grid**: 16th note syncopation. 
  - **Note Duration**: Extremely staccato. Notes rarely sustain. Guitars and percussion hit and immediately mute.
  - **Placement**: Guitars hit on off-beat 16ths (e.g., the "e" and "a" of the beat). The "ear candy" sound hits exactly once at the end of a phrase (e.g., Bar 2, Beat 4.75).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Often relies heavily on Minor Pentatonic or Dorian, utilizing the root, minor 3rd, 4th, 5th, and minor 7th to create "bluesy" but robotic riffs.
  - **Voicings**: Single notes or simple open 5th dyads. Full chords are rarely used in the rhythmic guitar parts to avoid cluttering the frequency spectrum.

* **Step C: Sound Design & FX**
  - **Melodic Percussion (Bass)**: A synthesized or sampled percussive hit (like a tom or clave) with a fast attack, no sustain, and fast release. 
  - **Rhythmic Guitar**: A dry, plucky sawtooth/pulse wave with a low-pass filter to mimic a palm-muted guitar. ZERO reverb or delay.
  - **Sparse Ear Candy**: A high-pitched, strange texture (e.g., a pure square wave or FM bell) that provides stark contrast to the dry, woody sounds of the rest of the beat.

* **Step D: Mix & Automation**
  - Completely dry mix. Elements are panned strictly (e.g., guitar hard left, ear candy hard right) to create a wide stereo field without using spatial effects like reverb that would wash out the groove.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Melodic Percussion (Bass) | MIDI + ReaSynth (Sine/Triangle, fast decay) | Safely mimics a "repitched tom" without relying on external, unavailable `.wav` samples. |
| Dry Rhythmic Guitar | MIDI + ReaSynth (Sawtooth, staccato notes) | Recreates the dry, plucky, percussive use of a melodic instrument. MIDI note lengths are kept extremely short (0.1 QN). |
| Sparse Ear Candy | MIDI + ReaSynth (Square, high octave) | Injected only once at the end of the 2-bar loop, fulfilling the "sparse placement" rule. |

> **Feasibility Assessment**: 85%. The script perfectly captures the arrangement theory, MIDI timing, syncopation, and dryness of Pharrell's style. However, to reach 100% authenticity, the user would need to replace the generated ReaSynth placeholders with high-quality sampled claves, toms, and physical-modeled guitars.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Pharrell_Groove",
    track_name: str = "Neptunes_Style",
    bpm: int = 96,
    key: str = "F",
    scale: str = "pentatonic_minor",
    bars: int = 2,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Creates a Pharrell/Neptunes-style inverted groove featuring repitched melodic percussion, 
    staccato rhythmic guitars, and sparse ear-candy placement.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate (forces multiples of 2 for the loop).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    if scale not in SCALES:
        scale = "pentatonic_minor"
    
    root_val = NOTE_MAP.get(key.capitalize(), 5) # Default F
    scale_intervals = SCALES[scale]

    # Ensure bars is a multiple of 2 to allow the "sparse" event to happen at the end of the phrase
    bars = max(2, bars + (bars % 2))

    # Helper function to get midi pitch from scale degree
    def get_pitch(octave, degree):
        degree = degree % len(scale_intervals)
        octave_offset = (degree // len(scale_intervals)) * 12
        return (octave * 12) + root_val + scale_intervals[degree] + octave_offset

    # Helper function to add notes
    def add_midi_note(take, start_qn, duration_qn, pitch, vel):
        start_time = start_qn * (60.0 / bpm)
        end_time = (start_qn + duration_qn) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    track_count = RPR.RPR_CountTracks(0)

    # === Track 1: Melodic Percussion (Bass) ===
    # Represents repitched toms/claves acting as the bass groove
    RPR.RPR_InsertTrackAtIndex(track_count, True)
    trk_perc = RPR.RPR_GetTrack(0, track_count)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_perc, "P_NAME", f"{track_name}_MelodicPerc", True)
    
    # Add ReaSynth (Sine wave to act as a subby tom)
    fx_perc = RPR.RPR_TrackFX_AddByName(trk_perc, "ReaSynth", False, -1)
    # Set to fast decay to make it percussive
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 1, 0.0)  # Square mix 0
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 2, 0.0)  # Saw mix 0
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 4, 0.01) # Attack
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 5, 0.1)  # Decay
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 6, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(trk_perc, fx_perc, 7, 0.1)  # Release

    item_perc = RPR.RPR_AddMediaItemToTrack(trk_perc)
    RPR.RPR_SetMediaItemInfo_Value(item_perc, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_perc, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_perc = RPR.RPR_AddTakeToMediaItem(item_perc)

    # === Track 2: Dry Rhythmic "Guitar" ===
    # Very short, staccato off-beat syncopations
    RPR.RPR_InsertTrackAtIndex(track_count + 1, True)
    trk_gtr = RPR.RPR_GetTrack(0, track_count + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_gtr, "P_NAME", f"{track_name}_RhythmicGtr", True)
    RPR.RPR_SetMediaTrackInfo_Value(trk_gtr, "D_PAN", -0.5) # Pan Left for width
    
    fx_gtr = RPR.RPR_TrackFX_AddByName(trk_gtr, "ReaSynth", False, -1)
    # Saw wave, no sustain, mimicking a muted guitar pluck
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 1, 0.0)  # Square mix 0
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 2, 0.8)  # Saw mix up
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 4, 0.0)  # Attack
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 5, 0.05) # Very short decay
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 6, 0.0)  # Sustain
    RPR.RPR_TrackFX_SetParam(trk_gtr, fx_gtr, 7, 0.05) # Release

    item_gtr = RPR.RPR_AddMediaItemToTrack(trk_gtr)
    RPR.RPR_SetMediaItemInfo_Value(item_gtr, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_gtr, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_gtr = RPR.RPR_AddTakeToMediaItem(item_gtr)

    # === Track 3: Sparse Ear Candy ===
    # A distinct sound that hits only once per loop
    RPR.RPR_InsertTrackAtIndex(track_count + 2, True)
    trk_candy = RPR.RPR_GetTrack(0, track_count + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(trk_candy, "P_NAME", f"{track_name}_EarCandy", True)
    RPR.RPR_SetMediaTrackInfo_Value(trk_candy, "D_PAN", 0.5) # Pan Right
    
    fx_candy = RPR.RPR_TrackFX_AddByName(trk_candy, "ReaSynth", False, -1)
    # Square wave for a distinct, synthetic contrast to the other sounds
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 1, 0.8)  # Square mix
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 2, 0.0)  # Saw mix
    RPR.RPR_TrackFX_SetParam(trk_candy, fx_candy, 3, 0.2)  # Extra tuning for a bell-like feel

    item_candy = RPR.RPR_AddMediaItemToTrack(trk_candy)
    RPR.RPR_SetMediaItemInfo_Value(item_candy, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item_candy, "D_LENGTH", bars * 4 * (60.0 / bpm))
    take_candy = RPR.RPR_AddTakeToMediaItem(item_candy)

    # === MIDI Generation Loop ===
    note_count = 0
    for b in range(0, bars, 2): # Iterate in 2-bar chunks
        bar_qn = b * 4
        
        # -- Melodic Percussion Groove (Bass, Octave 2 & 3) --
        # Syncopated 16th note pattern
        add_midi_note(take_perc, bar_qn + 0.00, 0.2, get_pitch(2, 0), velocity_base)      # Beat 1 (Root)
        add_midi_note(take_perc, bar_qn + 0.75, 0.2, get_pitch(2, 1), velocity_base - 10) # Beat 1.75 (m3)
        add_midi_note(take_perc, bar_qn + 1.50, 0.2, get_pitch(2, 2), velocity_base - 15) # Beat 2.5 (4th)
        add_midi_note(take_perc, bar_qn + 3.00, 0.2, get_pitch(2, 3), velocity_base)      # Beat 4 (5th)
        
        add_midi_note(take_perc, bar_qn + 4.00, 0.2, get_pitch(2, 0), velocity_base)      # Bar 2, Beat 1
        add_midi_note(take_perc, bar_qn + 5.25, 0.2, get_pitch(2, 4), velocity_base - 10) # Bar 2, Beat 2.25 (m7)
        add_midi_note(take_perc, bar_qn + 6.50, 0.2, get_pitch(3, 0), velocity_base)      # Bar 2, Beat 3.5 (Root + octave)
        note_count += 7

        # -- Rhythmic Guitar Groove (Octave 4) --
        # Extremely dry, staccato, 2-note bursts acting like percussion
        add_midi_note(take_gtr, bar_qn + 1.25, 0.1, get_pitch(4, 0), velocity_base - 5)   # Beat 2.25 (e)
        add_midi_note(take_gtr, bar_qn + 1.50, 0.1, get_pitch(4, 0), velocity_base - 5)   # Beat 2.5  (&)
        
        add_midi_note(take_gtr, bar_qn + 5.25, 0.1, get_pitch(4, 0), velocity_base - 5)   # Bar 2, Beat 2.25
        add_midi_note(take_gtr, bar_qn + 5.50, 0.1, get_pitch(4, 0), velocity_base - 5)   # Bar 2, Beat 2.5
        add_midi_note(take_gtr, bar_qn + 7.50, 0.1, get_pitch(4, 0), velocity_base - 10)  # Bar 2, Beat 4.5
        note_count += 5

        # -- Sparse Ear Candy (Octave 6) --
        # Only happens ONCE at the very end of the 2-bar phrase
        add_midi_note(take_candy, bar_qn + 7.75, 0.25, get_pitch(6, 4), velocity_base + 10) # Bar 2, Beat 4.75
        note_count += 1

    RPR.RPR_MIDI_Sort(take_perc)
    RPR.RPR_MIDI_Sort(take_gtr)
    RPR.RPR_MIDI_Sort(take_candy)
    RPR.RPR_UpdateArrange()

    return f"Created Pharrell-style arrangement: 3 tracks ('{track_name}'), {note_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale?
- [x] Is it purely ADDITIVE?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?