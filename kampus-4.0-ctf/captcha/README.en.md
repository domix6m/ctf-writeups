# Captcha

Miscellaneous, Medium · [Polski](README.md)

Each video is noise where the background moves one way and the letters move the other way. `solve.py` finds the two main shifts between frames, takes the pixels moving like the smaller area as text, and recognises characters by comparing them with letters rendered from fonts. It fetches a round from `/api/new` and sends the answers to `/api/submit`, retrying when recognition gets something wrong.

Scripts: [solve.py](solve.py)
