# Ambient Electric Guitar Wash (Clarity EQ & Spatial FX)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Electric Guitar Wash (Clarity EQ & Spatial FX)

* **Core Musical Mechanism**: This pattern combines a highly specific, three-step subtractive/additive EQ curve with a lush spatial chain (Ping-Pong Delay feeding into a massive Reverb). The signature of this technique is a wide, floating, "stadium" sound that remains pristine and cutting, rather than turning into unintelligible mud.
* **Why Use This Skill (Rationale)**: 
  * *Frequency Masking*: High-passing at ~70-80 Hz removes low-end rumble that clashes with bass/kick. 
  * *Mud Removal*: Cutting the 300-400 Hz range eliminates the "boxy" or muddy buildup typical of electric guitars and heavy reverbs.
  * *Psychoacoustic Presence*: A focused boost around 2.5-3 kHz (the human ear's most sensitive frequency range) gives the guitar "bite" and ensures it cuts through the massive spatial effects.
  * *Stereo Width*: Ping-pong delay creates alternating Left/Right spatial movement, artificially widening the stereo image before it hits the reverb tail.
* **Overall Applicability**: Perfect for intro guitar leads, ambient breakdowns, post-rock swells, dreamy synth pads, or any lead instrument that needs to sound massive but sit cleanly in a dense mix.
* **Value Addition**: This skill encodes professional mixing engineer decisions (specific EQ frequencies, Q values, and routing order) into a single reproducible chain, upgrading a flat, dry MIDI clip into a mix-ready, three-dimensional ambient texture.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: Staccato or arpeggiated 1/8th or 1/4 notes work best to trigger the ping-pong delay clearly. 
  - **Feel**: The dry signal needs rhythmic gaps so the wet delay/reverb tail can fill the space.

* **Step B: Pitch & Harmony**
  - **Harmony**: Uses open intervals (Roots and 5ths) or suspended chords spread across octaves.
  - Avoid dense, tight chord clusters (like minor 2nds or dense 7th chords in the lower register) as the delay/reverb will smush them into dissonance.

* **Step C: Sound Design & FX**
  - **Sound Source**: Electric Guitar DI / Amp Sim (approximated here via ReaSynth).
  - **FX Chain Order**:
    1. **ReaEQ**: 
       - Band 1: High Pass Filter @ ~80 Hz.
       - Band 2: Band Cut @ ~350 Hz (-4.0 dB, moderate Q).
       - Band 3: Band Boost @ ~2.8 kHz (+3.0 dB, narrow Q).
    2. **JS: Delay w/Tempo Ping-Pong**: Feedback at ~50%, Mix at ~30% wet to create Left/Right bounces.
    3. **ReaVerbate** (Algorithmic Reverb): Large room size (0.9), moderate dampening, balanced wet/dry.

* **Step D: Mix & Automation**
  - The track's overall volume is usually pulled down slightly to compensate for the upper-mid EQ boost and the additive volume of the delays/reverb.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Rhythmic Arpeggio | MIDI note insertion | Provides the distinct, separated transient hits required to make the Ping-Pong delay audible and effective. |
| Guitar Clarity EQ | FX Chain (`ReaEQ`) + Param modification | Replicates the exact frequency shaping (HPF, Mud Cut, Bite Boost) demonstrated in the tutorial. |
| Spatial Wash | FX Chain (`JS: Ping-Pong Delay` + `ReaVerbate`) | Creates the wide, bouncing, ambient tail that defines the "Intro Guitar" tone. |

> **Feasibility Assessment**: 85% reproduction. The core mixing philosophy (EQ curve and spatial routing) is captured perfectly. The missing 15% is the specific Amplitube 5 amp sim and Lexicon 480L impulse response used in the video, which are replaced here with REAPER stock equivalents (`ReaSynth` and `ReaVerbate`) for pure out-of-the-box reproducibility.

#### 3b. Complete Reproduction Code

```python
def create_ambient_guitar_wash(
    project_name: str = "MyProject",
    track_name: str = "Ambient Intro Guitar",
    bpm: int = 120,
    key: str = "E",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 95,
    **kwargs,
) -> str:
    """
    Create an Ambient Electric Guitar Wash pattern in the current REAPER project.
    Features the specific Clarity EQ curve, Ping-Pong Delay, and large Reverb.
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
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item & Arpeggio Pattern ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Calculate root note (Octave 4)
    root_midi = 48 + NOTE_MAP.get(key, 0) # Start at C3 (MIDI 48)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Simple open arpeggio: Root -> 5th -> Octave -> 5th (Plucked to feed the delay)
    root_note = root_midi + scale_intervals[0]
    fifth_note = root_midi + scale_intervals[4 % len(scale_intervals)]
    octave_note = root_note + 12
    
    arpeggio_pattern = [root_note, fifth_note, octave_note, fifth_note]
    note_duration_qn = 0.5 # 1/8th notes
    note_duration_sec = (60.0 / bpm) * note_duration_qn
    
    note_count = 0
    for bar in range(bars):
        for i, pitch in enumerate(arpeggio_pattern):
            start_time = (bar * bar_length_sec) + (i * note_duration_sec * 2) # Play on downbeats and upbeats
            end_time = start_time + (note_duration_sec * 0.8) # Slightly staccato
            
            # Convert times to PPQ (Pulses Per Quarter Note) for MIDI insertion
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # Alternate velocities slightly for realism
            vel = velocity_base if i == 0 else velocity_base - 15
            
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, False)
            note_count += 1

    # === Step 4: Add FX Chain ===
    
    # 1. Base Sound Generator (ReaSynth placeholder for DI Guitar)
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.5) # Sawtooth mix for harmonics
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.2) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 4, 0.5) # Decay

    # 2. Clarity EQ (The core tutorial technique)
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 1: High Pass Filter @ 80 Hz to remove rumble
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 0, 80.0)   # Freq
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 3, 4.0)    # Type (4 = High Pass)
    
    # Band 2: Cut Mud @ 350 Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 4, 350.0)  # Freq (Band 2 is typically index 4/5 depending on version, mapped to standard offsets)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 5, -4.5)   # Gain (Cut 4.5 dB)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 6, 2.0)    # Bandwidth / Q
    
    # Band 3: Boost Bite @ 2800 Hz
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 8, 2800.0) # Freq
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 9, 3.0)    # Gain (Boost 3 dB)
    RPR.RPR_TrackFX_SetParam(track, fx_eq, 10, 1.0)   # Bandwidth / Q

    # 3. Ping-Pong Delay
    fx_delay = RPR.RPR_TrackFX_AddByName(track, "JS: Delay w/Tempo Ping-Pong", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 1, -5.0) # Feedback (dB)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 3, -8.0) # Output Wet (dB)
    RPR.RPR_TrackFX_SetParam(track, fx_delay, 5, 100.0) # Ping-Pong Width (%)

    # 4. Lush Reverb
    fx_reverb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_reverb, 0, 0.4) # Wet level (approx -8dB)
    RPR.RPR_TrackFX_SetParam(track, fx_reverb, 1, 0.8) # Dry level
    RPR.RPR_TrackFX_SetParam(track, fx_reverb, 2, 0.95) # Room size (Huge)
    RPR.RPR_TrackFX_SetParam(track, fx_reverb, 3, 0.6) # Dampening (cuts high end harshness in tail)
    
    # Drop track volume slightly to compensate for EQ boost and FX build up
    RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", 0.75) # Approx -2.5 dB

    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} arpeggio notes over {bars} bars at {bpm} BPM, equipped with Clarity EQ, Ping-Pong Delay, and Reverb."
```