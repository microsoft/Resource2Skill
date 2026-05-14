### 1. High-level Design Pattern Extraction

> **Skill Name**: Subtractive Arrangement & Transitional Dropouts

* **Core Musical Mechanism**: This skill demonstrates how to derive song structure from a single loop using **subtraction** and **temporal contrast**, punctuated by a **pre-chorus vacuum** (dropout). Rather than writing completely new parts for the verse, the verse is created by removing elements (the lead melody), halving the rhythmic density (half-time hi-hats), and selectively omitting the downbeat kick. The transition is then forced via a hard drum mute and a swelling noise riser.
* **Why Use This Skill (Rationale)**: Music relies on tension and release. A loop playing endlessly causes listener fatigue. By employing subtractive arrangement ("deleting things is adding things"), you create dynamic contrast. The drum dropout right before the chorus functions as a "psychoacoustic vacuum"—by momentarily removing low-end and rhythmic energy, the subsequent downbeat of the chorus feels dramatically heavier and wider.
* **Overall Applicability**: Essential for hip-hop beatmaking, trap, EDM, and modern pop. It’s the foundational technique for turning an 8-bar "beat block" into a fully structured Verse/Chorus song format.
* **Value Addition**: Encodes professional arrangement workflow into code. It prevents the "stuck in the loop" phase by automatically generating structured variation, utilizing half-time feel shifts, and inserting automated transitional risers without relying on external audio samples.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120-150 BPM (Defaulting to 130 BPM).
  - **Verse vs. Chorus Rhythm**: The hi-hats play 8th notes in the Verse (half-time feel) and 16th notes in the Chorus. 
  - **Subtraction**: The very first kick drum of the verse is omitted to ease the listener in.
  - **Dropout**: On the last bar of the verse, all drums (Kick, Snare, Hats) are muted starting on Beat 3, creating a silent gap before the drop.

* **Step B: Pitch & Harmony**
  - **Progression**: Follows a classic 1-6-4-5 structural progression (e.g., i - VI - iv - v in minor), standard for dramatic modern beats. 
  - **Voicing**: Triads are tightly voiced around a central octave, computing dynamically to fit any requested key and scale.
  - **Lead Motif**: A sparse, repetitive arpeggio that only activates during the Chorus to distinguish the sections.

* **Step C: Sound Design & FX**
  - Synthesized using REAPER's native `ReaSynth`.
  - **Kick**: Low-pitched sine wave with a fast release.
  - **Snare/Hats**: Fast bursts of white noise.
  - **Riser**: A specialized ReaSynth noise patch that swells over the transition bar.

* **Step D: Mix & Automation**
  - Track volumes are pre-balanced to prevent clipping.
  - **Riser Automation**: A track volume envelope is created and automated to sweep from `-inf` to `0dB` during the dropout bar, instantly dropping back down to silence precisely on the Chorus downbeat.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Subtractive Structure** | MIDI note insertion logic | Precise programmatic control to omit specific beats and alter note resolution (1/8 vs 1/16) per section. |
| **Transitional Riser** | Track Volume Envelope Automation | Replicates the "filter sweep/riser" effect fluidly using stock API tools, ensuring the swell builds perfectly to the grid. |
| **Drums & Synths** | `ReaSynth` parameterized FX chains | Generates snappy, tunable drum transients and melodic tones natively without relying on missing external sample files. |

