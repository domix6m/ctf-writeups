# Leftover Sample

Reverse Engineering, Medium · [Polski](README.md)

The binary is obfuscated with movfuscator and wouldn't run on my Kali (arm64), so I wrote an emulator in Unicorn (`emu.py`). The program compares the SHA-256 of the input with a hash in the binary, but before that it XORs a 40-byte table with a key that depends only on earlier input characters, and never uses the result. That let me recover the flag one character at a time (`char[i] = table[i] ^ key[i]`; `keys.py` reads the keys, `solve.py` runs the loop), and I checked that its SHA-256 matches the hash in the binary. I rebuilt `emu.py` from the session history because the file was gone from disk.

Scripts: [emu.py](emu.py), [keys.py](keys.py), [solve.py](solve.py)
