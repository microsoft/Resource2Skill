### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Arrangement & Tension Building Scaffold

* **Core Musical Mechanism**: The tutorial demonstrates a **Subtractive Arrangement Strategy**. Rather than building a track from the ground up linearly, the producer starts with the climax of the track (the fully fleshed-out "Chorus" loop containing all drums, bass, and melodies) and duplicates it across the timeline. Other sections (Intro, Verse) are created by systematically *deleting* elements (e.g., muting the kick drum, removing the hi-hats, dropping the bass). Tension is then injected back into the arrangement using automation, specifically a rising low-pass filter sweep on the melodic elements, building energy right before the chorus drop.

* **Why Use This Skill (Rationale)**: 
  * **Groove Contrast**: Dropping the hi-hats and bass during the first half of a verse creates a sparse, empty feel. When the bass and hats return in the second half, the sudden density provides immediate forward momentum.
  * **Psychoacoustics & Tension**: A low-pass filter cuts out high frequencies, making the track sound "muffled" or distant. Slowly opening the filter introduces high-frequency energy, which human ears perceive as an approaching, escalating threat or excitement—the quintessential EDM/Hip-Hop "build-up."
  * **Workflow Efficiency**: Subtractive arrangement prevents "loopitis" (getting stuck in an 8-bar loop) by immediately forcing a full song structure onto the timeline.

* **Overall Applicability**: This arrangement scaffold is universal in modern music production, specifically in Hip-Hop, Trap, Pop, and EDM. It provides a foundational blueprint for pacing energy across a 2-to-3 minute track.

* **Value Addition**: Instead of generating a single isolated loop, this skill encodes macro-level song structure. It generates a 5-part arrangement (Intro -> Chorus -> Verse 1A -> Verse 1B Build -> Chorus 2) complete with energy drops, drum variation, and built-in automation sweeps.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 120 BPM (configurable).
  * **Grid & Pacing**: Sections are typically 4 or 8 bars long.
  * **Drum Variation**: 
    - *Chorus*: Full 4-on-the-floor or trap beat with continuous 8th-note hi-hats.
    - *Verse Drop*: The very first kick drum is muted to create a split-second pause (impact gap), and hats are entirely removed to halve the perceived energy.

* **Step B: Pitch & Harmony**
  * **Progression**: Uses a universal I - V - vi - IV (or i - v - VI - iv) progression mapped automatically to the user's chosen key and scale.
  * **Bass Interaction**: The bass mirrors the root notes but uses syncopation. It is completely muted during the first half of the verse to thin out the frequency spectrum.

* **Step C: Sound Design & FX**
  * **Filter Build**: A High Cut (Low-pass) filter is applied to the main melodic/chord bus. 
  * **ReaEQ**: Used natively by setting Band 4 (High Shelf) to a minimum gain (-24dB), effectively turning it into a low-pass filter.

* **Step D: Mix & Automation**
  * **Envelope Sweep**: The frequency of the filter is fully open (20kHz+) during the Intro and Chorus. At the start of the "Build" section (Verse 1B), it snaps down to ~200Hz, then sweeps up in a linear/parabolic curve to ~10kHz right before the next Chorus drops, instantly snapping back to fully open.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Song Structure** | Timeline / MIDI Items | Arranges items sequentially on the timeline to demonstrate macro-pacing (Intro -> Chorus -> Verse). |
| **Musical Content** | Computed MIDI notes | Computes scale-relative chords and syncopated bass to provide a functional musical bed. |
| **Synthesizers** | `ReaSynth` FX | Ensures the generated MIDI produces immediate, self-contained audio without relying on external VSTs. |
| **Tension Build** | `ReaEQ` + Envelope Automation | Automating an EQ frequency sweep natively recreates the tutorial's master bus filter transition. |

