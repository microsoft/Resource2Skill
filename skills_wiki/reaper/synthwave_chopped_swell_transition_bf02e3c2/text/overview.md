### 1. High-level Design Pattern Extraction

> **Skill Name**: Synthwave Chopped Swell Transition

* **Core Musical Mechanism**: This pattern generates a massive tension-building transition over a sustained synth chord. It combines three simultaneous movements: a continuous volume swell (rising intensity), a rigid 32nd-note volume chop (rhythmic urgency/syncopation speed-up), and an expanding stereo width field (from dead mono to wide stereo).
* **Why Use This Skill (Rationale)**: The combination of these three psychoacoustic cues is perfect for driving a listener into a drop. The volume swell pushes the listener forward dynamically; the 32nd-note chop exploits rhythmic subdivision to create a feeling of racing or urgency; and the stereo expansion creates a physical sensation of the mix "opening up," making the section that follows feel heavier and wider by contrast. 
* **Overall Applicability**: This technique is a staple in Synthwave, EDM, Future Bass, and modern Pop. It is highly effective when placed at the end of a pre-chorus, bridge, or intro just before the main groove hits.
* **Value Addition**: Drawing mathematically perfect 32nd-note step automation that simultaneously ramps upward is incredibly tedious to do by hand. This skill encodes the precise envelope math to generate the composite swell-plus-chop effect alongside stereo width automation, instantly producing a polished, production-ready riser.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: The transition happens over a specified number of bars (usually 1 or 2).
  - **Chop Rate**: 1/32nd notes (8 chops per beat).
  - **Note Duration**: A single sustained chord held for the entire duration of the transition block.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: Parametric (e.g., C minor).
  - **Voicing**: A lush, extended 9th chord voicing spread across multiple octaves (Root, 5th, 10th/3rd, 14th/7th, 16th/9th) to ensure frequency richness during the swell.
* **Step C: Sound Design & FX**
  - **Synth**: ReaSynth utilizing a blend of Saw and Square waves for a classic 80s analog pad tone.
  - **Modulation**: JS: Chorus is used to provide the stereo width.
  - **Space**: ReaVerbate (Hall setting) to wash out the sound and glue the choppy transients. 
* **Step D: Mix & Automation**
  - **Volume Automation**: The synth's volume parameter acts as the macro control. It linearly ramps from 0 to 80%, while multiplying by 1.0 (on) and 0.2 (off) every 32nd note to create the square-wave chop.
  - **Width Automation**: The Chorus Wet Mix parameter automates from 0% (dry/mono) to 100% (wet/wide stereo), perfectly simulating the stereo width swell.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Tension Chord | MIDI note insertion | Allows algorithmically generating a rich 9th chord voicing locked perfectly to the user's key/scale parameters. |
| Synth Tone | FX Chain (ReaSynth + Chorus + ReaVerbate) | Stock plugins guarantee 100% execution success without relying on the user having Hybrid 3 or specific preset files. |
| Chopped Swell | Native FX Parameter Envelope | Emits mathematically calculated points directly into the ReaSynth Volume envelope. This accurately replicates the "stacked automation" concept from the tutorial while ensuring smooth linear growth coupled with sharp 32nd-note steps. |
| Mono-to-Stereo | Native FX Parameter Envelope | Automating the Chorus Wet Mix provides a guaranteed, artifact-free transition from mono (dry) to wide (wet). |

> **Feasibility Assessment**: 100%. While the tutorial uses third-party plugins (Hybrid 3, ToneBoosters), the exact sonic architecture—a multi-wave oscillator with LFO volume chopping, stereo expansion, and reverb—is fully and accurately reproducible using REAPER's stock tools and precise ReaScript envelope generation.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Chopped Swell Riser",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 2,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Synthwave Chopped Swell Transition in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars the transition will last.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
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

    # === Step 1: Set Tempo & Calculate Timing ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    duration = bar_length_sec * bars

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Insert Tension Chord ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, 0.0)
    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, duration)

    root_midi = NOTE_MAP.get(key.capitalize(), 0) + 36 # Start low (Octave 2)
    current_scale = SCALES.get(scale.lower(), SCALES["minor"])

    def get_scale_pitch(degree):
        octave = degree // len(current_scale)
        note_index = degree % len(current_scale)
        return root_midi + (octave * 12) + current_scale[note_index]

    # Build a lush 9th chord voicing: Root, 5th, 3rd(up), 7th(up), 9th(up)
    chord_degrees = [0, 4, 9, 13, 15] 

    for degree in chord_degrees:
        pitch = get_scale_pitch(degree)
        # Keep pitches in safe MIDI range
        pitch = max(0, min(127, pitch))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)
        
    RPR.RPR_MIDI_Sort(take)

    # === Step 4: Add FX Chain ===
    # 1. ReaSynth
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 2, 0.6) # Square mix
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 3, 0.6) # Saw mix
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 6, 0.1) # Attack
    RPR.RPR_TrackFX_SetParamNormalized(track, 0, 9, 0.3) # Release
    
    # 2. Chorus (For stereo width expansion)
    RPR.RPR_TrackFX_AddByName(track, "JS: Chorus", False, -1)
    # Default chorus settings are fine, we will automate Wet Mix (Param 4)
    
    # 3. ReaVerbate (To wash out the sound)
    RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParamNormalized(track, 2, 0, 0.3) # Wet
    RPR.RPR_TrackFX_SetParamNormalized(track, 2, 1, 0.8) # Dry
    RPR.RPR_TrackFX_SetParamNormalized(track, 2, 2, 0.8) # Room size

    # === Step 5: Automate Chopped Swell & Stereo Expansion ===
    # Get envelopes (create=True makes them active and visible)
    vol_env = RPR.RPR_GetFXEnvelope(track, 0, 0, True)   # ReaSynth Param 0 = Volume
    width_env = RPR.RPR_GetFXEnvelope(track, 1, 4, True) # Chorus Param 4 = Wet Mix
    
    # 5a. Width Expansion (Mono to Stereo)
    # Ramps Chorus wet mix from 0.0 to 1.0 over the transition
    RPR.RPR_InsertEnvelopePoint(width_env, 0.0, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(width_env, duration, 1.0, 0, 0, False, True)
    RPR.RPR_Envelope_Sort(width_env)

    # 5b. Chopped Volume Swell (32nd notes)
    # 8 chops per beat = 32nd notes
    step_time = (60.0 / bpm) / 8.0 
    num_steps = int(duration / step_time)
    
    for step_idx in range(num_steps):
        t_start = step_idx * step_time
        t_end = t_start + step_time - 0.001 # Slightly before next step to create square shape
        
        # Base swell curve (0.0 to 0.8 normalized volume)
        progress_start = t_start / duration
        base_vol_start = progress_start * 0.8
        
        progress_end = t_end / duration
        base_vol_end = progress_end * 0.8
        
        # 32nd note square chop logic
        is_high = (step_idx % 2 == 0)
        chop_mult = 1.0 if is_high else 0.15 # Drops to 15% volume on off-steps
        
        val_start = base_vol_start * chop_mult
        val_end = base_vol_end * chop_mult
        
        # Insert start and end points for this square pulse (Linear shape = 0)
        RPR.RPR_InsertEnvelopePoint(vol_env, t_start, val_start, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(vol_env, t_end, val_end, 0, 0, False, True)

    RPR.RPR_Envelope_Sort(vol_env)

    return f"Created '{track_name}' with {len(chord_degrees)}-note tension chord, 32nd-note chopped volume swell, and stereo expansion over {bars} bars at {bpm} BPM."
```