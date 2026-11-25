# Asteroid Relay

Miscellaneous, Easy · [Polski](README.md)

I ran a local HTTP server (`srv.py`), exposed it with `ssh -R 80:127.0.0.1:8088 nokey@localhost.run` and adjusted the replies in `resp.py` based on the errors the unit returned, running each attempt with `go.sh`. The JWT was the hardest part: only a `kid` pointing to `/dev/null` produced an error with the key format `unit:<lowercase serial>`, so I signed the token with it, with `state: "on"` and a short `exp`. After that I sent back `sequence`, the commands from the dictionary in the challenge text, an update manifest with `install: "now"` and a config with `remote_mode: "maintenance"`, and then `GET /remote/console` returned the flag.

Scripts: [srv.py](srv.py), [resp.py](resp.py), [variant.json](variant.json), [go.sh](go.sh)
