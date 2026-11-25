# Captcha

Miscellaneous, Medium · [English](README.en.md)

Każdy filmik to szum, w którym tło przesuwa się w jedną stronę, a litery w drugą. `solve.py` szuka dwóch głównych przesunięć między klatkami, jako tekst bierze piksele poruszające się jak mniejszy obszar, a znaki rozpoznaje przez porównanie z literami wyrenderowanymi z fontów. Rundę pobiera z `/api/new` i wysyła odpowiedzi na `/api/submit`, ponawiając próbę, gdy rozpoznawanie się pomyli.

Skrypty: [solve.py](solve.py)
