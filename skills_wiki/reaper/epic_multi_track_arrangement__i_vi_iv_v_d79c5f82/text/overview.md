### 1. High-level Design Pattern Extraction

> **Skill Name**: Epic Multi-Track Arrangement (i-VI-iv-V)

* **Core Musical Mechanism**: A multi-track arrangement built around a dramatic harmonic minor chord progression (`i - VI - iv - V` or `Bm - G - Em - F#`). It utilizes four distinct interlocking layers: a backbeat rock drum groove, driving 8th-note pulsing bass, sustained rhythm chords (pads/power chords), and a continuous 16th-note ascending/descending lead arpeggio. 
* **Why Use This Skill (Rationale)**: This arrangement template demonstrates the classic "wall of sound" approach used in rock, metal, synthwave, and trailer music. The use of a major `V` chord in a minor key creates a strong leading-tone resolution back to the tonic (`i`). By separating the frequency bands (low bass pulses, mid-range sustained chords, high-register fast arpeggios), the mix remains clear despite being incredibly dense and energetic. 
* **Overall Applicability**: This pattern is perfect for choruses, climaxes, and drops. It acts as a massive-sounding template that can be routed to virtual guitars, analog synths, or orchestral libraries.
* **Value Addition**: Instead of manually plotting out multi-track relationships, this skill programmatically aligns an entire 4-piece band. It computes chord voicings, arpeggiates them mathematically, aligns a drum groove, and natively colors the tracks in REAPER to support the "Color by Track" MIDI editor workflow highlighted in the tutorial.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 120 BPM, 4/4 Time Signature.
  * **Drums**: Standard heavy rock groove. Kick on 1, 2-and, 3-and, 4. Snare on 2 and 4. Hi-hat playing straight 8th notes. 
  * **Bass**: Continuous, driving 8th notes (0.5 beats) playing slightly staccato for a kinetic, pumping feel.
  * **Rhythm**: Sustained whole notes (4 beats) anchoring the harmony.
  * **Lead**: Continuous 16th-note arpeggios (0.25 beats) sweeping up and down the chord tones.

