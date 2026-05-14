# Neo-Jazz Groove & "The Lick"

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neo-Jazz Groove & "The Lick"

* **Core Musical Mechanism**: This pattern outlines a classic 2-bar minor jazz/funk vamp (Im9 to IV13). It relies on three interdependent layers: 
  1. A walking/syncopated bassline that anticipates chord changes by hitting the root on the "and" of 4.
  2. Comping chords that deliberately "avoid the 1" (downbeat) to create a syncopated, swinging groove, using advanced jazz tensions (9ths and 13ths) with smooth voice leading.
  3. A melodic improvisation layer utilizing the blues scale, always culminating in the famous jazz motif known as "The Lick" (1-2-b3-4-2-b7-1) to create a sense of harmonic resolution.

* **Why Use This Skill (Rationale)**: 
  * *Syncopation & Groove*: By placing the chords exclusively on the upbeats (the "and" of the beat) and anticipating the bass movement, you create forward momentum (swing).
  * *Voice Leading*: Moving from a minor 9th (e.g., C-Eb-G-Bb-D) to a dominant 13th (F-Eb-G-A-D) requires only one note to change (Bb moves to A). This minimal finger movement creates a highly professional, cohesive harmonic bed.
  * *Tension/Resolution*: "The Lick" is a culturally universally recognized jazz motif that naturally resolves a minor pentatonic/blues run back to the tonic.

* **Overall Applicability**: Perfect for neo-soul, lofi hip-hop, jazz-hop, or electric piano (Rhodes/Wurlitzer) interludes. It serves as a fantastic foundation for a track's verse or a playful bridge/solo section.

* **Value Addition**: Transforms a basic chord progression into an authentic jazz arrangement by applying specific off-beat rhythmic grids, advanced chord voicing (tensions), and genre-accurate melodic phrasing.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 100-115 BPM.
  * **Grid**: 1/8th note grid with an inherent swing feel.
  * **Bass**: Plays quarter notes on beats 1, 2, 3, and an 8th-note anticipation on the "and" of 4 (beat 4.5).
  * **Chords**: Plays 8th notes on the upbeats (beats 1.5, 2.5, 3.5), strictly avoiding beat 1.
  * **Solo**: A mix of 8th and quarter notes. "The Lick" plays perfectly across a single bar: four 8th notes, one quarter note, one 8th note, resolving to a tied quarter/half note.

* **Step B: Pitch & Harmony**
  * **Progression**: Im9 → IV13 (e.g., Cmin9 to F13). This is the quintessential Dorian mode vamp.
  * **Voicings** (Relative to tonic): 
    * Im9: b3, 5, b7, 9 (Root played by bass)
    * IV13: b3, 5, 6(13), 9 (Root played by bass). Note how the b7 of the Im9 drops a half-step to become the 3 of the IV chord.
  * **Solo (The Lick)**: 1, 2, b3, 4, 2, b7 (octave down), 1.

* **Step C: Sound Design & FX**
  * **Instrument**: Standard synthesizer (ReaSynth) mapped across three discrete frequency bands (Bass, Mid/Chords, High/Solo).
  * **Mix**: The bass is kept mono and centered. The chords are slightly lowered in volume to act as a bed. The solo is kept prominent.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Multi-part Arrangement | `RPR_InsertTrackAtIndex` | Separates Bass, Chords, and Solo into distinct, mixable layers mimicking the left/right hand separation. |
| Syncopation & The Lick | `RPR_MIDI_InsertNote` | Provides exact PPQ-level control to place chords on the off-beats and sequence "The Lick" accurately. |
| Jazz Voicing Math | Python logic (`NOTE_MAP` offsets) | Dynamically computes 9th and 13th chord intervals based on any user-provided key. |
| Instrument setup | `RPR_TrackFX_AddByName` | Adds ReaSynth to immediately hear the harmonic relationships without requiring external VSTs. |