> **Feasibility Assessment**: 100% reproducible within the constraints of native REAPER tools. The script fully generates a dynamic, multi-track Verse-to-Chorus arrangement, simulating the beatmaker's structural workflow entirely through ReaScript.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Arranged_Beat",
    bpm: int = 130,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a dynamic Verse-to-Chorus arrangement using subtractive 
    techniques, half-time rhythm shifts, and a transition riser.
    """
    import reaper_python as RPR

    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
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

    base_note = 48 + NOTE_MAP.get(key, 0) # C3
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    def get_scale_degree_pitch(degree_0_indexed):
        octave = degree_0_indexed // len(scale_intervals)
        idx = degree_0_indexed % len(scale_intervals)
        return base_note + (octave * 12) + scale_intervals[idx]

    beats_per_bar = 4
    beat_len = 60.0 / bpm
    
    # Split the arrangement structurally
    verse_bars = max(2, bars // 2)
    
    def add_track(name, vol=1.0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", f"{track_name}_{name}", True)
        RPR.RPR_SetMediaTrackInfo_Value(tr, "D_VOL", vol)
        return tr

    def insert_midi(track, start_beat, end_beat, notes):
        if not notes: return None
        start_time = start_beat * beat_len
        end_time = end_beat * beat_len
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", end_time - start_time)
        take = RPR.RPR_AddTakeToMediaItem(item)

        RPR.RPR_MIDI_DisableSort(take)
        for note in notes:
            b_pos, b_len, pitch, vel = note
            n_start = start_time + (b_pos - start_beat) * beat_len
            n_end = n_start + b_len * beat_len
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_start)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, n_end)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)
        RPR.RPR_MIDI_Sort(take)
        return item

    # Create Tracks
    chords_tr = add_track("Chords", 0.4)
    lead_tr = add_track("Lead", 0.5)
    kick_tr = add_track("Kick", 0.9)
    snare_tr = add_track("Snare", 0.7)
    hat_tr = add_track("HiHat", 0.4)
    riser_tr = add_track("Riser", 0.8)

    # Instrument FX Chains
    RPR.RPR_TrackFX_AddByName(chords_tr, "ReaSynth", False, -1)
    
    RPR.RPR_TrackFX_AddByName(lead_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(lead_tr, 0, 1, 1.0) # Square wave
    
    RPR.RPR_TrackFX_AddByName(kick_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(kick_tr, 0, 4, 0.1) # Fast release for thump
    
    RPR.RPR_TrackFX_AddByName(snare_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_tr, 0, 0, 0.0) # No Osc
    RPR.RPR_TrackFX_SetParam(snare_tr, 0, 5, 1.0) # Full Noise
    RPR.RPR_TrackFX_SetParam(snare_tr, 0, 4, 0.15) # Snare decay
    
    RPR.RPR_TrackFX_AddByName(hat_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(hat_tr, 0, 0, 0.0) 
    RPR.RPR_TrackFX_SetParam(hat_tr, 0, 5, 1.0)
    RPR.RPR_TrackFX_SetParam(hat_tr, 0, 4, 0.03) # Super fast hat decay
    
    RPR.RPR_TrackFX_AddByName(riser_tr, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(riser_tr, 0, 0, 0.2) 
    RPR.RPR_TrackFX_SetParam(riser_tr, 0, 5, 1.0) # Noise sweep
    RPR.RPR_TrackFX_SetParam(riser_tr, 0, 3, 0.5) # Slow attack

    # Generate Note Data
    c_notes, l_notes, k_notes, s_notes, h_notes = [], [], [], [], []
    
    # Standard pop/trap progression (1, 6, 4, 5)
    progression = [0, 5, 3, 4]

    for bar in range(bars):
        is_verse = bar < verse_bars
        is_transition = bar == verse_bars - 1
        b_start = bar * beats_per_bar
        
        # 1. Chords (Plays constantly to hold structure)
        deg = progression[bar % len(progression)]
        r_p = get_scale_degree_pitch(deg)
        t_p = get_scale_degree_pitch(deg + 2)
        f_p = get_scale_degree_pitch(deg + 4)
        # Tight voicings
        if t_p > base_note + 12: t_p -= 12
        if f_p > base_note + 12: f_p -= 12
        
        c_notes.append((b_start, 4.0, r_p, velocity_base - 10))
        c_notes.append((b_start, 4.0, t_p, velocity_base - 10))
        c_notes.append((b_start, 4.0, f_p, velocity_base - 10))

        # 2. Lead (Subtraction: Only in Chorus)
        if not is_verse:
            lr_p = r_p + 12
            lt_p = t_p + 12
            l_notes.append((b_start, 1.5, lr_p, velocity_base))
            l_notes.append((b_start + 1.5, 0.5, lt_p, velocity_base))
            l_notes.append((b_start + 2.0, 1.0, lr_p, velocity_base))

        # 3. Kick (Subtraction: Drop first kick of verse & transition dropout)
        if bar == 0:
            kicks = [2.5, 3.5]
        elif is_transition:
            kicks = [0]
        else:
            kicks = [0, 2.5, 3.5]
            
        for k in kicks:
            k_notes.append((b_start + k, 0.5, 24, velocity_base + 15))

        # 4. Snare (Transition dropout)
        snares = [1] if is_transition else [1, 3]
        for s in snares:
            s_notes.append((b_start + s, 0.5, 60, velocity_base))

        # 5. Hats (Temporal Contrast: Half-time verse, 16ths chorus)
        step = 0.5 if is_verse else 0.25
        num_steps = int(4 / step)
        for i in range(num_steps):
            pos = i * step
            if is_transition and pos >= 2.0: # Stop hats at dropout
                continue
            vel = velocity_base if i % 2 == 0 else velocity_base - 25
            h_notes.append((b_start + pos, 0.1, 60, vel))

    # Insert MIDI for main tracks
    insert_midi(chords_tr, 0, bars * beats_per_bar, c_notes)
    insert_midi(lead_tr, 0, bars * beats_per_bar, l_notes)
    insert_midi(kick_tr, 0, bars * beats_per_bar, k_notes)
    insert_midi(snare_tr, 0, bars * beats_per_bar, s_notes)
    insert_midi(hat_tr, 0, bars * beats_per_bar, h_notes)

    # 6. Riser Automation (Swells during the transition bar)
    trans_bar = verse_bars - 1
    r_notes = [(trans_bar * beats_per_bar, 4.0, 60, velocity_base)]
    insert_midi(riser_tr, 0, bars * beats_per_bar, r_notes)

    # Toggle Volume Envelope visibility to ensure it exists, then write to it
    RPR.RPR_SetOnlyTrackSelected(riser_tr)
    RPR.RPR_Main_OnCommand(40406, 0) # Track: Toggle track volume envelope visible
    env = RPR.RPR_GetTrackEnvelopeByName(riser_tr, "Volume")
    
    if env:
        start_t = trans_bar * beats_per_bar * beat_len
        end_t = (trans_bar + 1) * beats_per_bar * beat_len
        
        # Sweep from -inf (0.0) up to 0dB (1.0), then hard mute on the drop
        RPR.RPR_InsertEnvelopePoint(env, start_t, 0.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, end_t, 1.0, 0, 0, False, True)
        RPR.RPR_InsertEnvelopePoint(env, end_t + 0.01, 0.0, 0, 0, False, True)
        RPR.RPR_Envelope_Sort(env)

    return f"Created subractive '{track_name}' arrangement ({verse_bars} bars Verse -> {bars - verse_bars} bars Chorus) at {bpm} BPM in {key} {scale}."
```