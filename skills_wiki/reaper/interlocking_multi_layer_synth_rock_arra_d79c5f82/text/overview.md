### 1. High-level Design Pattern Extraction

> **Skill Name**: Interlocking Multi-Layer Synth-Rock Arrangement

* **Core Musical Mechanism**: This pattern relies on a highly structured, interlocking 4-layer arrangement (Drums, Bass, Rhythm Chords, Lead Arpeggio). The driving momentum comes from a continuous 8th-note bassline anchored to the root notes of a minor key chord progression (i - VI - VII - iv). Rhythmic tension is created by placing a cyclical 6-note 16th-note arpeggio over a standard 4/4 drum beat, resulting in a subtle, shifting polyrhythm that naturally evolves across the measures.

* **Why Use This Skill (Rationale)**: This arrangement perfectly demonstrates the concept of frequency and rhythmic masking. By assigning a distinct rhythmic grid to each layer (Drums on 4ths/8ths, Bass on 8ths, Rhythm holding whole notes, Lead on 16ths), the elements never clash. As demonstrated in the video's workflow, visualizing all these MIDI layers at once allows producers to ensure that chord voicings complement the bass root, and the lead arpeggios explicitly outline the active chord tones without muddying the midrange. 

* **Overall Applicability**: This is a classic composition technique for the climax or "drop" of Synthwave, Pop-Punk, Electronic Rock, and modern cinematic tracks. It creates a dense, driving wall of sound while maintaining complete melodic clarity.

