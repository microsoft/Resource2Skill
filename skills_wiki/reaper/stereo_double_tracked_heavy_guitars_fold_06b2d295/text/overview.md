# Stereo Double-Tracked Heavy Guitars (Folder Bus Routing)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Stereo Double-Tracked Heavy Guitars (Folder Bus Routing)

* **Core Musical Mechanism**: The signature technique of modern metal and heavy rock production: recording two distinct performances of the exact same riff, panning one 100% Left and the other 100% Right, and grouping them under a single "Parent" folder track. The parent track houses the stereo Amp Simulation (and EQ/compression), combining the dual performances into a single, cohesive "wall of sound."
* **Why Use This Skill (Rationale)**: Double-tracking relies on psychoacoustics. Because the two performances are played by a human, there are microscopic discrepancies in timing (transients) and velocity between the left and right channels. The human ear interprets these differences as massive stereo width. Bussing them to a single Parent Folder ensures they are processed through the same virtual "amp cabinet," gluing them together tonally while cutting CPU usage in half compared to running dual mono amp sims. 
* **Overall Applicability**: Essential for rhythm guitars in Metal, Hard Rock, Punk, and dense Pop productions. It leaves the phantom center of the stereo field completely empty, creating space for the kick drum, bass guitar, snare, and lead vocals to cut through clearly.
* **Value Addition**: Compared to just copying a MIDI clip (which only makes the signal louder and phasey in mono), this skill programmatically mimics human double-tracking by introducing randomized timing offsets (the Haas effect sweet spot, 5-25ms) and velocity variations to the right channel, simulating a true second take.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: Typically 130–180 BPM (tutorial uses 170 BPM for a syncopated, aggressive feel).
  - **Grid/Rhythm**: 16th note subdivisions. The riff relies on quick, palm-muted pedal tones on the 16th notes, punctuated by longer 8th-note power chords on syncopated off-beats.
  - **Humanization**: The right-panned track is shifted by a random continuous offset (5–20ms) and has slight velocity variance to generate a wide stereo phase difference.

* **Step B: Pitch & Harmony**
  - **Scale/Key**: Phrygian or Minor scale (using the Root, Minor 3rd, Perfect 4th, and Diminished 5th/Tritone).
  - **Voicings**: Single "chug" notes on the root, expanding into Power Chords (Root + Perfect 5th) to create harmonic weight and accenting.

* **Step C: Sound Design & FX**
  - **Child Tracks (L & R)**: Raw tone generators (ReaSynth blending Saw and Square waves) to mimic the unamplified DI (Direct Injection) signal of electric guitar strings.
  - **Parent Folder Track**: `JS: Distortion` and `ReaEQ` applied to the bus. The distortion drives the combined stereo signal, and the EQ acts as a primitive Cabinet Simulator (rolling off extreme highs and lows).

