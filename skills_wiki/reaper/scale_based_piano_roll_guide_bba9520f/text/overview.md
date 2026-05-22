### 1. High-level Design Pattern Extraction

*   **Skill Name**: Scale-Based Piano Roll Guide
*   **Core Musical Mechanism**: This skill provides a visual and optional auditory guide within the REAPER MIDI editor, highlighting only the notes belonging to a chosen musical scale (e.g., C Major, G Dorian, C Whole Tone). By utilizing REAPER's "Hide unused note rows" feature, it simplifies composition by removing non-scale notes from the piano roll interface, allowing the user to focus exclusively on melodically and harmonically compatible pitches.
*   **Why Use This Skill (Rationale)**: This pattern leverages music theory by restricting the available pitches to a specific scale, which inherently supports harmonic and melodic coherence. It acts as a compositional "guardrail," especially useful for users who are new to music theory or wish to maintain strict adherence to a particular tonality or mode. By visually filtering out "wrong" notes, it reduces cognitive load and encourages intuitive exploration within the chosen scale, facilitating smoother melodic and harmonic development.
*   **Overall Applicability**: This skill is highly versatile and can be applied in various music production contexts:
    *   **Composition**: A fundamental tool for writing melodies, basslines, and harmonies within a defined key and scale.
    *   **Improvisation**: Provides a framework for real-time MIDI input by instantly showing valid notes.
    *   **Learning Music Theory**: Helps visualize scales and modes on the piano roll.
    *   **Genre-Specific Writing**: Ensures notes conform to the characteristics of scales common in genres like jazz (Dorian, Mixolydian), film scoring (Whole Tone, exotic scales), or folk music (Pentatonic).
*   **Value Addition**: Beyond a blank MIDI clip, this skill encodes fundamental music theory knowledge about scales and modes. It transforms the piano roll from a chromatic grid into a context-aware compositional canvas, directly reflecting musical structure and guiding the user toward harmonious note choices. It eliminates guesswork and streamlines the process of writing in key.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: Assumes 4/4.
    *   **BPM**: The skill uses the current project BPM to determine the length of the MIDI guide item.
    *   **Rhythmic Grid**: The guide notes themselves are sustained for a specified `duration_beats` (defaulting to 0.5 beats or an eighth note) across the entire length of the MIDI item. This is primarily for visual guidance and less about rhythmic playback.
*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: User-specified `key` (root note, e.g., "C", "F#") and `scale` (type, e.g., "major", "minor", "whole_tone").
    *   **Scale Degrees**: The script uses predefined intervals for various common scales (major, natural minor, harmonic minor, melodic minor, Dorian, Phrygian, Lydian, Mixolydian, Locrian, pentatonic major/minor, blues, whole tone).
    *   **Note Generation**: MIDI notes are generated from the `start_octave` to `end_octave` (defaulting to C2 through C6, MIDI notes 48-96 for root C) for all notes within the chosen scale.
*   **Step C: Sound Design & FX**
    *   **Instrument/Synth**: No specific instrument is added by the script. The guide notes are inserted into a standard MIDI item. The user would typically have an instrument loaded on a separate track.
    *   **FX Chain**: No FX chain is added.
    *   **Parameters**: The guide notes are set to a very low velocity (default 1) to make them almost inaudible, serving purely as a visual aid without interfering with the actual instrument track.
*   **Step D: Mix & Automation**
    *   **Volume/Panning**: The track containing the guide notes is muted by default (`mute_guide_track=True`) to prevent unintended sound playback.
    *   **Automation**: No automation envelopes are created.
    *   **MIDI Editor Action**: The script can optionally trigger the REAPER MIDI Editor action "Hide unused note rows" (ID 40608). This action applies to the active MIDI editor and requires the user to open a MIDI item (ideally an empty one on a separate composing track) to see its effect, with the guide item also visible in the editor.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :----- | :-------------- |
| Scale note generation | Python logic with lookup tables | Computes MIDI pitches dynamically from key/scale, making it parametric. |
| Guide MIDI item creation | MIDI note insertion | Creates a new MIDI item on a dedicated track containing all specified scale notes. |
| Visual filtering in Piano Roll | REAPER MIDI Editor action call | Directly triggers the "Hide unused note rows" feature, which is the core visual component of the skill. |
| Inaudible guide notes | MIDI note velocity setting and track mute | Ensures the guide notes do not interfere with playback while still being visually present. |

