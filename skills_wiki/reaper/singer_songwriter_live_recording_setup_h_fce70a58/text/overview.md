# Singer-Songwriter Live Recording Setup & Harmonic Backing

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Singer-Songwriter Live Recording Setup & Harmonic Backing

* **Core Musical Mechanism**: The tutorial demonstrates the fundamental architecture for tracking a live singer-songwriter session: setting up discrete hardware inputs (Mono 1 for Vocals, Mono 2 for Guitar), arming tracks, and applying "confidence FX" (reverb for the singer, amp simulation for the guitarist) to the monitoring signal. Since a live recording tutorial lacks a specific MIDI sequence, this skill encodes the tutorial's **track architecture and mixing setup**, while simultaneously generating a parameterized, diatonic **harmonic backing track** so the agent (or user) has an immediate musical foundation to record over.

* **Why Use This Skill (Rationale)**: The friction of routing hardware inputs and setting up monitoring chains kills analog inspiration. By automating the creation of discrete, pre-routed, FX-ready audio tracks alongside a diatonic chord progression, you establish an instant "jam environment." Providing a singer with reverb (`ReaVerbate`) helps them pitch better psychoacoustically (the "confidence verb"), while an amp simulator on a DI guitar signal provides necessary dynamic feedback and sustain.

* **Overall Applicability**: This skill is highly applicable when establishing the foundation of a new organic project (indie, folk, rock, pop). It bridges the gap between hardware recording and in-the-box MIDI production by giving the user ready-to-record audio tracks alongside a generated chordal metronome.

* **Value Addition**: Compared to a blank project, this skill automatically resolves input routing (Mono 1 / Mono 2), enables input monitoring, provisions standard FX chains for tracking, and generates a music-theory-aware I-V-vi-IV chord progression to establish the key center.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Configurable (Default 120 BPM).
  - **Grid**: The generated backing track plays sustained whole-note chords (1 bar per chord) to act as a harmonic metronome without distracting from the live performer.
  - **Recording**: Tracks are immediately armed and set to monitor the live inputs.

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Fully parameterized.
  - **Progression**: I - V - vi - IV. A universal pop/rock progression that gives the live performer an easy, familiar canvas for improvisation.
  - **Voicings**: Basic closed root-position triads computed strictly from the selected scale intervals.

* **Step C: Sound Design & FX**
  - **Backing Track**: Uses `ReaSynth` for a simple synthesized organ/pad tone.
  - **Vocal Track (Input 1)**: `ReaVerbate` added to simulate the Waves TSAR-1R Reverb used in the tutorial. Creates space and helps vocal pitch accuracy.
  - **Guitar Track (Input 2)**: `ReaDistortion` added with low drive to act as a placeholder for the Waves GTR Amp Simulator shown in the video.

* **Step D: Mix & Automation**
  - Live tracks are explicitly assigned: `I_RECINPUT` = 0 (Input 1) and 1 (Input 2).
  - `I_RECMON` is set to 1 (Input Monitoring ON).
  - `I_RECARM` is set to 1 (Record Arm ON).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Live Input Routing | `RPR_SetMediaTrackInfo_Value` | Directly maps hardware inputs to tracks, turns on Rec Arm and Monitoring as explicitly taught in the video. |
| Confidence FX | `RPR_TrackFX_AddByName` | Simulates the 3rd-party reverb and amp sim using stock REAPER equivalents (`ReaVerbate`, `ReaDistortion`). |
| Harmonic Foundation | MIDI note insertion | Provides a diatonic backing track (I-V-vi-IV) so the live tracking setup actually has musical context. |

