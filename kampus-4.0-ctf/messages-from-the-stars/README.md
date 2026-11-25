# Messages From The Stars

Forensics, Easy · [English](README.en.md)

Najpierw sprawdziłem LSB próbek w `signal.wav`, ale były same zera. W FFT widać tylko dwa tony, 500 Hz i 1500 Hz, więc potraktowałem każdy impuls jako bit (niski to 0, wysoki to 1) i dostałem 1679 bitów, czyli 23 × 73, jak w wiadomości z Arecibo. `solve.py` układa bity w obrazek 23 × 73, a po obróceniu go o 90° widać flagę.

Skrypty: [solve.py](solve.py)
