# Afro-Cuban Piano Montuno & Tumbao

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Afro-Cuban Piano Montuno & Tumbao

* **Core Musical Mechanism**: The defining signature of Afro-Cuban Latin Jazz piano comping relies on two distinct, interlocking rhythmic layers played simultaneously. The right hand plays a **Montuno**, a 2-bar syncopated pattern of broken chords that heavily emphasizes the offbeats (the "ands" of the beat) outlining a 2-3 Clave. The left hand plays a **Tumbao**, a foundational bass pattern playing the root and fifth, which uniquely *anticipates* chord changes by hitting the root of the *next* measure's chord a full beat early (on beat 4).
* **Why Use This Skill (Rationale)**: This dual-layer pattern creates immense forward momentum and rhythmic tension. The Tumbao's anticipation (beat 4) drags the harmonic progression forward before the downbeat arrives, creating a sense of urgency. The Montuno dances around the main beats, forcing the listener to feel the implicit pulse. By separating the outer chord tones (played in octaves on the beat) and the inner chord tones (played on the syncopated offbeats), it creates a self-contained micro-melody that outlines the harmony without stepping on a soloist's toes.
* **Overall Applicability**: Essential for authentic Latin Jazz, Salsa, Afro-Cuban grooves, and widely applicable to adding Latin flavor to Pop, House, and Electronic dance music (where "Montuno-style" synth plucks are incredibly common). 
* **Value Addition**: This skill moves beyond static block chords, encoding a culturally specific, highly syncopated 2-bar polyrhythm and automated voice-leading/chord-breaking into a single generative action.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Time Signature**: 4/4
  * **BPM**: Usually fast, 140–180 BPM (cut time feel).
  * **Right Hand (Montuno) Rhythm**: Based on 2-3 Son Clave. 
    * Bar 1: `Beat 1.0` (outer), `Beat 2.5` (inner), `Beat 3.5` (outer), `Beat 4.5` (inner)
    * Bar 2: `Beat 1.5` (outer), `Beat 2.5` (inner), `Beat 3.5` (outer), `Beat 4.5` (inner)
  * **Left Hand (Tumbao) Rhythm**: 
    * `Beat 1.0` (Root of current chord)
    * `Beat 2.5` (Fifth of current chord)
    * `Beat 4.0` (Root of the *next* chord - Anticipation)
* **Step B: Pitch & Harmony**
  * Computes a standard 4-bar progression (I - IV - V - I for major, i - iv - V - i for minor).
  * **Montuno Voicing**: Breaks the triad into outer octaves (Root) and inner chord tones (3rd and 5th). 
  * **Tumbao Voicing**: Strictly Root and 5th, pitched in the C2-C3 bass register.
* **Step C: Sound Design & FX**
  * Instrument: ReaSynth configured to sound like a punchy, percussive Electric Piano.
  * Fast attack (0.0s), quick decay (0.3s), zero sustain, short release (0.1s).
  * Sawtooth/Square wave blend to allow the syncopations to cut through a mix.
* **Step D: Mix & Automation**
  * The anticipated beat 4 in the Tumbao bass is given a slight velocity accent to emphasize the harmonic push.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Montuno Syncopation | MIDI note insertion | Requires absolute precision on 8th-note offbeats across a 2-bar cycle. |
| Tumbao Anticipation | MIDI note insertion | Requires programmatic lookahead to inject the *next* measure's root note onto the current measure's beat 4. |
| Percussive Piano Tone | FX chain (ReaSynth) | Uses native REAPER synthesis with zero-sustain ADSR envelopes to emulate the staccato piano/montuno sound without requiring external VSTis or sample libraries. |

