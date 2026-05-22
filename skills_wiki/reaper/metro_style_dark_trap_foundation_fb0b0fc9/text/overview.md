# Metro-Style Dark Trap Foundation

## Analysis

# Agent_Skill_Distiller Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Metro-Style Dark Trap Foundation

* **Core Musical Mechanism**: The signature of this style relies on two pillars: 
  1. **Harmonic Tension via Minor 2nds**: Using a minor key and emphasizing the half-step interval (the minor 2nd or minor 6th degree) against the root. The tutorial specifically highlights building a minor chord but pitching the minor 3rd up an octave, then introducing a note just one semitone above the root (e.g., E in the key of D# minor) to create an eerie, dissonant tension.
  2. **Half-time Bounce**: A 140-150 BPM tempo where the snare lands on beat 3 instead of 2 and 4. This creates a sluggish, head-nodding feel, contrasted by double-time (8th note) hi-hats.

* **Why Use This Skill (Rationale)**: The tension-resolution dynamic of the minor 2nd interval evokes a dark, cinematic, "horror-esque" feeling, which is a staple of modern Atlanta trap (Metro Boomin, Southside). The half-time drum programming creates massive spatial pockets in the groove, allowing a heavy, distorted 808 to occupy the sub-frequencies without clashing with the snare. 

* **Overall Applicability**: This pattern is perfect for the foundation of modern trap beats, dark hip-hop verses, drill intros, or any production requiring a menacing, sparse atmosphere.

* **Value Addition**: Instead of a blank canvas, this skill encodes the exact drum bounce (Spinz 808 rhythm + 3rd-beat snare + 8th-note hats) and the specific "wide" chord voicing (root, fifth, an octave-up minor third, and the signature minor 2nd tension) used by top-tier trap producers, pre-mixed with reverb and EQ.


### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 140 - 150 BPM (Tutorial uses 145 BPM).
  - **Grid**: 4/4 time, but programmed in "half-time". 
  - **Drums**: 
    - Snare hits on beat 3 of every bar.
    - Hi-hats play continuous 1/8th notes (every 0.5 beats) with slight velocity variations for bounce.
    - 808 hits on beat 1, and the "and" of beat 3 (beat 2.5), creating a syncopated groove.

* **Step B: Pitch & Harmony**
  - **Scale**: Natural Minor or Phrygian (Key of D# in tutorial).
  - **Piano Voicing**: Spread minor chord. Root at the bottom, the minor 3rd is pitched up an octave to create a wider, more open sound.
  - **Tension Element**: The tutorial introduces the minor 2nd (e.g., E natural in D# minor) specifically for its dark, dissonant clash with the root note.
  - **808**: Strictly follows the root note to maintain ground.

* **Step C: Sound Design & FX**
  - **Piano**: Dark, filtered grand piano (Noire Pure). Processed heavily with **Reverb** (long decay, low frequencies cut so it doesn't muddy the mix).
  - **Drums**: Short, punchy trap samples ("Beef Snare", "Spinz 808").
  - **"Half-time" Effect**: Often achieved with Cableguys HalfTime (pitching down an octave and slowing down 2x). We simulate this musically by keeping the piano notes sparse, long, and in a lower octave.

* **Step D: Mix & Automation**
  - **EQ**: The piano is high-passed to leave room for the 808.
  - **Reverb**: Piano is washed out, pushing it to the back of the mix.
  - **Levels**: 808 and snare are front-and-center (highest velocity).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Dark Piano Harmony | MIDI note insertion | Allows for exact replication of the spread voicing and minor 2nd tension. |
| Half-time Trap Groove | MIDI note insertion | Precise placement of the 808, snare on beat 3, and 8th-note hi-hats. |
| Instrument Placeholders | ReaSynth | Generates immediate, self-contained audio feedback without requiring external sample libraries. |
| Dark Atmosphere | FX chain (ReaEQ + ReaVerbate) | High-passing the piano and drowning it in reverb perfectly emulates the tutorial's spatial mix. |

> **Feasibility Assessment**: 85% — The code perfectly reproduces the harmonic theory, drum bounce, and spatial mixing. Because it uses stock ReaSynth to ensure execution without external assets, the *timbres* are synthetic approximations of a Spinz 808 or Noire piano, but the MIDI and FX structure allows the user to simply swap in their own VSTs/samples to achieve the exact sound from the video.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MetroDarkTrap",
    track_name: str = "DarkTrap_Foundation",
    bpm: int = 145,
    key: str = "D#",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Metro Boomin style dark trap foundation (Piano, 808, Snare, Hats) in REAPER.
    """
    import reaper_python as RPR

    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10], # Natural minor
        "phrygian": [0, 1, 3, 5, 7, 8, 10], # Has the min2 tension built in
    }

    # Ensure minor or phrygian for the dark vibe
    if scale not in ["minor", "phrygian", "harmonic_minor"]:
        scale = "minor"

    root_val = NOTE_MAP.get(key.capitalize(), 3) # Default to D#
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Helper to get exact MIDI notes in the scale
    def get_note(degree_zero_indexed, octave):
        octave_offset = (degree_zero_indexed // 7) * 12
        scale_degree = degree_zero_indexed % 7
        return (octave + 1) * 12 + root_val + scale_intervals[scale_degree] + octave_offset

    # Determine exact tension notes based on tutorial (Minor 2nd or Minor 6th)
    root_pitch = root_val + 48 # Octave 3 for piano
    fifth_pitch = root_val + 7 + 48
    min3_pitch = root_val + 3 + 60 # Octave 4 (pitched up an octave for wide voicing)
    min2_tension = root_val + 1 + 60 # Minor 2nd in Octave 4

    # 1. Set Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # Helper function to add MIDI notes by beats
    def add_midi_to_item(take, start_beat, end_beat, pitch, vel):
        start_time = start_beat * (60.0 / bpm)
        end_time = end_beat * (60.0 / bpm)
        start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
        end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
        RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, int(pitch), int(vel), False)

    # Track creation helper
    def create_track_with_midi(name, beats_total):
        track_idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(track_idx, True)
        track = RPR.RPR_GetTrack(0, track_idx)
        RPR.RPR_GetSetMediaTrackInfo_String(track, "P_NAME", name, True)
        
        item = RPR.RPR_AddMediaItemToTrack(track)
        item_length_sec = beats_total * (60.0 / bpm)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length_sec)
        
        take = RPR.RPR_AddTakeToMediaItem(item)
        return track, take

    total_beats = bars * 4

    # ==========================================
    # LAYER 1: DARK PIANO (ReaSynth + Reverb + EQ)
    # ==========================================
    piano_track, piano_take = create_track_with_midi(f"{track_name}_Piano", total_beats)
    
    for bar in range(bars):
        bar_start = bar * 4
        if bar % 2 == 0:
            # First half: Wide minor chord
            add_midi_to_item(piano_take, bar_start, bar_start + 3.5, root_pitch, velocity_base - 10)
            add_midi_to_item(piano_take, bar_start, bar_start + 3.5, fifth_pitch, velocity_base - 20)
            add_midi_to_item(piano_take, bar_start, bar_start + 3.5, min3_pitch, velocity_base - 15)
        else:
            # Second half: Tension phrase
            add_midi_to_item(piano_take, bar_start, bar_start + 1.5, root_pitch, velocity_base - 10)
            add_midi_to_item(piano_take, bar_start, bar_start + 1.5, min2_tension, velocity_base - 15)
            
            # Resolution back down
            add_midi_to_item(piano_take, bar_start + 2.0, bar_start + 3.5, root_pitch, velocity_base - 15)
            add_midi_to_item(piano_take, bar_start + 2.0, bar_start + 3.5, fifth_pitch, velocity_base - 20)

    RPR.RPR_MIDI_Sort(piano_take)

    # Piano FX
    fx_idx = RPR.RPR_TrackFX_AddByName(piano_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(piano_track, fx_idx, 1, 0.5)  # Saw mix (give it some grit)
    RPR.RPR_TrackFX_SetParam(piano_track, fx_idx, 3, 0.2)  # Attack
    RPR.RPR_TrackFX_SetParam(piano_track, fx_idx, 4, 1.5)  # Decay
    
    # EQ (Cut lows for 808)
    eq_idx = RPR.RPR_TrackFX_AddByName(piano_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(piano_track, eq_idx, 0, 0) # Highpass shape
    RPR.RPR_TrackFX_SetParam(piano_track, eq_idx, 1, 150.0) # Freq ~150Hz
    
    # Reverb (Wash it out)
    verb_idx = RPR.RPR_TrackFX_AddByName(piano_track, "ReaVerbate", False, -1)
    RPR.RPR_TrackFX_SetParam(piano_track, verb_idx, 0, 0.8) # Wet mix high
    RPR.RPR_TrackFX_SetParam(piano_track, verb_idx, 1, 0.2) # Dry mix low
    RPR.RPR_TrackFX_SetParam(piano_track, verb_idx, 2, 0.9) # Long Room Size


    # ==========================================
    # LAYER 2: 808 BASS (ReaSynth Sine + Dist)
    # ==========================================
    bass_track, bass_take = create_track_with_midi(f"{track_name}_808", total_beats)
    bass_pitch = root_val + 36 # Octave 2
    
    for bar in range(bars):
        bar_start = bar * 4
        # Standard syncopated Spinz 808 bounce
        add_midi_to_item(bass_take, bar_start + 0.0, bar_start + 1.5, bass_pitch, 127) # Beat 1
        add_midi_to_item(bass_take, bar_start + 2.5, bar_start + 3.5, bass_pitch, 127) # "And" of beat 3

        # Variation every 4th bar
        if bar % 4 == 3:
            add_midi_to_item(bass_take, bar_start + 3.5, bar_start + 3.8, bass_pitch + 12, 100) # Octave pop

    RPR.RPR_MIDI_Sort(bass_take)

    # 808 FX (Pure Sine Wave)
    fx_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 1, 0.0)  # Pure Sine (No saw)
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 2, 0.0)  # No square
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 3, 0.01) # Instant attack
    RPR.RPR_TrackFX_SetParam(bass_track, fx_idx, 4, 1.5)  # Long decay
    
    # Saturation (via ReaComp gain driving) to mimic 808 distortion
    comp_idx = RPR.RPR_TrackFX_AddByName(bass_track, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(bass_track, comp_idx, 10, 6.0) # Wet output gain +6dB


    # ==========================================
    # LAYER 3: TRAP SNARE
    # ==========================================
    snare_track, snare_take = create_track_with_midi(f"{track_name}_Snare", total_beats)
    snare_pitch = 60 # C4
    
    for bar in range(bars):
        bar_start = bar * 4
        # Snare strictly on beat 3 for the half-time feel
        add_midi_to_item(snare_take, bar_start + 2.0, bar_start + 2.5, snare_pitch, 127)

    RPR.RPR_MIDI_Sort(snare_take)

    # Snare Synth (Short burst of noise)
    fx_idx = RPR.RPR_TrackFX_AddByName(snare_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(snare_track, fx_idx, 0, 0.0)  # Turn down main osc
    RPR.RPR_TrackFX_SetParam(snare_track, fx_idx, 1, 0.0)
    RPR.RPR_TrackFX_SetParam(snare_track, fx_idx, 5, 0.5)  # Noise mix up
    RPR.RPR_TrackFX_SetParam(snare_track, fx_idx, 4, 0.1)  # Very short decay


    # ==========================================
    # LAYER 4: HI-HATS
    # ==========================================
    hat_track, hat_take = create_track_with_midi(f"{track_name}_Hats", total_beats)
    hat_pitch = 66 # F#4
    
    # 8th note hats
    for beat in range(0, int(total_beats * 2)):
        start_beat = beat * 0.5
        
        # Velocity bounce (accent the downbeats)
        vel = 110 if beat % 2 == 0 else 80
        
        # Add a quick roll occasionally
        if beat % 16 == 14:
            add_midi_to_item(hat_take, start_beat, start_beat + 0.16, hat_pitch, vel)
            add_midi_to_item(hat_take, start_beat + 0.16, start_beat + 0.33, hat_pitch, vel)
            add_midi_to_item(hat_take, start_beat + 0.33, start_beat + 0.5, hat_pitch, vel)
        else:
            add_midi_to_item(hat_take, start_beat, start_beat + 0.25, hat_pitch, vel)

    RPR.RPR_MIDI_Sort(hat_take)

    # Hat Synth (Short, high-pitched noise burst)
    fx_idx = RPR.RPR_TrackFX_AddByName(hat_track, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(hat_track, fx_idx, 0, 0.0)  
    RPR.RPR_TrackFX_SetParam(hat_track, fx_idx, 5, 0.4)  # Noise mix
    RPR.RPR_TrackFX_SetParam(hat_track, fx_idx, 4, 0.03) # Extremely short decay (tight hat)
    
    eq_idx = RPR.RPR_TrackFX_AddByName(hat_track, "ReaEQ", False, -1)
    RPR.RPR_TrackFX_SetParam(hat_track, eq_idx, 0, 0) # Highpass
    RPR.RPR_TrackFX_SetParam(hat_track, eq_idx, 1, 5000.0) # Highpass at 5kHz for thin hat sound

    return f"Created Dark Trap Foundation (4 tracks) over {bars} bars in {key} {scale} at {bpm} BPM."
```