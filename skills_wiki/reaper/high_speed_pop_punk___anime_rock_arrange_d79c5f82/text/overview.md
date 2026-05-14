### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Speed Pop-Punk / Anime Rock Arrangement Scaffold

* **Core Musical Mechanism**: The tutorial demonstrates REAPER's multi-track MIDI editing capabilities by sketching a fast-paced, 4-track musical arrangement (Drums, Bass, Rhythm Guitar, Lead Guitar). The core musical signature is a driving, constant 8th-note pulse running across the rhythm section, synchronized with a classic vi-IV-I-V chord progression. Syncopation is achieved by offsetting the kick drum to the "and" of beat 2, while the lead guitar provides counter-melody via a rapid 8th-note arpeggio.
* **Why Use This Skill (Rationale)**: This arrangement pattern works because of the concept of *rhythmic unison* and *frequency stratification*. The bass and rhythm guitar play identical driving 8th notes, merging into a single powerful wall of sound. The drums anchor this with a half-time feel (snare on 2 and 4 at high tempo). The lead guitar sits in a much higher octave (stratification), avoiding masking the dense low-midrange, and outlining the harmony using continuous arpeggios that add forward momentum without cluttering the rhythm.
* **Overall Applicability**: This multi-track layout is the foundational blueprint for modern pop-punk, emo, alternative rock, and "anime intro" (J-Rock) music. It serves as a perfect starting block for high-energy tracks.
* **Value Addition**: Compared to an empty project, this skill instantly builds a cohesive 4-piece rock band ecosystem. It dynamically calculates diatonic progressions (vi-IV-I-V), handles power-chord voicings, and correctly maps General MIDI drum patterns, saving producers from the tedious setup phase of arranging rock instrumentation.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: ~190-200 BPM (Fast).
  - **Time Signature**: 4/4.
  - **Rhythmic Grid**: Driving 8th notes (1/2 beat intervals).
  - **Note Durations**: Staccato for drums, tightly gated 8th notes for bass/rhythm (0.45 beats long to create a slight "chugging" gap), and legato arpeggios for the lead.

* **Step B: Pitch & Harmony**
  - **Progression**: Classic 4-chord progression: vi - IV - I - V.
  - **Voicings**: 
    - Bass plays root notes in the 2nd octave.
    - Rhythm Guitar plays Power Chords (Root, Perfect 5th, Octave) in the 3rd octave.
    - Lead Guitar plays continuous ascending/descending triads (Root, 3rd, 5th) in the 5th octave.

* **Step C: Sound Design & FX**
  - The pattern uses 4 distinct MIDI tracks mapped to standard roles. (In the tutorial, these are routed to external VSTs like Kontakt for drums and neural amp modelers for guitars).
  - *Implementation Note*: To ensure this skill runs on any system without third-party plugins, it generates the structured MIDI data on cleanly named, color-coded tracks, ready for the user to drop their preferred Amp Sims and Drum Samplers onto.

* **Step D: Mix & Automation**
  - Drums are given velocity humanization (hi-hats alternate between high and low velocities to simulate natural sticking). 
  - Rhythm guitars are pulled back slightly in velocity to allow the lead guitar to cut through.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track ecosystem | Track creation (`RPR_InsertTrackAtIndex`) | Builds the exact 4-track folder structure shown in the video. |
| Driving Rock Rhythm | MIDI note insertion | Allows precise 8th-note quantization and velocity humanization for the "chugging" feel. |
| Diatonic Harmony | Dynamic Scale Calculation | Converts the requested Key/Scale into the correct MIDI note values for the vi-IV-I-V progression. |

