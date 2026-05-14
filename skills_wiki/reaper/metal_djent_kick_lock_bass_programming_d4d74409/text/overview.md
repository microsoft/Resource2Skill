### 1. High-level Design Pattern Extraction

> **Skill Name**: Metal/Djent Kick-Lock Bass Programming

* **Core Musical Mechanism**: This technique involves programming a bass guitar MIDI track to rhythmically "lock" to a syncopated kick drum pattern. The bass pedals on a low root note (e.g., Drop C) using a mix of staccato 16th notes for fast bursts and sustained 8th/quarter notes for heavy impacts. Occasional octave (+12 semitones) or minor third (+3 semitones) jumps are used to mirror the rhythm guitar's melodic variations.
* **Why Use This Skill (Rationale)**: In modern metal, metalcore, and djent, the bass guitar's primary role is to reinforce the kick drum and the rhythm guitar. Striking simultaneously with the kick creates a massive, unified low-end transient. Crucially, the instructor notes that virtual bass libraries (like DjinnBass or MODO Bass) often sound overly aggressive, clanky, and harsh when MIDI velocities are left at the default 127. Pulling the velocities down to exactly 110 hits the sample library's dynamic "sweet spot"—maintaining a heavy attack while taming the piercing high-end frequencies of the pick attack.
* **Overall Applicability**: Essential for heavy music production (Metalcore, Djent, Deathcore, Hard Rock) where the bass acts as the percussive glue between fast double-kick drums and down-tuned rhythm guitars.
* **Value Addition**: Transforms a flat, robotic bass drone into an aggressive, grooving rhythm section by encoding authentic metal syncopation, octave guitar-mirroring, and genre-specific velocity sweet spots.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 16th-note resolution.
  - **Pattern**: Highly syncopated, mimicking a metal breakdown pattern.
  - **Articulation**: Fast successive notes (e.g., the "e" and "a" of a beat) are drawn as short staccato 1/16th notes, while strong downbeats (1, 2, 3, 4) or isolated hits are drawn as longer sustained 1/8th or 1/4 notes to fill out the sub-frequencies.
* **Step B: Pitch & Harmony**
  - **Pedal Point**: Vast majority of notes are played on the lowest open string (the root note of the key, MIDI note 24 or 36 depending on octave).
  - **Fretboard Jumps**: Rhythmic variation is added by moving up to the 12th fret (octave jump, +12) or the 3rd fret (minor 3rd, +3) to match theoretical rhythm guitar fills.
* **Step C: Sound Design & FX**
  - **Instrument**: Intended for virtual bass VSTis (DjinnBass, Eurobass, SubMission Audio, etc.). Our script uses ReaSynth as a stock placeholder.
* **Step D: Mix & Automation**
  - **Velocity Control**: Fixed strictly at `110` to avoid the harsh sample layers triggered at 127, providing a cleaner, more mixable tone.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Kick-Locking | `RPR_MIDI_InsertNote` | Allows us to place staccato and legato notes on a precise 16th-note grid. |
| Taming harshness | Hardcoded `vel = 110` | Replicates the instructor's specific advice for programming virtual metal bass. |
| Guitar mirroring | Dynamic pitch offsets | Adds the 12th fret (+12) and 3rd fret (+3) variations to the 2nd bar of the loop. |

> **Feasibility Assessment**: 100% reproducible for the MIDI and rhythm composition. The specific DjinnBass VST tone cannot be produced with stock plugins, so a basic ReaSynth is inserted as a placeholder. The user should swap ReaSynth for their preferred bass VSTi to achieve the exact sound from the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Metal Kick-Lock Bass",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Metal/Djent Kick-Lock Bass sequence in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (110-150 recommended for this style).
        key: Root note (e.g., "C" for Drop C tuning).
        scale: Scale type (affects the fret jumps).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (fixed to 110 per tutorial to avoid harshness).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
                
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Insert a placeholder synth (User should replace this with DjinnBass or MODO Bass)
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define root note in the lowest register (e.g., C1 = MIDI 24)
    base_midi_note = 24 + NOTE_MAP.get(key, 0)
    
    # Define syncopated rhythm patterns (Start QN, Length QN, Pitch Offset)
    # Bar A: Pure percussive pedal on the root note mimicking a kick drum breakdown
    pattern_bar_a = [
        (0.0, 0.5, 0),    # Beat 1 (legato impact)
        (0.75, 0.25, 0),  # Beat 1a (staccato)
        (1.0, 0.25, 0),   # Beat 2 (staccato)
        (1.25, 0.25, 0),  # Beat 2e (staccato)
        (1.5, 0.5, 0),    # Beat 2& (legato)
        (2.5, 0.25, 0),   # Beat 3& (staccato)
        (2.75, 0.25, 0),  # Beat 3a (staccato)
        (3.0, 0.5, 0),    # Beat 4 (legato)
    ]
    
    # Bar B: Same rhythm, but incorporates 12th fret (+12) and 3rd fret (+3) jumps 
    # to mirror a hypothetical guitar riff as advised in the tutorial
    pattern_bar_b = [
        (0.0, 0.5, 0),    # Beat 1
        (0.75, 0.25, 0),  # Beat 1a
        (1.0, 0.25, 12),  # Beat 2  -> OCTAVE JUMP
        (1.25, 0.25, 12), # Beat 2e -> OCTAVE JUMP
        (1.5, 0.5, 0),    # Beat 2&
        (2.5, 0.25, 3),   # Beat 3& -> MINOR 3RD JUMP
        (2.75, 0.25, 3),  # Beat 3a -> MINOR 3RD JUMP
        (3.0, 0.5, 0),    # Beat 4
    ]

    qn_per_bar = 4.0
    note_count = 0

    # === Step 4: Insert Notes ===
    for b in range(bars):
        bar_offset = b * qn_per_bar
        # Alternate between the pedal pattern and the jump pattern
        current_pattern = pattern_bar_a if b % 2 == 0 else pattern_bar_b
        
        for start_qn, len_qn, pitch_offset in current_pattern:
            # Convert Quarter Notes (Beats) to Seconds
            start_sec = ((start_qn + bar_offset) / bpm) * 60.0
            end_sec = ((start_qn + len_qn + bar_offset) / bpm) * 60.0
            
            # Convert Seconds to Project Pulse Quarter (PPQ) for ReaScript MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            note_pitch = base_midi_note + pitch_offset
            
            # Insert the note. Crucially, velocity is forced to `velocity_base` (110)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note_pitch), velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} bass notes over {bars} bars at {bpm} BPM (Velocity strictly at {velocity_base} to reduce harshness)."
```