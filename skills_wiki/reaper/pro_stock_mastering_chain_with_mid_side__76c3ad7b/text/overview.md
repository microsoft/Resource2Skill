# Pro Stock Mastering Chain with Mid/Side Processing

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pro Stock Mastering Chain with Mid/Side Processing

* **Core Musical Mechanism**: A comprehensive signal flow for mastering (or master bus processing) using entirely native plugins. The signature of this chain is its multi-stage dynamic control: Subtractive EQ → Soft Clipping → Mid/Side Compression → Bus Glue → Brickwall Limiting. 

* **Why Use This Skill (Rationale)**: 
  - **Soft Clipping before Compression**: By shaving off unmusical, microscopic transient spikes with a clipper (*Event Horizon*), the subsequent compressors don't overreact to peaks, resulting in a louder, cleaner mix without pumping.
  - **Mid/Side Compression**: Encodes the stereo image into Center (Mid) and Edges (Side). Compressing the Mid channel tightens the kick, bass, snare, and lead vocal. Compressing the Side channel separately allows you to control the width, tame harsh cymbals, or push ambient reverbs and wide synths forward without burying the lead vocal.
  - **Serial Processing**: Spreading dynamic reduction across a clipper, two targeted M/S compressors, a stereo bus "glue" compressor, and a limiter yields a much more transparent result than forcing one limiter to do all the work.

* **Overall Applicability**: This should be applied to a "Print Track," "Submix," or "Master Bus" where all instrument and vocal subgroups are routed. It is universally applicable across electronic, pop, and rock genres where loudness, width, and control are required.

* **Value Addition**: Encodes advanced signal flow (Mid/Side matrixing and plugin pin routing) and professional mastering staging into a single, deployable script, saving the user from complex manual I/O configuration.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - Not applicable (Processing FX chain).

* **Step B: Pitch & Harmony**
  - Not applicable.

* **Step C: Sound Design & FX**
  - **1. Subtractive EQ (`ReaEQ`)**: High-Pass Filter at 30Hz to remove inaudible sub-rumble that eats up limiter headroom. Low-Pass Filter at 18kHz to remove harsh digital sizzle.
  - **2. Peak Clipper (`JS: Event Horizon Clipper`)**: Soft clips peaks at -1.0dB ceiling. Threshold at -7.0dB allows it to catch the loudest transients.
  - **3. M/S Matrix (`JS: Mid/Side Encoder & Decoder`)**: Sandwiches the dual compressors, translating Left/Right into Mid/Side and back.
  - **4. Mid Compressor (`ReaComp`)**: Pin-routed to process *only* the left channel (which contains the Mid signal post-encoder). Fast attack (15ms) to catch drum transients, ratio 2.0:1.
  - **5. Side Compressor (`ReaComp`)**: Pin-routed to process *only* the right channel (Side signal). Very fast attack (10ms) to clamp down on wide harshness, ratio 2.5:1. 
  - **6. Glue Compressor (`ReaComp`)**: Standard stereo processing. Slow attack (30ms) to let the punch through, long release (200ms) for smooth pumping, gentle 1.5:1 ratio.
  - **7. Brickwall Limiter (`ReaLimit`)**: Final safety net with a ceiling of -0.7dB to prevent inter-sample clipping on MP3/streaming conversion.

* **Step D: Mix & Automation**
  - Internal plugin pin routing is strictly defined via the REAPER API to isolate processing to specific channels.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| FX Chain Assembly | `RPR_TrackFX_AddByName` | Loads REAPER's native JSFX and VSTs sequentially. |
| Mid/Side Routing | `RPR_TrackFX_SetPinMappings` | Advanced API manipulation to hijack ReaComp's inputs/outputs so it functions as a dedicated Mid or Side processor without needing third-party plugins. |
| Mastering Curves | `RPR_TrackFX_SetParam` | Dials in the exact thresholds, attack times, and EQ frequencies shown in the tutorial. |

