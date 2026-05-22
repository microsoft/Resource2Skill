# Three-Energy Groove Generator (Down, Up, Side-to-Side)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Three-Energy Groove Generator (Down, Up, Side-to-Side)

* **Core Musical Mechanism**: This pattern decomposes rhythm into three distinct "energies" layered on top of one another:
    1. **Down Energy**: Notes played directly on the pulse (quarter notes). Provides grounding, structure, and weight.
    2. **Up Energy**: Notes played on the exact off-beats (8th note 'ands'). Provides a bouncing, lifting, and airy counter-balance to the downbeats.
    3. **Side-to-Side Energy**: Notes played on the intermediate syncopated 16th notes (e.g., the 'e' or 'a' of the beat). This breaks the rigid symmetry of the straight 8th notes, injecting humanity, tension, chaos, and "grind" into the pattern.

* **Why Use This Skill (Rationale)**: A track containing only "Down" energy feels robotic and heavy (like a relentless four-on-the-floor kick with no hi-hats). Adding "Up" energy gives it momentum and bounce, but it remains symmetrical and slightly sterile. Adding the "Side-to-Side" (16th note syncopation) tricks the brain into feeling a human, pushing-and-pulling groove. This mirrors fundamental groove theory, where syncopation acts as the "seasoning" that challenges a predictable rhythmic grid. 

* **Overall Applicability**: This is universally applicable to programming drum beats (Kick = Down, Hat = Up, Ghost Snare/Perc = Side), writing basslines, or sequencing arpeggiated synths. It shines particularly in dance music, neo-soul, boom-bap, and any genre where the "feel" of the rhythm is the driving force.

* **Value Addition**: Instead of a flat sequence of notes, this skill explicitly codes the interplay of structural beats vs. syncopated off-beats, creating a complete, breathing musical riff with distinct velocity and pitch contours for each energy layer.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Time Signature**: 4/4
  * **Grid**: 1/16th notes
  * **Down Energy**: Beats 1.0, 2.0, 3.0, 4.0
  * **Up Energy**: Beats 1.5, 2.5, 3.5, 4.5
  * **Side-to-Side Energy**: Select 16th-note subdivisions, e.g., 1.75, 2.25, 3.75, 4.25.
  * **Durations**: Staccato notes (0.2 beats) to ensure the syncopated gaps are clean and audible.

* **Step B: Pitch & Harmony**
  * **Down Energy**: Root note (low octave) for grounding.
  * **Up Energy**: Root note (upper octave) or Fifth for lift.
  * **Side-to-Side Energy**: Minor/Major 3rd or 5th, creating a melodic interplay that weaves between the structural roots.

* **Step C: Sound Design & FX**
  * **Instrument**: A stock `ReaSynth` programmed with a quick decay to make the rhythmic interplay extremely obvious.
  * **FX Chain**: `ReaComp` to glue the velocities together and prevent the syncopated notes from getting lost. 

* **Step D: Mix & Automation**
  * Velocities are tiered: Down beats are hardest (110), Up beats are softer (80) to feel "lighter", and Side-to-Side notes are medium-hard (95) to poke through as accents.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| 3-Energy Rhythmic Interplay | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise mathematical placement on the 1/4, 1/8, and 1/16 grids. |
| Tiered Dynamics | MIDI Velocity control | Matches the tutorial's concept of grounding (heavy) vs airy (light) energies. |
| Synth Sound | FX chain (`ReaSynth`) | Provides immediate audio feedback of the "grindy" synth riff demonstrated in the video without relying on external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The core lesson of the video is pure rhythmic theory and sequence programming, which ReaScript's MIDI API handles perfectly. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "3-Energy Groove Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a synth groove combining Down, Up, and Side-to-Side energies.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Extract scale details
    root_val = NOTE_MAP.get(key.upper() if key.upper() in NOTE_MAP else key.capitalize(), 0)
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Pitch definitions based on the scale
    # Ensure scale arrays don't go out of bounds if using pentatonic
    idx_3rd = 2 if len(scale_intervals) > 2 else 1
    idx_5th = 4 if len(scale_intervals) > 4 else 2
    
    pitch_down = root_val + scale_intervals[0] + 36   # Root (Octave 3) - Grounding
    pitch_up   = root_val + scale_intervals[0] + 48   # Octave up (Octave 4) - Airy/Lifting
    pitch_side = root_val + scale_intervals[idx_3rd] + 36 # 3rd degree - Melodic/Syncopated

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_duration_sec = 60.0 / bpm
    bar_length_sec = beat_duration_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Note Duration (Staccato 16th note feel)
    note_duration_beats = 0.2

    # Rhythmic grid configuration (in beat positions relative to a 4-beat bar)
    down_beats = [0.0, 1.0, 2.0, 3.0]
    up_beats   = [0.5, 1.5, 2.5, 3.5]
    side_beats = [0.75, 1.25, 2.75, 3.25] # Syncopated 16ths
    
    note_count = 0

    # === Step 4: Insert MIDI Notes ===
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        # 1. DOWN ENERGY (Heavy, Grounding)
        for b in down_beats:
            start_time_sec = (bar_offset_beats + b) * beat_duration_sec
            end_time_sec = start_time_sec + (note_duration_beats * beat_duration_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            vel = min(127, int(velocity_base * 1.1)) # Accent Downbeats
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_down, vel, False)
            note_count += 1
            
        # 2. UP ENERGY (Light, Airy)
        for b in up_beats:
            start_time_sec = (bar_offset_beats + b) * beat_duration_sec
            end_time_sec = start_time_sec + (note_duration_beats * beat_duration_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            vel = max(1, int(velocity_base * 0.8)) # Softer Upbeats
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_up, vel, False)
            note_count += 1
            
        # 3. SIDE-TO-SIDE ENERGY (Syncopated, Chaos)
        for b in side_beats:
            start_time_sec = (bar_offset_beats + b) * beat_duration_sec
            end_time_sec = start_time_sec + (note_duration_beats * beat_duration_sec)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
            
            vel = min(127, int(velocity_base * 0.95)) # Medium Velocity
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch_side, vel, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument and FX Chain ===
    # Add a stock synth to immediately hear the result
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth for a pluck/staccato feel to hear the syncopation clearly
    # Param 1 = Attack (0.0 = fast)
    # Param 2 = Decay (0.2 = fast decay)
    # Param 3 = Sustain (0.0 = no sustain)
    # Param 4 = Release (0.1 = fast release)
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.0) 
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.2)
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.0)
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1)
    
    # Add ReaComp to catch the accents and glue the groove
    fx_comp = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 0, -12.0) # Thresh
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 1, 4.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 2, 5.0)   # Attack (ms)
    RPR.RPR_TrackFX_SetParam(track, fx_comp, 3, 50.0)  # Release (ms)

    return f"Created '{track_name}' with {note_count} groove notes (Down, Up, Side-to-Side) over {bars} bars at {bpm} BPM."
```