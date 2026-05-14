# Neo-Soul / R&B Extended Chord Engine

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neo-Soul / R&B Extended Chord Engine

* **Core Musical Mechanism**: The tutorial demonstrates a chord-generating engine focused on "Jazz/R&B" styles, paired with a Rhodes electric piano. The defining signature of this sound is the use of **lush, extended chord voicings** (minor 9ths, major 9ths, dominant 13ths, and minor 11ths) played with **syncopated rhythmic pushes**. Instead of standard root-position triads, the harmony spans multiple octaves, placing the root in the bass and clustering the extensions (7ths, 9ths, 11ths) in the middle register. 
* **Why Use This Skill (Rationale)**: Extended chords introduce harmonic ambiguity and richness (e.g., a major 9th chord contains both a major and a minor triad). When paired with syncopation (striking a chord an eighth or sixteenth note *before* the downbeat of the next measure), it creates the signature laid-back "pocket" groove fundamental to Neo-Soul, R&B, and modern Hip-Hop. The synthesized Rhodes tone (using Triangle/Sine waves with Tremolo) compliments these voicings because its rounded frequency response prevents the dense chord extensions from sounding harsh or clashing.
* **Overall Applicability**: Perfect for intro beds, verse progressions in lo-fi hip-hop, Neo-soul grooves, or deep house breakdowns. 
* **Value Addition**: This skill moves beyond basic triads to encode professional jazz/R&B chord voicings and rhythmic humanization (strumming effects and syncopation). It provides a self-contained "Rhodes" electric piano sound using native REAPER effects, completely bypassing the need for third-party VSTs.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 80-95 BPM.
  - **Grid/Feel**: 16th-note subdivision, heavily swung or laid back.
  - **Pattern**: A 2-bar loop where the second and fourth chords are "pushed" (played on the "and" of beat 3, anticipating the next chord). A slight delay is applied between notes of the same chord (a 15ms "strum" effect) to emulate a human keyboardist.

* **Step B: Pitch & Harmony**
  - **Key/Scale Logic**: Adapts dynamically.
    - *Major Context*: `ii9` → `V13` → `Imaj9` → `vi11`
    - *Minor Context*: `i9` → `iv9` → `v7b9` → `bVImaj9`
  - **Voicings**: 
    - `min9` stack: `[Root, +15, +19, +22, +26]` (e.g., C2, Eb3, G3, Bb3, D4)
    - `maj9` stack: `[Root, +14, +19, +23, +26]`
    - `dom13` stack: `[Root, +10, +16, +21, +26]`
    - `dom7b9` stack: `[Root, +16, +19, +22, +25]`

* **Step C: Sound Design & FX**
  - **Synthesizer**: `ReaSynth` configured to emulate a Rhodes tone (prominent Triangle wave, soft attack, long release).
  - **Modulation**: `JS: Tremolo` to recreate the classic Rhodes Suitcase stereo panning/tremolo effect (around 2Hz, subtle depth).
  - **Space**: `ReaVerbate` for a small room ambiance.

* **Step D: Mix & Automation**
  - Strummed velocity humanization: Each note in the chord receives a slightly randomized velocity deviation to make the digital synth respond with natural dynamics.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| R&B Chord Voicings | MIDI note insertion (`RPR_MIDI_InsertNote`) | Allows precise programming of 5-note extended harmony stacks and humanized "strum" timing. |
| Rhodes Piano VST | FX chain (`ReaSynth` + `JS: Tremolo`) | The third-party plugins in the tutorial are unavailable. This native chain faithfully recreates the warm, modulated electric piano tone. |
| Progression Logic | Python conditional logic | Dynamically adapts the harmonic progression based on the provided scale (Major vs. Minor context). |

