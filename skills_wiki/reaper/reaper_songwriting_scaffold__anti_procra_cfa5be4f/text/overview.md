### 1. High-level Design Pattern Extraction

> **Skill Name**: REAPER Songwriting Scaffold (Anti-Procrastination Layout)

* **Core Musical Mechanism**: The provided video is a *workflow and DAW customization tutorial* rather than a track-building walkthrough. The core philosophy advocated by the creator is to avoid "procrastination through over-customization" by having a setup that allows you to "just jump in" and capture creative flow. The defining musical pattern extracted here is the **Songwriting Layout** (showcased at 03:09), which consists of a ready-to-record, color-coded multi-track structure (Drums, Bass, Chords, Melody) prepopulated with foundational rhythm and harmony.

* **Why Use This Skill (Rationale)**: "Blank canvas syndrome" is a primary killer of momentum. By programmatically generating a pre-routed, color-coded folder with fundamental rhythmic anchors (kick/snare) and diatonic harmonic placeholders (chords/bass), the producer bypasses the mechanical setup phase. Musically, having a diatonic triad progression and a standard 4/4 drum grid established immediately provides the necessary musical context (groove and key center) to inspire an overriding melody or sound design experimentation.

* **Overall Applicability**: This is the ultimate "Day 1 / Idea Sketching" skill. It is perfectly suited for jump-starting a new REAPER project across any genre (pop, rock, electronic, lo-fi), providing an instant, organized sandbox for songwriting before diving into the granular customization the video warns against over-using.

* **Value Addition**: Compared to a blank MIDI clip or a completely empty project, this skill encodes DAW routing hierarchy (Folder track management), UI organization (track coloring), and basic music theory (diatonic chord generation and drum sequencing), instantly mirroring the professional songwriting layout shown in the tutorial.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4 (standard).
  - **BPM Range**: Parametric (defaults to 120 BPM).
  - **Grid Divisions**: The drum scaffold generates a fundamental 8th-note hi-hat grid, with kick on beats 1 and 3, and snare on beats 2 and 4.
  - **Harmonic Rhythm**: Chords and bassline change on the downbeat of every bar.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (supports major, minor, dorian, etc.).
  - **Chord Voicings**: Standard diatonic root-position triads. The pattern alternates between the I (or i) chord and the IV / V / VI chords depending on the scale, computing correct major/minor intervals mathematically based on the selected scale array.
  - **Bass**: Plays the root note of the active chord, 2 octaves below the triads.

* **Step C: Sound Design & FX**
  - Because this extracts the *workflow setup* shown in the tutorial, it relies on standard REAPER routing and color-coding rather than heavy third-party VSTs.
  - Tracks are natively colored mirroring the video's layout: Drums (Red), Bass (Blue), Chords (Purple), Melody (Green).

* **Step D: Mix & Automation (if applicable)**
  - Tracks are automatically grouped inside a parent "Songwriting Scaffold" folder track. This keeps the mixer clean and allows for global volume/bus processing on the entire sketch.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Project Setup & Workflow** | Track routing & UI Colors (`I_FOLDERDEPTH`, `I_CUSTOMCOLOR`) | Replicates the organizational Layout feature explicitly shown at 03:09. |
| **Drums / Foundational Groove** | MIDI note insertion | Provides an immediate rhythmic anchor (Kick/Snare/Hat) without relying on external/unavailable sample libraries. |
| **Chords & Bass** | Programmatic MIDI scaling | Translates the selected parameters into a diatonic scaffold, proving the template is immediately ready for creative work. |

