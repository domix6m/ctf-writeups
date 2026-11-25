# Cascading Sabotage Sheets

Reverse Engineering, Medium · [Polski](README.md)

The panel logic isn't in JavaScript but in CSS: it's an 8086 CPU emulator that uses new Chromium features. I opened the panel in Chromium, read the program memory with `getComputedStyle` (`dump_mem.js`), saved it to `mem.bin` (`make_mem.py`) and disassembled it with capstone. The program encrypts the 16-character code in two reversible rounds and compares the result with a constant table, so `solve.py` computes the code backwards (`3A7E4535DEF5F87B`), and entering it in the panel gave me the flag.

Scripts: [dump_mem.js](dump_mem.js), [make_mem.py](make_mem.py), [solve.py](solve.py)
