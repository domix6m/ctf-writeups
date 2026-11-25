import json, base64, hmac, hashlib
def b64(d): return base64.urlsafe_b64encode(d).rstrip(b'=').decode()
def ub(s): return base64.urlsafe_b64decode(s+'='*(-len(s)%4))
MAP = {"BOOT_SYNC": "ACK", "TRACKING_SYNC": "ACK", "ASTEROID_LOCKED": "HOLD", "UPDATE_WINDOW": "INSTALL_UPDATE"}
V = json.load(open("variant.json"))
def sign(hd, pl, key):
    si = b64(json.dumps(hd,separators=(',',':')).encode())+'.'+b64(json.dumps(pl,separators=(',',':')).encode())
    return si+'.'+b64(hmac.new(key.encode(), si.encode(), hashlib.sha256).digest())
def respond(method, path, headers, body):
    r = {}
    sq = headers.get("x-ads-sequence") or headers.get("X-Ads-Sequence") or headers.get("X-ADS-Sequence")
    if sq: r["sequence"] = int(sq)
    if isinstance(body, dict) and "token" in body:
        h,p,s = body["token"].split('.')
        hd = json.loads(ub(h)); pl = json.loads(ub(p))
        pl["state"] = "on"; pl["exp"] = pl.get("iat",0) + 30
        r["token"] = sign(hd, pl, "unit:"+body["hardware"]["serial"].lower())
        r["state"] = "on"
    t = body.get("type") if isinstance(body, dict) else None
    if t in MAP: r["command"] = MAP[t]
    if isinstance(body, dict) and body.get("type") == "FIRMWARE_UPDATE_REQUEST":
        r = {"version": "2.4.3-ads", "protocol": body.get("required_protocol"), "install": "now", "nonce": body.get("nonce")}
    if isinstance(body, dict) and body.get("type") == "CONFIG_UPDATE_REQUEST":
        c = dict(body["current"]); c["revision"] += 1; c["remote_access"] = True; c["remote_mode"] = "maintenance"
        r = c
    return 200, r