> **Feasibility Assessment**: 100%. Because the source material is an educational workflow video rather than an audio-dependent track deconstruction, we can fully reproduce the *creative layout and generative template* directly using REAPER's native Python API without any reliance on missing audio files or external plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Songwriting_Scaffold",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a color-coded, ready-to-write Songwriting Layout (Drums, Bass, Chords, Melody)
    grouped in a parent folder, pre-populated with a basic foundational groove and diatonic harmony.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the scaffold.
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

    # Normalize parameters
    base_midi_note = NOTE_MAP.get(key.capitalize(), 0) + 48 # Base octave (C3)
    scale_arr = SCALES.get(scale.lower(), SCALES["minor"])
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # --- HELPER: Calculate pitch from scale degree ---
    def get_pitch(root, scale_array, degree):
        octave_shift = degree // len(scale_array)
        note_idx = degree % len(scale_array)
        return root + (octave_shift * 12) + scale_array[note_idx]

    # --- HELPER: Insert safe MIDI note ---
    def add_note(take, start_beat, end_beat, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # --- HELPER: Create color encoded track ---
    def create_track(name, color_val, folder_depth=0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "I_CUSTOMCOLOR", color_val | 0x1000000)
        if folder_depth != 0:
            RPR.RPR_SetMediaTrackInfo_Value(trk, "I_FOLDERDEPTH", folder_depth)
        return trk

    # Define Colors based on video (03:09) - format is R + (G*256) + (B*65536)
    COLOR_PARENT = 100 + (100 * 256) + (100 * 65536) # Grey
    COLOR_DRUMS  = 255 + (50 * 256) + (50 * 65536)   # Red
    COLOR_BASS   = 50 + (100 * 256) + (255 * 65536)  # Blue
    COLOR_CHORDS = 180 + (50 * 256) + (255 * 65536)  # Purple
    COLOR_MELODY = 50 + (255 * 256) + (50 * 65536)   # Green

    # === 1. Create Folder Parent ===
    parent_track = create_track(track_name, COLOR_PARENT, folder_depth=1)

    # === 2. Create Drums Track & Grooove ===
    drums_trk = create_track("DRUMS", COLOR_DRUMS, folder_depth=0)
    drum_item = RPR.RPR_CreateNewMIDIItemInProj(drums_trk, 0.0, total_length_sec, False)
    drum_take = RPR.RPR_GetActiveTake(drum_item)
    
    for b in range(bars):
        bar_beat = b * beats_per_bar
        # Kick (36) on 1 and 3
        add_note(drum_take, bar_beat + 0.0, bar_beat + 0.5, 36, velocity_base)
        add_note(drum_take, bar_beat + 2.0, bar_beat + 2.5, 36, velocity_base)
        # Snare (38) on 2 and 4
        add_note(drum_take, bar_beat + 1.0, bar_beat + 1.5, 38, velocity_base)
        add_note(drum_take, bar_beat + 3.0, bar_beat + 3.5, 38, velocity_base)
        # Hi-hat (42) on 8th notes
        for i in range(8):
            hat_beat = bar_beat + (i * 0.5)
            vel = velocity_base if i % 2 == 0 else int(velocity_base * 0.7)
            add_note(drum_take, hat_beat, hat_beat + 0.25, 42, vel)
    RPR.RPR_MIDI_Sort(drum_take)

    # === 3. Create Bass Track & Rhythm ===
    bass_trk = create_track("BASS", COLOR_BASS, folder_depth=0)
    bass_item = RPR.RPR_CreateNewMIDIItemInProj(bass_trk, 0.0, total_length_sec, False)
    bass_take = RPR.RPR_GetActiveTake(bass_item)

    # Chord progression mapping (Scale degrees: 0, 3, 4, 0)
    progression_degrees = [0, 3, 4, 0] 

    for b in range(bars):
        bar_beat = b * beats_per_bar
        deg = progression_degrees[b % len(progression_degrees)]
        # Bass note (2 octaves down)
        bass_pitch = get_pitch(base_midi_note - 24, scale_arr, deg)
        add_note(bass_take, bar_beat, bar_beat + 3.5, bass_pitch, velocity_base)
    RPR.RPR_MIDI_Sort(bass_take)

    # === 4. Create Chords Track ===
    chords_trk = create_track("CHORDS", COLOR_CHORDS, folder_depth=0)
    chords_item = RPR.RPR_CreateNewMIDIItemInProj(chords_trk, 0.0, total_length_sec, False)
    chords_take = RPR.RPR_GetActiveTake(chords_item)

    for b in range(bars):
        bar_beat = b * beats_per_bar
        deg = progression_degrees[b % len(progression_degrees)]
        
        # Diatonic Triads
        root_pitch = get_pitch(base_midi_note, scale_arr, deg)
        third_pitch = get_pitch(base_midi_note, scale_arr, deg + 2)
        fifth_pitch = get_pitch(base_midi_note, scale_arr, deg + 4)
        
        # Rhythmic pulsing (syncopated rhythm on chords)
        for chord_start in [0.0, 1.5, 2.5]:
            start_b = bar_beat + chord_start
            end_b = start_b + 1.0 if chord_start != 1.5 else start_b + 0.5
            
            add_note(chords_take, start_b, end_b, root_pitch, int(velocity_base * 0.9))
            add_note(chords_take, start_b, end_b, third_pitch, int(velocity_base * 0.8))
            add_note(chords_take, start_b, end_b, fifth_pitch, int(velocity_base * 0.8))
    RPR.RPR_MIDI_Sort(chords_take)

    # === 5. Create Melody Track (Closes Folder) ===
    # I_FOLDERDEPTH = -1 signals that this track is the last in the parent folder
    melody_trk = create_track("MELODY", COLOR_MELODY, folder_depth=-1)
    
    # Just an empty clip ready for recording the main idea
    RPR.RPR_CreateNewMIDIItemInProj(melody_trk, 0.0, total_length_sec, False)

    return f"Created Songwriting Scaffold '{track_name}' (Drums, Bass, Chords, Melody) over {bars} bars at {bpm} BPM in {key} {scale}."
```