> **Feasibility Assessment**: 95% reproducible. The tutorial uses a few free third-party Tukan JSFX (like the Multiband and specific meters), but the underlying *techniques* are perfectly reconstructed using REAPER's native equivalents (ReaComp, ReaEQ). The core M/S architecture and clipping flow is identical.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Mastering Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Pro Stock Mastering Chain with Mid/Side Processing in REAPER.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created mastering track.
        bpm: Tempo in BPM.
        key: Root note (unused for FX chain).
        scale: Scale type (unused for FX chain).
        bars: Number of bars (unused).
        velocity_base: Base velocity (unused).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the constructed mastering chain.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Mastering Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Build the Mastering FX Chain ===

    # 1. ReaEQ - Cleaning extreme lows and highs
    hpf_lpf_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: High-Pass Filter @ 30Hz
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 0, 30.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 3, 4.0)  # Type 4 = HighPass
    # Band 4: Low-Pass Filter @ 18kHz
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 12, 18000.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, hpf_lpf_idx, 15, 3.0)     # Type 3 = LowPass

    # 2. Event Horizon Clipper - Catching stray peaks before compression
    clipper_idx = RPR.RPR_TrackFX_AddByName(track, "Event Horizon Clipper", False, -1)
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 0, -7.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 1, -1.0) # Ceiling
    RPR.RPR_TrackFX_SetParam(track, clipper_idx, 2, 2.0)  # Soft Clip amount

    # 3. Mid/Side Encoder (Translates L/R to M/S on channels 1 & 2)
    enc_idx = RPR.RPR_TrackFX_AddByName(track, "Mid/Side Encoder", False, -1)

    # 4. ReaComp (Mid Compressor)
    mid_comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Pin Routing: Force ReaComp to process ONLY Channel 1 (Mid)
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 0, 0, 0, 1) # Input L <- Ch 1
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 0, 1, 0, 0) # Input R <- None
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 1, 0, 0, 1) # Output L -> Ch 1
    RPR.RPR_TrackFX_SetPinMappings(track, mid_comp_idx, 1, 1, 0, 0) # Output R -> None
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 0, -12.0) # Threshold
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 1, 2.0)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 3, 15.0)  # Attack ms
    RPR.RPR_TrackFX_SetParam(track, mid_comp_idx, 4, 100.0) # Release ms

    # 5. ReaComp (Side Compressor)
    side_comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    # Pin Routing: Force ReaComp to process ONLY Channel 2 (Side)
    # We route Ch 2 into the plugin's Left Input, and output back to Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 0, 0, 0, 2) # Input L <- Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 0, 1, 0, 0) # Input R <- None
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 1, 0, 0, 2) # Output L -> Ch 2
    RPR.RPR_TrackFX_SetPinMappings(track, side_comp_idx, 1, 1, 0, 0) # Output R -> None
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 0, -18.0) # Threshold (sides usually quieter)
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 1, 2.5)   # Ratio
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 3, 10.0)  # Attack ms
    RPR.RPR_TrackFX_SetParam(track, side_comp_idx, 4, 50.0)  # Release ms

    # 6. Mid/Side Decoder (Translates M/S back to L/R)
    dec_idx = RPR.RPR_TrackFX_AddByName(track, "Mid/Side Decoder", False, -1)

    # 7. ReaComp (Stereo Bus Glue)
    glue_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 0, -8.0)  # Threshold
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 1, 1.5)   # Ratio (gentle)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 3, 30.0)  # Attack (slow, lets punch through)
    RPR.RPR_TrackFX_SetParam(track, glue_idx, 4, 200.0) # Release (smooth)

    # 8. ReaLimit (Final Brickwall Limiter)
    limit_idx = RPR.RPR_TrackFX_AddByName(track, "ReaLimit", False, -1)
    RPR.RPR_TrackFX_SetParam(track, limit_idx, 0, -0.5) # Threshold (pushing into limit)
    RPR.RPR_TrackFX_SetParam(track, limit_idx, 1, -0.7) # Ceiling (safe headroom for MP3 conversion)

    return f"Created mastering track '{track_name}' featuring Subtractive EQ, Peak Clipping, discrete M/S Compression, Bus Glue, and Brickwall Limiting."
```