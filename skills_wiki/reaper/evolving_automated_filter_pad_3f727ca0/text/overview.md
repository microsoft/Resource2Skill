### 1. High-level Design Pattern Extraction

**Skill Name**: Evolving Automated Filter Pad 

* **Core Musical Mechanism**: Track Envelope Automation. This skill dynamically modulates synthesis and mixing parameters (Volume, Pan, and Filter Cutoff) over time. Instead of playing a static chord, automation curves are drawn to create a continuous, evolving transformation of the sound's amplitude, spatial positioning, and frequency spectrum.
* **Why Use This Skill (Rationale)**: Static synthesized chords can sound lifeless and artificial. By automating volume, we create an organic "swell" or "fade-in" that mimics the natural attack of string ensembles or brass. Automating an EQ frequency (Low-Pass filter effect) adds a timbral crescendo, gradually revealing the high-frequency harmonic content. Panning automation provides spatial width and movement, preventing the mix from feeling congested in the center. Together, these elements create tension and release.
* **Overall Applicability**: This is the fundamental technique for creating "risers", transition swells, intro pads, and breakdown atmospheres in almost all genres of electronic, pop, and cinematic music.
* **Value Addition**: Compared to a blank MIDI clip or a static synth patch, this skill encodes the concept of *macro-dynamics*. It demonstrates how to programmatically control REAPER's automation lanes (Track Volume, Track Pan, and specific VST FX Parameters) without needing to manually ride the faders in "Write" or "Touch" mode.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Rhythm**: Sustained chord (whole notes extending across the entire generated block).
  - **Grid**: Envelopes start at bar 1 (beat 1) and linearly sweep to the end of the specified bar count. 
* **Step B: Pitch & Harmony**
  - **Harmony**: A fundamental diatonic triad (Root, 3rd, 5th) built from the parameterized key and scale.
  - **Voicing**: Close position triad in the 3rd/4th octave to provide a thick mid-range tone suitable for filtering.
* **Step C: Sound Design & FX**
  - **Generator**: `ReaSynth` provides the raw oscillator tone (a bright wave that acts as good fodder for filtering).
  - **Filter/Sculpting**: `ReaEQ` is used as a filter. Band 1's frequency is modulated. (By default, Band 1 is a low-shelf, but sweeping its frequency upward still mimics the effect of a low-pass filter opening up, as it brings back the higher frequency energy).
* **Step D: Mix & Automation**
  - **Volume Envelope**: Fades in from `0.0` (-inf dB) to `1.0` (0 dB).
  - **Pan Envelope**: Sweeps from `-0.5` (50% Left) to `0.5` (50% Right).
  - **FX Envelope**: ReaEQ Band 1 Frequency sweeps from `0.1` (low frequencies) to `0.8` (high frequencies) on REAPER's normalized 0.0-1.0 plugin parameter scale.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Pad | MIDI note insertion | Allows parameterized chord generation locked to the project tempo and scale. |
| Synthesis & Filtering | FX chain (`ReaSynth` + `ReaEQ`) | Uses stock REAPER plugins to guarantee reproducibility without external VSTs. |
| Volume & Pan Swell | Track Envelopes (`GetTrackEnvelopeByName`) | Perfectly reproduces the tutorial's focus on automating core track properties over time. |
| Filter Sweep | FX Parameter Envelopes (`GetFXEnvelope`) | Directly demonstrates automating a specific plugin parameter (ReaEQ frequency) as shown in the tutorial. |

> **Feasibility Assessment**: 100% — REAPER's ReaScript API provides direct access to both Track Envelopes (Volume/Pan) and FX Parameter Envelopes, allowing us to programmatically draw the exact automation curves Kenny Gioia created manually using a MIDI controller/mouse in Write mode.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Automated Swell Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create an Evolving Automated Filter Pad in the current REAPER project.
    
    Demonstrates Track Volume, Track Pan, and FX Parameter (ReaEQ) envelope automation.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars for the swell duration.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation of the automated track.
    """
    import reaper_python as RPR

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

    # === Step 1: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Time and Item Calculation ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 3: Insert Sustained MIDI Chord ===
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    root_midi = NOTE_MAP[key] + 48 # Octave 3
    chord_degrees = [0, 2, 4] # Root, 3rd, 5th triad
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    for degree in chord_degrees:
        octave_offset = (degree // len(scale_intervals)) * 12
        scale_idx = degree % len(scale_intervals)
        pitch = root_midi + scale_intervals[scale_idx] + octave_offset
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instruments and FX ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)

    # === Step 5: Automate Track Volume and Pan ===
    # Select track and trigger actions to show default envelopes so we can grab them safely
    RPR.RPR_SetOnlyTrackSelected(track)
    RPR.RPR_Main_OnCommand(40406, 0) # Toggle track volume envelope visible
    RPR.RPR_Main_OnCommand(40407, 0) # Toggle track pan envelope visible

    # Volume Swell (0.0 = -inf dB, 1.0 = 0 dB)
    vol_env = RPR.RPR_GetTrackEnvelopeByName(track, "Volume")
    if vol_env:
        RPR.RPR_InsertEnvelopePoint(vol_env, 0.0, 0.0, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(vol_env, item_length, 1.0, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(vol_env)

    # Pan Sweep (-0.5 = 50% L, 0.5 = 50% R)
    pan_env = RPR.RPR_GetTrackEnvelopeByName(track, "Pan")
    if pan_env:
        RPR.RPR_InsertEnvelopePoint(pan_env, 0.0, -0.5, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(pan_env, item_length, 0.5, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(pan_env)

    # === Step 6: Automate FX Parameter (ReaEQ Frequency) ===
    # Param 0 in ReaEQ is Band 1 Frequency. get/create=True ensures we can automate it.
    eq_env = RPR.RPR_GetFXEnvelope(track, eq_idx, 0, True)
    if eq_env:
        # VST parameters are normalized 0.0 to 1.0 in REAPER
        RPR.RPR_InsertEnvelopePoint(eq_env, 0.0, 0.1, 0, 0, False, False)
        RPR.RPR_InsertEnvelopePoint(eq_env, item_length, 0.8, 0, 0, False, False)
        RPR.RPR_Envelope_Sort(eq_env)

    return f"Created '{track_name}' (Automated Swell) with a {key} {scale} triad over {bars} bars at {bpm} BPM"
```