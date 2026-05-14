# Lo-Fi Hip Hop Drum Groove (Boom Bap)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Lo-Fi Hip Hop Drum Groove (Boom Bap)

* **Core Musical Mechanism**: This pattern relies on heavily dynamic, heavily syncopated drum programming to emulate the loose, "humanized" feel of a real drummer playing an MPC sampler. It features a sparse, off-beat kick drum, a steady backbeat snare, and a defining 3-layer hi-hat rhythm (on-beat, off-beat, and a 16th-note "ghost" skip) with drastically different MIDI velocities.
* **Why Use This Skill (Rationale)**: The groove theory here is centered around **velocity dynamics and micro-syncopation**. By drastically lowering the velocity of the 8th-note off-beats and adding an even quieter 16th-note ghost hit right before the next beat (the "a" of *1 e & a*), it creates a dragging, cyclical "skip" that gives Lo-Fi music its signature head-nodding bounce. The kicks are kept sparse and syncopated (hitting on the 8th-note "ands") to leave ample room in the low-end frequency spectrum for deep sub-basses or jazzy upright bass lines.
* **Overall Applicability**: Perfect as the rhythmic foundation for Lo-Fi Hip Hop, Chillhop, Boom Bap, and Neo-Soul tracks. 
* **Value Addition**: Compared to a flat 4/4 drum loop, this encodes vital velocity humanization and syncopated grid placement (ghost notes) that agents usually struggle to program organically.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 76 BPM (typical Lo-Fi range is 70-85 BPM).
  - **Time Signature**: 4/4.
  - **Rhythmic Grid**: 1/16th notes.
  - **Pattern Length**: 2-bar repeating loop.

* **Step B: Pitch & Harmony (General MIDI Drum Map)**
  - **Kick (MIDI Note 36 - C1)**: 
    - Bar 1: Beat 1 (1.1.00), Beat 2 "and" (1.2.50)
    - Bar 2: Beat 1 (2.1.00), Beat 2 "and" (2.2.50), Beat 3 "and" (2.3.50)
  - **Snare (MIDI Note 38 - D1)**: 
    - Beats 2 and 4 (1.2.00, 1.4.00, 2.2.00, 2.4.00)
  - **Hi-Hats (MIDI Note 42 - F#1)**: 
    - On-beats (1.1.00, 1.2.00, etc.) - High Velocity (~90%)
    - Off-beats (1.1.50, 1.2.50, etc.) - Medium Velocity (~60%)
    - Ghost-beats (1.1.75, 1.2.75, etc. - the 16th note right before the next beat) - Low Velocity (~35%)

* **Step C: Sound Design & FX**
  - The tutorial uses a dedicated Drum VST/Sampler. Because REAPER does not have a native drum kit with pre-loaded samples out of the box, this skill uses MIDI programming mapped to standard General MIDI (GM) layout. This ensures that when the user (or agent) routes the track to *any* standard drum sampler (like Sitala, MT Power Drum Kit, or ReaSamplOmatic5000), it will instantly trigger the correct drum shells.

* **Step D: Mix & Automation**
  - The core "automation" is baked directly into the MIDI note velocities, driving the sampler's volume envelope dynamically on a per-hit basis rather than using track automation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm, Timing & Accents | `RPR_MIDI_InsertNote` with mathematically scaled velocities | Grants precise, per-tick control over the 16th-note ghost hits and velocity dynamics required for the Lo-Fi bounce. |
| Item Creation | `RPR_CreateNewMIDIItemInProj` | Automatically initializes a clean MIDI take perfectly synced to the exact bar lengths. |

> **Feasibility Assessment**: 100% reproducible for the MIDI/Rhythm sequence. The tone of the drums will depend entirely on the user's chosen drum VST/samples, but the *groove* (which is the focus of the tutorial) is fully captured.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lo-Fi Drums",
    bpm: int = 76,
    key: str = "C",      # Unused for drums, kept for signature consistency
    scale: str = "minor", # Unused for drums, kept for signature consistency
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a dynamic Lo-Fi / Boom Bap drum groove in the current REAPER project.
    Generates a heavily humanized MIDI sequence mapped to General MIDI standards.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (76 is standard for this genre).
        key: Ignored for drum generation.
        scale: Ignored for drum generation.
        bars: Number of bars to generate (must be an even number for the 2-bar kick variation).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Safely create a new MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # General MIDI Mappings
    KICK_PITCH = 36  # C1
    SNARE_PITCH = 38 # D1
    HAT_PITCH = 42   # F#1

    # Velocity scaling for the Lo-Fi feel
    v_kick = min(127, int(velocity_base * 1.0))
    v_snare = min(127, int(velocity_base * 1.0))
    v_hat_on = min(127, int(velocity_base * 0.90))
    v_hat_off = min(127, int(velocity_base * 0.60))
    v_hat_ghost = min(127, int(velocity_base * 0.35))

    # Helper function to place MIDI notes based on beat grid
    def add_drum_hit(pitch, beat_position, duration_in_beats, vel):
        start_time_sec = beat_position * (60.0 / bpm)
        end_time_sec = (beat_position + duration_in_beats) * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
        # Note: selected=False, muted=False, chan=0
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)

    # === Step 4: Populate the Rhythm Pattern ===
    note_count = 0
    
    for b in range(bars):
        bar_beat_offset = b * 4.0

        # --- SNARE ---
        # Hits steadily on beat 2 and 4
        add_drum_hit(SNARE_PITCH, bar_beat_offset + 1.0, 0.25, v_snare) # Beat 2
        add_drum_hit(SNARE_PITCH, bar_beat_offset + 3.0, 0.25, v_snare) # Beat 4
        note_count += 2

        # --- HI-HATS ---
        # 3-layer syncopated pattern on every beat
        for i in range(4):
            # 1. On-beat (1.0, 2.0, 3.0, 4.0)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.0, 0.25, v_hat_on)
            # 2. Off-beat 8th note (1.5, 2.5, 3.5, 4.5)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.5, 0.25, v_hat_off)
            # 3. Ghost 16th note before the next beat (1.75, 2.75, 3.75, 4.75)
            add_drum_hit(HAT_PITCH, bar_beat_offset + i + 0.75, 0.25, v_hat_ghost)
            note_count += 3

        # --- KICK DRUM ---
        # 2-Bar alternating boom-bap pattern
        if b % 2 == 0:
            # First bar pattern: Beat 1, and the "and" of Beat 2
            add_drum_hit(KICK_PITCH, bar_beat_offset + 0.0, 0.25, v_kick) # 1.1.00
            add_drum_hit(KICK_PITCH, bar_beat_offset + 1.5, 0.25, v_kick) # 1.2.50
            note_count += 2
        else:
            # Second bar pattern: Beat 1, the "and" of Beat 2, and the "and" of Beat 3
            add_drum_hit(KICK_PITCH, bar_beat_offset + 0.0, 0.25, v_kick) # 2.1.00
            add_drum_hit(KICK_PITCH, bar_beat_offset + 1.5, 0.25, v_kick) # 2.2.50
            add_drum_hit(KICK_PITCH, bar_beat_offset + 2.5, 0.25, v_kick) # 2.3.50
            note_count += 3

    # Important: sort the MIDI events so they playback correctly
    RPR.RPR_MIDI_Sort(take)

    # Note: No internal sampler (like ReaSynth) is added because synthesizing 
    # a snare and high-hat out of a basic oscillator sounds awful and obscures the groove. 
    # The track is ready for a VSTi drum sampler to be dropped onto it.

    return f"Created '{track_name}' with {note_count} dynamic drum MIDI notes over {bars} bars at {bpm} BPM."
```