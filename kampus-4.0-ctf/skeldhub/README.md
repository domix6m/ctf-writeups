# SkeldHub

Miscellaneous, Medium · [English](README.en.md)

Po rejestracji dostałem repo na Gitei z workflow `triage.yml`, który zapisuje linię `Room:` z treści issue do `$GITHUB_ENV`, a w kolejnym kroku ma w środowisku sekret `FLAG`. Kilka linii `Room:` pozwoliło mi dopisać `BASH_ENV=report.txt`, przez co bash w drugim kroku wykonał treść mojego issue jako skrypt. Issue wypisywało `FLAG` w base64, bo runner maskuje sekrety w logach, więc pobrałem log joba przez API i go zdekodowałem. W `solve.sh` hasło do konta jest zastąpione przez `<HASLO>`.

Skrypty: [solve.sh](solve.sh)
