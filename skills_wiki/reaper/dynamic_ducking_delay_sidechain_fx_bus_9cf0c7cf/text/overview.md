# Dynamic Ducking Delay (Sidechain FX Bus)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Ducking Delay (Sidechain FX Bus)

* **Core Musical Mechanism**: The pattern routes a lead element (like a vocal or synth solo) to an FX bus containing a Delay followed by a Compressor. The dry lead signal is routed to the delay *and* simultaneously routed to the sidechain input of the compressor. This forces the delay tail to "duck" (reduce in volume) while the lead is active, and dramatically swell up into the empty spaces (pauses/rests) as the compressor releases.
* **Why Use This Skill (Rationale)**: This technique solves the core problem of temporal and frequency masking. If a wet delay is too loud, it washes out the lead vocal and reduces intelligibility. By using dynamic ducking, you get the best of both worlds: a clean, up-front lead sound during the performance, and a lush, expansive delay throw that fills the rhythmic gaps, creating an intense sense of depth and a "push-and-pull" groove.
* **Overall Applicability**: Essential for lead vocals in dense mixes (Pop, EDM, Hip-Hop), lead guitar solos, and prominent synth lines. It allows producers to use extreme amounts of reverb or delay without muddying the mix.
* **Value Addition**: Compared to a standard send/return setup, this skill encodes advanced routing architecture (4-channel track routing) and dynamics processing parameters specifically tuned for inverse rhythmic interplay.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Source Rhythm**: For the effect to be audible, the source material *must* have rests/gaps. The pattern uses a 1-bar active phrase followed by a 1-bar complete rest, repeated.
  - **Delay Timing**: 1/4 note or dotted 1/8 note delays work best, as they create a distinct rhythmic echo that fills the 1-bar gap.
* **Step B: Pitch & Harmony**
  - To demonstrate the effect, a simple pentatonic minor staccato riff is used for the lead line.
* **Step C: Sound Design & FX**
  - **Track 1 (Lead)**: ReaSynth (staccato pluck).
  - **Track 2 (FX Bus)**: 
    - **ReaDelay**: 100% Wet, 0% Dry. 1/4 note delay time, 30% feedback.
    - **ReaComp**: Placed *after* the delay. Fast attack (3ms) to duck immediately, medium release (150ms) to swell musically. Ratio at 8:1 for aggressive clamping. 
* **Step D: Mix & Automation (Sidechain Routing)**
  - The FX bus is expanded to 4 channels.
  - **Send 1 (Audio)**: Lead Track (Channels 1/2) -> FX Bus (Channels 1/2).
  - **Send 2 (Sidechain trigger)**: Lead Track (Channels 1/2) -> FX Bus (Channels 3/4).
  - ReaComp's detector input is set to Auxiliary L+R (Channels 3/4).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| Sidechain Routing | `RPR_CreateTrackSend` & `RPR_SetTrackSendInfo_Value` | Essential to achieve the 1/2 -> 3/4 routing required for sidechain compression shown in the video. |
| Dynamic Ducking | FX Chain (`ReaComp` with Aux Input) | Matches the tutorial's technique of placing a compressor after the delay on the bus. |
| Musical Context | MIDI note insertion & `ReaSynth` | Provides an instant, testable lead melody with distinct pauses to highlight the delay swelling. |

