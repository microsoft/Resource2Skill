# Digital Gain Staging (Headroom Trim & Unity Faders)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Digital Gain Staging (Headroom Trim & Unity Faders)

* **Core Musical Mechanism**: Decoupling a track's intrinsic source signal level (input gain/trim) from its mixing level (track fader). The core technique involves inserting a dedicated "Trim" or "Gain" utility plugin at the very top of the track's FX chain to reduce source levels down to a standardized safe digital headroom (-12 dBFS peaks / -18 dBFS average), allowing the track's main fader to remain at Unity (0 dB) to begin the mix.
* **Why Use This Skill (Rationale)**: In digital systems, signals must never exceed 0 dBFS (which causes hard clipping/distortion). Additionally, most analog-modeled plugins (compressors, EQs, saturators) are calibrated to an analog sweet spot where 0 VU equals roughly -18 dBFS. By trimming input signals down to this sweet spot *before* they hit any plugins, you ensure optimal signal-to-noise ratio and prevent internal clipping. Furthermore, DAW faders are logarithmic; they have the highest physical resolution near 0 dB. Keeping faders near Unity gives you the finest control over volume automation.
* **Overall Applicability**: This is a universal foundational skill for setting up a new mix in any genre. It is especially critical when dealing with raw recordings, multi-mic drum setups, or software synths (which frequently output extremely hot signals near 0 dBFS by default).
* **Value Addition**: Compared to just pulling down the track faders on hot signals (which ruins fader throw resolution and still drives plugins too hard), this skill encodes professional mix preparation. It ensures the signal hits the FX chain at the ideal level, preserving dynamic range and headroom on the master bus.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * *Context-agnostic*: This is a signal flow and mixing technique, meaning it applies regardless of the BPM or rhythmic grid. (The provided code generates a basic quarter-note pulse to demonstrate the signal flow).
* **Step B: Pitch & Harmony**
  * *Context-agnostic*: Applies to all harmonic and melodic material. 
* **Step C: Sound Design & FX**
  * **Instrument**: Any source (e.g., ReaSynth).
  * **Trim Plugin**: `JS: Volume Adjustment` (or equivalent Trim/Gain plugin). This must be placed in Slot 1 (index 0), *before* any dynamics or EQ processing.
  * **Target Parameter**: "Adjustment (dB)" is set to a negative value (e.g., `-12.0 dB`) to attenuate hot source material down to the digital sweet spot (-12 dBFS peak).
* **Step D: Mix & Automation**
  * **Track Fader**: Strictly initialized to `0.0 dB` (Unity Gain).
  * **Master Bus**: The aggregate effect of gain-staging all individual tracks ensures the Master Bus meter has plenty of headroom and does not hit the "solid red" clipping threshold.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Signal Source | MIDI notes & ReaSynth | Generates a hot default audio signal to demonstrate the need for gain staging. |
| Gain Staging / Trim | FX Chain (`JS: Volume Adjustment`) | Matches the tutorial's exact instruction to "drop a trim or gain plugin on each channel" to control initial levels. |
| Peak Targeting | FX Parameter (`TrackFX_SetParam`) | Automates turning the signal down by exactly -12 dB to hit the recommended digital peak target. |
| Fader Resolution | `SetMediaTrackInfo_Value` | Forces the track fader to exactly 1.0 (0 dB / Unity Gain) to maintain fader throw resolution. |

> **Feasibility Assessment**: 100% — The fundamental physics of REAPER's 64-bit float mix engine allow us to perfectly replicate the tutorial's gain staging setup using a stock JSFX trim plugin and exact fader manipulation.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Gain_Staged_Synth",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a correctly Gain-Staged track demonstrating the "Trim + Unity Fader" method.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note.
        scale: Scale type.
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created gain-staged setup.
    """
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_minor": [0, 3, 5, 7, 10],
    }

    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)
    
    # CRITICAL: Keep track fader exactly at Unity (0 dB) to maximize fader throw resolution
    # 1.0 represents 0 dB in REAPER's linear volume scale
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 1.0)

    # === Step 3: Create MIDI Signal Source ===
    # We create a simple repeating root note pulse to generate an audio signal
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    root_midi = 48 + NOTE_MAP.get(key, 0) # Octave 3 root
    
    # Insert 1/4 notes for the duration of the item
    notes_to_create = bars * 4
    quarter_note_len = 1.0  # 1 beat
    for i in range(notes_to_create):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, i * quarter_note_len * (60.0/bpm))
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, (i + 0.8) * quarter_note_len * (60.0/bpm))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, root_midi, velocity_base, False)

    # === Step 4: Add FX Chain (Source -> Trim -> Processing) ===
    
    # 1. Sound Source (Defaults to very loud, close to 0 dBFS)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. GAIN STAGING TRIM PLUGIN (The core skill)
    # Placed immediately after the instrument (or at the top of an audio track)
    trim_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Volume Adjustment", False, -1)
    
    # We attenuate the signal by -12.0 dB right at the top of the chain.
    # This simulates targeting the -12 dBFS digital sweet spot mentioned in the tutorial.
    # Parameter 0 in "JS: Volume Adjustment" is "Adjustment (dB)"
    RPR.RPR_TrackFX_SetParam(track, trim_idx, 0, -12.0)
    
    # 3. Subsequent Processing (Now receiving signal at proper analog sweet spot)
    comp_idx = RPR.RPR_TrackFX_AddByName(track, "ReaComp", False, -1)
    
    # Lower compressor threshold to match the newly gain-staged -12dBFS signal
    RPR.RPR_TrackFX_SetParamNormalized(track, comp_idx, 0, 0.4) # Threshold roughly adapted

    return f"Created gain-staged track '{track_name}'. Fader is locked at 0dB (Unity). Source trimmed by -12dB using JS Volume before hitting ReaComp."
```