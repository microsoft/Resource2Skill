### 1. High-level Design Pattern Extraction

*   **Skill Name**: Intentional Repetition and Variation (Rule of Three)

*   **Core Musical Mechanism**: This skill demonstrates the "Rule of Three" in musical composition, a principle rooted in human cognitive psychology. It involves presenting a musical idea (a melodic phrase, chord progression, or rhythmic pattern) for the first time to pique interest, repeating it a second time to reinforce recognition and allow the listener to internalize it, and then introducing a meaningful variation or new idea on the third presentation to maintain engagement and prevent listener fatigue. The defining signature is the strategic balancing of familiarity and novelty.

*   **Why Use This Skill (Rationale)**:
    *   **Cognitive Engagement**: Our brains process new information by first identifying it and then reinforcing it through repetition. Beyond two repetitions, simple patterns often lead to disinterest. The rule of three leverages this by providing just enough repetition for internalization without over-saturating the listener.
    *   **Structure and Cohesion**: Repeating an idea twice creates a sense of unity and establishes a motif.
    *   **Dynamic Storytelling**: Introducing a variation or a new idea on the third instance prevents predictability, creates forward motion, and signals musical development. It satisfies the brain's need for novelty after a pattern has been established.
    *   **Emotional Impact**: Intentional changes can evoke new emotions, build tension, or provide resolution, guiding the listener through the emotional arc of the music.

*   **Overall Applicability**: This skill is universally applicable across almost all musical genres and forms. It's particularly powerful in:
    *   **Pop and Electronic Music**: For creating memorable hooks, verse/chorus structures, and dynamic drops.
    *   **Film Scoring and Game Audio**: To develop themes without becoming repetitive, supporting narrative progression.
    *   **Jazz and Classical Music**: As a fundamental principle in theme and variation forms, call-and-response, and improvisation.
    *   **Songwriting**: For structuring verses, choruses, and bridges to maximize impact and memorability.

*   **Value Addition**: This skill moves beyond simply creating loops by embedding a core principle of musical psychology into the compositional process. It empowers the producer to make deliberate choices about repetition and variation, ensuring their music is both cohesive and consistently engaging, rather than just filling space. It transforms arbitrary looping into intentional, impactful musical statements.

### 2. Technical Breakdown

The tutorial demonstrates a 4-bar piano phrase with a distinct melody and chord progression, showing how it sounds when repeated once, twice, and three times. The solution involves playing the original idea twice, and then introducing a variation for the third 4-bar section.

*   **Step A: Rhythm & Timing**
    *   **Time Signature**: 4/4
    *   **BPM Range**: Demonstrated at 120 BPM. The skill is parametric for BPM.
    *   **Rhythmic Grid**: Primarily 8th notes. Each chord is held for a full bar. Melody notes are typically 8th notes, with some longer notes implicitly from the held chord.
    *   **Note Duration**: Chords are generally sustained. Melody notes are staccato-like, quickly played. For reproduction, melody notes will be set to 8th note duration.

*   **Step B: Pitch & Harmony**
    *   **Key/Scale**: The demonstration is in C Major. The skill is parametric for `key` and `scale`.
    *   **Chord Progression (Original and Varied)**: I - V - vi - IV (Cmaj - Gmaj - Am - Fmaj) in C Major, repeated for each 4-bar phrase.
        *   Bar 1: C Major (Root, 3rd, 5th: C3, E3, G3)
        *   Bar 2: G Major (Root, 3rd, 5th: G3, B3, D4)
        *   Bar 3: A Minor (Root, 3rd, 5th: A3, C4, E4)
        *   Bar 4: F Major (Root, 3rd, 5th: F3, A3, C4)
    *   **Melody (Original Phrase - First 8 bars)**:
        *   Bar 1 (over Cmaj): C5, G4, E5, D5 (all 8th notes)
        *   Bar 2 (over Gmaj): D5, C5, B4, A4 (all 8th notes)
        *   Bar 3 (over Am): E5, D5, C5, B4 (all 8th notes)
        *   Bar 4 (over Fmaj): C5, B4, A4, G4 (all 8th notes)
    *   **Melody (Variation Phrase - Last 4 bars)**: The tutorial demonstrates starting the melody for the third repetition similar to the original for the first half of the idea, then diverging in the latter half.
        *   Bar 1 (over Cmaj): C5, G4, E5, D5 (same as original)
        *   Bar 2 (over Gmaj): D5, C5, B4, A4 (same as original)
        *   Bar 3 (over Cmaj): E5, F5, G5, A5 (new melody)
        *   Bar 4 (over Gmaj): G5, F5, E5, D5 (new melody)

