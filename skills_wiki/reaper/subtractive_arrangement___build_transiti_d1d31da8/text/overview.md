### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Arrangement & Build Transition

* **Core Musical Mechanism**: This pattern demonstrates how to break out of the "8-bar loop" trap using **subtractive arrangement**. Instead of building up from scratch, you take your densest section (the Chorus) and selectively mute elements to create a Verse. Specifically, this skill drops the kick drum for the first half of the verse, uses a half-time/sparse hi-hat rhythm, completely removes the lead instrument, and glues the sections back together using an automated Riser swell. 

* **Why Use This Skill (Rationale)**: Musically, this creates dynamic contrast through density and absence. By depriving the listener of the driving kick drum and lead melody during the verse, you build anticipation. When those elements slam back in at the chorus, the psychoacoustic impact of the "drop" is vastly amplified. The automated riser acts as a cognitive cue, warning the listener's brain that a high-energy shift is imminent.

* **Overall Applicability**: Essential for beatmakers, hip-hop/trap producers, and EDM artists who struggle with turning loops into full songs. This technique provides an instant structural roadmap.

* **Value Addition**: This skill transforms a static loop into a living arrangement. It encodes knowledge of structural pacing—specifically, the "kick drop-in" halfway through a verse and the transitional riser to bridge low-energy and high-energy sections.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: Typically 120-140 BPM (Hip-Hop/Trap).
  - **Grid**: 4/4 time signature.
  - **Subtractive Rhythm**:
    - *Verse (Bars 1-8)*: Sparse 1/4-note hi-hats. Kick is entirely muted for Bars 1-4, dropping in on Bar 5 to increase momentum. 
    - *Chorus (Bars 9-16)*: Dense 1/8-note hi-hats. Constant, driving kick drum pattern.

* **Step B: Pitch & Harmony**
  - **Progression**: 4-bar loop (e.g., i - VI - III - VII in natural minor).
  - **Arrangement Layers**:
    - *Bass & Chords*: Play consistently through both Verse and Chorus to anchor the harmony.
    - *Lead Melody*: Muted during the Verse, introduced only at the Chorus to maximize melodic impact.

* **Step C: Sound Design & FX**
  - **Placeholder Synths**: ReaSynth is used to block out the arrangement. 
  - **Riser**: A sustained synth note placed exactly two bars before the Chorus.

* **Step D: Mix & Automation**
  - **Volume Swell**: The Riser track has an automation envelope on the Track Volume. It starts at `-inf` dB (amplitude 0.0) two bars before the drop, and swells up to `0 dB` (amplitude 1.0) on a curved trajectory right before the Chorus hits.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Arrangement Blocks | Sequenced MIDI Items over 16 bars | Allows programmatic rendering of Verse vs. Chorus variations |
| Subtractive Drums | Conditional `RPR_MIDI_InsertNote` | Elegantly handles halving hi-hat density and delaying the kick entrance |
| Riser Transition | Track Volume Envelope (`RPR_InsertEnvelopePoint`) | Replicates the smooth, automated build-up shown in the tutorial using native REAPER envelopes |

