# Essential EDM Block Chord Progression (I - V - vi - IV)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Essential EDM Block Chord Progression (I - V - vi - IV)

* **Core Musical Mechanism**: This pattern generates the foundational harmonic layer of an electronic dance music (EDM) or pop track using a classic 4-chord progression (I - V - vi - IV). Instead of relying on a human player to voice the chords, it relies on strict intervallic stacking (+4/+7 for Major, +3/+7 for Minor) to instantly construct block chords. The chords are played as fully sustained, legato whole-notes, creating a continuous "pad" or "bed" of harmony.
* **Why Use This Skill (Rationale)**: The I-V-vi-IV progression is arguably the most successful harmonic sequence in modern popular music. Moving from the stable Tonic (I) to the tense Dominant (V), resolving deceptively into the emotional Submediant (vi), and resting on the uplifting Subdominant (IV) creates a perfectly balanced emotional loop. By stacking exact MIDI intervals, we eliminate the need to memorize scale degrees and ensure perfect harmonic alignment.
* **Overall Applicability**: This is the starting point for 80% of modern Pop, EDM, Future Bass, and House tracks. These block chords are typically routed to a lush supersaw synth, a filtered pad, or an aggressive piano. 
* **Value Addition**: Compared to an empty project, this skill instantly injects a radio-ready harmonic progression. It also employs basic voice-leading (dropping the V, vi, and IV chords down an octave relative to the root) to prevent the chords from leaping wildly up the keyboard, ensuring a cohesive, professional-sounding pad texture.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature**: 4/4
  - **Tempo**: 120 - 128 BPM (standard EDM range).
  - **Grid/Duration**: 1 whole note (4 beats) per chord. The chords are strictly quantized and 100% legato, meaning the end of one chord perfectly touches the start of the next, leaving no gaps.

* **Step B: Pitch & Harmony**
  - **Key/Scale**: Diatonic Major.
  - **Progression**: I - V - vi - IV.
  - **Chord Qualities**: 
    - **I**: Major triad (Root, +4 semitones, +7 semitones)
    - **V**: Major triad
    - **vi**: Minor triad (Root, +3 semitones, +7 semitones)
    - **IV**: Major triad
  - **Voice Leading**: To maintain a tight sound, the root notes are mapped intelligently so the progression stays clustered (e.g., C3, G2, A2, F2 instead of leaping up to G3 and A3).

* **Step C: Sound Design & FX**
  - **Instrument**: A polyphonic synthesizer pad. (In REAPER, we use the stock `ReaSynth` to make the MIDI immediately audible).
  - **Character**: Fully sustained, rich harmonic content. 

* **Step D: Mix & Automation**
  - **Velocity**: Fixed flat velocity (e.g., 100) since early EDM pad layers often rely on synth-internal envelopes rather than MIDI velocity dynamics.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track & Item Creation | `RPR_InsertTrackAtIndex`, `RPR_CreateNewMIDIItemInProj` | Additive setup of the workspace for the chords. |
| Harmonic Stacking | `RPR_MIDI_InsertNote` | Directly applies the +3/+4/+7 custom action logic from the tutorial into precise, perfectly quantized MIDI data. |
| Voice Leading | Pitch Offset Math | Solves the "clumsiness" of painting chords by automatically calculating the closest bass notes for the progression. |
| Instrument | `RPR_TrackFX_AddByName` | Adds REAPER's native `ReaSynth` so the user can immediately hear the block chords. |

> **Feasibility Assessment**: 100%. The script perfectly recreates the exact major/minor chord stacking logic demonstrated by Kenny Gioia, mapping it out over the timeline into a fully functional 4-bar loop.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "EDM Pad Chords",
    bpm: int = 120,
    key: str = "C",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create an Essential EDM Block Chord Progression in the current REAPER project.

    Args:
        project_name: Project identifier.
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (defaults to major for this specific progression).
        bars: Number of bars to generate (loops the 4-bar progression).
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides (e.g., use_7ths=True).

    Returns:
        Status string describing the creation.
    """
    import reaper_python as RPR

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Check if 7th chords were requested via kwargs
    use_7ths = kwargs.get("use_7ths", False)

    # Chord structure templates (Intervallic distances in semitones from root)
    if use_7ths:
        CHORD_TEMPLATES = {
            "major": [0, 4, 7, 11], # Major 7th
            "minor": [0, 3, 7, 10], # Minor 7th
        }
    else:
        CHORD_TEMPLATES = {
            "major": [0, 4, 7],     # Major Triad
            "minor": [0, 3, 7],     # Minor Triad
        }

    # The I - V - vi - IV Progression
    # Offsets are calculated to provide good voice leading (keeping notes close together)
    # rather than jumping all the way up the octave.
    progression = [
        {"numeral": "I",  "root_offset": 0,  "quality": "major"}, # e.g., C3
        {"numeral": "V",  "root_offset": -5, "quality": "major"}, # e.g., G2
        {"numeral": "vi", "root_offset": -3, "quality": "minor"}, # e.g., A2
        {"numeral": "IV", "root_offset": -7, "quality": "major"}, # e.g., F2
    ]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)

    # === Step 2: Create Additive Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add Basic Synthesizer ===
    # Adds ReaSynth so the chords are audible immediately
    RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)

    # === Step 4: Create MIDI Item ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    # Create MIDI item
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 5: Insert Chord Notes ===
    # Base octave 3 (REAPER C3 = MIDI note 48 usually, standard for pads)
    base_midi_note = 48 + NOTE_MAP.get(key.capitalize(), 0)
    
    notes_added = 0

    for bar in range(bars):
        # Loop the 4-chord progression if bars > 4
        chord_def = progression[bar % len(progression)]
        
        # Timing (Project Quarter Notes)
        start_qn = bar * 4.0
        end_qn = start_qn + 4.0 # Whole note duration
        
        # Convert QN to MIDI Ticks (PPQ)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, start_qn)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, end_qn)

        # Calculate actual pitches for this chord
        chord_root = base_midi_note + chord_def["root_offset"]
        intervals = CHORD_TEMPLATES[chord_def["quality"]]
        
        for interval in intervals:
            pitch = chord_root + interval
            
            # Ensure pitch is within safe MIDI bounds
            if 0 <= pitch <= 127:
                RPR.RPR_MIDI_InsertNote(
                    take, 
                    False,          # selected
                    False,          # muted
                    start_ppq,      # start time
                    end_ppq,        # end time
                    0,              # channel
                    int(pitch),     # pitch
                    velocity_base,  # velocity
                    True            # noSort (we sort at the end)
                )
                notes_added += 1

    # Finalize MIDI by sorting the event list
    RPR.RPR_MIDI_Sort(take)

    # Update REAPER UI
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {notes_added} notes (I-V-vi-IV) over {bars} bars at {bpm} BPM in {key} {scale}."
```