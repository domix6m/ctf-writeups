# Emergency Link

Web, Easy · [English](README.en.md)

Strona to prank z popupami, dźwiękami i spamem schowka, więc zamiast przeglądarki użyłem curla. W plikach JS znalazłem jedyne zapytanie do backendu, `/api/messages?room=emergency`, a `room='` zwracało błąd bazy, czyli SQL injection w SQLite. Przez `UNION SELECT` odczytałem z `sqlite_master` tabelę `secret` i w niej była flaga.

Skrypty: [solve.sh](solve.sh)
