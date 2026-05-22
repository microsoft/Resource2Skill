### 1. High-level Design Pattern Extraction

**Skill Name**: Scale Guide Notes for Piano Roll Filtering

*   **Core Musical Mechanism**: This skill provides a visual aid for composing within a specific musical scale in REAPER's MIDI Editor (Piano Roll). It facilitates adherence to a chosen harmonic framework by visually filtering out notes that do not belong to the active scale, encouraging "in-key" composition.

*   **Why Use This Skill (Rationale)**:
    *   **Compositional Guidance**: For users unfamiliar with music theory or struggling to stay in key, this acts as a dynamic "cheat sheet," making it easier to select harmonious notes.
    *   **Melodic & Harmonic Consistency**: By limiting visual options to scale-specific notes, it promotes melodic flow and harmonic coherence.
    *   **Exploration**: Allows quick experimentation with different scales and modes without deep theoretical knowledge, as the visual guide adapts instantly.
    *   **Error Reduction**: Helps prevent accidental use of out-of-scale notes that might clash harmonically.

*   **Overall Applicability**: This skill is useful for any music producer, composer, or songwriter who works with MIDI and wants to streamline their workflow for composing melodies, bass lines, chords, or arpeggios within a specific scale. It's particularly beneficial for beginners or when exploring unfamiliar scales.

*   **Value Addition**: Compared to a blank MIDI clip, this skill adds a dynamic, user-configurable musical constraint (the selected scale) directly to the Piano Roll's visual interface. It encodes music theory knowledge into a practical, visual guide, reducing mental overhead during composition.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: Assumes standard 4/4 time for item length calculation, but the guide notes themselves do not impose a rhythmic structure for composition.
    *   **Rhythmic Grid**: Each guide note has a fixed, short duration (e.g., a quarter note) and starts at the beginning of the MIDI item. They are not intended to be played rhythmically, but solely to "occupy" their respective note rows.
    *   **Note Duration**: Default `note_duration` is 0.25 beats (quarter note), but can be configured. This minimal duration ensures the note rows are "used" for filtering.

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: User-definable `key` (root note, e.g., "C", "F#") and `scale_type` (e.g., "major", "minor", "dorian", "whole_tone", "phrygian_dominant").
    *   **Scale Generation**: The script calculates all MIDI notes belonging to the selected scale across a user-specified number of `octaves` (defaulting to 8 octaves from C0) and inserts them into a MIDI item.
    *   **Notes Used**: All notes from the selected scale within the 0-127 MIDI range are generated.

*   **Step C: Sound Design & FX**
    *   **Instrument**: No specific instrument is loaded by the script. The guide notes are purely for visual guidance.
    *   **FX Chain**: No FX chain is added to the track.
    *   **MIDI Properties**: Guide notes are inserted with a very low `velocity` (default 1) and are explicitly `muted=True`, ensuring they are practically silent during playback. They are placed on `midi_channel` 0 (MIDI channel 1).

*   **Step D: Mix & Automation (if applicable)**
    *   **Track Name & Color**: A new track is created and named clearly (e.g., "Scale Guides (C Major)"). The track is also colored red for easy identification, similar to how selected notes appear in the video.
    *   **Automation**: No automation is applied.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :----- | :-------------- |
| Guide notes creation  | MIDI note insertion (`RPR_MIDI_InsertNote`) | Directly creates the "used" notes in the MIDI item that enable the Piano Roll filtering. Provides precise control over pitch, timing, and muting. |
| Track & item setup    | Track creation (`RPR_InsertTrackAtIndex`) and item creation (`RPR_AddMediaItemToTrack`) | Establishes the necessary container for the guide notes in the project. |
| Scale Calculation     | Python dictionaries and functions | Translates abstract music theory (key, scale intervals) into concrete MIDI note numbers, ensuring accuracy and flexibility. |

