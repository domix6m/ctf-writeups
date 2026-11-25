# Leftover Sample

Reverse Engineering, Medium · [English](README.en.md)

Binarka jest zaciemniona movfuscatorem i nie dało się jej uruchomić na moim Kali (arm64), więc napisałem emulator w Unicornie (`emu.py`). Program porównuje SHA-256 wejścia z hashem w binarce, ale wcześniej XOR-uje 40-bajtową tablicę z kluczem, który zależy tylko od poprzednich znaków wejścia, a wyniku nigdzie nie używa. Dzięki temu odzyskałem flagę znak po znaku (`znak[i] = tablica[i] ^ klucz[i]`, klucze odczytuje `keys.py`, pętlę robi `solve.py`) i sprawdziłem, że jej SHA-256 zgadza się z hashem w binarce. `emu.py` odtworzyłem z historii sesji, bo plik zniknął z dysku.

Skrypty: [emu.py](emu.py), [keys.py](keys.py), [solve.py](solve.py)
