### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Ensemble Arrangement (Rock/Pop Template)

* **Core Musical Mechanism**: The simultaneous layering of four distinct musical roles (Drums, Bass, Rhythm Chords, Lead Arpeggio) tied to a single, cohesive harmonic progression. The pattern splits the frequency spectrum and rhythmic grid across multiple instruments to build a full arrangement loop. 
* **Why Use This Skill (Rationale)**: A core tenet of modern music production is vertical arrangement—ensuring that different instruments don't clash rhythmically or harmonically. By writing the backbeat (kick/snare), the low-end foundation (8th-note bass), the mid-range harmonic bed (sustained chords), and the top-end melody (arpeggios) in a single workflow, you create a locked-in groove. This is exactly why the multi-track MIDI workflow demonstrated in the tutorial is necessary: it allows the producer to visually align the ghost notes of the bass with the kick drum, and the arpeggios with the chord extensions.
* **Overall Applicability**: Generating the foundation (intro, verse, or chorus loop) for pop, rock, synthwave, or electronic tracks. 
* **Value Addition**: Instead of creating a single isolated melody or drum beat, this skill acts as a "band in a box," automatically generating a perfectly synchronized 4-part arrangement that guarantees harmonic and rhythmic alignment across the project.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, optimally around 110-130 BPM (120 BPM default).
  - **Drums**: Standard 4/4 backbeat (Kick on 1 & 3, Snare on 2 & 4) with 8th-note hi-hats.
  - **Bass**: Straight 8th-note pulse, locking in with the kick drum.
  - **Rhythm**: Whole notes (holding the chord for the full bar) to create a sustained harmonic bed.
  - **Lead**: 8th-note ascending/descending arpeggios to provide rhythmic momentum.

* **Step B: Pitch & Harmony**
  - **Progression**: I - IV - vi - V (or i - iv - VI - v in minor), mapped using scale degrees `[0, 3, 5, 4]`.
  - **Bass Voicing**: Root notes in Octave 2.
  - **Rhythm Voicing**: Root-position triads (Root, 3rd, 5th) in Octave 3.
  - **Lead Voicing**: Arpeggiated chord tones (Root, 3rd, 5th, 3rd) in Octave 4.

* **Step C: Sound Design & Track Setup**
  - Replicates the tutorial's visual workflow by creating four distinct tracks.
  - Color-codes the tracks exactly as demonstrated: Drums (Pink), Bass (Purple), Rhythm Guitar (Orange), Lead Guitar (Blue).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Setup & Color Coding | Track creation & `I_CUSTOMCOLOR` | Reproduces the visual multi-track setup highlighted in the video tutorial. |
| Harmonic/Rhythmic Generation | Programmatic MIDI insertion | Allows mathematically perfectly aligned chords, basslines, and drums that respond to user parameters (Key/Scale). |
| PPQ Timing | `RPR_MIDI_GetPPQPosFromProjTime` | Ensures notes are locked exactly to the REAPER grid regardless of the BPM setting. |

