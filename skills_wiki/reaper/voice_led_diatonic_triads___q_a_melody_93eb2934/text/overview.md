### 1. High-level Design Pattern Extraction

> **Skill Name**: Voice-Led Diatonic Triads & Q&A Melody

* **Core Musical Mechanism**: This pattern relies on a strict diatonic framework (using a scale grid) to build chords and melodies without traditional music theory. It uses three core techniques:
    1. **Scale-Locked Triads**: Building chords by placing a root note and skipping scale degrees (1st, 3rd, 5th of the relative scale).
    2. **Algorithmic Voice Leading**: Inverting notes (moving them up or down an octave) so that every chord in the progression sits in the same frequency register, minimizing jumps.
    3. **Question & Answer Melodic Phrasing**: Creating a rhythmic melodic motif (the "Question"), repeating it, and altering the final notes of the phrase to either create tension (ending on a higher/non-root note) or resolve (walking down to the root note - the "Answer").

* **Why Use This Skill (Rationale)**: This is a foolproof method for generating harmonically safe, pleasing loops. Voice leading ensures the chord changes sound smooth and professional rather than disjointed and amateurish. The Q&A melody structure leverages human psychology: repetition creates familiarity (the groove), and the varied endings provide the necessary tension and release (the hook).

* **Overall Applicability**: This is the foundational songwriting structure for pop, EDM, lo-fi hip hop, and piano ballads. It works perfectly as a starting point for verse pads, intro pianos, or main drop synth lines.

* **Value Addition**: This skill programmatically encodes "visual" music theory. Instead of hardcoding static MIDI pitches, it calculates diatonic scale degrees, mathematically groups chords into the tightest possible voicings (voice leading), and generates a structured 4-bar melodic phrase that musically resolves itself.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & Tempo**: 4/4 time, typically 110-130 BPM.
  - **Chord Rhythm**: Sustained whole notes (1 bar per chord).
  - **Melody Rhythm**: Syncopated 8th notes, establishing a fixed rhythm in Bar 1 that repeats in subsequent bars to create a cohesive motif.

* **Step B: Pitch & Harmony**
  - **Scale Selection**: Fully diatonic. The tutorial uses F Natural Minor (and later G Major).
  - **Chord Progression**: Uses a standard pop progression, derived dynamically from scale degrees (e.g., i - VI - III - v).
  - **Voice Leading Logic**: The first chord sets a "center of gravity" (average pitch). Subsequent chord notes are automatically shifted up or down by octaves until they are as close to this center as possible.
  - **Melody Logic**:
    - *Bars 1 & 3 (Question A)*: Ascending diatonic notes.
    - *Bar 2 (Question B)*: Same rhythm, but ends on a higher scale degree (creates tension).
    - *Bar 4 (Answer)*: Same rhythm, but walks down to the root note of the scale (creates resolution).

* **Step C: Sound Design & FX**
  - **Instrument**: Piano (ReaSynth will be configured to act as an electric piano proxy).
  - **Envelope**: Soft attack, medium decay, and long release to emulate piano keys being pressed and held.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Scale/Diatonic Logic | Python Array Math | Allows us to calculate standard major/minor triad spacings dynamically in any key. |
| Voice Leading | Pitch Averaging Algorithm | Replicates the video's technique of "selecting notes and moving them an octave up/down to be closer to the previous chord". |
| MIDI Generation | `RPR_MIDI_InsertNote` | Precise control over note placement, duration, and velocity. |
| Sound | `ReaSynth` + `ReaEQ` | Provides an immediate, self-contained instrument playback without needing external VSTs like Cloud Piano. |

