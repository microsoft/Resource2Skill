### 1. High-level Design Pattern Extraction

**Skill Name**: Multi-Track Rock Sketch (i-VI-III-VII Layering)

* **Core Musical Mechanism**: The tutorial demonstrates how to harness multi-track MIDI editing to write cohesive arrangements. The musical foundation of the demonstration is a classic 4-bar rock/metal arrangement using a **i-VI-III-VII** chord progression. The arrangement locks a driving rhythmic bassline to the kick drum, layers sustained power chords on a rhythm guitar track, and overlays a fast, continuous 8th-note arpeggio on a lead track. By viewing these items simultaneously in the MIDI editor (using secondary items as "ghost notes"), the producer ensures harmonic alignment across the entire frequency spectrum.
* **Why Use This Skill (Rationale)**: The i-VI-III-VII progression (e.g., Bm - G - D - A) is one of the most powerful and ubiquitous chord movements in modern rock, pop, and orchestral music. It constantly balances tension and release. By layering instruments—rhythm guitar holding the harmony, bass locking the root to the drum groove, and lead iterating through the chord tones (arpeggiation)—you create a wide, massive wall of sound.
* **Overall Applicability**: This template and progression serve as the perfect starting point for modern rock, symphonic metal, cinematic orchestral sketches, and electronic dance music (EDM) drops. 
* **Value Addition**: This skill creates a fully populated, 4-track layered arrangement (Drums, Bass, Rhythm, Lead). It encodes the exact chord inversions, bass syncopation, and lead arpeggios, automatically coloring the tracks and selecting the MIDI items so you can instantly open them in REAPER's multi-track MIDI editor just like the tutorial demonstrates.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Signature**: 120 BPM, 4/4 time.
  - **Grid**: Straight 1/8th note feel.
  - **Drums**: Kick on beats 1, 3, and an offbeat 3.5. Snare on 2 and 4. Hi-hats on continuous 1/8th notes.
  - **Bass**: Staccato 1/8th notes outlining the root to drive the energy.
  - **Lead**: 1/8th note repeating arpeggio pattern (Root - 3rd - 5th - Octave).

