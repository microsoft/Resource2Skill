### 1. High-level Design Pattern Extraction

> **Skill Name**: Evolving Automated Synth Pad

* **Core Musical Mechanism**: The foundational principle extracted from the tutorial is **parameter automation over time** to breathe life into static sounds. While the tutorial focuses on the UI mechanics of "Write," "Touch," and "Latch" modes, the musical result of these tools is the creation of continuous dynamic movement. This skill programmatically generates the *result* of drawn automation—swelling volume, shifting oscillator timbres, and pitch bends—applied to a sustained chord. 

* **Why Use This Skill (Rationale)**: Static synthesizer chords can sound lifeless and digital. By automating parameters like volume, oscillator mix, and tuning over several bars, we introduce macro-dynamics and acoustic realism. A volume swell creates a natural crescendo (tension), while a slow filter or waveform sweep adds timbral evolution that keeps the listener engaged without adding new notes.

* **Overall Applicability**: This technique is perfect for ambient intro pads, cinematic transitions, electronic music breakdowns, and lo-fi hip-hop drones. It acts as a compositional "glue" that fills frequency spectrums while maintaining a sense of forward momentum.

* **Value Addition**: Compared to a blank MIDI clip or a static synth patch, this skill encodes the concept of *automation-driven sound design*. It doesn't just play a chord; it morphs the chord over time, demonstrating how to programmatically grab FX envelopes and draw precise shapes (linear, slow start/end, bezier) without manual fader riding.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: 120 BPM (configurable).
  - **Rhythm**: A single, sustained block chord held for the entire duration (e.g., 4 bars). 
  - **Motion**: The "rhythm" is dictated by the slow, sweeping automation envelopes rather than discrete MIDI note hits.

* **Step B: Pitch & Harmony**
  - **Harmony**: Uses a lush, extended 9th chord (Minor 9th or Major 9th depending on the scale parameter) to provide a rich frequency spectrum. 
  - **Voicing**: Root (Octave 3), Minor/Major 3rd, Perfect 5th, Minor/Major 7th, Major 9th.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth`.
  - **Automation Targets**: 
    - *Volume (Param 0)*: Faded from silence to 80% and back to zero to create a cinematic swell.
    - *Saw Mix (Param 8)*: Crossfades from a pure, warm sine wave into a brighter, harmonically rich sawtooth wave.
    - *Tuning (Param 1)*: A slight pitch-drop (tape stop effect) at the very end of the phrase.

* **Step D: Mix & Automation**
  - Uses `RPR_GetFXEnvelope` with the `create_new=True` flag to force the creation of automation lanes.
  - Inserts points using `RPR_InsertEnvelopePoint` with specific curve shapes (0 = linear, 2 = slow start/end, 5 = bezier).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Pad Harmony | MIDI note insertion | Generates the foundational sustained chord allowing the synth to sound continuously. |
| Sound Source | FX chain (ReaSynth) | Uses REAPER's native synth to ensure 100% compatibility without external VSTs. |
| Evolving Movement | FX Automation Envelopes | The core tutorial focus. Directly grabs parameter envelopes (`RPR_GetFXEnvelope`) and inserts specific curve points to simulate recorded fader movements. |

> **Feasibility Assessment**: 100% reproducible. By translating the manual fader riding demonstrated in the video into programmatic envelope generation, we perfectly capture the musical intent of the tutorial using only REAPER's native ReaScript API and stock plugins.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Evolving Automated Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Evolving Automated Synth Pad in the current REAPER project.
    
    Generates a sustained 9th chord and applies parameter automation 
    to Volume, Timbre (Saw Mix), and Tuning to create evolving movement.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars the pad sustains and evolves.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
    
    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # === Step 3: Add FX (ReaSynth) ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Set base ReaSynth parameters for a pad-like sound
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 0, 0.0) # Volume starts at 0
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 3, 0.1) # Soft Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_idx, 6, 0.8) # Long Release
    
    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    item_length_sec = sec_per_beat * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Calculate pitches for a lush 9th chord
    root_val = NOTE_MAP.get(key.upper(), 0) + 48 # Base Octave 3
    if scale.lower() in ["major", "mixolydian"]:
        chord_intervals = [0, 4, 7, 11, 14] # Major 9
    else:
        chord_intervals = [0, 3, 7, 10, 14] # Minor 9
        
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length_sec)
    
    for interval in chord_intervals:
        pitch = min(127, max(0, root_val + interval))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base)
        
    RPR.RPR_MIDI_Sort(take)
    
    # === Step 5: Automate Parameters (The Core Skill) ===
    # Envelope Shapes: 0=Linear, 1=Square, 2=Slow Start/End, 5=Bezier
    
    # 1. Automate Volume (Param 0): Swell in and fade out
    env_vol = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    if env_vol:
        RPR.RPR_InsertEnvelopePoint(env_vol, 0.0, 0.0, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length_sec * 0.25, 0.7, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length_sec * 0.75, 0.7, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, item_length_sec, 0.0, 2, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    # 2. Automate Saw Wave Mix (Param 8): Morph timbre from sine to sawtooth
    env_saw = RPR.RPR_GetFXEnvelope(track, fx_idx, 8, True)
    if env_saw:
        RPR.RPR_InsertEnvelopePoint(env_saw, 0.0, 0.0, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_saw, item_length_sec * 0.5, 0.8, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_saw, item_length_sec, 0.0, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_saw)
        
    # 3. Automate Tuning (Param 1): Tape-stop pitch drop at the end (0.5 is center)
    env_tune = RPR.RPR_GetFXEnvelope(track, fx_idx, 1, True)
    if env_tune:
        RPR.RPR_InsertEnvelopePoint(env_tune, 0.0, 0.5, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_tune, item_length_sec - sec_per_beat, 0.5, 5, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_tune, item_length_sec, 0.35, 0, 0.0, False, True)
        RPR.RPR_Envelope_SortPoints(env_tune)
        
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with 3 automated FX envelopes (Volume, Timbre, Pitch) over {bars} bars at {bpm} BPM."
```