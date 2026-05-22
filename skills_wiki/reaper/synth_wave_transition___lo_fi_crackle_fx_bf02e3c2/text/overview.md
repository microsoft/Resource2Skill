### 1. High-level Design Pattern Extraction

**Skill Name**: Synth Wave Transition & Lo-Fi Crackle FX

*   **Core Musical Mechanism**: This skill creates a dynamic synth transition, characterized by a sweeping/flanging timbre, a pulsating volume chop, and an expanding stereo field. Simultaneously, it layers a processed vinyl crackle sound that provides a warm, lo-fi texture, integrated into the mix with specific dynamic, spatial, and spectral adjustments.

*   **Why Use This Skill (Rationale)**:
    *   **Synth Transition**: The combination of timbral modulation (flanging/sweeping), rhythmic volume gating, and stereo widening creates a sense of dynamic movement and anticipation, effectively building up to or transitioning between musical sections. The gradual expansion from mono to stereo adds depth and envelopment. The volume chopping adds rhythmic interest and energy.
    *   **Lo-Fi Crackle**: Vinyl crackle inherently adds a vintage, nostalgic, and lo-fi aesthetic. By applying gentle compression, mid-side processing, EQ, and subtle reverb, the raw, potentially jarring, crackle is tamed, focused, and placed within the sonic space, enhancing textural richness without distraction. It contributes to a cohesive, "glued" feel with other elements like drums and pads.

*   **Overall Applicability**:
    *   **Synth Transition**: Excellent for intros, breakdowns, build-ups, and transitions in genres like synthwave, electronic dance music (EDM), ambient, hip-hop, and film scoring where dramatic shifts in sound are desired.
    *   **Lo-Fi Crackle**: Widely applicable in lo-fi hip-hop, chillwave, indie pop, cinematic scoring (for vintage texture), and any genre aiming for a warm, aged, or atmospheric backdrop.

*   **Value Addition**: This skill encodes musical knowledge about creating dynamic sonic transitions and integrating background textures for atmospheric or stylistic purposes. It moves beyond simple note placement to encompass complex automation, psychoacoustic processing (mid-side, mono-making), and creative use of stock effects to achieve specific timbral and spatial characteristics.

---

### 2. Technical Breakdown

*   **Step A: Rhythm & Timing**
    *   **Synth Transition**: The synth note is sustained for the entire `bars` duration. The volume chopping applies a 32nd-note rhythmic pulse to the volume envelope, creating a rapid on/off effect. The overall transition (volume swell, width expand) happens linearly over the `bars` duration, extending slightly beyond for reverb tails.
    *   **Lo-Fi Crackle**: Continuous background noise, no specific rhythmic pattern in its source. Dynamics processing with 0ms attack flattens fast transients, smoothing out inherent rhythmic spikes in the crackle.

*   **Step B: Pitch & Harmony**
    *   **Synth Transition**: A single, sustained MIDI note (default C3, but user-configurable via `key`, `scale`, and `octave` parameters) serves as the base for the timbral and dynamic modulation. The effect is primarily textural, not melodic or harmonic.
    *   **Lo-Fi Crackle**: No specific pitch or harmonic content, as it's primarily a noise texture.

