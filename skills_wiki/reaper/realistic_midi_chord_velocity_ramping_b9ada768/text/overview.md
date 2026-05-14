### 1. High-level Design Pattern Extraction

**Skill Name**: Realistic MIDI Chord Velocity Ramping

* **Core Musical Mechanism**: Modulating MIDI note velocities over time in a smooth, continuous curve (crescendo/decrescendo) instead of using flat, static velocity values. In the tutorial, the creator demonstrates drawing a ramp in the CC velocity lane to shape a sequence of copied chords/notes.
* **Why Use This Skill (Rationale)**: Flat, static velocities sound robotic and artificial. Acoustic instruments (like a Grand Piano) respond dramatically to the force of key presses—altering not just volume, but harmonic content and brightness. Creating velocity swells adds "breath," groove, and emotional realism to a programmed MIDI performance.
* **Overall Applicability**: This technique is essential for programming realistic pianos, string sections, brass, and organic drum patterns (e.g., hi-hat swells, ghost notes on a snare). 
* **Value Addition**: A standard loop of quantized MIDI chords lacks human feel. By procedurally applying an LFO-like or triangular math curve to the MIDI velocities, we encode the physical dynamics of a human player swelling into the downbeat of a measure.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time Signature: 4/4
  * BPM: 120 (Configurable)
  * Rhythmic Grid: 8th notes (driving chord pulse). 
  * Note Duration: Slightly staccato (e.g., 90% of a full 8th note) to leave space between the strikes and prevent muddy overlapping.

* **Step B: Pitch & Harmony**
  * Key/Scale: Minor scale (Configurable)
  * Progression: A classic 4-bar progression (i - VI - III - VII or similar parameterized degrees).
  * Voicings: Basic triads dynamically computed from the scale array.

* **Step C: Sound Design & FX**
  * Instrument: VSTi Grand Piano in the tutorial. We will substitute with `ReaSynth` as a guaranteed stock placeholder. 
  * FX Chain: Basic synthesis to emulate a simple electronic keyboard so the velocity changes are audible.

* **Step D: Mix & Automation**
  * CC Velocity Lane: Notes are assigned velocity mathematically in a "swell" (triangle wave) spanning the bar. The middle notes of the measure hit harder (around 100-110 velocity), while the beginning and end of the measure drop down to a softer touch (around 70 velocity).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Chords | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise control over note length, quantization, and individual velocities. |
| Harmony / Key | Python Scale Array Math | Dynamically computes triad intervals from the selected scale instead of relying on hardcoded pitch values. |
| Velocity Swell | Mathematical Ramp (Absolute offset) | Mimics the user dragging a linear "ramp" line across the CC Velocity lane as shown in the tutorial. |
| Instrument | `ReaSynth` via `RPR_TrackFX_AddByName` | Ensures the script runs safely and produces sound without relying on external third-party VSTs (like the specific Grand Piano). |

**Feasibility Assessment**: 100% — The fundamental music production lesson (MIDI item creation, drawing chords, and humanizing them with velocity curves) is perfectly replicable using pure ReaScript and stock functionality.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a chord progression with humanized velocity swells in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Peak MIDI velocity (0-127) at the height of the swell.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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

    # Ensure valid inputs
    root_pitch = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Common 4-bar progression (1-index corresponding to I, VI, III, VII)
    progression_degrees = [0, 5, 2, 6] 

    def get_scale_pitch(degree: int, octave: int = 4) -> int:
        """Returns the MIDI pitch for a given scale degree (0-indexed)."""
        scale_length = len(scale_intervals)
        octave_offset = degree // scale_length
        scale_degree = degree % scale_length
        return root_pitch + (octave + octave_offset) * 12 + scale_intervals[scale_degree]

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

    # === Step 4: Add Chords & Velocity Swells ===
    total_notes_created = 0
    note_duration_qn = 0.45  # Slightly less than an 8th note (0.5 QN) for staccato articulation
    
    for bar in range(bars):
        chord_root_deg = progression_degrees[bar % len(progression_degrees)]
        
        # Build triad (Root, 3rd, 5th)
        chord_degrees = [chord_root_deg, chord_root_deg + 2, chord_root_deg + 4]
        
        # 8 pulses per bar (8th notes)
        for eighth_note in range(8):
            # Calculate absolute time in seconds, then convert to PPQ
            start_qn = (bar * beats_per_bar) + (eighth_note * 0.5)
            end_qn = start_qn + note_duration_qn
            
            # Use REAPER TimeMap functions to resolve PPQ
            start_time = RPR.RPR_TimeMap2_QNToTime(0, start_qn)
            end_time = RPR.RPR_TimeMap2_QNToTime(0, end_qn)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Mathematical Velocity Swell: Creates a triangle wave shape mimicking mouse-drag automation.
            # Middle of the bar (eighth_note = 3.5) hits hardest at velocity_base.
            # Edges drop down by ~35 units.
            swell_offset = abs(eighth_note - 3.5) * 10
            vel = int(velocity_base - swell_offset)
            vel = max(1, min(127, vel)) # Clamp 1-127

            # Add each note of the triad
            for deg in chord_degrees:
                pitch = get_scale_pitch(deg, octave=4)
                
                # Add slight humanization to individual triad velocities
                humanized_vel = vel
                if deg == chord_degrees[1]:
                    humanized_vel -= int(velocity_base * 0.1) # 3rd is slightly softer
                elif deg == chord_degrees[2]:
                    humanized_vel -= int(velocity_base * 0.05) # 5th is medium
                
                humanized_vel = max(1, min(127, humanized_vel))

                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # Selected
                    False,          # Muted
                    start_ppq, 
                    end_ppq, 
                    0,              # Channel
                    pitch, 
                    humanized_vel, 
                    True            # noSort
                )
                total_notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain ===
    # Using stock ReaSynth as a stand-in for the Grand Piano
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth slightly to sound more like an electric key (lower sustain, some decay)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.3) # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1) # Sustain

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {total_notes_created} humanized velocity notes over {bars} bars at {bpm} BPM."
```