* **Step B: Pitch & Harmony**
  * **Key/Scale**: B minor (default), utilizing the Harmonic Minor pivot.
  * **Progression**: `i` (B minor), `VI` (G major), `iv` (E minor), `V` (F# major). 
  * **Voicings**: The bass plays the root in Octave 1/2. The rhythm track plays closed triads in Octave 3/4. The lead arpeggiates Root-3rd-5th-Octave-5th-3rd in Octave 4/5.

* **Step C: Sound Design & FX**
  * **Stock REAPER Placeholders**: Since third-party VSTs (like Shreddage or GGD) are not guaranteed, the skill loads native `ReaSynth` on the tonal tracks.
  * **Bass**: ReaSynth tuned down, square wave mix for a gritty synth-bass tone.
  * **Lead**: ReaSynth with a fast decay and saw wave to approximate a plucked/arpeggiated guitar or synth.

* **Step D: Mix & Automation**
  * Tracks are distinctly colored (Purple, Pink, Orange, Cyan) so that when viewed together in REAPER's single MIDI editor (with "Color Notes by Track" enabled), the producer can easily visualize how the arpeggios weave through the sustained chords.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Creation & Coloring | `RPR_InsertTrackAtIndex`, `RPR_SetTrackColor` | Sets up the multi-track environment exactly as visually shown in the workflow tutorial. |
| Drum, Bass, Rhythm, Lead Notes | `RPR_MIDI_InsertNote` | Provides exact control over rhythm, velocity, and pitch calculation for all 4 interlocking parts. |
| Sound Design | `RPR_TrackFX_AddByName` (ReaSynth) | Ensures the generated MIDI is instantly audible using only stock REAPER plugins. |

> **Feasibility Assessment**: 100% reproducible for the musical composition, MIDI layout, and track coloring. The specific Shreddage/GGD sample libraries used in the video are replaced with REAPER's native `ReaSynth` to ensure safe, self-contained execution.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Epic Rock",
    bpm: int = 120,
    key: str = "B",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Creates an epic 4-track arrangement (Drums, Bass, Rhythm, Lead) demonstrating 
    multi-track MIDI workflows with an interlocking i-VI-iv-V progression.
    """
    import reaper_python as RPR

    # Note mapping
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    root_val = NOTE_MAP.get(key.capitalize(), 11) # Default to B

    # Define the progression relative to root
    if scale.lower() == "major":
        # I - IV - ii - V
        progression = [(0, "maj"), (5, "maj"), (2, "min"), (7, "maj")]
    else:
        # i - VI - iv - V (Harmonic minor dominant)
        progression = [(0, "min"), (8, "maj"), (5, "min"), (7, "maj")]

    def get_chord_notes(root_note, ctype):
        if ctype == "maj":
            return [root_note, root_note + 4, root_note + 7]
        else: # min
            return [root_note, root_note + 3, root_note + 7]

    def rgb_to_native(r, g, b):
        return r | (g << 8) | (b << 16) | 0x1000000

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    
    beats_per_bar = 4
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * beats_per_bar
    item_length = bar_sec * bars

    track_setup = [
        {"name": f"{track_name} Drums", "color": rgb_to_native(128, 0, 255), "synth": False},
        {"name": f"{track_name} Bass", "color": rgb_to_native(255, 0, 128), "synth": True},
        {"name": f"{track_name} Rhythm", "color": rgb_to_native(255, 128, 0), "synth": True},
        {"name": f"{track_name} Lead", "color": rgb_to_native(0, 255, 255), "synth": True}
    ]

    takes = []

    # Create Tracks & Items
    start_idx = RPR.RPR_CountTracks(0)
    for i, t in enumerate(track_setup):
        idx = start_idx + i
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", t["name"], True)
        RPR.RPR_SetTrackColor(track, t["color"])
        
        # Add basic synth to tonal tracks so they make sound
        if t["synth"]:
            fx_idx = RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
            # Tweak ReaSynth volume to avoid clipping (-12dB approx)
            RPR.RPR_TrackFX_SetParam(track, fx_idx, 0, 0.25)
            
            # If Bass, mix in square wave
            if "Bass" in t["name"]:
                RPR.RPR_TrackFX_SetParam(track, fx_idx, 1, 0.5) # Square mix

        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
        take = RPR.RPR_AddTakeToMediaItem(item)
        takes.append(take)

    take_drums, take_bass, take_rhythm, take_lead = takes

    # Helper for MIDI insertion
    def insert_note(take, start_beat, duration_beats, pitch, vel):
        start_time = start_beat * beat_sec
        end_time = (start_beat + duration_beats) * beat_sec
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), True)

    # Populate MIDI Data
    for b in range(bars):
        chord_rel, ctype = progression[b % len(progression)]
        chord_root_pitch = root_val + chord_rel
        
        # 1. DRUMS (General MIDI Mapping: 36=Kick, 38=Snare, 42=HiHat)
        for beat in range(8): # 8th notes
            beat_pos = (b * 4) + (beat * 0.5)
            # Hi-hats every 8th note
            insert_note(take_drums, beat_pos, 0.25, 42, velocity_base - 10)
            
            # Snare on 2 and 4 (beat indices 2 and 6)
            if beat == 2 or beat == 6:
                insert_note(take_drums, beat_pos, 0.25, 38, velocity_base)
                
            # Kick pattern: beats 1, 2-and, 3-and, 4
            if beat in [0, 3, 5, 6]:
                insert_note(take_drums, beat_pos, 0.25, 36, velocity_base + 10)

        # 2. BASS (Driving 8th notes)
        bass_pitch = chord_root_pitch + 24 # Octave 1/2
        for beat in range(8):
            beat_pos = (b * 4) + (beat * 0.5)
            # Slight staccato duration (0.4 beats instead of 0.5)
            insert_note(take_bass, beat_pos, 0.4, bass_pitch, velocity_base)

        # 3. RHYTHM (Sustained Chords)
        rhythm_notes = get_chord_notes(chord_root_pitch + 48, ctype) # Octave 3/4
        for pitch in rhythm_notes:
            insert_note(take_rhythm, b * 4, 4.0, pitch, velocity_base - 20)

        # 4. LEAD (16th Note Arpeggio)
        lead_chord = get_chord_notes(chord_root_pitch + 60, ctype) # Octave 4/5
        arp_pattern = [
            lead_chord[0], lead_chord[1], lead_chord[2], lead_chord[0] + 12,
            lead_chord[2], lead_chord[1], lead_chord[0], lead_chord[2] - 12
        ]
        
        for step in range(16): # 16th notes
            beat_pos = (b * 4) + (step * 0.25)
            arp_pitch = arp_pattern[step % len(arp_pattern)]
            insert_note(take_lead, beat_pos, 0.2, arp_pitch, velocity_base)

    # Sort MIDI events for all takes
    for take in takes:
        RPR.RPR_MIDI_Sort(take)

    return f"Created 4-track Epic {key} {scale} Arrangement (Drums, Bass, Rhythm, Lead) over {bars} bars at {bpm} BPM."
```