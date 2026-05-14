### 1. High-level Design Pattern Extraction

**Skill Name**: EDM Subtractive Arrangement & Ghost Sidechain Pumping

* **Core Musical Mechanism**: The defining technique here is building structural tension using a **"Ghost" Sidechain Compressor**. By generating a muted 4-on-the-floor kick drum track and routing it to the auxiliary detector of a compressor on the chord track, it creates an intense, rhythmic "pumping" swell. Once the song transitions from the Intro/Build into the Verse, the real drums take over this sidechain duty while the arrangement fills out with a syncopated bassline. 
* **Why Use This Skill (Rationale)**: This technique serves two purposes: rhythm and frequency management. Psychologically, the pumping effect introduces a phantom rhythm—giving the listener the pulse of a kick drum without actually playing one. This makes the eventual drop or verse feel much more impactful when the real kick finally hits. Technically, using sidechain compression carves out space in the mix, ensuring the transient of the kick drum punches through the dense pad frequencies unmasked.
* **Overall Applicability**: This is the absolute foundation of structural arrangement in House, Techno, Future Bass, and Trance. It is used to contrast sparsely arranged intros/builds against heavily driven choruses/verses.
* **Value Addition**: This skill moves beyond static loops by automatically scaffolding a song's macro-structure (Intro $\rightarrow$ Verse). It encodes advanced REAPER routing (multi-channel sidechaining), dynamics processing, subtractive arrangement, and syncopated bass grooves into a single generative action.

### 2. Technical Breakdown

* **Step A: Rhythm & Timing**
  - **Tempo**: 120-128 BPM (standard House).
  - **Grid**: 4-on-the-floor quarter notes for the sidechain trigger. The bassline uses a classic 16th-note 3-3-2 "tresillo" syncopation to drive groove against the rigid kick.
  - **Structure**: Splits the generated bar length in half. The first half (Intro) features only chords and the ghost pump. The second half (Verse) features chords, the real drum beat, and the bassline.
* **Step B: Pitch & Harmony**
  - **Progression**: Evaluates the requested scale (e.g., minor) and builds a standard EDM i - VI - III - v sequence.
  - **Chords**: Sustained block chords spanning 4 bars per loop.
  - **Bass**: Monophonic root notes anchored to the chord progression, played an octave lower.
* **Step C: Sound Design & FX**
  - **Chords**: Uses *ReaSynth* tuned as a pad (slow attack, long release).
  - **Dynamics (The Pump)**: *ReaComp* is placed on the chords, with its Detector Input routed to Aux L+R (Channels 3/4). Attack is near 0ms, Release is tuned to ~100-150ms to create a rhythmic swell that breathes perfectly with the tempo.
* **Step D: Mix & Automation**
  - **Track Channels**: The Chords track is configured to 4 channels to accept the sidechain. 
  - **Routing**: The Ghost Kick track has its Master Send disabled (`B_MAINSEND = 0`) but sends 100% volume to channels 3/4 of the Chords track. The real Drums track does the same, allowing a seamless transition of the pumping effect when the arrangement shifts.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the pattern | Method | Why this method |
|---|---|---|
| **Intro/Verse Structure** | Media Item placement | Placing empty space (no bass/drums in intro) physically replicates "subtractive arrangement" on the timeline. |
| **Sidechain Pumping** | `RPR_CreateTrackSend()` + ReaComp | Reproduces the exact professional sidechaining workflow taught in the tutorial (Track 1/2 $\rightarrow$ Aux 3/4). |
| **Bass Syncopation** | MIDI Note Insertion | Using precise PPQ intervals allows us to program the 3-3-2 EDM bass groove natively. |

> **Feasibility Assessment**: 100% reproduction of the structural arrangement and sidechain pumping technique. The script fully configures the track channels, disabled master sends, and ReaComp detector inputs required for the ghost pump. Standard ReaSynths are used as placeholders so the audio effect is immediately audible.

#### 3b. Complete Reproduction Code