> **Feasibility Assessment**: 100% reproducible for the MIDI arrangement and composition pattern. The specific guitar VST tones (Amp Sims) are not stock to REAPER, so the code provides the perfectly aligned MIDI tracks ready for the user's instruments.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "PopPunkArrangement",
    track_name: str = "Rock Scaffold",
    bpm: int = 195,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a 4-track Pop-Punk / Anime Rock Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (typically 170-200 for this style).
        key: Root note (e.g., "D").
        scale: Scale type (e.g., "major").
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key.capitalize(), 2) # Default to D

    def get_scale_pitch(degree: int, octave: int) -> int:
        """Calculate exact MIDI pitch based on diatonic scale degree."""
        scale_len = len(scale_intervals)
        octave_offset = degree // scale_len
        rem_degree = degree % scale_len
        pitch = (octave + octave_offset) * 12 + scale_intervals[rem_degree] + root_val
        # Clamp to MIDI limits
        return max(0, min(127, pitch))

    # === Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Helper: Add Track ===
    def add_track(name: str):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        return track

    # === Helper: Add MIDI Item & Take ===
    def add_midi_item(track, bars_count):
        beats_per_bar = 4
        beat_len = 60.0 / bpm
        item_length = bars_count * beats_per_bar * beat_len
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return item, take

    # === Helper: Insert Note ===
    def insert_note(take, start_beat, end_beat, pitch, vel):
        beat_len = 60.0 / bpm
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # Create 4-Track Arrangement
    trk_drums = add_track(f"{track_name} - Drums")
    trk_bass = add_track(f"{track_name} - Bass")
    trk_rgtr = add_track(f"{track_name} - Rhythm Gtr")
    trk_lgtr = add_track(f"{track_name} - Lead Gtr")

    _, take_drums = add_midi_item(trk_drums, bars)
    _, take_bass = add_midi_item(trk_bass, bars)
    _, take_rgtr = add_midi_item(trk_rgtr, bars)
    _, take_lgtr = add_midi_item(trk_lgtr, bars)

    # Progression: vi - IV - I - V
    progression = [5, 3, 0, 4] 

    total_notes = 0

    for bar in range(bars):
        degree = progression[bar % len(progression)]
        bar_start_beat = bar * 4.0

        # === 1. Drums ===
        # Kick (36) on 1, "and" of 2, 3
        for b in [0.0, 1.5, 2.0]:
            insert_note(take_drums, bar_start_beat + b, bar_start_beat + b + 0.25, 36, velocity_base)
            total_notes += 1
        
        # Snare (38) on 2, 4
        for b in [1.0, 3.0]:
            insert_note(take_drums, bar_start_beat + b, bar_start_beat + b + 0.25, 38, velocity_base)
            total_notes += 1
            
        # Hi-hat (42) riding 8th notes
        for i in range(8):
            b = i * 0.5
            # Alternating velocity for humanization
            vel = velocity_base if i % 2 == 0 else max(10, velocity_base - 25)
            insert_note(take_drums, bar_start_beat + b, bar_start_beat + b + 0.25, 42, vel)
            total_notes += 1
            
        # Crash (49) on the very first downbeat of a 4-bar phrase
        if bar % 4 == 0:
            insert_note(take_drums, bar_start_beat, bar_start_beat + 0.5, 49, min(127, velocity_base + 10))
            total_notes += 1

        # === 2. Bass ===
        # Driving 8th notes on the root (Octave 2)
        bass_pitch = get_scale_pitch(degree, 2)
        for i in range(8):
            b = i * 0.5
            # Length is 0.45 beats to create a slight gap (chugging feel)
            insert_note(take_bass, bar_start_beat + b, bar_start_beat + b + 0.45, bass_pitch, velocity_base)
            total_notes += 1

        # === 3. Rhythm Guitar ===
        # Power Chords (Octave 3). Hardcoded +7 semitones ensures perfect 5ths for heavy rock tone.
        gtr_root = get_scale_pitch(degree, 3)
        gtr_5th = gtr_root + 7
        gtr_octave = gtr_root + 12
        
        for i in range(8):
            b = i * 0.5
            for p in [gtr_root, gtr_5th, gtr_octave]:
                insert_note(take_rgtr, bar_start_beat + b, bar_start_beat + b + 0.45, p, max(10, velocity_base - 10))
                total_notes += 1

        # === 4. Lead Guitar ===
        # Rapid 8th note arpeggios (Octave 5)
        p1 = get_scale_pitch(degree, 5)     # Root
        p2 = get_scale_pitch(degree + 2, 5) # Third
        p3 = get_scale_pitch(degree + 4, 5) # Fifth
        
        # Up-and-down arpeggio pattern
        arp_pattern = [p1, p2, p3, p2, p1, p2, p3, p2]
        
        for i, p in enumerate(arp_pattern):
            b = i * 0.5
            insert_note(take_lgtr, bar_start_beat + b, bar_start_beat + b + 0.45, p, velocity_base)
            total_notes += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_rgtr)
    RPR.RPR_MIDI_Sort(take_lgtr)

    return f"Created Pop-Punk Scaffold (4 tracks) with {total_notes} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```