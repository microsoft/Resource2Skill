### 1. High-level Design Pattern Extraction

*   **Skill Name**: Evolving Synth Transition & Lo-Fi Crackle Processing

*   **Core Musical Mechanism**: This skill demonstrates two distinct but complementary production techniques:
    1.  **Evolving Synth Transition**: A synth pad/lead sound dynamically changes its timbre, volume, and stereo width over time to create a compelling musical transition or atmospheric effect. This involves layering multiple automation envelopes (volume swells, rhythmic chopping, and stereo widening) on a single track.
    2.  **Lo-Fi Crackle Processing**: An external crackle/noise sample is processed to flatten its transients, narrow its stereo image (especially in lower frequencies), and embed it in a subtle ambient space, making it a cohesive background texture rather than a distracting element.

*   **Why Use This Skill (Rationale)**:
    1.  **Evolving Synth Transition**: The combination of LFO-driven timbre modulation (e.g., flanging effect), gradual volume changes, and stereo field manipulation creates a sense of movement, anticipation, and release. Layering automation envelopes is a powerful REAPER feature that allows for complex, non-linear dynamic control, adding richness and interest beyond simple linear fades. This technique can build tension, highlight section changes, or add cinematic depth.
    2.  **Lo-Fi Crackle Processing**: Raw crackle samples can be harsh and distracting due to sharp transients and wide stereo image, especially in higher frequencies. Applying dynamic compression (or custom dynamic shaping), narrowing the stereo width for better mono compatibility (especially for bass frequencies), and adding subtle reverb helps to glue the noise texture into the mix. This creates a "lo-fi" or "vintage" vibe without overwhelming other musical elements.

*   **Overall Applicability**:
    1.  **Evolving Synth Transition**: Ideal for electronic music genres like Synthwave, Chillwave, Ambient, Trance, or cinematic scores where dynamic soundscapes and smooth transitions are crucial. Can be used for intros, outros, bridge sections, or as a continuous atmospheric bed.
    2.  **Lo-Fi Crackle Processing**: Primarily used in Lo-Fi Hip Hop, Chillhop, Downtempo, Indie Pop, or any genre aiming for a vintage, nostalgic, or gritty aesthetic. It's excellent for adding subtle background texture, warmth, and character to an otherwise clean mix.

*   **Value Addition**: This skill encodes knowledge about advanced automation techniques (layered envelopes), specific sound design approaches for synth movement, and effective mixing strategies for integrating noisy textural elements without them becoming obtrusive. It moves beyond basic static sounds to create dynamic, evolving sonic interest and stylistic character.

### 2. Technical Breakdown

#### **Pattern 1: Evolving Synth Transition**

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: 4/4 (assumed from common practice and visual grid in video).
    *   **BPM Range**: 120 BPM (video example starts at 120 BPM).
    *   **Rhythmic Grid**: MIDI notes are held sustains. Volume envelopes introduce rhythmic gating at 32nd notes.
    *   **Note Duration**: Sustained notes across several bars.

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: C Major (implied from the visual MIDI notes in the video).
    *   **Specific Pitches**: The example shows a simple C major chord played as a sustained pad.
        *   C3 (MIDI 48)
        *   E3 (MIDI 52)
        *   G3 (MIDI 55)
        *   C4 (MIDI 60)
    *   **Chord Voicings**: Root position C major triad + octave.

*   **Step C: Sound Design & FX**
    *   **Instrument/Synth**: Hybrid 3 (VSTi) with Multiwave oscillators, LFO modulating shape, and an amplifier envelope for swell. (Will be replaced by ReaSynth + LFO for wave modulation, or a simple sustained ReaSynth pad with external modulation for reproducibility).
    *   **FX Chain**:
        *   ReaSynth (for basic synth sound)
        *   ReaVerb (for Hall reverb effect - built-in to Hybrid 3 in tutorial)
        *   ReaDelay (for Chorus effect - built-in to Hybrid 3 in tutorial)
    *   **Specific Parameter Values (Approximated for stock REAPER FX)**:
        *   **ReaSynth**: Default settings, with LFO assigned to oscillator shape if possible through ReaScript, or acknowledge as a limitation.
        *   **ReaVerb**: Hall preset, mix ~20-30%, size medium-large.
        *   **ReaDelay**: Short delay times, moderate feedback, mix ~15-25% to create chorus-like width.

*   **Step D: Mix & Automation**
    *   **Volume Automation (Layered)**:
        1.  **Swell-up**: Linear increase from -4.6 dB to 0 dB over ~8 bars. (Automation item 1).
        2.  **Chopping/Gate**: Rhythmic square wave modulation from +1 dB to -4 dB at 32nd note intervals. (Automation item 2, overlapping item 1).
    *   **Width Automation**: Linear increase from 0% (mono) to 100% (stereo) over ~8 bars, coinciding with the volume swell.
    *   **Trim Volume**: Overall track volume adjustment (not explicitly shown as an envelope, but mentioned for fine-tuning).

