# Ambient Cinematic No-Drums Coordinator

This T5 coordinator creates a coherent ambient piece instead of stacking
independent loop fragments. It sets a single tempo/key context, creates five
named non-drum roles, and fills the full timeline with long sustained notes:
string pad foundation, rising drone, sparse piano motif, cello-style bass, and
ethereal voice-like pad.

Use it when the brief says ambient, cinematic, Brian Eno, Tim Hecker, Hammock,
slow evolution, sustained drone, sparse piano, or explicitly **NO drums**.

```python
def create_pattern(bpm=90, key="C", scale="minor", bars=60, **kwargs):
    from math import floor
    NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    root = NOTE.get(key, 0)
    total = int(bars) * 4
    project.bpm = float(bpm)
    project.name = "Ambient Cinematic No-Drums"
    project.tracks[:] = [t for t in project.tracks if not any(x in t.name.lower() for x in ("ambient coordinator", "string pad", "rising drone", "sparse piano", "cello bass", "voice pad"))]
    def track(name, program):
        t = Track(name=name, program=program, is_drum=False, channel=len(project.tracks) % 15)
        project.tracks.append(t)
        return t
    strings = track("String Pad Foundation", 48)
    drone = track("Rising Drone Filter Sweep", 95)
    piano = track("Sparse Piano Motif", 0)
    cello = track("Cello Bass Sustains", 42)
    voice = track("Ethereal Voice Pad", 89)
    cm = [root + 48, root + 51, root + 55]
    ab = [root + 44, root + 48, root + 51]
    eb = [root + 51, root + 55, root + 58]
    bb = [root + 46, root + 50, root + 53]
    chords = [cm, ab, eb, bb]
    for section_start in range(0, total, 16):
        chord = chords[(section_start // 16) % len(chords)]
        for p in chord:
            strings.notes.append({"pitch": p, "start_time": section_start, "duration": min(16, total-section_start), "velocity": 48})
            voice.notes.append({"pitch": p + 24, "start_time": section_start + 2, "duration": min(14, total-section_start-2), "velocity": 34})
        cello.notes.append({"pitch": chord[0] - 24, "start_time": section_start, "duration": min(16, total-section_start), "velocity": 55})
    for section_start in range(0, total, 32):
        for j, p in enumerate([root + 36, root + 43, root + 48, root + 55]):
            start = section_start + j * 4
            if start < total:
                drone.notes.append({"pitch": p, "start_time": start, "duration": min(28 - j * 4, total-start), "velocity": 26 + j * 9})
    for bar in (8, 24, 40):
        start = bar * 4
        if start >= total:
            continue
        motif = [root + 72, root + 75, root + 79, root + 77]
        for j, p in enumerate(motif):
            piano.notes.append({"pitch": p, "start_time": start + j * 1.5, "duration": 1.1, "velocity": 42 + j * 4})
    for idx, t in enumerate(project.tracks):
        t.fx.extend(["ReaEQ low cut 120Hz" if "Bass" not in t.name else "ReaEQ low shelf 80Hz", "Large hall reverb", "Slow auto-pan"])
    return "Ambient no-drums coordinator created 5 coherent sustained roles across the full form."
```