* **Value Addition**: Compared to a blank project, this skill encodes a fully fleshed-out four-part orchestration complete with drum patterns, driving basslines, functional harmonic chord voicings, and a shifting 16th-note arpeggiator algorithm tied mathematically to the changing chords.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically driven at 120-140 BPM.
  - **Drums**: Sturdy rock groove. Kicks on beats 1 and 3, snares on 2 and 4. 8th-note hi-hats with accented downbeats.
  - **Bass**: Straight 8th notes, staccato length (0.45 beats) to leave room for the kick transient.
  - **Rhythm Chords**: Held whole notes (4 beats) changing once per bar.
  - **Lead Arp**: 16th notes executing a 6-note cycle (Root, 3rd, 5th, Octave, 5th, 3rd) over a 16-note grid, creating a shifting accent pattern.

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Natural Minor (Aeolian). The demonstration loosely centers around F# minor.
  - **Progression**: i - VI - VII - iv (e.g., F#m - Dmaj - Emaj - Bm). This is a quintessential "heroic/driving" progression.
  - **Voicings**: The rhythm track plays closed triad voicings plus an octave in the 3rd/4th octave range to provide a thick midrange pad/chug.

* **Step C: Sound Design & FX**
  - While the script below generates the raw MIDI, standard application involves:
    - **Drums**: Heavy, compressed acoustic or hybrid drum samples.
    - **Bass**: A sawtooth-based sub/mid bass with sidechain compression ducking the kick.
    - **Rhythm**: Super-saw synths or distorted electric guitars.
    - **Lead**: A plucky, high-resonance synth patch (Octave 5) with ping-pong delay.

* **Step D: Mix & Automation**
  - **Velocities**: Hardcoded dynamically. Kick (110), Snare (115), Hats alternate (90/80). Bass is perfectly even (100) for a sequenced electronic feel. Lead notes are slightly softened (95) so they don't pierce the ear.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track Orchestration | Track Creation (`InsertTrackAtIndex`) | The tutorial explicitly highlights multi-track editing; we need 4 separate tracks to demonstrate the workflow. |
| Drum/Bass/Chord/Arp Patterns | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides algorithmic generation of interlocking rhythms and harmonies perfectly quantized to the grid. |
| Harmonic Awareness | Real-time interval math | Ensures the bass, chords, and arpeggios all adapt perfectly to the chosen `key` and `scale` parameters. |

> **Feasibility Assessment**: 100% reproducible for the core MIDI composition and track generation. The visual REAPER theme/colors and specific instrument VSTs (like Kontakt) shown in the video are user-specific, so the code generates standard MIDI items ready to be routed to your virtual instruments of choice.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "SynthRock",
    bpm: int = 130,
    key: str = "F#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an interlocking 4-track Synth-Rock Arrangement (Drums, Bass, Chords, Lead).
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Prefix for the generated tracks.
        bpm: Tempo in BPM.
        key: Root note (e.g., "F#", "C", "A").
        scale: Scale type (major, minor, harmonic_minor, dorian).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        
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
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Validate scale and key
    root_pitch = NOTE_MAP.get(key, 6) # Default to F#
    intervals = SCALES.get(scale, SCALES["minor"])

    # Set tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    
    # Progression degrees: i - VI - VII - iv
    progression = [0, 5, 6, 3]

    # Helper: Create a track with an empty MIDI item
    def create_track_with_midi(name, index_offset):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} {name}", True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", beat_len * beats_per_bar * bars)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, item, take

    # Helper: Insert MIDI note via PPQ calculation
    def insert_note(take, start_beat, length_beats, pitch, vel):
        start_time = start_beat * beat_len
        end_time = (start_beat + length_beats) * beat_len
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        
        # Clamp velocity
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Initialize the 4 layers
    _, _, take_drums = create_track_with_midi("Drums", 0)
    _, _, take_bass = create_track_with_midi("Bass", 1)
    _, _, take_rhythm = create_track_with_midi("Rhythm Chords", 2)
    _, _, take_lead = create_track_with_midi("Lead Arp", 3)

    # Generate patterns bar by bar
    for b in range(bars):
        # Determine current chord degree and notes
        deg = progression[b % len(progression)]
        
        # Calculate chord triad (root, 3rd, 5th of the current degree)
        c0 = intervals[deg]
        c1 = intervals[(deg + 2) % 7] + (12 if (deg + 2) >= 7 else 0)
        c2 = intervals[(deg + 4) % 7] + (12 if (deg + 4) >= 7 else 0)
        chord_pitches = [c0, c1, c2]

        # --- 1. DRUMS ---
        for beat in range(4):
            curr_beat = b * 4 + beat
            
            # Kick (MIDI 36) on 1 and 3
            if beat in [0, 2]:
                insert_note(take_drums, curr_beat, 0.25, 36, velocity_base + 10)
            
            # Snare (MIDI 38) on 2 and 4
            if beat in [1, 3]:
                insert_note(take_drums, curr_beat, 0.25, 38, velocity_base + 15)

            # Hi-hats (MIDI 42) on 8th notes (downbeat heavier than upbeat)
            insert_note(take_drums, curr_beat, 0.25, 42, velocity_base - 10)
            insert_note(take_drums, curr_beat + 0.5, 0.25, 42, velocity_base - 20)

        # Crash cymbal (MIDI 49) on the very first beat of the loop
        if b == 0:
            insert_note(take_drums, 0, 1.0, 49, velocity_base + 20)

        # --- 2. BASS ---
        # Driving 8th notes following the chord root (Octave 2)
        bass_pitch = root_pitch + 24 + c0
        for i in range(8):
            insert_note(take_bass, b * 4 + i * 0.5, 0.45, bass_pitch, velocity_base)

        # --- 3. RHYTHM CHORDS ---
        # Whole note block chords (Octave 4) + top octave
        rhythm_octave = root_pitch + 48
        for p in chord_pitches:
            insert_note(take_rhythm, b * 4, 4.0, rhythm_octave + p, velocity_base - 10)
        # Add root an octave up for thickness
        insert_note(take_rhythm, b * 4, 4.0, rhythm_octave + c0 + 12, velocity_base - 10)

        # --- 4. LEAD ARP ---
        # 16th notes executing a 6-note shifting pattern over the chord tones (Octave 5)
        lead_octave = root_pitch + 60
        arp_pattern = [c0, c1, c2, c0 + 12, c2, c1]
        
        for i in range(16): # 16 sixteenth notes per bar
            arp_pitch = lead_octave + arp_pattern[i % len(arp_pattern)]
            insert_note(take_lead, b * 4 + i * 0.25, 0.2, arp_pitch, velocity_base - 5)

    # Sort MIDI events sequentially for all takes
    for take in [take_drums, take_bass, take_rhythm, take_lead]:
        RPR.RPR_MIDI_Sort(take)

    return f"Created interlocking 4-track arrangement ('{track_name}...') over {bars} bars at {bpm} BPM in {key} {scale}."
```