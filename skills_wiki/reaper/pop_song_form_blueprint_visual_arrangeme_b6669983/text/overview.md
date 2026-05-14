# Pop Song Form Blueprint (Visual Arrangement & Chords)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pop Song Form Blueprint (Visual Arrangement & Chords)

* **Core Musical Mechanism**: This skill translates the abstract concept of "Song Form" (Intro, Verse, Chorus, Bridge) into a concrete, visual, and musical project structure. It creates a staggered, multi-track "jigsaw puzzle" arrangement where each section type lives on its own dedicated, color-coded track. To make the form audible, it populates these sections with diatonic block chords, assigning different harmonic functions to different sections (e.g., a grounded progression starting on the `i` chord for the Verse, contrasting with an uplifting, epic progression starting on the `VI` chord for the Chorus). 

* **Why Use This Skill (Rationale)**: Modern pop and electronic music rely heavily on structural contrast to maintain listener interest (macrodynamics). Slicing, labeling, and color-coding sections—as shown in the tutorial—is a crucial workflow for analyzing reference tracks and building your own arrangements. By splitting different sections onto dedicated child tracks routed to a parent instrument bus, you create a visual "blueprint" that makes arranging, copying, and extending song sections effortless. 

* **Overall Applicability**: This is the ultimate starting point for a blank project. Instead of staring at an empty timeline, this skill instantly generates a full 52-bar pop arrangement structure, complete with foundational chords, allowing the producer to immediately start layering drums, bass, and melodies over a pre-defined map.

* **Value Addition**: It encodes the standard Pop/Top-40 arrangement timeline (Verse/Chorus structure) and pairs it with functional diatonic chord progressions, bridging the gap between mechanical DAW editing (slicing/coloring) and actual music theory composition.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Form**: Intro (4 bars) → Verse 1 (8 bars) → Chorus 1 (8 bars) → Verse 2 (8 bars) → Chorus 2 (8 bars) → Bridge (4 bars) → Chorus 3 (8 bars) → Outro (4 bars).
  - **Rhythm**: Whole-note block chords (1 chord per bar) leaving a slight 1/16th note gap at the end of each bar for articulation.

* **Step B: Pitch & Harmony**
  - Uses a parametric key and scale lookup table.
  - **Intro / Outro**: `i` (Tonic pedal/establishment)
  - **Verses**: `i - VI - III - VII` (Standard minor pop progression, grounded)
  - **Choruses**: `VI - III - VII - i` (Starts on the submediant for an emotional "lift")
  - **Bridge**: `iv - v - VI - VII` (Rising tension leading back into the final Chorus)

* **Step C: Sound Design & FX**
  - **Routing**: Creates a Parent Track ("Song Form Chords") armed with a basic `ReaSynth` generator.
  - **Visuals**: Creates 5 Child Tracks ("Intro", "Verse", "Chorus", "Bridge", "Outro"). Each track is assigned a distinct OS-level color code. Empty MIDI items are placed on these child tracks, forming a staggered, visual jigsaw puzzle of the song structure.

* **Step D: Mix & Automation**
  - Child tracks automatically route their MIDI and audio up to the Parent Track folder, keeping the mix console clean while allowing visual separation in the arrange window.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Creating the "Jigsaw" layout | `RPR_InsertTrackAtIndex` & Folder Routing | Matches the tutorial's workflow of dedicating specific tracks to specific song sections for structural clarity. |
| Visual Labeling | `I_CUSTOMCOLOR` & `P_NAME` manipulation | Replicates the color-coding and item naming demonstrated in the video to visually parse the song form. |
| Audible Structure | `RPR_CreateNewMIDIItemInProj` & `RPR_MIDI_InsertNote` | Fills the structural placeholders with actual diatonic chords, translating structural theory into musical data. |

