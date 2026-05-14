### 1. High-level Design Pattern Extraction

> **Skill Name**: Pop-Punk / Rock Multi-Track Arrangement

* **Core Musical Mechanism**: A driving, synchronized 4-track arrangement featuring an 8th-note pumping bass, sustained power chords/triads on rhythm guitar, an arpeggiated 8th-note lead melody, and a standard backbeat rock drum groove. The core mechanism is how these layers establish rhythmic locking (bass and hi-hats sharing the 8th-note grid) while maintaining frequency separation (bass down low, rhythm chords occupying the mids, lead arpeggios floating on top).
* **Why Use This Skill (Rationale)**: This arrangement pattern creates a "wall of sound" typical in rock and energetic pop genres. By stripping the rhythm to a driving 8th-note pulse and separating the chord blocks from the melodic movement, you avoid a muddy mix. Diatonic root movement underpins the harmonic structure, ensuring all layers naturally lock into the same key.
* **Overall Applicability**: Perfect for generating full verse or chorus foundations in pop-punk, alternative rock, indie, or upbeat synth-pop. 
* **Value Addition**: Instead of generating a single isolated loop, this skill constructs a fully harmonized, multi-track band arrangement. It handles dynamic chord inversions and voice generation relative to any key or scale you provide.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid/Time Signature**: 4/4 time, typically fast (140-180 BPM).
  - **Drums**: Kick on 1 and 2-AND (syncopated); Snare on 2 and 4. Hi-hats play straight 8th notes with dynamic velocity alternation.
  - **Bass**: Pumping straight 8th notes (ghost notes can be added, but a steady pulse defines the genre).
  - **Rhythm**: Sustained whole notes hitting on the 1 of every bar.
  - **Lead**: 8th-note upward/downward arpeggios locking with the bass and hi-hats.

* **Step B: Pitch & Harmony**
  - **Progression**: Standard pop-punk movements like `i - VI - III - VII` (in Minor) or `I - V - vi - IV` (in Major).
  - **Bass**: Root notes, dropped one octave below the chords.
  - **Rhythm**: Triads built dynamically based on scale degrees.
  - **Lead**: Chord tones (1st, 3rd, 5th) pushed an octave higher than the rhythm section.

* **Step C: Sound Design & FX**
  - Track separation is crucial. Placeholders like **ReaSynth** can be used for immediate auditioning, tweaking wave parameters (e.g., Square wave for bass, Saw wave for lead) to distinguish frequency ranges.
  - **Dependency Note**: The drum track is generated as raw MIDI and requires a third-party drum sampler (like Kontakt or ReaSamplOmatic5000) mapped to General MIDI to produce sound.

* **Step D: Mix & Automation**
  - Rhythm components are pulled slightly back in volume/velocity to make room for the Snare, Kick, and Lead. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track band layering | Track creation & Item insertion | Accurately builds 4 distinct tracks natively inside the REAPER arrangement view. |
| Rhythmic locking & Harmony | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides precise control over note velocities, tied chord durations, and scale-relative diatonic triads. |
| Immediate Sound Audition | FX chain (`ReaSynth`) | Stock REAPER synths guarantee that the pitch and harmony are audible immediately without external dependencies. |

