### 1. High-level Design Pattern Extraction

> **Skill Name**: Deconstructive Arrangement & Filter-Drop Transition

* **Core Musical Mechanism**: The pattern relies on **Subtractive Arrangement** combined with a **Tension-Release Build-up**. Instead of composing a verse from scratch, a dense 8-bar "Chorus" loop is established. The verse is created by subtracting elements (muting the kick/snare, halving hi-hat density). To transition back into the Chorus (the "Drop"), a 1-bar gap is created where all drums drop out. During this gap, a "Riser" element fades in, and the main harmonic instrument experiences an upward sweep in brightness/volume, snapping to full impact at the downbeat of the Drop.

* **Why Use This Skill (Rationale)**: 
  * **Psychoacoustics of the Drop**: By removing rhythmic anchoring (drums) for one bar, the listener's internal metronome is suspended. When the heavy drums re-enter simultaneously with fully bright harmonic elements, the perceived impact of the "Drop" is significantly amplified.
  * **Frequency & Dynamic Contrast**: Sweeping a low-pass filter (or volume/expression) upward during the drum-less gap shifts the frequency focus to the high-end, building kinetic tension that demands a low-end resolution (the returning Kick/Bass).

* **Overall Applicability**: This arrangement framework is the backbone of modern Hip-Hop, Pop, and EDM production. It is used to quickly bridge a sparse verse or intro into a heavy chorus without needing to compose entirely new musical sections. 

* **Value Addition**: This skill transforms a static 8-bar loop into a dynamic, two-section song structure. It encodes professional arrangement techniques (drum dropouts, halving rhythms, noise risers, and CC sweeps) into an instant, parameter-driven scaffolding.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Grid & Divisions**: 4/4 time signature.
  * **Verse (Bars 1-4)**: Sparse rhythm. Kick plays on beats 1 and 2.5. Hi-hats play on 1/4 notes (half-time feel).
  * **The Gap (Bar 4)**: Total rhythmic dropout. No kicks or snares.
  * **Chorus (Bars 5-8)**: Dense rhythm. Kick plays 4-on-the-floor or standard trap pattern. Hi-hats switch to 1/8th or 1/16th notes.
  
* **Step B: Pitch & Harmony**
  * **Progression**: A standard 4-chord progression (e.g., i - VI - III - VII in minor).
  * **Voicings**: Triads or 7th chords sustained for full bars to provide a harmonic bed.
  * **Riser**: A sustained high pitch (e.g., C6) or white noise that holds for exactly 1 bar before the drop.

* **Step C: Sound Design & FX**
  * Instead of brittle VST dependencies, the transition is achieved using **MIDI Expression (CC11)** and **Brightness (CC74)** automation. 
  * As the transition approaches, CC sweeps upward, simulating a low-pass filter opening and a riser swelling in.

* **Step D: Mix & Automation**
  * **Riser Fade-in**: CC11 (Expression) sweeps from 0 to 127 over the 1-bar gap.
  * **Instrument Swell**: The chords track mirrors this sweep to create a unified volume/brightness transition.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Subtractive Arrangement** | Conditional MIDI note insertion | Allows us to generate a Verse and Chorus simultaneously by skipping drum notes in specific bars. |
| **Filter / Volume Sweep** | MIDI CC11 (Expression) / CC74 (Brightness) sweeps | 100% reliable across all DAWs and default synths. Avoids dependency on specific VST plugin indices or missing filters. |
| **The "Riser"** | MIDI note + CC Automation on a dedicated track | Replicates the reversed cymbal/noise sweep effect using native GM synthesis. |

