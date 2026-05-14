### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Track Band Template & Ghost-Note Workflow

* **Core Musical Mechanism**: A synchronized 4-part arrangement (Drums, Bass, Rhythm Chords, Lead Arpeggios) constructed to leverage multi-track MIDI editing. The tracks are harmonically locked using a shared scale-degree progression (`I - vi - IV - V`), enabling the composer to see the "ghost notes" of the rhythm section while writing lead melodies.
* **Why Use This Skill (Rationale)**: Managing multiple MIDI instruments (like an orchestral section or a rock band) is visually chaotic. By setting up color-coded tracks and linking selection to visibility, a producer can view interlocking rhythms and frequency masking across the whole arrangement at once. Musically, this specific arrangement demonstrates strong rhythmic synergy: the driving 8th-note bass locks with the kick drum on beats 1 and 2.5, while the lead arpeggio glues the sustained rhythm guitar chords together.
* **Overall Applicability**: This is the foundational setup for rock/pop/metal tracking, orchestral mockups, or complex electronic productions where seeing the harmonic relationship between the bassline, chords, and leads is critical.
* **Value Addition**: Compared to a blank project, this skill automatically sets up a vividly color-coded, 4-track musical jam. It generates an endlessly loopable rhythm section and arpeggiated lead tied to whatever scale and key you parameterize, providing an immediate canvas to practice multi-track "Logic-style" MIDI editing in REAPER.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Time Signature & Tempo**: 4/4 time, typically driving at around 120 BPM.
  * **Drums**: Standard rock beat (Kick on 1, 2.5, 3; Snare on 2 and 4; strict 8th-note hi-hats).
  * **Bass & Lead**: Continuous 8th-note driving rhythms. The notes are played slightly staccato (duration of 0.45 beats) to leave a tiny gap for articulation and groove.
  * **Rhythm Guitar**: Sustained whole-note chords to provide a harmonic bed.

* **Step B: Pitch & Harmony**
  * **Progression**: Follows a universal `1st - 6th - 4th - 5th` scale degree progression (e.g., `C - Am - F - G` in Major, or `Cm - Ab - Fm - Gm` in Minor).
  * **Voicings**: The Rhythm Guitar plays close-voiced root-position triads. The Lead Guitar plays a 1-3-5-8 rolling arpeggio an octave higher.

* **Step C: Sound Design & FX**
  * The tutorial explicitly focuses on the MIDI visual setup rather than specific synth plugins. To reproduce this safely in a stock REAPER environment, the tracks are grouped, named, and vibrantly color-coded (Purple, Blue, Green, Orange) exactly as shown in the tutorial's custom theme to enable the "Color notes by track" workflow. 

* **Step D: Mix & Automation**
  * The tracks are heavily separated by octave: Bass (C1-C2), Rhythm (C2-C3), Lead (C4-C5), preventing frequency masking right at the MIDI composition stage.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Setup & Colors | `RPR_InsertTrackAtIndex`, `I_CUSTOMCOLOR` | Perfectly recreates the visual environment required for the tutorial's multi-track workflow. |
| Musical Interlocking | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows calculation of exact harmony stacks and interlocking 8th-note rhythms using music theory math. |
| Synchronization | `RPR_MIDI_GetPPQPosFromProjTime` | Ensures the 4 independent tracks maintain perfect phase alignment across the generated loops regardless of tempo. |