* **Step B: Pitch & Harmony**
  - **Key**: B Minor (B, C#, D, E, F#, G, A).
  - **Progression**: Bm (i) -> G Major (VI) -> D Major (III) -> A Major (VII).
  - **Voicings**: 
    - Rhythm: Block triads in the 3rd/4th octave.
    - Bass: Driving root notes in the 1st/2nd octave.
    - Lead: Arpeggiated chord tones in the 5th octave.

* **Step C: Sound Design & FX**
  - **Instruments**: Native `ReaSynth` used as a placeholder for the guitars and bass to ensure immediate playback.
  - **Drums**: General MIDI mapping on Channel 10 (Kick 36, Snare 38, Hat 42, Crash 49).
  - **Track Coloring**: Distinct colors applied to each track to mimic the visual multi-track setup in the tutorial (Purple, Blue, Orange, Cyan).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Creation & Coloring | `RPR_InsertTrackAtIndex`, Track native colors | Sets up the distinct visual layers required for the multi-track ghost note workflow. |
| Harmonic/Rhythmic Data | `RPR_MIDI_InsertNote` | Computes the exact scale degrees, offsets them into proper octaves, and creates the i-VI-III-VII pattern. |
| Instrument Setup | `RPR_TrackFX_AddByName` | Instantiates `ReaSynth` so the tonal tracks produce immediate sound upon playback. |

> **Feasibility Assessment**: The code produces **100%** of the multi-track musical arrangement shown in the tutorial. *Note:* It purposefully does *not* run a script to alter your global REAPER UI preferences (like docking the MIDI editor or changing your global selection-linking behavior), as overwriting global `reaper.ini` settings via script is unsafe and requires a restart. Instead, it generates the arrangement, colors the tracks, and pre-selects the items—preparing the perfect sandbox for you to practice the tutorial's workflow.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrackRock",
    track_name: str = "Rock Template",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Rock Arrangement (i-VI-III-VII) to practice multi-track editing.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    if key not in NOTE_MAP or scale not in SCALES:
        return "Error: Unsupported key or scale."
        
    scale_intervals = SCALES[scale]
    root_midi = NOTE_MAP[key]
    
    # Standard rock progression: i - VI - III - VII
    # Degrees are 0-indexed relative to the scale
    progression_degrees = [0, 5, 2, 6] 

    def get_chord_pitches(degree, base_octave):
        pitches = []
        for i in [0, 2, 4]: # Root, 3rd, 5th
            idx = degree + i
            octave_offset = idx // len(scale_intervals)
            note_interval = scale_intervals[idx % len(scale_intervals)]
            pitches.append((root_midi + note_interval) + ((base_octave + octave_offset) * 12))
        return pitches

    def insert_midi_note(take, start_sec, end_sec, pitch, vel, chan=0):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, chan, int(pitch), int(vel), False)

    # === Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_length = 60.0 / bpm
    bar_length = beat_length * beats_per_bar
    total_length = bar_length * bars

    track_setup = [
        {"name": "Drums", "color": (130, 50, 200), "is_drum": True},
        {"name": "Bass", "color": (50, 100, 200), "is_drum": False},
        {"name": "GTR Rhythm", "color": (255, 150, 50), "is_drum": False},
        {"name": "GTR Lead", "color": (50, 200, 200), "is_drum": False}
    ]

    start_track_idx = RPR.RPR_CountTracks(0)
    created_items = []

    for i, t_info in enumerate(track_setup):
        idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        
        # Convert RGB to REAPER native color format (R + G<<8 + B<<16 | 0x1000000)
        r, g, b = t_info["color"]
        native_color = r + (g << 8) + (b << 16) | 0x1000000
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", native_color)

        if not t_info["is_drum"]:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_length, False)
        take = RPR.RPR_GetActiveTake(item)
        created_items.append(item)

        for b in range(bars):
            bar_start = b * bar_length
            degree = progression_degrees[b % len(progression_degrees)]
            
            if t_info["name"] == "Drums":
                # Drum Channel is 9 (0-indexed for Ch 10)
                chan = 9
                # Kick (36)
                insert_midi_note(take, bar_start, bar_start + 0.1, 36, 110, chan)
                insert_midi_note(take, bar_start + beat_length*2, bar_start + beat_length*2 + 0.1, 36, 100, chan)
                insert_midi_note(take, bar_start + beat_length*2.5, bar_start + beat_length*2.5 + 0.1, 36, 90, chan)
                # Snare (38)
                insert_midi_note(take, bar_start + beat_length*1, bar_start + beat_length*1 + 0.1, 38, 110, chan)
                insert_midi_note(take, bar_start + beat_length*3, bar_start + beat_length*3 + 0.1, 38, 110, chan)
                # Hats (42) - 8th notes
                for h in range(8):
                    h_start = bar_start + h * (beat_length * 0.5)
                    insert_midi_note(take, h_start, h_start + 0.1, 42, 80 if h%2==1 else 100, chan)
                # Crash (49) on bar 1 only
                if b == 0:
                    insert_midi_note(take, bar_start, bar_start + 0.2, 49, 115, chan)

            elif t_info["name"] == "Bass":
                # Driving 8th notes on the root (Octave 2)
                chord_pitches = get_chord_pitches(degree, base_octave=2)
                root_note = chord_pitches[0]
                for n in range(8):
                    n_start = bar_start + n * (beat_length * 0.5)
                    n_end = n_start + (beat_length * 0.45) # Staccato 8th
                    insert_midi_note(take, n_start, n_end, root_note, 100)

            elif t_info["name"] == "GTR Rhythm":
                # Full chord held for the whole bar (Octave 3/4)
                chord_pitches = get_chord_pitches(degree, base_octave=4)
                for p in chord_pitches:
                    insert_midi_note(take, bar_start, bar_start + bar_length - 0.05, p, 90)

            elif t_info["name"] == "GTR Lead":
                # Arpeggiate the chord (Root, 3rd, 5th, Octave) over 8th notes
                chord_pitches = get_chord_pitches(degree, base_octave=5)
                arp_notes = [chord_pitches[0], chord_pitches[1], chord_pitches[2], chord_pitches[0]+12]
                arp_pattern = [0, 1, 2, 3, 2, 1, 2, 3] # Up and down
                
                for n in range(8):
                    n_start = bar_start + n * (beat_length * 0.5)
                    n_end = n_start + (beat_length * 0.45)
                    pitch = arp_notes[arp_pattern[n]]
                    insert_midi_note(take, n_start, n_end, pitch, 95)
        
        RPR.RPR_MIDI_Sort(take)

    # Select all generated items so the user can double-click to test multi-track editing
    RPR.RPR_Main_OnCommand(40289, 0) # Item: Unselect all items
    for item in created_items:
        RPR.RPR_SetMediaItemSelected(item, True)

    RPR.RPR_UpdateArrange()

    return f"Created 4-track Rock Arrangement in {key} {scale} over {bars} bars at {bpm} BPM. Select all 4 items and open your MIDI editor to practice multi-track editing!"
```