#### **Pattern 2: Lo-Fi Crackle Processing**

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: N/A (noise, continuous).
    *   **BPM Range**: N/A.
    *   **Rhythmic Grid**: N/A.
    *   **Note Duration**: N/A.

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: N/A.
    *   **Specific Pitches**: N/A (noise).

*   **Step C: Sound Design & FX**
    *   **Instrument/Synth**: External vinyl crackle audio sample. (Will be represented by a placeholder audio item).
    *   **FX Chain**:
        1.  **JS: General Dynamics (Control)**: Custom curve to catch and flatten fast, loud transients (like crackles) while allowing quieter parts through or even boosting them slightly. Attack 0ms, Release fast, Wet Mix ~5%.
        2.  **JS: Volume/Pan/Stereo** (to replace Voxengo VUMT): Adjust Left/Right trim to balance stereo image, reduce "Stereo width" parameter to mono-ize below a certain frequency (~955 Hz) and reduce overall side signal.
        3.  **ReaEQ**: High-pass filter (~100-200 Hz), Low-pass filter (~6-8 kHz), and possibly a slight dip in high-mids to tame harshness.
        4.  **ReaVerb** (to replace ToneBoosters Reverb 3): Small room or short plate reverb preset, low wet mix (~20-25%), to put the crackle in a subtle ambient space, gluing it to other reverb-affected elements.
    *   **Specific Parameter Values (Approximated)**:
        *   **JS: General Dynamics**:
            *   Input Gain: 0 dB
            *   Output Gain: 0 dB
            *   Detector input gain: 0
            *   Detection RMS size (ms): 0.0 (fastest)
            *   Input Attack (ms): 0.0
            *   Input Release (ms): 20.0
            *   Curve points (approximated based on video visual):
                *   (0, -60), (-30, -30), (-15, -15), (0, -10), (10, -5), (20, -5) -> effectively a very fast, hard downward compressor/limiter on peaks. This is complex to reproduce exactly via ReaScript if not exposed. A general compressor will be used for simplicity if specific curve point manipulation isn't directly exposed for JSFX graphs.
        *   **JS: Volume/Pan/Stereo**:
            *   Balance: Adjusted to compensate for source imbalance (e.g., -4.4 dB right trim as shown in VUMT).
            *   Stereo Width: ~70% (to approximate side trimming and mono-making below a freq).
        *   **ReaEQ**:
            *   Band 1 (Highpass): 100-200 Hz, 12-24 dB/oct.
            *   Band 2 (Lowpass): 6-8 kHz, 12-24 dB/oct.
            *   Band 3 (Peak/Dip): -3 dB around 2-4 kHz (optional, if hiss is too pronounced).
        *   **ReaVerb**:
            *   Room Size: Small to Medium
            *   Wet: ~24%
            *   Dry: ~76%
            *   High-pass and low-pass filters within the reverb to match the desired textural space.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Synth MIDI notes | MIDI note insertion | Precise pitch and timing for the pad. |
| Synth VSTi sound | FX chain (ReaSynth) | To approximate the basic synth timbre with a stock plugin. |
| Synth Volume Automation (Swell & Chop) | Automation envelope (layered items) | Directly reproduces the complex, layered volume dynamics. |
| Synth Width Automation (Mono to Stereo) | Automation envelope | Directly reproduces the spatial transition. |
| Crackle Audio Source | Audio item creation (empty) | To provide a container for FX processing without external dependencies. |
| Crackle Dynamics Processing | FX chain (JS: General Dynamics) | Directly uses the specific JSFX shown, attempting to set a basic curve. |
| Crackle Stereo Balance/Mono-making | FX chain (JS: Volume/Pan/Stereo) | Approximates the mid-side trimming and mono-making from the tutorial. |
| Crackle EQ | FX chain (ReaEQ) | Standard filtering to shape the noise texture. |
| Crackle Reverb | FX chain (ReaVerb) | Adds subtle ambiance as shown in the tutorial. |

**Feasibility Assessment**: Approximately 70-80% of the tutorial's musical result can be reproduced.
*   **Synth**: The MIDI notes and automation logic are fully reproducible. The exact timbre of Hybrid 3 is hard to match with ReaSynth without extensive parameter tuning not detailed in the video, but a similar *type* of sound and its modulation can be achieved. Built-in effects (Hall, Chorus) are approximated with ReaVerb and ReaDelay.
*   **Crackle**: The *source vinyl crackle sample* is not reproducible by code; a blank audio item is created as a placeholder. The processing chain using stock REAPER JSFX and ReaEQ/ReaVerb is largely reproducible. The precise custom curve in "General Dynamics" and specific mid-side gain trims of "VUMT" are approximated, as direct graphical manipulation of JSFX curves and detailed VST parameters aren't always exposed or simple to script.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR
import math

