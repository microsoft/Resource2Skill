### 1. High-level Design Pattern Extraction

> **Skill Name**: The "Rule of 3" Compositional Phrase Structure (A-A-B or A-A-A')

* **Core Musical Mechanism**: The "Rule of 3" dictates how many times a musical idea should be repeated before it is altered. You introduce an idea (1st time), reinforce the idea by repeating it identically (2nd time), and then **break the pattern** on the 3rd repetition to maintain listener engagement. The 3rd repetition either goes somewhere completely new, or starts the same but changes the ending.
* **Why Use This Skill (Rationale)**: This rule exploits how the human brain processes information. When a listener hears a phrase once, it piques interest. The second time confirms the pattern and solidifies the hook. However, by the third time, the brain has "solved" the pattern and will actively tune it out if it doesn't change. Altering the 3rd repetition (A-A-B structure) resets the listener's attention span and creates structural momentum.
* **Overall Applicability**: This applies to absolutely every genre of music and every element of production: chord progressions, vocal melodies, drum fills, basslines, and arrangement block structures (e.g., Intro, Verse, Pre-Chorus). 
* **Value Addition**: Instead of a static 4-bar loop that repeats indefinitely (a common amateur mistake), this skill encodes a dynamic 12-bar or 16-bar compositional structure. It automatically creates expectation and subverts it, instantly elevating a static loop into a compelling musical journey.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Grid & Phrasing**: Built on 4-bar phrases. 
  - **Macro-Structure**: 12 bars total. 
    - Bars 1-4: Phrase A (Introduction)
    - Bars 5-8: Phrase A (Reinforcement)
    - Bars 9-12: Phrase B (Variation - starts exactly like A for 2 bars, then diverges for the last 2 bars).
  - **Tempo**: 120 BPM (adjustable).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Major (parameterized).
  - **Progression A (Bars 1-8)**: I - V - vi - IV (degrees 0, 4, 5, 3). A familiar, repeating pop loop.
  - **Progression B (Bars 9-12)**: I - V - ii - V (degrees 0, 4, 1, 4). The progression starts the same but goes to the supertonic (ii) to create a turnaround instead of the expected vi - IV.
  - **Melody**: A diatonic motif is mapped to the chords. It repeats exactly in Phrase 1 and 2, but on Phrase 3, the melody climbs upward on the new chords to create a crescendo of tension.

* **Step C: Sound Design & FX**
  - **Instrument**: Stock `ReaSynth` (two instances: one for chords, one for melody).
  - **FX Chain**: `ReaEQ` (low-pass filtering to tame harsh synth oscillators) and `ReaDelay` to add spatial depth and glue the phrases together.

* **Step D: Mix & Automation**
  - The Chords track is panned slightly left and lowered in volume.
  - The Melody track is panned slightly right. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **A-A-B Phrase Structure** | MIDI note insertion | Requires explicit control over note timings, pitches, and looping logic to physically write the variation in the 3rd phrase. |
| **Harmonic Variation** | Diatonic Math (Scale Degrees) | Allows the variation (the ii-V turnaround) to adapt to any key or scale passed as a parameter. |
| **Audibility/Timbre** | FX chain (ReaSynth + ReaDelay) | Ensures the pattern is immediately listenable and pleasant in a default REAPER session without external VSTs. |

> **Feasibility Assessment**: 100% reproducible. The tutorial teaches a structural composition concept. The code successfully encodes this exact psychological rule into a generated 12-bar MIDI arrangement that physically demonstrates the "start the same, end differently" technique described in the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern_rule_of_3(
    project_name: str = "RuleOf3Project",
    track_name: str = "Rule_of_3",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 12, # Hardcoded internally to 12 to demonstrate the 3 phrases
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 12-bar composition demonstrating the 'Rule of 3' (A-A-B structure).
     Phrase 1 (Bars 1-4): Idea A
     Phrase 2 (Bars 5-8): Idea A
     Phrase 3 (Bars 9-12): Idea B (Starts the same, changes ending)
    """
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
    }

    if scale not in SCALES:
        scale = "major"
    
    root_midi = 36 + NOTE_MAP.get(key.upper(), NOTE_MAP.get(key.capitalize(), 0))
    scale_intervals = SCALES[scale]
    scale_len = len(scale_intervals)

    def get_midi_pitch(degree: int, base_octave: int = 0) -> int:
        """Convert a diatonic scale degree (0-indexed) to a MIDI note."""
        octave_shift = base_octave + (degree // scale_len)
        interval = scale_intervals[degree % scale_len]
        pitch = root_midi + (octave_shift * 12) + interval
        return min(max(pitch, 0), 127)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    beats_per_bar = 4
    PPQ = 960 # standard REAPER PPQ

    # === Step 2: Track Setup ===
    def create_instrument_track(name: str, pan: float, vol: float):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol)
        
        # Add basic Synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        # Add EQ to filter harsh highs
        eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 0) # Band 1 Type (Low Shelf)
        RPR.RPR_TrackFX_SetParam(track, eq_idx, 12, 1) # Band 4 Type (High Pass)
        # Add Delay
        RPR.RPR_TrackFX_AddByName(track, "ReaDelay", False, -1)
        return track

    chords_track = create_instrument_track(f"{track_name}_Chords", -0.2, 0.4)
    melody_track = create_instrument_track(f"{track_name}_Melody", 0.2, 0.7)

    # Calculate times
    total_bars = 12
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * total_bars

    # Create Items
    chords_item = RPR.RPR_AddMediaItemToTrack(chords_track)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(chords_item, "D_LENGTH", total_length_sec)
    chords_take = RPR.RPR_AddTakeToMediaItem(chords_item)

    melody_item = RPR.RPR_AddMediaItemToTrack(melody_track)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(melody_item, "D_LENGTH", total_length_sec)
    melody_take = RPR.RPR_AddTakeToMediaItem(melody_item)

    # === Step 3: Define "Rule of 3" Compositional Data ===
    
    # Chords: Root degrees for 4 bars
    progression_A = [0, 4, 5, 3] # I, V, vi, IV
    progression_B = [0, 4, 1, 4] # I, V, ii, V (Starts same, diverges)

    # Melody A: (scale_degree, start_beat, duration_beats)
    melody_A_bar1 = [(0, 0.0, 1.0), (2, 1.0, 1.0), (4, 2.0, 1.0), (2, 3.0, 1.0)]
    melody_A_bar2 = [(4, 0.0, 2.0), (1, 2.0, 2.0)]
    melody_A_bar3 = [(5, 0.0, 1.5), (7, 1.5, 1.5), (2, 3.0, 1.0)]
    melody_A_bar4 = [(3, 0.0, 4.0)]
    
    phrase_melody_A = [melody_A_bar1, melody_A_bar2, melody_A_bar3, melody_A_bar4]

    # Melody B: First 2 bars same as A. Last 2 bars climb up to build tension
    melody_B_bar3 = [(1, 0.0, 1.0), (3, 1.0, 1.0), (5, 2.0, 1.0), (8, 3.0, 1.0)]
    melody_B_bar4 = [(7, 0.0, 4.0)]
    
    phrase_melody_B = [melody_A_bar1, melody_A_bar2, melody_B_bar3, melody_B_bar4]

    # Structural Master Map
    # Index 0: Phrase 1 (The Introduction)
    # Index 1: Phrase 2 (The Reinforcement)
    # Index 2: Phrase 3 (The Rule of 3 Variation!)
    structure = [
        {"chords": progression_A, "melody": phrase_melody_A},
        {"chords": progression_A, "melody": phrase_melody_A},
        {"chords": progression_B, "melody": phrase_melody_B}
    ]

    # === Step 4: Write MIDI Notes ===
    
    for phrase_idx, phrase in enumerate(structure):
        phrase_start_beat = phrase_idx * 16 # 4 bars * 4 beats
        
        # Write Chords
        for bar_idx, chord_root in enumerate(phrase["chords"]):
            bar_start_beat = phrase_start_beat + (bar_idx * 4)
            start_ppq = int(bar_start_beat * PPQ)
            end_ppq = int((bar_start_beat + 4.0) * PPQ)
            
            # Write a Triad (Root, 3rd, 5th)
            for interval in [0, 2, 4]:
                pitch = get_midi_pitch(chord_root + interval, base_octave=1)
                RPR.RPR_MIDI_InsertNote(chords_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base, False)

        # Write Melody
        for bar_idx, bar_melody in enumerate(phrase["melody"]):
            bar_start_beat = phrase_start_beat + (bar_idx * 4)
            
            for note_degree, note_start, note_dur in bar_melody:
                start_ppq = int((bar_start_beat + note_start) * PPQ)
                end_ppq = int((bar_start_beat + note_start + note_dur) * PPQ)
                
                # Make slightly legato overlap or staccato depending on vibe. Let's do a slight gap
                end_ppq -= int(PPQ * 0.05) 
                
                pitch = get_midi_pitch(note_degree, base_octave=2)
                RPR.RPR_MIDI_InsertNote(melody_take, False, False, start_ppq, end_ppq, 0, pitch, velocity_base + 10, False)

    # Sort MIDI events after insertion (Required API step)
    RPR.RPR_MIDI_Sort(chords_take)
    RPR.RPR_MIDI_Sort(melody_take)
    
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' Rule of 3 pattern: 12 bars (A-A-B structure) at {bpm} BPM in {key} {scale}."
```