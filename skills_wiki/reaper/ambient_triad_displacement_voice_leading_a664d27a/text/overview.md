# Ambient Triad Displacement & Voice-Leading Sketch

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Triad Displacement & Voice-Leading Sketch

* **Core Musical Mechanism**: The pattern relies on "composition-first" ambient writing. Instead of starting with massive, looping synth pads, it begins "in black and white" (a simple piano-like patch) using strictly 3-voice triadic harmony. It employs rigorous **stepwise voice leading** (moving each note by the smallest possible distance when changing chords) and then applies **melodic displacement**—taking the middle note of the triad and transposing it up an octave. 

* **Why Use This Skill (Rationale)**: Massive ambient synths often mask poor composition. By forcing the harmony into a strict 3-voice structure, you prevent frequency mud. Stepwise voice leading ensures the progression flows smoothly rather than jumping disjointedly. Displacing the middle voice up an octave solves two problems at once: it opens up the chord voicing (creating a lush, wide interval gap between bass and tenor) and automatically generates a soaring, evolving melody from the internal harmony without requiring a separate melodic pass.

* **Overall Applicability**: This is the perfect starting point for ambient, cinematic, or neo-classical tracks. By establishing a solid harmonic and melodic foundation first, you can later assign these distinct MIDI voices to different instruments (e.g., bass note to a drone synth, tenor note to a texture pad, and the displaced soprano note to a string or lead synth).

* **Value Addition**: Compared to a blank MIDI clip or a basic blocked chord progression, this skill algorithmically solves voice-leading. It encodes counterpoint rules to minimize finger movement between chords and automatically structures a wide, open-voiced melodic arrangement.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo Range**: 70 - 90 BPM (Ambient/Slow).
  - **Rhythm**: Sustained whole notes. One chord per bar, allowing the harmony to breathe. No syncopation; the focus is entirely on harmonic movement.

* **Step B: Pitch & Harmony**
  - **Progression**: An evolving diatonic sequence (e.g., I - vi - IV - V in Major, or i - VI - iv - v in Minor).
  - **Voice Leading**: Computes the shortest absolute distance between pitch classes of consecutive chords.
  - **Displacement**: The formula is `[Bass, Middle, Top] -> [Bass, Top, Middle + 12 semitones]`. 

* **Step C: Sound Design & FX**
  - **Instrument**: `ReaSynth` configured as a soft electric piano/sketch instrument. Fast attack, medium decay, low sustain. This honors the creator's advice to start "in black and white."
  - **Space**: `ReaVerbate` added for a small ambient tail, giving the sketch enough atmosphere to be inspiring without masking the notes.

* **Step D: Mix & Automation**
  - **Velocities**: The displaced melody note is given a slightly higher velocity (110) than the supporting harmony notes (85-90) to ensure the generated melody "sings" over the accompaniment.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Stepwise Voice-Leading | Python Algorithmic MIDI Generation | Requires calculating absolute distances between pitch classes to find the optimal inversion. |
| Melodic Displacement | Python Array Manipulation | Programmatically extracts the middle array index and adds +12 to the pitch before inserting the MIDI note. |
| "Black & White" Tone | FX Chain (`ReaSynth` + `ReaVerbate`) | Simulates the clean, exposed piano/wurlitzer tone recommended by the creator for the drafting phase. |

