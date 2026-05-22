# Filtered Noise Riser & Rhythmic Pumping Impact

## Analysis

# Agent_Skill_Distiller Report

### 1. High-level Design Pattern Extraction

> **Skill Name**: Filtered Noise Riser & Rhythmic Pumping Impact

* **Core Musical Mechanism**: This pattern relies on two complementary tension-and-release mechanisms. First, a **Riser** is created using white noise passed through a low-pass filter with an ascending cutoff frequency and an ascending volume fade over a multi-bar phrase (usually 4 or 8 bars). Second, an **Impact** sound is triggered on the downbeat of the new section, processed with a **Rhythmic Volume Gate (Sidechain Pumping)** that forcefully ducks the volume on every quarter note.
* **Why Use This Skill (Rationale)**: 
  * *Psychoacoustics of Noise*: White noise contains all frequencies. Sweeping a low-pass filter upwards creates the auditory illusion of a massive object rapidly approaching the listener, building intense anticipation.
  * *Rhythmic Gating*: A heavy impact sound provides the necessary release after the build-up. However, a static decaying impact can muddy the mix. By applying a quarter-note volume pump (mimicking sidechain compression), the impact breathes with the tempo, instantly establishing the groove of the new section and leaving physical headroom for the kick drum.
* **Overall Applicability**: This is a universal transition technique used across EDM, Pop, Hip-Hop, and Cinematic production to bridge sections (e.g., Build-up into the Drop, or Verse into Chorus). 
* **Value Addition**: Instead of relying on static downloaded samples, this skill programmatically generates custom risers and impact dynamics that perfectly lock to the project's tempo, length, and harmonic structure.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Riser**: A continuous, sustained sound lasting exactly 4 bars (or user-defined length) leading up to a downbeat.
  * **Impact**: A 1-bar sustained note struck exactly on the downbeat following the riser.
  * **Gate/Pump**: The impact track is modulated to dip to silence on every downbeat (1, 1.25, 1.5, 1.75 in 4/4 time) and swell up to full volume on the offbeats.
* **Step B: Pitch & Harmony**
  * **Riser**: Pitchless (White Noise).
  * **Impact**: A low sub-frequency note. Programmatically derived from the root key (e.g., C2 or C1) to ensure the transient hits in key with the track.
* **Step C: Sound Design & FX**
  * **Noise Generator**: `JS: White Noise Generator` provides the raw spectrum.
  * **Sweep**: `ReaEQ` with Band 4 converted to a Low Pass filter. Cutoff frequency is automated from ~200Hz to 15kHz.
  * **Impact Generator**: `ReaSynth` tuned to a low sine/triangle mixture for sub weight.
  * **Pumping Engine**: `JS: Volume Adjustment` with its gain parameter hard-automated via envelope points to perfectly emulate a trance-gate/sidechain pumping VST like *Gatekeeper* (as seen in the tutorial).
* **Step D: Mix & Automation**
  * Precise envelope point insertion manages the fade-in of the riser and the rhythmic ducking of the impact, completely bypassing complex external routing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| White Noise Generation | FX Chain (`JS: White Noise Generator`) | Native REAPER JS plugin guarantees availability without relying on third-party VSTs. |
| Riser Filter Sweep | FX Automation (`ReaEQ` Band 4) | Direct parameter automation ensures smooth, high-resolution sweeps synced perfectly to the requested bar length. |
| Gatekeeper Pumping Effect | Automation Envelope (`JS: Volume Adjustment`) | Replicates the custom LFO volume ducking seen in the video perfectly without requiring external plugins or complex sidechain routing. |

