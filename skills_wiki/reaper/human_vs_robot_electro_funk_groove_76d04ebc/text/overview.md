# "Human vs. Robot" Electro-Funk Groove

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: "Human vs. Robot" Electro-Funk Groove

* **Core Musical Mechanism**: The signature aesthetic of Daft Punk's *Random Access Memories* is the juxtaposition of loose, expressive, unquantized human performances (live acoustic drums, funky bass, guitars) against rigid, perfectly quantized, static electronic sequences (drum machines, arpeggiators, vocoders). 
* **Why Use This Skill (Rationale)**: Musically, if everything is perfectly quantized, the track feels lifeless. If everything is unquantized, it can feel messy or lose its dancefloor drive. By strictly quantizing a 16th-note synthesizer pulse (the "Robot") while allowing the drum groove and syncopated bassline to slightly drift off the grid with dynamic velocities (the "Human"), psychoacoustics create a profound sense of "pocket" and groove. The rigid synth acts as an anchor, making the human swing feel even more expressive by contrast.
* **Overall Applicability**: Perfect for disco-house, electro-funk, synth-pop, and French house. This pattern is ideal for creating the foundational loop of a track that needs both emotional warmth and dancefloor energy.
* **Value Addition**: Compared to a standard step-sequenced MIDI clip, this skill structurally encodes *feel*. It uses math (randomized offsets in timing and velocity) to simulate a studio session player, while generating a classic 4-chord progression (i - VI - III - VII) to anchor the robotic synth.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  * **Tempo**: 100-120 BPM (classic disco/funk tempo).
  * **Human Elements (Drums & Bass)**: Programmed with a 16th-note grid but heavily "humanized." Velocities vary wildly (e.g., hi-hats emphasize the downbeats with lower velocities on the upbeats). Timing is shifted by +/- 5 to 15 milliseconds off the perfect grid. 
  * **Robot Elements (Synth/Vocoder)**: Strictly locked to the exact 16th-note grid with 0ms deviation and fixed, robotic velocities (e.g., 100 on every note) for mechanical precision.

* **Step B: Pitch & Harmony**
  * **Progression**: The classic Daft Punk i - VI - III - VII progression (e.g., Am, F, C, G). 
  * **Human Bass**: Plays a syncopated funk pattern strictly following the root of the chords, occasionally jumping an octave on the off-beat 16th notes.
  * **Robot Synth**: Plays continuous 16th-note pulsing triads. 

* **Step C: Sound Design & FX**
  * **Human Bass**: Emulated using ReaSynth with a warm square/saw blend, acting as an analog synth-bass or DI bass placeholder.
  * **Robot Synth**: Emulated using ReaSynth with a sawtooth wave, high sustain/release, and filtered via ReaEQ to create a warm, pulsing pad/arp.

* **Step D: Mix & Automation**
  * The "Human" tracks (Drums, Bass) are mixed slightly louder and given a wider dynamic range.
  * The "Robot" track is low-passed to sit behind the groove, providing harmonic context without drowning out the rhythm section.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| "Human vs Robot" Contrast | Algorithmic MIDI insertion | Allows us to literally separate programmatic logic: `random` offsets for the "Human" tracks, and strict mathematical grids for the "Robot" track. |
| Harmonic Progression | Scale/Chord math | Dynamically calculates the i-VI-III-VII progression in any key parameter passed to the script. |
| Sound Design | Native ReaSynth & ReaEQ | Ensures the code is 100% self-contained and executable in any vanilla REAPER session without requiring external VSTs or sampled audio. |