> **Feasibility Assessment**: 90% reproduction. While the exact GUI and proprietary sample set of the advertised VSTs are omitted, the *musical result*—the lush Neo-Soul chords, the syncopated groove, and the modeled electric piano tone—is fully reproduced using native REAPER components.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Neo-Soul Rhodes",
    bpm: int = 85,
    key: str = "Eb",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 85,
    **kwargs,
) -> str:
    """
    Create a Neo-Soul / R&B extended chord progression in the current REAPER project.

    Args:
        project_name: Project identifier (for logging).
        track_name: Name for the created track.
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor, dorian, etc.).
        bars: Number of bars to generate.
        velocity_base: Base MIDI velocity (0-127).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the created track and pattern.
    """
    import reaper_python as RPR
    import random

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 2: Create Track ===
    track_idx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(track_idx, True)
    track = RPR.RPR_GetTrack(0, track_idx)
    RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # === Step 3: Add FX Chain (Rhodes Emulation) ===
    # 3.1 ReaSynth for the electric piano tone
    synth_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 0, 0.7)   # Volume
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 1, 0.0)   # Tuning
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 2, 0.0)   # Square mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 3, 0.0)   # Saw mix
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 4, 0.8)   # Triangle mix (Main Rhodes body)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 5, 0.3)   # Extra sine (Warmth)
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 6, 0.02)  # Soft Attack
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 7, 0.6)   # Decay
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 8, 0.4)   # Sustain
    RPR.RPR_TrackFX_SetParam(track, synth_idx, 9, 0.8)   # Long Release
    
    # 3.2 JS: Tremolo for Suitcase stereo panning vibe
    trem_idx = RPR.RPR_TrackFX_AddByName(track, "JS: Tremolo", False, -1)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 0, 2.5)    # Frequency (Hz)
    RPR.RPR_TrackFX_SetParam(track, trem_idx, 1, -12.0)  # Amount (dB)

    # 3.3 ReaVerbate for space
    verb_idx = RPR.RPR_TrackFX_AddByName(track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 0, 0.15)   # Wet
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 1, 1.0)    # Dry
    RPR.RPR_TrackFX_SetParam(track, verb_idx, 2, 0.5)    # Room Size

    # === Step 4: Music Theory & Voicing Setup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    tonic_pitch = NOTE_MAP.get(key.capitalize(), 0) + 36 # C2 Base octave
    
    # Define Progression based on scale (2-bar loop)
    progression = []
    if scale.lower() in ["major", "mixolydian", "pentatonic_major"]:
        # ii9 - V13 - Imaj9 - vi11
        progression = [
            {"root_offset": 2, "voicing": [0, 15, 19, 22, 26]},  # ii9
            {"root_offset": 7, "voicing": [0, 10, 16, 21, 26]},  # V13
            {"root_offset": 0, "voicing": [0, 14, 19, 23, 26]},  # Imaj9
            {"root_offset": 9, "voicing": [0, 15, 19, 22, 29]},  # vi11
        ]
    else:
        # Minor Context: i9 - iv9 - v7b9 - bVImaj9
        progression = [
            {"root_offset": 0, "voicing": [0, 15, 19, 22, 26]},  # i9
            {"root_offset": 5, "voicing": [0, 15, 19, 22, 26]},  # iv9
            {"root_offset": 7, "voicing": [0, 16, 19, 22, 25]},  # v7b9
            {"root_offset": 8, "voicing": [0, 14, 19, 23, 26]},  # bVImaj9
        ]

    # === Step 5: Create MIDI Item ===
    beats_per_bar = 4
    item_length_qn = bars * beats_per_bar
    item_length_sec = (60.0 / bpm) * item_length_qn
    
    item = RPR.RPR_CreateNewMIDIItemInProj(track, 0.0, item_length_sec, False)
    take = RPR.RPR_GetActiveTake(item)

    # === Step 6: Insert Syncopated Chord Events ===
    note_count = 0
    
    # Loop over the requested number of bars
    for bar in range(bars):
        qn_offset = bar * 4.0
        
        # Decide which two chords to play based on even/odd bar
        if bar % 2 == 0:
            chords_to_play = [
                (progression[0], qn_offset + 0.0, 2.25),  # Downbeat, holds into beat 3
                (progression[1], qn_offset + 2.5, 1.25)   # Pushed on "and" of 3
            ]
        else:
            chords_to_play = [
                (progression[2], qn_offset + 0.0, 2.25),
                (progression[3], qn_offset + 2.5, 1.25)
            ]
            
        for chord_data, start_qn, length_qn in chords_to_play:
            root_note = tonic_pitch + chord_data["root_offset"]
            
            # Insert each note in the chord stack
            for i, interval in enumerate(chord_data["voicing"]):
                pitch = root_note + interval
                if pitch > 127: pitch = 127
                
                # Humanize velocity (accents the top melody note slightly)
                vel_shift = random.randint(-12, 5)
                if i == len(chord_data["voicing"]) - 1:
                    vel_shift += 10 # Emphasize top extension
                vel = max(1, min(127, velocity_base + vel_shift))
                
                # Strum effect (15ms delay per note upward)
                strum_offset_qn = i * 0.02
                note_start_qn = start_qn + strum_offset_qn
                note_end_qn = note_start_qn + length_qn - 0.1 # Slight gap before next chord
                
                start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_start_qn)
                end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjQN(take, note_end_qn)
                
                RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, pitch, vel, True)
                note_count += 1

    RPR.RPR_MIDI_Sort(take)
    RPR.RPR_UpdateArrange()

    return f"Created '{track_name}' with {note_count} lush extended notes over {bars} bars at {bpm} BPM in {key} {scale}."
```