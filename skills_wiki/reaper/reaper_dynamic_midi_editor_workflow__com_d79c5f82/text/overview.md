### 1. High-level Design Pattern Extraction

*   **Skill Name**: REAPER Dynamic MIDI Editor Workflow (Compositional Sketch)

*   **Core Musical Mechanism**: This skill focuses on a highly efficient MIDI composition workflow within REAPER, leveraging a single, docked MIDI editor that dynamically displays selected MIDI items across multiple tracks. It allows for quick referencing of "ghost notes" from unselected items and enables multi-track editing (when a specific option is toggled). The musical demonstration uses this workflow to rapidly layer a guitar chord progression, bassline, drum beat, and lead melody.

*   **Why Use This Skill (Rationale)**: This workflow significantly enhances the speed and fluidity of MIDI composition, especially when working with multiple interconnected instrumental parts.
    *   **Visual Context**: By displaying all selected MIDI items (active and secondary/ghost notes) in a single editor, it provides immediate visual feedback on the melodic and harmonic relationships between different instruments, aiding in arrangement decisions and avoiding clashes.
    *   **Rapid Iteration**: The ability to quickly switch the active editable item with a single click (or shortcut) minimizes interruptions, keeping the composer in a creative flow state.
    *   **Inter-part Editing**: Multi-track editing within the same MIDI editor is invaluable for crafting counter-melodies, basslines that respond to chords, or drum patterns that lock in with rhythmic elements, ensuring tight integration between parts.
    *   **Ergonomics**: Docking the editor and saving screen layouts (via REAPER's Screensets) creates a consistent, organized workspace, reducing cognitive load from managing multiple floating windows.

*   **Overall Applicability**: This workflow is highly versatile and applicable to any genre involving multi-track MIDI composition, from orchestral scoring and game audio to electronic music, rock, pop, and hip-hop. It's particularly useful for:
    *   Composers arranging multiple instrumental sections (strings, brass, woodwinds).
    *   Producers building complex rhythmic interplay between drums, bass, and synth arpeggios.
    *   Songwriters sketching out full instrumental arrangements efficiently.

*   **Value Addition**: Compared to a blank MIDI clip, this skill encodes a *powerful and efficient compositional workflow*. While the code primarily generates a basic musical example (chords, bass, drums, lead), the true value extracted is the *methodology* demonstrated in the video for interacting with MIDI data in a synchronized, contextual, and editable environment. The generated music serves as a concrete application of this workflow.

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: 4/4
    *   **BPM Range**: The video demonstrates at 120 BPM. The skill is parametric for BPM.
    *   **Rhythmic Grid**: Primarily 1/4 and 1/8 notes, with some 1/16th notes for drums and lead melody.
    *   **Note Duration**: Varying durations from staccato (drums) to sustained (chords/bass).

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: The demonstration uses a G Natural Minor scale. The skill is parametric for key and scale.
    *   **Chord Progression (for demo)**: Gm - Cm - Dm - EbM (over 4 bars, repeating).
        *   Gm (Root, minor 3rd, perfect 5th)
        *   Cm (Root, minor 3rd, perfect 5th)
        *   Dm (Root, minor 3rd, perfect 5th)
        *   EbM (Root, major 3rd, perfect 5th)
    *   **Bassline**: Follows the root notes of the chord progression.
    *   **Lead Melody**: Arpeggiated and melodic patterns derived from the underlying chords/scale.

*   **Step C: Sound Design & FX**
    *   **Instruments**: The video uses third-party VSTs (Kontakt, Parallax, Odin2, Sublab2). For reproducibility with stock REAPER, the code will use `ReaSynth` for all melodic/harmonic parts and `ReaSamplOmatic5000` loaded with a generic drum kit for drums.
    *   **FX Chain**:
        *   Each instrument track (GTR RHY, BASS, GTR LEAD) has a `ReaSynth` instance.
        *   The "DRUMS" track has a `ReaSamplOmatic5000` instance.
        *   No specific additional FX (EQ, Compression, Reverb, Delay) are demonstrated or explicitly mentioned for the *sound design itself* beyond the instruments. The code will add basic ReaEQ and ReaComp for a typical setup.

*   **Step D: Mix & Automation (if applicable)**
    *   **Volume/Panning**: Default levels and panning.
    *   **Automation**: No explicit automation is demonstrated in the musical section.
    *   **MIDI Editor Workflow Settings (User Preferences/Setup - Not in generated code)**:
        *   REAPER Preferences > MIDI Editor:
            *   "One MIDI editor per: **project**"
            *   "When using one MIDI editor per project:"
                *   "**Active MIDI item follows selection changes in arrange view**"
                *   "**Selection is linked to visibility**"
                *   "**Selection is linked to editability**"
                *   "Close editor when the active item is deleted in the arrange view: **unchecked**"
                *   "Opacity (1-3) for notes/CC in secondary media items: **2 or 3**"
        *   **MIDI Editor Docking**: Use the "Dock editor" toolbar button (top-right of MIDI Editor) to dock it to the bottom of the main REAPER window.
        *   **Screensets**: Use REAPER's "Screensets/Layouts" window (`View > Screensets/Layouts`) to save and load custom window arrangements (e.g., one with the docked MIDI editor open).
        *   **Multi-track Editing Toggle**: A custom action (e.g., bound to a toolbar button as "SINGLE TRACK EDIT") to toggle "Options: Avoid automatically setting MIDI items from other tracks editable". This action controls whether ghost notes are editable.
        *   **MIDI Editor View Options**: Right-click piano keys in MIDI editor > View > Color notes by > **Track**.
        *   **Quick Grid/Velocity Adjustment**: The video mentions using mousewheel scripts for grid size (`Script: mpl_Adjust MIDI Editor grid (mousewheel).lua`) and velocity (`Edit: Adjust value for events (mousewheel/MIDI controller only)`). These are separate ReaScripts that enhance workflow but are not part of the musical pattern generation itself.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :-------------------- | :-------------------- |
| Track Creation | `RPR_InsertTrackAtIndex()` | To add new tracks for each instrument. |
| Instrument Loading | `RPR_TrackFX_AddByName()` | To add `ReaSynth` for melodic/harmonic parts and `ReaSamplOmatic5000` for drums. |
| MIDI Item Creation | `RPR_AddMediaItemToTrack()`, `RPR_SetMediaItemInfo_Value()`, `RPR_AddTakeToMediaItem()` | To create MIDI containers on tracks. |
| MIDI Note Insertion | `RPR_MIDI_InsertNote()` within `RPR_MIDI_SetItemExt()` | For precise placement, duration, and velocity of notes for chords, bass, drums, and lead. |
| Global Tempo | `RPR_RPR_SetCurrentBPM()` | To ensure the project tempo matches the specified BPM. |
| Track Naming | `RPR_GetSetMediaTrackInfo_String()` | To clearly label instrument tracks. |
| Basic Mixing FX | `RPR_TrackFX_AddByName()` | To provide a basic starting point for EQ and Compression, as typically done in production. |
| Drum Samples | Dummy `ReaSamplOmatic5000` slots | As actual drum samples are external, this sets up the instrument but requires manual sample loading for exact sound. |

**Feasibility Assessment**: 85%. The code successfully creates tracks, loads stock REAPER instruments, and inserts MIDI notes for a representative guitar chord progression, bassline, drum beat, and lead melody. It sets up basic mixing effects. The remaining 15% largely accounts for the specific timbre of third-party VSTs shown in the tutorial (which cannot be replicated with stock ReaSynth) and the specific visual/GUI workflow settings (like docking, custom screensets, and custom toolbar actions) which are user setup rather than direct musical output from a generation script. The fundamental musical relationships and dynamic MIDI editing capabilities are reflected.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "G",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a multi-instrument MIDI composition demonstrating the dynamic REAPER MIDI editor workflow.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., individual track velocities).

    Returns:
        Status string, e.g., "Created 'Drums' with 32 notes over 4 bars at 120 BPM"
    """
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
    # Drum map for ReaSamplOmatic5000 (standard GM map for drums)
    DRUM_MAP = {
        "kick": 36, "snare": 38, "hi_hat_closed": 42, "hi_hat_open": 46, "crash": 49
    }

    # Ensure scale exists
    if scale not in SCALES:
        return f"Error: Scale '{scale}' not found."

    # Get root MIDI value
    root_midi = NOTE_MAP.get(key, 0) + 48 # Base C4 for melodies/chords

    # Get scale degrees
    current_scale = SCALES[scale]

    def get_midi_note(degree, octave_offset=0):
        if 0 <= degree < len(current_scale):
            return root_midi + current_scale[degree] + (octave_offset * 12)
        return root_midi + (degree * 1) + (octave_offset * 12) # Fallback if degree out of bounds

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Tracks ===
    track_names = ["DRUMS", "BASS", "GTR RHY", "GTR LEAD"]
    tracks = {}
    for name in track_names:
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        tracks[name] = track

        # Add basic FX (ReaEQ, ReaComp)
        RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
        RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)

    # === Step 3: Create MIDI Items and insert notes ===
    beats_per_bar = 4
    quarter_note_len = 60.0 / bpm
    item_length_beats = beats_per_bar * bars
    item_length_sec = quarter_note_len * item_length_beats

    notes_inserted_count = 0

    # --- DRUMS ---
    drum_track = tracks["DRUMS"]
    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", item_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    RPR.RPR_MIDI_SetItemExt(drum_take, "", 0, 0, 0, 0) # Clear existing MIDI

    # Add ReaSamplOmatic5000 and load dummy samples (user to replace)
    RPR.RPR_TrackFX_AddByName(drum_track, "ReaSamplOmatic5000", False, -1)
    # Configure ReaSamplOmatic5000 for multiple samples if needed, but for now, just for kicks/snares
    # Note: Loading actual samples via script is complex and depends on file paths.
    # User will need to manually load desired drum samples into ReaSamplOmatic5000.

    midi_events = RPR.MIDI_GetAllEvts(drum_take, "") # For older versions of Reaper, need to pass True to enable editing
    RPR.MIDI_SetItemExt(drum_take, midi_events, len(midi_events), 0, 0, 0)
    
    # Drum pattern (Kick on 1 & 3, Snare on 2 & 4, Hi-hat 1/8ths)
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        # Kick
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat, bar_start_beat + quarter_note_len, 0, DRUM_MAP["kick"], kwargs.get("kick_velocity", velocity_base + 10), False)
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + 2*quarter_note_len, bar_start_beat + 3*quarter_note_len, 0, DRUM_MAP["kick"], kwargs.get("kick_velocity", velocity_base + 10), False)
        # Snare
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + quarter_note_len, bar_start_beat + 2*quarter_note_len, 0, DRUM_MAP["snare"], kwargs.get("snare_velocity", velocity_base), False)
        RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + 3*quarter_note_len, bar_start_beat + 4*quarter_note_len, 0, DRUM_MAP["snare"], kwargs.get("snare_velocity", velocity_base), False)
        # Hi-hat (1/8th notes)
        for i in range(8):
            RPR.MIDI_InsertNote(drum_take, False, False, bar_start_beat + i * quarter_note_len / 2, bar_start_beat + (i+0.5) * quarter_note_len / 2, 0, DRUM_MAP["hi_hat_closed"], kwargs.get("hi_hat_velocity", velocity_base - 20), False)
        notes_inserted_count += 12 # 2 kick, 2 snare, 8 hi-hat per bar

    RPR.MIDI_Sort(drum_take)
    RPR.MIDI_CommitItem(drum_take)

    # --- GUITAR RHYTHM (Chords) ---
    gtr_rhy_track = tracks["GTR RHY"]
    gtr_rhy_item = RPR.RPR_AddMediaItemToTrack(gtr_rhy_track)
    RPR.RPR_SetMediaItemInfo_Value(gtr_rhy_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(gtr_rhy_item, "D_LENGTH", item_length_sec)
    gtr_rhy_take = RPR.RPR_AddTakeToMediaItem(gtr_rhy_item)
    RPR.RPR_MIDI_SetItemExt(gtr_rhy_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(gtr_rhy_track, "ReaSynth", False, -1)
    
    # Chord progression: Gm, Cm, Dm, EbM
    chords_progression = [
        [get_midi_note(0, 0), get_midi_note(2, 0), get_midi_note(4, 0)], # Gm (0, 2, 4 in G minor)
        [get_midi_note(3, 0), get_midi_note(5, 0), get_midi_note(7, 0)], # Cm (root of C, which is 3rd degree of G minor, + minor 3rd (Eb=5), perfect 5th (G=7))
        [get_midi_note(4, 0), get_midi_note(6, 0), get_midi_note(8, 0)], # Dm (root of D, which is 4th degree of G minor, + minor 3rd (F=6), perfect 5th (A=8))
        [get_midi_note(5, 0), get_midi_note(7, 0), get_midi_note(9, 0)], # EbM (root of Eb, which is 5th degree of G minor, + major 3rd (G=7), perfect 5th (Bb=9))
    ]
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        current_chord_notes = chords_progression[bar % len(chords_progression)]
        for note_midi in current_chord_notes:
            RPR.MIDI_InsertNote(gtr_rhy_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, 0, note_midi, kwargs.get("chord_velocity", velocity_base - 10), False)
            notes_inserted_count += 1
    RPR.MIDI_Sort(gtr_rhy_take)
    RPR.MIDI_CommitItem(gtr_rhy_take)

    # --- BASS ---
    bass_track = tracks["BASS"]
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", item_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)
    RPR.RPR_MIDI_SetItemExt(bass_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1) # Use ReaSynth for bass
    
    # Bass follows root notes of chords, one octave lower
    bass_roots = [get_midi_note(0, -1), get_midi_note(3, -1), get_midi_note(4, -1), get_midi_note(5, -1)]
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        root_midi = bass_roots[bar % len(bass_roots)]
        RPR.MIDI_InsertNote(bass_take, False, False, bar_start_beat, bar_start_beat + beats_per_bar, 0, root_midi, kwargs.get("bass_velocity", velocity_base + 5), False)
        notes_inserted_count += 1
    RPR.MIDI_Sort(bass_take)
    RPR.MIDI_CommitItem(bass_take)

    # --- GUITAR LEAD ---
    gtr_lead_track = tracks["GTR LEAD"]
    gtr_lead_item = RPR.RPR_AddMediaItemToTrack(gtr_lead_track)
    RPR.RPR_SetMediaItemInfo_Value(gtr_lead_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(gtr_lead_item, "D_LENGTH", item_length_sec)
    gtr_lead_take = RPR.RPR_AddTakeToMediaItem(gtr_lead_item)
    RPR.RPR_MIDI_SetItemExt(gtr_lead_take, "", 0, 0, 0, 0)
    RPR.RPR_TrackFX_AddByName(gtr_lead_track, "ReaSynth", False, -1) # Use ReaSynth for lead

    # Simple arpeggiated lead line (G minor pentatonic over Gm, Cm, Dm, EbM)
    lead_pattern_beats = quarter_note_len / 2 # 1/8th notes
    lead_notes = [
        (get_midi_note(0, 1), 0), (get_midi_note(3, 1), 1), (get_midi_note(5, 1), 2), (get_midi_note(7, 1), 3), # Gm arpeggio
        (get_midi_note(3, 1), 4), (get_midi_note(5, 1), 5), (get_midi_note(7, 1), 6), (get_midi_note(8, 1), 7), # Cm arpeggio
        (get_midi_note(4, 1), 8), (get_midi_note(6, 1), 9), (get_midi_note(8, 1), 10), (get_midi_note(10, 1), 11), # Dm arpeggio
        (get_midi_note(5, 1), 12), (get_midi_note(7, 1), 13), (get_midi_note(9, 1), 14), (get_midi_note(11, 1), 15), # EbM arpeggio
    ]
    
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        for note_midi_offset, beat_offset in lead_notes:
            RPR.MIDI_InsertNote(gtr_lead_take, False, False, bar_start_beat + beat_offset * lead_pattern_beats, bar_start_beat + (beat_offset + 0.5) * lead_pattern_beats, 0, note_midi_offset, kwargs.get("lead_velocity", velocity_base + 20), False)
            notes_inserted_count += 1
    RPR.MIDI_Sort(gtr_lead_take)
    RPR.MIDI_CommitItem(gtr_lead_take)

    RPR.RPR_UpdateArrange()

    return f"Created '{', '.join(track_names)}' tracks with {notes_inserted_count} notes over {bars} bars at {bpm} BPM in {key} {scale}."

```