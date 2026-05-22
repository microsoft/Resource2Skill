# Diatonic Triad Progression Generator

## Analysis

# 1. High-level Design Pattern Extraction

> **Skill Name**: Diatonic Triad Progression Generator

* **Core Musical Mechanism**: The foundational technique demonstrated in the tutorial is building diatonic triads (three-note chords) strictly within a chosen key and scale. The creator visually demonstrates that once you identify the notes of a scale (e.g., all white keys for C Major / A Minor), you can build harmonious chords by picking a root note and stacking every other note in that scale on top of it. This automatically generates a mix of Major, Minor, and Diminished chords that perfectly belong together.

* **Why Use This Skill (Rationale)**: This is the bedrock of Western tonal harmony. By restricting chord tones strictly to the scale (diatonic harmony), tension and release are naturally managed without introducing harsh dissonance. The specific spatial relationship—stacking notes in "thirds" (skipping a scale degree)—creates triads, which provide enough harmonic information to establish a mood without cluttering the frequency spectrum. 

* **Overall Applicability**: This skill is universally applicable across almost all genres—from pop, EDM, and hip-hop to orchestral music and rock. Generating a 4-bar or 8-bar diatonic chord loop is usually "Step 1" of music production, providing the harmonic bed over which basslines are written and melodies are sung.

* **Value Addition**: Compared to a blank MIDI clip or mindlessly clicking notes, this skill encodes fundamental music theory. It translates conceptual inputs ("I want a I-V-vi-IV progression in G minor") into exact mathematical MIDI pitch calculations, ensuring the resulting chords are always perfectly in key.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically around 100-120 BPM for beginners (the video shifts tempo at the end).
  - **Rhythmic Grid**: The tutorial relies on long, sustained chords playing for exactly 1 full bar (whole notes) or 1/2 bar (half notes) to establish a harmonic foundation.
  - **Duration**: Legato (notes touch end-to-end exactly on the grid lines).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Major / A Minor are heavily featured, though the theory applies universally.
  - **Voicings**: Root position block chords (Root, 3rd, 5th). 
  - **Construction Logic**: To build a chord on the 1st degree of the scale, play the 1st, 3rd, and 5th notes of that scale. To build on the 2nd degree, play the 2nd, 4th, and 6th notes.

* **Step C: Sound Design & FX**
  - **Instrument**: The tutorial shows Native Instruments Kontakt, but explicitly notes that third-party VSTs can be finicky to set up. To ensure guaranteed reproduction, stock REAPER plugins (like `ReaSynth`) are preferred for immediate sound generation.

* **Step D: Mix & Automation (if applicable)**
  - Basic volume leveling. The video briefly shows pulling the track fader down to prevent clipping.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Diatonic Chord Generation | API: `RPR_MIDI_InsertNote` | Allows us to calculate scale degrees mathematically and insert exact MIDI pitches. |
| Grid Alignment | Time-to-PPQ conversion | `RPR_MIDI_GetPPQPosFromProjTime` ensures notes lock perfectly to the REAPER grid regardless of BPM. |
| Sound Generation | FX Chain: `ReaSynth` | The tutorial uses Kontakt, but acknowledging the creator's own disclaimer about VST troubleshooting, loading a stock REAPER synth guarantees the agent's code will produce audible sound immediately without external libraries. |

> **Feasibility Assessment**: 100% reproduction of the musical theory and MIDI structure shown in the video. The specific timbral tone of the Kontakt patches used in the video is approximated using REAPER's built-in ReaSynth to ensure perfect script execution on any machine.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Diatonic Chords",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Diatonic Triad Progression in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: 
            progression (list): List of scale degrees (1-7) for the chords. Default [1, 5, 6, 4].
            octave (int): Base octave for the chords. Default 4.

    Returns:
        Status string detailing the track creation.
    """
    import reaper_python as RPR

    # --- Configuration & Theory Parameters ---
    progression = kwargs.get("progression", [1, 5, 6, 4]) # Standard pop progression (I-V-vi-IV)
    base_octave = kwargs.get("octave", 4)
    
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "major"
    if key not in NOTE_MAP:
        key = "C"

    root_pitch_class = NOTE_MAP[key]
    scale_intervals = SCALES[scale]

    # --- Step 1: Project Setup ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Add new track at the end
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Lower volume slightly to prevent clipping (-6dB approx)
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.5)

    # --- Step 2: Add Sound Generator ---
    # We use ReaSynth to guarantee sound output without third-party VSTs
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Soften the ReaSynth sound (lower square/saw mix, increase release)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.1) # Saw mix
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5) # Release time

    # --- Step 3: Time & Item Calculation ---
    beats_per_bar = 4
    beat_duration_sec = 60.0 / bpm
    bar_duration_sec = beat_duration_sec * beats_per_bar
    total_duration_sec = bar_duration_sec * bars

    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, total_duration_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # --- Step 4: Diatonic Chord Generation ---
    notes_added = 0
    chords_per_bar = 1
    duration_per_chord_sec = bar_duration_sec / chords_per_bar
    
    # Loop over the requested number of bars
    for bar in range(bars):
        # Loop the progression
        chord_degree = progression[bar % len(progression)] 
        scale_index = chord_degree - 1 # 0-indexed
        
        # Calculate time positions
        start_time = bar * bar_duration_sec
        end_time = start_time + duration_per_chord_sec
        
        # Convert time to PPQ (MIDI ticks)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Build the triad (Root, 3rd, 5th) in the diatonic scale
        for triad_interval in [0, 2, 4]:
            target_index = scale_index + triad_interval
            
            # Handle wrapping to the next octave if we exceed the 7-note scale
            octave_offset = target_index // 7
            wrapped_index = target_index % 7
            
            # Calculate final MIDI pitch
            note_pitch_class = (root_pitch_class + scale_intervals[wrapped_index]) % 12
            # Add an extra octave offset if the scale interval calculation wrapped past C
            pitch_wrap = 1 if (root_pitch_class + scale_intervals[wrapped_index]) >= 12 else 0
            
            midi_pitch = (base_octave + octave_offset + pitch_wrap) * 12 + note_pitch_class
            
            # Keep pitch within safe MIDI bounds (0-127)
            midi_pitch = max(0, min(127, midi_pitch))
            
            # Insert Note
            # RPR_MIDI_InsertNote(take, selected, muted, startppqpos, endppqpos, chan, pitch, vel, noSort)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, midi_pitch, velocity_base, False)
            notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    prog_str = "-".join(str(d) for d in progression)
    return f"Created '{track_name}' playing {prog_str} in {key} {scale}. {notes_added} notes across {bars} bars at {bpm} BPM."
```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)? *(Yes, builds chords strictly using scale degree logic + intervals)*
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)? *(Yes, uses `RPR_InsertTrackAtIndex`)*
- [x] Does it set the track name so the element is identifiable? *(Yes)*
- [x] Are all velocity values in the 0-127 MIDI range? *(Yes)*
- [x] Are note timings quantized to the musical grid (no floating-point drift)? *(Yes, calculated securely via `GetPPQPosFromProjTime`)*
- [x] Does the function return a descriptive status string? *(Yes)*
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? *(Yes, generates continuous diatonic chords exactly as constructed in the video's piano roll)*
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters? *(Yes)*
- [x] Does it avoid hardcoded file paths or external sample dependencies? *(Yes, uses REAPER's native `ReaSynth` plugin)*