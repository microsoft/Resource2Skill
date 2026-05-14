# Chromatic Sampler Instrument Setup (Pitched Chop)

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: Chromatic Sampler Instrument Setup (Pitched Chop)

* **Core Musical Mechanism**: The tutorial demonstrates how to transform a single, static audio sample (like a guitar note or vocal snippet) into a fully playable, polyphonic, chromatic synthesizer patch using ReaSamplOmatic5000.
* **Why Use This Skill (Rationale)**: This technique bridges the gap between audio and MIDI. By enabling "Obey note-offs" and "Semitone shifted" mode, the static audio file is forced to respect MIDI note durations and pitch tracking. Musically, this creates a distinct, artificial "chop" sound because the attack transients and formants are pitched up/down unnaturally, creating the classic psychoacoustic signature of 90s sampler-based music. 
* **Overall Applicability**: This is a fundamental workflow for lo-fi hip-hop (piano/guitar chops), EDM and future bass (vocal chops), and old-school jungle/rave (stab chords).
* **Value Addition**: The script below encodes the precise, syncopated, staccato rhythmic framework required to actually play a chopped sample effectively, while configuring the exact track routing and plugin environment shown in the tutorial.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, highly effective between 90-120 BPM.
  - **Rhythm**: 16th-note syncopation (e.g., triggering on the "a" of beat 1, or the "and" of beat 2). 
  - **Duration**: Strict staccato (very short) note lengths. This is absolutely critical to trigger the sampler's "note-off" behavior demonstrated in the video.
* **Step B: Pitch & Harmony**
  - **Scale**: Minor Pentatonic. Pentatonic scales are ideal for vocal/instrument chops because they avoid dissonant half-steps, allowing the producer to jump wildly across the keyboard while remaining musically safe.
* **Step C: Sound Design & FX**
  - **Instrument**: ReaSamplOmatic5000 (RS5K).
  - **Settings**: "Obey note-offs" (stops the sample when the key is released), "Semitone shifted" (maps pitch across the keyboard), and adjusting the Pitch@Start to map the sample's root note.
* **Step D: Mix & Automation**
  - No advanced automation shown, though this technique is universally followed by applying reverb and delay tails to the dry chops.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Plugin Instantiation | `RPR_TrackFX_AddByName` | Sets up the exact RS5K instance shown in the tutorial. |
| Staccato Chop Rhythm | MIDI note insertion | Requires precise, mathematical note lengths and syncopated placements to demonstrate the "obey note-off" behavior of the sampler. |
| Playback Fallback | FX Chain (ReaSynth) | Since an automated API script cannot guess local `.wav` file paths on a user's machine, ReaSynth is added to ensure the generated pattern produces immediate, audible sound. |

> **Feasibility Assessment**: 80% — The code perfectly creates the track, the precise staccato MIDI pattern, and the FX chain. However, REAPER's ReaScript API does not natively support injecting an arbitrary external `.wav` file into RS5K without highly complex and brittle State Chunk string manipulation. The code sets up the exact environment, but relies on the user to perform the final visual step shown in the video: dragging a sample into the plugin window.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pitched Chop Sampler",
    bpm: int = 110,
    key: str = "D",
    scale: str = "pentatonic_minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a track with ReaSamplOmatic5000 and a syncopated, staccato MIDI pattern 
    designed for chopped samples. 

    Note: Drag your own audio sample into the RS5K interface and set the mode to 
    'Semitone shifted' to complete the tutorial's effect. ReaSynth is included as 
    a temporary fallback so the pattern makes sound immediately.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain ===
    # Add the Sampler from the tutorial
    RPR.RPR_TrackFX_AddByName(track, "ReaSamplOmatic5000", False, -1)
    # Add ReaSynth as a fallback so the MIDI clip produces sound before a sample is loaded
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)
    
    # Syncopated 16th-note rhythm grid for "chopped" feel
    # Format: (16th note position, duration in 16ths, scale degree index)
    rhythm_grid = [
        (0, 1, 0),    # Beat 1
        (3, 1, 2),    # Beat 1 'a' (syncopation)
        (6, 1, 1),    # Beat 2 'and' (syncopation)
        (8, 1, 0),    # Beat 3
        (11, 1, 3),   # Beat 3 'a' (syncopation)
        (14, 1, 4)    # Beat 4 'and' (syncopation)
    ]

    sixteenth_sec = bar_length_sec / 16.0
    root_midi = 60 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    
    note_count = 0

    # === Step 5: Insert MIDI Notes ===
    for bar in range(bars):
        bar_offset_sec = bar * bar_length_sec
        for pos, dur, degree in rhythm_grid:
            # Calculate timing in seconds
            start_sec = bar_offset_sec + (pos * sixteenth_sec)
            # Multiply duration by 0.6 to make it sharply staccato, forcing RS5K "note-off" behavior
            end_sec = start_sec + (dur * sixteenth_sec * 0.6)  
            
            # Convert to PPQ for REAPER API
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Calculate Pitch
            octave = degree // len(scale_intervals)
            note_idx = degree % len(scale_intervals)
            pitch = root_midi + (octave * 12) + scale_intervals[note_idx]
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
            note_count += 1
            
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} staccato notes over {bars} bars at {bpm} BPM. Please open RS5K to drag in a sample."
```