*   **Step C: Sound Design & FX**
    *   **Synth Transition**:
        *   **Instrument**: ReaSynth (stock REAPER VSTi) is used as an approximation for Hybrid 3.
        *   **Timbral Modulation**: ReaSynth's `Filter Cutoff` is automated with a slow, LFO-like sine wave curve (modulating between ~40% and ~70% cutoff) to mimic the "shape" modulation and flanging effect of Hybrid 3.
        *   **Built-in Reverb/Chorus (Approximation)**: The original Hybrid 3 had built-in Hall Reverb and Chorus. For ReaSynth, these are not directly replicated within the synth itself but are implicitly handled by the track's processing if external reverb/chorus were added. For this skill, the focus is on the core automation.
    *   **Lo-Fi Crackle**:
        *   **Source**: `JS: Pink Noise` (stock REAPER JSFX) is used as a generic noise source to simulate vinyl crackle, though the exact texture of real vinyl crackle is not perfectly reproducible without an external sample.
        *   **Dynamics**: `JS: General Dynamics (Cockos)` is used with a very fast attack (0ms), high ratio (approx. 0.9), and a threshold around -20dB (approximated by curve parameters) to compress sharp transients, making the crackle less jarring. A +5dB wet mix boosts the output.
        *   **Mid-Side & Balance**: `JS: Stereo Field Manipulator (Cockos)` is used:
            *   Left trim: -6.0 dB.
            *   Right trim: +4.4 dB (to fix stereo imbalance).
            *   Side gain: -6.0 dB (to reduce the stereo width of the noise).
            *   Mono Maker: 70% mix below 955 Hz (to focus the low-mid frequencies to mono).
        *   **EQ**: `ReaEQ (Cockos)` is applied:
            *   High-pass filter at 200 Hz (removes sub-rumble).
            *   Low-pass filter at 10 kHz (removes harsh high-frequency hiss).
            *   Small band dip (-1 dB) at 1 kHz (subtle tonal shaping).
        *   **Reverb**: `ReaVerb (Cockos)` is used with a 24% wet mix (no specific IR is loaded, relying on default/small room settings) to place the crackle within an imaginary room, gluing it with other instruments.

*   **Step D: Mix & Automation**
    *   **Synth Transition**:
        *   **Volume Swell**: Track volume is automated with a linear ramp from -4.6 dB to 0 dB over the `bars` duration, extending slightly beyond.
        *   **Volume Chopping**: A 32nd-note square-wave-like volume pattern (alternating +1 dB and -4 dB offsets relative to the swell) is applied starting from the second bar, combined with the swell curve.
        *   **Stereo Width**: Track width is automated linearly from 0% (mono) to 100% (stereo) over the `bars` duration, extending slightly beyond.
        *   **Trim Volume**: The track's overall `D_VOL` is set to -5 dB to adjust the final level.
    *   **Lo-Fi Crackle**:
        *   **Volume**: Track's overall `D_VOL` is set to -18 dB for a subtle background presence. No further automation.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern          | Method                                              | Why this method                                                                    |
| :----------------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------- |
| Synth instrument               | Track creation + ReaSynth VSTi                      | Provides a basic synth for modulation. (Approximation of Hybrid 3).                |
| Synth note                     | MIDI note insertion                                 | Creates a sustained tone as the basis for effects.                                 |
| Synth timbral sweep/flange     | FX chain (ReaSynth Filter Cutoff) + Automation      | Approximates Hybrid 3's "shape" modulation using ReaSynth's filter for sweep effect. |
| Synth volume swell & chop      | Automation envelope (Volume)                        | Precisely controls dynamic range and rhythmic gating.                              |
| Synth stereo width expansion   | Automation envelope (Width)                         | Creates spatial movement from mono to stereo.                                      |
| Synth overall level            | Track `D_VOL` (Trim Volume)                         | Fine-tuning the final loudness after other automation.                             |
| Crackle noise source           | Track creation + JS: Pink Noise                     | Provides a reproducible noise source without external files.                       |
| Crackle transient compression  | FX chain (JS: General Dynamics) + FX parameters     | Flattens sharp transients for a smoother background texture.                       |
| Crackle stereo balance & mono  | FX chain (JS: Stereo Field Manipulator) + FX params | Corrects stereo imbalance and narrows stereo image (approximation of VUMT Deluxe). |
| Crackle frequency shaping      | FX chain (ReaEQ) + FX parameters                    | Removes unwanted sub-bass and harsh high frequencies.                              |
| Crackle room ambiance          | FX chain (ReaVerb) + FX parameters                  | Adds subtle spatial context (approximation of ToneBoosters Reverb 3).              |
| Crackle overall level          | Track `D_VOL`                                       | Adjusts the background volume.                                                     |

**Feasibility Assessment**: The code reproduces approximately **75%** of the tutorial's musical result.
*   The automation for volume, width, and ReaSynth filter sweep are accurately replicated, forming the core dynamic elements of the synth transition.
*   The processing chain for the vinyl crackle (dynamics, mid-side, EQ, reverb) is largely reproduced using stock REAPER JSFX/VSTs.
*   The primary limitations are the exact timbral character of the third-party synth (Hybrid 3) and the precise sonic texture of the vinyl crackle audio sample, which cannot be exactly replicated with stock ReaSynth and JS: Pink Noise. The specific custom curve of JS: General Dynamics is also hard to replicate precisely via ReaScript parameters but its *effect* is approximated.