> **Feasibility Assessment**: 100% reproducible. While the video uses SoundToys EchoBoy, the exact same sidechain routing logic and dynamic swelling effect is perfectly achieved using REAPER's stock `ReaDelay` and `ReaComp`.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "MyProject",
    track_name: str = "Lead Synth",
    bpm: int = 120,
    key: str = "E",
    scale: str = "pentatonic_minor",
    bars: int = 4,
    velocity_base: int = 110,
    **kwargs,
) -> str:
    """
    Create a Lead Synth track and a Dynamic Ducking Delay FX bus using sidechain compression.
    """
    import reaper_python as RPR
    
    # Music theory lookup tables
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "pentatonic_minor": [0, 3, 5, 7, 10]
    }
    
    scale_intervals = SCALES.get(scale, SCALES["pentatonic_minor"])
    root_pitch = NOTE_MAP.get(key, 4) + 60 # Octave 4

    RPR.RPR_SetCurrentBPM(0, bpm, False)

    # === Step 1: Create Source Track (Lead) ===
    idx_lead = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_lead, True)
    tr_lead = RPR.RPR_GetTrack(0, idx_lead)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_lead, "P_NAME", track_name, True)
    
    # Add an instrument so we have a sound
    RPR.RPR_TrackFX_AddByName(tr_lead, "ReaSynth", False, -1)

    # === Step 2: Create MIDI Data (Phrases with Gaps) ===
    beats_per_bar = 4
    bar_length_sec = (60.0 / bpm) * beats_per_bar
    item_length = bar_length_sec * bars
    
    item = RPR.RPR_AddMediaItemToTrack(tr_lead)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", item_length)
    take = RPR.RPR_AddTakeToMediaItem(item)
    
    # Generate an active phrase in Bar 1, REST in Bar 2, Phrase in Bar 3, REST in Bar 4
    for b in range(bars):
        if b % 2 == 1:
            continue # Leave odd bars (2 and 4) completely empty for the delay to swell
            
        bar_start = b * bar_length_sec
        # Write a syncopated 1/8 note riff
        for i, step in enumerate([0, 1.5, 2.5, 3]): 
            q_note_len = 60.0 / bpm
            start_time = bar_start + (step * q_note_len)
            end_time = start_time + (q_note_len * 0.5) # staccato notes
            
            note_idx = i % len(scale_intervals)
            pitch = root_pitch + scale_intervals[note_idx]
            
            RPR.RPR_MIDI_InsertNote(take, False, False, 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, start_time), 
                                    RPR.RPR_MIDI_GetPPQPosFromProjTime(take, end_time), 
                                    1, pitch, velocity_base, False)
    RPR.RPR_MIDI_Sort(take)

    # === Step 3: Create Dynamic Delay FX Bus ===
    idx_fx = RPR.RPR_CountTracks(0)
    RPR.RPR_InsertTrackAtIndex(idx_fx, True)
    tr_fx = RPR.RPR_GetTrack(0, idx_fx)
    RPR.RPR_GetSetMediaTrackInfo_String(tr_fx, "P_NAME", "Dynamic Delay Bus", True)
    
    # Set FX track to 4 channels to accommodate sidechain input
    RPR.RPR_SetMediaTrackInfo_Value(tr_fx, "I_NCHAN", 4)

    # === Step 4: Routing & Sidechain Setup ===
    # Send 1: Audio to Delay (Lead 1/2 -> FX 1/2)
    send_audio = RPR.RPR_CreateTrackSend(tr_lead, tr_fx)
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_audio, "I_SRCCHAN", 0) # 0 = ch 1/2
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_audio, "I_DSTCHAN", 0) # 0 = ch 1/2
    
    # Send 2: Sidechain Trigger (Lead 1/2 -> FX 3/4)
    send_sc = RPR.RPR_CreateTrackSend(tr_lead, tr_fx)
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "I_SRCCHAN", 0) # 0 = ch 1/2
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "I_DSTCHAN", 2) # 2 = ch 3/4
    RPR.RPR_SetTrackSendInfo_Value(tr_lead, 0, send_sc, "D_VOL", 1.0) # Ensure trigger is strong

    # === Step 5: Add and Configure FX ===
    # 1. Delay
    fx_delay = RPR.RPR_TrackFX_AddByName(tr_fx, "ReaDelay", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 0, -120.0) # Dry = -inf (100% wet bus)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 1, 0.0)    # Wet = 0dB
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_delay, 13, 1.0)   # Length 1 Musical = 1 quarter note
    
    # 2. Compressor (Ducking)
    fx_comp = RPR.RPR_TrackFX_AddByName(tr_fx, "ReaComp", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 0, -25.0) # Threshold (clamp down hard)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 1, 8.0)   # Ratio 8:1
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 2, 2.0)   # Attack 2ms (fast duck)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 3, 200.0) # Release 200ms (musical swell)
    RPR.RPR_TrackFX_SetParam(tr_fx, fx_comp, 15, 1.0)  # Detector Input: 1.0 = Aux L+R (Ch 3/4)
    
    return f"Created '{track_name}' and 'Dynamic Delay Bus' with 4-channel sidechain routing over {bars} bars at {bpm} BPM."
```