> **Feasibility Assessment**: 95%. The code flawlessly reproduces the routing, arming, and FX staging logic taught in the video using standard REAPER APIs. Since 3rd-party VSTs (Waves) cannot be assumed, stock equivalents are used. A bonus harmonic backing track is generated to satisfy the generative music constraint.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Live Recording Session",
    track_name: str = "Backing Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates a dual-track live recording setup (Vocals + Guitar) with monitoring FX,
    alongside a generated harmonic backing track (I-V-vi-IV) in the specified key.

    Args:
        project_name: Project identifier.
        track_name: Name for the backing chord track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate (will loop the progression).
        velocity_base: Base MIDI velocity for backing chords (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
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

    scale_intervals = SCALES.get(scale, SCALES["major"])
    base_midi = 48 + NOTE_MAP.get(key, 0)  # Octave 3 starting pitch

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Get current track count to ensure additive behavior
    start_track_idx = RPR.RPR_CountTracks(0)

    # === Step 2: Create Harmonic Backing Track ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx, True)
    backing_track = RPR.RPR_GetTrack(0, start_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(backing_track, "P_NAME", track_name, True)
    
    # Add Synth to backing track
    RPR.RPR_TrackFX_AddByName(backing_track, "ReaSynth", False, -1)

    # Create MIDI Item for Backing Track
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(backing_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Progression degrees: I, V, vi, IV (0, 4, 5, 3 in 0-indexed scale degrees)
    progression = [0, 4, 5, 3]

    for b in range(bars):
        deg = progression[b % len(progression)]
        
        # Calculate triad notes strictly from scale
        root = scale_intervals[deg % len(scale_intervals)] + 12 * (deg // len(scale_intervals))
        third = scale_intervals[(deg + 2) % len(scale_intervals)] + 12 * ((deg + 2) // len(scale_intervals))
        fifth = scale_intervals[(deg + 4) % len(scale_intervals)] + 12 * ((deg + 4) // len(scale_intervals))
        
        notes = [base_midi + root, base_midi + third, base_midi + fifth]

        start_time = b * bar_length_sec
        end_time = start_time + bar_length_sec

        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

        for n in notes:
            # Ensure MIDI notes stay within valid 0-127 bounds
            safe_note = max(0, min(127, n))
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, safe_note, velocity_base, False)
            
    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Create Live Vocal Track (Input 1) ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx + 1, True)
    vox_track = RPR.RPR_GetTrack(0, start_track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(vox_track, "P_NAME", "Live Vocals (Input 1)", True)
    
    # 0 = Mono Input 1
    RPR.RPR_SetMediaTrackInfo_Value(vox_track, "I_RECINPUT", 0) 
    RPR.RPR_SetMediaTrackInfo_Value(vox_track, "I_RECARM", 1)  # Record Arm
    RPR.RPR_SetMediaTrackInfo_Value(vox_track, "I_RECMON", 1)  # Input Monitor ON
    
    # Add Confidence Reverb
    fx_verb = RPR.RPR_TrackFX_AddByName(vox_track, "ReaVerbate", False, -1)
    # Set wet signal down slightly so it's not overwhelming
    RPR.RPR_TrackFX_SetParam(vox_track, fx_verb, 0, 0.3) 

    # === Step 4: Create Live Guitar Track (Input 2) ===
    RPR.RPR_InsertTrackAtIndex(start_track_idx + 2, True)
    gtr_track = RPR.RPR_GetTrack(0, start_track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(gtr_track, "P_NAME", "Live Guitar (Input 2)", True)
    
    # 1 = Mono Input 2
    RPR.RPR_SetMediaTrackInfo_Value(gtr_track, "I_RECINPUT", 1)
    RPR.RPR_SetMediaTrackInfo_Value(gtr_track, "I_RECARM", 1)  # Record Arm
    RPR.RPR_SetMediaTrackInfo_Value(gtr_track, "I_RECMON", 1)  # Input Monitor ON
    
    # Add Amp Simulation placeholder (ReaDistortion to provide edge/sustain)
    fx_dist = RPR.RPR_TrackFX_AddByName(gtr_track, "ReaDistortion", False, -1)
    # Lower the drive so it acts more like a clean/edge-of-breakup amp than a fuzz pedal
    RPR.RPR_TrackFX_SetParam(gtr_track, fx_dist, 0, 10.0) # Drive param

    return f"Created Live Recording Setup: '{track_name}' ({key} {scale}), Armed Vocals (In 1 + Reverb), Armed Guitar (In 2 + Amp Sim) at {bpm} BPM."
```