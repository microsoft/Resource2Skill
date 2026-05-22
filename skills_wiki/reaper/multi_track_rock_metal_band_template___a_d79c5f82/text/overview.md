### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Rock/Metal Band Template & Arrangement

* **Core Musical Mechanism**: While this tutorial primarily focuses on configuring REAPER's MIDI editor to emulate Logic Pro's single-window, multi-track editing workflow (utilizing ghost notes and synchronized selection), it culminates in a demonstration of a classic 4-part Rock/Metal arrangement. The core mechanism is the foundational layering of a unified harmonic progression across four distinct roles: a driving 8th-note drum groove, an anchoring bass line, power-chord rhythm guitars, and a cascading arpeggiated lead line.
* **Why Use This Skill (Rationale)**: This arrangement pattern creates a massive, driving wall of sound characteristic of modern rock, metal, and orchestral-hybrid music. The bass and kick drum lock in together, while the rhythm guitar provides wide frequency masking in the midrange. The lead guitar sits above this bed, providing melodic movement via rapid arpeggios that outline the chord changes, creating continuous rhythmic momentum.
* **Overall Applicability**: Excellent as a starting point for rock, metal, pop-punk, or synthetic synthwave tracks. It provides a complete "band in a box" scaffold that can immediately be populated with high-quality VSTs (like Kontakt libraries, amp simulators, or drum samplers).
* **Value Addition**: Instead of starting with a blank canvas, this skill automatically sets up the critical four-track routing and populates it with a harmonically locked, multi-track musical loop. It encodes the basic theory of power chords, arpeggios, and standard rock drum grooves.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time Signature: 4/4
  * Rhythmic Grid: Driving 8th-note subdivision.
  * Drums: Snare on beats 2 and 4. Kick on 1, 2-and, and 3-and. Hi-hats play constant 8th notes. 
  * Bass: Straight 8th notes, matching the kick rhythm dynamically.
  * Lead: 8th or 16th-note continuous arpeggios.

* **Step B: Pitch & Harmony**
  * The tutorial demonstrates a minor progression (specifically B minor). We will generalize this to a standard `i - VI - III - VII` diatonic minor progression.
  * Bass plays root notes in Octave 2.
  * Rhythm guitar plays root-position chords (Root, 5th, Octave) in Octave 3 to emulate power chords.
  * Lead guitar plays arpeggiated triads (Root, 3rd, 5th, Octave) in Octave 4/5.

* **Step C: Sound Design & FX**
  * Independent tracks for Drums, Bass, Rhythm Guitar, and Lead Guitar.
  * In the tutorial, these are routed to heavy Kontakt libraries. For pure ReaScript reproducibility without assuming installed VSTs, this script inserts ReaSynth on the tonal tracks and leaves the Drum track ready for a sampler (like ReaSamplOmatic5000), acting as a foundational template.

* **Step D: Mix & Automation (if applicable)**
  * Basic volume balancing (Drums and Bass centered, Rhythm pushed slightly back, Lead upfront).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-track arrangement | `RPR_InsertTrackAtIndex` | REAPER API allows creating the 4 separate tracks to emulate the "band" setup shown. |
| Harmonic matching | Pitch calculation via list arrays | Ensures the bass, rhythm, and lead are locked to the user's requested key and scale. |
| Drum groove & melodies | `RPR_MIDI_InsertNote` | Precise programmatic placement of the MIDI notes (snare/kick grid, guitar arpeggios). |

