# Salience-Aware Complementary Bassline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Salience-Aware Complementary Bassline

* **Core Musical Mechanism**: The defining technique of this pattern is **Auditory Salience Balancing**. It creates a call-and-response relationship in rhythmic density between a sample/melody and the bassline. When the main sample is "busy" (high movement), the bass provides a sparse, sustained, or simple foundational root. When the main sample "breathes" (low movement, typically at the end of a phrase), the bass line injects complex, transient, pentatonic fills to maintain momentum.
* **Why Use This Skill (Rationale)**: The human ear prioritizes movement (auditory salience). If all instruments play complex rhythms simultaneously, it causes cognitive overload and frequency masking (mud). If all instruments play sustained notes, the track lacks groove. By actively contrasting the bassline's rhythmic complexity against the sample's, you create a "pocket." Furthermore, selecting a transient (plucky) bass shape over a sustained one leaves "open space" in the mix, reducing low-end rumble while retaining punch.
* **Overall Applicability**: Essential for Hip-Hop, R&B, Lo-Fi, and House production where you are working with an existing melodic loop or sample. It bridges the gap between a generic "808 on the downbeat" and a professional, grooving bassline that interacts dynamically with the track.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes three expert-level rules: (1) Synthesizer ADSR shaping for transient vs. sustained bass, (2) Foundational chord-root tracing, and (3) Syncopated phrase-end fills using pentatonic passing notes.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 80-120 BPM (highly versatile).
  - **Grid**: Foundational notes land strictly on downbeats (1.1, 3.1). Fills are strictly quantized to 16th notes (1/16) at the end of 2-bar or 4-bar phrases.
  - **Duration**: Core notes are either staccato (if transient) or legato (if sustained). Fills are highly staccato (short gates) to ensure clarity and punch.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Adheres to the defined key/scale (e.g., C Minor).
  - **Foundation**: Traces the root notes of a standard 4-bar progression (e.g., i - VI - III - VII).
  - **Movement (Fills)**: Uses the minor or major pentatonic scale to walk down or jump octaves at phrase boundaries. The pentatonic scale is used because it lacks the dissonant tritone intervals of diatonic scales, making it harmonically "safe" for rapid bass runs.

* **Step C: Sound Design & FX**
  - **Instrument**: Simple sine/triangle oscillator (ReaSynth).
  - **Envelope**: Plucky/Transient (Attack = 0ms, Decay = 200ms, Sustain = low, Release = 100ms) to leave space between notes, preventing bass pile-up.
  - **Timbre (Color)**: Low harmonic content. Using a triangle/sine wave inherently reduces upper harmonic "color," ensuring the bass doesn't clash with the mid-range of complex samples.

* **Step D: Mix & Automation**
  - Velocities are varied: Downbeats hit at maximum impact (110-120), while 16th-note fills use lower, varying velocities (80-100) to simulate ghost notes and realistic playing dynamics.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Bass Envelope (Transient vs Sustained) | FX Chain (ReaSynth ADSR manipulation) | ReaSynth's parameters allow direct manipulation of the ADSR envelope to fulfill Step 1 of the video's framework ("Choose your bass shape"). |
| Foundational Bassline | MIDI note insertion (Downbeats) | Computes the root of the scale/chord progression and drops it on the 1 of every bar, fulfilling Step 2 ("Build a foundational bassline"). |
| Movement / Auditory Salience | MIDI note insertion (16th-note Fills) | Injects rapid pentatonic MIDI runs exclusively at the end of bars 2 and 4, fulfilling Step 3 ("Add movement where there is space"). |

