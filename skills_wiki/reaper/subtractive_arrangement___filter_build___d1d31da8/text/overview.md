### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Arrangement & Filter Build (The "Beat Drop" Transition)

* **Core Musical Mechanism**: The tutorial demonstrates how to transform a dense, repetitive 8-bar loop (the "Chorus") into a full song structure using **subtractive arrangement** and **tension-building automation**. The core mechanism involves stripping away foundational energy (muting the kick and bass) and halving the rhythmic momentum (halftime hi-hats) to create a "Verse". Tension is then injected back into the arrangement using a low-pass filter sweep (muffling the harmony) and a synthesized, reverb-washed riser, culminating in a sudden release of energy (the "Drop") back into the Chorus.

* **Why Use This Skill (Rationale)**: This relies on the psychological principle of dynamic contrast. Continuous dense loops cause listener fatigue. By removing the low-end frequencies and slowing the perceived subdivision (halftime hats), you give a vocalist/rapper acoustic space. Reintroducing the kick provides a mid-verse bounce. Finally, muffling the high frequencies via a filter sweep pushes the harmonic elements into the psychoacoustic "background"; when the filter snaps open at the drop, it creates a massive sense of width, brightness, and release.

* **Overall Applicability**: Essential for Hip-Hop, Trap, Pop, and EDM. This is the definitive workflow for escaping the "8-bar loop trap" and structuring a full track that keeps listeners engaged.

* **Value Addition**: Compared to a static loop, this skill encodes professional macro-arrangement techniques (ABA structuring), dynamic momentum control (subdivision manipulation), and mix-based tension (filter and riser automation).


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo/Signature**: ~140 BPM, 4/4 Trap/Hip-hop feel.
  - **Chorus**: Kick on beats 1, 2.5, 3.5. Snare on 3. Hats playing steady 1/8th notes.
  - **Verse 1A (Energy Drop)**: Kick is muted. Hats are slowed down to 1/4 notes (halftime).
  - **Verse 1B (The Build)**: Kick returns. Hats return to 1/8th notes. Riser occupies the final bar.

* **Step B: Pitch & Harmony**
  - **Progression**: Algorithmic dynamic progression (e.g., i - VI - iv - v).
  - **Bass**: Root notes mirroring the chord progression, completely muted during the first half of the verse.
  - **Chords**: Sustained triads providing the harmonic bed, subjected to heavy filtering during the transition.

* **Step C: Sound Design & FX**
  - **Instruments**: Uses REAPER's native `ReaSynth` to synthesize foundational placeholders for Kick, Snare, Hats, Bass, Chords, and the Riser.
  - **Riser FX**: A synthesized pitch-bending oscillator fed into `ReaVerbate` with high wetness to create a "wash out" effect. 
  - **Chorus/Chords FX**: `ReaEQ` is applied to the harmonic bed to control frequency presence over time.

* **Step D: Mix & Automation**
  - **Filter Sweep**: `ReaEQ` Band 4 (High Shelf) gain is automated on the Chords track. It drops to -20dB during the "Build" section to create a muffled, underwater sound, then snaps back to 0dB exactly on the drop.
  - **Riser Automation**: The Riser track automates ReaSynth's Tuning (pitch bend) and Volume (fade in) over a 1-bar duration to swell into the transition.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Subtractive Arrangement** | MIDI note insertion | Allows us to algorithmically conditionally skip the Kick, Bass, and half the Hi-hats during specific bars. |
| **Harmony Generation** | Scale-degree math | Computes correct I-VI-IV-V triads entirely from the parameterized `key` and `scale`. |
| **Filter Build** | FX Envelope Automation (`ReaEQ`) | Precisely replicates the tutorial's muffled "High Cut" EQ transition by automating High Shelf Gain. |
| **Synthesized Riser** | `ReaSynth` + `ReaVerbate` + Automation | Replaces the need for external samples by synthesizing a pitch-sweeping, volume-fading noise wash directly inside REAPER. |