> **Feasibility Assessment**: 100% reproducible for the MIDI and arrangement logic. The tutorial uses third-party Kontakt guitar libraries which cannot be summoned via stock ReaScript, so the script generates the exact MIDI performances on explicitly labeled tracks ready for your chosen VSTs.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrackArrangement",
    bpm: int = 120,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-part ensemble arrangement (Drums, Bass, Rhythm, Lead) in the specified key.
    
    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (e.g., "C", "D", "F#").
        scale: Scale type ("major", "minor", etc.).
        bars: Number of bars to generate (default 4 to match the progression).
        velocity_base: Base MIDI velocity.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
    }
    
    # Fallback to major if scale not found
    current_scale = SCALES.get(scale.lower(), SCALES["major"])
    root_val = NOTE_MAP.get(key, 0)
    
    # Helper to calculate pitch from scale degree and octave
    def get_pitch(degree: int, octave: int) -> int:
        scale_len = len(current_scale)
        oct_shift = degree // scale_len
        rem_deg = degree % scale_len
        # +1 to make octave 3 start at MIDI note 48 (standard C3)
        return root_val + current_scale[rem_deg] + ((octave + oct_shift + 1) * 12)

    # I, IV, vi, V progression mapped to 0-indexed scale degrees
    progression = [0, 3, 5, 4] 

    # Set tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # Time/Grid calculations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Track definition config (matching tutorial colors)
    def make_color(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    tracks_config = [
        {"name": "Drums",    "color": make_color(255, 105, 180)}, # Pink
        {"name": "Bass",     "color": make_color(128, 0, 128)},   # Purple
        {"name": "GTR RHY",  "color": make_color(255, 165, 0)},   # Orange
        {"name": "GTR LEAD", "color": make_color(0, 191, 255)}    # Blue
    ]

    start_track_idx = RPR.RPR_CountTracks(0)
    takes = {}

    # === Step 1: Initialize Tracks and MIDI Items ===
    for i, t_conf in enumerate(tracks_config):
        track_idx = start_track_idx + i
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Set Name and Color
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_conf["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_conf["color"])
        
        # Create MIDI Item
        item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
        take = RPR.RPR_GetActiveTake(item)
        takes[t_conf["name"]] = take

    # Helper function to add a note precisely
    def add_note(take, start_beat, duration_beats, pitch, velocity):
        start_time = start_beat * (60.0 / bpm)
        end_time = (start_beat + duration_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity, True)

    # === Step 2: Populate Musical Data ===
    
    total_beats = bars * beats_per_bar
    
    # 2A. Drums (Standard Rock Beat)
    drum_take = takes["Drums"]
    for b in range(int(total_beats)):
        # Kick on 1 and 3
        if b % 4 == 0 or b % 4 == 2:
            add_note(drum_take, b, 0.5, 36, velocity_base)
        # Snare on 2 and 4
        if b % 4 == 1 or b % 4 == 3:
            add_note(drum_take, b, 0.5, 38, velocity_base)
            
    # Hi-hats on 8th notes
    for hb in range(int(total_beats * 2)):
        beat_pos = hb * 0.5
        vel = velocity_base if hb % 2 == 0 else int(velocity_base * 0.7) # Accents on downbeats
        add_note(drum_take, beat_pos, 0.25, 42, vel)

    # 2B. Bass, Rhythm, and Lead
    bass_take = takes["Bass"]
    rhy_take = takes["GTR RHY"]
    lead_take = takes["GTR LEAD"]
    
    for bar in range(bars):
        deg = progression[bar % len(progression)]
        start_beat = bar * beats_per_bar
        
        # Bass: 8th notes on the Root
        bass_pitch = get_pitch(deg, 2)
        for i in range(8):
            add_note(bass_take, start_beat + (i * 0.5), 0.45, bass_pitch, velocity_base)
            
        # Rhythm: Whole note Triads
        p1 = get_pitch(deg, 3)
        p2 = get_pitch(deg + 2, 3)
        p3 = get_pitch(deg + 4, 3)
        add_note(rhy_take, start_beat, 4.0, p1, int(velocity_base*0.9))
        add_note(rhy_take, start_beat, 4.0, p2, int(velocity_base*0.8))
        add_note(rhy_take, start_beat, 4.0, p3, int(velocity_base*0.8))
        
        # Lead: 8th note Arpeggios (Root, 3rd, 5th, 3rd sequence)
        arp_sequence = [p1 + 12, p2 + 12, p3 + 12, p2 + 12] # Octave 4
        for i in range(8):
            arp_pitch = arp_sequence[i % 4]
            add_note(lead_take, start_beat + (i * 0.5), 0.4, arp_pitch, velocity_base)

    # === Step 3: Sort MIDI events ===
    for take in takes.values():
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track ensemble (Drums, Bass, Rhythm, Lead) over {bars} bars in {key} {scale} at {bpm} BPM."
```