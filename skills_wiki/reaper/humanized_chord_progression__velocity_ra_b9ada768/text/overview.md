### 1. High-level Design Pattern Extraction

> **Skill Name**: Humanized Chord Progression (Velocity Ramping & Voicing)

* **Core Musical Mechanism**: The tutorial demonstrates the transition from robotic, statically drawn MIDI blocks (max velocity) to a "humanized" performance by dragging a linear ramp/curve across the velocity Control Change (CC) lane and tweaking individual note velocities. The core mechanism is **velocity contouring**—varying how hard each note is struck to create a dynamic, living performance.
* **Why Use This Skill (Rationale)**: When all notes in a chord are played at exact maximum velocity (127) at the exact same time, it sounds mechanical and synthetic. In real life, a pianist plays the root note with a different weight than the third or fifth, and a musical phrase naturally crescendos (swells) or decrescendos. Contouring the velocities of a MIDI sequence prevents ear fatigue and breathes emotion into virtual instruments.
* **Overall Applicability**: This technique is universally necessary for programming realistic acoustic instruments (pianos, strings, orchestral percussion) and is highly effective for building swelling synth pads, lo-fi keys, or emotional verse sections in any genre.
* **Value Addition**: Instead of a flat block of MIDI notes, this skill computes a multi-bar chord progression where the overall phrase gradually builds in intensity (velocity crescendo) while internally, each chord features realistic dynamic voicing (the root is heaviest, the third is softest).

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time signature: 4/4.
  * Rhythm: Whole notes (1 chord per bar) spanning across a 4-bar phrase.
  * The notes snap perfectly to the grid at the start of each bar.

* **Step B: Pitch & Harmony**
  * Key/Scale: Configurable (e.g., C Major).
  * Harmony: A standard 4-chord progression (I - V - vi - IV).
  * Voicings: Standard triads, but the *velocities* inside the triad are weighted (Root = Base Velocity, 3rd = -15% velocity, 5th = -5% velocity).

* **Step C: Sound Design & FX**
  * Instrument: The tutorial uses a 3rd party VST ("Grand Piano" by Audiolatry). Since 3rd party VSTs cannot be guaranteed in all environments, the pattern will fall back to adding `ReaSynth` to ensure the script is safe and executable, while replicating the MIDI structure identically.

* **Step D: Mix & Automation**
  * Velocity Swell: The phrase ramps over the 4 bars. Bar 1 starts quieter (e.g., 60 velocity), and by Bar 4, the chords peak (e.g., 110 velocity), mimicking the linear click-and-drag velocity automation shown in the CC lane at `05:54` in the video.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| MIDI Chord Creation | `RPR_MIDI_InsertNote` | Allows us to define exact musical pitches via math instead of relying on pre-recorded items. |
| Velocity Humanization | Algorithmic Velocity Math | We calculate a linear ramp across the bars and apply individual offsets to the root, 3rd, and 5th to replicate the manual CC lane dragging shown. |
| Sound Generator | `RPR_TrackFX_AddByName` (ReaSynth) | Provides a stock, built-in tone generator to hear the chords without depending on unavailable third-party VSTs. |

> **Feasibility Assessment**: 95% reproducible. The exact third-party piano VST from the video is substituted with a stock REAPER instrument, but the core MIDI manipulation, piano roll logic, velocity editing, and algorithmic humanization represent the exact techniques taught in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 70,
    **kwargs,
) -> str:
    """
    Create a Humanized Chord Progression with velocity ramping in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (defaults to 4).
        velocity_base: Base starting MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR
    import math

    # === Music Theory Lookups ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Get base pitch (Octave 3)
    root_pitch = NOTE_MAP.get(key.upper() if len(key)==1 else key.capitalize(), 0) + 48
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    # Define a common 4-chord progression based on scale degrees (0-indexed)
    # Major: I - V - vi - IV (0, 4, 5, 3)
    # Minor: i - VI - III - VII (0, 5, 2, 6)
    if scale == "major":
        progression_degrees = [0, 4, 5, 3] 
    else:
        progression_degrees = [0, 5, 2, 6]

    def get_pitch_in_scale(degree_index):
        octave_offset = (degree_index // 7) * 12
        scale_degree = degree_index % 7
        return root_pitch + octave_offset + scale_intervals[scale_degree]

    # === Step 1: Initialize Project & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Create new track additively
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Add FX (Stock Instrument Fallback) ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Lower volume slightly to avoid clipping on chords
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # === Step 3: Create MIDI Item & Take ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    bar_length_sec = sec_per_beat * beats_per_bar
    total_length_sec = bar_length_sec * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
    
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert "Humanized" MIDI Notes ===
    # We will loop through the progression, placing one chord per bar.
    # Velocity will gradually crescendo (ramp up) over the progression.
    end_velocity_target = min(127, velocity_base + 40) # Ramp up by 40
    
    note_count = 0
    
    for bar_idx in range(bars):
        # Determine which chord in the progression we are on
        prog_idx = bar_idx % len(progression_degrees)
        root_degree = progression_degrees[prog_idx]
        
        # Build triad (root, 3rd, 5th)
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4]
        
        # Calculate timing for this bar (whole notes)
        start_time = bar_idx * bar_length_sec
        end_time = start_time + bar_length_sec
        
        # Convert absolute time to PPQ (pulses per quarter note)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Calculate overall velocity swell for this bar (linear interpolation)
        progress = bar_idx / max(1, (bars - 1))
        bar_base_vel = velocity_base + (end_velocity_target - velocity_base) * progress
        
        # Insert notes with internal chord voicing humanization
        for i, degree in enumerate(chord_degrees):
            pitch = get_pitch_in_scale(degree)
            
            # Voicing humanization:
            # Root is strongest, 3rd is quietest (-15%), 5th is mid (-5%)
            if i == 0:
                note_vel = bar_base_vel
            elif i == 1:
                note_vel = bar_base_vel * 0.85
            else:
                note_vel = bar_base_vel * 0.95
                
            # Clamp velocity
            note_vel = max(1, min(127, int(note_vel)))
            
            # Insert note
            # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), note_vel, True)
            note_count += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    
    # Update timeline/UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} humanized chord notes over {bars} bars at {bpm} BPM."
```