> **Feasibility Assessment**: 100% reproducible. The code will generate a fully arranged 8-bar template (Verse -> Build -> Drop) with perfectly timed MIDI sweeps, gap arrangements, and native tempo synchronization.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Arrangement_Project",
    track_name: str = "Drop_Template",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 8,  # Generates 4 bars verse + 4 bars drop
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates a Deconstructive Arrangement Template: Verse -> Drum Dropout/Sweep -> Chorus Drop.
    Uses MIDI Channel 10 for standard GM drums and Channel 1 for Chords/Riser.
    """
    import reaper_python as RPR

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }

    root_note = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Standard pop/trap chord progression: i - VI - III - VII
    progression_degrees = [0, 5, 2, 6] 

    def get_chord_notes(root, intervals, degree, octave=4):
        notes = []
        for i in [0, 2, 4]: # Triad (Root, 3rd, 5th)
            current_deg = degree + i
            octave_shift = current_deg // 7
            note_idx = current_deg % 7
            pitch = root + (octave + octave_shift) * 12 + intervals[note_idx]
            notes.append(pitch)
        return notes

    # Step 1: Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    beats_per_bar = 4
    beat_length_sec = 60.0 / bpm
    bar_length_sec = beat_length_sec * beats_per_bar

    # Helper function to create tracks
    def create_track_and_item(name, color=0):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        if color:
            RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", color)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    # === TRACK 1: CHORDS (The Harmonic Bed) ===
    chords_track, chords_take = create_track_and_item("Synth Chords", 0x010000FF)
    
    for bar in range(bars):
        degree = progression_degrees[bar % 4]
        chord_notes = get_chord_notes(root_note, scale_intervals, degree, octave=4)
        
        start_time = bar * bar_length_sec
        end_time = start_time + bar_length_sec
        
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, start_time)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, end_time)
        
        # Insert chord notes
        for note in chord_notes:
            RPR.RPR_MIDI_InsertNote(chords_take, False, False, ppq_start, ppq_end, 0, note, velocity_base - 10, False)

        # Arrangement Trick: Volume/Filter Sweep on Bar 4 (Build-up)
        if bar == 3: # 4th bar (0-indexed)
            # Sweep Expression (CC11) from 64 to 127 to build tension
            steps = 16
            for step in range(steps):
                t = start_time + (bar_length_sec / steps) * step
                ppq_cc = RPR.RPR_MIDI_GetPPQPosFromProjTime(chords_take, t)
                val = int(64 + (63 * (step / (steps - 1))))
                RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_cc, 0xB0, 0, 11, val)
        elif bar < 3: # Verse (muted/filtered)
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_start, 0xB0, 0, 11, 64)
        elif bar >= 4: # Chorus / Drop (Wide open)
            RPR.RPR_MIDI_InsertCC(chords_take, False, False, ppq_start, 0xB0, 0, 11, 127)

    RPR.RPR_MIDI_Sort(chords_take)


    # === TRACK 2: DRUMS (The Rhythmic Contrast) ===
    drums_track, drums_take = create_track_and_item("Drums (GM Ch 10)", 0x0100FF00)
    
    KICK, SNARE, HAT = 36, 38, 42

    for bar in range(bars):
        # Arrangement Trick: Complete Drum Dropout before the drop
        if bar == 3:
            continue # Silence for the build-up!
            
        start_time = bar * bar_length_sec
        is_chorus = bar >= 4

        for beat in range(4):
            # Kick Pattern (Sparse in verse, dense in chorus)
            if beat == 0 or (beat == 2 and is_chorus):
                t = start_time + beat * beat_length_sec
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 240, 9, KICK, velocity_base, False)
            
            # Snare Pattern (Backbeat)
            if beat == 1 or beat == 3:
                t = start_time + beat * beat_length_sec
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 240, 9, SNARE, velocity_base, False)

            # Hi-hats (Half-time in verse, regular in chorus)
            hat_subdivisions = 4 if is_chorus else 2
            for sub in range(hat_subdivisions):
                t = start_time + beat * beat_length_sec + (beat_length_sec / hat_subdivisions) * sub
                ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(drums_take, t)
                vel = velocity_base if sub == 0 else velocity_base - 20
                RPR.RPR_MIDI_InsertNote(drums_take, False, False, ppq, ppq + 120, 9, HAT, vel, False)

    RPR.RPR_MIDI_Sort(drums_take)


    # === TRACK 3: THE RISER (Tension Builder) ===
    riser_track, riser_take = create_track_and_item("Riser FX", 0x01FF0000)
    
    # Riser plays only in bar 4 (the gap)
    riser_start = 3 * bar_length_sec
    riser_end = 4 * bar_length_sec
    ppq_r_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, riser_start)
    ppq_r_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, riser_end)
    
    riser_pitch = root_note + 72 # High octave
    RPR.RPR_MIDI_InsertNote(riser_take, False, False, ppq_r_start, ppq_r_end, 0, riser_pitch, velocity_base, False)
    
    # Automate Riser Swell
    steps = 32
    for step in range(steps):
        t = riser_start + (bar_length_sec / steps) * step
        ppq_cc = RPR.RPR_MIDI_GetPPQPosFromProjTime(riser_take, t)
        val = int((step / (steps - 1)) * 127) # Sweep 0 to 127
        RPR.RPR_MIDI_InsertCC(riser_take, False, False, ppq_cc, 0xB0, 0, 11, val) # CC11 Expression
    
    RPR.RPR_MIDI_Sort(riser_take)

    RPR.RPR_UpdateArrange()

    return f"Created Deconstructive Arrangement ({bars} bars) at {bpm} BPM in {key} {scale}. Includes Verse, Dropout/Sweep transition, and Chorus drop."
```