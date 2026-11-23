#!/usr/bin/env python3
"""Make the ad's music: a short upbeat chiptune loop, pure Python, no
samples. 132 BPM, A minor, 22 seconds, 44.1 kHz stereo WAV.

A square-wave lead plays a bright pentatonic riff over a triangle-wave
bass on the roots (Am - F - C - G, one bar each), with a noise hat on the
off-beats. Short envelopes keep it from clicking. Written for this ad
only; the tune is original, four bars looping.
"""
import math
import struct
import wave

SR = 44100
DUR = 22.0
BPM = 132
BEAT = 60.0 / BPM          # one quarter note
EIGHTH = BEAT / 2.0        # one 8th note


def note_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def square(phase):
    return 1.0 if (phase % 1.0) < 0.5 else -1.0


def triangle(phase):
    p = phase % 1.0
    return 4.0 * p - 1.0 if p < 0.5 else 3.0 - 4.0 * p


# lead riff: (midi, 8ths) — A minor pentatonic, call and answer
RIFF = [
    (69, 1), (72, 1), (76, 1), (79, 1), (76, 1), (72, 1), (69, 1), (67, 1),
    (69, 1), (72, 1), (76, 1), (81, 1), (79, 1), (76, 1), (72, 1), (69, 2),
    (69, 1), (72, 1), (76, 1), (79, 1), (81, 1), (79, 1), (76, 1), (72, 1),
    (76, 1), (79, 1), (81, 1), (84, 1), (81, 1), (79, 1), (76, 1), (72, 2),
]
# bass roots, one bar each: Am, F, C, G (midi)
BASS = [45, 41, 48, 43]


def envelope(t, length):
    """Quick attack, exponential-ish decay."""
    if t < 0.005:
        return t / 0.005
    return max(0.0, 1.0 - (t / length) * 0.85)


def main():
    total = int(SR * DUR)
    out = [0.0] * (total * 2)
    # expand the riff to the full length
    seq = []
    while sum(d for _, d in seq) * EIGHTH < DUR:
        seq.extend(RIFF)
    t = 0.0
    idx = 0
    # precompute a deterministic noise table for the hat
    noise = [((i * 1103515245 + 12345) >> 16 & 0x7FFF) / 16384.0 - 1.0
             for i in range(int(SR * 0.05))]
    n = len(seq)
    step = 0
    pos = 0
    while pos < total:
        midi, d8 = seq[step % n]
        step += 1
        length = d8 * EIGHTH
        nsamp = int(length * SR)
        freq = note_freq(midi)
        bar = int((pos / SR) / (BEAT * 4)) % 4
        bass_freq = note_freq(BASS[bar])
        for i in range(nsamp):
            if pos + i >= total:
                break
            tt = i / SR
            env = envelope(tt, length)
            lead = square(tt * freq) * 0.16 * env
            bass = triangle(tt * bass_freq) * 0.22 * envelope(tt, length)
            # hat on the off-beat 8th (every second 8th)
            hat = 0.0
            if (step % 2) == 0 and i < int(SR * 0.03):
                hat = noise[i % len(noise)] * 0.05 * (1.0 - i / (SR * 0.03))
            s = lead + bass + hat
            out[(pos + i) * 2] += s
            out[(pos + i) * 2 + 1] += s
        pos += nsamp
    # gentle fade out over the last half second
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
