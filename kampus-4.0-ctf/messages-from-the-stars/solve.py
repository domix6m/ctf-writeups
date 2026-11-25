#!/usr/bin/env python3
"""
Dekoder sygnalu FSK (500 Hz = 0, 1500 Hz = 1) -> bitmapa.

Sygnal sklada sie z impulsow tonu przedzielonych cisza. Kazdy impuls to jeden
bit: niski ton (~500 Hz) = 0, wysoki ton (~1500 Hz) = 1.
Liczba bitow (1679) to iloczyn dwoch liczb pierwszych 23 x 73, wiec skrypt
sam dobiera wymiary obrazu (jak w wiadomosci z Arecibo).

Uzycie:
    python3 decode_signal.py signal.wav [-o out.png] [--scale 12]
"""
import argparse
import itertools
import wave

import numpy as np
from PIL import Image


def read_wav(path):
    with wave.open(path) as w:
        n_ch, sw, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    dtype = {1: np.uint8, 2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dtype=dtype).astype(np.float64)
    if sw == 1:
        x -= 128
    if n_ch > 1:
        x = x.reshape(-1, n_ch).mean(axis=1)
    return x, rate


def extract_bits(x, rate, win_ms=5, split_hz=1000):
    """Dzieli sygnal na okna, wykrywa impulsy (okna z dzwiekiem)
    i dla kazdego impulsu okresla dominujaca czestotliwosc."""
    win = int(rate * win_ms / 1000)
    segs = x[: len(x) // win * win].reshape(-1, win)
    energy = np.abs(segs).mean(axis=1)
    active = energy > energy.max() * 0.1

    bits = []
    idx = 0
    for is_on, group in itertools.groupby(active):
        length = len(list(group))
        if is_on:
            chunk = x[idx * win:(idx + length) * win]
            spec = np.abs(np.fft.rfft(chunk * np.hanning(len(chunk))))
            freq = np.fft.rfftfreq(len(chunk), 1 / rate)[spec.argmax()]
            bits.append(1 if freq > split_hz else 0)
        idx += length
    return bits


def factor_pairs(n):
    return [(a, n // a) for a in range(2, int(n ** 0.5) + 1) if n % a == 0]


def to_image(bits, width, scale):
    height = len(bits) // width
    arr = np.array(bits[: width * height], dtype=np.uint8).reshape(height, width)
    img = Image.fromarray((1 - arr) * 255)  # 1 = czarny piksel, 0 = bialy
    return img.resize((width * scale, height * scale), Image.NEAREST), arr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("-o", "--out", default="message.png")
    ap.add_argument("--width", type=int, help="wymus szerokosc obrazu")
    ap.add_argument("--scale", type=int, default=12)
    args = ap.parse_args()

    x, rate = read_wav(args.wav)
    bits = extract_bits(x, rate)
    n = len(bits)
    print(f"Odczytano {n} bitow (jedynek: {sum(bits)})")
    pairs = factor_pairs(n)
    print(f"Mozliwe wymiary: {pairs}")

    width = args.width or (pairs[0][0] if pairs else 64)
    img, arr = to_image(bits, width, args.scale)
    img.save(args.out)
    print(f"Zapisano {args.out} ({width} x {len(bits) // width})")
    # tekst jest zapisany bokiem - obrot o 90 stopni w lewo daje czytelny napis
    rot_path = args.out.rsplit(".", 1)[0] + "_rotated.png"
    img.rotate(90, expand=True).save(rot_path)
    print(f"Zapisano {rot_path} (obrocony, do czytania)\n")
    for row in np.rot90(arr, 1):
        print("".join("#" if b else "." for b in row))


if __name__ == "__main__":
    main()