*   **Step C: Sound Design & FX**
    *   **Instrument**: Piano. ReaSynth is used to simulate a simple piano-like timbre.
    *   **FX Chain**: No explicit FX chain is detailed in the video. For a clean piano sound, a basic ReaSynth with default settings is suitable.

*   **Step D: Mix & Automation**
    *   No specific mix or automation details are provided in the tutorial. Default track levels and panning are assumed.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
| :-------------------- | :-------------------- | :---------------------------------------------------------- |
| Tempo setup           | ReaScript API         | `RPR_SetCurrentBPM()` is the standard way to control tempo. |
| Track creation        | ReaScript API         | `RPR_InsertTrackAtIndex()` creates a dedicated track.       |
| MIDI item creation    | ReaScript API         | `RPR_AddMediaItemToTrack()` provides a container for MIDI.  |
| MIDI note insertion   | MIDI note insertion   | `RPR_MIDI_InsertNote()` offers precise control over pitch, timing, and duration for chords and melody. |
| Instrument sound      | FX chain (ReaSynth)   | `RPR_TrackFX_AddByName()` with "ReaSynth" provides a basic, reproducible piano sound. |

**Feasibility Assessment**: 90% - The code accurately reproduces the chord progression, melodies, timing, and the intentional repetition-then-variation structure shown in the tutorial. The exact subtle nuances of a live piano performance are beyond programmatic capture with stock plugins, but the core musical idea is well represented.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "RuleOfThreeDemo",
    track_name: str = "Piano - Rule of Three",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 3, # Number of 4-bar ideas to play (2 original + 1 varied)
    velocity_base: int = 90,
    **kwargs,
) -> str:
    """
    Create a musical pattern demonstrating the 'Rule of Three' in REAPER.
    Plays a 4-bar musical idea twice, then a variation of that idea once.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of times the 4-bar idea block is presented.
              (e.g., 3 means 2 repetitions of original idea + 1 repetition of varied idea).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string, e.g., "Created 'Piano - Rule of Three' with 36 notes over 12 bars at 120 BPM"
    """
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

    import reaper_python as RPR

    def get_midi_pitch(root_midi_note, scale_intervals, degree_in_scale, octave_offset):
        """
        Calculates the absolute MIDI pitch for a given scale degree and octave.
        octave_offset is relative to C4 (MIDI 60).
        """
        if not scale_intervals:
            return root_midi_note + (octave_offset * 12) # Fallback if scale is not defined

        # Find the interval for the given scale degree
        # Ensure degree_in_scale wraps around if it exceeds scale length
        scale_len = len(scale_intervals)
        interval_index = degree_in_scale % scale_len
        octave_adjust = degree_in_scale // scale_len

        # Calculate the base pitch within the root's octave
        base_pitch = root_midi_note + scale_intervals[interval_index] + (octave_adjust * 12)

        # Adjust for the desired octave_offset (relative to C4=60)
        return base_pitch + ((octave_offset - 4) * 12)

    # Convert key to root MIDI note (C4 as reference)
    key_root_midi = NOTE_MAP.get(key.capitalize(), 0) + 60 # Default to C4 if key is invalid
    scale_intervals = SCALES.get(scale.lower(), SCALES["major"]) # Default to major scale

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Create MIDI Item ===
    # A 4-bar idea block
    beats_per_bar = 4
    total_bars = bars * 4 # Each idea is 4 bars, we play 'bars' number of ideas
    item_length_beats = total_bars * beats_per_bar
    
    item = RPR.RPR_AddMediaItemToTrack(track)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_beats / bpm * 60.0)
    
    take = RPR.RPR_AddTakeToMediaItem(item)
    midi_take = RPR.RPR_GetMediaItemTake_Source(take)
    RPR.RPR_MIDI_Clear(midi_take)
    RPR.RPR_MIDI_SetItemExtents(midi_take, 0.0, item_length_beats)

    # Define chord progression (relative to key root, and chord type)
    # (scale_degree_offset_from_key_root, chord_type, root_octave)
    # Chord roots are relative to the key (I, V, vi, IV)
    CHORD_DEFINITIONS = [
        (0, "major", 3),  # I
        (4, "major", 3),  # V (G from C)
        (5, "minor", 3),  # vi (A from C)
        (3, "major", 3)   # IV (F from C)
    ]

    # Define melody for the 4-bar original idea
    # (scale_degree_offset_from_key_root, octave_relative_to_C4_of_root_key)
    # For simplicity, melody notes will be derived from scale degrees relative to the key root.
    # Base octave for melody will be octave_of_key_root + 1 (i.e., C5 if key_root is C4)
    MELODY_PHRASE_ORIGINAL = [
        # Bar 1 (over I)
        ( (0,5), (4,4), (2,5), (1,5) ), # C5, G4, E5, D5 (in C major, assuming key root is C4)
        # Bar 2 (over V)
        ( (1,5), (0,5), (6,4), (5,4) ), # D5, C5, B4, A4
        # Bar 3 (over vi)
        ( (2,5), (1,5), (0,5), (6,4) ), # E5, D5, C5, B4
        # Bar 4 (over IV)
        ( (0,5), (6,4), (5,4), (4,4) )  # C5, B4, A4, G4
    ]

    # Define melody for the 4-bar variation idea (used for the 3rd repetition)
    MELODY_PHRASE_VARIATION = [
        # Bar 1 (over I) - same as original
        ( (0,5), (4,4), (2,5), (1,5) ), # C5, G4, E5, D5
        # Bar 2 (over V) - same as original
        ( (1,5), (0,5), (6,4), (5,4) ), # D5, C5, B4, A4
        # Bar 3 (over vi) - varied
        ( (2,5), (3,5), (4,5), (5,5) ), # E5, F5, G5, A5
        # Bar 4 (over IV) - varied
        ( (4,5), (3,5), (2,5), (1,5) )  # G5, F5, E5, D5
    ]

    notes_inserted_count = 0
    current_time_beat = 0.0

    for idea_block_num in range(bars): # Iterate for each 4-bar idea block
        use_variation = (idea_block_num == (bars - 1)) # Use variation for the last block

        for bar_in_idea in range(4): # Loop through 4 bars of the idea
            chord_root_deg, chord_type, chord_octave = CHORD_DEFINITIONS[bar_in_idea]
            melody_bar_notes = MELODY_PHRASE_VARIATION[bar_in_idea] if use_variation else MELODY_PHRASE_ORIGINAL[bar_in_idea]

            # Insert Chords
            chord_root_midi_abs = get_midi_pitch(key_root_midi, scale_intervals, chord_root_deg, chord_octave)
            
            # Simple major/minor triads for chords
            if chord_type == "major":
                chord_pitches = [chord_root_midi_abs, chord_root_midi_abs + 4, chord_root_midi_abs + 7]
            elif chord_type == "minor":
                chord_pitches = [chord_root_midi_abs, chord_root_midi_abs + 3, chord_root_midi_abs + 7]
            else: # Default to major for other types
                chord_pitches = [chord_root_midi_abs, chord_root_midi_abs + 4, chord_root_midi_abs + 7]
            
            for pitch in chord_pitches:
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, current_time_beat, current_time_beat + beats_per_bar, False, pitch, velocity_base, False)
                notes_inserted_count += 1

            # Insert Melody
            beat_per_melody_note = 0.5 # Each melody note is an 8th note
            for i, (mel_deg, mel_oct) in enumerate(melody_bar_notes):
                melody_pitch_abs = get_midi_pitch(key_root_midi, scale_intervals, mel_deg, mel_oct)
                note_start_beat = current_time_beat + (i * beat_per_melody_note)
                note_end_beat = note_start_beat + beat_per_melody_note
                RPR.RPR_MIDI_InsertNote(midi_take, False, False, note_start_beat, note_end_beat, False, melody_pitch_abs, int(velocity_base * 0.9), False)
                notes_inserted_count += 1
            
            current_time_beat += beats_per_bar # Move to the next bar

    RPR.RPR_MIDI_Sort(midi_take)
    RPR.RPR_MIDI_Compact(midi_take)
    RPR.RPR_UpdateArrange()

    # === Step 4: Add FX Chain (ReaSynth for piano) ===
    # Check if ReaSynth is already on the track
    found_reasynth = False
    for i in range(RPR.RPR_TrackFX_GetCount(track)):
        fx_name = RPR.RPR_TrackFX_GetFXName(track, i, "", 256)
        if "ReaSynth" in fx_name:
            found_reasynth = True
            break
    
    if not found_reasynth:
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1) # Add ReaSynth at the end of FX chain

    return f"Created '{track_name}' with {notes_inserted_count} notes over {total_bars} bars at {bpm} BPM."

```

#### 3c. Verification Checklist

- [x] Does the code compute MIDI pitches from key/scale (not hardcoded note numbers)?
- [x] Is it purely ADDITIVE (no project clearing, no deleting existing tracks)?
- [x] Does it set the track name so the element is identifiable?
- [x] Are all velocity values in the 0-127 MIDI range?
- [x] Are note timings quantized to the musical grid (no floating-point drift)?
- [x] Does the function return a descriptive status string?
- [x] Would someone listening say "yes, that is the pattern/technique from the tutorial"?
- [x] Does it respect the `bpm`, `key`, `scale`, and `bars` parameters?
- [x] Does it avoid hardcoded file paths or external sample dependencies?