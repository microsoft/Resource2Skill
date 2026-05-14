# Trap/Drill 808 Portamento Glide (Native Overlapping Slides)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Trap/Drill 808 Portamento Glide (Native Overlapping Slides)

* **Core Musical Mechanism**: The defining characteristic of this skill is the "808 glide" or "slide"—a monophonic pitch bend triggered by **overlapping MIDI notes** in conjunction with a synth/sampler set to **Portamento** mode with a maximum of 1 voice. When a new note is played before the previous note finishes, the instrument mathematically interpolates (glides) the pitch from the first note to the second over a specified millisecond duration, creating a fluid, sweeping bass movement.
* **Why Use This Skill (Rationale)**: Pitch gliding creates immense rhythmic momentum and tension. By sliding up to a higher octave or a perfect fifth on an off-beat, the bass line emphasizes syncopation and transitions smoothly between chord changes or drum hits. Psychoacoustically, the continuous pitch sweep grabs the listener's attention much more aggressively than a discrete note jump, forming the backbone of modern Trap, Drill, and UK Bass grooves.
* **Overall Applicability**: Essential for modern hip-hop 808 basslines, heavy EDM synth basses, and G-Funk lead synth melodies. It turns static, blocky bass progressions into fluid, vocal-like performances.
* **Value Addition**: This encodes the specific relationship between MIDI note duration programming and monophonic synth settings. A standard block MIDI chord progression fails here; the skill teaches that *deliberate note overlapping* is the mechanical requirement to trigger portamento logic in DAWs.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **BPM Range**: 140 - 160 BPM (Trap/Drill tempos).
  - **Grid**: 1/8th and 1/16th note syncopations.
  - **Durations (Crucial)**: Base notes are sustained. Glide notes must be programmed to begin *before* the preceding base note ends. The length of the overlap dictates the start of the glide, while the portamento parameter dictates the speed of the pitch sweep.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically minor or harmonic minor. 
  - **Pitches**: 
    - Base notes sit in the sub-bass range (MIDI notes 24-36 / C1-C2).
    - Glide notes frequently jump +12 semitones (an octave) or +7 semitones (a perfect fifth).
* **Step C: Sound Design & FX**
  - **Instrument**: The tutorial demonstrates `ReaSamplOmatic5000` (RS5K).
  - **Required Plugin Settings**:
    - `Max voices` = 1 (Forces the sampler into monophonic mode).
    - `Portamento` = > 0ms (e.g., 50ms - 150ms). Controls the glide speed.
* **Step D: Mix & Automation**
  - No explicit automation envelopes are needed for the pitch bend—the overlapping MIDI notes natively control when the slide happens based on the synth's internal portamento engine.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Monophonic 808 Tone | FX Chain (`ReaSynth`) | The tutorial uses `ReaSamplOmatic5000` with an imported audio sample. To guarantee self-contained execution without requiring external WAV downloads, `ReaSynth` is used as an audible 808 sub-bass substitute. |
| Portamento Glide Settings | FX Parameter (`RPR_TrackFX_SetParam`) | Directly sets the monophonic portamento knob in ReaSynth to enable pitch sweeping. |
| Glide Triggering | MIDI Note Insertion (Overlapping) | Deliberately inserting notes whose start-time precedes the end-time of the previous note is the mandatory trigger for the portamento effect shown in the video. |

> **Feasibility Assessment**: 100% of the *musical technique* (overlapping MIDI + portamento gliding) is reproduced. We substitute `ReaSynth` for `RS5K` to ensure the script plays an audible 808 out-of-the-box without failing due to a missing hard-drive sample, fully respecting the tutorial's core mechanism.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Glide Bass",
    bpm: int = 150,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Trap/Drill 808 bass pattern with overlapping notes triggering Portamento glides.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # We drop the root note down to the sub-bass octave (MIDI octave 2 -> base 24)
    base_midi_note = NOTE_MAP.get(key, 0) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (ReaSynth tuned as an 808 Sub) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure ReaSynth to sound like a deep 808 and enable Portamento
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.8)   # Param 0: Volume
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.0)   # Param 3: Square Mix (0 = clean)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 1.0)   # Param 5: Triangle Mix (fat sub)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.8)   # Param 6: Extra Sine Mix (deep sub)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.35)  # Param 8: Portamento (approx 150ms glide)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # === Step 5: Program MIDI Notes (with deliberate overlapping) ===
    # Pattern: 
    # Beat 0.0 -> 1.0: Sustained root note
    # Beat 1.5 -> 2.5: Sustained root note
    # Beat 2.5 -> 3.5: Sustained root note 
    # Beat 3.25 -> 4.0: High glide note (Overlaps the 2.5 note to trigger the portamento slide!)
    
    pattern_beats = [
        {"start": 0.0,  "end": 1.0, "pitch_offset": 0},
        {"start": 1.5,  "end": 2.5, "pitch_offset": 0},
        {"start": 2.5,  "end": 3.5, "pitch_offset": 0},
        {"start": 3.25, "end": 4.0, "pitch_offset": 12}, # Overlaps previous note by 0.25 beats, slides +1 Octave
    ]
    
    notes_created = 0
    
    for bar in range(bars):
        bar_beat_offset = bar * beats_per_bar
        
        for note in pattern_beats:
            # Convert beats to time in seconds
            start_time = (bar_beat_offset + note["start"]) * (60.0 / bpm)
            end_time = (bar_beat_offset + note["end"]) * (60.0 / bpm)
            
            # Convert time to PPQ (Pulses Per Quarter Note) for accurate MIDI placement
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            pitch = base_midi_note + note["pitch_offset"]
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, pitch, velocity_base, False
            )
            notes_created += 1

    # Force sort to finalize MIDI
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} overlapping notes over {bars} bars at {bpm} BPM to trigger portamento glides."
```