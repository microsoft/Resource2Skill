# Legato Bass Slide Finesse (Overlapping Ghost Notes)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Legato Bass Slide Finesse (Overlapping Ghost Notes)

* **Core Musical Mechanism**: This technique relies on MIDI note overlapping (legato) and keyswitches to trigger portamento/slides in virtual bass instruments (like MODO BASS 2). Because some VSTs struggle to trigger downward slides naturally, a "finesse" technique is used: placing a tiny, heavily overlapped "ghost note" at the lower target pitch immediately preceding the main target note.
* **Why Use This Skill (Rationale)**: Physically, a bass guitar slide represents a continuous shift in pitch across frets without plucking the string again. Virtual instruments mimic this using monophonic legato modes triggered by overlapping MIDI notes. The ghost note trick forces the VST's sample engine to register the downward interval and initialize the slide envelope properly when standard legato overlap fails to do so. 
* **Overall Applicability**: Essential for sequencing realistic basslines in Hip-Hop, R&B, Funk, and Neo-Soul. It replaces rigid, robotic jumps with expressive, human-feeling fretboard glides.
* **Value Addition**: Compared to standard grid-quantized basslines, this skill introduces microscopic timing overlaps and utility notes (keyswitches) that encode deep knowledge of how virtual instrument engines interpret MIDI for humanization.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature/BPM**: 4/4 time, typically 70–100 BPM for R&B/Hip-Hop.
  - **Grid Usage**: Primary notes on the 1/4 or 1/8 grid, but note *lengths* are manually extended by 1/16th or 1/32nd to bleed into the next note.
  - **The "Finesse" Trick**: For downward slides, a 1/32nd ghost note is placed just before the beat, bleeding into the downbeat of the target note.
* **Step B: Pitch & Harmony**
  - **Keyswitch**: C0 (MIDI note 24) is held down to instruct the VST to activate "Legato" mode.
  - **Pitches**: Typically low bass registers (E1 to C3). The pattern moves by large intervals (e.g., Root up to the Fifth, then sliding down to the Minor 3rd).
* **Step C: Sound Design & FX**
  - **Instrument**: MODO BASS 2 (or any monophonic synth/sampler with Portamento/Glide enabled). 
  - **FX Parameter**: To emulate this in stock REAPER without external VSTs, `ReaSynth` is used with the *Portamento* parameter increased, which responds to the exact same overlapping MIDI logic.
* **Step D: Mix & Automation**
  - Slide target notes are often placed at a slightly lower velocity than the initial plucked note to simulate the natural loss of kinetic energy on a real bass string during a slide.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Keyswitch & Legato overlaps | `RPR_MIDI_InsertNote` | Precise start/end PPQ times are required to create the overlaps (legato) and ghost notes that trigger the slide. |
| Pitch computation | Python arithmetic | Computes the precise MIDI note numbers (Root, Fifth, Third) dynamically based on the requested scale. |
| Synth Slide Emulation | FX chain (`ReaSynth`) | Because MODO BASS 2 is a 3rd party VST, we use ReaSynth's Portamento (Param 6) to reproducibly prove the overlapping MIDI logic creates a slide. |

> **Feasibility Assessment**: 90% — The script perfectly recreates the MIDI sequencing technique (the keyswitch, the overlapping legato, and the downward slide finesse trick). However, because we cannot guarantee the user has MODO BASS 2 installed, the script falls back to REAPER's native `ReaSynth` with portamento enabled to demonstrate the acoustic result of the MIDI overlaps.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Legato Bass",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Legato Bass Slide Finesse pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR
    import math

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

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Resolve pitches
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 0) + 36  # Base C2 (MIDI 36)
    
    # Extract scale degrees (safely wrapping octaves if needed)
    root = root_midi
    third = root_midi + scale_intervals[2 % len(scale_intervals)]
    fifth = root_midi + scale_intervals[4 % len(scale_intervals)]
    
    keyswitch_note = 24  # C0 (Standard for VST Legato toggle)

    # Define the note pattern [start_beat, end_beat, pitch, velocity]
    # Note how the end_beats overlap the subsequent start_beats to trigger legato.
    note_events = [
        # 1. The MODO Bass Legato Keyswitch (Hold across the whole phrase)
        (0.0, beats_per_bar * bars, keyswitch_note, 127),
        
        # 2. Pluck Root
        (0.0, 1.25, root, velocity_base),
        
        # 3. Slide Up to Fifth (overlaps Root by 0.25 beats)
        (1.0, 2.25, fifth, velocity_base - 5),
        
        # 4. The Tutorial's "Finesse Trick" for sliding DOWN 
        # A tiny ghost note overlapping the end of the previous note
        (2.125, 2.25, third, int(velocity_base * 0.5)), 
        
        # 5. Main Third (Slide target)
        (2.25, 3.25, third, velocity_base - 10),
        
        # 6. Slide back to Root
        (3.0, 4.0, root, velocity_base - 10)
    ]

    # Convert beats to PPQ and insert notes
    for start_beat, end_beat, pitch, vel in note_events:
        # Loop this 1-bar pattern across the generated item
        for bar in range(bars):
            # Calculate time in seconds
            start_sec = (start_beat + (bar * beats_per_bar)) * (60.0 / bpm)
            end_sec = (end_beat + (bar * beats_per_bar)) * (60.0 / bpm)
            
            # Bound the end_sec to item length
            if start_sec >= item_length:
                continue
            end_sec = min(end_sec, item_length)
            
            # Convert to PPQ
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), int(vel), True
            )

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain (ReaSynth Emulation) ===
    # Adding ReaSynth to demonstrate the slide effect without requiring 3rd party VSTs
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # ReaSynth Param 6 is Portamento. We turn it up to create the glide
    # that happens when MIDI notes overlap.
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.4)
    # Turn down the mix levels slightly to sound a bit more bass-like
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5) # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Release

    return f"Created '{track_name}' with Legato overlapping notes and downward finesse trick over {bars} bars at {bpm} BPM"
```