> **Feasibility Assessment**: 100% reproducible. The rhythmic offsets, chord voicings, and the interaction between the Tumbao bass and Montuno right hand are mathematically deterministic and perfectly executed via REAPER's MIDI API.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "AfroCuban_Piano",
    bpm: int = 150,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Afro-Cuban Piano Montuno and Tumbao pattern in REAPER.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type ('major' or 'minor').
        bars: Number of bars to generate (should be even for Clave phrasing).
        velocity_base: Base MIDI velocity (0-127).
    
    Returns:
        Status string detailing the operation.
    """
    import reaper_python as RPR

    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Define generic I-IV-V-I progression based on scale
    if scale.lower() == "minor":
        # offsets in semitones, is_major boolean
        # i (min), iv (min), V (maj - harmonic minor), i (min)
        progression = [(0, False), (5, False), (7, True), (0, False)] 
    else:
        # I (maj), IV (maj), V (maj), I (maj)
        progression = [(0, True), (5, True), (7, True), (0, True)]

    # Setup tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Create Track
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Create MIDI Item
    beats_per_bar = 4.0
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    base_root = 48 + NOTE_MAP.get(key.capitalize(), 0) # e.g., C3
    total_notes_added = 0

    # Generate MIDI for each bar
    for bar in range(bars):
        bar_start_qn = bar * beats_per_bar
        
        current_chord = progression[bar % len(progression)]
        next_chord = progression[(bar + 1) % len(progression)]
        
        c_root = base_root + current_chord[0]
        c_third = c_root + (4 if current_chord[1] else 3)
        c_fifth = c_root + 7
        
        n_root = base_root + next_chord[0]

        # -------------------------------------------------------------
        # RIGHT HAND: MONTUNO (2-Bar Pattern)
        # Emphasizing outer root octaves and inner 3rd/5th notes
        # -------------------------------------------------------------
        outer_notes = [c_root + 12, c_root + 24] # e.g., C4, C5
        inner_notes = [c_third + 12, c_fifth + 12] # e.g., E4, G4
        
        # 2-3 Clave Montuno Rhythm phrasing
        if bar % 2 == 0:
            # Bar 1: Hits on beats 1, 2&, 3&, 4&
            montuno_rhythm = [
                (0.0, outer_notes), 
                (1.5, inner_notes), 
                (2.5, outer_notes), 
                (3.5, inner_notes)
            ]
        else:
            # Bar 2: Hits on beats 1&, 2&, 3&, 4&
            montuno_rhythm = [
                (0.5, outer_notes), 
                (1.5, inner_notes), 
                (2.5, outer_notes), 
                (3.5, inner_notes)
            ]

        for beat, notes in montuno_rhythm:
            start_qn = bar_start_qn + beat
            end_qn = start_qn + 0.4 # Staccato/percussive length
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            for pitch in notes:
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base, False)
                total_notes_added += 1

        # -------------------------------------------------------------
        # LEFT HAND: TUMBAO
        # Bass plays 1, 2&, and strongly anticipates the next chord on 4
        # -------------------------------------------------------------
        tumbao_rhythm = [
            (0.0, [c_root - 12], 1.0), # Beat 1 (Root)
            (1.5, [c_fifth - 12], 1.0), # Beat 2& (Fifth)
            (3.0, [n_root - 12], 1.0)   # Beat 4 (Anticipated Next Root)
        ]

        for beat, notes, dur in tumbao_rhythm:
            start_qn = bar_start_qn + beat
            end_qn = start_qn + dur
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)
            
            for pitch in notes:
                # Add a slight velocity accent to the anticipated beat 4 push
                vel = velocity_base + 12 if beat == 3.0 else velocity_base
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), min(127, vel), False)
                total_notes_added += 1

    RPR.RPR_MIDI_Sort(take)

    # Setup ReaSynth to emulate a plucky Electric Piano / Montuno keys sound
    fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth (Cockos)", False, -1)
    if fx_idx >= 0:
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.0)  # Attack (instant)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.3)  # Decay (short)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 2, 0.0)  # Sustain (none)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 3, 0.1)  # Release (quick)
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 4, 0.0)  # Square mix 
        RPR.RPR_TrackFX_SetParam(track, fx_idx, 5, 0.7)  # Saw mix (bit of bite)

    return f"Created '{track_name}' with {total_notes_added} notes over {bars} bars at {bpm} BPM in {key} {scale}."
```