# Crewmate Management System

Binary Exploitation, Easy · [Polski](README.md)

The service runs `eval()` on the expression you type, but only allows crewmate colour names, the `open` function and numbers, so you can't type the path as text. From the Dockerfile I knew the flag is in `archive/flag.txt`, so I built that path from single letters cut out of record fields (e.g. `red.rank[1]` is `a`) and generated the whole payload with `gen_payload.py`. Nothing came back through `ncat`, so I sent `open(...).read()` through `openssl s_client` with a few `sleep`s and the server returned the flag.

Scripts: [gen_payload.py](gen_payload.py), [solve.sh](solve.sh)
