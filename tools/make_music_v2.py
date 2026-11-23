#!/usr/bin/env python3
"""Make the ad's NEW music: a fresh original tune, pure Python, no
samples. 120 BPM, D major, 22 seconds, 44.1 kHz stereo WAV.

A sine-pluck lead plays a bright D-major riff over a triangle bass
(D - Bm - G - A, one bar each), with a soft kick on beats 1 and 3 and
a noise hat on the off-beats. Written for this ad only; the tune is
original and has never been used anywhere.
"""
import math
import struct
import wave

SR = 44100
DUR = 22.0
BPM = 120
BEAT = 60.0 / BPM          # one quarter note
SIXTEENTH = BEAT / 4.0     # one 16th note


def note_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def sine(phase):
    return math.sin(2.0 * math.pi * (phase % 1.0))


def triangle(phase):
    p = phase % 1.0
    return 4.0 * p - 1.0 if p < 0.5 else 3.0 - 4.0 * p


# lead riff: (midi, 16ths) — D major, four bars, one bar each chord.
# D5=74 F#5=78 A5=81 E5=76 B4=71 A4=69 G4=67 G5=79 C#5=73 D5=74
RIFF = [
    # bar 1 (D)
    (74, 2), (78, 2), (81, 2), (78, 2), (76, 2), (74, 2), (71, 2), (69, 2),
    # bar 2 (Bm)
    (71, 2), (74, 2), (78, 2), (81, 2), (78, 2), (76, 2), (74, 2), (71, 2),
    # bar 3 (G)
    (67, 2), (71, 2), (74, 2), (79, 2), (74, 2), (71, 2), (69, 2), (67, 2),
    # bar 4 (A)
    (69, 2), (73, 2), (76, 2), (81, 2), (76, 2), (73, 2), (71, 2), (69, 2),
]
# bass roots, one bar each: D, Bm, G, A (midi)
BASS = [50, 47, 43, 45]


def pluck_env(t, length):
    """Fast attack, exponential decay — a pluck."""
    if t < 0.004:
        return t / 0.004
    return math.exp(-3.0 * t / length)


def main():
    total = int(SR * DUR)
    out = [0.0] * (total * 2)
    seq = []
    while sum(d for _, d in seq) * SIXTEENTH < DUR:
        seq.extend(RIFF)
    noise = [((i * 1103515245 + 12345) >> 16 & 0x7FFF) / 16384.0 - 1.0
             for i in range(int(SR * 0.05))]
    n = len(seq)
    step = 0
    pos = 0
    bar_len = BEAT * 4
    while pos < total:
        midi, d16 = seq[step % n]
        step += 1
        length = d16 * SIXTEENTH
        nsamp = int(length * SR)
        freq = note_freq(midi)
        bar = int((pos / SR) / bar_len) % 4
        bass_freq = note_freq(BASS[bar])
        # beat position inside the bar (0..3) for the kick
        beat_in_bar = int(((pos / SR) % bar_len) / BEAT)
        for i in range(nsamp):
            if pos + i >= total:
                break
            tt = i / SR
            env = pluck_env(tt, length)
            lead = sine(tt * freq) * 0.20 * env
            # add a soft octave shimmer to the lead
            lead += sine(tt * freq * 2.0) * 0.05 * env
            bass = triangle(tt * bass_freq) * 0.24 * pluck_env(tt, length)
            # kick on beats 1 and 3 (beat_in_bar 0 and 2), first 0.12 s
            kick = 0.0
            if beat_in_bar in (0, 2) and i < int(SR * 0.12):
                kt = i / SR
                kick = math.sin(2.0 * math.pi * (120.0 - 60.0 * kt / 0.12) * kt) \
                    * 0.30 * (1.0 - kt / 0.12)
            # hat on the off-beat 16th (every odd 16th step)
            hat = 0.0
            if (step % 2) == 0 and i < int(SR * 0.03):
                hat = noise[i % len(noise)] * 0.04 * (1.0 - i / (SR * 0.03))
            s = lead + bass + kick + hat
            out[(pos + i) * 2] += s
            out[(pos + i) * 2 + 1] += s
        pos += nsamp
    # fade in over the first 0.3 s, fade out over the last 0.5 s
    fade_in = int(SR * 0.3)
    for i in range(fade_in):
        g = i / fade_in
        out[i * 2] *= g
        out[i * 2 + 1] *= g
    fade = int(SR * 0.5)
    for i in range(fade):
        g = 1.0 - i / fade
        out[(total - fade + i) * 2] *= g
        out[(total - fade + i) * 2 + 1] *= g
    peak = max(abs(v) for v in out) or 1.0
    scale = 0.85 / peak
    with wave.open("music.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, v * scale)) * 32767))
            for v in out)
        w.writeframes(frames)
    print("wrote music.wav: %.1f s, %d samples" % (DUR, total))


if __name__ == "__main__":
    main()
