# Messages From The Stars

Forensics, Easy · [Polski](README.md)

First I checked the LSB of the samples in `signal.wav`, but it was all zeros. FFT shows only two tones, 500 Hz and 1500 Hz, so I treated each pulse as a bit (low is 0, high is 1) and got 1679 bits, which is 23 × 73, like the Arecibo message. `solve.py` arranges the bits into a 23 × 73 image, and after rotating it by 90° the flag is visible.

Scripts: [solve.py](solve.py)
