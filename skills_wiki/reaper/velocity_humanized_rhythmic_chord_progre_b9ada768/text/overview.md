### 1. High-level Design Pattern Extraction

> **Skill Name**: Velocity-Humanized Rhythmic Chord Progression

* **Core Musical Mechanism**: The defining characteristic of this pattern is **MIDI Velocity Humanization**. Instead of static, identical velocity values (which sound robotic), the pattern assigns a strict velocity hierarchy to the notes within a chord (strong bass, softer inner voices) and introduces slight random variance. It applies this to a rhythmic block-chord progression to simulate a live keyboard player dynamically varying their finger pressure. 
* **Why Use This Skill (Rationale)**: In music production, heavily quantized and maxed-velocity MIDI loops sound artificial and fatiguing to the ear. By adjusting the velocity lane (as shown in the tutorial), we recreate the natural physical dynamics of a performance. A strong bass note anchors the fundamental frequency, while softer 3rds and 5ths prevent the mid-range from becoming muddy or overpowering.
* **Overall Applicability**: Essential for any genre utilizing virtual pianos, electric pianos, strings, or pad synthesizers (e.g., Lo-Fi Hip Hop, Pop, Neo-Soul, House). It serves as the rhythmic and harmonic backbone of a track.
* **Value Addition**: Compared to drawing static MIDI blocks, this skill encodes the concept of *chord voicing dynamics* (bass vs. harmony) and micro-dynamic variation, making virtual instruments instantly sound more expensive and realistic.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Quarter notes (1/4) with a slight staccato articulation (notes take up 90% of the beat to leave a tiny gap, preventing overlapping MIDI note choking).
  - **Tempo Range**: 100-120 BPM (defaults to 120 as shown in the tutorial).
* **Step B: Pitch & Harmony**
  - **Progression**: I - V - vi - IV (Diatonic progression derived parametrically from the chosen key and scale).
  - **Voicing**: Root position triads with an added sub-octave bass note (e.g., C2 + C3 + E3 + G3), explicitly recreating the "add an octave down below" technique from the tutorial.
* **Step C: Sound Design & FX**
  - **Instrument**: Uses REAPER's stock `ReaSynth` as a reliable stand-in for the "Grand Piano" VST shown in the tutorial.
  - **Parameters**: Lowered cutoff and a slightly extended release time to mimic a mellow piano or electric keyboard.
* **Step D: Mix & Automation**
  - **Velocities (The "Automation" substitute)**: 
    - Bass note: Strongest (Base velocity on downbeats, slightly softer on offbeats).
    - Inner chord notes: -10 to -15 velocity reduction relative to the bass, plus a ±5 randomized humanization factor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Voicing | MIDI note insertion | Allows stacking specific scale degrees (Root, 3rd, 5th, Bass) procedurally. |
| Velocity Humanization | MIDI note velocity | Replicates the CC lane velocity clicking/dragging shown in the tutorial directly at the note-creation level. |
| Instrument | FX Chain (ReaSynth) | Provides a self-contained, stock sound source so the script executes safely without needing external VSTs like the one in the video. |

> **Feasibility Assessment**: 100% reproduction of the *musical technique*. While the specific 3rd-party Grand Piano VST cannot be instantiated without assuming the user owns it, the core lesson—MIDI editing, chord creation, and velocity humanization—is perfectly reproduced using stock REAPER functions.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Humanized Piano Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create a Velocity-Humanized Rhythmic Chord Progression in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity for the strong bass notes (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import random

    # === Music Theory Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    root_pitch_class = NOTE_MAP.get(key.capitalize(), 0)
    base_midi_note = 48 + root_pitch_class # Octave 3 starting point
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])

    def get_scale_pitch(degree_zero_indexed):
        """Returns the MIDI pitch for a given diatonic scale degree."""
        octave = degree_zero_indexed // len(scale_intervals)
        idx = degree_zero_indexed % len(scale_intervals)
        return base_midi_note + (octave * 12) + scale_intervals[idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Instrument (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a more mellow, electric piano-ish pluck
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5)  # Square mix down
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.4)  # Release time extended

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Generate Humanized MIDI Notes ===
    # Standard I - V - vi - IV progression (0, 4, 5, 3 in zero-indexed scale degrees)
    progression = [0, 4, 5, 3] 
    note_count = 0

    for bar in range(bars):
        chord_root_degree = progression[bar % len(progression)]
        
        # Calculate triad pitches + sub-octave bass
        root_pitch = get_scale_pitch(chord_root_degree)
        third_pitch = get_scale_pitch(chord_root_degree + 2)
        fifth_pitch = get_scale_pitch(chord_root_degree + 4)
        bass_pitch = root_pitch - 12
        
        # 4 quarter-note chord strikes per bar
        for beat in range(4):
            start_pos = (bar * beats_per_bar + beat) * beat_length_sec
            # Leave a 10% gap so notes are slightly detached (staccato articulation)
            end_pos = start_pos + (beat_length_sec * 0.9)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            
            # --- Velocity Humanization Logic ---
            # Bass is heavy on downbeats (beats 0, 2), lighter on offbeats (beats 1, 3)
            v_bass = velocity_base if beat % 2 == 0 else velocity_base - 10
            
            # Inner chord voices are softer overall, with random human variance
            v_root = velocity_base - 12 + random.randint(-4, 4)
            v_third = velocity_base - 16 + random.randint(-5, 5)
            v_fifth = velocity_base - 14 + random.randint(-4, 4)
            
            # Ensure velocity constraints (1-127)
            v_bass = max(1, min(127, int(v_bass)))
            v_root = max(1, min(127, int(v_root)))
            v_third = max(1, min(127, int(v_third)))
            v_fifth = max(1, min(127, int(v_fifth)))
            
            # Insert notes
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, v_bass, True)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_pitch, v_root, True)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, third_pitch, v_third, True)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fifth_pitch, v_fifth, True)
            note_count += 4

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} velocity-humanized notes over {bars} bars at {bpm} BPM."
```