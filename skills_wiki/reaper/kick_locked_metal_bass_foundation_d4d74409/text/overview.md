### 1. High-level Design Pattern Extraction

> **Skill Name**: Kick-Locked Metal Bass Foundation

* **Core Musical Mechanism**: Rhythmic unison between the bass guitar and the kick drum. The bass primarily plays pedaled root notes (open strings or lowest notes) in exact synchronization with a syncopated kick drum pattern. To prevent the part from becoming overly monotonous, occasional octave jumps (+12 semitones, representing the 12th fret on a bass) are inserted at phrase turnarounds.
* **Why Use This Skill (Rationale)**: In rock, metal, and metalcore, the bass guitar often serves as the "glue" between the drums and the rhythm guitars. By locking the bass exactly to the kick drum, the kick feels melodic and heavy, while the bass guitar gains a massive percussive attack. Additionally, lowering the MIDI velocity (from the default 127 down to ~110) prevents modern sampled bass instruments from sounding overly harsh, clicky, and abrasive on every single note.
* **Overall Applicability**: Essential for hard rock, metalcore, djent, pop-punk, and heavy modern pop. It is the fundamental technique for programming MIDI bass libraries (like DjinnBass, MODO Bass, Eurobass, etc.).
* **Value Addition**: Transforms a static, sustained bassline into a driving, aggressive groove. It encodes the specific velocity-taming technique used by producers to make virtual basses sound like real players rather than machine guns.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 16th-note syncopated grid (typical for metal).
  - **Pattern**: A mixture of staccato 16th notes (for fast double-kick flurries) and 8th/quarter notes (for heavy downbeats).
  - **Turnarounds**: At the end of a 2-bar or 4-bar phrase, rhythmic density often changes, or notes are held slightly longer to introduce a fill.
* **Step B: Pitch & Harmony**
  - **Root Note Pedal**: 95% of the notes sit on the root note of the track's key (e.g., C1 or C2 for "Drop C" tuning).
  - **Octave Displacement**: Moving the root note up exactly one octave (12 semitones) during phrase endings provides variation without disrupting the harmonic foundation. 
* **Step C: Sound Design & FX**
  - **Instrument**: Modern virtual bass VSTs (DjinnBass shown in the tutorial).
  - **Velocity Control**: Capped around 110. In heavy music, velocities of 127 often trigger the "slap" or maximum-aggression layers of a sampler. Pulling it back to 110 keeps the tone thick but removes annoying string/fret noise.
* **Step D: Mix & Automation**
  - Usually sent to a split-processing chain (sub-bass vs. distorted grit), though the fundamental MIDI programming is the core focus here.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Synchronization | MIDI note insertion via `RPR_MIDI_InsertNote` | Allows programmatic generation of a syncopated 16th-note "kick" grid. |
| Taming Harshness | Explicit Velocity scaling (`vel = 110`) | Directly reproduces the tutorial's advice to drop velocity from 127 to remove excessive high-end string noise. |
| Variation / Turnarounds | Pitch math (`pitch + 12`) | Replicates the "12th fret" octave jump demonstrated in the video for phrase endings. |
| Instrument | `ReaSynth` (Placeholder) | Provides an immediate, stock, low-end tone since third-party VSTs like DjinnBass cannot be guaranteed on the execution environment. |

> **Feasibility Assessment**: 100% of the MIDI programming technique is reproduced. The specific timbre of Submission Audio's DjinnBass cannot be fully replicated with stock plugins, but the script sets up a thick ReaSynth bass tone as a working placeholder.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Bass (Kick-Locked)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly lowered from 127 to remove string noise
    **kwargs,
) -> str:
    """
    Create a kick-locked metal bassline in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc. - mostly irrelevant as we pedal the root).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), intentionally lowered for tone control.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note map to find the root pitch
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Metal bass tunings typically place the root very low (C1 or C2). 
    # MIDI note 24 is C1.
    root_pitch = NOTE_MAP.get(key, 0) + 24 
    
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

    # Core syncopated metal/djent rhythm representing a kick drum pattern.
    # List of tuples: (start_beat, length_in_beats)
    kick_rhythm_beats = [
        (0.0, 0.5),    # Downbeat
        (0.75, 0.25),  # 16th note syncopation ("a" of 1)
        (1.5, 0.5),    # Upbeat of 2
        (2.25, 0.25),  # 16th note 
        (2.5, 0.25),   # 8th note
        (3.0, 0.5)     # Downbeat of 4
    ]

    notes_created = 0

    # === Step 4: Generate MIDI Notes ===
    for bar in range(bars):
        for start_beat, length in kick_rhythm_beats:
            
            # Determine if we should do an octave jump for variation
            # We do this on the last beat of every 2nd bar (phrase turnaround)
            is_turnaround = (bar % 2 == 1) and (start_beat == 3.0)
            pitch = root_pitch + 12 if is_turnaround else root_pitch
            
            # Calculate actual timing in seconds, then convert to PPQ
            actual_start_beat = start_beat + (bar * beats_per_bar)
            start_time = actual_start_beat * (60.0 / bpm)
            end_time = (actual_start_beat + length) * (60.0 / bpm)
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Insert the note
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, True)
            notes_created += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Stock FX Chain Placeholder ===
    # Since we can't guarantee DjinnBass is installed, we create a heavy sub-bass with ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Adjust ReaSynth for a more "bass guitar" fundamental tone (more Saw/Square, less Sine)
    RPR.RPR_TrackFX_SetParam(track, 0, 0, 0.0) # Sine vol down
    RPR.RPR_TrackFX_SetParam(track, 0, 1, 0.7) # Square/Saw vol up
    RPR.RPR_TrackFX_SetParam(track, 0, 2, 0.5) # Triangle vol up
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.1) # Faster attack

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM. Velocity clamped at {velocity_base} to reduce sampler string noise."
```