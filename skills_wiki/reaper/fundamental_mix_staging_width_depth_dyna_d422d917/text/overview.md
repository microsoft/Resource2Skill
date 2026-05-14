# Fundamental Mix Staging (Width, Depth & Dynamics)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Fundamental Mix Staging (Width, Depth & Dynamics)

* **Core Musical Mechanism**: The pattern establishes a structured mixing foundation by assigning spatial and dynamic roles to different instruments. It achieves **width** by hard-panning complementary midrange elements (Guitar and Kalimba) to opposite sides (Left/Right). It achieves **depth** by sending specific tracks (Electric Piano) to a shared Reverb return bus rather than applying reverb directly to the channel. It achieves **dynamic control** by compressing the lead vocal and tucking the backup/octave vocal under it via volume attenuation. Finally, it uses **top-down shaping** by applying an EQ to the entire Mix Bus.
* **Why Use This Skill (Rationale)**: 
    * *Width (Panning)*: Panning instruments away from the center clears up the "phantom center" for the most important elements (Vocals, Kick, Snare, Bass). 
    * *Depth (Aux/Send Reverb)*: Using a shared reverb bus glues multiple instruments into the same simulated acoustic space, saves CPU, and allows independent EQ/processing of the reverb tail.
    * *Dynamics (Compression)*: A vocal track naturally fluctuates in volume. Compression "squeezes" the dynamic range, making the quiet parts louder and the loud parts quieter, ensuring the vocal sits consistently on top of the mix.
* **Overall Applicability**: This is the universal starting point for mixing almost any modern genre (Pop, Rock, Hip-Hop, EDM). Whenever a session feels "cluttered," "muddy," or "flat," applying this exact staging (panning out the clutter, routing time-based FX to busses, compressing the lead, and EQing the master) is the necessary first step.
* **Value Addition**: Instead of just inserting raw tracks, this skill encodes the *architecture* of a mix. It provides a pre-routed, spatially balanced template where elements are already sitting in their correct mix pockets.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120 BPM (Standard pop/rock tempo as a placeholder).
  - **Rhythm**: Basic sustained chords and rhythmic plucks to demonstrate the spatial separation without crowding the arrangement.
* **Step B: Pitch & Harmony**
  - **Key/Scale**: C Minor (C, D, Eb, F, G, Ab, Bb).
  - The arrangement separates frequency ranges: 
    - Vocals (Main & Octave) hold the center focus.
    - Electric Piano provides the midrange harmonic bed.
    - Kalimba and Guitar play complementary rhythmic/arpeggiated lines on the sides.
* **Step C: Sound Design & FX**
  - **Mix Bus (Folder Parent)**: Houses a **ReaEQ** for overall track tonal shaping.
  - **Lead Vocal**: Contains **ReaComp** to control dynamics.
  - **Reverb Bus**: Contains **ReaVerbate** set to 100% wet, receiving audio from the Electric Piano.
  - All sound sources are simulated using stock **ReaSynth** instances so the script remains 100% self-contained and reproducible without external audio files.
* **Step D: Mix & Automation (if applicable)**
  - **Kalimba**: Panned 100% Right (+1.0).
  - **Guitar**: Panned 100% Left (-1.0).
  - **Vocal Octave**: Volume attenuated to 50% (-6dB) so it doesn't compete with the lead.
  - **Electric Piano Send**: Routed to the Reverb Bus with a send level of ~50%.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Mix Staging & Panning | Track creation & `RPR_SetMediaTrackInfo_Value()` | Allows programmatic setup of volume faders, panning (-1.0 to 1.0), and folder hierarchies. |
| Reverb Bus Routing | `RPR_CreateTrackSend()` | Exactly replicates the tutorial's technique of sending an instrument (Electric Piano) to an Aux Reverb track. |
| Plugin Instantiation | `RPR_TrackFX_AddByName()` | Adds ReaComp (Vocals), ReaEQ (Mix Bus), and ReaVerbate (Reverb Return). |
| Audio Source Generation | MIDI items + ReaSynth | Since external audio cannot be guaranteed, this generates placeholder musical parts so the user can actually hit "Play" and hear the mixing techniques in action. |

