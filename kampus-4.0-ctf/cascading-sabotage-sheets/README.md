# Cascading Sabotage Sheets

Reverse Engineering, Medium · [English](README.en.md)

Logika panelu nie jest w JavaScripcie, tylko w CSS: to emulator procesora 8086, który korzysta z nowych funkcji Chromium. Otworzyłem panel w Chromium, odczytałem pamięć programu przez `getComputedStyle` (`dump_mem.js`), zapisałem ją do `mem.bin` (`make_mem.py`) i zdeasemblowałem capstone'em. Program szyfruje 16-znakowy kod w dwóch odwracalnych rundach i porównuje wynik ze stałą tablicą, więc `solve.py` liczy kod od końca (`3A7E4535DEF5F87B`), a po wpisaniu go w panelu dostałem flagę.

Skrypty: [dump_mem.js](dump_mem.js), [make_mem.py](make_mem.py), [solve.py](solve.py)
