# Emergency Link

Web, Easy · [Polski](README.md)

The site is a prank with popups, sounds and clipboard spam, so I used curl instead of a browser. In the JS files I found the only backend request, `/api/messages?room=emergency`, and `room='` returned a database error, so it was SQL injection in SQLite. With `UNION SELECT` I read the `secret` table from `sqlite_master`, and the flag was in it.

Scripts: [solve.sh](solve.sh)
