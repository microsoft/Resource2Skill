### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Band Scaffold & Workflow Template

* **Core Musical Mechanism**: The tutorial demonstrates a specialized workflow for writing multi-part arrangements (Drums, Bass, Rhythm Guitar, Lead Guitar) inside a single, unified MIDI editor. The musical vehicle for this workflow is a driving, 8th-note rock/metal pattern. The signature of this pattern is strict interlocking alignment: the bass and rhythm guitar play identical rhythmic pulses (8th notes) reinforcing the chord roots, the drums provide a steady backbeat anchor, and the lead instrument floats on top with a slower, syncopated melody. 

* **Why Use This Skill (Rationale)**: Writing music across multiple interacting instruments requires seeing the "big picture." Musically, this technique leverages harmonic and rhythmic vertical alignment. By coloring MIDI notes by *Track* instead of Velocity or Pitch, producers can immediately visually identify frequency masking and rhythmic clashing. The driving i-VI-III-VII minor progression used in the video provides immediate forward momentum, relying on the tension of the minor 6th and the resolution of the dominant-functioning VII chord.

* **Overall Applicability**: This is universally applicable for any multi-instrument genre: rock, metal, orchestral mockups, or layered EDM synths. Generating this multi-track template allows a producer to immediately practice the "Color Notes by Track" single-window workflow without having to manually record 4 separate instruments first.

* **Value Addition**: Instead of just a blank project, this skill provides a fully harmonized, 4-part arrangement mathematically locked to the user's chosen key and scale. It color-codes the tracks automatically, setting up the exact prerequisite needed to utilize REAPER's multi-track MIDI editing capabilities.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically 120-140 BPM (default 120).
  - **Rhythm Grid**: 
    - *Bass & Rhythm Guitar*: Straight, driving 1/8th notes. 
    - *Drums*: Standard rock beat (Kick on 1 and 3; Snare on 2 and 4; Hi-hat on straight 1/8th notes).
    - *Lead*: Longer, legato melody notes (1/2 notes and 1/4 notes) to contrast the driving rhythm section.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: B Minor (natural minor) in the video, but fully parameterized. 
  - **Progression**: i - VI - III - VII. In a minor scale, this maps to scale degrees 1, 6, 3, and 7.
  - **Voicings**: 
    - Bass plays the root note 2 octaves down.
    - Rhythm Guitar plays power chords (Root + Perfect 5th + Octave) 1 octave down.
    - Lead Guitar plays passing notes within the scale structure.

* **Step C: Sound Design & FX**
  - **Instruments**: Native `ReaSynth` added as a placeholder tone generator for the tonal tracks (Bass, Rhythm, Lead). 
  - **Workflow Setup**: Tracks are uniquely color-coded (Pink for Drums, Purple for Bass, Orange for Rhythm, Blue for Lead). In REAPER's MIDI Editor, changing the view to *Color Notes by: Track* will perfectly mimic the video's workflow.

* **Step D: Mix & Automation**
  - Track volumes are roughly balanced via basic velocity assignments (Kick/Snare hit harder than Hi-hats, Lead is slightly louder than rhythm guitar).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Creation & Coloring | `RPR_InsertTrackAtIndex`, `RPR_SetMediaTrackInfo_Value` | Essential for recreating the visual multi-track workflow shown in the video. |
| Interlocking Arrangements | `RPR_CreateNewMIDIItemInProj`, `RPR_MIDI_InsertNote` | Computes the i-VI-III-VII progression dynamically across 4 instruments using scale math. |
| Placeholder Sound | `RPR_TrackFX_AddByName` (ReaSynth) | Ensures the tonal tracks make sound immediately without requiring external VSTs (like Kontakt/NeuralDSP). |

