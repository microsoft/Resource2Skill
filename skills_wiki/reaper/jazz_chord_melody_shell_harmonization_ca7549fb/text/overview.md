# Jazz Chord-Melody Shell Harmonization

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Jazz Chord-Melody Shell Harmonization

* **Core Musical Mechanism**: The tutorial demonstrates the core technique of "Chord Melody" playing: combining a single-note melody with independent chordal accompaniment on a single instrument. The most foundational approach shown is **Shell Voicing Harmonization**. Instead of playing full, clunky 5- or 6-note chords, the pattern isolates the melody on the top strings, grounds it with the root note in the bass, and uses "guide tones" (the 3rd and 7th) in the middle register to outline the harmony with minimal clutter and smooth voice leading.
* **Why Use This Skill (Rationale)**: Musically, playing full chords under an active melody creates frequency masking and physical clumsiness. By utilizing 3-note shell voicings (Root + 3rd + 7th), you provide the complete harmonic identity of a jazz chord without stepping on the melody. Furthermore, holding the chord tones as sustained layers while the melody moves rhythmically creates the "illusion" of two separate musicians playing together (as referenced by Joe Pass in the video).
* **Overall Applicability**: This technique is essential for jazz guitar and piano, Neo-Soul, lo-fi hip-hop, and R&B. It's particularly useful when arranging a solo instrument piece or when composing a dense track where the harmonic instrument needs to leave space in the mix.
* **Value Addition**: A blank MIDI clip has no concept of voice leading. This skill encodes standard jazz voice leading principles (where the 7th of a minor chord falls by a half-step to become the 3rd of a dominant chord) directly into the MIDI generation, ensuring the resulting chords sound professional, smooth, and inherently "jazzy."

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / Tempo**: 4/4 time, typically at a relaxed 80-110 BPM.
  - **Grid / Duration**: The bass and guide tones are played as sustained chords (lasting 4 quarter notes) on the downbeat. The melody is played over them using syncopated rhythms (a mix of dotted-quarters and eighths) to create independence.
* **Step B: Pitch & Harmony**
  - **Progression**: The pattern employs a classic Jazz ii-V-I-VI turnaround, which is fully transposable based on the chosen key. 
  - **Voicings**: 
    - **ii7**: Root, minor 3rd, minor 7th.
    - **V7**: Root, minor 7th, major 3rd.
    - **Imaj7**: Root, major 3rd, major 7th.
    - **VI7**: Root, minor 7th, major 3rd.
  - **Voice Leading**: The inner voices explicitly follow smooth step-wise motion (e.g., the minor 7th of the ii7 drops down a half-step to become the major 3rd of the V7).
* **Step C: Sound Design & FX**
  - **Instrument**: A warm, hollow electric piano or jazz guitar tone. In stock REAPER, this is approximated using `ReaSynth` by mixing out the harsh Sawtooth wave, turning up the Square/Pulse wave, and adding a soft release.
* **Step D: Mix & Automation**
  - Velocity is scaled: the melody is emphasized (vel ~95), while the underlying shell chords are played softer (vel ~75-80) so they don't overpower the lead line.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Voicings & Voice Leading | MIDI Note Insertion | Allows exact calculation of intervals, inversions, and voice-leading drops (e.g., resolving the 7th to the 3rd). |
| Melody-Chord Independence | MIDI Length / Timing | Placing sustained whole-notes for chords alongside syncopated 1.5-beat melody notes within the same item mimics the solo-guitarist illusion. |
| Jazz Tone | ReaSynth FX | Tweaking stock ReaSynth parameters to a soft pulse-wave provides a reliable "mellow" tone without needing external VSTs. |