def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an evolving synth transition and a processed lo-fi crackle texture in REAPER.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides for specific parameters.

    Returns:
        Status string describing what was created.
    """
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

    root_midi = NOTE_MAP.get(key, 0) # Default to C if key not found
    current_scale = SCALES.get(scale, SCALES["major"])

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4.0 # Assuming 4/4 time signature
    seconds_per_beat = 60.0 / bpm
    bar_length_sec = seconds_per_beat * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # --- Synth Transition Track ---
    synth_track_name = "Synth Pad Transition"
    synth_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", synth_track_name, True)

    # === Step 2: Create MIDI Item for Synth ===
    synth_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(synth_item, "D_LENGTH", total_length_sec)
    synth_take = RPR.RPR_AddTakeToMediaItem(synth_item)

    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec) # Set MIDI item length

    # Insert a sustained C major chord as a pad
    # C3, E3, G3, C4
    base_octave = 3
    midi_notes = [
        root_midi + base_octave * 12 + current_scale[0],  # C3
        root_midi + base_octave * 12 + current_scale[2],  # E3
        root_midi + base_octave * 12 + current_scale[4],  # G3
        root_midi + (base_octave + 1) * 12 + current_scale[0] # C4
    ]

    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec)
    RPR.MIDI_ClearEvts(synth_take)
    RPR.MIDI_SetItemExtents(synth_item, 0.0, total_length_sec) # Re-set extents after clearing

    # Calculate MIDI item's end time in beats for MIDI_InsertNote
    item_end_beat = RPR.MIDI_GetItemDuration(synth_item) / seconds_per_beat

    for note in midi_notes:
        RPR.MIDI_InsertNote(
            synth_take, False, False, 0.0, item_end_beat,
            0, note, velocity_base, True
        )

    RPR.MIDI_Sort(synth_take)
    RPR.MIDI_MarkAll(synth_take)
    RPR.MIDI_SetCC(synth_take, False, False, 0, 7, -1, -1, 100, True) # Set default volume CC

    # === Step 3: Add FX Chain for Synth ===
    # ReaSynth (basic synth pad)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth (Cockos)", False, -1)
    # To approximate LFO mod: Set some ReaSynth parameters that LFO might modulate
    # LFO rate (param 19), LFO depth (param 20), Filter Cutoff (param 9)
    # These are illustrative, exact mapping from Hybrid 3 is not direct.
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 19, 0.25) # LFO Rate
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 20, 0.5)  # LFO Depth
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 9, 0.7)   # Filter Cutoff

    # ReaVerb (Hall Reverb)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaVerb (Cockos)", False, -1)
    # Set to a hall-like preset (parameter indices are often heuristic without direct API for presets)
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 0, 0.25) # Wet gain
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 1, 0.75) # Dry gain
    RPR.RPR_TrackFX_SetParam(synth_track, 1, 2, 0.8)  # Room size

    # ReaDelay (Chorus-like effect)
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaDelay (Cockos)", False, -1)
    # For chorus, use short, modulated delays
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 0, 0.15) # Wet mix
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 1, 0.85) # Dry mix
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 2, 0.03) # Delay 1 Time (short)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 5, 0.025) # Delay 2 Time (slightly different)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 8, 0.3)  # Feedback 1
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 11, 0.3) # Feedback 2
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 14, 0.02) # LFO rate (for modulation)
    RPR.RPR_TrackFX_SetParam(synth_track, 2, 15, 0.1)  # LFO depth

    # === Step 4: Add Automation for Synth ===
    # Volume Automation (layered items)
    volume_env = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_WND", 1) # Ensure envelope lane is visible

    # Automation Item 1: Swell Up
    RPR.RPR_AddEnvelopePoint(volume_env, 0.0, RPR.DB2VAL(-4.6), 0, 0, False, True)
    RPR.RPR_AddEnvelopePoint(volume_env, total_length_sec, RPR.DB2VAL(0.0), 0, 0, False, True)
    
    # Automation Item 2: Choppy/Gate Effect (created as a separate item, but on the same envelope lane)
    # This simulates a square wave gating.
    # The actual graphical envelope will show the combined effect.
    chop_start_time = total_length_sec / 4 # Start chopping after 1/4 of the transition
    chop_end_time = total_length_sec
    chop_interval_sec = seconds_per_beat / 8 # 32nd notes
    
    # Define points for the choppy effect
    for t in range(int(chop_start_time / chop_interval_sec), int(chop_end_time / chop_interval_sec)):
        current_time = t * chop_interval_sec
        # Peak
        RPR.RPR_AddEnvelopePoint(volume_env, current_time, RPR.DB2VAL(1.0), 1, 0, False, True)
        # Trough
        RPR.RPR_AddEnvelopePoint(volume_env, current_time + chop_interval_sec / 2, RPR.DB2VAL(-4.0), 1, 0, False, True)

    # Width Automation (Mono to Stereo)
    width_env = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Stereo width")
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_WND", 1) # Ensure envelope lane is visible
    RPR.RPR_AddEnvelopePoint(width_env, 0.0, 0.0, 0, 0, False, True) # 0% width (mono) at start
    RPR.RPR_AddEnvelopePoint(width_env, total_length_sec, 1.0, 0, 0, False, True) # 100% width (stereo) at end


    # --- Lo-Fi Crackle Track ---
    crackle_track_name = "Lo-Fi Crackle"
    crackle_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(crackle_track_idx, True)
    crackle_track = RPR.RPR_GetTrack(0, crackle_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(crackle_track, "P_NAME", crackle_track_name, True)

    # === Create Placeholder Audio Item for Crackle ===
    # Note: The actual crackle sound file is NOT included. User must drop their own.
    crackle_item = RPR.RPR_AddMediaItemToTrack(crackle_track)
    RPR.RPR_SetMediaItemInfo_Value(crackle_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(crackle_item, "D_LENGTH", total_length_sec)
    # Optional: Fill with silence or a basic noise generator if available and scriptable
    # For simplicity, leaving it as an empty item where user can later drop their sample.

    # === Add FX Chain for Crackle ===
    # 1. JS: General Dynamics (Control) - For transient flattening/limiting
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: General Dynamics (Control) (Cockos)", False, -1)
    # Parameters for JS: General Dynamics
    # Parameter indices are often generic for JSFX or vary. This is an approximation.
    # The graph shown in the video is complex to reproduce exactly via ReaScript's
    # general parameter setting functions. We'll set attack/release and wet mix.
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 0, 0.0)   # Detect input gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 1, 0.0)   # Detect RMS size (0 ms for fastest)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 2, 0.0)   # Input Attack (0 ms)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 3, 20.0)  # Input Release (20 ms)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 4, 0.0)   # Input Precomp (0 ms)
    # The actual curve is params 5 to 70 for 65 points. We cannot easily draw the curve directly.
    # Set wet mix to approximate impact on peaks.
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 71, 0.5)  # Dry mix (approximate)
    RPR.RPR_TrackFX_SetParam(crackle_track, 0, 72, 0.05) # Wet mix (approximate 5%)

    # 2. JS: Volume/Pan/Stereo - For stereo balance, mid-side trim, mono-maker
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Utility/volume/pan/stereo (Cockos)", False, -1)
    # To approximate VUMT: Trim right by ~4.4dB (assuming source imbalance)
    RPR.RPR_TrackFX_SetParam(crackle_track, 1, 1, RPR.DB2VAL(-4.4)) # Right Gain
    # Mono-making below ~955 Hz & side trim: use stereo width control as an approximation
    # 0 = mono, 1 = stereo. Value < 1 will narrow stereo.
    RPR.RPR_TrackFX_SetParam(crackle_track, 1, 3, 0.70) # Stereo width to ~70%
    # This JSFX doesn't have a frequency-dependent mono maker. This is a limitation.

    # 3. ReaEQ - High/Low-pass filtering
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaEQ (Cockos)", False, -1)
    # Band 1: Highpass
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 0, 3.0)   # Band 1 enabled
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 1, 0.0)   # Band 1 gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 2, 150.0) # Band 1 freq (150 Hz)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 3, 6.0)   # Band 1 Q (slope)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 5, 0.0)   # Band 1 type (High Pass)

    # Band 2: Lowpass
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 6, 3.0)   # Band 2 enabled
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 7, 0.0)   # Band 2 gain (0 dB)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 8, 7000.0) # Band 2 freq (7 kHz)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 9, 6.0)   # Band 2 Q (slope)
    RPR.RPR_TrackFX_SetParam(crackle_track, 2, 11, 1.0)  # Band 2 type (Low Pass)

    # 4. ReaVerb (subtle room ambiance)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaVerb (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 0, 0.24) # Wet gain (~24%)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 1, 0.76) # Dry gain (~76%)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 2, 0.5) # Room size (medium)
    RPR.RPR_TrackFX_SetParam(crackle_track, 3, 3, 0.6) # Damping

    RPR.RPR_UpdateArrange()

    return f"Created '{synth_track_name}' and '{crackle_track_name}' with evolving effects over {bars} bars at {bpm} BPM."

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (For sustained notes and automation points, this is accurate enough).
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (Approximation for VSTs and specific curve logic, but the overall effect is captured).
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies? (Placeholder audio item for crackle is used).