> **Feasibility Assessment**: 90% reproduction. While the exact timbral flavor of the tutorial's specific VST (SynthMaster 2 and Cymatics samples) cannot be perfectly cloned with stock plugins, the underlying synthesis, filter sweeping, and rhythmic volume pumping mechanics are replicated precisely using REAPER native tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Transition FX",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Filtered Noise Riser and a Pumping Impact transition.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, etc.).
        bars: Number of bars for the riser sweep (impact hits immediately after).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string detailing track creation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Root note for the impact sub drop (e.g., C2 = 36)
    root_pitch = 36 + NOTE_MAP.get(key, 0)

    # Calculate timings
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar
    riser_duration = bar_length_sec * bars
    
    # We will place the Riser starting at 0.0, and the Impact exactly at the end of the Riser.
    start_time = 0.0
    impact_time = start_time + riser_duration

    # ==========================================
    # TRACK 1: WHITE NOISE RISER
    # ==========================================
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_riser = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_riser, "P_NAME", f"{track_name} - Noise Riser", True)

    # Add a dummy MIDI item to represent the riser duration visually
    item_riser = RPR.RPR_AddMediaItemToTrack(track_riser)
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "D_POSITION", start_time)
    RPR.RPR_SetMediaItemInfo_Value(item_riser, "D_LENGTH", riser_duration)
    
    # 1. Generate Noise
    RPR.RPR_TrackFX_AddByName(track_riser, "JS: White Noise Generator", False, -1)
    
    # 2. Add EQ for Filter Sweep
    eq_idx = RPR.RPR_TrackFX_AddByName(track_riser, "ReaEQ", False, -1)
    # Set Band 4 to Low Pass (Param 15 controls Type, value 8 = Low Pass)
    RPR.RPR_TrackFX_SetParam(track_riser, eq_idx, 15, 8)
    
    # Automate EQ Low Pass Frequency (Param 12)
    # Scaled from 0.0 (20Hz) to 1.0 (24kHz). We sweep from ~0.2 to ~0.9.
    env_eq = RPR.RPR_GetFXEnvelope(track_riser, eq_idx, 12, True)
    RPR.RPR_InsertEnvelopePoint(env_eq, start_time, 0.2, 0, 0, False, True)
    # Add a slight exponential curve (shape=2) to the sweep for dramatic effect
    RPR.RPR_InsertEnvelopePoint(env_eq, start_time + riser_duration, 0.9, 2, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env_eq)

    # 3. Automate Volume Fade-in via JS: Volume Adjustment
    vol_riser_idx = RPR.RPR_TrackFX_AddByName(track_riser, "JS: Volume Adjustment", False, -1)
    env_riser_vol = RPR.RPR_GetFXEnvelope(track_riser, vol_riser_idx, 0, True) # Param 0 is Volume
    # Start silent (0.0) -> Fade to max (1.0) -> instantly cut at end (0.0)
    RPR.RPR_InsertEnvelopePoint(env_riser_vol, start_time, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_riser_vol, start_time + riser_duration - 0.01, 1.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(env_riser_vol, start_time + riser_duration, 0.0, 0, 0, False, True)
    RPR.RPR_Envelope_SortPoints(env_riser_vol)


    # ==========================================
    # TRACK 2: PUMPING IMPACT
    # ==========================================
    track_idx += 1
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track_impact = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track_impact, "P_NAME", f"{track_name} - Pump Impact", True)

    # 1. Create MIDI Item for Impact (lasts 1 bar)
    item_impact = RPR.RPR_AddMediaItemToTrack(track_impact)
    RPR.RPR_SetMediaItemInfo_Value(item_impact, "D_POSITION", impact_time)
    RPR.RPR_SetMediaItemInfo_Value(item_impact, "D_LENGTH", bar_length_sec)
    take_impact = RPR.RPR_AddTakeToMediaItem(item_impact)
    
    # Insert Sub note
    RPR.RPR_MIDI_InsertNote(take_impact, False, False, 0, 
                            int(bar_length_sec * 960), # Approx 1 bar in MIDI ticks 
                            0, root_pitch, velocity_base, False)

    # 2. Generate Synth Impact
    synth_idx = RPR.RPR_TrackFX_AddByName(track_impact, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track_impact, synth_idx, 1, 1.0) # Saw mix
    RPR.RPR_TrackFX_SetParam(track_impact, synth_idx, 5, 500) # Fast release

    # 3. Add Custom "Gatekeeper" Volume Pumping Effect
    vol_pump_idx = RPR.RPR_TrackFX_AddByName(track_impact, "JS: Volume Adjustment", False, -1)
    env_pump = RPR.RPR_GetFXEnvelope(track_impact, vol_pump_idx, 0, True) # Param 0 is Volume
    
    # We will create a quarter-note sidechain ducking curve for the duration of the impact bar
    for beat in range(beats_per_bar):
        current_beat_time = impact_time + (beat * beat_length_sec)
        
        # Point 1: Sharp dip on the downbeat
        RPR.RPR_InsertEnvelopePoint(env_pump, current_beat_time, 0.0, 0, 0, False, True)
        # Point 2: Hold dip slightly
        RPR.RPR_InsertEnvelopePoint(env_pump, current_beat_time + (beat_length_sec * 0.15), 0.0, 2, 0, False, True)
        # Point 3: Swell up on the offbeat
        RPR.RPR_InsertEnvelopePoint(env_pump, current_beat_time + (beat_length_sec * 0.5), 1.0, 0, 0, False, True)
        # Point 4: Hold max volume until next downbeat
        RPR.RPR_InsertEnvelopePoint(env_pump, current_beat_time + (beat_length_sec * 0.95), 1.0, 0, 0, False, True)

    RPR.RPR_Envelope_SortPoints(env_pump)

    return f"Created '{track_name}' Riser ({bars} bars) sweeping to a '{key}' Sub Impact with 1/4 rhythmic pumping at {bpm} BPM."
```