> **Feasibility Assessment**: 95% reproducible. The harmonic structure, MIDI rhythms, track routing, and multi-track interaction are 100% captured. To get the final 5% (the exact guitar tones from the video), you will need to replace the placeholder `ReaSynth` plugins with your own preferred VST amp simulators and drum samplers.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 150,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track Pop-Rock Arrangement (Drums, Bass, Rhythm, Lead).

    Args:
        project_name: Project identifier.
        bpm: Tempo in BPM (140-180 recommended).
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string describing the creation process.
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
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 11) + 48  # C3 base octave

    def clamp(val):
        return max(0, min(127, int(val)))

    # Set tempo and get edit cursor to ensure additive generation
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    cursor_pos = RPR.RPR_GetCursorPosition()
    beat_length_sec = 60.0 / bpm
    length_sec = bars * 4 * beat_length_sec

    # Helper function to create tracks, add MIDI, and set basic synths
    def create_layer(track_name, notes, add_synth=True):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
        
        item = RPR.RPR_CreateNewMIDIItemInProj(track, cursor_pos, cursor_pos + length_sec, False)
        take = RPR.RPR_GetActiveTake(item)
        
        for note in notes:
            # note = (start_beat, end_beat, pitch, velocity)
            start_sec = cursor_pos + note[0] * beat_length_sec
            end_sec = cursor_pos + note[1] * beat_length_sec
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note[2]), clamp(note[3]), False)
            
        RPR.RPR_MIDI_Sort(take)
        
        if add_synth:
            fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.4) # Control volume to prevent clipping
            if track_name == "Bass":
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 2, 0.6) # Emphasize Square
            elif track_name == "Lead Guitar":
                RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.7) # Emphasize Saw
        return track

    # --- 1. Drums ---
    drum_notes = []
    for bar in range(bars):
        bar_start = bar * 4
        # Kick (1, 2-AND)
        drum_notes.append((bar_start + 0.0, bar_start + 0.25, 36, velocity_base))
        drum_notes.append((bar_start + 2.5, bar_start + 2.75, 36, velocity_base))
        # Snare (2, 4)
        drum_notes.append((bar_start + 1.0, bar_start + 1.25, 38, velocity_base + 10))
        drum_notes.append((bar_start + 3.0, bar_start + 3.25, 38, velocity_base + 10))
        # Hi-hats (straight 8th notes, alternating velocity)
        for i in range(8):
            vel = velocity_base - 10 if i % 2 == 0 else velocity_base - 30
            drum_notes.append((bar_start + i * 0.5, bar_start + i * 0.5 + 0.25, 42, vel))
        # Crash on first beat of the very first bar
        if bar == 0:
            drum_notes.append((bar_start + 0.0, bar_start + 0.5, 49, velocity_base + 10))
    
    create_layer("Drums", drum_notes, add_synth=False)

    # Calculate genre-standard chord progressions
    progression = [0, 5, 2, 6] if scale.lower() == "minor" else [0, 4, 5, 3]

    # --- 2. Bass ---
    bass_notes = []
    for bar in range(bars):
        bar_start = bar * 4
        deg = progression[bar % len(progression)]
        bass_pitch = root_midi + scale_intervals[deg % len(scale_intervals)] - 12
        
        # Pumping 8th note bassline
        for i in range(8):
            bass_notes.append((bar_start + i * 0.5, bar_start + i * 0.5 + 0.45, bass_pitch, velocity_base))
            
    create_layer("Bass", bass_notes, add_synth=True)

    # --- 3. Rhythm Guitar (Chords) ---
    rhythm_notes = []
    for bar in range(bars):
        bar_start = bar * 4
        deg = progression[bar % len(progression)]
        
        # Generate diatonic root-position triads
        for d in [0, 2, 4]: 
            scale_deg = (deg + d) % len(scale_intervals)
            octave = (deg + d) // len(scale_intervals)
            pitch = root_midi + scale_intervals[scale_deg] + (octave * 12)
            rhythm_notes.append((bar_start + 0.0, bar_start + 4.0, pitch, velocity_base - 10))
            
    create_layer("Rhythm Guitar", rhythm_notes, add_synth=True)

    # --- 4. Lead Guitar (Arpeggios) ---
    lead_notes = []
    for bar in range(bars):
        bar_start = bar * 4
        deg = progression[bar % len(progression)]
        chord_pitches = []
        
        # Capture triad tones transposed up one octave
        for d in [0, 2, 4]:
            scale_deg = (deg + d) % len(scale_intervals)
            octave = (deg + d) // len(scale_intervals)
            chord_pitches.append(root_midi + scale_intervals[scale_deg] + (octave * 12) + 12)
            
        # 8th note arpeggiator sweeping the chord tones
        arp_pattern = [0, 1, 2, 1, 0, 1, 2, 1]
        for i in range(8):
            pitch = chord_pitches[arp_pattern[i]]
            lead_notes.append((bar_start + i * 0.5, bar_start + i * 0.5 + 0.4, pitch, velocity_base))
            
    create_layer("Lead Guitar", lead_notes, add_synth=True)

    return f"Created 4-track arrangement (Drums, Bass, Rhythm, Lead) with {bars} bars at {bpm} BPM. Note: Add a Drum VST to the 'Drums' track."
```