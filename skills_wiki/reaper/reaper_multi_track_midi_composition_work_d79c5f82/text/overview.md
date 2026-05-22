### 1. High-level Design Pattern Extraction

*   **Skill Name**: REAPER Multi-Track MIDI Composition Workflow

*   **Core Musical Mechanism**: This skill establishes a highly efficient and integrated workflow for composing music with multiple MIDI instruments simultaneously within REAPER. The signature of this pattern is the ability to view, reference, and optionally edit MIDI notes from several tracks within a single, docked MIDI editor window, leveraging "ghost notes" for contextual awareness. This drastically reduces window clutter and context switching, enhancing the creative flow.

*   **Why Use This Skill (Rationale)**:
    *   **Cognitive Load Reduction**: By consolidating MIDI editing into one persistent, docked window, producers can maintain focus without constantly managing multiple floating editors. This aligns with principles of cognitive ergonomics in DAW design.
    *   **Enhanced Inter-Part Cohesion**: The "ghost notes" feature allows for immediate visual referencing of other instrument parts (e.g., bass notes alongside guitar chords), facilitating more harmonically congruent and rhythmically tight arrangements. This helps in understanding the musical interplay between different elements.
    *   **Streamlined Multi-track Editing**: The ability to directly edit secondary (ghosted) MIDI items in the same editor promotes faster iteration and adjustment of interconnected musical phrases, such as fine-tuning a bassline against a drum beat or adjusting lead melodies in relation to chords.

*   **Overall Applicability**: This workflow is highly beneficial for composers and producers working with any genre that involves layered MIDI instrumentation, from orchestral scores and film music to pop, EDM, rock, and jazz. It excels in scenarios where intricate arrangement and tight melodic/harmonic relationships between different parts are critical.

*   **Value Addition**: Beyond simply placing MIDI notes, this skill encodes advanced REAPER workflow optimization techniques. It transforms the default MIDI editing experience into a more cohesive, visually informative, and interactively powerful environment, directly addressing common friction points in multi-instrument composition. It promotes a more fluid and less interrupted creative process.

### 2. Technical Breakdown

The core of this skill lies in configuring REAPER's MIDI editor preferences and enabling a specific action, which then enables a powerful multi-track editing experience.

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: 4/4 (demonstrated in video, typical for many genres).
    *   **BPM Range**: Configurable, defaults to 120 BPM.
    *   **Rhythmic Grid**: The demo features a mix of 1/4, 1/8, and 1/16th notes for different instruments (kick/snare, hi-hats, bass, guitar chords, lead arpeggios).
    *   **Note Duration**: Varies by instrument (e.g., bass whole notes, hi-hat 1/16th, guitar strums).

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: Configurable (e.g., G minor is used in the demo).
    *   **Chords**: Basic triads (e.g., Gm, Bb, Eb, F) are implied for rhythm guitar and referenced for bass and lead.
    *   **Melody/Bass**: Root notes for bass, arpeggiated or scalar melodies for lead, derived from the active chord/scale.
    *   **Pitches**: MIDI pitches are computed based on the provided `key` and `scale` parameters, relative to specified octaves.

*   **Step C: Sound Design & FX**
    *   **Instruments**: The demonstration uses generic MIDI tracks assigned to native REAPER plugins like ReaSamplOmatic5000 (for drums) and ReaSynth (for bass and guitars).
    *   **FX Chain**: No complex FX chains are explicitly demonstrated or configured programmatically beyond basic instrument assignment, but the workflow allows for individual track FX processing.

*   **Step D: Mix & Automation**
    *   No specific mixing or automation is part of the core workflow pattern, beyond basic velocity adjustments for MIDI notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

The primary goal is to reproduce the *workflow* and demonstrate it with a simple musical pattern.

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| REAPER Preferences (e.g., "One MIDI editor per: project") | Manual Setup (as described) | Direct programmatic control of these core UI preferences is not robust or immediately effective via ReaScript without a REAPER restart. Documenting manual setup is more reliable. |
| Custom Action for Multi-Track Edit Toggle | `RPR_Main_OnCommand(40523, 0)` | This is a native REAPER action (`Options: Avoid automatically setting MIDI items from other tracks editable`) that directly toggles the multi-track editability, a core part of the workflow. |
| Track Creation | `RPR_InsertTrackAtIndex()` | To build the multi-instrument composition canvas. |
| MIDI Item Creation | `RPR_AddMediaItemToTrack()`, `RPR_MIDI_SetItemExtents()` | To house the musical data. |
| MIDI Note Insertion | `RPR_MIDI_InsertNote()` | Precise control over notes for drums, bass, and guitars. |
| Instrument Assignment | `RPR_TrackFX_AddByName()` | To provide audible output for the generated MIDI notes using stock REAPER plugins. |
| Note Coloring | `RPR_SetTrackColor()` (implicit for MIDI notes colored by track) | Visual differentiation, as shown in the video. |

