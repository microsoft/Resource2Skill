def create_pattern(bpm=150, key="F#", scale="minor", bars=48, **kwargs):
    NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    minor = [0, 2, 3, 5, 7, 8, 10]
    root = NOTE.get(key, 6)
    total_bars = int(bars)
    project.bpm = float(bpm)
    project.name = "Future Bass Drop"

    def track(name, program=0, is_drum=False):
        t = Track(name=name, program=program, is_drum=is_drum, channel=9 if is_drum else len(project.tracks) % 15)
        project.tracks.append(t)
        return t

    pad = track("Airy Sidechained Pad", 89)
    stabs = track("Chopped Vocal-like Synth Stabs", 81)
    lead = track("Detuned Supersaw Lead", 81)
    lead_hi = track("Final Drop Octave Lead", 80)
    sub = track("Heavy 808 Sub Bass", 38)
    drums = track("Half-time Trap Drums", 0, True)
    build = track("Build Snare Roll and Filter Sweep", 95, True)

    prog = [0, 5, 2, 6]
    def degree_pitch(deg, octave):
        return (octave + 1) * 12 + root + minor[deg % len(minor)]

    chords = []
    for deg in prog:
        base = degree_pitch(deg, 4)
        chords.append([base, base + 7, base + 12, base + 15])

    for bar in range(total_bars):
        start = bar * 4.0
        in_intro = bar < 8
        in_build = 8 <= bar < 16
        in_drop = 16 <= bar < 32
        in_break = 32 <= bar < 40
        in_final = 40 <= bar < 48
        chord = chords[bar % 4]
        pad_vel = 42 if in_intro else 62 if in_build else 88 if in_drop else 50 if in_break else 104
        for p in chord:
            pad.notes.append({"pitch": p, "start_time": start, "duration": 3.75, "velocity": pad_vel})
        if in_intro or in_break or bar % 4 == 3:
            for j, off in enumerate([0.0, 1.5, 2.25, 3.0]):
                p = degree_pitch((bar + j * 2) % 7, 5)
                stabs.notes.append({"pitch": p, "start_time": start + off, "duration": 0.22, "velocity": 72 if not in_drop else 88})
        if in_build:
            build.notes.append({"pitch": 49, "start_time": start, "duration": 3.8, "velocity": 45 + (bar - 8) * 8})
            div = 4 if bar < 12 else 8 if bar < 15 else 16
            for i in range(div):
                off = i * (4.0 / div)
                build.notes.append({"pitch": 38, "start_time": start + off, "duration": 0.08, "velocity": min(124, 58 + i * 4)})
        if in_drop or in_final:
            for off in [0.0, 1.5, 2.75]:
                drums.notes.append({"pitch": 36, "start_time": start + off, "duration": 0.18, "velocity": 118})
            drums.notes.append({"pitch": 38, "start_time": start + 2.0, "duration": 0.18, "velocity": 114})
            for i in range(8):
                drums.notes.append({"pitch": 42, "start_time": start + i * 0.5, "duration": 0.1, "velocity": 72 + (i % 2) * 18})
            if bar % 4 == 3:
                drums.notes.append({"pitch": 49, "start_time": start, "duration": 0.45, "velocity": 108})
            bass = degree_pitch(prog[bar % 4], 1)
            for off, dur in [(0.0, 1.2), (1.5, 0.75), (2.75, 1.0)]:
                sub.notes.append({"pitch": bass, "start_time": start + off, "duration": dur, "velocity": 118})
            motif = [0, 2, 4, 6, 4, 2, 1, 2]
            for i, deg in enumerate(motif):
                p = degree_pitch(deg, 5) + (12 if i in (3, 7) else 0)
                lead.notes.append({"pitch": p, "start_time": start + i * 0.5, "duration": 0.36, "velocity": 106})
                if in_final:
                    lead_hi.notes.append({"pitch": p + 12, "start_time": start + i * 0.5, "duration": 0.32, "velocity": 92})

    drums.fx.extend(["ReaEQ transient bright", "ReaComp punch", "ReaLimit"])
    sub.fx.extend(["ReaEQ HP30 LP120", "low shelf 65Hz", "sidechain duck metadata"])
    pad.fx.extend(["ReaEQ low cut", "chorus stereo widen", "sidechain pump", "large hall reverb"])
    lead.fx.extend(["unison detune chorus", "ping-pong delay", "glossy plate reverb"])
    lead_hi.fx.extend(["octave doubler", "bright shelf", "short plate reverb"])
    stabs.fx.extend(["formant-style filter", "short delay", "wide chorus"])
    build.fx.extend(["rising filter sweep", "snare roll acceleration"])
    return "Future bass coordinator created intro, build, drop, breakdown, and final octave-doubled drop."
