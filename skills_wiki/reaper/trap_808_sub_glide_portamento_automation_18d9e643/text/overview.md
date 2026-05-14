# Trap 808 Sub Glide (Portamento Automation)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Trap 808 Sub Glide (Portamento Automation)

* **Core Musical Mechanism**: The defining signature of this pattern is the rapid, continuous pitch-sweep (portamento) of a low-frequency sine wave (808 or sub-bass) between two notes. Instead of a distinct second attack, the pitch "slides" up or down (usually by exactly one octave or a perfect fifth) immediately before or during a rhythmic hit.
* **Why Use This Skill (Rationale)**: This pitch glide exploits psychoacoustics—rapidly sweeping low frequencies creates a physical sensation of "drop" or "lift" (often called "bounce" in hip-hop). Harmonically, keeping the glide to a perfect octave preserves the key while radically changing the bass register, adding high-energy movement without clashing with the existing chord progression. 
* **Overall Applicability**: Essential for modern Trap, UK/NY Drill, Future Bass, and modern Hip-Hop. The 808 glide acts as a dynamic rhythmic transition, typically placed at the end of a 2-bar or 4-bar phrase to lead back into the downbeat.
* **Value Addition**: This skill transforms a static sub-bass into a modern 808 by encoding exact envelope shapes (timing and curve tension) required to make a pitch-slide sound musical rather than just out-of-tune.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 120–150 BPM (Standard Trap/Drill tempos).
  - **Grid**: The slide typically begins 1/8th or 1/16th note *before* the target beat and resolves perfectly on the grid line.
  - **Duration**: Base notes are long and sustained; slide notes are short and act as grace notes.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Key-dependent, usually Minor or Harmonic Minor. 
  - **Interval**: The pitch bends exactly +12 semitones (one octave up) or +7 semitones (a perfect fifth).
  - **Voicing**: Strictly monophonic sub-register (C1 - G2).

* **Step C: Sound Design & FX**
  - **Instrument**: A pure sine wave with a moderate attack (to prevent clicking) and a moderate release.
  - **Saturation**: Heavy distortion/saturation is required so the sub-bass produces upper harmonics, allowing the glide to be heard on smaller speakers.
  - **Glide Method**: In native REAPER, bypassing 3rd-party VSTs is best achieved by drawing an automation curve on the synth's native Pitch/Tuning parameter, exactly mimicking the `ReaPitch` automation curve demonstrated in the tutorial.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **808 Generation** | `ReaSynth` + `JS: Saturation` | Creates a convincing, heavy 808 sub-bass using 100% stock REAPER tools without needing external audio samples. |
| **Rhythm** | MIDI note insertion | Allows parameterized mapping to the project's key and tempo. |
| **808 Glide/Slide** | Track FX Parameter Envelope | Directly mirrors the tutorial's technique of drawing pitch-shift automation curves (Methods 2 from the video), avoiding the 2-semitone limit of standard MIDI pitch bend. |

> **Feasibility Assessment**: 100% reproducible. By combining a synthesized sine wave, saturation, and native FX parameter automation, we perfectly recreate the characteristic 808 pitch slide demonstrated in the video natively inside REAPER.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "808 Sub Glide",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a Trap/Drill 808 sub bass with a characteristic octave glide.
    """
    import reaper_python as RPR

    # Music theory lookup for sub bass (C1 - B1 range)
    NOTE_MAP = {
        "C": 24, "C#": 25, "Db": 25, "D": 26, "D#": 27, "Eb": 27,
        "E": 28, "F": 29, "F#": 30, "Gb": 30, "G": 31, "G#": 32,
        "Ab": 32, "A": 33, "A#": 34, "Bb": 34, "B": 35
    }
    base_pitch = NOTE_MAP.get(key.upper(), 24)

    # === Step 1: Set Tempo & Create Track ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 2: Build 808 Sound Design (ReaSynth + Saturation) ===
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Configure ReaSynth as a Sub Bass
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 0, 0.8)  # Volume
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 1, 0.5)  # Tuning (Center 0.5 = 0 shift)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 2, 0.05) # Attack (slight fade to avoid clicks)
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 3, 0.6)  # Decay
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 4, 0.8)  # Sustain
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 5, 0.3)  # Release
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 6, 0.0)  # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, synth_idx, 7, 0.0)  # Saw mix

    # Add Saturation to generate 808 harmonics
    sat_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Saturation", False, -1)
    if sat_idx >= 0:
        RPR.RPR_TrackFX_SetParamNormalized(track, sat_idx, 0, 0.75) # Drive amount

    # === Step 3: Create MIDI Item & Rhythm ===
    beats_per_bar = 4
    bar_len = (60.0 / bpm) * beats_per_bar
    item_len = bar_len * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 808 Pattern: Hit on Beat 1, Hit on Beat 3, Slide on Beat 4
    sec_per_beat = 60.0 / bpm
    
    for b in range(bars):
        bar_start = b * bar_len
        
        # Note 1: Downbeat
        start1 = bar_start + 0.0
        end1 = bar_start + (sec_per_beat * 1.5)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start1), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end1), 
                                0, base_pitch, velocity_base, False)
                                
        # Note 2: Offbeat hitting into the slide
        start2 = bar_start + (sec_per_beat * 2.5)
        end2 = bar_start + (sec_per_beat * 4.0)
        RPR.RPR_MIDI_InsertNote(take, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start2), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end2), 
                                0, base_pitch, velocity_base, False)

    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Automate the 808 Pitch Glide ===
    # Get the envelope for ReaSynth "Tuning" (Param Index 1)
    # Range is 0.0 (-24st) to 1.0 (+24st). Center is 0.5. An octave up (+12st) is 0.75.
    env = RPR.RPR_GetFXEnvelope(track, synth_idx, 1, True)
    
    for b in range(bars):
        bar_start = b * bar_len
        
        # Slide timing: starts half a beat before the end of the bar, peaks at the end
        slide_start = bar_start + (sec_per_beat * 3.0)
        slide_peak = bar_start + (sec_per_beat * 3.5)
        slide_end = bar_start + (sec_per_beat * 4.0)
        
        # Insert Envelope Points (Time, Value, Shape, Tension, Selected, NoSort)
        # Shape 2 = Slow Start/End (perfect for smooth glides)
        RPR.RPR_InsertEnvelopePoint(env, slide_start - 0.01, 0.5, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_start, 0.5, 2, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_peak, 0.75, 0, 0.0, False, True) # Glides up +1 octave
        RPR.RPR_InsertEnvelopePoint(env, slide_end, 0.75, 0, 0.0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, slide_end + 0.01, 0.5, 0, 0.0, False, True) # Snap back to normal

    RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' with 808 Pitch Automation Glide (+1 Octave) over {bars} bars at {bpm} BPM."
```