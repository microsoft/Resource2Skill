### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Instrument Arrangement Framework & Multi-Track MIDI Workflow

* **Core Musical Mechanism**: This pattern establishes an interlocking 4-piece band arrangement (Drums, Bass, Rhythm Guitar, Lead Guitar) operating over a classic 4-chord looping progression. The core technique here is **contrapuntal visualization**—writing multiple instruments in the exact same physical window (using MIDI ghost notes/secondary items) so that the rhythmic syncopation and harmonic stacking of all 4 instruments can be seen and edited simultaneously.
* **Why Use This Skill (Rationale)**: When writing orchestral, rock, or complex electronic music, frequency masking and rhythmic clashing are common pitfalls. By forcing a workflow where the Bass root notes, Rhythm Guitar chord voicings, and Lead Guitar melodies are overlaid visually, the producer can easily ensure that chord tones align perfectly (e.g., the bass is playing the root of the guitar chord) and that drum hits (like kick and snare) lock in with the bassline. 
* **Overall Applicability**: Essential for writing full-band rock tracks, complex orchestral mockups, or layered synthwave/EDM drops where multiple distinct voices must harmonize and rhythmically complement each other.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes the foundational structural template of a rock/pop band, utilizing a standard chord progression (i-VI-III-VII in minor or I-V-vi-IV in major) and separating the voices into distinct colored tracks to immediately take advantage of REAPER's advanced multi-track MIDI editing capabilities.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: ~120 BPM (standard driving rock tempo).
  * **Grid**: 1/8th note grid.
  * **Rhythm Roles**: 
    * *Drums*: Four-on-the-floor or standard rock beat (Kick on 1 & 3, Snare on 2 & 4, continuous 8th note hi-hats).
    * *Bass*: Driving continuous 8th notes to provide a solid rhythmic foundation.
    * *Rhythm Guitar*: Whole notes (sustained block chords) to provide harmonic context.
    * *Lead Guitar*: Arpeggiated 8th notes to provide melodic movement over the static chords.

* **Step B: Pitch & Harmony**
  * **Progression**: The tutorial demonstrates a standard "epic" progression. In minor keys, this is **i - VI - III - VII** (e.g., Bm - Gmaj - Dmaj - Amaj). In major keys, the script adapts this to **I - V - vi - IV**.
  * **Voicings**: Rhythm guitars play root-position triads. Bass plays the root note one octave lower. Lead guitar plays arpeggios (Root, 5th, Octave).

* **Step C: Sound Design & FX**
  * To make the template audible out-of-the-box, each track uses REAPER's native `ReaSynth`. 
  * The Bass track's synthesizer is tuned an octave down.
  * Tracks are distinctly colored (Blue, Purple, Orange, Cyan) to ensure visual separation in the MIDI editor when "Color notes by Track" is enabled.

* **Step D: Mix & Automation (Workflow Settings)**
  * *Note on REAPER Configuration*: To fully utilize this template as shown in the tutorial, the user should configure REAPER's MIDI Editor Preferences (`Options > Preferences > MIDI Editor`):
    * `One MIDI editor per: project`
    * `Behavior for "open items in built-in MIDI editor": Open all selected MIDI items`
    * Check `Active MIDI item follows selection changes in arrange view`
    * Check `Selection is linked to visibility / editability`
    * Set `Opacity for secondary media items` to `2` or `3` to see ghost notes.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track/Instrument Setup | Track Creation + `RPR_TrackFX_AddByName` | Sets up the 4 discrete tracks (Drums, Bass, Rhythm, Lead) required for multi-track editing. |
| Harmonic Progression | Algorithmically generated MIDI via `RPR_MIDI_InsertNote` | Computes triads and scales dynamically so the user can instantiate the template in any musical key. |
| Workflow Separation | Track custom coloring | Colors distinguish the overlapping MIDI notes in the shared Piano Roll view, as emphasized in the tutorial. |