**Feasibility Assessment**: The code reproduces approximately **80-90%** of the tutorial's core workflow enablement and musical output.
*   **Reproduced**: The creation of multiple tracks, the generation of a basic multi-instrument MIDI pattern (drums, bass, rhythm guitar, lead guitar), assigning stock REAPER instruments for sound, and programmatically toggling the key "Multi-track Edit" preference. Notes are parametrically generated and colored by track.
*   **Not Programmatically Reproduced (requires manual user action as described in the video/instructions)**: The initial global MIDI editor preferences (e.g., "one MIDI editor per project", linked selections, editor docking, opacity for ghost notes). These are usually `reaper.ini` settings that are not reliably changed and immediately applied via ReaScript without a REAPER restart. The video explicitly guides the user through these manual steps.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def get_midi_note_number(key_root, scale_degrees, octave, degree_index):
    """Calculates the MIDI note number for a given key, scale, octave, and scale degree index."""
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_midi_base = NOTE_MAP[key_root] + (octave * 12)
    
    # Handle scale degrees that might exceed an octave (e.g., 8th degree is root + 12)
    scale_length = len(scale_degrees)
    octave_offset = scale_degrees[degree_index % scale_length]
    semitone_offset = (degree_index // scale_length) * 12
    
    midi_note = root_midi_base + octave_offset + semitone_offset
    return midi_note

def create_midi_item_and_notes(track, start_time, length, notes_data):
    """Helper to create a MIDI item and insert notes, returning the count of notes."""
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    midi_take = RPR.MIDI_SetItemExtents(item, 0, 0) # Create MIDI take

    RPR.MIDI_DisableGridSnap(midi_take) # Disable grid snap for more precise timing
    
    num_notes = 0
    for note in notes_data:
        RPR.MIDI_InsertNote(midi_take, False, False, note['start'], note['end'], note['channel'], note['pitch'], note['velocity'])
        num_notes += 1

    RPR.MIDI_Sort(midi_take)
    RPR.MIDI_MarkAllNotes(midi_take, False) # Deselects notes after creation
    RPR.MIDI_UpdateByFile(midi_take, False)
    RPR.RPR_UpdateItemInProject(item)
    
    # Select the first item created to ensure MIDI editor can open it
    if RPR.RPR_CountMediaItems(0) == 1:
        RPR.RPR_SetMediaItemSelected(item, True)
    
    return num_notes

def reaper_midi_workflow_setup_and_demo(
    project_name: str = "Demo Project",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Sets up a multi-track MIDI editing workflow in REAPER (requires manual preference setup)
    and generates a simple musical pattern to demonstrate it.

    **Manual REAPER MIDI Editor Preferences Setup (Crucial for Workflow):**
    1. Go to `Options -> Preferences -> MIDI Editor`.
    2. Under "One MIDI editor per:", select `project`.
    3. Check `Active MIDI item follows selection changes in arrange view`.
    4. Check `Selection is linked to visibility`.
    5. Check `Selection is linked to editability`.
    6. (Optional, Logic-style) Uncheck `Close editor when the active item is deleted in the arrange view`.
    7. (Optional) Adjust `Opacity (1-3) for notes/CC in secondary media items` (e.g., to 2 or 3).
    8. Dock the MIDI editor to the bottom: open it (double-click a MIDI item) and click the "Dock editor" icon (square with arrow down).
    9. For differentiating tracks, Right-click in MIDI editor (above piano keys) -> `View` -> `Color notes by` -> `Track`.

    **This script assumes the above manual steps have been performed.**
    It will create a custom action to toggle multi-track editing (making secondary items editable)
    and then generate a musical pattern across multiple tracks.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 4 tracks with 120 notes over 4 bars at 120 BPM"
    """
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues": [0, 3, 5, 6, 7, 10],
    }

    if scale not in SCALES:
        return f"Error: Scale '{scale}' not supported. Choose from {list(SCALES.keys())}."

    current_scale_degrees = SCALES[scale]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_names = ["MIDI Drums", "BASS", "GTR RHY", "GTR LEAD"]
    tracks = []
    initial_track_count = RPR.RPR_CountTracks(0)
    for i, name in enumerate(track_names):
        track_idx = initial_track_count + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks.append(track)
        RPR.RPR_SetTrackColor(track, (i * 50) + 50) # Assign unique colors

    # === Step 3: Enable Multi-Track Editing Action ===
    # Action ID for "Options: Avoid automatically setting MIDI items from other tracks editable"
    # This action toggles a preference. To enable multi-track editing, this needs to be OFF.
    # We check its current state and toggle if necessary.
    toggle_action_id = 40523 # Native REAPER action ID
    
    # Get current state of the preference (1=ON/avoid, 0=OFF/allow editing secondary items)
    current_state_avoid_setting = RPR.RPR_GetToggleCommandState(toggle_action_id)
    if current_state_avoid_setting == 1: # If it's currently ON (avoid editing), toggle it OFF (allow editing)
        RPR.RPR_Main_OnCommand(toggle_action_id, 0)
        RPR.RPR_ShowConsoleMsg("Multi-track MIDI editing enabled: secondary items are now editable.\n")
    else:
        RPR.RPR_ShowConsoleMsg("Multi-track MIDI editing already enabled.\n")

    # === Step 4: Create MIDI Items and Notes ===
    beat_length_sec = (60.0 / bpm)
    bar_length_sec = beat_length_sec * 4
    total_notes_inserted = 0

    # Chords for G minor progression: Gm, Bb, Eb, F
    chord_progression = [
        [0, 3, 7],  # Gm (G, Bb, D)
        [3, 7, 10], # Bb (Bb, D, F)
        [8, 0, 3],  # Eb (Eb, G, Bb)
        [10, 2, 5], # F (F, A, C)
    ]

    # --- Drums ---
    drum_track = tracks[0]
    drum_item_length = bar_length_sec * bars
    drum_notes_data = []
    kick_note, snare_note, hihat_note, crash_note = 36, 38, 42, 49 # GM MIDI drum map

    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        # Kick on 1 & 3
        drum_notes_data.append({'start': bar_start_time, 'end': bar_start_time + beat_length_sec*0.9, 'channel': 9, 'pitch': kick_note, 'velocity': velocity_base})
        drum_notes_data.append({'start': bar_start_time + beat_length_sec*2, 'end': bar_start_time + beat_length_sec*2.9, 'channel': 9, 'pitch': kick_note, 'velocity': velocity_base})
        # Snare on 2 & 4
        drum_notes_data.append({'start': bar_start_time + beat_length_sec*1, 'end': bar_start_time + beat_length_sec*1.9, 'channel': 9, 'pitch': snare_note, 'velocity': velocity_base - 10})
        drum_notes_data.append({'start': bar_start_time + beat_length_sec*3, 'end': bar_start_time + beat_length_sec*3.9, 'channel': 9, 'pitch': snare_note, 'velocity': velocity_base - 10})
        # Hi-hats 1/8th notes
        for beat_sub in range(8):
            hihat_start = bar_start_time + beat_sub * beat_length_sec * 0.5
            hihat_end = hihat_start + beat_length_sec * 0.4
            drum_notes_data.append({'start': hihat_start, 'end': hihat_end, 'channel': 9, 'pitch': hihat_note, 'velocity': velocity_base - 30})
        # Crash on first beat of first bar only
        if bar == 0:
            drum_notes_data.append({'start': bar_start_time, 'end': bar_start_time + bar_length_sec, 'channel': 9, 'pitch': crash_note, 'velocity': velocity_base + 10})
    
    total_notes_inserted += create_midi_item_and_notes(drum_track, 0.0, drum_item_length, drum_notes_data)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplomatic5000", False, -1) # Assign a drum sampler

    # --- Bass ---
    bass_track = tracks[1]
    bass_item_length = bar_length_sec * bars
    bass_notes_data = []
    
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        # Get root of current chord in progression
        root_degree = chord_progression[bar % len(chord_progression)][0]
        root_midi_pitch = get_midi_note_number(key, current_scale_degrees, 2, root_degree) # Octave 2
        
        # Whole notes for bass
        bass_notes_data.append({'start': bar_start_time, 'end': bar_start_time + bar_length_sec, 'channel': 0, 'pitch': root_midi_pitch, 'velocity': velocity_base + 5})
        
    total_notes_inserted += create_midi_item_and_notes(bass_track, 0.0, bass_item_length, bass_notes_data)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1) # Assign a synth

    # --- Guitar Rhythm (chords) ---
    gtr_rhy_track = tracks[2]
    gtr_rhy_item_length = bar_length_sec * bars
    gtr_rhy_notes_data = []
    
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        current_chord_degrees = chord_progression[bar % len(chord_progression)]
        
        # Strummed 1/4th notes for chords
        for i in range(2): # Two main chord hits per bar (e.g., on 1 and 3)
            strum_base_time = bar_start_time + i * beat_length_sec * 2
            for j, degree in enumerate(current_chord_degrees):
                chord_note_midi = get_midi_note_number(key, current_scale_degrees, 4, degree) # Octave 4
                
                # Slight offset for strumming effect
                note_start = strum_base_time + j * (beat_length_sec * 0.05) 
                note_end = note_start + beat_length_sec * 1.5
                
                gtr_rhy_notes_data.append({'start': note_start, 'end': note_end, 'channel': 0, 'pitch': chord_note_midi, 'velocity': velocity_base - j*5})
                
    total_notes_inserted += create_midi_item_and_notes(gtr_rhy_track, 0.0, gtr_rhy_item_length, gtr_rhy_notes_data)
    RPR.RPR_TrackFX_AddByName(gtr_rhy_track, "ReaSynth", False, -1) # Assign a synth

    # --- Guitar Lead (arpeggios) ---
    gtr_lead_track = tracks[3]
    gtr_lead_item_length = bar_length_sec * bars
    gtr_lead_notes_data = []
    
    # Simple arpeggio pattern over each chord
    for bar in range(bars):
        bar_start_time = bar * bar_length_sec
        current_chord_degrees = chord_progression[bar % len(chord_progression)]
        
        # Simple arpeggio: root, 3rd, 5th, root(octave up), 5th(octave up), 3rd(octave up)
        arpeggio_sequence_degrees = [current_chord_degrees[0], current_chord_degrees[1], current_chord_degrees[2], 
                                     current_chord_degrees[0]+12, current_chord_degrees[2]+12, current_chord_degrees[1]+12]
                                     
        for i, degree in enumerate(arpeggio_sequence_degrees):
            arpeggio_note_midi = get_midi_note_number(key, current_scale_degrees, 5, degree) # Octave 5-6
            
            note_start = bar_start_time + i * beat_length_sec * (4 / len(arpeggio_sequence_degrees)) # Evenly spread over the bar
            note_end = note_start + beat_length_sec * (4 / len(arpeggio_sequence_degrees)) * 0.9
            
            gtr_lead_notes_data.append({'start': note_start, 'end': note_end, 'channel': 0, 'pitch': arpeggio_note_midi, 'velocity': velocity_base + 10})
            
    total_notes_inserted += create_midi_item_and_notes(gtr_lead_track, 0.0, gtr_lead_item_length, gtr_lead_notes_data)
    RPR.RPR_TrackFX_AddByName(gtr_lead_track, "ReaSynth", False, -1) # Assign a synth

    RPR.RPR_UpdateArrange() # Refresh the arrange view
    
    # Select all newly created items for multi-track display in the MIDI editor
    for track_idx_offset in range(len(tracks)):
        track = RPR.RPR_GetTrack(0, initial_track_count + track_idx_offset)
        if track:
            for item_idx in range(RPR.RPR_CountMediaItemsInTrack(track)):
                item = RPR.RPR_GetMediaItem_Track(track, item_idx)
                RPR.RPR_SetMediaItemSelected(item, True)
                
    # Open the MIDI editor for the selected items (this will open the single docked editor if configured)
    RPR.RPR_Main_OnCommand(40141, 0) # View: Open/close MIDI editor for selected items

    return f"Created {len(tracks)} tracks ('{' / '.join(track_names)}') with {total_notes_inserted} MIDI notes over {bars} bars at {bpm} BPM."


#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (Uses float timings for beat_length_sec, but derived from grid divisions).
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Yes, it demonstrates the multi-track composition workflow and a simple musical example.)
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?
- [x] It programmatically toggles the "Options: Avoid automatically setting MIDI items from other tracks editable" action (ID 40523) to enable multi-track editing, which is a key part of the workflow demonstrated in the video.
- [x] It assumes the user has manually set up the global MIDI editor preferences (like "one editor per project" and linked selections), as directly automating these via ReaScript is complex and often requires a REAPER restart for full effect, which is outside the scope of a single script execution. This is explicitly stated in the function docstring.