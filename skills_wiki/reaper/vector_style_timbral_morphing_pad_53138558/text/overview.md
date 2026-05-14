# Vector-Style Timbral Morphing Pad

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Vector-Style Timbral Morphing Pad

* **Core Musical Mechanism**: The defining feature of this pattern is the continuous, cyclic crossfading between multiple distinct synthesizer timbres. By applying synchronized Low Frequency Oscillators (LFOs) to the volume of different synth layers and offsetting their phases evenly (e.g., 0°, 120°, 240°), the texture smoothly "rotates" through different sonic characters while sustaining a single chord progression.
* **Why Use This Skill (Rationale)**: Static pad chords can quickly become ear-fatiguing or boring. Timbral morphing introduces internal movement and evolution without requiring complex harmonic changes or melodic busyness. Psychoacoustically, the shifting spectral balance (from pure sine to saturated harmonics to wide chorus) keeps the listener's brain engaged, mimicking the complex harmonic evolution found in acoustic instruments (like a bowing change on a cello or a breath swell on a brass instrument). 
* **Overall Applicability**: This technique is essential for creating evolving, atmospheric pads, sustaining drones, or complex textural soundbeds. It shines in ambient music, cinematic underscoring, and intros/breakdowns in electronic music where harmony moves slowly and texture takes the lead.
* **Value Addition**: Compared to a static MIDI block, this skill encodes advanced synthesis techniques (Vector Synthesis) into standard DAW tools. It demonstrates how to use mathematics (phase-offset sine waves) to create musical breath and movement, and includes a programmatic diatonic chord generator that ensures the underlying harmony is always musical.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Grid**: Mid-to-slow tempos (90-120 BPM). 
  - **Rhythm**: Whole-note chords spanning full bars to allow the slow LFOs time to complete their cycles.
  - **Modulation Timing**: LFOs are tempo-synced, completing one full cycle every 2 bars, creating a slow, breathing rhythm independent of the MIDI note attacks.

* **Step B: Pitch & Harmony**
  - **Harmony**: A 4-bar diatonic progression (i - VI - III - VII in minor, or I - vi - IV - V in major).
  - **Voicings**: Extended 4-note voicings (7th chords) built by stacking thirds from the chosen scale.
  - **Pitch Offsets**: The three synth layers are offset by -1, 0, and +1 octaves, respectively, so the morphing travels across the frequency spectrum as well as across timbres.

* **Step C: Sound Design & FX**
  - **Layer 1 (Lows)**: Pure oscillator (`ReaSynth`), pitched down an octave, panned slightly left.
  - **Layer 2 (Mids)**: Oscillator (`ReaSynth`) driven through harmonic distortion (`JS: Saturation`), original octave, panned center.
  - **Layer 3 (Highs)**: Oscillator (`ReaSynth`) widened with `JS: Chorus`, pitched up an octave, panned slightly right.
  - **Master Bus**: `ReaVerbate` on the parent folder to glue the layers together in a shared acoustic space.

* **Step D: Mix & Automation**
  - **The Morph Engine**: Volume automation envelopes are drawn using offset Cosine waves.
    - Layer 1 Phase: 0 radians (starts at max volume)
    - Layer 2 Phase: 2π/3 radians (120 degrees)
    - Layer 3 Phase: 4π/3 radians (240 degrees)

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Chord Progression | MIDI note insertion | Allows algorithmic generation of diatonic 7th chords based on the provided key/scale parameters. |
| Morphing Modulation | FX Parameter Automation Envelope | Drawing mathematically perfect Cosine wave points into the volume envelope is highly robust in ReaScript, avoiding brittle UI chunk manipulations while achieving the exact LFO parameter modulation shown in the tutorial. |
| Timbre Variation | FX chain (ReaSynth + JS FX) | Replicates the tutorial's use of different VSTs by using stock REAPER JS plugins (Saturation, Chorus) to drastically alter the default ReaSynth tone. |
| Routing Setup | Parent Folder + 3 Child Tracks | The tutorial routes 3 synths on 1 track out to 6 channels into a JS Mixer. Building 3 standard tracks inside a Folder achieves the exact same summing/morphing result, but is significantly more stable in Python than manipulating raw bitmask pin mappings. |

