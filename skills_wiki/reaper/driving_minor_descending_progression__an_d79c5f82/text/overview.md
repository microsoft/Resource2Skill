### 1. High-level Design Pattern Extraction

> **Skill Name**: Driving Minor Descending Progression (Andalusian Cadence / Rock Arrangement)

* **Core Musical Mechanism**: A 4-bar descending harmonic progression in a minor key (`i - VII - VI - V`). The defining signature of this pattern is its relentless, driving rhythm section (8th-note chugging bassline and syncopated kick/snare) contrasting with wide, sustained synth chords and a cascading 8th-note lead arpeggio. 

* **Why Use This Skill (Rationale)**: This progression (often associated with the Andalusian Cadence when the V chord is major) relies heavily on the tension and release principle. The major V chord in a minor key (borrowed from the harmonic minor scale) creates a strong leading-tone pull back to the root `i` chord. Musically, the constant 8th notes in the bass create a "motor rhythm" that drives momentum forward, while the syncopated kick drum creates rhythmic interplay against the rigid bass.

* **Overall Applicability**: This pattern is highly applicable to Synthwave, Hard Rock, Metal, and driving cinematic scores. It acts as a perfect "high-energy chorus" or "drop" arrangement.

* **Value Addition**: Compared to a blank project, this skill encodes a full multi-track rock/synthwave arrangement, correctly voicing the descending minor harmony, locking a syncopated drum groove to an 8th-note bassline, and designing basic subtractive synth patches natively inside REAPER.

---

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 BPM. Time signature: 4/4.
  - **Drums**: A syncopated driving groove. Kick on `1`, `2-and`, `3`, `4-and`. Snare on the backbeats (`2` and `4`). Hi-hats on straight 8th notes.
  - **Bass**: Relentless straight 8th notes ("chugging"). Notes are slightly detached (staccato) to create a plucky, driving feel.
  - **Chords**: Whole notes, held for the entire bar.
  - **Lead**: Straight 8th-note arpeggios mapping the intervals of the underlying chord.

* **Step B: Pitch & Harmony**
  - **Key**: B Minor (though parameterized).
  - **Progression**: `i - VII - VI - V` (Major V).
  - **Intervals**:
    - Bar 1 (`i`): Root, minor 3rd, perfect 5th.
    - Bar 2 (`VII`): Major chord starting a whole step below the root.
    - Bar 3 (`VI`): Major chord starting a major third below the root.
    - Bar 4 (`V`): Major chord starting a perfect fourth below the root (harmonic minor substitution).

* **Step C: Sound Design & FX**
  - **Drums**: Mapped to standard General MIDI (GM) values (Kick: 36, Snare: 38, Hat: 42, Crash: 49).
  - **Bass**: `ReaSynth` configured to a plucky sawtooth wave (Saw mix = 1.0, Attack = 0.0, Decay = 0.1).
  - **Chords**: `ReaSynth` configured to a warm pad (Saw/Square mix = 0.5, slow attack = 0.1, high sustain = 0.8).
  - **Lead**: `ReaSynth` configured to a pure square wave pluck (Square mix = 1.0, short decay = 0.1).

* **Step D: Mix & Automation**
  - Basic velocity balancing is baked into the MIDI sequence (e.g., Hi-hats are slightly quieter than Kicks/Snares, the arpeggio has a slight velocity contour to mimic human playing).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Harmonic & Rhythmic Arrangement | MIDI note insertion | Allows exact control of the driving 8th-note grid, chord voicings, and drum syncopation. |
| Track & Item Management | Media Item API | Needed to construct a multi-track looping arrangement across separate elements. |
| Synthesizer Sound Design | FX Chain (`ReaSynth`) | Simulates the distinct tones (plucky bass, wide chords, retro lead) directly using REAPER's native synth without external VST dependencies. |

