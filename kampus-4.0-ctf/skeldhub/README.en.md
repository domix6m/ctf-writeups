# SkeldHub

Miscellaneous, Medium · [Polski](README.md)

After registering I got a Gitea repo with a `triage.yml` workflow that writes the `Room:` line from the issue body into `$GITHUB_ENV`, and its next step has the `FLAG` secret in its environment. Several `Room:` lines let me add `BASH_ENV=report.txt`, so bash in the second step ran my issue body as a script. The issue printed `FLAG` in base64, because the runner masks secrets in logs, so I downloaded the job log through the API and decoded it. In `solve.sh` the account password is replaced with `<HASLO>`.

Scripts: [solve.sh](solve.sh)
