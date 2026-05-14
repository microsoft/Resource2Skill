### 1. High-level Design Pattern Extraction

> **Skill Name**: Alt-Rock / Pop-Punk Anthem Groove (vi-IV-I-V)

* **Core Musical Mechanism**: This pattern is defined by the ubiquitous "heroic" vi-IV-I-V chord progression (demonstrated in the video as Bm - G - D - A) paired with a driving, motorik rhythm section. The signature of this technique is the rhythmic contrast: sustained, wide power chords in the rhythm guitar, a relentlessly pulsating 8th-note root-pedal bassline, and a rock backbeat with constant 8th-note hi-hats. 
* **Why Use This Skill (Rationale)**: The vi-IV-I-V progression works universally because it balances emotional tension and resolution perfectly. Starting on the relative minor (vi) establishes a slightly melancholic or urgent tone, moving to the subdominant (IV) creates an uplifting swell, the tonic (I) provides a triumphant arrival, and the dominant (V) creates the dominant-to-minor (V-vi) deceptive cadence that seamlessly loops the progression back around. The 8th-note bassline glues the groove together by establishing a fast, forward-moving pulse (often quantized completely straight to grid) underneath the slower-moving chords.
* **Overall Applicability**: This is a foundational block for modern rock, pop-punk, synth-wave, and even high-energy electronic music (like melodic dubstep or trance). It excels in choruses, intros, and climaxes where high energy and emotional weight are required simultaneously. 
* **Value Addition**: Compared to a blank MIDI clip, this skill immediately provides a structurally complete, mixed-ensemble arrangement (Drums, Bass, Guitar) locked into a synchronized, emotionally impactful rock groove. 

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Time Signature & BPM**: 4/4 time. Works best in the 140–170 BPM range (typical for high-energy rock/pop-punk). 
  - **Grid**: Strict 1/8th note grid. No swing; the genre relies on straight, driving mechanics.
  - **Drums**: Kick on 1, 2-and, 3. Snare on 2 and 4. Hi-hats on every 8th note. Crash on the downbeat of the 1st bar.
  - **Bass**: Continuous 8th notes, tightly snapped to the grid, full legato (or slight staccato depending on the intended aggression).

* **Step B: Pitch & Harmony**
  - **Key/Scale**: D Major (or B Natural Minor). 
  - **Progression**: vi - IV - I - V (B minor, G Major, D Major, A Major).
  - **Guitar Voicings**: Block chords/power chords sustaining for an entire bar. 
  - **Bass**: Plays the root note of the chord exclusively in the 1st or 2nd octave to stay out of the guitars' frequency range.

* **Step C: Sound Design & FX**
  - **Drums**: A punchy, acoustic drum kit sample (General MIDI mapping used: Kick 36, Snare 38, Hat 42, Crash 49).
  - **Bass**: Usually a DI bass or a distorted synth bass (sub-heavy). 
  - **Guitar**: High-gain rhythm guitars. In the MIDI domain, this is represented by wide triad or power-chord voicings.

* **Step D: Mix & Automation**
  - All MIDI is drawn precisely on the grid. Velocities are kept uniformly high (100-115) to emulate the "hard-hitting" playing style typical of the genre.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Track Routing & Setup | `RPR_InsertTrackAtIndex`, `RPR_AddMediaItemToTrack` | Allows us to safely build a multi-instrument ensemble (Drums, Bass, Chords) without overwriting the user's project. |
| Harmonic/Rhythmic Logic | Programmatic scale degree calculations & loops | Computes exact pitches for the vi-IV-I-V progression dynamically regardless of the user's chosen root key. |
| Note Generation | `RPR_MIDI_InsertNote` | Provides the exact control over timing, velocity, and pitch required for the tight 8th-note bassline and drum backbeat. |