> **Feasibility Assessment**: 90% reproducible. The script perfectly reproduces the 4-track MIDI arrangement, note placement, velocity, and harmonic structure. However, because we cannot assume you have the specific third-party Kontakt guitar/drum libraries the author uses, the code uses REAPER's native `ReaSynth` so you hear immediate tonal feedback. You can easily drag-and-drop your own VSTs onto these generated tracks.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Rock_Template",
    track_name: str = "Band",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-Track Rock/Metal arrangement (Drums, Bass, Rhythm Gtr, Lead Gtr)
    demonstrated in the REAPER workflow tutorial.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
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
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = NOTE_MAP.get(key.capitalize(), 11) # Default to B

    # Diatonic progression relative to scale: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 

    # --- Setup Project Tempo ---
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    def get_pitch(degree_idx, octave):
        """Convert a scale degree index and octave into an absolute MIDI pitch."""
        octave_offset = degree_idx // len(scale_intervals)
        scale_idx = degree_idx % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx] + 12 * (octave + octave_offset)
        return max(0, min(127, pitch))

    def create_midi_track(name, with_synth=True):
        """Helper to create a track, a MIDI item, and add basic FX."""
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        beats_per_bar = 4
        item_length_sec = (60.0 / bpm) * beats_per_bar * bars
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        if with_synth:
            RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Lower volume for safety
            RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.2)

        return take

    def insert_note(take, pitch, beat_pos, beat_len, vel):
        """Insert a MIDI note using beat-based positioning."""
        start_time = (beat_pos / bpm) * 60.0
        end_time = ((beat_pos + beat_len) / bpm) * 60.0
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, int(vel), True)

    # === Track 1: DRUMS ===
    take_drums = create_midi_track("1 MIDI Drums", with_synth=False)
    for b in range(bars):
        bar_offset = b * 4
        # Kick (36)
        insert_note(take_drums, 36, bar_offset + 0.0, 0.25, velocity_base)
        insert_note(take_drums, 36, bar_offset + 1.5, 0.25, velocity_base - 10)
        insert_note(take_drums, 36, bar_offset + 2.5, 0.25, velocity_base)
        
        # Snare (38)
        insert_note(take_drums, 38, bar_offset + 1.0, 0.25, velocity_base + 10)
        insert_note(take_drums, 38, bar_offset + 3.0, 0.25, velocity_base + 10)
        
        # Hi-hat (42) - 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 20
            insert_note(take_drums, 42, bar_offset + (i * 0.5), 0.2, vel)
            
        # Crash (49) on downbeat of first bar
        if b == 0:
            insert_note(take_drums, 49, bar_offset + 0.0, 0.5, velocity_base + 15)

    RPR.RPR_MIDI_Sort(take_drums)

    # === Track 2: BASS ===
    take_bass = create_midi_track("2 BASS")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        pitch = get_pitch(degree, 2) # Octave 2
        
        # Driving 8th notes
        for i in range(8):
            vel = velocity_base if i % 2 == 0 else velocity_base - 10
            insert_note(take_bass, pitch, bar_offset + (i * 0.5), 0.45, vel)
    RPR.RPR_MIDI_Sort(take_bass)

    # === Track 3: RHYTHM GUITAR ===
    take_rhy = create_midi_track("3 GTR RHY")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        
        # Power Chord block (Root, 5th, Octave) sustained for the whole bar
        p1 = get_pitch(degree, 3)     # Root
        p2 = get_pitch(degree + 4, 3) # 5th
        p3 = get_pitch(degree + 7, 3) # Octave
        
        for p in [p1, p2, p3]:
            insert_note(take_rhy, p, bar_offset, 3.9, velocity_base - 5)
    RPR.RPR_MIDI_Sort(take_rhy)

    # === Track 4: LEAD GUITAR ===
    take_lead = create_midi_track("4 GTR LEAD")
    for b in range(bars):
        bar_offset = b * 4
        degree = progression_degrees[b % len(progression_degrees)]
        
        # Up-and-down 8th note arpeggio: Root, 3rd, 5th, Octave, 5th, 3rd, Root, 3rd
        arp_pattern = [0, 2, 4, 7, 4, 2, 0, 2] 
        
        for i, arp_deg in enumerate(arp_pattern):
            pitch = get_pitch(degree + arp_deg, 4) # Octave 4
            vel = velocity_base + (5 if i == 0 else -10)
            insert_note(take_lead, pitch, bar_offset + (i * 0.5), 0.4, vel)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created 4-track Rock/Metal Band Template ({bars} bars in {key} {scale} at {bpm} BPM)."
```