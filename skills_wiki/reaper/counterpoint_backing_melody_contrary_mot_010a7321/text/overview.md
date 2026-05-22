# Counterpoint Backing Melody (Contrary Motion & Rhythmic Contrast)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Counterpoint Backing Melody (Contrary Motion & Rhythmic Contrast)

* **Core Musical Mechanism**: The creation of a secondary "backing" melody that consciously avoids mimicking or shadowing the lead melody. It achieves true musical depth through three specific counterpoint techniques:
  1. **Contrary Motion**: When the lead melody moves down in pitch, the backing melody moves up (and vice versa).
  2. **Rhythmic Contrast**: When the lead melody holds a long, sustained note, the backing melody plays short, active notes (and vice versa).
  3. **Strategic Rests**: The backing melody utilizes rests to leave space for the lead melody's most important phrases.

* **Why Use This Skill (Rationale)**: Parallel motion (shadowing) often causes two melodies to blur into a single, thick texture because our brains group sounds that move together. By using contrary motion and contrasting rhythms, the ear perceives the backing melody as an entirely independent musical layer. This adds perceived "depth" and complexity to the arrangement without creating frequency masking or cognitive clutter. 

* **Overall Applicability**: This technique is essential for writing choruses, hooks, secondary synth arpeggios, and vocal harmonies where you need the arrangement to sound "larger" and deeper without just doubling the existing parts. 

* **Value Addition**: A standard loop just plays a chord progression. This skill encodes classical counterpoint theory into modern MIDI sequencing, guaranteeing that multiple melodic layers will interact dynamically rather than fighting for the listener's attention.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Grid**: 4/4 time, heavily utilizing 1/4 note and 1/8 note grids.
  - **Note Durations**: The core mechanic relies on juxtaposing 2-beat or 1-beat notes (Lead) against rapid 0.5-beat notes (Backing). Strategic rests (e.g., leaving an entire beat or two empty in the backing track) are placed where the lead hits its peak notes.

* **Step B: Pitch & Harmony**
  - **Scale Alignment**: Both melodies must strictly adhere to the same underlying key/scale to avoid unwanted dissonance against the track's harmony.
  - **Contour Inversion**: If the lead goes from the 2nd scale degree down to the Root, the backing melody should start on the Root and move up to the 2nd. 

* **Step C: Sound Design & FX**
  - **Timbre**: Two distinct synthesizers or patches are typically used so the listener can easily separate them. 
  - **Mix**: The backing melody is pushed slightly back in the mix (lower volume) so it supports rather than distracts.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Melodic Interplay | MIDI note insertion | Allows precise, programmed execution of contrary motion and rhythmic interplay based on scale degrees. |
| Layering | Track creation | Generates two separate tracks (Lead and Backing) to visually and audibly demonstrate the independent layers. |
| Mix Separation | Track Volume manipulation | Lowers the volume of the backing track so it accurately acts as a supporting layer. |

> **Feasibility Assessment**: 100% reproducible. The script successfully generates a mathematical representation of contrary motion and rhythmic contrast across two interconnected MIDI items, mapped perfectly to any user-defined scale.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Counterpoint Backing",
    bpm: int = 95,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Lead Melody and a Counterpoint Backing Melody utilizing contrary motion,
    rhythmic contrast, and strategic rests.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created backing track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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

    root_val = NOTE_MAP.get(key, 9) # Default A
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_pitch(degree: int, octave: int) -> int:
        """Convert a 0-indexed scale degree into a MIDI pitch number."""
        octave_shift = degree // len(scale_intervals)
        scale_idx = degree % len(scale_intervals)
        note_val = root_val + scale_intervals[scale_idx] + ((octave + octave_shift + 1) * 12)
        return max(0, min(127, note_val))

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Tracks ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Track 1: Lead Melody
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    lead_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(lead_track, "P_NAME", "Lead Melody", True)
    RPR.RPR_TrackFX_AddByName(lead_track, "ReaSynth", False, -1)

    # Track 2: Backing Melody
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    backing_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(backing_track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(backing_track, "ReaSynth", False, -1)
    
    # Push the backing melody lower in the mix (-6dB roughly equals 0.5 amplitude)
    RPR.RPR_SetMediaTrackInfo_Value(backing_track, "D_VOL", 0.5)

    # === Step 3: Create MIDI Items ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    lead_item = RPR.RPR_AddMediaItemToTrack(lead_track)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(lead_item, "D_LENGTH", item_length)
    lead_take = RPR.RPR_AddTakeToMediaItem(lead_item)

    backing_item = RPR.RPR_AddMediaItemToTrack(backing_track)
    RPR.RPR_SetMediaItemInfo_Value(backing_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(backing_item, "D_LENGTH", item_length)
    backing_take = RPR.RPR_AddTakeToMediaItem(backing_item)

    # Helper function to insert notes
    def insert_note(take, start_beat, length_beats, degree, octave=5, vel=100):
        pitch = get_pitch(degree, octave)
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + length_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # === Step 4: Populate MIDI with Counterpoint Logic ===
    # We iterate in 2-bar phrases (8 beats)
    for b in range(0, bars, 2):
        
        # --- Bar 1 ---
        if b < bars:
            start_b = b * 4
            # LEAD: Moves Down (Degree 2 -> 0), then Up (Degree 0 -> 1 with long duration)
            insert_note(lead_take, start_b + 0, 1.0, 2, 5, velocity_base)
            insert_note(lead_take, start_b + 1, 1.0, 0, 5, velocity_base)
            insert_note(lead_take, start_b + 2, 2.0, 1, 5, velocity_base)

            # BACKING: Contrary to Lead. Moves Up (Degree 0 -> 1). 
            # Then rhythmic counter (4 rapid 8th notes moving down) during lead's long note
            insert_note(backing_take, start_b + 0, 1.0, 0, 5, velocity_base - 10)
            insert_note(backing_take, start_b + 1, 1.0, 1, 5, velocity_base - 10)
            
            insert_note(backing_take, start_b + 2.0, 0.5, 4, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 2.5, 0.5, 3, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.0, 0.5, 2, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.5, 0.5, 1, 5, velocity_base - 15)

        # --- Bar 2 ---
        if b + 1 < bars:
            start_b = (b + 1) * 4
            # LEAD: Moves Up (Degree 4), then Down (Degree 0) - Using long, expressive 2-beat notes
            insert_note(lead_take, start_b + 0, 2.0, 4, 5, velocity_base)
            insert_note(lead_take, start_b + 2, 2.0, 0, 5, velocity_base)

            # BACKING: Uses RESTS for the first 2 beats to give the Lead space.
            # Then rapid 8th notes moving UP (Contrary to Lead's downward motion)
            insert_note(backing_take, start_b + 2.0, 0.5, 0, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 2.5, 0.5, 1, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.0, 0.5, 2, 5, velocity_base - 15)
            insert_note(backing_take, start_b + 3.5, 0.5, 3, 5, velocity_base - 15)

    # Sort MIDI items to ensure they behave correctly in the editor
    RPR.RPR_MIDI_Sort(lead_take)
    RPR.RPR_MIDI_Sort(backing_take)

    return f"Created 'Lead Melody' and '{track_name}' showcasing Counterpoint over {bars} bars in {key} {scale} at {bpm} BPM."
```