> **Feasibility Assessment**: 100% reproducible. The script perfectly reproduces the MIDI arrangement, rhythmic groove, and harmonic structure demonstrated in the tutorial. The user will simply need to assign their favorite virtual instruments (e.g., Kontakt, drums, synths) to the generated tracks.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "AltRock_Anthem",
    track_name: str = "PopPunk_Groove",
    bpm: int = 150,
    key: str = "D",
    scale: str = "major",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Creates a multi-track Alt-Rock/Pop-Punk Anthem Groove (vi-IV-I-V progression)
    complete with 8th-note driving bass, sustained chords, and a rock drum beat.

    Args:
        project_name: Project identifier.
        track_name: Base name for the generated tracks.
        bpm: Tempo in BPM (140-170 recommended).
        key: Root note (e.g., "D", "C#").
        scale: Scale type (defaults to major).
        bars: Number of bars to generate (should be a multiple of 4).
        velocity_base: Base MIDI velocity (0-127).

    Returns:
        Status string.
    """
    import reaper_python as RPR

    # === Music Theory & Lookup Tables ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10]
    }

    if scale not in SCALES:
        scale = "major"
    
    base_pitch = NOTE_MAP.get(key.capitalize(), 2) # Default to D if invalid
    scale_intervals = SCALES[scale]
    
    # Progression: vi - IV - I - V (mapped to 0-indexed scale degrees)
    # In major: vi=5, IV=3, I=0, V=4
    # In minor: i=0, VI=5, III=2, VII=6
    if scale == "major":
        progression = [5, 3, 0, 4] 
    else:
        progression = [0, 5, 2, 6]

    def get_pitch(degree, octave):
        """Calculates exact MIDI pitch given a scale degree and octave."""
        norm_degree = degree % 7
        octave_offset = degree // 7
        return base_pitch + scale_intervals[norm_degree] + 12 * (octave + octave_offset + 1)

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    def create_midi_track(name):
        """Helper to create a track and an empty MIDI item/take spanning the loop length."""
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", total_length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return take

    def insert_note(take, start_time, end_time, pitch, velocity):
        """Helper to convert seconds to PPQ and insert a MIDI note."""
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(velocity), "")

    RPR.RPR_Undo_BeginBlock2(0)

    # === Step 2: Create Drums ===
    drum_take = create_midi_track(f"{track_name}_Drums")
    beat_sec = 60.0 / bpm
    half_beat_sec = beat_sec / 2.0

    for bar in range(bars):
        bar_start = bar * bar_length_sec
        
        # Crash on downbeat of first bar, otherwise hats
        if bar == 0:
            insert_note(drum_take, bar_start, bar_start + half_beat_sec, 49, velocity_base) # Crash
        
        for beat in range(4):
            beat_start = bar_start + (beat * beat_sec)
            
            # 8th note Hi-Hats
            insert_note(drum_take, beat_start, beat_start + half_beat_sec * 0.9, 42, velocity_base - 10)
            insert_note(drum_take, beat_start + half_beat_sec, beat_start + beat_sec * 0.9, 42, velocity_base - 20)
            
            # Kick on 1, 2-and, 3
            if beat == 0 or beat == 2:
                insert_note(drum_take, beat_start, beat_start + half_beat_sec, 36, velocity_base)
            if beat == 1: # The 'and' of 2
                insert_note(drum_take, beat_start + half_beat_sec, beat_start + beat_sec, 36, velocity_base - 5)
            
            # Snare on 2 and 4
            if beat == 1 or beat == 3:
                insert_note(drum_take, beat_start, beat_start + half_beat_sec, 38, velocity_base)

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Create Driving Bass ===
    bass_take = create_midi_track(f"{track_name}_Bass")
    for bar in range(bars):
        bar_start = bar * bar_length_sec
        chord_degree = progression[bar % len(progression)]
        bass_pitch = get_pitch(chord_degree, 1) # Octave 1
        
        # Continuous 8th notes
        for eighth in range(8):
            note_start = bar_start + (eighth * half_beat_sec)
            # Slight gap to make it pulsate
            note_end = note_start + (half_beat_sec * 0.95)
            # Alternate picking velocity emphasis
            vel = velocity_base if eighth % 2 == 0 else velocity_base - 15
            insert_note(bass_take, note_start, note_end, bass_pitch, vel)

    RPR.RPR_MIDI_Sort(bass_take)

    # === Step 4: Create Rhythm Guitars/Chords ===
    chord_take = create_midi_track(f"{track_name}_Chords")
    for bar in range(bars):
        bar_start = bar * bar_length_sec
        chord_degree = progression[bar % len(progression)]
        
        # Build triad (root, third, fifth)
        root = get_pitch(chord_degree, 3)     # Octave 3
        third = get_pitch(chord_degree + 2, 3) 
        fifth = get_pitch(chord_degree + 4, 3) 
        octave = get_pitch(chord_degree + 7, 3) # Add the octave for a wider "power" sound
        
        # Sustained for the entire bar with a tiny gap at the end
        note_end = bar_start + bar_length_sec * 0.98
        
        insert_note(chord_take, bar_start, note_end, root, velocity_base)
        insert_note(chord_take, bar_start, note_end, third, velocity_base - 10)
        insert_note(chord_take, bar_start, note_end, fifth, velocity_base - 10)
        insert_note(chord_take, bar_start, note_end, octave, velocity_base - 5)

    RPR.RPR_MIDI_Sort(chord_take)

    RPR.RPR_Undo_EndBlock2(0, "Create Alt-Rock Anthem Groove", -1)

    return f"Created 3 Tracks (Drums, Bass, Chords) over {bars} bars in {key} {scale} at {bpm} BPM."
```