> **Feasibility Assessment**: 80% — The script successfully reproduces the rhythmic and harmonic interplay between rigid electronic sequencing and loose funky grooves. The missing 20% is the actual timbre of legendary session musicians (like Nile Rodgers' guitar or Omar Hakim's drums), which cannot be generated via code and requires real sample libraries. ReaSynth acts as an effective structural placeholder.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "RAM_Tribute",
    track_name: str = "ElectroFunk",
    bpm: int = 115,
    key: str = "A",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a "Human vs. Robot" Electro-Funk Groove in REAPER.
    
    Creates 3 tracks:
    1. Human Drums (Dynamic velocity, loose timing)
    2. Human Bass (Syncopated, loose timing, dynamic velocity)
    3. Robot Synth (100% quantized 16th-note chord pulse, fixed velocity)
    """
    import random
    import reaper_python as RPR

    # === Music Theory Lookup ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "dorian": [0, 2, 3, 5, 7, 9, 10]
    }
    
    # Fallback to minor if scale not found
    scale_intervals = SCALES.get(scale.lower(), SCALES["minor"])
    root_midi = 36 + NOTE_MAP.get(key.upper(), 9) # Default to A1 (45) for bass

    # Classic i - VI - III - VII progression (0-indexed scale degrees)
    # E.g. in A minor: A min, F maj, C maj, G maj
    progression_degrees = [0, 5, 2, 6] 

    def get_chord_notes(degree_idx, octave_offset=0):
        """Builds a basic triad from the scale degree."""
        root_val = scale_intervals[degree_idx % len(scale_intervals)]
        third_val = scale_intervals[(degree_idx + 2) % len(scale_intervals)]
        fifth_val = scale_intervals[(degree_idx + 4) % len(scale_intervals)]
        
        # Adjust for octave wrapping within the scale array
        if third_val < root_val: third_val += 12
        if fifth_val < root_val: fifth_val += 12
        
        base_pitch = root_midi + (octave_offset * 12)
        return [base_pitch + root_val, base_pitch + third_val, base_pitch + fifth_val]

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, True)
    quarter_len = 60.0 / bpm
    bar_len = quarter_len * 4

    def add_track_with_item(name, length_sec):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        track = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    def insert_midi(take, pos_sec, dur_sec, pitch, vel):
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, pos_sec + dur_sec)
        # Ensure velocity is within MIDI bounds
        vel = max(1, min(127, int(vel)))
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), vel, True)

    total_length = bar_len * bars

    # === Step 2: Human Drums (Loose, Dynamic) ===
    drum_track, drum_take = add_track_with_item(f"{track_name}_HumanDrums", total_length)
    
    for bar in range(bars):
        bar_start = bar * bar_len
        
        # Kick & Snare
        for beat in range(4):
            beat_time = bar_start + (beat * quarter_len)
            human_offset = random.uniform(-0.015, 0.015) # Loose timing
            vel_human = random.randint(-10, 10)
            
            if beat in [0, 2]: # Kick on 1 and 3
                insert_midi(drum_take, beat_time + human_offset, 0.1, 36, velocity_base + 10 + vel_human)
            else: # Snare on 2 and 4
                insert_midi(drum_take, beat_time + human_offset, 0.1, 38, velocity_base + vel_human)
                
            # Syncopated ghost kick right before beat 3
            if beat == 1:
                ghost_time = beat_time + (quarter_len * 0.75)
                insert_midi(drum_take, ghost_time + human_offset, 0.1, 36, velocity_base - 30)

        # Hi-hats (16th notes with strong dynamic groove)
        for i in range(16):
            hat_time = bar_start + (i * quarter_len / 4.0)
            human_offset = random.uniform(-0.01, 0.01)
            # Emphasize downbeats and off-beats differently
            if i % 4 == 0: hat_vel = velocity_base - 10   # On the beat
            elif i % 2 == 0: hat_vel = velocity_base - 20 # 8th note offbeat
            else: hat_vel = velocity_base - 40            # 16th note in-between
            
            hat_vel += random.randint(-5, 5)
            insert_midi(drum_take, hat_time + human_offset, 0.05, 42, hat_vel)

    RPR.RPR_MIDI_Sort(drum_take)

    # === Step 3: Human Bass (Syncopated, Loose) ===
    bass_track, bass_take = add_track_with_item(f"{track_name}_HumanBass", total_length)
    
    for bar in range(bars):
        bar_start = bar * bar_len
        # Get the root note of the current chord in the progression
        chord_root = get_chord_notes(progression_degrees[bar % len(progression_degrees)])[0]
        
        # Bass Rhythm Pattern: Beat 1 (Quarter), Beat 2.75 (16th syncopation, octave), Beat 3.5 (8th syncopation)
        bass_hits = [
            (0.0, 0.4, chord_root, 10),                 # Downbeat
            (1.75, 0.2, chord_root + 12, 5),            # Syncopated octave pop
            (2.5, 0.3, chord_root, -5),                 # Anticipate beat 3
            (3.0, 0.2, chord_root, 0)                   # Beat 4
        ]
        
        for pos_beats, dur_beats, pitch, vel_mod in bass_hits:
            hit_time = bar_start + (pos_beats * quarter_len)
            dur_time = dur_beats * quarter_len
            human_offset = random.uniform(-0.02, 0.01) # Bass tends to lay slightly back in the pocket
            insert_midi(bass_take, hit_time + human_offset, dur_time, pitch, velocity_base + vel_mod + random.randint(-10, 10))

    RPR.RPR_MIDI_Sort(bass_take)
    
    # Add a warm synth bass placeholder
    RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 1, 0.3) # Saw mix
    RPR.RPR_TrackFX_SetParam(bass_track, 0, 2, 0.7) # Square mix

    # === Step 4: Robot Synth (Perfect Grid, Static Velocity) ===
    synth_track, synth_take = add_track_with_item(f"{track_name}_RobotSynth", total_length)
    
    for bar in range(bars):
        bar_start = bar * bar_len
        chord_notes = get_chord_notes(progression_degrees[bar % len(progression_degrees)], octave_offset=1)
        
        # 16th note pulsing chords
        for i in range(16):
            pulse_time = bar_start + (i * quarter_len / 4.0)
            # ZERO human offset, PERFECT mathematical grid. Static velocity.
            for note in chord_notes:
                insert_midi(synth_take, pulse_time, (quarter_len / 4.0) * 0.8, note, velocity_base - 15)

    RPR.RPR_MIDI_Sort(synth_take)
    
    # Add a classic Daft Punk filtered synth pad/arp sound
    RPR.RPR_TrackFX_AddByName(synth_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 1, 1.0) # 100% Saw
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 2, 0.0) # 0% Square
    RPR.RPR_TrackFX_SetParam(synth_track, 0, 4, 0.2) # Short release
    
    # Filter it to sit in the background behind the human groove
    eq_idx = RPR.RPR_TrackFX_AddByName(synth_track, "ReaEQ", False, -1)
    # Band 4 is High Shelf by default, change to Low Pass to muffle the robot synth
    RPR.RPR_TrackFX_SetParam(synth_track, eq_idx, 12, 0.0) # Band 4 freq (low pass around 1000Hz)

    return f"Created Human vs Robot groove: '{track_name}' across 3 tracks, playing a {bars}-bar {key} {scale} sequence at {bpm} BPM."
```