> **Feasibility Assessment**: 90% - The structural arrangement, MIDI timing variations, and automation build are perfectly reproduced. Because we don't have access to the creator's exact 3rd-party drum samples and VSTs, the script relies on native ReaSynth placeholders. The producer is encouraged to swap these out for their own VSTs.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "SubtractiveArrangement",
    track_name: str = "ArrangementBus",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Length of one section (Verse is 8, Chorus is 8. Total = 16)
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Subtractive Verse into Chorus arrangement with an automated build.
    """
    import reaper_python as RPR

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "major": [0, 2, 4, 5, 7, 9, 11]
    }
    
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Chord progression degrees: i - VI - III - VII
    prog_degrees = [0, 5, 2, 6] 
    
    # Calculate time metrics
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    total_bars = bars * 2  # Verse + Chorus
    
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        trk = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
        return trk

    def create_midi_item(trk, start_t, end_t):
        item = RPR.RPR_CreateNewMIDIItemInProj(trk, start_t, end_t, False)
        return RPR.RPR_GetActiveTake(item)

    def insert_note(take, pitch, start_time, duration, vel):
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time + duration)
        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, int(pitch), int(vel), False)

    # 1. Create Tracks
    trk_drums = add_track(f"{track_name}_Drums")
    trk_bass = add_track(f"{track_name}_Bass")
    trk_chords = add_track(f"{track_name}_Chords")
    trk_lead = add_track(f"{track_name}_Lead")
    trk_riser = add_track(f"{track_name}_Riser")

    # 2. Generate Arrangement Items
    take_drums = create_midi_item(trk_drums, 0, total_bars * bar_sec)
    take_bass = create_midi_item(trk_bass, 0, total_bars * bar_sec)
    take_chords = create_midi_item(trk_chords, 0, total_bars * bar_sec)
    take_lead = create_midi_item(trk_lead, bars * bar_sec, total_bars * bar_sec) # Lead ONLY in Chorus
    
    # 3. Populate MIDI Events (Loop over all bars)
    for bar in range(total_bars):
        b_time = bar * bar_sec
        is_chorus = bar >= bars
        
        # --- DRUMS (Subtractive arrangement logic) ---
        # Kick: Muted in first half of Verse, active everywhere else
        is_kick_active = is_chorus or (bar >= bars / 2)
        if is_kick_active:
            insert_note(take_drums, 36, b_time, beat_sec * 0.5, velocity_base) # Beat 1
            insert_note(take_drums, 36, b_time + (beat_sec * 2.5), beat_sec * 0.5, velocity_base - 10) # Beat 3-and

        # Snare: Standard on 2 and 4
        insert_note(take_drums, 38, b_time + beat_sec, beat_sec * 0.25, velocity_base)
        insert_note(take_drums, 38, b_time + (beat_sec * 3), beat_sec * 0.25, velocity_base)

        # Hi-Hats: Sparse 1/4 notes in Verse, Dense 1/8 notes in Chorus
        hat_steps = 8 if is_chorus else 4
        hat_spacing = (beats_per_bar * beat_sec) / hat_steps
        for h in range(hat_steps):
            vel = velocity_base if h % 2 == 0 else velocity_base - 25
            insert_note(take_drums, 42, b_time + (h * hat_spacing), beat_sec * 0.125, vel)

        # --- BASS & CHORDS ---
        prog_idx = bar % 4
        degree = prog_degrees[prog_idx]
        
        # Get scale notes for the triad
        r_note = root_val + scale_intervals[degree] + 48 # Octave 4
        third = root_val + scale_intervals[(degree + 2) % 7] + 48 + (12 if degree+2 >= 7 else 0)
        fifth = root_val + scale_intervals[(degree + 4) % 7] + 48 + (12 if degree+4 >= 7 else 0)
        
        bass_note = r_note - 24 # Octave 2
        
        # Insert Chords
        insert_note(take_chords, r_note, b_time, bar_sec * 0.95, velocity_base - 20)
        insert_note(take_chords, third, b_time, bar_sec * 0.95, velocity_base - 20)
        insert_note(take_chords, fifth, b_time, bar_sec * 0.95, velocity_base - 20)
        
        # Insert Bass
        insert_note(take_bass, bass_note, b_time, bar_sec * 0.95, velocity_base)

        # --- LEAD (Chorus Only) ---
        if is_chorus:
            # Syncopated rhythmic motif using chord tones
            insert_note(take_lead, r_note + 12, b_time + beat_sec * 0.5, beat_sec * 0.25, velocity_base)
            insert_note(take_lead, third + 12, b_time + beat_sec * 1.5, beat_sec * 0.5, velocity_base)
            insert_note(take_lead, fifth + 12, b_time + beat_sec * 2.75, beat_sec * 0.25, velocity_base)

    # 4. Riser & Automation Build (Transition effect)
    riser_bars = 2
    transition_start = (bars - riser_bars) * bar_sec
    transition_end = bars * bar_sec
    
    take_riser = create_midi_item(trk_riser, transition_start, transition_end)
    insert_note(take_riser, root_val + 60, transition_start, transition_end - transition_start, velocity_base)
    
    # Automate Riser Track Volume to swell up
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env_vol = RPR.RPR_GetTrackEnvelopeByName(trk_riser, "Volume")
    
    if env_vol:
        # Shape 2 represents "Slow start/end" which gives a nice parabolic build
        # value 0.0 = silence, 1.0 = 0dB
        RPR.RPR_InsertEnvelopePoint(env_vol, transition_start, 0.0, 2, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env_vol, transition_end, 1.0, 0, 0, False, True)
        RPR.RPR_Envelope_SortPoints(env_vol)

    RPR.RPR_UpdateArrange()

    return f"Created subtractive arrangement: {bars}-bar Verse into {bars}-bar Chorus at {bpm} BPM with automated transition."
```