### 1. High-level Design Pattern Extraction

> **Skill Name**: Four-on-the-Floor House Drum Loop

* **Core Musical Mechanism**: The video demonstrates the user loading a drum machine (Reason's Redrum) and auditioning a classic "House" rhythm patch. The defining signature of this pattern is the "four-on-the-floor" rhythm: a solid kick drum on every quarter note, reinforced by a clap or snare on beats 2 and 4, and punctuated by a closed hi-hat on the eighth-note offbeats.
* **Why Use This Skill (Rationale)**: This is the fundamental groove engine of modern electronic dance music. The steady quarter-note kick anchors the pulse (providing predictability), the backbeat clap provides the driving energy, and the offbeat hi-hat creates syncopated momentum, psychoacoustically compelling the listener to move or dance in the "spaces" between the kicks.
* **Overall Applicability**: This pattern is the literal foundation for House, Techno, Disco, and countless subgenres of EDM and Pop. It is perfect as a starting rhythmic bed for a new track or as the core groove for a dance drop.
* **Value Addition**: Instead of manually programming kicks, claps, and hats one by one, this skill instantly generates a perfectly quantized, velocity-balanced foundational MIDI drum groove. It maps to the General MIDI (GM) drum standard, meaning it can be routed to almost any drum sampler or synth immediately.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **BPM Range**: ~120-128 BPM (The script defaults to 120 BPM, standard for House)
  - **Rhythmic Grid**: 1/8 notes.
  - **Pattern**:
    - Kick: Beats 1, 2, 3, 4 (Quarter notes)
    - Clap: Beats 2, 4
    - Closed Hat: The "and" of every beat (eighth-note offbeats)
* **Step B: Pitch & Harmony**
  - Uses the General MIDI Drum Map (Channel 10):
    - Kick Drum: MIDI Note 36 (C1)
    - Hand Clap: MIDI Note 39 (D#1)
    - Closed Hi-Hat: MIDI Note 42 (F#1)
* **Step C: Sound Design & FX**
  - In the tutorial, a third-party VST (Reason Rack Plugin / Redrum) is used. To ensure maximum reproducibility, the extracted code creates standard MIDI notes on a new track. The user can then place their preferred drum sampler (like ReaSamplOmatic5000, Battery, or Redrum) on the track to voice the pattern.
* **Step D: Mix & Automation**
  - Velocity is modulated to create a subtle groove: Kicks are strong (110), Claps are slightly backed off (100) to blend with the kick, and Hats are lighter (90) to maintain a bouncy feel without overpowering the mix.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Four-on-the-floor rhythm | MIDI note insertion | Provides exact control over timing (PPQ), velocity, and rhythmic subdivisions required to perfectly reproduce the groove heard in the video. |
| General MIDI Mapping | MIDI Channel 10 | Ensures the output will trigger the correct elements (Kick, Clap, Hat) on standard drum machine plugins without relying on the specific proprietary VST shown in the video. |

> **Feasibility Assessment**: 85%. The code flawlessly reproduces the rhythmic timing, velocities, and MIDI layout of the pattern auditioned in the video. Because the specific Reason Redrum VST patch cannot be programmatically invoked without the user owning that specific third-party software, the script provides the universal MIDI backbone ready to drive any drum instrument.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "House Drums (MIDI)",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a classic Four-on-the-Floor House Drum Pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM (120-128 recommended for House).
        key: Ignored for drum pattern.
        scale: Ignored for drum pattern.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (scaled internally for groove).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created pattern.
    """
    import reaper_python as RPR

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

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)

    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Insert MIDI Notes (GM Drum Map) ===
    # MIDI Note definitions
    KICK = 36   # C1
    CLAP = 39   # D#1
    HAT = 42    # F#1

    # Rhythmic definition: (beat_offset, pitch, velocity_modifier, duration_in_beats)
    # Beat 0 = Beat 1, Beat 1 = Beat 2, etc.
    groove_pattern = [
        (0.0, KICK, 1.1, 0.25),  # Beat 1 Kick
        (0.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (1.0, KICK, 1.1, 0.25),  # Beat 2 Kick
        (1.0, CLAP, 1.0, 0.25),  # Beat 2 Clap
        (1.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (2.0, KICK, 1.1, 0.25),  # Beat 3 Kick
        (2.5, HAT,  0.9, 0.25),  # Offbeat Hat
        (3.0, KICK, 1.1, 0.25),  # Beat 4 Kick
        (3.0, CLAP, 1.0, 0.25),  # Beat 4 Clap
        (3.5, HAT,  0.9, 0.25),  # Offbeat Hat
    ]

    notes_created = 0
    midi_channel = 9 # Channel 10 (0-indexed) is the standard drum channel

    for bar in range(bars):
        bar_offset_beats = bar * beats_per_bar
        
        for beat_pos, pitch, vel_mod, dur in groove_pattern:
            start_beat = bar_offset_beats + beat_pos
            end_beat = start_beat + dur

            # Convert beats to time, then to PPQ for accurate placement
            start_time = start_beat * (60.0 / bpm)
            end_time = end_beat * (60.0 / bpm)

            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)

            # Calculate final velocity, keeping it safely within 1-127 bounds
            final_velocity = int(velocity_base * vel_mod)
            final_velocity = max(1, min(127, final_velocity))

            RPR.RPR_MIDI_InsertNote(
                take, 
                False,          # selected
                False,          # muted
                start_ppq,      # start time
                end_ppq,        # end time
                midi_channel,   # channel
                pitch,          # pitch
                final_velocity, # velocity
                True            # noSort (we sort once at the end for performance)
            )
            notes_created += 1

    # Sort the MIDI stream after all notes are added
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {notes_created} GM drum notes over {bars} bars at {bpm} BPM"
```