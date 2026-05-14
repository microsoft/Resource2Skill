### 1. High-level Design Pattern Extraction

> **Skill Name**: Interlocking Multi-Track Arrangement Template (Drums, Bass, Chords, Arp)

* **Core Musical Mechanism**: This pattern represents the core of a harmonically and rhythmically synchronized multi-instrument arrangement. It relies on a "vertical" composition approach where the Bass locks rhythmically with the Drum Kick and roots itself on the fundamental of the Chords, while a Lead synth plays an arpeggiated contour built entirely from the sustained chord tones. 
* **Why Use This Skill (Rationale)**: The tutorial explicitly focuses on the workflow of editing multiple MIDI instruments in a single piano roll. This arrangement pattern acts as the perfect structural foundation for that workflow. By looking at all tracks simultaneously (using ghost notes/opacity), you prevent frequency/harmonic masking, ensure the groove pocket (Kick + Bass) is tight, and maintain strict harmonic boundaries (Chords + Arp). 
* **Overall Applicability**: This 4-part structure is the universal backbone for rock, metal, synthwave, and orchestral music (the genres highlighted by the creator). It serves as an instant starting point for a full song section (Intro, Chorus, or Drop).
* **Value Addition**: Compared to a blank MIDI clip, this skill instantly builds a complete, color-coded, 4-track band. It encodes the music theory needed to generate a valid i-VI-III-VII chord progression, extracts the correct root notes for the bassline, arpeggiates the chord tones for the lead, and underpins it with a standard 8th-note rock drum groove.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, highly adaptable (defaulting to 120 BPM, though the tutorial sits in a driving rock/metal tempo).
  - **Drums**: Standard rock beat. Kicks on 1, 2-AND, 3. Snare on 2 and 4. Hi-hats driving on straight 8th notes. 
  - **Bass**: Driving 8th notes strictly following the root notes.
  - **Rhythm**: Sustained whole-note block chords changing every bar.
  - **Lead**: 8th-note continuous arpeggio cycling through the chord triad.

* **Step B: Pitch & Harmony**
  - **Progression**: i - VI - III - VII (represented as scale degrees 1, 6, 3, 7 in natural minor).
  - **Voicings**: Basic closed-position triads for the rhythm track. The bass plays two octaves below the chord roots. The lead plays one octave above the chords.
  - **Key/Scale**: Parameterized, but defaults to a minor scale (e.g., B minor as seen in the tutorial).

* **Step C: Sound Design & FX**
  - The script sets up 4 distinct tracks (`Drums`, `Bass`, `Rhythm`, `Lead`).
  - **Workflow Optimization**: Tracks are assigned distinct custom colors (Red, Purple, Blue, Orange) specifically to utilize the "Color notes by Track" feature demonstrated in the tutorial.
  - **Instruments**: ReaSynth is added to melodic tracks as a placeholder sound generator so the arrangement can be auditioned immediately.

* **Step D: Mix & Automation (if applicable)**
  - Basic volume staging is achieved via MIDI velocity (Accented downbeats on drums, slightly softer rhythm chords to leave room for the lead).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Setup & Coloring | `RPR_InsertTrackAtIndex`, `RPR_SetMediaTrackInfo_Value` | Creates the multi-track environment and sets track colors to match the MIDI Editor workflow shown in the video. |
| Harmonic Generation | Scale-degree math & `RPR_MIDI_InsertNote` | Computes exactly which pitches belong to the progression without hardcoding arbitrary MIDI notes. |
| Rhythmic Synchronization | Time-to-PPQ conversion | Ensures the 8th-note bass perfectly aligns with the Kick drums across the generated arrangement. |

