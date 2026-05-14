# Electric Guitar Double-Tracking & Amp Sim Workflow

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Electric Guitar Double-Tracking & Amp Sim Workflow

* **Core Musical Mechanism**: This skill encapsulates the modern workflow for producing heavy electric guitars. It sets up a double-tracked stereo configuration (hard panned Left and Right), applies an Amp Simulation/Distortion FX chain, enables loop-recording, and generates a driving, palm-muted style 8th-note power chord progression. To simulate two distinct recorded takes (as discussed in the tutorial's comping section), the second track features a slight timing delay (Haas effect/humanization) and velocity variance.
* **Why Use This Skill (Rationale)**: A single dry direct-input (DI) guitar sounds thin and sterile. Adding an Amp Simulator provides crucial harmonic saturation (distortion) and speaker cabinet impulses. Furthermore, duplicating the track to create a double-tracked performance panned hard left and right utilizes the stereo field to create a massive "wall of sound." The slight timing differences between the left and right takes trick the brain into hearing a wider, fuller instrument rather than a single point of sound.
* **Overall Applicability**: Essential for rock, metal, pop-punk, and alternative productions where thick, wide rhythm guitars are required. It also serves as a perfect template for tracking live instruments using zero-latency VST monitoring and loop-based "comping".
* **Value Addition**: Transforms a basic synthesized or DI sound into a wide, mix-ready rhythm guitar texture while properly configuring REAPER's timeline for looping and overdubbing.

# Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 1/8th note driving rhythm.
  - **Tempo Range**: 100-160 BPM.
  - **Timing Trick**: The right channel is offset by 15-20 milliseconds with slight velocity differences to simulate a guitarist recording a second distinct "take" (Double Tracking).
  - **Looping**: Project timeline is configured to loop the generated bars automatically.

* **Step B: Pitch & Harmony**
  - **Harmony**: Uses Power Chords (Root + 5th). 
  - **Voicing**: MIDI plays the Root note in the lower register (e.g., C2) and its perfect 5th simultaneously to emulate a guitar fretboard shape.

* **Step C: Sound Design & FX**
  - **Generator**: `ReaSynth` configured as a sawtooth wave (mimicking the raw harmonic content of a guitar string).
  - **Drive**: `JS: Distortion` to add clipping and sustain.
  - **Cabinet/Amp**: `JS: Guitar amp modeler` to filter the harsh high-end of the distortion, simulating the frequency response of a real guitar cabinet. 

* **Step D: Mix & Automation (if applicable)**
  - **Panning**: Track 1 is panned 100% Left (-1.0); Track 2 is panned 100% Right (1.0).
  - **Routing**: Tracks are armed for recording (`I_RECARM = 1`) to emulate the tutorial's readiness state.

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythm & Power Chords | MIDI note insertion | Allows generation of root/fifth chords mathematically derived from the key parameter. |
| Double Tracking | Duplicated iteration with offset | Shifting the Right track by 18ms simulates the human variance of recording multiple takes. |
| Amp Simulation Tone | FX chain (`ReaSynth` → `JS: Distortion` → `JS: Amp Modeler`) | Replicates the "Guitar Rig 5" sound design step using purely native REAPER plugins. |
| Workflow Setup | Transport/Track API | Sets record arming, loop points, and repeat toggle as demonstrated in the tutorial. |

> **Feasibility Assessment**: 90% — While native JS plugins cannot perfectly emulate the tone of Native Instruments Guitar Rig 5, the functional workflow, stereo double-tracking, and harmonic rhythm pattern are 100% accurate to the standard modern rock production methodology discussed.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Electric Guitar",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 105,
    **kwargs,
) -> str:
    """
    Create a Double-Tracked Electric Guitar workflow in REAPER.
    
    Generates a driving 8th-note power chord riff across two hard-panned tracks,
    processed through a distortion and amp modeling chain, and prepares the 
    timeline for loop recording.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks (Left/Right will be appended).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # 7-note scale structures to extract the perfect 5th (index 4)
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9, 12, 14], # padded to avoid index errors
        "pentatonic_minor": [0, 3, 5, 7, 10, 12, 15], 
        "blues":            [0, 3, 5, 6, 7, 10, 12],
    }

    # === Step 1: Set Tempo and Timeline ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars

    # Enable looping (Repeat) and set time selection loop points
    RPR.RPR_GetSetRepeat(1)
    RPR.RPR_GetSet_LoopTimeRange2(0, True, True, 0.0, item_length, False)

    # Resolve notes: Base octave = 2 (MIDI 36 is C2)
    base_midi = 36 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    # Get the 5th interval (usually +7 semitones)
    fifth_interval = scale_intervals[4] if len(scale_intervals) > 4 else 7
    fifth_midi = base_midi + fifth_interval

    # We will generate two tracks to simulate double-tracking (Left and Right)
    pans = [-1.0, 1.0]
    suffixes = ["L", "R"]
    
    for i in range(2):
        # === Step 2: Create Track ===
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        
        # Name track, set panning, and arm for recording
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name} {suffixes[i]}", True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pans[i])
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_RECARM", 1)

        # === Step 3: Add FX Chain (Amp Sim Workflow) ===
        # ReaSynth acts as the raw DI guitar string
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        # JS Distortion acts as the overdrive pedal
        dist_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Distortion", False, -1)
        # JS Guitar Amp Modeler acts as the amp/cab simulator
        amp_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Guitar amp modeler", False, -1)
        
        # Increase distortion gain slightly
        RPR.RPR_TrackFX_SetParam(track, dist_idx, 0, 15.0) # Gain

        # === Step 4: Create MIDI Item & Synthesize Performance ===
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Double tracking simulation: Right track is delayed by 18ms and has slightly lower velocity
        humanize_offset_sec = 0.018 if i == 1 else 0.0
        vel_mod = -5 if i == 1 else 0

        # Generate 8th-note driving power chords
        note_length_sec = (60.0 / bpm) * 0.5  # 8th note duration
        note_duration_sec = note_length_sec * 0.85  # Slight gap for palm-mute separation
        
        for bar in range(bars):
            for eighth in range(8):
                start_sec = (bar * bar_length_sec) + (eighth * note_length_sec) + humanize_offset_sec
                end_sec = start_sec + note_duration_sec
                
                # Convert seconds to Postion in Quarter Notes (PPQ)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
                
                # Accent every downbeat (1, 2, 3, 4)
                velocity = velocity_base + vel_mod if eighth % 2 == 0 else velocity_base - 15 + vel_mod
                velocity = max(1, min(127, int(velocity)))
                
                # Insert Root
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, base_midi, velocity, False)
                # Insert 5th (Power Chord)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, fifth_midi, velocity, False)

    return f"Created double-tracked '{track_name}' (L/R) with Amp Sim workflow over {bars} bars at {bpm} BPM in {key} {scale}."
```