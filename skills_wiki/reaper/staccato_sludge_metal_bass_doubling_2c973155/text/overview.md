### 1. High-level Design Pattern Extraction

> **Skill Name**: Staccato Sludge/Metal Bass Doubling

* **Core Musical Mechanism**: The video demonstrates extracting a staccato, syncopated metal guitar riff and converting it into a locked-in MIDI bassline. The core musical signature here is the **tight rhythmic doubling** of a distorted guitar. It utilizes rapid, muted staccato 16th/8th notes on a low pedal tone (root) interspersed with sustained syncopated accents (often jumping to the minor third or flat second) to create a heavy, driving "sludge" or "djent" feel.
* **Why Use This Skill (Rationale)**: In heavy music genres (Metal, Hardcore, Sludge, Djent), the bass guitar's primary role is to perfectly lock in with the kick drum and the rhythm guitar's right-hand picking pattern. This perfect rhythmic unison creates a psychoacoustic illusion of one massive, wide instrument rather than separate guitars and bass. The contrast between short, percussive muted notes and sustained power chords generates rhythmic tension and release.
* **Overall Applicability**: Essential for metal, hard rock, and heavy electronic music (like Synthwave or Doomcore) where a driving, percussive low-end foundation is required to match aggressive riffing.
* **Value Addition**: While the video relies on a premium third-party VST (Toontrack EZbass) to analyze an existing audio file, this skill encodes the *resulting musical theory* directly into a generative MIDI pattern. It provides a highly syncopated, genre-accurate heavy metal bass template that you can instantly drop into a session without needing to manually program the intricate staccato/legato timing changes.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: Typically 100 - 130 BPM (the video uses 122 BPM).
  - **Rhythmic Grid**: 16th note grid.
  - **Note Durations**: A heavy mix of short, staccato "chug" notes (representing palm mutes, ~0.25 beats) and longer sustained accents (~0.75 to 1.0 beats).
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Typically Minor or Phrygian (for that dark, heavy sound). 
  - **Voicing**: Single notes sitting exclusively in the lowest octave (MIDI octave 1 or 2). Heavy reliance on the Root pedal tone, with rhythmic jumps to the second and third scale degrees.
* **Step C: Sound Design & FX**
  - **Instrument**: A bass synthesizer (ReaSynth) utilizing a blend of Sawtooth (for aggressive midrange cut) and Sine (for sub-bass weight).
  - **FX Chain**: ReaEQ (cutting muddy low-mids, boosting presence around 1kHz) and compression to keep the staccato notes punchy and uniform.
* **Step D: Mix & Automation**
  - Centered panning, high velocity (100-127) for sustained notes to simulate hard string plucks, and slightly lower velocity (85-95) for the rapid staccato notes to simulate palm-muting.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Audio-to-MIDI Emulation** | MIDI note insertion | Standard REAPER cannot natively perform complex polyphonic audio-to-MIDI analysis without 3rd-party tools. To follow safety constraints, we synthesize the *resulting* metal bass pattern directly via MIDI. |
| **Rhythmic Syncopation** | Time-calculated PPQ insertion | Allows for exact replication of the staccato/legato rhythmic contrast (16th note "chugs" vs sustained accents) shown in the EZbass piano roll. |
| **Heavy Bass Tone** | FX Chain (ReaSynth + ReaComp + ReaEQ) | Emulates the grit, sub-weight, and aggressive attack of a metal bass DI using only REAPER stock plugins. |

> **Feasibility Assessment**: 80%. This script faithfully recreates the tightly quantized, syncopated metal MIDI bassline and a stock synthesizer proxy tone. It does *not* reproduce the actual audio-analysis step (which requires the Toontrack EZbass VST or an external audio file as shown in the video), complying with the constraint to avoid external dependencies or unavailable audio source files.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Sludge Metal Bass",
    bpm: int = 122,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 115,
    **kwargs,
) -> str:
    """
    Create a tight, syncopated Sludge/Metal MIDI bassline in the current REAPER project.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (122 matches the tutorial).
        key: Root note (e.g., E is standard for metal).
        scale: Scale type (minor or phrygian recommended).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for aggressive playing.
    
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "phrygian":         [0, 1, 3, 5, 7, 8, 10], # Added for metal authenticity
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Fallback to minor if scale is not found
    if scale not in SCALES:
        scale = "minor"
    
    scale_intervals = SCALES[scale]
    
    # Calculate base octave for metal bass (usually octave 1, MIDI notes 24-35)
    root_midi = NOTE_MAP.get(key, 4) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Define a syncopated sludge/metal rhythmic pattern (positions in beats)
    # Tuple: (beat_start, length_in_beats, scale_degree_idx, is_staccato)
    riff_pattern = [
        (0.00, 0.75, 0, False), # Sustained downbeat root
        (1.00, 0.25, 0, True),  # Staccato 16th chug
        (1.50, 0.25, 0, True),  # Staccato 16th chug
        (2.00, 0.50, 2, False), # Syncopated jump to 3rd degree
        (2.50, 0.50, 1, False), # Syncopated jump to 2nd degree
        (3.00, 0.25, 0, True),  # Machine-gun 16ths...
        (3.25, 0.25, 0, True),
        (3.50, 0.25, 0, True),
        (3.75, 0.25, 0, True)
    ]

    # === Step 4: Insert MIDI Notes ===
    total_notes = 0
    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        for beat_start, length, degree_idx, is_staccato in riff_pattern:
            # Calculate pitch
            # Handle out-of-bounds scale degrees safely
            degree = scale_intervals[degree_idx % len(scale_intervals)]
            pitch = root_midi + degree
            
            # Dynamic velocity based on playing style
            vel = int(velocity_base * 0.85) if is_staccato else velocity_base
            vel = max(1, min(127, vel))
            
            # Calculate timing
            start_sec = (bar_offset_beats + beat_start) * beat_sec
            end_sec = start_sec + (length * beat_sec)
            
            # Add slight gap for staccato "palm mute" feel
            if is_staccato:
                end_sec -= (0.05 * beat_sec) 
                
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            total_notes += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain (Stock Heavy Bass Synth) ===
    # 1. ReaSynth for the raw oscillator
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)  # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 1.0)  # Sawtooth mix (aggressive)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.8)  # Extra sine (sub bass)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.4)  # Filter cutoff (tame the extreme highs)

    # 2. ReaEQ to shape the tone (cut mud, boost attack)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 2: Cut mud at ~250Hz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 3, 250.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 4, -4.0)  # Gain
    # Band 3: Boost pick attack / string grind at ~1.5kHz
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 6, 1500.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 7, 5.0)    # Gain

    # 3. ReaComp to squash and limit (even out the staccato vs legato notes)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 0, -18.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 1, 6.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 2, 5.0)   # Attack (ms)
    RPR.RPR_TrackFX_SetParam(track, comp_idx, 3, 50.0)  # Release (ms)

    return f"Created '{track_name}' with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}"
```