> **Feasibility Assessment**: 100% reproducible for the theoretical concept. While the specific timbre of the presenter's Gibson ES-335 requires physical acoustic properties and specific amp sims, the *compositional mechanism* (shell voicings under an active melody) is completely encoded and playable natively in REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Jazz_Chord_Melody",
    track_name: str = "Chord Melody Guitar",
    bpm: int = 90,
    key: str = "C",
    scale: str = "major",  # The script adapts a jazz ii-V-I-VI regardless of scale input
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Jazz Chord-Melody arrangement utilizing Shell Voicings.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B) for the I chord.
        scale: Ignored functionally, context is a jazz turnaround.
        bars: Number of bars to generate (will loop the 4-bar turnaround).
        velocity_base: Base MIDI velocity (0-127).
        
    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    if key not in NOTE_MAP:
        key = "C"

    # Define base octave (C2 = 36)
    root_midi = 36 + NOTE_MAP[key]

    # Structure: List of tuples -> (beat_start, beat_end, pitch_offset, velocity)
    # Pitch offsets are relative to the I chord root_midi.
    # This precisely encodes the ii-V-I-VI turnaround with proper voice leading.
    progression_data = []

    # Bar 1: ii7 chord
    b_offset = 0
    # Shell: Root(+2), m3(+17), m7(+24)
    progression_data.extend([
        (b_offset+0.0, b_offset+4.0, 2, velocity_base - 5),
        (b_offset+0.0, b_offset+4.0, 17, velocity_base - 10),
        (b_offset+0.0, b_offset+4.0, 24, velocity_base - 10),
    ])
    # Melody
    progression_data.extend([
        (b_offset+0.0, b_offset+1.5, 29, velocity_base + 10),
        (b_offset+1.5, b_offset+2.0, 28, velocity_base),
        (b_offset+2.0, b_offset+4.0, 26, velocity_base + 5),
    ])

    # Bar 2: V7 chord
    b_offset = 4
    # Shell: Root(+7), m7(+17), M3(+23) -- Note: the 24 from ii7 resolves smoothly down to 23
    progression_data.extend([
        (b_offset+0.0, b_offset+4.0, 7, velocity_base - 5),
        (b_offset+0.0, b_offset+4.0, 17, velocity_base - 10),
        (b_offset+0.0, b_offset+4.0, 23, velocity_base - 10),
    ])
    # Melody
    progression_data.extend([
        (b_offset+0.0, b_offset+1.5, 28, velocity_base + 10),
        (b_offset+1.5, b_offset+2.0, 26, velocity_base),
        (b_offset+2.0, b_offset+4.0, 24, velocity_base + 5),
    ])

    # Bar 3: Imaj7 chord
    b_offset = 8
    # Shell: Root(+12), M3(+16), M7(+23) -- Note: the 17 from V7 resolves smoothly down to 16
    progression_data.extend([
        (b_offset+0.0, b_offset+4.0, 12, velocity_base - 5),
        (b_offset+0.0, b_offset+4.0, 16, velocity_base - 10),
        (b_offset+0.0, b_offset+4.0, 23, velocity_base - 10),
    ])
    # Melody
    progression_data.extend([
        (b_offset+0.0, b_offset+1.5, 26, velocity_base + 10),
        (b_offset+1.5, b_offset+2.0, 28, velocity_base),
        (b_offset+2.0, b_offset+4.0, 31, velocity_base + 5),
    ])

    # Bar 4: VI7 chord (Turnaround)
    b_offset = 12
    # Shell: Root(+9), m7(+19), M3(+25)
    progression_data.extend([
        (b_offset+0.0, b_offset+4.0, 9, velocity_base - 5),
        (b_offset+0.0, b_offset+4.0, 19, velocity_base - 10),
        (b_offset+0.0, b_offset+4.0, 25, velocity_base - 10),
    ])
    # Melody
    progression_data.extend([
        (b_offset+0.0, b_offset+1.5, 28, velocity_base + 10),
        (b_offset+1.5, b_offset+2.0, 25, velocity_base),
        (b_offset+2.0, b_offset+4.0, 26, velocity_base + 5),
    ])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    total_beats = bars * beats_per_bar
    item_length_sec = (total_beats * 60.0) / bpm
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes ===
    total_notes_added = 0
    
    for bar in range(bars):
        pattern_bar = bar % 4
        bar_beat_start = bar * 4
        
        # Filter notes for the current pattern bar
        for b_start, b_end, pitch_offset, vel in progression_data:
            if b_start >= (pattern_bar * 4) and b_start < ((pattern_bar + 1) * 4):
                # Adjust to the actual timeline position
                actual_b_start = bar_beat_start + (b_start % 4)
                actual_b_end = bar_beat_start + (b_end - (pattern_bar * 4))
                
                # Calculate absolute time
                start_time = (actual_b_start * 60.0) / bpm
                end_time = (actual_b_end * 60.0) / bpm
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                pitch = root_midi + pitch_offset
                
                # Clamp velocity & pitch
                pitch = max(0, min(127, pitch))
                vel = max(1, min(127, int(vel)))
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Instrument FX (Mellow Jazz Tone) ===
    # Using stock ReaSynth tweaked for a mellow, dark electric guitar/piano sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 0: Volume, 1: Saw, 2: Square, 3: Triangle, 4: Release, 5: Extra Sine
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)  # Remove harsh sawtooth
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)  # Add warm square/pulse
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)  # Slight triangle for body
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.7)  # Generous release (simulates string sustain)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.5)  # Add extra sine for fundamental depth

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars (ii-V-I-VI Chord Melody in {key}) at {bpm} BPM."
```