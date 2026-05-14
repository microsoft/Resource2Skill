# Dynamic MIDI Drum Sequencing & Velocity Articulation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic MIDI Drum Sequencing & Velocity Articulation

* **Core Musical Mechanism**: Rhythmic sequencing using General MIDI drum mapping with strict attention to velocity articulation. The tutorial emphasizes moving away from "blocky" piano roll durations (rectangles) to discrete triggers (triangles/diamonds), highlighting that drum groove relies entirely on timing placement and velocity variations (accents and ghost notes) rather than note length or harmony.
* **Why Use This Skill (Rationale)**: Programming all drums at identical velocities creates a robotic, "machine-gun" effect. By accenting downbeat hi-hats and lowering off-beat velocities—and by utilizing low-velocity ghost notes on the snare—you introduce human feel and groove. The discrete "named notes" approach compartmentalizes the unpitched percussive elements, making rhythmic interplay easier to visualize and sequence. 
* **Overall Applicability**: Foundational for any genre utilizing programmed drums (Rock, Pop, Boom-Bap, Synthwave). It sets up a standard, predictable MIDI framework that can drive any generic drum sampler VST.
* **Value Addition**: Compared to a blank MIDI clip, this skill encodes a standard 8th-note rock/pop groove with pre-calculated syncopations (off-beat kick) and humanized velocity curves, alongside a standard mixing channel strip (EQ + Compression) ready for a drum VST.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, typically 100-120 BPM.
  - **Grid**: 16th note grid utilized for syncopation. 
  - **Pattern**: 
    - Kick on 1, 3, and the "and" of 3 (syncopation).
    - Snare on 2 and 4, with 16th-note ghost notes (low velocity) on the "a" of 2 and 4.
    - Hi-hats playing straight 8th notes.
  - **Velocity Articulation**: Downbeat hi-hats are accented (100% base velocity), off-beats are lowered (60%). Ghost snares sit at 40% velocity.

* **Step B: Pitch & Harmony**
  - Drums are unpitched, adhering to the standard General MIDI (GM) drum map:
    - Kick = 36 (C2)
    - Snare = 38 (D2)
    - Closed Hi-Hat = 42 (F#2)
    - Crash Cymbal = 49 (C#3)
  - *(Note: The script includes a root-note offset computation. By default in "C", it maps perfectly to GM. If a different key is passed, the kit transposes, which is highly useful for tuned electronic 808 kits).*

* **Step C: Sound Design & FX**
  - **FX Chain**: A foundational drum bus chain is attached using REAPER's stock `ReaEQ` (for carving out low-mid mud) and `ReaComp` (for gluing the kit and adding punch).
  - **Instrument**: MIDI is left generic so the user/agent can easily drop a drum sampler (like RS5K, MT Power Drum Kit, or EZDrummer) onto the track.

* **Step D: Mix & Automation**
  - Not automated in this step, but velocities handle the dynamic mix balance natively inside the MIDI item.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Groove | `RPR_MIDI_InsertNote()` | Allows mathematically precise control over QN timing and exact velocity (0-127) for ghost notes and accents, replacing the manual GUI drag-and-drop shown in the video. |
| Drum Map Transposition | Python Dictionary Lookup | Computes GM standard pitches but allows offset based on root key for tuned electronic kits. |
| Drum Bus FX | `RPR_TrackFX_AddByName()` | Automatically adds ReaEQ and ReaComp to prepare the track for mixing. |

> **Feasibility Assessment**: 100%. While the video focuses heavily on clicking UI menus to change note shapes to diamonds/triangles, this script entirely bypasses the need for UI manipulation by directly coding the *musical intent* of those edits: a dynamically articulated drum performance mapped to standard note values.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Drum Kit",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Dynamic MIDI Drum Groove with velocity articulations.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (used to offset GM drum map for tuned 808s; C = standard GM).
        scale: Scale type (unused for standard drums, kept for signature compatibility).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127) for accents.
        **kwargs: Additional overrides.

    Returns:
        Status string describing what was created.
    """
    import reaper_python as RPR

    # Music theory lookup table to determine root offset
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key, 0)
    
    # Compute MIDI pitches based on Key. 
    # If key is "C" (0), standard GM mapping is perfectly preserved.
    # If another key is provided, the kit transposes (useful for pitched 808s).
    kick_note = 36 + root_val
    snare_note = 38 + root_val
    hh_closed = 42 + root_val
    crash = 49 + root_val

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Add a MIDI item that spans the requested number of bars
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    note_count = 0

    # === Step 4: Populate Rhythmic Pattern with Dynamic Velocity ===
    for b in range(bars):
        bar_qn = b * 4.0
        
        # 1. KICK: On beats 1, 3, and a syncopated kick on the "and" of 3
        kicks_qn = [0.0, 2.0, 2.5]
        for q in kicks_qn:
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.25),
                1, kick_note, velocity_base, False)
            note_count += 1
                
        # 2. SNARE: Backbeats on 2 and 4, plus 16th ghost notes
        # Format: (QN position, velocity)
        snares = [
            (1.0, velocity_base),                     # Solid backbeat (Beat 2)
            (2.75, int(velocity_base * 0.4)),         # Ghost note before Beat 4
            (3.0, velocity_base),                     # Solid backbeat (Beat 4)
            (4.75, int(velocity_base * 0.4))          # Ghost note leading into next bar
        ]
        for q, vel in snares:
            # Prevent ghost notes from bleeding past bar 4.0
            if q < 4.0:
                RPR.RPR_MIDI_InsertNote(take, False, False, 
                    RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                    RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.15),
                    1, snare_note, vel, False)
                note_count += 1
                
        # 3. HI-HAT: 8th notes with alternating accents
        for i in range(8):
            q = i * 0.5
            # Accent the downbeats (0.0, 1.0, 2.0, 3.0), lower velocity on off-beats
            hh_vel = velocity_base if i % 2 == 0 else int(velocity_base * 0.6)
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + q + 0.15),
                1, hh_closed, hh_vel, False)
            note_count += 1
                
        # 4. CRASH: Emphasize the downbeat of the very first bar
        if b == 0:
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + 0.0),
                RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_qn + 0.5),
                1, crash, velocity_base, False)
            note_count += 1

    # Finalize MIDI structure
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add Drum Bus FX Chain ===
    # Pre-loading standard mixing tools for the drum bus
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)

    return f"Created '{track_name}' with {note_count} articulated drum notes over {bars} bars at {bpm} BPM."
```