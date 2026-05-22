### 1. High-level Design Pattern Extraction

> **Skill Name**: Rhythmic Sidechain Volume Pumping (Automation)

* **Core Musical Mechanism**: The tutorial demonstrates how to use automation envelopes (Trim/Read, Touch, Write, Latch modes) to continuously alter parameters over time. The most musically impactful application of this mechanism is **Rhythmic Volume Pumping** (often called "fake sidechaining"). By drawing an automation envelope that sharply ducks the volume on the downbeat and swells back up on the offbeat, we can rhythmically transform a static, sustained sound.

* **Why Use This Skill (Rationale)**: This technique simulates the psychoacoustic effect of extreme mix-bus compression triggered by a heavy kick drum (the classic "four-on-the-floor" EDM/House sidechain sound). Musically, it creates a powerful sense of forward momentum and groove. By encoding this as drawn automation rather than relying on a compressor, you gain 100% precise control over the shape, depth, and timing of the "pump" without needing an actual trigger track.

* **Overall Applicability**: This pattern is essential in Electronic, Pop, House, and Lo-Fi Hip Hop. It works brilliantly on sustained chord pads, white noise risers, and heavy basslines to ensure they lock into the groove and leave spectral space for the kick drum.

* **Value Addition**: Instead of manually riding faders or setting up complex sidechain routing, this skill programmatically generates mathematically perfect, tempo-synced volume swells. It takes a completely lifeless, sustained MIDI chord and instantly gives it a modern, rhythmic pulse.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Rhythmic Grid**: The automation envelope resets every 1/4 note (on the beat).
  - **Note Duration**: The underlying MIDI note is a sustained, continuous chord held for the entire generated duration. The rhythm is entirely created by the volume automation.

* **Step B: Pitch & Harmony**
  - **Harmony**: Generates a diatonic triad (Root, 3rd, 5th) based on the user-provided `key` and `scale`.
  - **Voicing**: A tight, mid-range closed triad (rooted at MIDI pitch 48 / C3) to act as a solid pad.

* **Step C: Sound Design & FX**
  - **Instrument**: REAPER's native `ReaSynth`.
  - **Automation Target**: We bypass the main track volume fader (leaving it free for mixing) and instead apply the automation envelope directly to ReaSynth's internal Volume parameter (Parameter Index 0). 

* **Step D: Mix & Automation**
  - **Envelope Shape**: 
    - At `time 0` (the downbeat): Volume = 0.0 (Silence)
    - At `time + 1/8th note`: Volume = 0.7 (Full swell)
    - At `time + just before next downbeat`: Volume drops back to 0.0 to prepare for the next pump.
  - **Tension**: Linear points are used to create a natural, slightly aggressive ramp-up curve.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic Pad | MIDI note insertion (`RPR_MIDI_InsertNote`) | Provides the sustained sound source required to make the automation audible. |
| Synthesis | FX Chain (`ReaSynth`) | Native, lightweight, and deterministic sound source. |
| Rhythmic Pumping | FX Parameter Envelope (`RPR_GetFXEnvelope`, `RPR_InsertEnvelopePoint`) | Directly implements the automation techniques from the tutorial. Using an FX envelope instead of Track Volume leaves the mixing fader free for the user. |

> **Feasibility Assessment**: 100% reproducible. The code uses only native ReaScript API calls, built-in FX (ReaSynth), and explicit mathematical timing to programmatically draw the automation shapes demonstrated in the video. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Pumping Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a sustained pad with rhythmic 1/4-note volume pumping (fake sidechain automation).

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
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
        "harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
        "dorian":           [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":       [0, 2, 4, 5, 7, 9, 10],
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create Sustained MIDI Item ===
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_length_sec = beat_sec * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Determine diatonic triad (Root, 3rd, 5th)
    root_base = 48 + NOTE_MAP.get(key, 0) # Start at C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Safe fallback if scale is too short (e.g., pentatonic missing a true 5th)
    third_idx = 2 if len(scale_intervals) > 2 else 1
    fifth_idx = 4 if len(scale_intervals) > 4 else len(scale_intervals) - 1
    
    chord_pitches = [
        root_base,
        root_base + scale_intervals[third_idx],
        root_base + scale_intervals[fifth_idx]
    ]

    # Insert sustained notes
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, item_length)

    for pitch in chord_pitches:
        # noSort = False to ensure correct internal MIDI list sorting
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity_base, False)
    
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Instrument and Automate ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Param 0 in ReaSynth is Volume. We create an envelope for it.
    env = RPR.RPR_GetFXEnvelope(track, fx_idx, 0, True)
    
    # Draw the Pumping Envelope (4 times per bar)
    total_beats = bars * beats_per_bar
    
    for b in range(total_beats):
        t_start = b * beat_sec
        
        # Point 1: Duck the volume at the start of the beat (0.0 = silence)
        RPR.RPR_InsertEnvelopePoint(env, t_start, 0.0, 0, 0.0, False, True)
        
        # Point 2: Swell up 50% of the way through the beat (1/8th note delay)
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.5), 0.7, 0, 0.0, False, True)
        
        # Point 3: Hold the volume high until just before the next kick/beat
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.90), 0.7, 0, 0.0, False, True)
        
        # Point 4: Snap back down to prepare for the next downbeat
        RPR.RPR_InsertEnvelopePoint(env, t_start + (beat_sec * 0.99), 0.0, 0, 0.0, False, True)

    # Sort envelope points to apply changes
    RPR.RPR_Envelope_SortR(env)

    return f"Created '{track_name}' with {bars} bars of rhythmic sidechain automation at {bpm} BPM in {key} {scale}."
```