> **Feasibility Assessment**: 100% reproduction of the musical arrangement concept. While the specific third-party VSTs (like Kontakt libraries) are replaced with stock ReaSynth for universal compatibility, the MIDI logic, timing, track routing, and multi-track coloring exactly mirror the tutorial's project state.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrack Workflow",
    track_name: str = "Arrangement", # Base name, will create 4 specific tracks
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Interlocking Multi-Track Arrangement in the current REAPER project.
    Generates color-coded Drums, Bass, Rhythm, and Lead tracks to practice
    multi-track MIDI editing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name (ignored here, creates specific instruments).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type.
        bars: Number of bars to generate (cycles through 4-chord loop).
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
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key, 11) + 48 # Default to B2 (MIDI 59)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper function to get scale pitches across octaves
    def get_scale_pitch(base_note, intervals, degree):
        octave_shift = degree // len(intervals)
        scale_idx = degree % len(intervals)
        return base_note + intervals[scale_idx] + (octave_shift * 12)

    # Helper function to insert a note
    def add_note(take, start_beat, end_beat, pitch, velocity):
        # Convert beats to time (1 beat = 1 quarter note)
        beat_len = 60.0 / bpm
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), True)

    beats_per_bar = 4
    item_length_sec = (60.0 / bpm) * beats_per_bar * bars

    track_setup = [
        {"name": "Drums",  "color": 255 + (0 * 256) + (0 * 65536) | 16777216,   "synth": None},       # Red
        {"name": "Bass",   "color": 128 + (0 * 256) + (128 * 65536) | 16777216, "synth": "ReaSynth"}, # Purple
        {"name": "Rhythm", "color": 0 + (128 * 256) + (255 * 65536) | 16777216, "synth": "ReaSynth"}, # Blue
        {"name": "Lead",   "color": 255 + (165 * 256) + (0 * 65536) | 16777216, "synth": "ReaSynth"}  # Orange
    ]

    takes = {}

    # === Step 2 & 3: Create Tracks & MIDI Items ===
    for i, setup in enumerate(track_setup):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", setup["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", setup["color"])
        
        if setup["synth"]:
            RPR.RPR_TrackFX_AddByName(track, setup["synth"], False, -1)

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes[setup["name"]] = take

    # === Step 4: Populate MIDI Notes ===
    # Progression: i - VI - III - VII (0, 5, 2, 6 in scale degrees)
    progression = [0, 5, 2, 6] 

    for bar in range(bars):
        deg = progression[bar % len(progression)]
        bar_beat_start = bar * 4

        # 1. DRUMS (Kick: 36, Snare: 38, Hat: 42)
        for beat in range(8): # 8th notes
            beat_pos = bar_beat_start + (beat * 0.5)
            
            # Hi-hat on every 8th note
            add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 42, velocity_base - 10)
            
            # Snare on beats 2 and 4 (indices 2 and 6 in 8th-note array)
            if beat == 2 or beat == 6:
                add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 38, velocity_base + 10)
                
            # Kick on 1, 2-AND, 3 (indices 0, 3, 4)
            if beat == 0 or beat == 3 or beat == 4:
                add_note(takes["Drums"], beat_pos, beat_pos + 0.25, 36, velocity_base + 15)

        # 2. BASS (8th notes, following the root, 2 octaves down)
        bass_pitch = get_scale_pitch(root_midi - 24, scale_intervals, deg)
        for beat in range(8):
            beat_pos = bar_beat_start + (beat * 0.5)
            add_note(takes["Bass"], beat_pos, beat_pos + 0.45, bass_pitch, velocity_base)

        # 3. RHYTHM (Whole note block chords)
        chord_pitches = [
            get_scale_pitch(root_midi, scale_intervals, deg),     # Root
            get_scale_pitch(root_midi, scale_intervals, deg + 2), # Third
            get_scale_pitch(root_midi, scale_intervals, deg + 4)  # Fifth
        ]
        for p in chord_pitches:
            add_note(takes["Rhythm"], bar_beat_start, bar_beat_start + 4.0, p, velocity_base - 15)

        # 4. LEAD (8th note arpeggio using the chord tones, 1 octave up)
        for beat in range(8):
            beat_pos = bar_beat_start + (beat * 0.5)
            # Cycle through the triad: Root -> Third -> Fifth -> Root...
            arp_pitch = chord_pitches[beat % 3] + 12 
            add_note(takes["Lead"], beat_pos, beat_pos + 0.4, arp_pitch, velocity_base + 5)

    # Sort MIDI events for all takes
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created multi-track arrangement (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM in {key} {scale}."
```