> **Feasibility Assessment**: 100% reproducible for the MIDI composition technique. The specific "Cloud Piano" VST tone is approximated using REAPER's native ReaSynth with a piano-like ADSR envelope and a low-pass filter to mimic the soft, atmospheric tone.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Piano Chords & Melody",
    bpm: int = 120,
    key: str = "F",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create Voice-Led Diatonic Triads & Q&A Melody in the current REAPER project.
    
    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (e.g., F, G, C).
        scale: Scale type ('major' or 'minor').
        bars: Number of bars (must be a multiple of 4 for the Q&A phrasing).
        velocity_base: Base MIDI velocity (0-127).
    """
    import reaper_python as RPR

    # === Music Theory Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }
    
    if key not in NOTE_MAP or scale not in SCALES:
        return "Error: Invalid key or scale provided."

    root_midi = 48 + NOTE_MAP[key] # Starting around C3
    scale_intervals = SCALES[scale]

    def get_diatonic_pitch(degree, base_octave=0):
        """Convert a 0-based scale degree into a MIDI pitch."""
        octave_offset = degree // 7
        scale_idx = degree % 7
        return root_midi + (base_octave * 12) + (octave_offset * 12) + scale_intervals[scale_idx]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Track & Instrument ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Add ReaSynth (Piano-like ADSR)
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.05) # Attack: slightly soft
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.5)  # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.3)  # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.8)  # Release: long (piano pedal)
    
    # Add ReaEQ (Lowpass to make it sound like 'Cloud Piano')
    eq_idx = RPR.RPR_TrackFX_AddByName(track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 0, 3) # Band 1 Type: Lowpass
    RPR.RPR_TrackFX_SetParam(track, eq_idx, 1, 1000) # Cutoff frequency

    # === Step 3: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)

    # Progression degrees (0-based: 0=i, 5=VI, 2=III, 4=v)
    chord_progression_degrees = [0, 5, 2, 4] 

    note_count = 0
    center_of_gravity = None

    for i in range(bars):
        bar_start_pos = i * bar_length_sec
        bar_end_pos = bar_start_pos + bar_length_sec
        
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_start_pos)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, bar_end_pos)
        
        prog_idx = i % len(chord_progression_degrees)
        root_degree = chord_progression_degrees[prog_idx]

        # 1. Bass Note (Root minus 2 octaves)
        bass_pitch = get_diatonic_pitch(root_degree, base_octave=-2)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, bass_pitch, velocity_base - 10, False)
        note_count += 1

        # 2. Chord Triad (Root, 3rd, 5th)
        triad_pitches = [
            get_diatonic_pitch(root_degree, base_octave=0),
            get_diatonic_pitch(root_degree + 2, base_octave=0),
            get_diatonic_pitch(root_degree + 4, base_octave=0)
        ]

        # 3. Voice Leading Algorithm
        if center_of_gravity is None:
            # Set anchor based on the first chord
            center_of_gravity = sum(triad_pitches) / len(triad_pitches)
        else:
            # Invert notes to be as close to the center_of_gravity as possible
            for j in range(len(triad_pitches)):
                pitch = triad_pitches[j]
                # Shift octave down if too high
                while pitch - 12 >= center_of_gravity - 6:
                    pitch -= 12
                # Shift octave up if too low
                while pitch + 12 <= center_of_gravity + 6:
                    pitch += 12
                triad_pitches[j] = pitch

        for pitch in triad_pitches:
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), velocity_base - 20, False)
            note_count += 1

        # 4. Q&A Melody
        # Rhythm motif (in beats): 0.0, 1.0, 1.5, 2.5
        melody_rhythm = [0.0, 1.0, 1.5, 2.5]
        
        # Determine melody contour based on Q&A phrasing
        phrase_type = i % 4
        if phrase_type == 0 or phrase_type == 2:
            # Question A: Ascending motif
            melody_degrees = [root_degree, root_degree + 1, root_degree + 2, root_degree + 4]
        elif phrase_type == 1:
            # Question B: Ascending motif ending higher (tension)
            melody_degrees = [root_degree, root_degree + 1, root_degree + 4, root_degree + 6]
        else:
            # Answer (Bar 4): Descending motif resolving to tonic (0)
            melody_degrees = [root_degree + 4, root_degree + 2, root_degree + 1, 0]

        # Insert Melody Notes
        for j, beat in enumerate(melody_rhythm):
            m_start_sec = bar_start_pos + (beat * (60.0 / bpm))
            m_end_sec = m_start_sec + (0.5 * (60.0 / bpm)) # 8th note duration
            
            m_start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, m_start_sec)
            m_end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, m_end_sec)
            
            # Put melody 1 octave above chords
            m_pitch = get_diatonic_pitch(melody_degrees[j], base_octave=1) 
            
            RPR.RPR_MIDI_InsertNote(take, False, False, m_start_ppq, m_end_ppq, 0, m_pitch, velocity_base, False)
            note_count += 1

    RPR.RPR_MIDI_Sort(take)

    return f"Created '{track_name}' with {note_count} voice-led notes and Q&A melody over {bars} bars at {bpm} BPM in {key} {scale}."
```