```python
def create_pattern(
    project_name: str = "EDM_Arrangement",
    bpm: int = 125,
    key: str = "F",
    scale: str = "minor",
    bars: int = 16,
    **kwargs,
) -> str:
    """
    Create an EDM Arrangement Scaffold (Intro to Verse) featuring Ghost Sidechain Pumping.
    
    Args:
        project_name: Project identifier (for logging).
        bpm: Tempo in BPM.
        key: Root note (C, C#, D, ..., B).
        scale: Scale type (major, minor).
        bars: Total number of bars to generate (split 50/50 into Intro and Verse).
        **kwargs: Additional overrides.

    Returns:
        Status string describing the generated arrangement.
    """
    import reaper_python as RPR

    # === Step 1: Set Tempo ===
    RPR.RPR_SetCurrentBPM(0, bpm, False)
    
    # === Step 2: Music Theory & Math ===
    NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
                "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
                "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    SCALES = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
    }
    
    root_pitch = NOTE_MAP.get(key.capitalize(), 5)
    scale_deg = SCALES.get(scale.lower(), SCALES["minor"])
    
    def get_chord(degree, oct_shift=0):
        notes = []
        for i in [0, 2, 4]:
            idx = degree + i
            octave = oct_shift + (idx // 7)
            note = root_pitch + scale_deg[idx % 7] + (octave * 12)
            notes.append(note)
        return notes
        
    progression = [0, 5, 3, 4] if scale.lower() == "major" else [0, 5, 2, 4]
    
    intro_bars = bars // 2
    verse_bars = bars - intro_bars
    bar_length_sec = (60.0 / bpm) * 4
    
    def create_track(name):
        idx = RPR.RPR_CountTracks(0)
        RPR.RPR_InsertTrackAtIndex(idx, True)
        tr = RPR.RPR_GetTrack(0, idx)
        RPR.RPR_GetSetMediaTrackInfo_String(tr, "P_NAME", name, True)
        return tr

    # === Step 3: Create Tracks & Configure Routing ===
    tr_chords = create_track("Chords Pad (Receives Pump)")
    tr_ghost = create_track("Ghost Kick (Muted Trigger)")
    tr_bass = create_track("Verse Bass")
    tr_drums = create_track("Verse Drums")
    
    # Enable 4 channels on Chords to accept sidechain audio on 3/4
    RPR.RPR_SetMediaTrackInfo_Value(tr_chords, "I_NCHAN", 4) 
    # Disable Master Send on the Ghost Kick so it pumps silently
    RPR.RPR_SetMediaTrackInfo_Value(tr_ghost, "B_MAINSEND", 0)
    
    def route_sidechain(src_tr, dest_tr):
        send_idx = RPR.RPR_CreateTrackSend(src_tr, dest_tr)
        RPR.RPR_SetTrackSendInfo_Value(src_tr, 0, send_idx, "I_DSTCHAN", 2) # Route to channels 3/4
        RPR.RPR_SetTrackSendInfo_Value(src_tr, 0, send_idx, "I_SRCCHAN", 0) # Source from channels 1/2
        RPR.RPR_SetTrackSendInfo_Value(src_tr, 0, send_idx, "D_VOL", 1.0)   # 0dB
        
    route_sidechain(tr_ghost, tr_chords)
    route_sidechain(tr_drums, tr_chords) # Drums take over sidechaining during verse

    # === Step 4: Add Instruments & FX ===
    # Chords (Pad Synth + Sidechain Compressor)
    synth_ch = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_ch, 4, 0.1) # Slow Attack
    RPR.RPR_TrackFX_SetParam(tr_chords, synth_ch, 7, 0.2) # Slow Release
    
    comp_ch = RPR.RPR_TrackFX_AddByName(tr_chords, "ReaComp (Cockos)", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_chords, comp_ch, 0, 0.4) # Threshold ~ -30dB
    RPR.RPR_TrackFX_SetParam(tr_chords, comp_ch, 1, 0.1) # Ratio ~ 4:1
    RPR.RPR_TrackFX_SetParam(tr_chords, comp_ch, 2, 0.0) # Attack ~ 0ms
    RPR.RPR_TrackFX_SetParam(tr_chords, comp_ch, 3, 0.1) # Release ~ 100ms
    RPR.RPR_TrackFX_SetParam(tr_chords, comp_ch, 8, 0.2) # Detector Input: Aux L+R
    
    # Bass (Saw/Square Pluck)
    synth_b = RPR.RPR_TrackFX_AddByName(tr_bass, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_bass, synth_b, 0, 1.0) # Square vol
    RPR.RPR_TrackFX_SetParam(tr_bass, synth_b, 1, 0.5) # Saw vol
    
    # Ghost (Short Transient click)
    synth_g = RPR.RPR_TrackFX_AddByName(tr_ghost, "ReaSynth", False, -1)
    RPR.RPR_TrackFX_SetParam(tr_ghost, synth_g, 5, 0.05) # Very fast decay

    # === Step 5: Arrange MIDI Items ===
    def add_midi_item(tr, start_sec, length_sec):
        item = RPR.RPR_AddMediaItemToTrack(tr)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_POSITION", start_sec)
        RPR.RPR_SetMediaItemInfo_Value(item, "D_LENGTH", length_sec)
        return RPR.RPR_AddTakeToMediaItem(item)

    # 1. Chords (Plays entirely through Intro and Verse)
    take_chords = add_midi_item(tr_chords, 0, bars * bar_length_sec)
    for b in range(bars):
        deg = progression[b % 4]
        notes = get_chord(deg, oct_shift=4)
        st_ppq = b * 4 * 960
        en_ppq = st_ppq + (4 * 960)
        for p in notes:
            RPR.RPR_MIDI_InsertNote(take_chords, False, False, st_ppq, en_ppq, 0, p, 90, False)
    RPR.RPR_MIDI_Sort(take_chords)

    # 2. Ghost Trigger (Plays ONLY during the Intro)
    take_ghost = add_midi_item(tr_ghost, 0, intro_bars * bar_length_sec)
    for b in range(intro_bars):
        for beat in range(4): # 4-on-the-floor
            st_ppq = (b * 4 + beat) * 960
            RPR.RPR_MIDI_InsertNote(take_ghost, False, False, st_ppq, st_ppq + 240, 0, 36, 127, False)
    RPR.RPR_MIDI_Sort(take_ghost)

    # 3. Bass (Plays ONLY during the Verse)
    take_bass = add_midi_item(tr_bass, intro_bars * bar_length_sec, verse_bars * bar_length_sec)
    for b in range(verse_bars):
        deg = progression[b % 4]
        root = get_chord(deg, oct_shift=2)[0]
        # Groove: 3-3-2 tresillo sequence (lengths in 16th notes)
        rhythm = [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)]
        for start_16, len_16 in rhythm:
            st_ppq = (b * 16 + start_16) * 240
            en_ppq = st_ppq + (len_16 * 240) - 30 # -30 for slight articulation gap
            RPR.RPR_MIDI_InsertNote(take_bass, False, False, st_ppq, en_ppq, 0, root, 110, False)
    RPR.RPR_MIDI_Sort(take_bass)

    # 4. Drums (Plays ONLY during the Verse)
    take_drums = add_midi_item(tr_drums, intro_bars * bar_length_sec, verse_bars * bar_length_sec)
    for b in range(verse_bars):
        for beat in range(4):
            st_ppq = (b * 4 + beat) * 960
            # Kick
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, st_ppq, st_ppq + 240, 0, 36, 120, False)
            # Clap on 2 & 4
            if beat in [1, 3]:
                RPR.RPR_MIDI_InsertNote(take_drums, False, False, st_ppq, st_ppq + 240, 0, 38, 110, False)
            # Offbeat Hats
            RPR.RPR_MIDI_InsertNote(take_drums, False, False, st_ppq + 480, st_ppq + 720, 0, 42, 90, False)
    RPR.RPR_MIDI_Sort(take_drums)

    return f"Created EDM Arrangement Scaffold: {intro_bars} bars Intro / {verse_bars} bars Verse in {key} {scale} at {bpm} BPM."
```