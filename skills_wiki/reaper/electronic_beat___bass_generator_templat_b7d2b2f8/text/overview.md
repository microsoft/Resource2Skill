### 1. High-level Design Pattern Extraction

> **Skill Name**: Electronic Beat & Bass Generator Template (Stock Fallback)

* **Core Musical Mechanism**: The video demonstrates the workflow of establishing a foundation for electronic/dance music using generative MIDI drum sequencers (Reason Rack's Beat Map + Kong) and an advanced wavetable bass synthesizer (Massive X) routed through a rhythmic multi-effect (BLENDZ). Because these are proprietary third-party plugins, this skill extracts the *result* of this setup: a driving "four-on-the-floor" electronic beat paired with a syncopated, heavily filtered bassline. 
* **Why Use This Skill (Rationale)**: The interplay between a tight, quantized drum beat and off-beat (syncopated) bass notes creates the foundational "groove" of almost all modern dance music (house, techno, trance). Placing the bass notes exactly on the eighth-note off-beats avoids frequency masking with the kick drum (which hits on the downbeats), naturally creating a pumping, energetic feel.
* **Overall Applicability**: Used as the starting scaffold for electronic music, EDM, house, or synth-pop tracks. It gives the producer an immediate rhythmic foundation to jam over.
* **Value Addition**: Replaces an expensive, third-party VST template with a fully native REAPER equivalent. It automatically generates a structurally sound drum pattern and a matching syncopated bass MIDI item, whilst configuring ReaSynth and JS FX to emulate the tonal character of a wavetable bass patch.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo:** 120 BPM (classic house/techno tempo).
  - **Time Signature:** 4/4.
  - **Drum Rhythm:** Kick on every quarter note (1, 2, 3, 4). Snare on beats 2 and 4. Hi-hats on every eighth note.
  - **Bass Rhythm:** Staccato eighth-notes specifically placed on the "and" of the beats (1.5, 2.5, 3.5, 4.5) to interlock with the kick drum.

* **Step B: Pitch & Harmony**
  - The bassline derives its notes from the selected root key and scale (defaulting to C Minor).
  - It uses the Root (tonic) and occasionally jumps to the minor 3rd or flat 7th for melodic variation.
  - The pitch is transposed down by 2 octaves (MIDI pitches 24-40) to act as a sub/mid-bass.

* **Step C: Sound Design & FX**
  - **Drums**: Standard General MIDI map (Kick=36, Snare=38, Hat=42). Left as raw MIDI so the user can map it to ReaSamplOmatic5000 or their preferred sampler.
  - **Bass**: Emulates the Massive X patch using `ReaSynth` configured for a mix of Sawtooth (bite) and Square (sub-weight) waves.
  - **Rhythmic FX**: Emulates the "BLENDZ" plugin using the stock `JS: Tremolo` effect to give the bass patch a pulsing, moving character, followed by `ReaEQ` cutting high frequencies to keep it dark.

* **Step D: Mix & Automation**
  - The bass track volume is slightly reduced to leave headroom for the kick drum. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Generative Drums | MIDI note insertion | The video relies on Reason's "Beat Map". To reproduce this natively, we algorithmically generate a classic 4/4 drum map using `RPR_MIDI_InsertNote`. |
| Massive X Bass Patch | FX Chain (ReaSynth + JS:Tremolo + ReaEQ) | Massive X is unavailable natively. ReaSynth provides the raw oscillators, while Tremolo and EQ emulate the rhythmic movement and dark filtering seen in the video. |
| Bassline Groove | MIDI note insertion | We calculate exact PPQ (Pulses Per Quarter Note) positions to place the bass notes securely on the off-beats, creating an interlocking groove. |

> **Feasibility Assessment**: 80%. We cannot perfectly recreate the specific wavetable characteristics of the "Stuck Duck" Massive X preset or the algorithmic unpredictability of Reason Beat Map without those plugins. However, we successfully reproduce the *musical function*—the tight rhythmic interplay and low-end tonal scaffolding—using 100% stock REAPER actions.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Electronic Groove",
    track_name: str = "Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an Electronic Drum & Bass foundation natively in REAPER, 
    mimicking a third-party generative drum and wavetable bass workflow.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

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

    # Extract scale intervals and root note
    root_pitch = NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    
    # Calculate absolute timings
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_len_sec = 60.0 / bpm
    bar_length_sec = beat_len_sec * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # Helper function to insert MIDI notes accurately via PPQ
    def insert_midi(take, start_sec, end_sec, pitch, velocity):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), False)

    # === TRACK 1: GENERATIVE DRUMS EQUIVALENT ===
    drum_track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(drum_track_idx, True)
    drum_track = RPR.RPR_GetTrack(0, drum_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(drum_track, "P_NAME", f"{track_name} - Drums (MIDI)", True)

    drum_item = RPR.RPR_AddMediaItemToTrack(drum_track)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(drum_item, "D_LENGTH", total_length_sec)
    drum_take = RPR.RPR_AddTakeToMediaItem(drum_item)
    
    # GM Drum Mapping
    kick_note = 36
    snare_note = 38
    hat_note = 42

    for bar in range(bars):
        bar_offset = bar * bar_length_sec
        for beat in range(beats_per_bar):
            beat_start = bar_offset + (beat * beat_len_sec)
            
            # Kick on every quarter note (1, 2, 3, 4)
            insert_midi(drum_take, beat_start, beat_start + (beat_len_sec * 0.5), kick_note, velocity_base)
            
            # Snare on beats 2 and 4 (index 1 and 3)
            if beat % 2 != 0:
                insert_midi(drum_take, beat_start, beat_start + (beat_len_sec * 0.5), snare_note, velocity_base)
                
            # Hi-hats on every eighth note
            insert_midi(drum_take, beat_start, beat_start + (beat_len_sec * 0.25), hat_note, int(velocity_base * 0.7)) # Downbeat hat
            offbeat_start = beat_start + (beat_len_sec * 0.5)
            insert_midi(drum_take, offbeat_start, offbeat_start + (beat_len_sec * 0.25), hat_note, int(velocity_base * 0.9)) # Offbeat hat (accent)

    RPR.RPR_MIDI_Sort(drum_take)


    # === TRACK 2: BASS SYNTH EQUIVALENT ===
    bass_track_idx = drum_track_idx + 1
    RPR.RPR_InsertTrackAtIndex(bass_track_idx, True)
    bass_track = RPR.RPR_GetTrack(0, bass_track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(bass_track, "P_NAME", f"{track_name} - Bass (ReaSynth)", True)
    RPR.RPR_SetMediaTrackInfo_Value(bass_track, "D_VOL", 0.7) # Turn down slightly to sit under kick

    # Add FX Chain to mimic Massive X + BLENDZ
    synth_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    tremolo_fx = RPR.RPR_TrackFX_AddByName(bass_track, "JS: Tremolo", False, -1)
    eq_fx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaEQ", False, -1)

    # Configure ReaSynth for a "stuck" subby/buzzy bass (Saw + Square)
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 0, 0.0) # Volume (0dB base)
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 1, 0.5) # Tuning (center)
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 2, 0.8) # Sawtooth blend
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 3, 0.6) # Square blend
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 5, 0.05) # Fast attack
    RPR.RPR_TrackFX_SetParam(bass_track, synth_fx, 6, 0.2) # Fast decay for staccato feel

    # Configure JS Tremolo for rhythmic pumping
    RPR.RPR_TrackFX_SetParam(bass_track, tremolo_fx, 0, 4.0) # Frequency (Hz, sync approx to beat)
    RPR.RPR_TrackFX_SetParam(bass_track, tremolo_fx, 1, 60.0) # Amount (Depth)

    # Configure ReaEQ to cut harsh highs (Lowpass filter style)
    RPR.RPR_TrackFX_SetParam(bass_track, eq_fx, 0, 3) # Band 1 Type: High Cut
    RPR.RPR_TrackFX_SetParam(bass_track, eq_fx, 1, 800) # Cutoff frequency (Hz)
    
    # Create Bass MIDI Item
    bass_item = RPR.RPR_AddMediaItemToTrack(bass_track)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(bass_item, "D_LENGTH", total_length_sec)
    bass_take = RPR.RPR_AddTakeToMediaItem(bass_item)

    bass_octave_base = 24 # C1 = 24
    
    for bar in range(bars):
        bar_offset = bar * bar_length_sec
        for beat in range(beats_per_bar):
            # Syncopation: Bass notes land strictly on the off-beats (the "and" of the beat)
            offbeat_start = bar_offset + (beat * beat_len_sec) + (beat_len_sec * 0.5)
            note_len = beat_len_sec * 0.4 # Slightly staccato
            
            # Use root note, but add a passing minor 3rd/flat 7th at the end of every other bar
            note_degree = 0
            if beat == 3 and bar % 2 != 0:
                note_degree = 2 # Usually the 3rd degree in the scale array
                if len(scale_intervals) > 2:
                    note_pitch = bass_octave_base + root_pitch + scale_intervals[note_degree]
                else:
                    note_pitch = bass_octave_base + root_pitch + 3 # Fallback minor 3rd
            else:
                note_pitch = bass_octave_base + root_pitch
                
            insert_midi(bass_take, offbeat_start, offbeat_start + note_len, note_pitch, velocity_base)

    RPR.RPR_MIDI_Sort(bass_take)

    return f"Created native Electronic Groove scaffold (Drums & Bass) over {bars} bars at {bpm} BPM."
```