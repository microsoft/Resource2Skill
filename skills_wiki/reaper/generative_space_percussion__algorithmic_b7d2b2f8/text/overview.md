### 1. High-level Design Pattern Extraction

> **Skill Name**: Generative Space Percussion (Algorithmic Sequencing)

* **Core Musical Mechanism**: The tutorial demonstrates building a generative, algorithmic drum loop using the "Beat Map" algorithmic drum sequencer routed to the "Kong" drum machine, and subsequently washing it in a large hall reverb ("RV7000"). The defining signature is the probabilistic, syncopated, off-beat rhythmic feel combined with an expansive spatial atmosphere.
* **Why Use This Skill (Rationale)**: Algorithmic drum generation creates rhythms that feel more organic, surprising, and less rigid than standard grid-based step sequencing. Emphasizing off-beats creates a driving syncopation. Routing this directly into a large reverb smears the transients, transforming discrete drum hits into a cohesive, atmospheric texture often used in IDM, ambient techno, and generative music.
* **Overall Applicability**: Excellent for brainstorming starting grooves in electronic music, creating background rhythmic textures, or generating ambient pulse layers that sit behind a main beat.
* **Value Addition**: Instead of manually plotting a 4-bar loop, this skill encodes probabilistic logic to generate off-beat focused rhythms on the fly, dynamically tuning the "percussion" elements to the user's requested key and scale to ensure harmonic cohesion.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature / BPM**: 4/4, typically 110-125 BPM for this style.
  - **Grid**: 16th-note subdivisions.
  - **Pattern Logic**: Emulates the "OffBeat" preset shown in the video. Kicks anchor the downbeats (1 and 3) with a slight probability of syncopated 16th-note hits. Snares sit on 2 and 4 with occasional ghost notes. The high-frequency element (hi-hat) is heavily weighted to trigger on off-beat 16th notes with higher velocities, while on-beat hits are sparse and quiet.

* **Step B: Pitch & Harmony**
  - Because we are replacing a third-party drum machine with native REAPER tools, we will map the "Kick", "Snare", and "Hat" roles to specific pitches within the user's selected Key and Scale. 
  - Root note = Bass/Kick equivalent.
  - 5th scale degree = Snare equivalent.
  - Octave + 3rd scale degree = High-frequency blip/Hat equivalent.

* **Step C: Sound Design & FX**
  - **Instrument**: Native `ReaSynth` to produce percussive synthesized blips triggered by short MIDI notes.
  - **Reverb**: Native `ReaVerbate` replacing the Reason RV7000.
  - **Reverb Parameters**: Wet signal mixed high (~60%), large Room Size (~90%) to emulate the "ALL Hall" preset selected in the video, creating a dense, washed-out tail.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Algorithmic Rhythms | Python random library + `RPR_MIDI_InsertNote` | Simulates the proprietary "Beat Map" algorithm by generating probabilistic MIDI events on a new take. |
| Scale-tuned Percussion | Music theory lookup dictionaries | Ensures the generated percussive synths fit perfectly into the overall track's harmonic framework. |
| Reverb Wash | FX Chain (`ReaVerbate`) | Matches the user's action of adding the RV7000 Reverb module to process the dry sequence. |

> **Feasibility Assessment**: 70% — The tutorial explicitly relies on inserting the proprietary third-party VST *Reason Rack Plugin* and manipulating its internal modules (Beat Map, Kong, RV7000). Because ReaScript cannot script the internal UI of third-party VSTs, this code reproduces the *core musical concept* (an off-beat algorithmic drum sequence drowned in hall reverb) using 100% native REAPER tools.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Generative Space Perc",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an algorithmic, generative syncopated percussion pattern washed in reverb.
    Simulates the Reason 'Beat Map' to 'RV7000' workflow natively in REAPER.
    """
    import random
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

    # === Step 3: Calculate Timings ===
    beats_per_bar = 4
    qn_sec = 60.0 / bpm
    item_len = (qn_sec * beats_per_bar) * bars
    
    # Very short notes for percussive plucks
    note_duration_sec = qn_sec * 0.15 

    # === Step 4: Create MIDI Item ===
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_len)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 5: Derive Pitches ===
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Tune "drums" to the requested scale for a melodic generative feel
    kick_pitch = 36 + root_val                                          # C2 octave (Root)
    snare_pitch = 36 + root_val + scale_intervals[4 % len(scale_intervals)] # 5th degree
    hihat_pitch = 48 + root_val + scale_intervals[2 % len(scale_intervals)] # Octave up + 3rd degree

    # === Step 6: Generative Rhythmic Algorithm ===
    note_count = 0
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            for div in range(4):  # 16th note subdivisions
                time_sec = (bar * beats_per_bar * qn_sec) + (beat * qn_sec) + (div * 0.25 * qn_sec)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, time_sec + note_duration_sec)
                
                # "Kick" logic: Anchor on beats 1 and 3, occasional syncopation
                if beat in [0, 2] and div == 0:
                    vel = min(127, velocity_base + 10)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, kick_pitch, vel, True)
                    note_count += 1
                elif div == 3 and random.random() > 0.75:
                    vel = min(127, int(velocity_base * 0.7))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, kick_pitch, vel, True)
                    note_count += 1
                    
                # "Snare" logic: Anchor on beats 2 and 4, occasional ghost notes
                if beat in [1, 3] and div == 0:
                    vel = min(127, velocity_base + 15)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, snare_pitch, vel, True)
                    note_count += 1
                elif div == 2 and random.random() > 0.85:
                    vel = min(127, int(velocity_base * 0.4))
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, snare_pitch, vel, True)
                    note_count += 1
                    
                # "Hi-hat" logic: Emulate "OffBeat" preset. Favor offbeats.
                is_offbeat = (div % 2 != 0)
                prob = 0.85 if is_offbeat else 0.35
                if random.random() < prob:
                    vel = random.randint(int(velocity_base * 0.75), min(127, velocity_base + 5)) if is_offbeat else random.randint(30, 60)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, hihat_pitch, vel, True)
                    note_count += 1

    RPR.RPR_MIDI_Sort(take)

    # === Step 7: Sound Design FX Chain ===
    # 1. Add Synth to produce sound from our MIDI
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # 2. Add Reverb to create the large atmospheric space (emulating RV7000)
    fx_verb = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    
    # Configure Reverb parameters to mimic the "ALL Hall" setting
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 0, 0.6)  # Wet signal
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 1, 0.8)  # Dry signal
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 2, 0.9)  # Room size (Very Large)
    RPR.RPR_TrackFX_SetParam(track, fx_verb, 3, 0.4)  # Dampening

    return f"Created '{track_name}' with {note_count} algorithmically generated notes in {key} {scale} over {bars} bars at {bpm} BPM."
```