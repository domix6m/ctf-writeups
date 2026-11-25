# Crewmate Management System

Binary Exploitation, Easy · [English](README.en.md)

Serwis robi `eval()` na wpisanym wyrażeniu, ale przepuszcza tylko nazwy kolorów załogi, funkcję `open` i liczby, więc ścieżki nie da się wpisać jako tekstu. Z Dockerfile'a wiedziałem, że flaga leży w `archive/flag.txt`, więc skleiłem tę ścieżkę z pojedynczych liter wyciętych z pól rekordów (np. `red.rank[1]` to `a`), a cały payload wygenerowałem skryptem `gen_payload.py`. Przez `ncat` nic nie wracało, więc wysłałem `open(...).read()` przez `openssl s_client` z kilkoma `sleep` i serwer zwrócił flagę.

Skrypty: [gen_payload.py](gen_payload.py), [solve.sh](solve.sh)