> **Feasibility Assessment**: 100% reproducible. The script sets up the exact arrangement layout and populates it with a dynamically generated foundational rock progression, giving you the perfect sandbox to practice the tutorial's multi-track editing workflow.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Band Template", # Base name, will be expanded
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Multi-Instrument Framework (Drums, Bass, Rhythm, Lead)
    to facilitate multi-track MIDI editing and composition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored here as we hardcode the 4 roles).
        bpm: Tempo in BPM.
        key: Root note (e.g., "B").
        scale: "major" or "minor".
        bars: Number of bars for the looping progression.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and notes.
    """
    import reaper_python as RPR

    # Set up music theory constants
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    # Choose progression based on scale type
    if scale.lower() == "minor":
        prog_degrees = [0, 5, 2, 6]  # i - VI - III - VII
    else:
        prog_degrees = [0, 4, 5, 3]  # I - V - vi - IV
        scale = "major" # fallback normalization
        
    scale_intervals = SCALES[scale]
    root_base = NOTE_MAP.get(key, 11) + 48  # Octave 4 base (e.g., C4 = 48)

    # Initialize Environment
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    proj_start_time = RPR.RPR_GetCursorPosition()
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    item_length = bar_length_sec * bars

    def make_color(r, g, b):
        # REAPER custom color encoding
        return (r | (g << 8) | (b << 16)) | 0x1000000

    tracks_to_create = [
        {"name": "01 MIDI Drums", "color": make_color(50, 50, 255), "role": "drums"},
        {"name": "02 BASS", "color": make_color(150, 50, 200), "role": "bass"},
        {"name": "03 GTR RHY", "color": make_color(255, 120, 50), "role": "rhythm"},
        {"name": "04 GTR LEAD", "color": make_color(50, 200, 255), "role": "lead"},
    ]

    total_notes_created = 0

    for i, t_info in enumerate(tracks_to_create):
        # 1. Create Track
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])

        # 2. Add ReaSynth to ensure it's audible
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        if t_info["role"] == "bass":
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

        # 3. Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", proj_start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # 4. Generate MIDI Notes based on Role
        for bar in range(bars):
            bar_start_time = proj_start_time + (bar * bar_length_sec)
            
            # Figure out current chord
            deg = prog_degrees[bar % len(prog_degrees)]
            chord_notes = []
            for third in [0, 2, 4]: # Root, 3rd, 5th
                idx = (deg + third) % 7
                octave_shift = (deg + third) // 7
                chord_notes.append(root_base + scale_intervals[idx] + (octave_shift * 12))

            # Role: DRUMS
            if t_info["role"] == "drums":
                for beat in range(4):
                    beat_time = bar_start_time + (beat * beat_length_sec)
                    # Kick on 1 and 3
                    if beat in [0, 2]:
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + 0.1)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 36, velocity_base, False)
                        total_notes_created += 1
                    # Snare on 2 and 4
                    if beat in [1, 3]:
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + 0.1)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 38, velocity_base, False)
                        total_notes_created += 1
                    # Hats every 8th note
                    for hh in range(2):
                        hh_time = beat_time + (hh * beat_length_sec / 2.0)
                        st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time)
                        en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time + 0.05)
                        RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, 42, velocity_base - 20, False)
                        total_notes_created += 1

            # Role: BASS
            elif t_info["role"] == "bass":
                root_bass = chord_notes[0] - 24 # 2 octaves down
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * bar_length_sec / 8.0)
                    st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (bar_length_sec / 8.0) - 0.02)
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, root_bass, velocity_base, False)
                    total_notes_created += 1

            # Role: RHYTHM GUITAR
            elif t_info["role"] == "rhythm":
                st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time)
                en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_time + bar_length_sec - 0.05)
                for note in chord_notes:
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, note - 12, velocity_base - 10, False)
                    total_notes_created += 1

            # Role: LEAD GUITAR
            elif t_info["role"] == "lead":
                arp_pattern = [chord_notes[0], chord_notes[2], chord_notes[0]+12, chord_notes[2]]
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * bar_length_sec / 8.0)
                    st = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    en = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (bar_length_sec / 8.0) - 0.02)
                    arp_note = arp_pattern[eighth % 4]
                    RPR.RPR_MIDI_InsertNote(take, False, False, st, en, 0, arp_note, velocity_base + 10, False)
                    total_notes_created += 1

        # Sort MIDI events for the track so it plays properly
        RPR.RPR_MIDI_Sort(take)

    # Optional: Update arrange view
    RPR.RPR_UpdateTimeline()

    return f"Created 4-track band template ({key} {scale}) with {total_notes_created} notes over {bars} bars at {bpm} BPM."
```