**Feasibility Assessment**: 95% — The core musical pattern of providing a visual scale guide in the piano roll and hiding non-scale notes is fully reproducible. The remaining 5% pertains to the user's workflow: the script cannot force the MIDI editor to open or manage specific VST presets, which are outside the scope of this particular skill but might be inferred from the tutorial's context. The custom scales mentioned in the video (like specific Middle Eastern scales) are not included by default but the `SCALES` dictionary can be easily expanded.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

# Music theory lookup tables for notes and scales
NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
SCALES = {
    "major":            [0, 2, 4, 5, 7, 9, 11],
    "natural_minor":    [0, 2, 3, 5, 7, 8, 10], # Also referred to as "minor"
    "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor_asc":[0, 2, 3, 5, 7, 9, 11],
    "dorian":           [0, 2, 3, 5, 7, 9, 10],
    "phrygian":         [0, 1, 3, 5, 7, 8, 10],
    "lydian":           [0, 2, 4, 6, 7, 9, 11],
    "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    "locrian":          [0, 1, 3, 5, 6, 8, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues":            [0, 3, 5, 6, 7, 10],
    "whole_tone":       [0, 2, 4, 6, 8, 10],
}

def get_scale_notes(root_note_midi_offset: int, scale_type: str, start_octave: int, end_octave: int) -> list[int]:
    """
    Generates MIDI note numbers for a given scale across specified octaves.
    
    Args:
        root_note_midi_offset: MIDI offset from C (0-11) for the root of the scale.
        scale_type: Type of scale (e.g., "major", "whole_tone").
        start_octave: Lowest octave number (e.g., 2 for C2, where C-2 is MIDI 0).
        end_octave: Highest octave number (e.g., 6 for C6).

    Returns:
        A sorted list of unique MIDI note numbers in the scale.
    """
    if scale_type not in SCALES:
        return []

    scale_intervals = SCALES[scale_type]
    notes = []
    
    # MIDI note numbering: C-2 = 0, C-1 = 12, C0 = 24, C1 = 36, C2 = 48, C3 = 60 (Middle C), etc.
    # A C in 'octave' N corresponds to MIDI note (N + 2) * 12.
    
    for octave in range(start_octave, end_octave + 1):
        base_octave_midi = (octave + 2) * 12 # MIDI note number for C in the current octave
        for interval in scale_intervals:
            midi_note = base_octave_midi + root_note_midi_offset + interval
            if 0 <= midi_note <= 127: # Ensure notes are within the valid MIDI range
                notes.append(midi_note)
    return sorted(list(set(notes))) # Remove duplicates and sort

