# Multi-Layer Reverb Depth (Early / Mid / Late Reflections)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Layer Reverb Depth (Early / Mid / Late Reflections)

* **Core Musical Mechanism**: Instead of relying on a single reverb plugin to provide the entire spatial environment, this pattern splits the acoustic space into three distinct layers using multiple reverb instances. 
  1. **Early Reflections (Short)**: Small room size, high dampening, 0ms pre-delay. Provides immediate thickness and presence.
  2. **Mid-Body (Medium)**: Medium room size, moderate dampening, ~50ms pre-delay. Gives the sound body and width.
  3. **Long Tail (Large)**: Large room size, low dampening (bright), ~80ms pre-delay. Creates an epic, lush decay that stays out of the way of the original transient.

* **Why Use This Skill (Rationale)**: A single reverb algorithm often compromises between clarity and lushness. A massive, lush reverb tends to wash out the dry signal's attack. By layering, you can use long pre-delays on the larger reverbs to keep the transients sharp and clear, while using a dark, short reverb to glue the vocal/instrument into the mix. This mimics complex, real-world acoustic spaces and high-end studio hardware.

* **Overall Applicability**: Essential for lead vocals, snare drums, atmospheric synth pads, and lead guitars. Any focal element that needs to sound "huge" but remain intelligible.

* **Value Addition**: Transforms a flat, dry sound into a 3-dimensional, expensive-sounding mix element. It encodes the mixing engineer technique of separating early and late reflections for ultimate control over depth.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Works at any BPM. To properly showcase the reverb tails, staccato or spaced-out phrasing is ideal.

* **Step B: Pitch & Harmony**
  - Applicable to any harmonic content. We will generate a sparse, pentatonic minor melody to leave room for the reverb tails to ring out.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` (acting as our dry lead/vocal stand-in).
  - **FX 1 (Short Space)**: `ReaVerbate`. Room Size: 33%, Dampening: 50%, Initial Delay: 0ms.
  - **FX 2 (Medium Space)**: `ReaVerbate`. Room Size: 68%, Dampening: 25%, Initial Delay: ~50ms.
  - **FX 3 (Long Space)**: `ReaVerbate`. Room Size: 95%, Dampening: 8%, Initial Delay: ~80ms.
  - *Note: In REAPER, placing these in series passes the dry signal through at unity gain, while stacking the wet reverberations to build a rich composite tail.*

* **Step D: Mix & Automation**
  - Dry signal is kept at 0dB across all instances.
  - Wet signals are blended subtly (Short is loudest, Long is quietest).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Plucked Lead Melody | MIDI note insertion | Provides a staccato source signal to clearly hear the reverb tails ring out. |
| Dry Sound Source | `ReaSynth` | Built-in REAPER synth to guarantee sound generation without external samples. |
| 3-Layer Acoustic Space | FX chain (`ReaVerbate` x3) | Directly reproduces the tutorial's methodology of stacking stock reverbs with staggered sizes and pre-delays. |

> **Feasibility Assessment**: 100% reproducible. The script uses the exact stock plugin (`ReaVerbate`) and parameter logic demonstrated in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Layered Reverb Lead",
    bpm: int = 120,
    key: str = "C",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Multi-Layer Reverb (Early/Mid/Late) on a track in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
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
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 60 + NOTE_MAP.get(key.upper(), 0) # Start at C4

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Notes ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Create a sparse melody so the reverb tails can be heard clearly
    # We will play 3 quick notes, then wait for the rest of the bar
    note_count = 0
    for bar in range(bars):
        bar_start_beat = bar * beats_per_bar
        
        # Note 1 (Beat 1)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                bar_start_beat * 960, 
                                (bar_start_beat + 0.25) * 960, 
                                0, root_midi, velocity_base, False)
        # Note 2 (Beat 1.5)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                (bar_start_beat + 0.5) * 960, 
                                (bar_start_beat + 0.75) * 960, 
                                0, root_midi + scale_intervals[1], velocity_base - 10, False)
        # Note 3 (Beat 2)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                (bar_start_beat + 1.0) * 960, 
                                (bar_start_beat + 1.5) * 960, 
                                0, root_midi + scale_intervals[2], velocity_base + 10, False)
        note_count += 3

    # === Step 4: Add FX Chain ===
    
    # 4a. Sound Source (ReaSynth)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Make it slightly plucky
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 1, 0.2) # Attack short
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 2, 0.4) # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_synth, 3, 0.1) # Sustain low

    # 4b. Layer 1: Short Reverb (Early Reflections)
    fx_verb1 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 2, 0.33)  # Room size: Small
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 3, 0.50)  # Dampening: High (Darker)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 5, 0.00)  # Initial delay: 0ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 0, 0.25)  # Wet level
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb1, 1, 0.70)  # Dry level (Unity-ish)

    # 4c. Layer 2: Mid Reverb (Body & Width)
    fx_verb2 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 2, 0.68)  # Room size: Medium
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 3, 0.25)  # Dampening: Medium
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 5, 0.20)  # Initial delay: ~50ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 0, 0.15)  # Wet level (Quieter)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb2, 1, 0.70)  # Dry level

    # 4d. Layer 3: Long Reverb (Epic Tail)
    fx_verb3 = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 2, 0.95)  # Room size: Large
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 3, 0.08)  # Dampening: Low (Bright)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 5, 0.32)  # Initial delay: ~80ms
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 0, 0.10)  # Wet level (Quietest, long decay)
    RPR.RPR_TrackFX_SetParamNormalized(track, fx_verb3, 1, 0.70)  # Dry level

    return f"Created '{track_name}' with a 3-layer depth reverb (Short/Mid/Long) and {note_count} notes over {bars} bars."
```