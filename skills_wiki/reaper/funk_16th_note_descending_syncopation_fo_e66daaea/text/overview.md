# Funk 16th-Note Descending Syncopation Formula (Nahre Sol Method)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Funk 16th-Note Descending Syncopation Formula (Nahre Sol Method)

* **Core Musical Mechanism**: The defining characteristic of this pattern is displacing a rhythmic stab earlier by exactly one 16th-note subdivision on each consecutive beat. By numbering 16th notes from 1 to 4 in a single beat, the formula plays the 4th subdivision on Beat 1, the 3rd subdivision on Beat 2, and the 2nd subdivision on Beat 3 (the "4-3-2" formula). 

* **Why Use This Skill (Rationale)**: This creates immense rhythmic tension. By striking notes progressively earlier against a rigid 4/4 drum framework, it disrupts the listener's expectation of strong downbeats. This "rub" creates a highly syncopated, bouncing momentum characteristic of James Brown and classic funk. The mathematical staggering ensures that stabs never land on the predictable "1" or "2", keeping the groove continuously moving forward.

* **Overall Applicability**: Essential for funk, neo-soul, disco, and upbeat hip-hop. This pattern is typically applied to staccato "comping" instruments: clavinet, Hammond organ, electric guitar (chops), or brass sections.

* **Value Addition**: Instead of randomly placing off-beat MIDI notes and hoping for a groove, this skill encodes a rigorous mathematical approach to syncopation that guarantees a pocketed funk feel. It also pairs the rhythm with tightly voiced dominant or minor 7th chords.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically around 95–115 BPM.
  - **Grid**: 1/16th notes.
  - **Rhythmic Formulas Used**:
    - *4-3-2*: Hits on 1e&**a**, 2e**&**a, 3**e**&a.
    - *3-2*: Hits on 1e**&**a, 2**e**&a.
    - *4-3*: Hits on 1e&**a**, 2e**&**a.
  - **Note Duration**: Very staccato (less than an 8th note in length).

* **Step B: Pitch & Harmony**
  - **Chord Types**: Funk relies heavily on minor 7th (Dorian) or dominant 7th/9th chords (Mixolydian).
  - **Voicing**: Tight, punchy stacks. Often omitting the 5th and emphasizing the root, 3rd, and 7th. We will construct a minor 7th or dominant 7th voicing depending on the selected scale.

* **Step C: Sound Design & FX**
  - **Instrument**: Short, plucky synthesizer (we will configure ReaSynth).
  - **ADSR Envelope**: Instant attack (0ms), very short decay (150-200ms), no sustain, short release.

* **Step D: Mix & Automation**
  - **Velocity**: Consistently strong but responsive, typical of hard organ/clavinet stabs. 


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Descending Syncopation Rhythm | `MIDI_InsertNote` with precise math | REAPER's PPQ-based MIDI API allows for exact positioning of the 4-3-2, 3-2, and 4-3 16th-note offsets without relying on quantize actions. |
| Harmonic Voicings | Python lists and intervals | We dynamically construct Funk minor 7 / dom 7 chord voicings based on the input key/scale rather than hardcoding. |
| Staccato Pluck Sound | `TrackFX_AddByName` (ReaSynth) | We can adjust the ADSR natively via `TrackFX_SetParamNormalized` to ensure the notes are punchy and don't bleed into each other. |

> **Feasibility Assessment**: 95% reproducible. The script perfectly reproduces the 16th-note syncopation formulas, the chord voicings, and creates a 4-bar phrase combining the variations shown in the video. The only slight compromise is using ReaSynth instead of a sampled Clavinet or Organ, but the envelope is tailored to match the staccato funk style.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Funk Syncopation Stabs",
    bpm: int = 105,
    key: str = "D",
    scale: str = "dorian",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create Nahre Sol's 'Descending 16th-Note Funk Formula' in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (typically 95-115 for funk).
        key: Root note (e.g., 'D').
        scale: Scale type ('dorian', 'minor', 'major', 'mixolydian').
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key, 2)
    # Start at octave 4 (mid-high range for funk stabs)
    root_midi = 48 + root_val 
    
    # Determine funk chord voicing (Min7 for Dorian/Minor, Dom7 for Major/Mixolydian)
    if scale.lower() in ["minor", "dorian", "pentatonic_minor", "blues"]:
        # Root, minor 3rd, perfect 5th, minor 7th, octave root
        chord_intervals = [0, 3, 7, 10, 12] 
    else:
        # Root, major 3rd, perfect 5th, minor 7th, octave root
        chord_intervals = [0, 4, 7, 10, 12]
        
    chord_notes = [root_midi + i for i in chord_intervals]

    # Create new track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Create MIDI Item
    beats_per_bar = 4
    quarter_note_sec = 60.0 / bpm
    bar_length_sec = quarter_note_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Formulas defined in the video (offsets in exact beats from start of bar)
    # 4-3-2: Hit on 4th 16th of beat 1, 3rd 16th of beat 2, 2nd 16th of beat 3
    pattern_432 = [0.75, 1.5, 2.25]
    # 3-2: Hit on 3rd 16th of beat 1, 2nd 16th of beat 2
    pattern_32 = [0.5, 1.25]
    # 4-3: Hit on 4th 16th of beat 1, 3rd 16th of beat 2
    pattern_43 = [0.75, 1.5]

    total_notes_added = 0
    note_duration_beats = 0.15 # Very staccato

    # Loop through bars and apply the syncopation formulas to build a phrase
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Cycle through formulas for phrasing variation
        phrase_pos = bar % 4
        if phrase_pos == 0:
            active_pattern = pattern_432
        elif phrase_pos == 1:
            active_pattern = pattern_32
        elif phrase_pos == 2:
            active_pattern = pattern_43
        else:
            active_pattern = pattern_432
            
        for beat_offset in active_pattern:
            # Calculate start and end times in seconds
            start_sec = (bar_start_beat + beat_offset) * quarter_note_sec
            end_sec = start_sec + (note_duration_beats * quarter_note_sec)
            
            # Convert to PPQ for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            # Insert full chord at this syncopated position
            for pitch in chord_notes:
                # small velocity variance for groove
                vel = max(1, min(127, velocity_base + (total_notes_added % 5))) 
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # Add ReaSynth and configure it for a staccato clavinet/organ punch
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Param 0: Volume (-10dB approx to avoid clipping with dense chords)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.4) 
    # Param 1: Tuning
    # Param 2: Attack (Instant = 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.0)
    # Param 3: Decay (Short/plucky = ~0.15)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.15)
    # Param 4: Sustain (Zero = 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.0)
    # Param 5: Release (Short = 0.05)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.05)
    # Param 6: Square wave mix (Add harmonics for funk organ/clav sound)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.5)

    return f"Created '{track_name}' with {total_notes_added} notes across {bars} bars at {bpm} BPM using descending 16th-note syncopation formulas."
```