**Feasibility Assessment**: 100% reproducible. The script perfectly captures the rhythmic syncopation, the specific jazz chord tensions (9ths and 13ths), and the precise melodic phrasing of "The Lick" outlined in the tutorial. 

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "JazzJam",
    track_name: str = "Jazz_Vamp",
    bpm: int = 110,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Neo-Jazz groove featuring off-beat 9th/13th chords, a syncopated bass, 
    and a solo ending in "The Lick" in the current REAPER project.
    """
    import reaper_python as RPR

    # Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Music theory map
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    # Ensure bars is even, as the pattern is a 2-bar loop
    if bars < 2: bars = 2
    bars = bars - (bars % 2) 

    base_note = NOTE_MAP.get(key.upper(), 0) + 48 # e.g., C3 = 48

    # Helper function to add MIDI notes based on beat timings
    def add_midi_note(take, beat_start, beat_len, pitch, vel):
        sec_start = beat_start * (60.0 / bpm)
        sec_end = (beat_start + beat_len) * (60.0 / bpm)
        ppq_start = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, sec_start)
        ppq_end = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, sec_end)
        RPR.RPR_MIDI_InsertNote(take, False, False, ppq_start, ppq_end, 0, int(pitch), int(vel), False)

    # Helper to create a track and item
    def create_layer(name, vol, pan):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_VOL", vol)
        RPR.RPR_SetMediaTrackInfo_Value(track, "D_PAN", pan)
        
        # Add simple synth
        RPR.RPR_TrackFX_AddByName(track, "ReaSynth", False, -1)
        
        beats_per_bar = 4
        bar_length_sec = (60.0 / bpm) * beats_per_bar
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", bar_length_sec * bars)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take, item

    # Create the 3 layers
    take_bass, _ = create_layer(f"{track_name}_Bass", 0.8, 0.0)
    take_chords, _ = create_layer(f"{track_name}_Chords", 0.5, -0.2)
    take_lead, _ = create_layer(f"{track_name}_Solo", 0.9, 0.2)

    bass_vel = velocity_base
    chord_vel = int(velocity_base * 0.8)
    lead_vel = int(velocity_base * 1.1)

    # Loop through the bars 2 at a time
    for i in range(0, bars, 2):
        b_offset = i * 4.0 # Beats offset for the current 2-bar loop

        # --- TRACK 1: BASS ---
        # Bar 1: I chord (root)
        add_midi_note(take_bass, b_offset + 0.0, 1.0, base_note - 12, bass_vel)
        add_midi_note(take_bass, b_offset + 1.0, 1.0, base_note - 12, bass_vel)
        add_midi_note(take_bass, b_offset + 2.0, 1.0, base_note - 12, bass_vel)
        # Anticipation into IV chord
        add_midi_note(take_bass, b_offset + 3.5, 0.5, base_note - 7, bass_vel + 10) 
        
        # Bar 2: IV chord (4th degree)
        add_midi_note(take_bass, b_offset + 4.0, 1.0, base_note - 7, bass_vel)
        add_midi_note(take_bass, b_offset + 5.0, 1.0, base_note - 7, bass_vel)
        add_midi_note(take_bass, b_offset + 6.0, 1.0, base_note - 7, bass_vel)
        # Anticipation into I chord
        add_midi_note(take_bass, b_offset + 7.5, 0.5, base_note - 12, bass_vel + 10)


        # --- TRACK 2: CHORDS (Syncopated, avoiding the 1) ---
        # Im9 Voicing: b3, 5, b7, 9 -> [3, 7, 10, 14] relative to root
        im9_voicing = [base_note + 3, base_note + 7, base_note + 10, base_note + 14]
        for beat in [0.5, 1.5, 2.5]: # Off-beats
            for pitch in im9_voicing:
                add_midi_note(take_chords, b_offset + beat, 0.5, pitch, chord_vel)
        
        # IV13 Voicing: b3, 5, 13, 9 -> [3, 7, 9, 14] relative to root. Smooth voice leading!
        iv13_voicing = [base_note + 3, base_note + 7, base_note + 9, base_note + 14]
        for beat in [4.5, 5.5, 6.5]: # Off-beats
            for pitch in iv13_voicing:
                add_midi_note(take_chords, b_offset + beat, 0.5, pitch, chord_vel)


        # --- TRACK 3: SOLO ("Make cool shit up" + "The Lick") ---
        # Bar 1: Blues/Pentatonic descending riff
        add_midi_note(take_lead, b_offset + 0.0, 0.5, base_note + 15, lead_vel) # b3 (octave up)
        add_midi_note(take_lead, b_offset + 0.5, 0.5, base_note + 14, lead_vel) # 2 (octave up)
        add_midi_note(take_lead, b_offset + 1.0, 0.5, base_note + 12, lead_vel) # 1 (octave up)
        add_midi_note(take_lead, b_offset + 1.5, 0.5, base_note + 10, lead_vel) # b7
        add_midi_note(take_lead, b_offset + 2.0, 1.0, base_note + 7,  lead_vel) # 5

        # Bar 2: "The Lick" (1, 2, b3, 4, 2, b7, 1)
        add_midi_note(take_lead, b_offset + 4.0, 0.5, base_note + 12, lead_vel) # 1
        add_midi_note(take_lead, b_offset + 4.5, 0.5, base_note + 14, lead_vel) # 2
        add_midi_note(take_lead, b_offset + 5.0, 0.5, base_note + 15, lead_vel) # b3
        add_midi_note(take_lead, b_offset + 5.5, 0.5, base_note + 17, lead_vel) # 4
        add_midi_note(take_lead, b_offset + 6.0, 1.0, base_note + 14, lead_vel) # 2 (quarter)
        add_midi_note(take_lead, b_offset + 7.0, 0.5, base_note + 10, lead_vel) # b7 (lower)
        add_midi_note(take_lead, b_offset + 7.5, 1.5, base_note + 12, lead_vel) # 1 (resolving, tied)

    # Trigger MIDI sorts
    RPR.RPR_MIDI_Sort(take_bass)
    RPR.RPR_MIDI_Sort(take_chords)
    RPR.RPR_MIDI_Sort(take_lead)

    return f"Created Jazzy Vamp in {key} {scale} across 3 tracks (Bass, Chords, Solo) for {bars} bars at {bpm} BPM."
```