> **Feasibility Assessment**: 90% reproduction. The code perfectly generates the MIDI and harmonic arrangement as well as basic synth sound design using stock REAPER instruments. The user will only need to route the "Drums" track to their preferred drum sampler (e.g., MT Power Drum Kit or ReaSamplOmatic5000), as REAPER does not have a native acoustic drum kit built-in.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Driving Minor Descending Rock Arrangement in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (default minor).
        bars: Number of bars to generate (will loop the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key.capitalize(), 11) # Default to B
    base_octave = 3
    root_midi = root_val + 12 * base_octave

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # --- Helper Functions ---
    def add_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        return tr

    def add_midi_item(track, beats_length):
        start_time = 0.0
        end_time = beats_length * (60.0 / bpm)
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_time)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", end_time)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def add_note(take, pitch, start_beat, end_beat, vel):
        start_sec = start_beat * (60.0 / bpm)
        end_sec = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # --- Harmony Configuration ---
    # Chords relative to minor key root (Andalusian cadence i-VII-VI-V)
    # V is forced Major for harmonic minor tension/resolution
    progression = [
        [0, 3, 7],     # i   (minor)
        [-2, 2, 5],    # VII (Major)
        [-4, 0, 3],    # VI  (Major)
        [-5, -1, 2]    # V   (Major)
    ]

    total_beats = bars * 4

    # --- DRUMS (General MIDI Mapping) ---
    tr_drums = add_track("Drums (GM Map)")
    take_drums = add_midi_item(tr_drums, total_beats)
    for i in range(bars):
        bar_beat = i * 4
        # Kick: 1, 2-and, 3, 4-and
        add_note(take_drums, 36, bar_beat + 0.0, bar_beat + 0.25, velocity_base)
        add_note(take_drums, 36, bar_beat + 1.5, bar_beat + 1.75, velocity_base - 10)
        add_note(take_drums, 36, bar_beat + 2.0, bar_beat + 2.25, velocity_base)
        add_note(take_drums, 36, bar_beat + 3.5, bar_beat + 3.75, velocity_base - 10)
        
        # Snare: 2, 4
        add_note(take_drums, 38, bar_beat + 1.0, bar_beat + 1.25, velocity_base)
        add_note(take_drums, 38, bar_beat + 3.0, bar_beat + 3.25, velocity_base)
        
        # Hats: Straight 8th notes
        for eighth in range(8):
            hat_vel = velocity_base - 20 if eighth % 2 == 1 else velocity_base - 10
            add_note(take_drums, 42, bar_beat + eighth * 0.5, bar_beat + eighth * 0.5 + 0.25, hat_vel)
            
        # Crash on the 1st beat of alternating bars
        if i % 2 == 0:
            add_note(take_drums, 49, bar_beat + 0.0, bar_beat + 0.5, velocity_base + 10)
            
    RPR.RPR_MIDI_Sort(take_drums)

    # --- BASS (ReaSynth Plucky Saw) ---
    tr_bass = add_track("Bass")
    RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_bass, 0, 2, 0.0) # Square Mix
    RPR.RPR_TrackFX_SetParam(tr_bass, 0, 3, 1.0) # Saw Mix
    RPR.RPR_TrackFX_SetParam(tr_bass, 0, 6, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(tr_bass, 0, 7, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(tr_bass, 0, 8, 0.1) # Sustain
    
    take_bass = add_midi_item(tr_bass, total_beats)
    for i in range(bars):
        chord_idx = i % 4
        root_offset = progression[chord_idx][0]
        bass_pitch = root_midi + root_offset - 12 # Transpose 1 octave down
        bar_beat = i * 4
        
        # Driving 8th notes
        for eighth in range(8):
            # 0.45 beat length leaves a slight gap to create a driving staccato feel
            add_note(take_bass, bass_pitch, bar_beat + eighth * 0.5, bar_beat + eighth * 0.5 + 0.45, velocity_base)
            
    RPR.RPR_MIDI_Sort(take_bass)

    # --- CHORDS (ReaSynth Sustained Pad) ---
    tr_chords = add_track("Rhythm Chords")
    RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, 0, 2, 0.5) # Square Mix
    RPR.RPR_TrackFX_SetParam(tr_chords, 0, 3, 0.5) # Saw Mix
    RPR.RPR_TrackFX_SetParam(tr_chords, 0, 6, 0.1) # Attack (softer)
    RPR.RPR_TrackFX_SetParam(tr_chords, 0, 8, 0.8) # Sustain (held out)
    
    take_chords = add_midi_item(tr_chords, total_beats)
    for i in range(bars):
        chord_idx = i % 4
        chord = progression[chord_idx]
        bar_beat = i * 4
        
        # Whole note chord block
        for interval in chord:
            add_note(take_chords, root_midi + interval, bar_beat, bar_beat + 3.95, velocity_base - 15)
            
    RPR.RPR_MIDI_Sort(take_chords)

    # --- LEAD ARP (ReaSynth Square Pluck) ---
    tr_lead = add_track("Lead Arp")
    RPR.RPR_TrackFX_AddByName(tr_lead, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_lead, 0, 2, 1.0) # Square Mix
    RPR.RPR_TrackFX_SetParam(tr_lead, 0, 3, 0.0) # Saw Mix
    RPR.RPR_TrackFX_SetParam(tr_lead, 0, 6, 0.0) # Attack
    RPR.RPR_TrackFX_SetParam(tr_lead, 0, 7, 0.1) # Decay
    RPR.RPR_TrackFX_SetParam(tr_lead, 0, 8, 0.2) # Sustain
    
    take_lead = add_midi_item(tr_lead, total_beats)
    for i in range(bars):
        chord_idx = i % 4
        chord = progression[chord_idx]
        bar_beat = i * 4
        
        root = chord[0]
        third = chord[1]
        fifth = chord[2]
        
        # Arp pattern repeated twice per bar: [+1 Octave Root, Fifth, Third, Fifth]
        for half in range(2):
            b = bar_beat + half * 2
            add_note(take_lead, root_midi + root + 12, b + 0.0, b + 0.45, velocity_base)
            add_note(take_lead, root_midi + fifth,      b + 0.5, b + 0.95, velocity_base - 5)
            add_note(take_lead, root_midi + third,      b + 1.0, b + 1.45, velocity_base - 10)
            add_note(take_lead, root_midi + fifth,      b + 1.5, b + 1.95, velocity_base - 5)
            
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created multi-track Minor Descending Rock arrangement in {key} {scale} over {bars} bars at {bpm} BPM."
```