> **Feasibility Assessment**: 100% reproduction of the structural concepts. While the tutorial featured slicing an existing audio file (which an AI cannot blindly do without specific transient data), this script generates the *exact visual and structural outcome* of that slicing process from scratch, elevating it into a generative composition tool.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "SongFormBlueprint",
    track_name: str = "Song Form Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 52,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a full visual and musical Pop Song Form arrangement structure.
    Generates a parent synth track with color-coded child tracks for each section,
    populated with appropriate diatonic chord progressions.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 48, "C#": 49, "Db": 49, "D": 50, "D#": 51, "Eb": 51,
                "E": 52, "F": 53, "F#": 54, "Gb": 54, "G": 55, "G#": 56,
                "Ab": 56, "A": 57, "A#": 58, "Bb": 58, "B": 59}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10]
    }

    def get_chord_notes(degree, scale_intervals, root_midi):
        idx = degree - 1
        notes = []
        # Build a standard triad (root, 3rd, 5th in the chosen scale)
        for i in [0, 2, 4]:
            scale_idx = (idx + i) % len(scale_intervals)
            octave_shift = (idx + i) // len(scale_intervals)
            note = root_midi + scale_intervals[scale_idx] + (octave_shift * 12)
            notes.append(note)
        return notes

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Parent Track (Synth) ===
    parent_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(parent_idx, True)
    parent_track = RPR.RPR_GetTrack(0, parent_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaSynth", False, -1)
    
    # Set parent to act as a folder
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)

    # === Step 3: Define Sections and Create Child Tracks ===
    section_types = {
        "Intro":  {"color": (70, 130, 180)},  # Steel Blue
        "Verse":  {"color": (60, 179, 113)},  # Sea Green
        "Chorus": {"color": (205, 92, 92)},   # Indian Red
        "Bridge": {"color": (147, 112, 219)}, # Medium Purple
        "Outro":  {"color": (218, 165, 32)}   # Goldenrod
    }
    
    track_refs = {}
    
    for i, (s_name, s_data) in enumerate(section_types.items()):
        child_idx = parent_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(child_idx, True)
        child_track = RPR.RPR_GetTrack(0, child_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(child_track, "P_NAME", s_name, True)
        
        # Apply color mapping (REAPER format: R + G*256 + B*65536 | OS Flag)
        r, g, b = s_data["color"]
        color_int = r + (g * 256) + (b * 65536) | 0x1000000
        RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_CUSTOMCOLOR", color_int)
        
        # The last child track must close the folder depth
        if i == len(section_types) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child_track, "I_FOLDERDEPTH", -1)
            
        track_refs[s_name] = child_track

    # === Step 4: Define Chronological Arrangement Form ===
    # Using 1-based scale degrees for chord progressions
    structure = [
        {"type": "Intro",  "name": "Intro",    "bars": 4, "prog": [1, 1, 1, 1]},
        {"type": "Verse",  "name": "Verse 1",  "bars": 8, "prog": [1, 6, 3, 7, 1, 6, 3, 7]},
        {"type": "Chorus", "name": "Chorus 1", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Verse",  "name": "Verse 2",  "bars": 8, "prog": [1, 6, 3, 7, 1, 6, 3, 7]},
        {"type": "Chorus", "name": "Chorus 2", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Bridge", "name": "Bridge",   "bars": 4, "prog": [4, 5, 6, 7]},
        {"type": "Chorus", "name": "Chorus 3", "bars": 8, "prog": [6, 3, 7, 1, 6, 3, 7, 1]},
        {"type": "Outro",  "name": "Outro",    "bars": 4, "prog": [1, 1, 1, 1]}
    ]

    current_time = 0.0
    bar_length_sec = (60.0 / bpm) * 4
    beat_length_sec = 60.0 / bpm
    
    root_midi = NOTE_MAP.get(key, 48)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    # === Step 5: Generate Items and MIDI ===
    for sec in structure:
        sec_length_sec = sec["bars"] * bar_length_sec
        target_track = track_refs[sec["type"]]
        
        # Create a dedicated MIDI item for this specific section on the corresponding track
        item = RPR.RPR_CreateNewMIDIItemInProj(target_track, current_time, current_time + sec_length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        RPR.RPR_GetSetMediaItemTakeInfo_String(take, "P_NAME", sec["name"], True)
        
        # Apply the section color to the item to make the form pop visually
        r, g, b = section_types[sec["type"]]["color"]
        color_int = r + (g * 256) + (b * 65536) | 0x1000000
        RPR.RPR_SetMediaItemInfo_Value(item, "I_CUSTOMCOLOR", color_int)
        
        # Populate the item with chords
        for i, degree in enumerate(sec["prog"]):
            chord_start = current_time + (i * bar_length_sec)
            # Leave a 1/16th note gap for articulation
            chord_end = chord_start + bar_length_sec - (beat_length_sec * 0.25) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, chord_end)
            
            notes = get_chord_notes(degree, scale_intervals, root_midi)
            for note in notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note, velocity_base, None)
                
        RPR.RPR_MIDI_Sort(take)
        current_time += sec_length_sec
        
    return f"Created Pop Song Blueprint with 8 labeled sections across 5 grouped tracks in {key} {scale} at {bpm} BPM."
```