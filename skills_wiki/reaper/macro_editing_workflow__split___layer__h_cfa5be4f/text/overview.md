### 1. High-level Design Pattern Extraction

> **Skill Name**: Macro Editing Workflow: Split & Layer (Hocketing)

* **Core Musical Mechanism**: This video is primarily a workflow and UI customization tutorial for REAPER, rather than a guide on music theory. However, at **05:03**, the creator demonstrates a highly effective Custom Action: **"Split and put item above"** (selecting an item, splitting it, and moving the resulting piece up one track). Musically, this technique is the foundation of *hocketing*, vocal comping, and call-and-response arrangement—where a continuous musical phrase is split across multiple tracks to apply different processing, panning, or timbres to alternating sections.

* **Why Use This Skill (Rationale)**: While the video presents this as a time-saving macro, separating a continuous melody or drum break across multiple tracks is a foundational production technique. By routing halves of a phrase to different tracks, you can create stark contrast (e.g., Track A is dry and centered; Track B is heavy with reverb and panned wide). 

* **Overall Applicability**: This technique is universally used in vocal comping, glitch/IDM drum editing, and electronic music (where a single synth melody is split across multiple synth patches to create a "composite" lead). 

* **Value Addition**: Compared to a blank project, this skill provides a programmatic demonstration of the video's custom macro. It dynamically generates a musical phrase based on your chosen key/scale, splits it exactly in half, and routes the pieces to different tracks, mimicking the "Split and Move Up" action demonstrated in the tutorial.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: The script generates a continuous stream of 1/8th notes.
  - **Macro Timing**: The core macro divides the arrangement exactly in half. For a 4-bar phrase, the split occurs precisely at the start of Bar 3.

* **Step B: Pitch & Harmony**
  - The script uses the provided `key` and `scale` to generate an ascending arpeggiated line. 
  - The first half of the scale plays on the lower track; the second half plays on the upper track, demonstrating how continuous musical thought can be segmented.

* **Step C: Sound Design & FX**
  - **Routing/Layering**: The primary "effect" here is track separation. The macro creates an "Upper Track" (Destination) and a "Lower Track" (Source), allowing the user to easily assign contrasting VSTs or FX chains to the two halves of the phrase.

* **Step D: Mix & Automation**
  - By separating the items into two distinct tracks, independent volume and pan automation can be applied to each segment of the melody without requiring complex in-item automation envelopes.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Musical Generation | MIDI note insertion | Allows us to create a continuous phrase using the requested key and scale. |
| The Custom Action | `RPR_SplitMediaItem` & `RPR_MoveMediaItemToTrack` | Directly replicates the core custom macro demonstrated at 05:03 ("Split item at time selection" + "Move items up one track"). |

> **Feasibility Assessment**: 100% — While we cannot permanently edit the user's local REAPER UI shortcuts via script safely, we can fully replicate the *musical result* of the custom action demonstrated in the video. The script creates the tracks, generates the media, splits it, and moves it, performing the macro automatically.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Macro_Split",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Demonstrates the 'Split and Move Up' custom action shown in the video.
    Generates a continuous phrase, splits it in half, and moves the second half
    to a track above for layered processing / hocketing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name base for the created tracks.
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

    # === Step 2: Calculate Timings ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars
    split_time_sec = total_length_sec / 2.0  # We will split the phrase exactly in half

    # === Step 3: Create Upper and Lower Tracks ===
    num_tracks = RPR.RPR_CountTracks(0)
    
    # Upper Track (Destination)
    RPR.RPR_InsertTrackAtIndex(num_tracks, True)
    upper_track = RPR.RPR_GetTrack(0, num_tracks)
    RPR.RPR_GetSetMediaTrackInfo_String(upper_track, "P_NAME", f"{track_name}_Upper", True)
    
    # Lower Track (Source)
    RPR.RPR_InsertTrackAtIndex(num_tracks + 1, True)
    lower_track = RPR.RPR_GetTrack(0, num_tracks + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(lower_track, "P_NAME", f"{track_name}_Lower", True)

    # === Step 4: Generate Continuous MIDI Item on Lower Track ===
    item = RPR.RPR_CreateNewMIDIItemInProj(lower_track, 0.0, total_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)
    
    root_note = NOTE_MAP.get(key, 0) + 48  # Start at octave 4
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    note_length_sec = bar_length_sec / 8.0  # 1/8th notes
    
    total_notes = bars * 8
    for i in range(total_notes):
        scale_degree = i % len(scale_intervals)
        octave_shift = (i // len(scale_intervals)) * 12
        pitch = root_note + scale_intervals[scale_degree] + octave_shift
        
        # Keep pitch within safe MIDI bounds
        if pitch > 127: pitch = 127
        
        start_time = i * note_length_sec
        end_time = start_time + (note_length_sec * 0.8) # 80% gate length
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Execute the "Split and Move Up" Macro ===
    # Split the continuous phrase in half
    right_half_item = RPR.RPR_SplitMediaItem(item, split_time_sec)
    
    # Move the split portion up one track to demonstrate the macro
    if right_half_item:
        RPR.RPR_MoveMediaItemToTrack(right_half_item, upper_track)
        
    return f"Created workflow demo '{track_name}': generated {bars} bars of {key} {scale} MIDI, split phrase at {split_time_sec}s, and moved the second half to the track above at {bpm} BPM."
```