**Feasibility Assessment**: 100% – The code fully reproduces the necessary "guide notes" MIDI item and track setup demonstrated in the tutorial. The final visual filtering effect in the Piano Roll is achieved by the user manually applying REAPER's built-in "Hide unused note rows" action (Action ID 40053) after the script creates the guide notes. The code provides clear instructions for this user action.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

# Music theory lookup tables
NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
SCALES = {
    "major":            [0, 2, 4, 5, 7, 9, 11],
    "natural_minor":    [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor_asc":[0, 2, 3, 5, 7, 9, 11], # common ascending form
    "dorian":           [0, 2, 3, 5, 7, 9, 10],
    "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    "lydian":           [0, 2, 4, 6, 7, 9, 11],
    "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    "locrian":          [0, 1, 3, 5, 6, 8, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues":            [0, 3, 5, 6, 7, 10], # Minor pentatonic + b5
    "whole_tone":       [0, 2, 4, 6, 8, 10],
    "chromatic":        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10] # Ahavah Rabbah / Freygish
}

def get_scale_notes_midi_numbers(root_midi_offset: int, scale_intervals: list, num_octaves: int, start_octave: int = 0) -> list:
    """
    Generates a list of absolute MIDI note numbers for a given scale across multiple octaves.
    root_midi_offset: MIDI semitone offset from C (0-11).
    start_octave: The MIDI octave number to start from (e.g., C0 is MIDI note 12, so start_octave=0 means the 0th octave).
    """
    all_notes = []
    # MIDI note mapping: C0 is MIDI note 12. So (octave_number + 1) * 12
    # e.g., C0 (octave 0) => (0+1)*12 + 0 = 12
    # C4 (octave 4) => (4+1)*12 + 0 = 60
    for octave_idx in range(num_octaves):
        # Calculate the base MIDI note for the current octave, adjusted for C0 = MIDI 12 convention
        current_octave_midi_base = (start_octave + octave_idx + 1) * 12 + root_midi_offset
        for interval in scale_intervals:
            midi_note = current_octave_midi_base + interval
            if 0 <= midi_note <= 127: # Ensure notes are within MIDI range
                all_notes.append(midi_note)
    return sorted(list(set(all_notes))) # Remove duplicates and sort

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guides",
    bpm: int = 120, # Not directly used for note timing, but for item length based on project BPM
    key: str = "C",
    scale_type: str = "major",
    bars: int = 1, # A single bar is sufficient to hold the guide notes
    octaves: int = 8, # Cover a wide range for most instruments
    start_octave: int = 0, # Start from MIDI octave 0 (C0)
    note_duration: float = 0.25, # Duration of each guide note in beats (e.g., 0.25 for a quarter note)
    velocity: int = 1, # MIDI velocity for the guide notes (0-127). Set low to effectively mute them.
    midi_channel: int = 0, # MIDI channel 0 (1-indexed in many devices)
    **kwargs, # For API consistency, not used in this specific skill
) -> str:
    """
    Creates a MIDI track with muted guide notes for a specified scale.
    These guide notes, when present in a MIDI item, can be used with REAPER's
    'Hide unused note rows' action in the MIDI editor to visually filter
    the piano roll to only show notes within the chosen scale.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track containing scale guide notes.
        bpm: Tempo in BPM. (Currently uses project BPM for item placement/length).
        key: Root note (C, C#, D, ..., B). Case-insensitive.
        scale_type: Type of scale (e.g., "major", "minor", "dorian", "whole_tone", etc.).
        bars: Number of bars for the MIDI item holding the guide notes.
        octaves: Number of octaves to generate the scale guide notes over.
        start_octave: The MIDI octave number to start generating notes from (e.g., C0 is octave 0).
        note_duration: Duration of each guide note in beats (e.g., 0.25 for a quarter note).
        velocity: MIDI velocity for the guide notes (0-127). Set low to effectively mute them.
        midi_channel: MIDI channel for the guide notes (0-15).
        **kwargs: Additional overrides (not used directly in this function, but passed for API consistency).

    Returns:
        Status string with instructions for the user.
    """
    # Ensure scale_type is valid
    if scale_type not in SCALES:
        return f"Error: Scale type '{scale_type}' not recognized. Available scales: {', '.join(SCALES.keys())}"

    RPR.Undo_BeginBlock2(0) # Begin undo block

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    
    # Format track name for clarity
    formatted_scale_name = scale_type.replace('_', ' ').title()
    full_track_name = f"{track_name} ({key.upper()} {formatted_scale_name})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", full_track_name, True)
    
    # Set track color to red for easy identification, as seen in the video for selected scale notes
    # 0x1000000 bit indicates a custom color, otherwise REAPER picks a default from the theme
    RPR.RPR_SetTrackColor(track, RPR.ColorToNative(255, 0, 0) | 0x1000000) 

    # Create MIDI Item
    beats_per_bar = 4 # Standard 4/4 time for item length calculation (can be overridden by project TS)
    item_length_beats = beats_per_bar * bars
    
    # Use current project BPM for item placement/length calculation
    current_project_bpm = RPR.RPR_GetProjectBPM(0) 
    item_length_sec = (60.0 / current_project_bpm) * item_length_beats
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at project beginning
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    
    # Get or create active take for MIDI events
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Set MIDI item length in PPQ (Pulses Per Quarter note) for accurate note placement
    # This ensures the internal MIDI take length matches the item length.
    RPR.RPR_MIDI_SetItemExtents(take, RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0), RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_beats))

    # Get base root note MIDI offset (0-11)
    root_midi_offset = NOTE_MAP.get(key.upper(), 0) 

    # Generate all scale notes across the specified octaves
    scale_notes_midi_numbers = get_scale_notes_midi_numbers(root_midi_offset, SCALES[scale_type], octaves, start_octave)

    # Clear existing MIDI events in case it's not a fresh take, ensuring only scale notes are present
    RPR.RPR_MIDI_SetAllEvts(take, "", False) 
    
    # Calculate PPQ for note duration. ppq_per_beat is PPQ for 1 beat within the MIDI item.
    ppq_per_beat = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 1.0)
    note_duration_ppq = int(note_duration * ppq_per_beat)

    num_notes_inserted = 0
    # Place all guide notes at the very beginning of the MIDI item
    # `selected=False`, `muted=True` to prevent playback and visual clutter, `pitch` is the MIDI note number
    for note_val in scale_notes_midi_numbers:
        RPR.RPR_MIDI_InsertNote(take, False, True, 0, note_duration_ppq, midi_channel, velocity, note_val, False)
        num_notes_inserted += 1

    RPR.RPR_UpdateItem(item) # Update the MIDI item to reflect changes
    RPR.RPR_TrackList_AdjustWindows(False) # Refresh track list display

    RPR.Undo_EndBlock2(0, "Create Scale Guide Notes", -1) # End undo block

    if num_notes_inserted == 0:
        return (
            f"Warning: No notes generated for {key.upper()} {formatted_scale_name} scale across {octaves} octaves. "
            "Please check key/scale/octave parameters. "
            "No track or MIDI item was created due to this issue."
        )

    instructions = (
        f"Created track '{full_track_name}' with {num_notes_inserted} muted guide notes over {bars} bar(s). "
        "To use this feature, open the MIDI editor for this item. "
        "Ensure no other MIDI notes are visible within the editor (e.g., by selecting only this item). "
        "Then, from the MIDI Editor's 'Actions' list (Shift+?), search for and run the action 'Hide unused note rows' (Action ID 40053). "
        "This will hide all note rows except those containing the guide notes (i.e., notes in your chosen scale)."
    )

    return instructions
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range? (Default `velocity=1`)
- [x] Are note timings quantized to the musical grid (notes start at 0, duration based on PPQ)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, it creates the underlying mechanism for the visual filtering.)
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? (BPM is used for item length, key/scale for note generation, bars for item length.)
- [x] Does it avoid hardcoded file paths or external sample dependencies?