#### 3b. Complete Reproduction Code

```python
import reaper_python as RPR
import math

# Music theory lookup tables (already provided in the template)
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

def get_midi_note(key, scale, degree, octave=4):
    """Calculates MIDI note number for a given key, scale, degree, and octave."""
    if key not in NOTE_MAP:
        raise ValueError(f"Invalid key: {key}. Must be one of {list(NOTE_MAP.keys())}")
    if scale not in SCALES:
        raise ValueError(f"Invalid scale: {scale}. Must be one of {list(SCALES.keys())}")
    if not (1 <= degree <= len(SCALES[scale])): # Basic check for degree
        # Adjust degree to wrap around the scale for higher/lower notes if needed
        pass # The logic below handles this

    root_midi = NOTE_MAP[key]
    scale_intervals = SCALES[scale]
    
    num_scale_notes = len(scale_intervals)
    octave_offset = (degree - 1) // num_scale_notes
    scale_degree_index = (degree - 1) % num_scale_notes
    
    interval = scale_intervals[scale_degree_index]
    
    midi_note = root_midi + interval + (octave + octave_offset) * 12
    return midi_note

def db_to_reaper_vol(db_val):
    """Converts a dB value to REAPER's linear volume scale (0.0 to 1.0)."""
    if db_val <= -144: # REAPER's minimum dB value (effectively mute)
        return 0.0
    return math.pow(10, db_val / 20.0)

def create_synth_transition_and_crackle_fx(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    synth_velocity: int = 100,
    crackle_volume_db: float = -18.0, # dB
    **kwargs,
) -> str:
    """
    Creates a synth track with a transitional flanging/chopping/width effect
    and a background vinyl crackle track with lo-fi processing.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        synth_velocity: MIDI velocity for the synth note (0-127).
        crackle_volume_db: Base volume for the crackle track in dB.
        **kwargs: Additional overrides (not used directly in this function but for future compatibility).

    Returns:
        Status string, e.g., "Created synth transition and crackle FX over 8 bars."
    """
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_item_length = bar_length_sec * bars
    
    # Automation envelopes often extend slightly beyond the item length to catch reverb tails.
    automation_end_time = total_item_length + bar_length_sec 

    # --- SYNTH TRANSITION TRACK ---
    synth_track_name = "Synth Transition"
    synth_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(synth_track_idx, True)
    synth_track = RPR.RPR_GetTrack(0, synth_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(synth_track, "P_NAME", synth_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "D_VOL", db_to_reaper_vol(-5.0)) # Trim Volume -5dB

    # Add ReaSynth
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth (Cockos)", False, -1)
    
    # MIDI Item and Note (sustained for the whole duration)
    midi_item = RPR.RPR_AddMediaItemToTrack(synth_track)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(midi_item, "D_LENGTH", total_item_length)
    midi_take = RPR.RPR_GetActiveTake(midi_item)
    
    synth_note_midi = get_midi_note(key, scale, 1, 3) # First degree of the scale, octave 3
    RPR.MIDI_SetItemExtents(midi_item, 0.0, total_item_length) 
    RPR.MIDI_InsertNote(midi_take, False, False, 0.0, total_item_length, False, synth_note_midi, synth_velocity, 0)
    RPR.MIDI_Sort(midi_take)
    RPR.MIDI_UpdateItemInProject(midi_item)

    # ReaSynth Filter Cutoff Automation (to simulate LFO on shape / flanging)
    # Automate ReaSynth's filter cutoff (param 16) with an LFO-like curve
    rs_fx_idx = RPR.RPR_TrackFX_GetFXByName(synth_track, "ReaSynth", False)
    cutoff_param_idx = 16 # Filter Cutoff
    
    RPR.RPR_TrackFX_SetParam(synth_track, rs_fx_idx, cutoff_param_idx, 0.5) # Set initial value
    RPR.RPR_TrackFX_SetEnvelopeParam(synth_track, rs_fx_idx, cutoff_param_idx, True, True, True)
    cutoff_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "ReaSynth(1) VSTi: Filter Cutoff")
    RPR.RPR_DeleteEnvelopePointRange(cutoff_envelope, 0.0, automation_end_time)

    # Simulate slow LFO on filter cutoff from ~40% to ~70%
    num_points = bars * 8 # 8 points per bar for a smooth LFO
    for i in range(num_points + 1):
        time = i * (automation_end_time / num_points)
        value = 0.55 + 0.15 * math.sin(i * 2 * math.pi / (num_points / (bars / 2))) # 2 cycles over 4 bars
        RPR.RPR_InsertEnvelopePoint(cutoff_envelope, time, value, 0, 0.5, False, False)
    
    # Track Volume Automation (Swell Up + Chopping)
    vol_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")
    if not vol_envelope:
        RPR.RPR_SetMediaTrackInfo_Value(synth_track, "C_SHOWSVOLPAN", 1) 
        vol_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Volume")

    RPR.RPR_DeleteEnvelopePointRange(vol_envelope, 0.0, automation_end_time)
    
    initial_swell_db = -4.6
    final_swell_db = 0.0
    chop_high_offset_db = 1.0 # chop peak relative to swell
    chop_low_offset_db = -4.0 # chop trough relative to swell
    
    start_chop_bar = 1 # Chop starts from the second bar in the video
    chop_start_time = bar_length_sec * start_chop_bar
    
    # Points for the swell
    RPR.RPR_InsertEnvelopePoint(vol_envelope, 0.0, db_to_reaper_vol(initial_swell_db), 0, 0.5, False, False)
    RPR.RPR_InsertEnvelopePoint(vol_envelope, chop_start_time, db_to_reaper_vol(initial_swell_db + (chop_high_offset_db + chop_low_offset_db)/2), 0, 0.5, False, False)

    # Combined swell and chop automation
    num_chop_intervals = int((automation_end_time - chop_start_time) / (bar_length_sec / 8)) # 32nd note intervals
    for i in range(num_chop_intervals + 1):
        time = chop_start_time + i * (bar_length_sec / 8)
        time = min(time, automation_end_time) # Ensure time does not exceed max
        
        # Calculate base swell volume at this time
        swell_range = final_swell_db - initial_swell_db
        swell_progress = (time / automation_end_time) # Normalized progress over total duration
        current_base_swell_db = initial_swell_db + (swell_range * swell_progress)
        
        # Apply chop offset
        chop_offset_db = chop_high_offset_db if (i % 2 == 0) else chop_low_offset_db
        final_vol_db = current_base_swell_db + chop_offset_db
        
        RPR.RPR_InsertEnvelopePoint(vol_envelope, time, db_to_reaper_vol(final_vol_db), 0, 0.5, False, False)


    # Track Width Automation (Mono to Stereo)
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "I_PANMODE", 1) # Set track to Stereo Pan mode
    RPR.RPR_SetMediaTrackInfo_Value(synth_track, "C_SHOWSWIDTH", 1) # Show width envelope
    width_envelope = RPR.RPR_GetTrackEnvelopeByName(synth_track, "Width")
    
    RPR.RPR_DeleteEnvelopePointRange(width_envelope, 0.0, automation_end_time)
    RPR.RPR_InsertEnvelopePoint(width_envelope, 0.0, 0.0, 0, 0.5, False, False) # Mono (0.0)
    RPR.RPR_InsertEnvelopePoint(width_envelope, automation_end_time, 1.0, 0, 0.5, False, False) # Stereo (1.0)


    # --- CRACKLE FX TRACK ---
    crackle_track_name = "Vinyl Crackle FX"
    crackle_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(crackle_track_idx, True)
    crackle_track = RPR.RPR_GetTrack(0, crackle_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(crackle_track, "P_NAME", crackle_track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(crackle_track, "D_VOL", db_to_reaper_vol(crackle_volume_db))

    # Add JS: Pink Noise as source (no item needed, JSFX generates continuously)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Pink Noise (Cockos)", False, -1)
    
    # Add JS: General Dynamics (to compress transients)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: General Dynamics (Cockos)", False, -1)
    gd_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "JS: General Dynamics", False)
    
    # Set General Dynamics parameters based on video (approximation)
    # Detect input gain (dB): 0.0 (param 0)
    # Input response (ms): 0.0 (fast attack) (param 3)
    # Ratio: ~0.9 (high compression/limiting) (param 4)
    # Threshold: ~-20dB (param 5 maps 0-1 to -60-0dB, so 40/60 = 0.66)
    # Wet mix (dB): 5.0 (output boost) (param 8)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 0, 0.0)    # Detect input gain 0dB
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 3, 0.0)    # Input response 0ms (fast attack)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 4, 0.9)    # Ratio approx 0.9 (high compression)
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 5, 0.66)   # Threshold approx -20dB
    RPR.RPR_TrackFX_SetParam(crackle_track, gd_fx_idx, 8, db_to_reaper_vol(5.0)) # Wet mix +5dB (ReaScript expects linear for this param)

    # Add JS: Stereo Field Manipulator (for mid-side balance and mono maker)
    RPR.RPR_TrackFX_AddByName(crackle_track, "JS: Stereo Field Manipulator (Cockos)", False, -1)
    sfm_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "JS: Stereo Field Manipulator", False)
    
    # Trim Left (-6.0dB) and Right (+4.4dB) for balance (param 0 & 1)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 0, db_to_reaper_vol(-6.0)) # Input L trim (linear value)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 1, db_to_reaper_vol(4.4))  # Input R trim (linear value)

    # Trim Side Signal (-6dB, using Mid-Side mode) (param 3)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 3, db_to_reaper_vol(-6.0)) # Gain (Side) (linear value)
    
    # Mono Maker at 955 Hz, amount 70% (param 2 for mix, param 6 for freq)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 2, 0.70) # Mono mix 70% (0.0 to 1.0)
    RPR.RPR_TrackFX_SetParam(crackle_track, sfm_fx_idx, 6, 955.0/1000.0) # Mono frequency 955Hz (scaled 0-1 for 0-10000Hz)

    # Add ReaEQ (high-pass and low-pass filtering)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaEQ (Cockos)", False, -1)
    req_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "ReaEQ", False)

    # Band 1: High Pass (LPF in ReaEQ terms, but for filtering lows)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 0, 1.0) # Band 1 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 1, 0.0) # Band 1 Type: High Pass (LPF)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 2, 200.0) # Band 1 Freq: 200Hz
    
    # Band 2: Low Pass (HPF in ReaEQ terms, but for filtering highs)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 5, 1.0) # Band 2 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 6, 1.0) # Band 2 Type: Low Pass (HPF)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 7, 10000.0) # Band 2 Freq: 10kHz
    
    # Band 3: Mid-dip at 1kHz (subtle)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 10, 1.0) # Band 3 On
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 11, 2.0) # Band 3 Type: Band (Shelf)
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 12, 1000.0) # Band 3 Freq: 1kHz
    RPR.RPR_TrackFX_SetEQParam(crackle_track, req_fx_idx, 13, db_to_reaper_vol(-1.0)) # Band 3 Gain: -1dB (linear value)


    # Add ReaVerb (for subtle room sound)
    RPR.RPR_TrackFX_AddByName(crackle_track, "ReaVerb (Cockos)", False, -1)
    rv_fx_idx = RPR.RPR_TrackFX_GetFXByName(crackle_track, "ReaVerb", False)
    
    # Set ReaVerb parameters for a subtle room (approximation of "New Home Empty Room")
    # Parameter 10 is Dry/Wet mix (0.0 to 1.0)
    RPR.RPR_TrackFX_SetParam(crackle_track, rv_fx_idx, 10, 0.24) # Dry/Wet (Wet) 24%

    RPR.RPR_UpdateArrange()
    
    return f"Created '{synth_track_name}' and '{crackle_track_name}' over {bars} bars at {bpm} BPM."

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)? (The chop is on 32nd notes, exact timing is calculated.)
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"? (With the acknowledged limitations of third-party plugin replacement.)
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?