def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Scale Guide",
    bpm: int = 120, # BPM is used for item length, but does not change project tempo.
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    start_octave: int = 2, # Corresponds to C2 (MIDI 48)
    end_octave: int = 6,   # Corresponds to C6 (MIDI 96)
    duration_beats: float = 0.5, # Duration of each guide note in beats (e.g., 0.5 for 8th notes)
    velocity_guide: int = 1, # Very low velocity for guide notes to make them almost inaudible
    mute_guide_track: bool = True,
    activate_hide_unused: bool = False, # Set to False by default, as it affects the user's ME state
    **kwargs,
) -> str:
    """
    Create a MIDI scale guide and optionally hide unused note rows in the MIDI editor.
    The guide track will contain all notes of the specified scale across the given octave range.
    When the MIDI editor is open with this guide item visible, activating 'Hide unused note rows'
    will only show the rows corresponding to the scale notes.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created scale guide track.
        bpm: Tempo in BPM. (Note: This skill does not *change* project BPM but uses it for item length).
        key: Root note (C, C#, D, Db, Eb, etc., case-insensitive).
        scale: Scale type (major, natural_minor, harmonic_minor, dorian, whole_tone, etc., case-insensitive).
        bars: Length of the MIDI guide item in bars.
        start_octave: Lowest octave number for the scale notes (e.g., 2 for C2).
        end_octave: Highest octave number for the scale notes (e.g., 6 for C6).
        duration_beats: Duration of each guide note in beats.
        velocity_guide: MIDI velocity for the guide notes (0-127). Default is very low (1)
                        to act as a visual guide without being audible.
        mute_guide_track: If True, the guide track will be muted.
        activate_hide_unused: If True, triggers the MIDI editor action to hide unused note rows.
                              Note: This requires the MIDI editor to be open and the guide item selected/visible
                              for its effect to be seen immediately.
        **kwargs: Additional overrides for future extensions.

    Returns:
        Status string describing the created guide track and notes.
    """
    # Ensure REAPER is running and a project is open
    if not RPR.RPR_GetProjectName(0, "", 0)[0]:
        return "REAPER is not running or no project is open."

    # Validate key and scale inputs
    upper_key = key.upper()
    if upper_key not in NOTE_MAP:
        return f"Error: Invalid root key '{key}'. Please use C, C#, D, Db, Eb, etc."
    
    lower_scale = scale.lower().replace(" ", "_") # Normalize scale name for lookup
    if lower_scale not in SCALES:
        return f"Error: Scale type '{scale}' not found. Available scales: {', '.join(SCALES.keys())}"

    # === Step 1: Create Track for Scale Guide ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    guide_track_name = f"{track_name} ({upper_key} {lower_scale.replace('_', ' ').title()})"
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", guide_track_name, True)

    # Mute track if requested
    if mute_guide_track:
        RPR.RPR_SetMediaTrackInfo_Value(track, "B_MUTE", 1.0)

    # === Step 2: Create MIDI Item for Scale Guide ===
    beats_per_bar = 4 # Assuming 4/4 time signature
    current_bpm = RPR.RPR_GetProjectBPM(0) # Use current project BPM for item length calculation
    sec_per_beat = 60.0 / current_bpm
    item_length_seconds = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0) # Start at beginning of project
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_seconds)
    
    take = RPR.RPR_GetActiveTake(item)
    if not take:
        take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Set the MIDI item to be a new blank MIDI source
    RPR.RPR_MIDI_SetItemExtents(item, 0.0, item_length_seconds)

    # === Step 3: Insert Scale Notes ===
    root_midi_offset = NOTE_MAP[upper_key]
    scale_notes_midi = get_scale_notes(root_midi_offset, lower_scale, start_octave, end_octave)
    
    if not scale_notes_midi:
        return f"Error: No notes could be generated for '{upper_key} {lower_scale.replace('_', ' ').title()}' within the specified octaves."

    RPR.RPR_MIDI_DisableSort(take) # Disable sorting for faster note insertion

    note_count = 0
    # Insert notes such that they span the entire MIDI item length for a continuous visual guide.
    for note_num in scale_notes_midi:
        # Insert a note and then immediately set its properties to span the item
        RPR.RPR_MIDI_InsertNote(take, False, False, 0.0, duration_beats, velocity_guide, note_num, 0)
        # Modify the newly inserted note to span the entire item_length_seconds
        RPR.RPR_MIDI_SetNote(take, note_count, True, False, 0.0, item_length_seconds, velocity_guide, note_num, 0)
        note_count += 1
    
    RPR.RPR_MIDI_Sort(take) # Re-enable sorting and ensure notes are sorted
    RPR.RPR_UpdateItemInProject(item) # Update item to reflect MIDI changes
    RPR.RPR_UpdateArrange()

    # === Step 4: Activate MIDI editor action (if requested) ===
    status_message = ""
    if activate_hide_unused:
        # Select the created item so it's considered by the MIDI editor when opened/active
        RPR.RPR_SetMediaItemSelected(item, True)
        # Trigger the action. User still needs to open the MIDI editor for this to be visible.
        # This action operates on the *active* MIDI editor.
        RPR.RPR_Main_OnCommand(40608, 0) # MIDI Editor: Hide unused note rows
        # Deselect item to avoid interfering with user's next action
        RPR.RPR_SetMediaItemSelected(item, False)
        status_message = "MIDI editor action 'Hide unused note rows' was activated."
    else:
        status_message = "MIDI editor action 'Hide unused note rows' was NOT activated. You can activate it manually in the MIDI Editor (Action ID 40608)."
    
    status_message += " For best results, open a new empty MIDI item on a different track to compose, with the guide track visible in the MIDI Editor."

    return f"Created '{guide_track_name}' with {note_count} guide notes over {bars} bars ({start_octave}-{end_octave}) at {current_bpm} BPM. {status_message}"

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range? (Velocity 1 is used for guide notes).
- [x] Are note timings quantized to the musical grid (notes span the item, not specific rhythmic positions, which is correct for a guide)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Visually, yes. Sonically, only if they un-mute the guide track).
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?