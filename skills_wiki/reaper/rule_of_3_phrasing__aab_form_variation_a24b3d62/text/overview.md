### 1. High-level Design Pattern Extraction

> **Skill Name**: Rule of 3 Phrasing (AAB Form Variation)

* **Core Musical Mechanism**: The "Rule of 3" is a structural and psychological pattern where a musical idea (a melody, chord progression, or motif) is played once to introduce it, a second time to reinforce it, and altered on the third repetition to prevent listener fatigue. The core mechanism is **Expectation vs. Surprise**: building a recognizable pattern and then deliberately breaking it just as the brain begins to tune it out.

* **Why Use This Skill (Rationale)**: As explained in the tutorial, the human brain processes information through pattern recognition. The first exposure is novel. The second exposure confirms the pattern. By the third exposure, the brain anticipates the result perfectly and "tunes out," causing a loss of interest. By introducing a variation on the third repetition (going somewhere completely different, or starting the same but changing the tail end), you recapture the listener's attention and create forward musical momentum. 

* **Overall Applicability**: This is a fundamental principle of music composition applicable across all genres. It is highly effective for writing chord progressions, vocal melodies, drum fills (e.g., standard groove for 3 bars, fill on the 4th), and arrangement structures (Verse 1, Verse 2, Bridge).

* **Value Addition**: Compared to a basic looping MIDI clip, this skill encodes structural phrasing. It transforms a static 4-bar loop into a compelling 12-bar or 16-bar musical statement that guides the listener's attention naturally.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Grid**: 12-bar phrase structure.
  - **Form**: AAB. 
    - **A** (Bars 1-4): The core motif.
    - **A** (Bars 5-8): Exact repetition.
    - **B** (Bars 9-12): The variation (starts identically to A, but diverges musically in the final two bars).

* **Step B: Pitch & Harmony**
  - **Progression A**: `IV - V - I - vi` (e.g., F - G - C - Am). A standard, resolving pop progression.
  - **Progression B (Variation)**: `IV - V - ii - V` (e.g., F - G - Dm - G). Starts the same to trigger the brain's pattern recognition, but diverges into a suspended, tension-building `ii - V` turnaround instead of resolving, hooking the listener.
  - **Melody**: Follows the chord tones rhythmically for Motifs A, but switches to a faster, ascending arpeggio during the divergent chords in Motif B to emphasize the change.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a soft pluck/electric piano (sawtooth blend, short attack, medium decay, lower sustain).
  - **FX**: `ReaDelay` added lightly to provide spatial width and glue the phrases together.

* **Step D: Mix & Automation**
  - Melodic notes are struck at higher velocities than the underlying chord pads.
  - The divergent arpeggio in the final variation receives a slight velocity bump to accentuate the surprise.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| AAB Phrasing Structure | MIDI note insertion | Allows exact control over the repetition and the precise moment of musical divergence. |
| Diatonic Transposition | Programmatic Scale Math | Ensures the progression works seamlessly in any Key or Scale provided by the agent. |
| Tone Generation | FX chain (ReaSynth + ReaDelay) | Replicates the soft, chordal keyboard sound used to demonstrate the progression in the video. |

> **Feasibility Assessment**: 100% — The cognitive composition theory detailed in the video translates perfectly to a programmatic MIDI generation script using algorithmic form generation.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule of 3 Progression",
    bpm: int = 110,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, 
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 12-bar AAB "Rule of 3" chord and melody pattern in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Overridden internally to 12 to explicitly demonstrate the AAB form.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
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
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    scale_len = len(scale_intervals)
    root_pitch = NOTE_MAP.get(key.upper(), 0) + 48 # Octave 4 base

    # Helper function to get MIDI pitch by diatonic scale degree
    def get_pitch(degree, octave_offset=0):
        octave = (degree // scale_len) + octave_offset
        idx = degree % scale_len
        return root_pitch + scale_intervals[idx] + (octave * 12)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Synth and FX ===
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.4) # Saw blend
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.5) # Pulse width
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.02) # Attack
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.5) # Decay
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.3) # Sustain
    RPR.RPR_TrackFX_SetParam(track, fx_idx, 6, 0.8) # Release

    delay_idx = RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 0, -12.0) # Wet (dB approx)
    RPR.RPR_TrackFX_SetParam(track, delay_idx, 1, 0.25) # Delay length in musical notation (1/4 note)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    total_bars = 12 # Force 12 bars for AAB form
    item_length = (60.0 / bpm) * beats_per_bar * total_bars

    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Progression mapping: 
    # A (Bars 1-4):  IV, V, I, vi  -> Degrees 3, 4, 0, 5
    # A (Bars 5-8):  IV, V, I, vi  -> Degrees 3, 4, 0, 5
    # B (Bars 9-12): IV, V, ii, V  -> Degrees 3, 4, 1, 4 (Diverges in the second half)
    progression_degrees = [3, 4, 0, 5, 3, 4, 0, 5, 3, 4, 1, 4]

    RPR.RPR_MIDI_DisableSort(take)

    for bar_idx, chord_deg in enumerate(progression_degrees):
        bar_start_qn = bar_idx * 4.0

        # 1. Base Chords (Whole notes, Octave 3)
        chord_pitches = [get_pitch(chord_deg, -1), get_pitch(chord_deg + 2, -1), get_pitch(chord_deg + 4, -1)]
        for p in chord_pitches:
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + 4.0)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, p, velocity_base - 20, False)

        # 2. Melody Lines (Octave 5)
        # Identify if we are in Motif A or the expected start of Motif B
        if bar_idx < 10:
            # Standard repeated motif melody: Root -> 3rd -> 5th
            mel_pitches = [get_pitch(chord_deg, 1), get_pitch(chord_deg + 2, 1), get_pitch(chord_deg + 4, 1)]
            timings = [(0.0, 1.5), (1.5, 2.0), (2.0, 3.0)] # (start_beat, end_beat)
            for i, (st, en) in enumerate(timings):
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + st)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + en)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitches[i], velocity_base, False)
        else:
            # The "Surprise": Divergent melody for the end of Motif B
            if bar_idx == 10: # ii chord
                # Faster ascending arpeggio
                mel_pitches = [
                    get_pitch(chord_deg, 0),
                    get_pitch(chord_deg + 2, 0),
                    get_pitch(chord_deg + 4, 0),
                    get_pitch(chord_deg, 1),
                    get_pitch(chord_deg + 2, 1)
                ]
                timings = [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 4.0)]
                for i, (st, en) in enumerate(timings):
                    start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + st)
                    end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + en)
                    RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitches[i], velocity_base + 10, False)
            elif bar_idx == 11: # V chord
                # Powerful resolving long note
                mel_pitch = get_pitch(chord_deg, 1)
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, bar_start_qn + 4.0)
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, mel_pitch, velocity_base + 15, False)

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' featuring a 12-bar AAB 'Rule of 3' Form at {bpm} BPM in {key} {scale}"
```