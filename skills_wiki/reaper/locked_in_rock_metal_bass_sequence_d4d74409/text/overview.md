### 1. High-level Design Pattern Extraction

> **Skill Name**: Locked-In Rock/Metal Bass Sequence

* **Core Musical Mechanism**: The defining characteristic of this pattern is strict rhythmic synchronization between the bassline and the kick drum (often featuring fast 16th-note syncopations). Variation is achieved not by changing the fundamental rhythm or harmony, but by introducing targeted octave leaps (+12 semitones) to simulate a bass player jumping to the 12th fret. Additionally, MIDI velocities are intentionally reduced from maximum to tame the harsh top-end "twang" inherent in multi-sampled virtual bass instruments.
* **Why Use This Skill (Rationale)**: In modern metal, rock, and pop-punk, the bass and kick drum are treated as a single, massive low-end entity. Locking their rhythms together prevents low-frequency phase cancellation and creates a driving, punchy groove. The octave leaps add melodic contour and energy without muddying the sub-frequencies. Lowering the MIDI velocity is a psychoacoustic and sound-design trick: many virtual basses trigger aggressive, bright string-slap layers at velocities above 115; dialing it back to ~110 yields a thicker, more consistent, and mix-friendly tone.
* **Overall Applicability**: Essential for heavy rock, metalcore, djent, pop-punk, or any genre utilizing heavily distorted guitars where the bass needs to provide a rock-solid, tightly edited rhythmic foundation.
* **Value Addition**: Compared to a blank MIDI clip or a basic continuous bass note, this skill encodes the actual workflow of modern heavy music production: matching kick syncopation, utilizing realistic fret jumps, and managing VSTi velocity layers for optimal tone.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically ranging from 110 to 160 BPM.
  - **Grid**: Strict 16th-note grid. No swing.
  - **Durations**: A mix of staccato 16th notes (for fast double-kick patterns) and held 8th/quarter notes (for sustained hits).
* **Step B: Pitch & Harmony**
  - **Key/Pitch**: Often played on low open strings (e.g., Drop C, Drop A). The primary pitch maps to the root note of the key in a low octave (e.g., C1 = MIDI note 24).
  - **Voicing**: Monophonic.
  - **Variations**: Occasional +12 semitone leaps mapping to the 12th fret of the bass guitar.
* **Step C: Sound Design & FX**
  - **Instrument**: Virtual multi-sampled bass VSTi (e.g., DjinnBass, Loki Bass, MotoBass). *For REAPER reproduction, ReaSynth can serve as a placeholder.*
  - **Velocity**: Capped around 110 (out of 127) to avoid triggering overly aggressive string attack samples.
* **Step D: Mix & Automation**
  - Not heavily addressed in the source, but the pattern is designed to sit perfectly beneath heavy guitars by strictly holding the root note.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bass groove & Octave leaps | MIDI note insertion | Provides precise control over 16th-note syncopation timing, specific 110 velocity values, and exact +12 semitone pitch offsets. |
| Virtual Bass Placeholder | FX Chain (ReaSynth) | Ensures the generated MIDI is audible out-of-the-box without depending on third-party VSTs like DjinnBass. |

> **Feasibility Assessment**: 100% reproduction of the MIDI programming technique shown in the tutorial. The actual audio tone will differ because a basic ReaSynth patch is used instead of a premium sampled bass VST, but the core musical pattern, rhythm, and velocity logic are perfectly preserved.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass (Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Locked-In Rock/Metal Bass Sequence' in the current REAPER project.
    
    This script generates a syncopated, kick-following bassline utilizing
    controlled velocities and octave leaps, as common in heavy rock/metal production.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B). Defaults to C (Drop C style).
        scale: Scale type (not strictly used here as it rides the root, but accepted for compatibility).
        bars: Number of bars to generate (should be a multiple of 2 for the loop).
        velocity_base: Base MIDI velocity (0-127). Set to 110 to reduce VST string noise.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

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

    # Determine base pitch. Assuming a low tuned bass (e.g., C1 for modern metal)
    # MIDI note 24 is C1.
    root_offset = NOTE_MAP.get(key.upper(), 0)
    base_pitch = 24 + root_offset

    # Define a 2-bar 16th-note syncopated rhythm pattern typical of metal kick drums
    # Format: (start_16th_index, length_in_16ths, pitch_offset_semitones)
    pattern = [
        # Bar 1: Driving rhythm riding the open root note
        (0, 2, 0),   # Beat 1
        (2, 2, 0),   # Beat 1.5
        (4, 1, 0),   # Beat 2 (two fast 16ths)
        (5, 1, 0),
        (8, 2, 0),   # Beat 3
        (10, 2, 0),  # Beat 3.5
        (14, 2, 0),  # Beat 4.5 syncopation
        
        # Bar 2: Same rhythm but introducing the 12th-fret octave jump
        (16, 2, 0),  
        (18, 2, 0),  
        (20, 1, 0),  
        (21, 1, 0),
        (24, 2, 0),  
        (26, 2, 12), # Beat 3.5 - OCTAVE JUMP (+12 semitones)
        (30, 2, 0)   
    ]
    
    pattern_length_16ths = 32 # 2 bars * 16 sixteenth notes
    
    note_count = 0
    # Loop the 2-bar pattern to fill the requested number of bars
    loop_iterations = max(1, bars // 2)
    if bars % 2 != 0:
        loop_iterations += 1 # Ensure we cover odd numbers of bars
        
    for bar_pair in range(loop_iterations):
        bar_offset_16ths = bar_pair * pattern_length_16ths
        
        for start_idx, length, pitch_offset in pattern:
            start_16th = bar_offset_16ths + start_idx
            
            # Stop adding notes if we exceed the requested total bars
            if start_16th >= (bars * 16):
                continue
                
            end_16th = start_16th + length
            
            # Convert 16th note indices to Quarter Notes, then to Seconds
            start_qn = start_16th / 4.0
            end_qn = end_16th / 4.0
            
            start_pos = start_qn * (60.0 / bpm)
            end_pos = end_qn * (60.0 / bpm)
            
            # Convert Seconds to REAPER PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            pitch = base_pitch + pitch_offset
            
            # Insert note (using the specified 110 velocity base to tame transient harshness)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain Placeholder ===
    # Add ReaSynth as a stock placeholder to ensure the track produces low-end sound
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    if synth_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.0)   # Volume
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.4)   # Square mix
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.6)   # Saw mix (bite)
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.01)  # Fast attack
        RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.3)   # Snappy decay

    return f"Created '{track_name}' with {note_count} locked-in bass notes (including octave leaps) over {bars} bars at {bpm} BPM."
```