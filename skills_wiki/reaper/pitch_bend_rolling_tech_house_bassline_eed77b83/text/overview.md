# Pitch-Bend "Rolling" Tech-House Bassline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pitch-Bend "Rolling" Tech-House Bassline

* **Core Musical Mechanism**: Applying a rapid, high-to-low pitch-bend automation (a descending pitch envelope) to the attack transient of synthesized bass notes. Instead of relying purely on filter envelopes or complex LFOs, a quick pitch drop at the start of every note simulates the physical "thump" of a kick drum, making any simple waveform (like a saw or sine) sound incredibly bouncy and percussive.
* **Why Use This Skill (Rationale)**: In tech-house and deep house, the bassline must interlock perfectly with a 4/4 kick without clashing in the sub-frequencies. By using short, staccato notes with a sharp pitch-bend down, you create an artificial psychoacoustic "transient." This gives the bass extreme rhythmic clarity and a "rolling" groove that propels the track forward, even when the harmonic progression is just one or two notes.
* **Overall Applicability**: Essential for tech-house, UK garage, bass house, and minimal techno. It excels on off-beat syncopated basslines that play in the pockets between kick drums.
* **Value Addition**: Transforms a static, lifeless MIDI sequence into a driving, professional-sounding groove without needing third-party plugins. It encodes the knowledge of how macro-level MIDI control (Pitch Bend CC) can dictate micro-level sound design (transient shaping).


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 120 - 128 BPM (tech-house standard).
  - **Grid**: 1/16th note quantization.
  - **Pattern**: Syncopated 16th notes favoring off-beats (the "e", "&", and "a" of the beat), leaving the downbeat empty for the kick drum.
  - **Duration**: Short, staccato notes (~1/16th note length) with slight spaces between them to emphasize the bounce.

* **Step B: Pitch & Harmony**
  - **Progression**: Extremely simple, often just a two-note riff (e.g., F# dropping to F natural) alternating between bars. The tension comes from the rhythm, not complex chords.
  - **Register**: Very low (MIDI octave 1 or 2, around 35-45 Hz fundamental).

* **Step C: Sound Design & FX**
  - **Instrument**: A basic analog-style synthesizer (ReaSynth, Ableton Operator).
  - **Timbre**: A saw wave (for harmonics that cut through small speakers) mixed with a square/sine, heavily low-pass filtered.
  - **Automation**: Pitch bend starting at ~+2 semitones (MIDI value ~10192) and ramping down linearly to center (MIDI value 8192) over ~40-60 milliseconds at the exact start of every note.

* **Step D: Mix & Automation**
  - Bass is typically mono, sitting dead-center in the mix.
  - Sidechain compression is heavily implied in this genre to further duck the bass when the kick hits.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm & Pitch | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides exact control over 1/16th syncopations and the 2-bar chromatic progression. |
| The "Rolling" Effect | MIDI Pitch Bend CC (`RPR_MIDI_InsertCC`) | Accurately recreates John Summit's manual pitch-bend drawing technique from the tutorial, executing a fast ~50ms ramp at the attack of every single note. |
| Timbre / Synth | ReaSynth (FX Chain) | A stock REAPER plugin capable of producing the raw, thick Saw/Square waves necessary for this style of bassline. |

> **Feasibility Assessment**: 95% — The code accurately recreates the rhythmic pattern, the harmonic layout, and the crucial pitch-bend transient shaping entirely within native REAPER tools. The only minor deviation is using ReaSynth instead of Ableton's Operator, but the fundamental sound design principles map 1-to-1.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rolling Bass",
    bpm: int = 126,
    key: str = "F#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Pitch-Bend "Rolling" Bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM (124-128 is ideal for this genre).
        key: Root note (e.g., "F#").
        scale: Scale type (e.g., "minor").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & FX ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # Add a stock synth to generate the raw bass tone
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate fundamental MIDI note (Octave 1/2 for bass)
    root_midi = NOTE_MAP.get(key, 0) + 24 # +24 puts C at C1 (MIDI 24)

    # Typical tech-house rolling syncopated 16th note grid
    # These are 16th-note indices (0-15) within a 4/4 bar where notes occur
    # Intentionally avoiding the downbeats (0, 4, 8, 12) where the kick sits
    rhythm_16ths = [2, 3, 6, 9, 11, 14] 
    
    # Pitch bend automation settings
    pb_center = 8192
    pb_peak = 10192 # roughly +2000 as stated in the tutorial
    pb_duration_beats = 0.1 # ~45ms at 126 BPM, a very fast transient
    pb_steps = 6 # number of MIDI CC events to draw the curve
    note_count = 0

    # === Step 4: Generate Notes and Pitch Bend Curves ===
    for bar in range(bars):
        # The tutorial shifts from F# to F natural on the second bar
        # We mimic this two-bar tension drop by lowering the pitch by 1 semitone on odd bars
        current_pitch = root_midi if (bar % 2 == 0) else root_midi - 1
        
        for step in rhythm_16ths:
            # 16th note timing
            start_time = (bar * bar_length_sec) + (step * 0.25 * beat_sec)
            # Make the note slightly staccato (shorter than a full 16th)
            end_time = start_time + (0.2 * beat_sec) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the MIDI Note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, current_pitch, velocity_base, True)
            note_count += 1
            
            # Draw the Pitch Bend transient curve at the attack of the note
            pb_end_time = start_time + (pb_duration_beats * beat_sec)
            pb_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pb_end_time)
            pb_ppq_range = pb_end_ppq - start_ppq
            
            for i in range(pb_steps):
                fraction = i / (pb_steps - 1)
                # Linear ramp from pb_peak down to pb_center
                current_val = int(pb_center + (pb_peak - pb_center) * (1.0 - fraction))
                
                # Convert 14-bit integer to MIDI LSB / MSB
                lsb = current_val & 0x7F
                msb = (current_val >> 7) & 0x7F
                
                event_ppq = start_ppq + (fraction * pb_ppq_range)
                # 224 (0xE0) is the MIDI status byte for Pitch Bend
                RPR.RPR_MIDI_InsertCC(take, False, False, event_ppq, 224, 0, lsb, msb)

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} rolling bass notes over {bars} bars at {bpm} BPM, complete with Pitch Bend transient automation."
```