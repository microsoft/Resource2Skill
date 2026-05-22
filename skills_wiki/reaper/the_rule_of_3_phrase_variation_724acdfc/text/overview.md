# The "Rule of 3" Phrase Variation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: The "Rule of 3" Phrase Variation

* **Core Musical Mechanism**: The strategic limitation of literal repetition. When establishing a musical idea (a melody, chord progression, or drum groove), it is played exactly twice to establish familiarity. On the third iteration, the pattern diverges—either by introducing a completely new idea (A-A-B) or by starting the same but changing the ending (A-A-A'). 

* **Why Use This Skill (Rationale)**: This technique directly exploits how the human brain processes auditory information. As explained in the tutorial:
  - **1st Listen**: The brain hears a novel idea and is intrigued.
  - **2nd Listen**: The brain recognizes the pattern, reinforcing the idea and establishing a "hook" or groove.
  - **3rd Listen**: The brain fully predicts the outcome. If the pattern repeats exactly again, the listener's brain "tunes it out" and loses interest. By introducing a variation precisely at this moment of expected predictability, you re-capture the listener's attention, build tension, and propel the arrangement forward.

* **Overall Applicability**: This is a foundational composition and arrangement tool applicable to almost every genre. It is most commonly used for chord progressions in pop/EDM, vocal phrasing in songwriting, drop structures in electronic music, and drum fill placements (repeating a 1-bar drum loop twice, then adding a fill on the 3rd or 4th bar).

* **Value Addition**: Compared to a looped 4-bar MIDI clip, this skill encodes macro-arrangement structure. It transforms a static loop into a dynamic 12-bar section that naturally breathes, builds anticipation, and transitions smoothly into the next part of a song.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4 (Standard)
  - **Phrase Length**: The core idea is 4 bars long. To execute the Rule of 3, the total generated section is 12 bars (4 bars × 3 iterations).
  - **Rhythm**: Sustained chords with a simple, rhythmic top-line melody to clearly highlight the repetition and the eventual deviation.

* **Step B: Pitch & Harmony**
  - **Iterations 1 & 2 (Bars 1-8)**: A standard, familiar diatonic chord progression (e.g., I - V - vi - IV).
  - **Iteration 3 (Bars 9-12)**: The "Go Somewhere Different" option. The first two bars of this iteration (Bars 9-10) mirror the original progression (I - V), tricking the listener into expecting the usual loop. The final two bars (Bars 11-12) deviate to a turnaround progression (e.g., ii - V) to create tension leading into the next section.
  - **Voicings**: Diatonic 7th chords to provide harmonic richness.

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured to sound like a soft electric piano or pad (slower attack, moderate release, saw/square blend).
  - **FX Chain**: `ReaEQ` cutting harsh highs (lowpass filter) to simulate a darker, warmer tone that fits well as a foundational progression.

* **Step D: Mix & Automation**
  - Moderate volume levels. No complex automation needed, as the variation itself provides the dynamic movement.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **A-A-A' Structure** | MIDI note insertion | Allows programmatic control over musical phrases, looping the first two blocks and injecting diatonic variation into the third block. |
| **Diatonic Harmony** | Programmatic degree mapping | Computes exact MIDI notes dynamically based on the user's chosen key and scale, rather than relying on hardcoded C-major notes. |
| **Sound Design** | Track FX (`ReaSynth` + `ReaEQ`) | Provides an immediate, listenable electric piano/pad tone without relying on external 3rd-party VSTs. |

> **Feasibility Assessment**: 100%. The script fully reproduces the compositional concept demonstrated in the tutorial. It generates the A-A-A' structure with diatonic chords and a top-line melody, fully demonstrating the "Rule of 3".

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Rule Of 3 Progression",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,  # Length of the core phrase (Total length will be bars * 3)
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a 'Rule of 3' compositional structure in the current REAPER project.
    Generates a phrase, repeats it exactly, and then creates a variation on the 3rd repetition.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Length of the base phrase (default 4). Total generated bars = 12.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created arrangement.
    """
    import reaper_python as RPR

    # === Music Theory Lookups ===
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

    if key not in NOTE_MAP: key = "C"
    if scale not in SCALES: scale = "major"
    
    root_midi = 48 + NOTE_MAP[key] # Octave 4
    scale_intervals = SCALES[scale]
    
    def get_diatonic_pitch(degree: int, octave_offset: int = 0) -> int:
        """Convert a 0-indexed scale degree to a MIDI pitch."""
        octaves = degree // len(scale_intervals) + octave_offset
        step = degree % len(scale_intervals)
        return root_midi + (octaves * 12) + scale_intervals[step]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # Total length is 3 iterations of the base phrase
    iterations = 3
    total_bars = bars * iterations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * total_bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # === Step 4: Generate 'Rule of 3' MIDI Data ===
    # Define our chord progressions as arrays of scale degrees (0-indexed)
    # E.g., [0, 4, 5, 3] = I - V - vi - IV
    base_progression = [0, 4, 5, 3] 
    # Variation: starts the same (0, 4), changes ending (1, 4) = I - V - ii - V
    variation_progression = [0, 4, 1, 4] 

    def insert_chord(start_qn, length_qn, root_degree, velocity):
        """Inserts a diatonic 7th chord."""
        chord_degrees = [root_degree, root_degree + 2, root_degree + 4, root_degree + 6]
        for degree in chord_degrees:
            pitch = get_diatonic_pitch(degree, octave_offset=0)
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    start_qn * 960, 
                                    (start_qn + length_qn) * 960, 
                                    1, pitch, velocity, False)

    def insert_melody(start_qn, length_qn, root_degree, velocity):
        """Inserts a rhythmic top-line motif."""
        # A simple arpeggiated motif over the chord
        pitches = [
            get_diatonic_pitch(root_degree, octave_offset=1),
            get_diatonic_pitch(root_degree + 2, octave_offset=1),
            get_diatonic_pitch(root_degree + 4, octave_offset=1),
            get_diatonic_pitch(root_degree + 2, octave_offset=1)
        ]
        
        note_len = length_qn / 4
        for i, p in enumerate(pitches):
            pos = start_qn + (i * note_len)
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    pos * 960, 
                                    (pos + note_len * 0.8) * 960, 
                                    1, p, velocity + 10, False)

    # Build the sequence
    for i in range(iterations):
        # Is this the 3rd iteration? If so, use the variation progression.
        is_variation = (i == 2)
        progression = variation_progression if is_variation else base_progression
        
        # Loop through the bars in the phrase
        for bar_idx in range(bars):
            chord_idx = bar_idx % len(progression)
            root_deg = progression[chord_idx]
            
            # Calculate position in Quarter Notes (QN)
            global_bar = (i * bars) + bar_idx
            start_qn = global_bar * beats_per_bar
            
            # Insert chords and melody
            insert_chord(start_qn, beats_per_bar, root_deg, velocity_base - 15)
            insert_melody(start_qn, beats_per_bar, root_deg, velocity_base)

    RPR.RPR_MIDI_Sort(take)

    # === Step 5: Add FX Chain for a Mellow Pad/Keys Sound ===
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    
    # Tweak ReaSynth for a softer, piano/pad hybrid sound
    # Param 1: Volume, Param 2: Tuning, Param 3: Attack, Param 4: Decay, Param 5: Sustain, Param 6: Release
    RPR.RPR_TrackFX_SetParam(track, 0, 3, 0.05)   # Attack
    RPR.RPR_TrackFX_SetParam(track, 0, 4, 0.5)    # Decay
    RPR.RPR_TrackFX_SetParam(track, 0, 5, 0.5)    # Sustain
    RPR.RPR_TrackFX_SetParam(track, 0, 6, 0.6)    # Release
    
    # Mix in some saw wave (Param 7) for harmonics
    RPR.RPR_TrackFX_SetParam(track, 0, 7, 0.3)    

    # Add EQ to filter harsh highs (Lowpass)
    RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    # Band 4 is typically high shelf or lowpass. Let's force band 4 to lowpass.
    # Param 9 is band 4 type (0=lowshelf, 1=highshelf, 2=band, 3=lowpass, etc. in ReaEQ it's 8 for Lowpass)
    RPR.RPR_TrackFX_SetParam(track, 1, 9, 8.0) 
    # Param 10 is band 4 freq
    RPR.RPR_TrackFX_SetParam(track, 1, 10, 1500.0) # Cutoff at ~1.5kHz

    return f"Created '{track_name}' demonstrating the 'Rule of 3' over {total_bars} bars in {key} {scale} at {bpm} BPM."
```