> **Feasibility Assessment**: 100% of the *musical arrangement* and *track setup* is reproducible. Modifying global user preferences (like "One MIDI Editor per Project" and "Docking") is skipped because altering global user configs via script violates the non-destructive/additive safety rules, but the script sets up the perfect color-coded sandbox for the user to try those exact settings.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrackWorkflow",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part Rock/Metal Multi-Track Scaffold in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate (multiples of 4 work best).
        velocity_base: Base MIDI velocity (0-127).
    
    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    # Standard rock/pop progression relative to scale root
    # For minor: i (0), VI (5), III (2), VII (6)
    # For major: I (0), vi (5), IV (3), V (4)
    progression_indices = [0, 5, 2, 6] if scale == "minor" else [0, 5, 3, 4]
    
    if key not in NOTE_MAP or scale not in SCALES:
        return "Error: Invalid key or scale provided."
        
    root_midi = NOTE_MAP[key] + 48 # Base octave C3
    scale_intervals = SCALES[scale]

    # Helper function to compute pitch from scale degree
    def get_pitch(degree, octave_offset=0):
        octaves = degree // 7
        scale_idx = degree % 7
        return root_midi + scale_intervals[scale_idx] + ((octaves + octave_offset) * 12)

    # Helper function to generate track colors (R, G, B) to REAPER native format
    def make_color(r, g, b):
        return int(r + (g * 256) + (b * 65536)) | 0x1000000

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len = 60.0 / bpm
    item_length = beat_len * beats_per_bar * bars

    track_configs = [
        {"name": "Drums",      "color": make_color(255, 105, 180)}, # Pink
        {"name": "Bass",       "color": make_color(138, 43, 226)},  # Purple
        {"name": "Rhythm Gtr", "color": make_color(255, 140, 0)},   # Orange
        {"name": "Lead Gtr",   "color": make_color(30, 144, 255)}   # Blue
    ]

    base_track_idx = RPR.RPR_CountTracks(0)

    for i, cfg in enumerate(track_configs):
        track_idx = base_track_idx + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Set name and color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", cfg["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", cfg["color"])
        
        # Add basic synth to tonal tracks so they produce sound
        if cfg["name"] != "Drums":
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

        # Create MIDI item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
        take = RPR.RPR_GetActiveTake(item)
        
        # Populate MIDI data
        for bar in range(bars):
            chord_degree = progression_indices[bar % len(progression_indices)]
            bar_start_time = bar * beats_per_bar * beat_len
            
            if cfg["name"] == "Drums":
                # Kick/Snare/Hat pattern
                for beat in range(beats_per_bar):
                    beat_time = bar_start_time + (beat * beat_len)
                    
                    # Kick on 1 and 3, Snare on 2 and 4
                    is_snare = beat % 2 != 0
                    drum_pitch = 38 if is_snare else 36
                    
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, beat_time + (beat_len * 0.5))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 9, drum_pitch, velocity_base, False)
                    
                    # 8th note hi-hats (2 per beat)
                    for eighth in range(2):
                        hh_time = beat_time + (eighth * (beat_len / 2.0))
                        hh_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time)
                        hh_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, hh_time + (beat_len * 0.25))
                        RPR.RPR_MIDI_InsertNote(take, False, False, hh_start, hh_end, 9, 42, int(velocity_base * 0.8), False)

            elif cfg["name"] == "Bass":
                # Driving 8th notes on root
                pitch = get_pitch(chord_degree, octave_offset=-2)
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * (beat_len / 2.0))
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (beat_len * 0.45)) # slight staccato
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

            elif cfg["name"] == "Rhythm Gtr":
                # Driving 8th notes (Power Chords: Root + 5th)
                root_p = get_pitch(chord_degree, octave_offset=-1)
                fifth_p = root_p + 7 # Strict perfect 5th for power chord
                
                for eighth in range(8):
                    note_time = bar_start_time + (eighth * (beat_len / 2.0))
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + (beat_len * 0.45))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_p, velocity_base, False)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fifth_p, velocity_base, False)

            elif cfg["name"] == "Lead Gtr":
                # Simple slower melodic motif (Root -> 3rd -> 5th based on the scale)
                melody_degrees = [chord_degree, chord_degree + 2, chord_degree + 4]
                
                for i, m_deg in enumerate(melody_degrees):
                    if i > 1 and bar % 2 != 0: 
                        continue # Leave space on alternating bars
                        
                    note_time = bar_start_time + (i * beat_len * 1.5)
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, note_time + beat_len)
                    
                    pitch = get_pitch(m_deg, octave_offset=1)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base + 10, False)

        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track template (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {scale} at {bpm} BPM."
```