> **Feasibility Assessment**: 100%. The mathematical constraints of the voice-leading and displacement technique described in the video can be perfectly encoded into a generative script. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "AmbientProject",
    track_name: str = "Ambient Piano Sketch",
    bpm: int = 80,
    key: str = "C",
    scale: str = "major",
    bars: int = 8,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Creates an ambient chord sketch using strict 3-voice stepwise leading 
    and middle-voice melodic displacement, as described in the tutorial.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major":          [0, 2, 4, 5, 7, 9, 11],
        "minor":          [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "dorian":         [0, 2, 3, 5, 7, 9, 10],
        "mixolydian":     [0, 2, 4, 5, 7, 9, 10]
    }

    scale_intervals = SCALES.get(scale.lower(), SCALES["major"])
    root_midi = 48 + NOTE_MAP.get(key.upper(), 0) # Start around C3
    
    # Standard ambient diatonic progression: 1, 6, 4, 5 (0-indexed)
    progression_degrees = [0, 5, 3, 4] 

    def get_diatonic_pitch_classes(degree_0_index):
        """Returns the pitch classes (0-11) for a diatonic triad."""
        pcs = []
        for offset in [0, 2, 4]: # Root, 3rd, 5th
            idx = degree_0_index + offset
            octave_shift = idx // len(scale_intervals)
            scale_degree = idx % len(scale_intervals)
            pitch = root_midi + (octave_shift * 12) + scale_intervals[scale_degree]
            pcs.append(pitch % 12)
        return pcs

    # Step 1: Generate the raw target triads (Pitch Classes only)
    target_chords_pcs = [get_diatonic_pitch_classes(d) for d in progression_degrees]

    # Step 2: Algorithmic Voice Leading
    voiced_chords = []
    
    for i, target_pcs in enumerate(target_chords_pcs):
        if i == 0:
            # First chord: Root position near C3
            c = sorted([
                (target_pcs[0] + 48), 
                (target_pcs[1] + 48), 
                (target_pcs[2] + 48)
            ])
            # Ensure they are in the correct octave if modulo wrapped weirdly
            c = [p if p >= 48 else p + 12 for p in c]
            voiced_chords.append(sorted(c))
        else:
            prev_chord = voiced_chords[-1]
            best_inv = None
            best_dist = 9999
            
            # Brute force search all octave combinations between MIDI 36 and 72
            # to find the inversion with the absolute minimum movement from previous chord
            for o0 in [3, 4, 5]:
                for o1 in [3, 4, 5]:
                    for o2 in [3, 4, 5]:
                        p0 = target_pcs[0] + o0 * 12
                        p1 = target_pcs[1] + o1 * 12
                        p2 = target_pcs[2] + o2 * 12
                        c = sorted([p0, p1, p2])
                        
                        # Constraints: No unisons, max spread of ~1.5 octaves (19 semitones)
                        if c[0] == c[1] or c[1] == c[2]: continue
                        if c[2] - c[0] > 19: continue
                        
                        # Distance cost function
                        dist = sum(abs(c[j] - prev_chord[j]) for j in range(3))
                        if dist < best_dist:
                            best_dist = dist
                            best_inv = c
                            
            voiced_chords.append(best_inv)

    # Step 3: Apply the "Tutorial Secret" -> Displace middle voice up an octave
    final_chords = []
    for chord in voiced_chords:
        # chord is sorted [Low, Mid, High]
        displaced_chord = [
            (chord[0], velocity_base - 5),      # Bass (slightly softer)
            (chord[2], velocity_base - 10),     # Tenor/Alto (softest, backing pad)
            (chord[1] + 12, velocity_base + 15) # Displaced Melody (loudest, singing)
        ]
        final_chords.append(displaced_chord)

    # === REAPER Environment Setup ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Insert MIDI Notes
    notes_created = 0
    ticks_per_quarter = 960
    ticks_per_bar = ticks_per_quarter * beats_per_bar

    # Loop the 4-chord progression to fill requested bars
    for bar in range(bars):
        chord_idx = bar % len(final_chords)
        chord = final_chords[chord_idx]
        
        start_ppq = bar * ticks_per_bar
        end_ppq = start_ppq + ticks_per_bar - 10 # Slight gap for legato piano feel
        
        for pitch, vel in chord:
            RPR.RPR_MIDI_InsertNote(
                take, False, False, 
                start_ppq, end_ppq, 
                0, int(pitch), int(vel), True
            )
            notes_created += 1

    RPR.RPR_MIDI_Sort(take)

    # === Sound Design: "Black & White" Sketch Tone ===
    # 1. Add ReaSynth for a basic Electric Piano/Sine pluck
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    # Tweak ReaSynth for a plucky/piano envelope rather than a sustained organ
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.05) # Attack (fast but not clicking)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.3)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.1)  # Sustain (low)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.6)  # Release (medium long tail)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.5)  # Mix in some square wave for bite
    
    # 2. Add ReaVerbate to give it some ambient space without getting muddy
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.3)   # Wet mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 0.8)   # Dry mix
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.7)   # Room size (large)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 3, 0.4)   # Dampening

    return f"Created '{track_name}' with {notes_created} notes over {bars} bars at {bpm} BPM. Voice-leading algorithm applied."
```