> **Feasibility Assessment**: 100% reproducible for the *arrangement and automation structure*. Because we cannot use the producer's third-party sound libraries or downloaded riser samples, we use `ReaSynth` to generate clear, distinct placeholders (low sine for kick, high short tick for hats, pitch-swept tone for the riser) demonstrating the exact structural logic shown in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Arrangement_Tutorial",
    track_name: str = "Beat_Structure",
    bpm: int = 140,
    key: str = "C",
    scale: str = "minor",
    bars: int = 16, # 4-bar Chorus, 8-bar Verse/Build, 4-bar Chorus
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a full 16-bar Subtractive Arrangement & Drop Builder in REAPER.
    Demonstrates muting elements, halftime drum momentum, and a filter/riser transition.
    """
    import reaper_python as RPR

    # Set Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # Theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_midi = 48 + NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])

    def get_pitch(degree_idx):
        """Convert a 0-indexed scale degree into a MIDI pitch."""
        octave = degree_idx // 7
        idx = degree_idx % 7
        return root_midi + (octave * 12) + scale_intervals[idx]

    def add_track_with_synth(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", f"{track_name}_{name}", True)
        fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        return track, fx_idx

    def create_take(track, length_sec):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def insert_note(take, start_time, end_time, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Setup Timing
    beats_per_bar = 4
    sec_per_beat = 60.0 / bpm
    sec_per_bar = sec_per_beat * beats_per_bar
    total_sec = sec_per_bar * bars

    # Create Tracks
    kick_tr, _ = add_track_with_synth("Kick")
    snare_tr, _ = add_track_with_synth("Snare")
    hats_tr, _ = add_track_with_synth("Hats")
    bass_tr, _ = add_track_with_synth("Bass")
    chords_tr, _ = add_track_with_synth("Chords")
    riser_tr, riser_fx = add_track_with_synth("Riser")

    # Add Reverb to Riser to wash it out
    RPR.RPR_TrackFX_AddByName(riser_tr, "ReaVerbate", False, -1)

    # Create Takes
    kick_take = create_take(kick_tr, total_sec)
    snare_take = create_take(snare_tr, total_sec)
    hats_take = create_take(hats_tr, total_sec)
    bass_take = create_take(bass_tr, total_sec)
    chords_take = create_take(chords_tr, total_sec)
    riser_take = create_take(riser_tr, total_sec)

    # Arrangement Generation Loop (16 Bars)
    prog_degrees = [0, 5, 3, 4] # i - VI - iv - v progression

    for bar in range(bars):
        bar_start = bar * sec_per_bar
        
        # Arrangement Logic
        is_chorus = (bar < 4) or (bar >= 12)
        is_verse_a = (4 <= bar < 8)
        is_verse_build = (8 <= bar < 12)
        
        # Harmony Calculation
        chord_deg = prog_degrees[bar % 4]
        root_note = get_pitch(chord_deg)
        third_note = get_pitch(chord_deg + 2)
        fifth_note = get_pitch(chord_deg + 4)

        # 1. KICK (Muted in Verse A)
        if is_chorus or is_verse_build:
            for b in [0.0, 1.5, 2.5]: # Trap syncopation
                pos = bar_start + b * sec_per_beat
                insert_note(kick_take, pos, pos + 0.1, 36, velocity_base)

        # 2. SNARE (Plays throughout)
        snare_pos = bar_start + 2.0 * sec_per_beat
        insert_note(snare_take, snare_pos, snare_pos + 0.1, 60, velocity_base)

        # 3. HI-HATS (Halftime in Verse A)
        hat_step = 1.0 if is_verse_a else 0.5
        hat_beats = [i * hat_step for i in range(int(4 / hat_step))]
        for b in hat_beats:
            pos = bar_start + b * sec_per_beat
            insert_note(hats_take, pos, pos + 0.05, 84, velocity_base - 20)

        # 4. BASS (Muted in Verse A)
        if is_chorus or is_verse_build:
            insert_note(bass_take, bar_start, bar_start + sec_per_bar, root_note - 12, velocity_base)

        # 5. CHORDS (Plays throughout, automated later)
        insert_note(chords_take, bar_start, bar_start + sec_per_bar, root_note, velocity_base - 30)
        insert_note(chords_take, bar_start, bar_start + sec_per_bar, third_note, velocity_base - 30)
        insert_note(chords_take, bar_start, bar_start + sec_per_bar, fifth_note, velocity_base - 30)

        # 6. RISER (Plays only in Bar 12, the final bar of the build)
        if bar == 11:
            insert_note(riser_take, bar_start, bar_start + sec_per_bar, 60, velocity_base)

    # Sort MIDI events
    for take in [kick_take, snare_take, hats_take, bass_take, chords_take, riser_take]:
        RPR.RPR_MIDI_Sort(take)

    # ==========================================
    # AUTOMATION 1: Chords Filter Muffle (ReaEQ)
    # ==========================================
    chords_eq_idx = RPR.RPR_TrackFX_AddByName(chords_tr, "ReaEQ", False, -1)
    # Param 10 in ReaEQ is Band 4 (High Shelf) Gain. 
    # 0.5 = 0dB. 0.0 = max attenuation (muffled).
    chords_env = RPR.RPR_GetFXEnvelope(chords_tr, chords_eq_idx, 10, True)
    
    t_bar9 = 8 * sec_per_bar
    t_bar12_end = 12 * sec_per_bar

    # Envelope shape: Linear (0)
    RPR.RPR_InsertEnvelopePoint(chords_env, 0.0, 0.5, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(chords_env, t_bar9, 0.5, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(chords_env, t_bar9 + sec_per_beat, 0.1, 0, 0, False, True) # Muffle drops in!
    RPR.RPR_InsertEnvelopePoint(chords_env, t_bar12_end - sec_per_beat, 0.1, 0, 0, False, True) # Hold muffle...
    RPR.RPR_InsertEnvelopePoint(chords_env, t_bar12_end, 0.5, 0, 0, False, True) # Snap back to normal for the drop
    RPR.RPR_Envelope_Sort(chords_env)

    # ==========================================
    # AUTOMATION 2: Riser Build (ReaSynth)
    # ==========================================
    # Automate Volume (Param 0) to swell in
    riser_vol_env = RPR.RPR_GetFXEnvelope(riser_tr, riser_fx, 0, True)
    t_bar12_start = 11 * sec_per_bar
    
    RPR.RPR_InsertEnvelopePoint(riser_vol_env, 0.0, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(riser_vol_env, t_bar12_start, 0.0, 0, 0, False, True)
    RPR.RPR_InsertEnvelopePoint(riser_vol_env, t_bar12_end, 0.8, 0, 0, False, True) # Fade in
    RPR.RPR_InsertEnvelopePoint(riser_vol_env, t_bar12_end + 0.1, 0.0, 0, 0, False, True) # Cut off at drop
    RPR.RPR_Envelope_Sort(riser_vol_env)

    # Automate Tuning/Pitch (Param 1) to rise up
    riser_pitch_env = RPR.RPR_GetFXEnvelope(riser_tr, riser_fx, 1, True)
    RPR.RPR_InsertEnvelopePoint(riser_pitch_env, t_bar12_start, 0.5, 0, 0, False, True) # Center pitch
    RPR.RPR_InsertEnvelopePoint(riser_pitch_env, t_bar12_end, 0.8, 0, 0, False, True) # Pitch bends up
    RPR.RPR_Envelope_Sort(riser_pitch_env)

    return f"Created subtractive arrangement template '{track_name}' (16 bars) in {key} {scale} at {bpm} BPM with automated filter drop."
```