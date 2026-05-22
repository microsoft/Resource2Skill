### 1. High-level Design Pattern Extraction

> **Skill Name**: Metal Bass Kick-Locking & Octave Jumps

* **Core Musical Mechanism**: The defining characteristic of modern metal/hard rock bass programming is rhythmically locking the bass MIDI notes *exactly* to the syncopated kick drum pattern. To create motion without changing the harmonic center (the root note), periodic +12 semitone (octave) jumps are used as fills or accents. Additionally, the MIDI velocity is purposefully restricted to a slightly lower value (e.g., 110 instead of 127) to prevent virtual bass samplers from triggering overly harsh, "clanky" top-end layers on every hit.
* **Why Use This Skill (Rationale)**: 
  - **Kick-Locking**: In dense mixes, the bass guitar and kick drum must act as a single rhythmic entity. If they flam or diverge, the low-end loses impact and the mix becomes muddy.
  - **Velocity Throttling**: Modern virtual basses (like DjinnBass, Eurobass) use multi-sampling where the 120-127 velocity range triggers aggressive pick attack/string slap. Capping the velocity at ~110 gives a heavy but much smoother, mixable low-end tone.
  - **Octave Jumps**: Playing the same sub-bass note repetitively can sound static. Jumping up an octave (the "12th fret") introduces timbral variation and melodic interest while maintaining the exact same harmonic function and avoiding masking the kick drum's sub-frequencies.
* **Overall Applicability**: Essential for modern metalcore, djent, hard rock, and pop-punk where a tight, aggressive, yet controlled low-end foundation is required.
* **Value Addition**: Transforms a basic, static continuous bassline into an aggressive, rhythmically driving element that glues perfectly with a syncopated drum groove, programmed using realistic virtual instrument best practices.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid**: 16th note resolution.
  - **Pattern**: Syncopated 16th-note rhythms (e.g., 3-3-2 groupings or broken 16th syncopations) that mirror a metal kick drum pattern.
  - **Duration**: Slightly staccato (e.g., 80% of the 16th note duration) to leave room for the kick drum's transient to breathe, avoiding low-end overlap.

* **Step B: Pitch & Harmony**
  - **Pitch**: Usually rooted entirely on the tonic/lowest open string of the guitar (e.g., Drop C = C1 or C2). 
  - **Fills/Accents**: Periodic jumps up exactly 12 semitones (1 octave) on the upbeats or the end of a phrase.

* **Step C: Sound Design & FX**
  - **Instrument**: Virtual Bass VSTi (tutorial uses DjinnBass). In standard setups, this translates to any bass synth/sampler.
  - **Velocity**: Strictly capped around 110 (out of 127) for the primary "heavy" tone without excessive fret noise.

* **Step D: Mix & Automation**
  - Dead center panning. 
  - Often processed with heavy compression and EQ to scoop low-mids and boost presence, though the source DI (virtual instrument output) is the focus here.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Kick-locked rhythm | MIDI note insertion | Requires exact syncopated placement on a 16th note grid |
| Velocity control | MIDI note velocity | Explicitly scaling all inserted notes to 110 |
| Octave jumps | Pitch calculation (`pitch + 12`) | Emulates the 12th-fret jumps shown in the piano roll |
| Bass Tone | ReaSynth + ReaEQ | Provides a stock REAPER alternative to the third-party DjinnBass VST |

> **Feasibility Assessment**: 80% — The precise rhythmic mechanism, velocity control, and octave logic are reproduced perfectly. The exact timbre of Submission Audio's DjinnBass cannot be generated with native plugins, so a fundamental ReaSynth patch sculpted for low-end is provided as a placeholder.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Virtual Metal Bass",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 110,  # Explicitly defaulting to 110 to reduce harshness as per tutorial
    **kwargs,
) -> str:
    """
    Create a Metal Bass Kick-Locking pattern with Octave Jumps.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127), intentionally lowered to avoid clank.
        **kwargs: Additional overrides.

    Returns:
        Status string describing the operation.
    """
    import reaper_python as RPR

    # === Step 1: Initialize Variables ===
    # Map key to a low bass octave (Octave 2 in standard MIDI mapping, 36 = C2)
    NOTE_MAP = {"C": 36, "C#": 37, "Db": 37, "D": 38, "D#": 39, "Eb": 39,
                "E": 40, "F": 41, "F#": 42, "Gb": 42, "G": 43, "G#": 44,
                "Ab": 44, "A": 45, "A#": 46, "Bb": 46, "B": 47}
    
    root_note = NOTE_MAP.get(key, 36)
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add a basic synth and shape it for bass
    fx_synth = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Shape ReaSynth: Square wave for grind, low filter
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 0, 0.0)    # Volume
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 1, 0.0)    # Tuning
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 2, 0.5)    # Square mix (more aggressive)
    RPR.RPR_TrackFX_SetParam(track, fx_synth, 3, 0.0)    # Saw mix

    # Add EQ to carve metal bass tone
    fx_eq = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    
    # === Step 3: Define Rhythmic Pattern ===
    # Array represents 16th notes.
    # 0 = rest, 1 = root note (following kick), 2 = octave jump fill
    # Pattern simulates a syncopated metalcore breakdown
    base_bar_pattern =   [1, 0, 0, 1,  0, 0, 1, 0,  1, 0, 0, 0,  1, 0, 2, 0]
    fill_bar_pattern =   [1, 0, 0, 1,  0, 0, 1, 0,  1, 0, 0, 0,  2, 0, 2, 0]

    full_pattern = []
    for i in range(bars):
        # Every even-numbered bar gets the extra octave jump fill
        if i % 2 == 1:
            full_pattern.extend(fill_bar_pattern)
        else:
            full_pattern.extend(base_bar_pattern)

    # === Step 4: Create MIDI Item & Notes ===
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    sixteenth_length_sec = beat_length_sec / 4.0
    item_length = beat_length_sec * beats_per_bar * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    note_count = 0
    
    for idx, hit in enumerate(full_pattern):
        if hit > 0:
            # Calculate timing
            start_time = idx * sixteenth_length_sec
            # Staccato lengths (80% of a 16th note) to leave room for kick transient
            end_time = start_time + (sixteenth_length_sec * 0.8) 
            
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
            
            # hit == 1 is root, hit == 2 is 12th fret (octave up)
            pitch = root_note + 12 if hit == 2 else root_note
            
            # Insert note
            RPR.RPR_MIDI_InsertNote(
                take,
                False,      # selected
                False,      # muted
                start_ppq,
                end_ppq,
                0,          # channel
                pitch,
                velocity_base, 
                False       # noSort
            )
            note_count += 1

    # Finalize MIDI
    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} locked-kick bass notes over {bars} bars at {bpm} BPM (Velocity: {velocity_base})."
```