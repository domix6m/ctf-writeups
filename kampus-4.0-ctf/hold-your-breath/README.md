# Hold Your Breath

Binary Exploitation, Medium · [English](README.en.md)

Etykieta filtra jest czytana bez zera na końcu, więc po wpisaniu 32 znaków opcja Status wypisuje też adres `puts`, z którego policzyłem adres `system` w dołączonym libc. `clean_filter` zwalnia locka i śpi 5 sekund przed wywołaniem `f->log_func(f->label)`, więc jednym połączeniem uruchamiam czyszczenie, a drugim w tym czasie usuwam filtr i dodaję wpis do logu, który dostaje ten sam kawałek pamięci z moją komendą i adresem `system`. Wyniku nie widziałem na swoim połączeniu, więc najpierw `sleep`-em sprawdziłem, że `system()` się wykonuje, a potem przekierowałem wynik na sockety: `python3 solve.py 'cat f*>&4;cat f*>&5;cat f*>&6'`.

Skrypty: [solve.py](solve.py)