> **Feasibility Assessment**: 100% reproducible for the structural and automation concepts. Because the original tutorial relies on pre-rendered, proprietary samples (vocals, specific 808s, string libraries), this script generates native REAPER synthesizers and MIDI drum triggers as placeholders. The core lesson—subtractive arrangement and filter automation—is perfectly captured.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Structure",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Subtractive Arrangement Scaffold in the current REAPER project.
    Generates an Intro, Chorus, sparse Verse, building Verse, and second Chorus.
    Includes automated low-pass filter sweeps for tension.

    Args:
        bars: Defines the length of EACH structural section (e.g., bars=4 means a 20-bar total arrangement).
    """
    import reaper_python as RPR

    # --- Music Theory Lookups ---
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

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_pitch = NOTE_MAP.get(key, 0) + 36 # Start at Octave 2
    
    # Precompute 5 octaves of scale pitches to build chords safely
    scale_pitches = []
    for oct in range(5):
        for interval in scale_intervals:
            scale_pitches.append(base_pitch + (oct * 12) + interval)

    def build_diatonic_triad(degree, octave_offset=0):
        scale_len = len(scale_intervals)
        idx = degree + (octave_offset * scale_len)
        idx = min(idx, len(scale_pitches) - 5)
        return [scale_pitches[idx], scale_pitches[idx+2], scale_pitches[idx+4]]

    # --- Musical Pattern Generators ---
    def get_chords_pattern(num_bars):
        notes = []
        degrees = [0, 4, 5, 3] # Standard I-V-vi-IV (or relative minor equivalents)
        for b in range(num_bars):
            degree = degrees[b % len(degrees)]
            chord = build_diatonic_triad(degree, octave_offset=2) # Octave 4
            for pitch in chord:
                notes.append((pitch, b * 4, 4, int(velocity_base * 0.8)))
        return notes

    def get_bass_pattern(num_bars):
        notes = []
        degrees = [0, 4, 5, 3]
        for b in range(num_bars):
            degree = degrees[b % len(degrees)]
            pitch = scale_pitches[degree] # Octave 2
            # Syncopated groove
            notes.append((pitch, b*4 + 0, 1.5, velocity_base))
            notes.append((pitch, b*4 + 1.5, 0.5, velocity_base))
            notes.append((pitch, b*4 + 2, 2.0, velocity_base))
        return notes

    def get_drums_full(num_bars):
        notes = []
        for b in range(num_bars):
            # Kick (36)
            notes.append((36, b*4 + 0, 0.25, velocity_base))
            notes.append((36, b*4 + 1.5, 0.25, int(velocity_base * 0.8)))
            notes.append((36, b*4 + 2.5, 0.25, int(velocity_base * 0.8)))
            # Snare (38)
            notes.append((38, b*4 + 1, 0.25, velocity_base))
            notes.append((38, b*4 + 3, 0.25, velocity_base))
            # Hats (42) - continuous 8th notes
            for i in range(8):
                vel = int(velocity_base * 0.8) if i % 2 == 0 else int(velocity_base * 0.5)
                notes.append((42, b*4 + i*0.5, 0.125, vel))
        return notes

    def get_drums_sparse(num_bars):
        notes = []
        for b in range(num_bars):
            # Mute the very first kick drum for structural impact
            if b != 0:
                notes.append((36, b*4 + 0, 0.25, velocity_base))
                notes.append((36, b*4 + 1.5, 0.25, int(velocity_base * 0.8)))
                notes.append((36, b*4 + 2.5, 0.25, int(velocity_base * 0.8)))
            # Snare
            notes.append((38, b*4 + 1, 0.25, velocity_base))
            notes.append((38, b*4 + 3, 0.25, velocity_base))
            # No hi-hats
        return notes

    # --- Setup Project & Tracks ---
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beat_len = 60.0 / bpm
    bar_len = beat_len * 4

    def create_track_with_synth(name, is_drums=False):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        
        if not is_drums:
            fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            if name == "Bass":
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.0) # Square
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.6) # Triangle
            elif name == "Chords":
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 1, 0.5) # Saw
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 4, 0.8) # Attack
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 5, 0.7) # Release
        return track

    track_drums = create_track_with_synth("Drums", is_drums=True)
    track_bass = create_track_with_synth("Bass")
    track_chords = create_track_with_synth("Chords")

    def insert_midi(track, start_bar, num_bars, notes):
        if not notes: return
        start_time = (start_bar - 1) * bar_len
        length = num_bars * bar_len
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        RPR.RPR_SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0.0)
        
        for pitch, beat_offset, beat_dur, vel in notes:
            n_start = start_time + (beat_offset * beat_len)
            n_end = n_start + (beat_dur * beat_len)
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
        RPR.RPR_MIDI_Sort(take)

    # --- Timeline Arrangement ---
    section_len = max(1, bars) # e.g. 4 bars per section
    
    # 1. INTRO: Chords Only
    t_intro = 1
    insert_midi(track_chords, t_intro, section_len, get_chords_pattern(section_len))
    
    # 2. CHORUS 1: Full
    t_chorus1 = t_intro + section_len
    insert_midi(track_chords, t_chorus1, section_len, get_chords_pattern(section_len))
    insert_midi(track_bass, t_chorus1, section_len, get_bass_pattern(section_len))
    insert_midi(track_drums, t_chorus1, section_len, get_drums_full(section_len))
    
    # 3. VERSE 1A (Energy Drop): Chords + Sparse Drums (No Bass)
    t_verse_a = t_chorus1 + section_len
    insert_midi(track_chords, t_verse_a, section_len, get_chords_pattern(section_len))
    insert_midi(track_drums, t_verse_a, section_len, get_drums_sparse(section_len))
    
    # 4. VERSE 1B (Build): Full Arrangement returns
    t_verse_b = t_verse_a + section_len
    insert_midi(track_chords, t_verse_b, section_len, get_chords_pattern(section_len))
    insert_midi(track_bass, t_verse_b, section_len, get_bass_pattern(section_len))
    insert_midi(track_drums, t_verse_b, section_len, get_drums_full(section_len))
    
    # 5. CHORUS 2: Full
    t_chorus2 = t_verse_b + section_len
    insert_midi(track_chords, t_chorus2, section_len, get_chords_pattern(section_len))
    insert_midi(track_bass, t_chorus2, section_len, get_bass_pattern(section_len))
    insert_midi(track_drums, t_chorus2, section_len, get_drums_full(section_len))

    # --- Tension Building Automation (Filter Sweep) ---
    # Add ReaEQ to chords to act as a lowpass filter
    fx_idx = RPR.RPR_TrackFX_AddByName(track_chords, "ReaEQ", False, -1)
    
    # Param 10 is Band 4 Gain. Set to -24dB (Normalized 0.0)
    RPR.RPR_TrackFX_SetParamNormalized(track_chords, fx_idx, 10, 0.0)
    
    # Param 9 is Band 4 Frequency. We automate this.
    env = RPR.RPR_GetFXEnvelope(track_chords, fx_idx, 9, True)
    
    sweep_start_time = (t_verse_b - 1) * bar_len
    sweep_end_time = (t_chorus2 - 1) * bar_len
    
    # Keep open until Build section
    RPR.RPR_InsertEnvelopePoint(env, 0.0, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time - 0.001, 1.0, 0, 0, False, True)
    
    # Snap closed at start of Verse 1B (Tension starts)
    RPR.RPR_InsertEnvelopePoint(env, sweep_start_time, 0.2, 0, 0, False, True)
    
    # Sweep open smoothly up to ~10kHz at the drop
    RPR.RPR_InsertEnvelopePoint(env, sweep_end_time, 0.85, 0, 0, False, True)
    
    # Snap fully open precisely on the downbeat of Chorus 2
    RPR.RPR_InsertEnvelopePoint(env, sweep_end_time + 0.001, 1.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env)

    total_arranged_bars = section_len * 5
    return f"Created {total_arranged_bars}-bar Subtractive Arrangement Scaffold at {bpm} BPM in {key} {scale}."
```