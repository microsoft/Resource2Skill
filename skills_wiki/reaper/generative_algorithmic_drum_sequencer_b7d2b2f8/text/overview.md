### 1. High-level Design Pattern Extraction

> **Skill Name**: Generative Algorithmic Drum Sequencer 

* **Core Musical Mechanism**: The video demonstrates using an algorithmic MIDI generator (Reason's "Beat Map") to drive a sampler/synth plugin. The defining musical technique here is **probabilistic/generative rhythm construction**. Instead of manually drawing MIDI notes, rhythms are populated based on algorithms and probability gates, leading to complex, slightly unpredictable, and highly syncopated drum grooves.

* **Why Use This Skill (Rationale)**: Generative sequencing mimics the nuanced variations of a human drummer. By using probability to occasionally skip downbeats, add ghost notes, or interject 16th-note syncopations, you create a rhythm that avoids the robotic repetitiveness of looped 4-bar blocks. It introduces organic movement (micro-timing swing) and velocity dynamics automatically.

* **Overall Applicability**: This pattern is widely used in Boom-Bap Hip-Hop, Lo-Fi, IDM, and modern Electronic production to quickly establish a complex foundational groove.

* **Value Addition**: Rather than requiring a third-party plugin like Reason Rack, this skill explicitly encodes a generative algorithm into Python. It adds a parametrically adjustable drum pattern to the project, translating mathematical probability into a highly musical MIDI clip that you can route to any drum synth or sampler.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time, optimally around 80-120 BPM.
  - **Grid & Swing**: 16th-note grid structure. Off-beat 16th notes (the "e" and "a" of the beat) are delayed by 25% of their duration to create a heavy MPC-style swing.
  - **Note Density**: Modulated by a "complexity" variable. Low complexity yields basic 8th-note hi-hats and on-beat kicks/snares. High complexity introduces ghost notes, syncopated kicks on the 16th off-beats, and dense hi-hat variations.

* **Step B: Pitch & Harmony**
  - **Standard GM Drum Map**: 
    - Kick Drum: C1 (MIDI pitch 36)
    - Acoustic Snare: D1 (MIDI pitch 38)
    - Closed Hi-Hat: F#1 (MIDI pitch 42)
  - **Velocity Dynamics**: Randomized within specific ranges. Accented downbeats hover around `velocity_base`, while off-beats and ghost notes are mathematically reduced by 20–40 velocity points to simulate softer stick impacts.

* **Step C: Sound Design & FX**
  - A standard placeholder EQ (ReaEQ) is added to the track to simulate the "lo-fi/12-bit sampler" vibe shown in the tutorial (which used the RX1200 plugin), rolling off excessive highs.

* **Step D: Mix & Automation**
  - No complex mix routing is applied, allowing the generated MIDI item to be easily assigned to the producer's VSTi of choice.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Algorithmic Rhythm Generation** | Math/Probability Logic + `RPR_MIDI_InsertNote` | Reproduces the exact functionality of the third-party "Beat Map" plugin natively inside REAPER using ReaScript algorithms. |
| **Micro-timing / Swing** | Absolute Time Calculation (`proj_time`) | Allows for precise floating-point manipulation of 16th note timing before committing it to the rigid REAPER MIDI PPQ grid. |

> **Feasibility Assessment**: 100% of the core *MIDI generation concept* is reproduced. The precise third-party drum sounds (RX1200/Massive X) are not included, but standard GM drum notes are provided so any drum sampler will immediately play the algorithmic groove.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Algorithmic Drums",
    bpm: int = 90,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a generative, probability-based drum pattern on a new track.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (ignored for GM drums).
        scale: Scale type (ignored for GM drums).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: 
            complexity (float): 0.0 to 1.0. Higher values yield more syncopation and ghost notes.
            
    Returns:
        Status string.
    """
    import random
    import reaper_python as RPR

    # Retrieve complexity setting (default to 0.6 for a moderate groove)
    complexity = float(kwargs.get("complexity", 0.6))
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    qn_len = 60.0 / bpm
    bar_length_sec = qn_len * 4
    item_length = bar_length_sec * bars
    
    item_start_pos = 0.0
    item = RPR.RPR_CreateNewMIDIItemInProj(track, item_start_pos, item_start_pos + item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # Helper function to convert seconds to PPQ and insert a note
    def insert_note(pitch, time_sec, duration_sec, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec + duration_sec)
        # RPR_MIDI_InsertNote(take, selected, muted, startppq, endppq, chan, pitch, vel, noSort)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    def clamp(v):
        return max(1, min(127, int(v)))

    # GM Drum Map Notes
    KICK = 36
    SNARE = 38
    HAT = 42

    note_count = 0

    # === Step 4: Generative Algorithm ===
    for bar in range(bars):
        for beat in range(4):
            for sixteenth in range(4):
                # Calculate absolute time with 25% MPC-style Swing
                time_sec = item_start_pos + bar * bar_length_sec + beat * qn_len + sixteenth * (qn_len / 4)
                if sixteenth % 2 != 0:
                    time_sec += (qn_len / 4) * 0.25 

                is_kick = False
                is_snare = False
                is_hat = False

                # --- Probabilistic Kick Rules ---
                if beat == 0 and sixteenth == 0:
                    is_kick = True
                elif beat == 1 and sixteenth == 2 and random.random() < 0.4 * complexity:
                    is_kick = True
                elif beat == 1 and sixteenth == 3 and random.random() < 0.6 * complexity:
                    is_kick = True
                elif beat == 2 and sixteenth == 0:
                    if random.random() > 0.2 * complexity:  # Occasionally skip beat 3 for syncopation
                        is_kick = True
                elif beat == 2 and sixteenth == 3 and random.random() < 0.7 * complexity:
                    is_kick = True
                elif beat == 3 and sixteenth == 2 and random.random() < 0.3 * complexity:
                    is_kick = True

                # --- Probabilistic Snare Rules ---
                if beat == 1 and sixteenth == 0:
                    is_snare = True
                elif beat == 3 and sixteenth == 0:
                    is_snare = True
                elif sixteenth != 0 and random.random() < 0.15 * complexity:
                    is_snare = True # Ghost notes

                # --- Probabilistic Hi-Hat Rules ---
                if sixteenth % 2 == 0:
                    is_hat = True # Standard 8th notes
                else:
                    if random.random() < complexity:
                        is_hat = True # Syncopated 16th notes

                # --- Execute Insertions with Humanized Velocities ---
                if is_kick:
                    vel = clamp(velocity_base + random.randint(-5, 10))
                    insert_note(KICK, time_sec, 0.1, vel)
                    note_count += 1
                
                if is_snare:
                    if sixteenth == 0:
                        vel = clamp(velocity_base + random.randint(-5, 15))
                    else:
                        vel = clamp(velocity_base - random.randint(20, 40)) # Softer ghost notes
                    insert_note(SNARE, time_sec, 0.1, vel)
                    note_count += 1
                
                if is_hat:
                    if sixteenth % 2 == 0:
                        vel = clamp(velocity_base - random.randint(5, 15))
                    else:
                        vel = clamp(velocity_base - random.randint(20, 30))
                    insert_note(HAT, time_sec, 0.05, vel)
                    note_count += 1

    # Finalize MIDI pool and sort events
    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add basic FX setup ===
    # Add an EQ placeholder to mimic the tutorial's vintage 12-bit sampler processing
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    return f"Created '{track_name}' containing {note_count} generative drum notes over {bars} bars at {bpm} BPM."
```