# Afro-Cuban 3-2 Son Clave Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Afro-Cuban 3-2 Son Clave Timeline

* **Core Musical Mechanism**: The 3-2 Son Clave is an asymmetrical, two-measure rhythmic pattern that serves as the organizing structural timeline for Afro-Cuban music, Salsa, and many offshoots. The pattern is divided into two halves (a "yin and yang"): 
  * The **"3" side** is highly syncopated (a *tresillo* rhythm), pushing against the downbeats to create musical tension.
  * The **"2" side** is grounded and lands perfectly on the solid beats (beats 2 and 3), providing resolution and anchoring the groove.

* **Why Use This Skill (Rationale)**: As John Santos explains in the tutorial, the clave is not just a rhythm, but a restrictive framework (in a good way) that dictates where melodies and other instruments must sit. Composing "in clave" means aligning your melodic accents, bassline syncopations, and drum hits to agree with this specific tension-and-release structure. If a melody clashes with the clave (known as being *cruzado* or crossed), the groove immediately feels disjointed to the listener.

* **Overall Applicability**: This is the absolute foundation for Latin/Afro-Cuban rhythms (Salsa, Mambo, Son). Furthermore, its syncopated DNA heavily influences modern Pop, R&B, Reggaeton (the *dembow* is a modified tresillo), and Hip-Hop. It is used as a rhythmic spine to lock down complex, multi-layered percussion arrangements.

* **Value Addition**: Compared to a blank MIDI clip or a simple 4-on-the-floor kick drum, this script encodes a culturally and rhythmically critical 2-bar timeline. It teaches an agent how to construct asymmetrical rhythmic tension and provides a strict grid against which other musical elements (bass, piano *montunos*, vocal melodies) can be evaluated and composed.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * Time Signature: 4/4.
  * Tempo: Generally 80 - 120 BPM for traditional Son or Rumba.
  * Phrase Length: 2 bars (8 beats total).
  * Rhythm Grid (in beats, where Beat 1 = 0.0):
    * **Bar 1 ("3" side)**: Beat 1 (0.0), Beat 2 "and" (1.5), Beat 4 (3.0)
    * **Bar 2 ("2" side)**: Beat 2 (5.0), Beat 3 (6.0)
  * Note Duration: Very short and staccato (e.g., 16th notes).

* **Step B: Pitch & Harmony**
  * The Clave is unpitched percussion. 
  * General MIDI Standard maps the "Claves" instrument to MIDI Note 75. 
  * MIDI Channel 10 (Channel index 9) is standard for drums.

* **Step C: Sound Design & FX**
  * A traditional woodblock/clave sound is required. Since external sample libraries cannot be guaranteed in the environment, the script constructs a "synth-clave" using stock **ReaSynth**.
  * ReaSynth is configured to behave like a piece of resonant wood:
    * Attack: 0.0 ms (Instant transient)
    * Decay: ~50 ms (Rapid decay)
    * Sustain: 0.0 (No held note)
    * Release: ~50 ms
    * Waveform: Sine mixed with a bit of Square to add odd harmonics resembling a hard wood strike.

* **Step D: Mix & Automation**
  * Consistent velocity (around 100) to act as a solid metronomic timeline, with slight emphasis on the very first downbeat.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Clave Rhythm | MIDI Note Insertion | Exact positional placement of the 3-2 syncopation based on beat mathematics. |
| Sound Source | ReaSynth FX manipulation | Guarantees a sharp, percussive click tone without needing third-party audio samples. |
| Organization | 2-bar phrase loop | Translates the foundational Latin concept of 2-bar harmonic/rhythmic phasing. |

> **Feasibility Assessment**: 100% reproducible for the MIDI rhythm. The tone is an 80% approximation using a synthetic woodblock via ReaSynth, ensuring safety and execution without missing external audio dependencies.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "3-2 Son Clave",
    bpm: int = 100,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a foundational 3-2 Son Clave rhythm track.
    
    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (unused for unpitched percussion, but accepted per signature).
        scale: Scale type (unused for unpitched percussion).
        bars: Number of bars to generate (should ideally be an even number for full phrases).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    item_length_sec = beat_len_sec * beats_per_bar * bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # 3-2 Son Clave rhythm pattern defined in beats relative to a 2-bar sequence
    # Bar 1 (3 side): Beats 1.0, 2.5 (2 AND), 4.0
    # Bar 2 (2 side): Beats 2.0, 3.0 (which are 5.0 and 6.0 relatively)
    clave_pattern_beats = [0.0, 1.5, 3.0, 5.0, 6.0]

    pitch = 75     # General MIDI note for Claves
    channel = 9    # MIDI Channel 10 (0-indexed = 9) for drums
    notes_added = 0

    # Generate the pattern across the requested number of bars
    for bar_pair in range(0, bars, 2):
        offset_beats = bar_pair * beats_per_bar
        for b in clave_pattern_beats:
            absolute_beat = offset_beats + b
            
            # Ensure we don't write notes past the requested total bars
            if absolute_beat < (bars * beats_per_bar):
                # Calculate project time in seconds for conversion
                start_time_sec = absolute_beat * beat_len_sec
                # 16th note duration
                end_time_sec = start_time_sec + (beat_len_sec * 0.25)
                
                # Convert time to PPQ
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time_sec)
                
                # Slightly emphasize the very first downbeat of the 3-side
                vel = velocity_base + 10 if b == 0.0 else velocity_base
                vel = min(127, vel)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, channel, pitch, vel, True)
                notes_added += 1

    # Sort MIDI events after bulk insertion
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add Sound Design (Fallback Synth Clave) ===
    # Add a stock synthesizer to ensure it makes a percussive click 
    # even if no dedicated drum VST is loaded.
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Shape the ReaSynth envelope to act like a struck block of wood
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.5)   # Volume: -6dB
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.4)   # Square mix: Adds "wooden" odd harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.0)   # Attack: 0 ms (sharp transient)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 7, 0.05)  # Decay: very short
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 8, 0.0)   # Sustain: 0
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 9, 0.05)  # Release: very short

    return f"Created '{track_name}' with {notes_added} clave strikes over {bars} bars at {bpm} BPM."
```