> **Feasibility Assessment**: 90% — The script successfully encodes the 3-step framework into an intelligent generative pattern. While it cannot *literally* listen to an external audio sample to find empty space, it uses the standard production convention of phrase-end turnarounds (beats 3 and 4 of even bars) to place the complex movement, accurately mirroring the video's musical outcome.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Salience Bass",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 'Salience-Aware Complementary Bassline' in REAPER.
    Follows the 3-step framework:
    1. Shape the bass (Transient/Plucky ADSR via ReaSynth)
    2. Foundational Bassline (Roots on downbeats)
    3. Add Movement (Pentatonic 16th note fills at phrase ends)
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    PENTATONIC = {
        "major": [0, 2, 4, 7, 9],
        "minor": [0, 3, 5, 7, 10],
    }
    
    # Select scale arrays
    is_minor = "minor" in scale.lower()
    scale_intervals = SCALES["minor"] if is_minor else SCALES["major"]
    pent_intervals = PENTATONIC["minor"] if is_minor else PENTATONIC["major"]
    
    # Generic standard progression degrees (0-indexed)
    # Minor: i - VI - III - VII | Major: I - vi - IV - V
    progression = [0, 5, 2, 6] if is_minor else [0, 5, 3, 4]
    
    # Base octave for sub bass (C2 = MIDI note 36)
    root_midi = 36 + NOTE_MAP.get(key.capitalize(), 0)

    # === Step 1: Setup REAPER Environment & Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Instrument & Sound Design (Step 1 of Framework) ===
    # Add ReaSynth
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Configure for a "Transient/Plucky" shape (Less color, fast decay)
    # Param 1: Attack (0ms)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.0)
    # Param 2: Decay (fast)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.05)
    # Param 3: Sustain (low volume)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.2)
    # Param 4: Release (short)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.05)
    # Param 6: Square mix (0% for less upper harmonic "color")
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)
    # Param 7: Saw mix (0% for less color)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.0)
    # Param 8: Triangle mix (100% for smooth sub tone)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 1.0)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Helper function to add notes
    def add_note(start_sec, length_sec, pitch, velocity):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec + length_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(velocity), False)

    beat_len = 60.0 / bpm
    sixteenth_len = beat_len / 4.0

    note_count = 0

    # === Step 4: Generate MIDI (Steps 2 & 3 of Framework) ===
    for b in range(bars):
        bar_start = b * bar_length_sec
        degree = progression[b % len(progression)]
        chord_root_pitch = root_midi + scale_intervals[degree]
        
        # Adjust if pitch jumps too high, keep it subby
        if chord_root_pitch > 45: 
            chord_root_pitch -= 12

        # Step 2: Build a Foundational Bassline (Root on Beat 1)
        # We make it 1 beat long to simulate the transient open space
        add_note(bar_start, beat_len * 1.5, chord_root_pitch, velocity_base)
        note_count += 1

        # Step 3: Add Movement (Auditory Salience)
        # Add complex movement during the "empty space" (end of 2nd and 4th bars)
        if b % 2 == 1: 
            # We are in an even bar (b=1 is bar 2, b=3 is bar 4). Add fill on Beat 4.
            fill_start = bar_start + (beat_len * 3) # Starts exactly on beat 4
            
            # Pentatonic 16th note descending run
            # Note 1: Octave up (syncopated)
            add_note(fill_start, sixteenth_len * 0.8, chord_root_pitch + 12, velocity_base - 10)
            
            # Note 2: Pentatonic 4th degree (down 1 scale step from top)
            p_idx = 3 # 4th pentatonic note
            fill_pitch_2 = root_midi + pent_intervals[p_idx]
            if fill_pitch_2 < chord_root_pitch + 12: # Keep it relevant to current chord
                 fill_pitch_2 = chord_root_pitch + 12 - (SCALES["major"][1] if not is_minor else 2) # rough diatonic step down
            add_note(fill_start + sixteenth_len, sixteenth_len * 0.8, fill_pitch_2, velocity_base - 20)
            
            # Note 3: Pentatonic 3rd degree
            fill_pitch_3 = chord_root_pitch + pent_intervals[2]
            add_note(fill_start + (sixteenth_len * 2), sixteenth_len * 0.8, fill_pitch_3, velocity_base - 15)
            
            # Note 4: Back to root, leading into next bar
            add_note(fill_start + (sixteenth_len * 3), sixteenth_len * 0.8, chord_root_pitch, velocity_base - 5)
            
            note_count += 4
        else:
            # Odd bar (b=0 is bar 1, b=2 is bar 3). Keep it simple, just add an 8th note pickup on beat 4.5
            pickup_start = bar_start + (beat_len * 3.5)
            add_note(pickup_start, sixteenth_len * 1.5, chord_root_pitch, velocity_base - 15)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} dynamic bass notes over {bars} bars at {bpm} BPM. Plucky shape applied for frequency clarity."
```