> **Feasibility Assessment**: 100% of the *mixing concepts* (Panning, Volume, Aux Sends, Mix Bus EQ, Track Compression) are reproduced. The specific audio recordings of the tutorial's musicians are simulated with ReaSynth to ensure execution safety.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "Basic Mix Staging",
    track_name: str = "Mix Bus",
    bpm: int = 120,
    key: str = "C",
    scale: str = "minor",
    bars: int = 4,
    velocity_base: int = 100,
    **kwargs,
) -> str:
    """
    Create a Fundamental Mix Staging setup in REAPER based on the Pro Tools tutorial.
    This creates a Mix Bus folder containing panned instruments, a compressed vocal, 
    and a Reverb send/return architecture.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major":            [0, 2, 4, 5, 7, 9, 11],
        "minor":            [0, 2, 3, 5, 7, 8, 10]
    }

    # Setup core musical variables
    root_val = NOTE_MAP.get(key, 0)
    scale_intervals = SCALES.get(scale, SCALES["minor"])
    
    # Helpers for note generation
    def get_note(degree, octave=4):
        deg = degree % len(scale_intervals)
        oct_shift = degree // len(scale_intervals)
        return root_val + scale_intervals[deg] + ((octave + oct_shift) * 12)

    # Initialize Project Tempo
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    start_track_idx = RPR.RPR_CountTracks(0)
    
    # --- Helper to create a track with synth and MIDI ---
    def create_instrument_track(name, index, vol=1.0, pan=0.0):
        RPR.RPR_InsertTrackAtIndex(index, True)
        trk = RPR.RPR_GetTrack(0, index)
        RPR.RPR_GetSetMediaTrackInfo_String(trk, "P_NAME", name, True)
        
        # Apply Mix Settings
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_VOL", vol)
        RPR.RPR_SetMediaTrackInfo_Value(trk, "D_PAN", pan)
        
        # Add a basic synth so it produces sound
        RPR.RPR_TrackFX_AddByName(trk, "ReaSynth", False, -1)
        # Turn down ReaSynth volume to avoid blowing out speakers
        RPR.RPR_TrackFX_SetParam(trk, 0, 0, 0.1) 
        
        return trk

    def add_midi_notes(track, notes, duration_sec):
        item = RPR.RPR_AddMediaItemToTrack(track)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", duration_sec)
        take = RPR.RPR_AddTakeToMediaItem(item)
        
        for note_val, start_pos, end_pos in notes:
            # Convert seconds to MIDI ticks (Quarter Note = 960 PPQ)
            # RPR_MIDI_InsertNote takes PPQ. A simpler way in API is using the RPR_MIDI_InsertNote with manual PPQ calculation.
            # 1 beat = 60/BPM seconds. 1 beat = 960 ticks.
            start_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_pos)
            end_ppq = RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_pos)
            RPR.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 0, note_val, velocity_base, False)
            
        RPR.RPR_MIDI_Sort(take)
        return item

    # Time calculations
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    total_length_sec = bar_length_sec * bars

    # =====================================================================
    # 1. CREATE MIX BUS (Folder Parent)
    # =====================================================================
    mix_bus = create_instrument_track(track_name, start_track_idx)
    # Remove ReaSynth from Mix Bus (added by helper)
    RPR.RPR_TrackFX_Delete(mix_bus, 0)
    # Make it a folder parent
    RPR.RPR_SetMediaTrackInfo_Value(mix_bus, "I_FOLDERDEPTH", 1)
    
    # Add EQ to Mix Bus (Tutorial: "Mix Bus Processing")
    RPR.RPR_TrackFX_AddByName(mix_bus, "ReaEQ", False, -1)

    # =====================================================================
    # 2. MAIN VOCAL (Center, Compressed)
    # =====================================================================
    vocal_trk = create_instrument_track("Main Vocal", start_track_idx + 1)
    RPR.RPR_TrackFX_AddByName(vocal_trk, "ReaComp", False, -1)
    # Set ReaSynth to saw wave for more vocal-like harmonics
    RPR.RPR_TrackFX_SetParam(vocal_trk, 0, 1, 1.0) 
    
    # Melody notes for Vocal
    vocal_notes = []
    for b in range(bars):
        start_time = b * bar_length_sec
        vocal_notes.append((get_note(0, 5), start_time, start_time + 1.0))
        vocal_notes.append((get_note(2, 5), start_time + 1.0, start_time + 2.0))
    add_midi_notes(vocal_trk, vocal_notes, total_length_sec)

    # =====================================================================
    # 3. VOCAL OCTAVE (Center, Lower Volume)
    # =====================================================================
    # Tutorial: "Vocal octave part is a little loud... drag fader down"
    vocal_oct_trk = create_instrument_track("Vocal Octave", start_track_idx + 2, vol=0.5) # -6dB
    RPR.RPR_TrackFX_SetParam(vocal_oct_trk, 0, 1, 1.0) # Saw wave
    
    vocal_oct_notes = []
    for b in range(bars):
        start_time = b * bar_length_sec
        vocal_oct_notes.append((get_note(0, 4), start_time, start_time + 1.0))
        vocal_oct_notes.append((get_note(2, 4), start_time + 1.0, start_time + 2.0))
    add_midi_notes(vocal_oct_trk, vocal_oct_notes, total_length_sec)

    # =====================================================================
    # 4. KALIMBA (Panned Hard Right)
    # =====================================================================
    # Tutorial: "Move Kalimba track all the way to the right"
    kalimba_trk = create_instrument_track("Kalimba", start_track_idx + 3, pan=1.0)
    RPR.RPR_TrackFX_SetParam(kalimba_trk, 0, 0, 0.05) # Quieter
    
    kalimba_notes = []
    for b in range(bars * 4): # 1/4 note plucks
        start_time = b * (60.0/bpm)
        kalimba_notes.append((get_note(b%3 + 2, 6), start_time, start_time + 0.2))
    add_midi_notes(kalimba_trk, kalimba_notes, total_length_sec)

    # =====================================================================
    # 5. GUITAR (Panned Hard Left)
    # =====================================================================
    # Tutorial: "Pan guitar to the left to give us more space"
    guitar_trk = create_instrument_track("Guitar", start_track_idx + 4, pan=-1.0)
    RPR.RPR_TrackFX_SetParam(guitar_trk, 0, 2, 1.0) # Square wave
    
    guitar_notes = []
    for b in range(bars * 2): # 1/2 note plucks
        start_time = b * (60.0/bpm) * 2
        guitar_notes.append((get_note(4, 3), start_time, start_time + 0.4))
    add_midi_notes(guitar_trk, guitar_notes, total_length_sec)

    # =====================================================================
    # 6. ELECTRIC PIANO (Sent to Reverb)
    # =====================================================================
    # Tutorial: "Bust it to our reverb send"
    piano_trk = create_instrument_track("Electric Piano", start_track_idx + 5)
    
    piano_notes = []
    for b in range(bars):
        start_time = b * bar_length_sec
        # Play a minor chord
        piano_notes.append((get_note(0, 4), start_time, start_time + bar_length_sec))
        piano_notes.append((get_note(2, 4), start_time, start_time + bar_length_sec))
        piano_notes.append((get_note(4, 4), start_time, start_time + bar_length_sec))
    add_midi_notes(piano_trk, piano_notes, total_length_sec)

    # =====================================================================
    # 7. REVERB RETURN BUS (Folder Child End)
    # =====================================================================
    reverb_trk = create_instrument_track("Reverb Return", start_track_idx + 6)
    RPR.RPR_TrackFX_Delete(reverb_trk, 0) # Remove ReaSynth
    # Set to end of folder
    RPR.RPR_SetMediaTrackInfo_Value(reverb_trk, "I_FOLDERDEPTH", -1)
    
    # Add Reverb plugin
    fx_idx = RPR.RPR_TrackFX_AddByName(reverb_trk, "ReaVerbate", False, -1)
    # Set Wet to 100%, Dry to 0% (Standard Aux Return setup)
    RPR.RPR_TrackFX_SetParam(reverb_trk, fx_idx, 0, 1.0) # Wet
    RPR.RPR_TrackFX_SetParam(reverb_trk, fx_idx, 1, 0.0) # Dry
    
    # Route Piano to Reverb
    send_idx = RPR.RPR_CreateTrackSend(piano_trk, reverb_trk)
    RPR.RPR_SetTrackSendInfo_Value(piano_trk, 0, send_idx, "D_VOL", 0.5) # Send at 50%

    return f"Created Mixing Environment '{track_name}' with Panning, Reverb Busses, and Compression across 6 sub-tracks."
```