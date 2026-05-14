# Parallel Rock Bass Mixing Chain (Growl & Sub)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Parallel Rock Bass Mixing Chain (Growl & Sub)

* **Core Musical Mechanism**: This pattern addresses the classic mixing problem where a bass guitar needs to provide a solid, unwavering low-end foundation while simultaneously cutting through a dense rock mix. The solution is a dual-path architecture: 
  1. A **Main Track** heavily compressed for dynamic consistency and EQ'd to boost sub/low-mids.
  2. A **Parallel Track** (duplicate or send) heavily saturated/distorted to generate upper-order harmonics (growl), which is then blended quietly underneath the main track.

* **Why Use This Skill (Rationale)**: Distortion natively compresses and shapes EQ, but it often destroys fundamental low-end frequencies, making the bass sound "small" and "farty." By isolating the distortion on a parallel track, psychoacoustics work in our favor: the listener's brain merges the clean sub from the main track and the harmonic grit from the parallel track into a single, massive, aggressive bass instrument.

* **Overall Applicability**: Essential for Rock, Pop-Punk, Metal, and driving Indie mixes. It is also highly effective on synth basses (808s, Reese basses) in EDM and Hip-Hop when they need to translate well on small phone/laptop speakers (the upper harmonics trick the ear into hearing the missing fundamental).

* **Value Addition**: This skill moves beyond simply inserting notes; it encodes a professional mix-engineering routing architecture (parallel processing) and specific tonal shaping strategies (post-compression EQing for weight and presence).


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 110-140 BPM (standard driving rock tempo).
  - **Rhythm**: Straight driving 1/8th notes.
  - **Articulation**: Mostly legato with a slight gap (e.g., 90% note duration) to define the transient attack.

* **Step B: Pitch & Harmony**
  - **Pitch**: Anchored to the root note of the specified key, placed in the bass register (Octave 1 or 2).
  - **Velocity**: Consistently hard (110-120) to trigger the compressor and drive the parallel distortion track.

* **Step C: Sound Design & FX**
  - **Source**: A basic synthesizer (ReaSynth) acting as the bass source.
  - **Main FX Chain**: 
    - *Compressor (ReaComp)*: 4:1 Ratio, Threshold set to catch peaks (-15dB), medium attack (~20ms) to let the pick/finger transient through, ~300ms release to let it breathe.
    - *EQ (ReaEQ)*: Placed *after* compression. +5dB Low Shelf at ~200Hz for weight. +4dB Peak at ~2.5kHz for attack/string noise.
  - **Parallel FX Chain**:
    - *Overdrive (JS: Distortion)*: Driven hard to create square-wave-like harmonics.

* **Step D: Mix & Automation**
  - The Main Bass track is set to unity gain (0dB).
  - The Distorted Bass track is blended at approximately -12dB (25% volume) to add texture without overpowering the fundamental.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Driving Bass Rhythm | MIDI note insertion | Provides the consistent transient source material needed to demonstrate the mixing technique. |
| Dynamic Control & EQ | FX Chain (`ReaComp`, `ReaEQ`) | Exactly replicates the tutorial's tonal shaping workflow on the main signal. |
| Parallel Harmonics | Track Routing + `JS: Distortion` | Creates an auxiliary track and routes the main signal to it, mirroring the tutorial's track-duplication technique for clean blending. |

> **Feasibility Assessment**: 85% reproduction. The architectural concept, MIDI generation, and stock plugin routing are perfectly replicated. The tutorial uses a specific third-party plugin (TSE BOD) for the distortion, which is substituted here with REAPER's stock `JS: Distortion` to guarantee the code executes cleanly on any machine.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rock Bass",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 115,
    **kwargs,
) -> str:
    """
    Create a Parallel Rock Bass Mixing Chain in REAPER.
    Generates a driving 8th-note bassline and sets up a dual-track 
    (Main + Parallel Distortion) processing architecture.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Calculate root note in the bass register (Octave 1)
    # C1 is MIDI note 24.
    root_note = NOTE_MAP.get(key, 4) + 24 

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Main Bass Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    main_track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(main_track, "P_NAME", f"{track_name} Main", True)

    # === Step 3: Create MIDI Item & Driving 8th Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(main_track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Insert straight 8th notes
    total_notes = bars * 8
    beat_len = 60.0 / bpm
    eighth_len = beat_len / 2.0
    
    for i in range(total_notes):
        start_time = i * eighth_len
        # 90% duration for a slight gap between picked notes
        end_time = start_time + (eighth_len * 0.9) 
        
        # Convert seconds to MIDI ticks (Project PPQ is typically 960)
        start_qn = RPR.RPR_TimeMap2_timeToQN(0, start_time)
        end_qn = RPR.RPR_TimeMap2_timeToQN(0, end_time)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_note, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Main FX Chain (Synth -> Comp -> EQ) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaSynth", False, -1)
    
    # Add Compressor
    comp_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaComp", False, -1)
    # Set explicit normalized values for demonstration (Threshold down, Ratio 4:1)
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 0, 0.6) # Threshold
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 1, 0.1) # Ratio
    RPR.RPR_TrackFX_SetParam(main_track, comp_idx, 2, 0.02) # Attack (~20ms)
    
    # Add EQ
    eq_idx = RPR.RPR_TrackFX_AddByName(main_track, "ReaEQ", False, -1)
    # Set explicit normalized values for Low Shelf and Mid Peak
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 0, 0.15) # Freq 1 (~200Hz)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 1, 0.65) # Gain 1 (+5dB)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 3, 0.5)  # Freq 2 (~2.5kHz)
    RPR.RPR_TrackFX_SetParam(main_track, eq_idx, 4, 0.6)  # Gain 2 (+4dB)

    # === Step 5: Create Parallel Distortion Track ===
    RPR.RPR_InsertTrackAtIndex(track_idx + 1, True)
    dist_track = RPR.RPR_GetTrack(0, track_idx + 1)
    RPR.RPR_GetSetMediaTrackInfo_String(dist_track, "P_NAME", f"{track_name} Dist", True)
    
    # Set Parallel Track Volume to ~ -12dB (linear 0.25) to tuck it under the main mix
    RPR.RPR_SetMediaTrackInfo_Value(dist_track, "D_VOL", 0.25)
    
    # Add Distortion Plugin
    dist_idx = RPR.RPR_TrackFX_AddByName(dist_track, "JS: Distortion", False, -1)
    RPR.RPR_TrackFX_SetParam(dist_track, dist_idx, 0, 0.8) # Drive it hard

    # === Step 6: Route Main Track to Parallel Track ===
    # 0 = Post-Fader, 1 = Pre-FX, 3 = Post-FX
    RPR.RPR_CreateTrackSend(main_track, dist_track)

    return f"Created Parallel Bass Architecture: '{track_name} Main' routed to '{track_name} Dist' blending {total_notes} notes over {bars} bars."
```