* **Step D: Mix & Automation**
  - **Routing**: Track 1 is set as a Folder Parent (`I_FOLDERDEPTH = 1`). Track 2 is standard (`0`) and Track 3 ends the folder (`-1`).
  - **Panning**: Child 1 is panned hard left (`-1.0`); Child 2 is panned hard right (`1.0`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Folder Bus Routing** | `RPR_SetMediaTrackInfo_Value` (`I_FOLDERDEPTH`) | Programmatically recreates the REAPER folder architecture the tutorial teaches for routing double-tracks. |
| **Stereo Width** | Track panning (`D_PAN`) & Python `random` | Hard panning combined with programmatic micro-timing shifts mimics human dual-take performance accurately. |
| **Amp Simulation** | FX Chain on Parent Track | Replicates the architectural lesson of grouping tracks to process them through a single stereo instance of an amp sim. |
| **Metal Riff** | `RPR_MIDI_InsertNote` | Computes root notes and perfect 5ths mathematically to match the selected key. |

> **Feasibility Assessment**: 85%. The routing architecture, stereo widening, and MIDI timing logic perfectly mimic the production workflow taught. The remaining 15% is tonal: we are using stock ReaSynth and JS plugins to simulate the highly complex, premium Fortin Nameless Suite VST shown in the video. The structural and musical lessons, however, are fully intact.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Heavy Guitars",
    bpm: int = 170,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create Stereo Double-Tracked Heavy Guitars via Folder Routing.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (ignored here, riff explicitly uses Phrygian/Blues intervals).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created tracks and routing.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    # C2 as the base chug octave for metal
    root_pitch = NOTE_MAP.get(key, 0) + 36 

    # === Step 2: Create Folder Structure ===
    track_idx = RPR.RPR_CountTracks(0)
    
    # Parent Track (Amp Sim Bus)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    parent_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name + " Bus", True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1.0)
    
    # Child Take 1 (Hard Left)
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    child_l = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(child_l, "P_NAME", track_name + " L", True)
    RPR.RPR_SetMediaTrackInfo_Value(child_l, "I_FOLDERDEPTH", 0.0)
    RPR.RPR_SetMediaTrackInfo_Value(child_l, "D_PAN", -1.0) 
    
    # Child Take 2 (Hard Right)
    RPR.RPR_InsertTrackAtIndex(track_idx + 2, True)
    child_r = RPR.RPR_GetTrack(0, track_idx + 2)
    RPR.RPR_GetSetMediaTrackInfo_String(child_r, "P_NAME", track_name + " R", True)
    RPR.RPR_SetMediaTrackInfo_Value(child_r, "I_FOLDERDEPTH", -1.0) # Closes the folder
    RPR.RPR_SetMediaTrackInfo_Value(child_r, "D_PAN", 1.0) 

    # === Step 3: Add FX Chains ===
    # Add Amp Sim placeholders to the Parent Track
    RPR.RPR_TrackFX_AddByName(parent_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaEQ", False, -1)
    
    # Add raw tone generators to the Child Tracks to simulate raw guitar DI
    for child in [child_l, child_r]:
        synth_idx = RPR.RPR_TrackFX_AddByName(child, "ReaSynth", False, -1)
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 0, 0.15) # Volume
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 2, 0.6)  # Add Square mix for grit
        RPR.RPR_TrackFX_SetParam(child, synth_idx, 3, 0.8)  # Add Saw mix for brightness

    # === Step 4: Create MIDI Riff Pattern ===
    # Tuple format: (start_beat, length_beats, pitch_offset_from_root, is_power_chord)
    pattern = [
        (0.0, 0.25, 0, False), # 16th note palm mute
        (0.25, 0.25, 0, False),
        (0.5, 0.5, 3, True),   # 8th note minor 3rd power chord
        (1.0, 0.25, 0, False),
        (1.25, 0.25, 0, False),
        (1.5, 0.5, 5, True),   # 8th note Perfect 4th power chord
        (2.0, 0.25, 0, False),
        (2.25, 0.25, 0, False),
        (2.5, 0.5, 6, True),   # 8th note Diminished 5th power chord (Tritone)
        (3.0, 0.5, 0, False),  # 8th note palm mute
        (3.5, 0.5, 5, True),   # 8th note Perfect 4th power chord
    ]
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    def create_take_for_track(track, is_right_track):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for bar in range(bars):
            bar_offset = bar * beats_per_bar
            for p in pattern:
                start_beat, length_beats, pitch_offset, is_power_chord = p
                
                # Calculate absolute time in seconds
                start_time = (bar_offset + start_beat) * (60.0 / bpm)
                end_time = start_time + (length_beats * (60.0 / bpm))
                
                # The "Double Track" Magic: Humanize timing for the Right track 
                # This creates the stereo width (Haas effect) when panned
                if is_right_track:
                    start_time += random.uniform(0.005, 0.025)
                    end_time += random.uniform(0.005, 0.025)
                
                # Convert project time to MIDI PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
                
                # Dynamic Velocity humanization
                vel = velocity_base if not is_power_chord else min(127, velocity_base + 20)
                if is_right_track:
                    vel = max(1, min(127, vel + random.randint(-12, 12)))
                else:
                    vel = max(1, min(127, vel + random.randint(-4, 4)))
                    
                base_note = root_pitch + pitch_offset
                notes_to_add = [base_note]
                
                if is_power_chord:
                    notes_to_add.append(base_note + 7) # Add Perfect 5th interval
                    
                for note in notes_to_add:
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(note), int(vel), False)
                    
        RPR.RPR_MIDI_Sort(take)

    # Generate both "takes"
    create_take_for_track(child_l, False)
    create_take_for_track(child_r, True)

    return f"Created '{track_name} Bus' folder with hard-panned L/R simulated double-tracked guitars over {bars} bars at {bpm} BPM."
```