> **Feasibility Assessment**: 100% of the *musical MIDI structure* and *visual track setup* shown at the climax of the tutorial is reproduced. The workflow configuration itself (global REAPER preference changes) is intentionally omitted as scripts should be non-destructive/additive, but the resulting project provides the exact multi-track scenario the configuration is designed to edit.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MultiTrack_Workflow",
    track_name: str = "Band",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a 4-track color-coded Band Template (Drums, Bass, Rhythm, Lead)
    with an interlocking chord progression and arpeggios.

    Args:
        project_name: Project identifier (for logging).
        track_name: Base name for the created tracks.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, pentatonic_minor, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the creation.
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
        "pentatonic_major": [0, 2, 4, 7, 9],
        "pentatonic_minor": [0, 3, 5, 7, 10],
        "blues":            [0, 3, 5, 6, 7, 10],
    }

    # Step 1: Initialize values
    root_midi = NOTE_MAP.get(key, 0) + 48 # Anchor around C3 (note 48)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # Standard 4-chord progression: 1st, 6th, 4th, 5th degrees (0-indexed)
    progression = [0, 5, 3, 4] 

    def get_chord_notes(scale_degree, root_base):
        """Builds a 1-3-5-8 chord based on the scale degree."""
        notes = []
        for chord_tone in [0, 2, 4, 7]: # 1st, 3rd, 5th, and Octave
            deg = scale_degree + chord_tone
            octave = deg // len(scale_intervals)
            rem = deg % len(scale_intervals)
            pitch = root_base + (octave * 12) + scale_intervals[rem]
            notes.append(pitch)
        return notes

    def add_midi_note(take, start_beat, length_beats, pitch, vel):
        """Helper to safely insert MIDI notes using exact PPQ timing."""
        start_sec = (start_beat / bpm) * 60.0
        end_sec = ((start_beat + length_beats) / bpm) * 60.0
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_sec)
        
        # Clamp velocity
        vel = max(1, min(127, int(vel)))
        pitch = max(0, min(127, int(pitch)))
        
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)

    # Track setups (Colors mimic the tutorial's custom theme to allow 'Color by Track')
    tracks_info = [
        {"name": f"{track_name}_Drums", "role": "drums",  "color": 150 + (0 * 256) + (200 * 65536) | 0x1000000}, # Purple
        {"name": f"{track_name}_Bass",  "role": "bass",   "color": 0 + (100 * 256) + (255 * 65536) | 0x1000000}, # Blue
        {"name": f"{track_name}_Rhythm","role": "rhythm", "color": 0 + (200 * 256) + (100 * 65536) | 0x1000000}, # Green
        {"name": f"{track_name}_Lead",  "role": "lead",   "color": 255 + (150 * 256) + (0 * 65536) | 0x1000000}, # Orange
    ]

    start_track_idx = RPR.RPR_CountTracks(0)
    item_length_sec = (60.0 / bpm) * 4.0 * bars

    for i, t_info in enumerate(tracks_info):
        # Create track and apply colors
        RPR.RPR_InsertTrackAtIndex(start_track_idx + i, True)
        track = RPR.RPR_GetTrack(0, start_track_idx + i)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t_info["name"], True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "I_CUSTOMCOLOR", t_info["color"])

        # Create MIDI Item
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        role = t_info["role"]
        
        # Populate Musical Pattern
        for bar in range(bars):
            bar_start_beat = bar * 4.0
            chord_deg = progression[bar % len(progression)]
            chord_notes = get_chord_notes(chord_deg, root_midi)

            if role == "drums":
                # General MIDI mapping: Kick=36, Snare=38, HH=42, Crash=49
                for b in [0, 1.5, 2.0]:  # Rock Kick
                    add_midi_note(take, bar_start_beat + b, 0.25, 36, velocity_base)
                for b in [1.0, 3.0]:     # Snare
                    add_midi_note(take, bar_start_beat + b, 0.25, 38, velocity_base)
                for hz in range(8):      # 8th note Hi-hats
                    b = hz * 0.5
                    add_midi_note(take, bar_start_beat + b, 0.25, 42, velocity_base - 15)
                if bar == 0:             # Crash on the 1 of loop
                    add_midi_note(take, 0, 0.5, 49, velocity_base + 10)

            elif role == "bass":
                bass_pitch = chord_notes[0] - 12 # Octave down
                for idx in range(8): # Driving 8th notes
                    b = idx * 0.5
                    add_midi_note(take, bar_start_beat + b, 0.45, bass_pitch, velocity_base)

            elif role == "rhythm":
                for pitch in chord_notes[:3]: # Root, 3rd, 5th triad
                    add_midi_note(take, bar_start_beat, 4.0, pitch - 12, velocity_base - 10)

            elif role == "lead":
                # Arpeggio pattern using indices of the chord_notes list
                arp_pattern = [0, 1, 2, 3, 2, 1, 0, 1]
                for idx, tone_idx in enumerate(arp_pattern):
                    b = idx * 0.5
                    pitch = chord_notes[tone_idx] + 12 # Octave up
                    add_midi_note(take, bar_start_beat + b, 0.45, pitch, velocity_base + 5)
        
        # Apply sorting to clean up the MIDI event list
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track '{track_name}' band template over {bars} bars at {bpm} BPM in {key} {scale}."
```