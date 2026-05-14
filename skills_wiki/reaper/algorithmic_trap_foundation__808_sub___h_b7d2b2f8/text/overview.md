### 1. High-level Design Pattern Extraction

> **Skill Name**: Algorithmic Trap Foundation (808 Sub + Halftime Groove)

* **Core Musical Mechanism**: This pattern establishes the foundational rhythm and low-end harmony of Trap and modern Hip-Hop. It relies on a "halftime" feel (snare on beat 3 at 140+ BPM), heavily syncopated kick drums, and rapid-fire hi-hat rolls (16th/32nd notes). The harmonic anchor is an "808 Sub" — a sustained, deep sine/triangle wave that hits simultaneously with the kick drum to create massive low-frequency impact while outlining the chord progression.
* **Why Use This Skill (Rationale)**: The tutorial demonstrates combining a high-end synth (Massive X) for a dedicated 808 Sub with an algorithmic beat generator (Reason Rack's Beat Map + Kong Drum Designer). This workflow separates the sub-bass from the drum sampler to allow precise harmonic tuning and synthesis of the bass, while letting the drum sampler handle the transient percussion. Musically, the syncopation between the heavy 808 kicks and the fast, rigid hi-hats creates the characteristic tension and "bounce" of modern trap music.
* **Overall Applicability**: Perfect for Hip-Hop beats, Trap drops in EDM, Future Bass, or any genre requiring an aggressive, halftime rhythmic foundation with tuned sub-bass.
* **Value Addition**: Since the tutorial relies on third-party generative VSTs (Reason Beat Map), this skill extracts the *result* of that generative process into pure, reusable REAPER MIDI and native synthesis. It provides a mathematically accurate trap groove and a synthesized 808 bassline that dynamically adapts to the selected key, scale, and bar count.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 130–150 BPM (Defaulting to 140 BPM).
  - **Grid**: 1/16th notes with halftime phrasing.
  - **Kick**: Hits on beat 1, beat 3.5, and is syncopated on the "and" of beat 4 in alternating bars.
  - **Snare/Clap**: Rigidly placed on beat 3 of every bar.
  - **Hi-hat**: Continuous 8th notes, punctuated by 16th-note "rolls" at the end of phrases to transition into the next bar.
* **Step B: Pitch & Harmony**
  - **808 Sub**: Pitched in the C1-C2 range (40Hz–60Hz sweet spot). It follows a 1-6-5 minor progression (Root for bars 1-2, minor 6th degree for bar 3, perfect 5th degree for bar 4). 
  - **Note Length**: 808 notes are held for 3-4 sixteenths, mimicking the long decay of an analog 808 tom.
* **Step C: Sound Design & FX**
  - **808 Synth**: A combination of a Sine wave (for pure sub pressure) and a slight Triangle wave (for low-mid harmonics so it translates on smaller speakers), utilizing a fast attack and moderate release.
* **Step D: Mix & Automation**
  - The sub bass is isolated on its own track with native REAPER synthesis, while the drums are sequenced via standard GM MIDI mapping (Kick 36, Snare 38, Hat 42) ready for any drum sampler.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Trap Drum Groove | MIDI note insertion | Allows precise 16th-note quantization, velocity variation for hi-hats, and programmatic generation of trap rolls. |
| 808 Sub Harmonics | MIDI note insertion + Scale Lookup | Calculates the exact pitch for the 808 based on the input key and scale to ensure the sub-bass is musically in tune. |
| 808 Sound Design | FX chain (ReaSynth) | Recreates the core acoustic property of the Massive X "808 Sub" preset using stock REAPER plugins (pure sine + triangle blend). |

> **Feasibility Assessment**: 80% — While the exact timbres of Native Instruments Massive X and Reason Kong Drum Designer cannot be invoked without the user owning those third-party VSTs, the underlying algorithmic drum pattern, the halftime MIDI timing, and the synthesized 808 sub-bass tonal setup are fully reproduced using REAPER's native ReaSynth and MIDI API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Trap Beat",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Algorithmic Trap Drum Groove and an 808 Sub Bass in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM (typically 130-150 for trap).
        key: Root note (e.g., C, C#, D).
        scale: Scale type (e.g., minor, harmonic_minor).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # Music theory lookup tables for the 808 Bassline
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
    
    beat_len = 60.0 / bpm
    sixteenth_len = beat_len / 4.0
    bar_len = beat_len * 4

    # Helper function to create a track and a full-length MIDI item
    def setup_track_and_item(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_len * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === Step 2: Track Setup ===
    track_808, take_808 = setup_track_and_item(f"{track_name} 808 Sub")
    track_drums, take_drums = setup_track_and_item(f"{track_name} Drums (Kong/BeatMap)")

    # Construct the 808 Sub tone using ReaSynth
    # 1 is the 'instantiate' flag to add the FX
    fx_idx = RPR.RPR_TrackFX_AddByName(track_808, "ReaSynth", False, 1)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 0, 0.8)  # Volume
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 2, 0.0)  # Square mix (0%)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 3, 0.0)  # Saw mix (0%)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 4, 0.3)  # Triangle mix (30% for harmonics)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 5, 1.0)  # Extra Sine (100% for sub pressure)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 6, 0.0)  # Attack (Instant)
    RPR.RPR_TrackFX_SetParam(track_808, fx_idx, 9, 0.7)  # Release (Long decay for trap 808s)
    
    # Calculate base 808 pitch (Ensure it sits in the 40-60Hz sub range)
    root_idx = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    base_pitch = root_idx + 24  # Starts at C1
    if base_pitch < 28:         # If lower than E1, pitch up an octave to avoid muddiness
        base_pitch += 12

    # === Step 3: MIDI Pattern Generation ===
    for b in range(bars):
        base_step = b * 16
        
        # --- Kick Drum & 808 Harmonics ---
        kicks = [0, 10]          # Kick on Beat 1, and the 'and' of Beat 3
        if b % 2 == 1:
            kicks.append(14)     # Add syncopated kick before the end of even bars
            
        for k in kicks:
            start = (base_step + k) * sixteenth_len
            
            # Insert Kick Drum (GM Note 36)
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, start + sixteenth_len), 
                                    0, 36, velocity_base, False)
            
            # Insert 808 Sub (Follows Kick rhythm, changes pitch based on progression)
            pitch = base_pitch
            if b % 4 == 2:
                pitch = base_pitch + scale_intervals[5 % len(scale_intervals)] # Move to 6th degree
            elif b % 4 == 3:
                pitch = base_pitch + scale_intervals[4 % len(scale_intervals)] # Move to 5th degree
                
            RPR.RPR_MIDI_InsertNote(take_808, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, start), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take_808, start + sixteenth_len * 3.5), 
                                    0, pitch, velocity_base, False)

        # --- Halftime Snare ---
        snare_start = (base_step + 8) * sixteenth_len # Beat 3
        RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, snare_start), 
                                RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, snare_start + sixteenth_len), 
                                0, 38, velocity_base, False)

        # --- Algorithmic Hi-Hats with Rolls ---
        for h in range(16):
            play_hat = False
            # Standard 8th notes
            if h % 2 == 0:
                play_hat = True
            # Trap Roll logic: Insert fast 16ths at specific turnaround points
            elif b % 2 == 1 and h in [13, 15]: 
                play_hat = True
            elif b % 4 == 3 and h in [5, 7]:   
                play_hat = True
                
            if play_hat:
                hat_start = (base_step + h) * sixteenth_len
                # Add slight velocity variation to rolls to mimic realistic beat machines
                vel = int(velocity_base * 0.8) if h % 2 == 0 else int(velocity_base * 0.95)
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, 
                                        RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hat_start), 
                                        RPR.RPR_MIDI_GetPPQPosFromProjTime(take_drums, hat_start + sixteenth_len * 0.5), 
                                        0, 42, vel, False)

    # Sort MIDI items to finalize insertion
    RPR.RPR_MIDI_Sort(take_808)
    RPR.RPR_MIDI_Sort(take_drums)
    RPR.RPR_UpdateArrange()

    return f"Created Trap Beat ({bars} bars, {bpm} BPM) with dynamic 808 Sub Bass in {key} {scale}."
```