# Asteroid Relay

Miscellaneous, Easy · [English](README.en.md)

Postawiłem lokalny serwer HTTP (`srv.py`), wystawiłem go przez `ssh -R 80:127.0.0.1:8088 nokey@localhost.run` i poprawiałem odpowiedzi w `resp.py` na podstawie błędów zwracanych przez jednostkę, a każdą próbę puszczałem przez `go.sh`. Najtrudniejszy był token JWT: dopiero `kid` wskazujący na `/dev/null` dał błąd z formatem klucza `unit:<serial małymi literami>`, więc podpisałem nim token ze `state: "on"` i krótkim `exp`. Dalej odsyłałem `sequence`, komendy ze słownika z treści zadania, manifest aktualizacji z `install: "now"` i konfigurację z `remote_mode: "maintenance"`, po czym flagę zwrócił `GET /remote/console`.

Skrypty: [srv.py](srv.py), [resp.py](resp.py), [variant.json](variant.json), [go.sh](go.sh)