> **Feasibility Assessment**: 95% reproduction. The core musical and mathematical concept is perfectly replicated. The only deviation is substituting third-party plugins (Vital, TyrellN6) with REAPER stock FX chains to ensure it runs out-of-the-box on any user's machine.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Morphing Pad",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Vector-Style Timbral Morphing Pad in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the parent folder track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, mixolydian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.
        
    Returns:
        Status string describing the generated structure.
    """
    import math
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    base_note = NOTE_MAP.get(key, 0) + 48 # Anchor at C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_chord_notes(root_degree, intervals, base, num_notes=4):
        """Generates extended diatonic chords by stacking thirds"""
        notes = []
        for i in range(num_notes):
            deg = (root_degree + i * 2) % len(intervals)
            oct_shift = (root_degree + i * 2) // len(intervals)
            pitch = base + intervals[deg] + (oct_shift * 12)
            notes.append(min(127, max(0, pitch)))
        return notes

    # Progressions (i-VI-III-VII for minor, I-vi-IV-V for major)
    progression = [0, 5, 2, 6] if scale == "minor" else [0, 5, 3, 4]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Parent Folder ===
    start_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(start_idx, True)
    parent_track = RPR.RPR_GetTrack(0, start_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(parent_track, "P_NAME", track_name, True)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "I_FOLDERDEPTH", 1)
    RPR.RPR_SetMediaTrackInfo_Value(parent_track, "D_VOL", 0.8) # Provide headroom
    RPR.RPR_TrackFX_AddByName(parent_track, "ReaVerbate", False, -1)

    # === Synth Layer Configurations ===
    synths = [
        {"name": "Layer 1 (Lows)", "pan": -0.3, "oct": -1, "phase": 0.0, "fx": None},
        {"name": "Layer 2 (Sat)",  "pan": 0.0,  "oct": 0,  "phase": 2.0 * math.pi / 3.0, "fx": "JS: Saturation"},
        {"name": "Layer 3 (Cho)",  "pan": 0.3,  "oct": 1,  "phase": 4.0 * math.pi / 3.0, "fx": "JS: Chorus"}
    ]

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # === Step 3: Create Child Tracks, MIDI, and Modulation ===
    for i, s_cfg in enumerate(synths):
        idx = start_idx + 1 + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        child = RPR.RPR_GetTrack(0, idx)
        
        RPR.RPR_GetSetMediaTrackInfo_String(child, "P_NAME", f"{track_name} - {s_cfg['name']}", True)
        RPR.RPR_SetMediaTrackInfo_Value(child, "D_PAN", s_cfg["pan"])
        
        # Close folder on the last track
        if i == len(synths) - 1:
            RPR.RPR_SetMediaTrackInfo_Value(child, "I_FOLDERDEPTH", -1)
        else:
            RPR.RPR_SetMediaTrackInfo_Value(child, "I_FOLDERDEPTH", 0)

        # 3a. Add MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(child)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)

        # Generate Chords
        for bar in range(bars):
            deg = progression[bar % len(progression)]
            notes = get_chord_notes(deg, scale_intervals, base_note, 4)
            
            start_time = bar * bar_length_sec
            end_time = (bar + 1) * bar_length_sec
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            for pitch in notes:
                shifted_pitch = min(127, max(0, pitch + (s_cfg["oct"] * 12)))
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, shifted_pitch, velocity_base, True)
                
        RPR.RPR_MIDI_Sort(take)

        # 3b. Add FX Chain
        synth_fx_idx = RPR.RPR_TrackFX_AddByName(child, "ReaSynth", False, -1)
        if s_cfg["fx"]:
            RPR.RPR_TrackFX_AddByName(child, s_cfg["fx"], False, -1)

        # 3c. Generate LFO Volume Automation (Simulating Parameter Modulation)
        # Parameter 0 in ReaSynth is Volume. We get its envelope.
        env = RPR.RPR_GetFXEnvelope(child, synth_fx_idx, 0, True)
        
        # LFO Math: 1 full cycle every 2 bars
        lfo_freq_hz = 1.0 / (bar_length_sec * 2.0)
        step_sec = (60.0 / bpm) / 4.0 # 16th note resolution for the drawing points
        
        t = 0.0
        while t <= total_length_sec + step_sec:
            # Cosine ensures phase=0 starts at peak amplitude
            osc_val = (math.cos(2 * math.pi * lfo_freq_hz * t - s_cfg["phase"]) + 1.0) / 2.0
            # Scale to a musical range (e.g., 0.0 to 0.6)
            env_val = osc_val * 0.6
            RPR.RPR_InsertEnvelopePoint(env, t, env_val, 0, 0, False, True)
            t += step_sec
            
        RPR.RPR_Envelope_SortPoints(env)

    return f"Created '{track_name}' morphing pad structure with 3 offset synth layers over {bars} bars at {bpm} BPM."
```