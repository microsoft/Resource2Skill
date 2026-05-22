# 90s Pop Ballad Voice-Led Progression (I-V-vi-IV)

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: 90s Pop Ballad Voice-Led Progression (I-V-vi-IV)

* **Core Musical Mechanism**: The quintessential 90s pop ballad sound is driven by a I–V–vi–IV harmonic progression layered with strict **voice leading** (minimizing pitch movement between chord changes) and **dynamic bass separation**. Rather than jumping between clunky root-position block chords, the inner voices stay close together, sharing common tones and moving by step.
* **Why Use This Skill (Rationale)**: Smooth voice leading creates an emotive, soaring pad or piano texture that glues a mix together. By keeping the upper chord tones tightly grouped (within a single octave) while the bass notes move dynamically, you create a wide frequency spread that leaves perfect space in the middle for a lead vocal. 
* **Overall Applicability**: Essential for pop ballads, emotional RnB, cinematic emotional scoring, and lo-fi chillhop. Whenever a song needs a highly emotional, resolving, and continuous harmonic bed, this pattern works beautifully.
* **Value Addition**: This script encodes the exact "Minimize Movement" and "Auto Voice Leading" features demonstrated via the Scaler 3 VST. It programmatically computes the specific triadic inversions required to lock the inner voices of a I-V-vi-IV progression into a smooth, minimally shifting block.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: 4/4 time, typically slow (70-90 BPM).
  - **Rhythm Grid**: Sustained legato chords (lasting essentially the full bar). 
  - **Humanization**: A slight "strum" or stagger delay (~20ms) is added to the chord tones so they don't hit with rigid, robotic simultaneity.

* **Step B: Pitch & Harmony**
  - **Progression**: I – V – vi – IV in any Major key.
  - **Voice Leading Matrix** (Relative to the Tonic Root Note):
    - **I Chord**: Root position bass, 2nd inversion chord (-5, 0, +4 semitones)
    - **V Chord**: Root position bass, Root position chord (-5, -1, +2 semitones). *Notice how the notes drop gracefully by a maximum of 2 semitones from the I chord.*
    - **vi Chord**: Root position bass, 1st inversion chord (-3, 0, +4 semitones)
    - **IV Chord**: Root position bass, 2nd inversion chord (-3, 0, +5 semitones)

* **Step C: Sound Design & FX**
  - **Instrument**: Subtractive synthesizer (ReaSynth) tuned to mimic a soft pad/electric piano.
  - **FX Parameters**: A slightly softened attack prevents harsh transients, and a longer release creates a washed-out, legato sustain.
  - **Reverb**: ReaVerbate is added with a large room size to emulate the sweeping, airy 90s ballad aesthetic.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Auto Voice Leading | Algorithmic MIDI insertion | Calculates the exact inversions and semitone offsets needed to mimic Scaler 3's "Minimize Movement" feature directly in REAPER. |
| Ballad Humanization | Time-offset MIDI generation | Applies a micro-delay (strum) to higher notes and tapers velocity to soften the chord impact. |
| Ballad Tone | Track FX Chain (ReaSynth + ReaVerbate) | Synthesizes a soft, sustained electric piano/pad texture with spatial depth entirely using native plugins. |

> **Feasibility Assessment**: 100% reproducible. While the tutorial uses a specific paid VST (Scaler 3) to generate the chords, the *music theory outcome* of that VST is entirely replicated using pure math and MIDI data generation via ReaScript.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pop Ballad Pad",
    bpm: int = 80,
    key: str = "A",
    scale: str = "major", # Pop ballad progression heavily relies on major keys
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Creates a highly voice-led 90s Pop Ballad I-V-vi-IV chord progression.
    Mimics "Minimize Movement" and "Auto Voice Leading" features programmatically.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (70-90 recommended for ballads).
        key: Root note (C, C#, D, ..., B).
        scale: Ignored technically, standardizes to Major scale relationships.
        bars: Number of bars to generate (loops the 4-bar sequence).
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Setup core note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    if key not in NOTE_MAP:
        key = "A" # Default back to the video tutorial's key
        
    root_midi = NOTE_MAP[key] + 60 # Set root to C4 octave range

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Voice Leading Matrix (Offsets from Tonic Root)
    # This precisely emulates the tight inner-voicing from the tutorial
    voicings = [
        {"bass": -24, "chord": [-5, 0, 4]},   # I  (e.g., A2 Bass | E4, A4, C#5)
        {"bass": -17, "chord": [-5, -1, 2]},  # V  (e.g., E3 Bass | E4, G#4, B4)
        {"bass": -15, "chord": [-3, 0, 4]},   # vi (e.g., F#3 Bass| F#4, A4, C#5)
        {"bass": -19, "chord": [-3, 0, 5]},   # IV (e.g., D3 Bass | F#4, A4, D5)
    ]

    total_notes_added = 0
    strum_delay_sec = 0.015 # 15ms humanization strum

    # === Step 4: Generate MIDI Notes ===
    for bar in range(bars):
        chord_data = voicings[bar % 4]
        bar_start_time = bar * bar_length_sec
        # Sustain for 95% of the bar to leave a tiny breathing gap
        bar_end_time = bar_start_time + (bar_length_sec * 0.95)

        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_end_time)

        # 1. Insert Bass Note (dynamic voice grouping)
        bass_pitch = root_midi + chord_data["bass"]
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base, False)
        total_notes_added += 1

        # 2. Insert tightly grouped chord tones
        for i, note_offset in enumerate(chord_data["chord"]):
            note_pitch = root_midi + note_offset
            
            # Apply strum humanization
            note_start_time = bar_start_time + (i * strum_delay_sec)
            note_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_start_time)
            
            # Higher notes are played slightly softer
            note_vel = max(10, velocity_base - 10 - (i * 5))
            
            RPR.RPR_MIDI_InsertNote(take, False, False, note_start_ppq, end_ppq, 0, note_pitch, note_vel, False)
            total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Sound Design (FX Chain) ===
    # Add a soft synth
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the attack (Param 2) to remove clicking
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.03) 
    
    # Lengthen release (Param 5) for pad tail
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.35) 
    
    # Lower square wave mix (Param 8) and saw mix (Param 9) to favor sine/triangle for softer tone
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.0)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.2)

    # Add Reverb for the 90s ballad atmosphere
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.6) # Wet mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.8) # Dry mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.8) # Room Size (Large)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 4, 0.1) # High pass

    return f"Created '{track_name}' with {total_notes_added} voice-led notes over {bars} bars at {bpm} BPM in {key} Major."
```