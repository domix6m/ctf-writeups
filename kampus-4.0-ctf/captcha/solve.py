#!/usr/bin/env python3
"""
Impostor CAPTCHA solver (CTF).

Each video is random black/white dot noise. The background noise scrolls in one
direction (e.g. down 3px/frame) while the glyph pixels scroll the opposite way.
A single frame looks like pure noise, and a naive frame-diff shows decoy
("impostor") text - but per-pixel motion consistency isolates the real string:

  match_d(y,x) = mean_t [ frame_t(y,x) == frame_{t+1}(y+dy, x+dx) ]

For the two dominant shifts, the one covering the smaller area is the text.
The mask is cleaned, split into glyphs and classified by template matching
against glyphs rendered from system sans-serif bold fonts.

usage:  python solve.py [URL]           # solve a live round
        python solve.py --file a.webm   # just OCR a local video
"""
import io, sys, time, string, argparse
from concurrent.futures import ThreadPoolExecutor

import av, cv2, numpy as np, requests
from PIL import Image, ImageDraw, ImageFont

URL = "https://captcha-04ef1cbb74ef.inst.zerodayctf.pl"
CHARSET = string.ascii_uppercase + string.digits
FONTS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf",
]
GW, GH = 28, 36  # normalized glyph size


# ---------- motion -> mask ----------
def decode(data: bytes) -> np.ndarray:
    c = av.open(io.BytesIO(data))
    return np.stack([f.to_ndarray(format="gray") for f in c.decode(video=0)]) < 128


def motion_mask(b: np.ndarray, R: int = 5) -> np.ndarray:
    # 1) find the two dominant shifts cheaply on a few frame pairs
    sub = b[:6]
    glob = {}
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            glob[(dy, dx)] = (sub[:-1] == np.roll(sub[1:], (-dy, -dx), axis=(1, 2))).mean()
    top = sorted(glob, key=glob.get, reverse=True)[:2]
    # 2) full per-pixel maps only for those two; minority-area motion = text
    maps = {k: (b[:-1] == np.roll(b[1:], (-k[0], -k[1]), axis=(1, 2))).mean(0) for k in top}
    m = min(maps.values(), key=lambda v: (v > 0.8).mean())
    mask = (m > 0.7).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    return mask


# ---------- segmentation ----------
def segment(mask: np.ndarray):
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
    comps = [i for i in range(1, n) if st[i, 4] > 250 and st[i, 3] > 25]
    # merge components overlapping horizontally (broken glyphs)
    comps.sort(key=lambda i: st[i, 0])
    groups = []
    for i in comps:
        x, w = st[i, 0], st[i, 2]
        if groups:
            gx0, gx1, ids = groups[-1]
            if x < gx1 - 4:
                groups[-1] = (gx0, max(gx1, x + w), ids + [i]); continue
        groups.append((x, x + w, [i]))
    glyphs = []
    for x0, x1, ids in groups:
        g = np.isin(lab, ids).astype(np.uint8)
        ys, xs = np.nonzero(g)
        glyphs.append(g[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    return glyphs


def norm(g: np.ndarray) -> np.ndarray:
    h, w = g.shape
    s = GH / max(h, w * GH / GW)
    nh, nw = max(1, round(h * s)), max(1, round(w * s))
    r = cv2.resize(g.astype(np.float32), (nw, nh), interpolation=cv2.INTER_AREA)
    out = np.zeros((GH, GW), np.float32)
    y0, x0 = (GH - nh) // 2, (GW - nw) // 2
    out[y0:y0 + nh, x0:x0 + nw] = r
    return out


# ---------- templates ----------
def build_templates():
    T = []
    for fp in FONTS:
        try:
            font = ImageFont.truetype(fp, 64)
        except OSError:
            continue
        for ch in CHARSET:
            im = Image.new("L", (120, 120), 0)
            ImageDraw.Draw(im).text((20, 10), ch, font=font, fill=255)
            a = (np.array(im) > 127).astype(np.uint8)
            ys, xs = np.nonzero(a)
            g = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            for k in (0, 1):  # slight dilation variant (noisy masks look bolder)
                gg = cv2.dilate(g, np.ones((3, 3), np.uint8)) if k else g
                T.append((ch, norm(gg), g.shape[1] / g.shape[0]))
    return T


TEMPLATES = build_templates()


def classify(g: np.ndarray) -> str:
    v = norm(g); ar = g.shape[1] / g.shape[0]
    best, bc = -1e9, "?"
    for ch, t, tar in TEMPLATES:
        s = -np.abs(v - t).sum() - 40 * abs(np.log(ar / tar))
        if s > best:
            best, bc = s, ch
    return bc


def solve_video(data: bytes) -> str:
    return "".join(classify(g) for g in segment(motion_mask(decode(data))))


# ---------- network ----------
def run(url: str):
    s = requests.Session()
    t0 = time.time()
    rnd = s.post(url + "/api/new").json()
    with ThreadPoolExecutor(len(rnd["videos"])) as ex:
        blobs = list(ex.map(lambda p: s.get(url + p).content, rnd["videos"]))
        answers = list(ex.map(solve_video, blobs))
    print(f"answers={answers}  ({time.time() - t0:.2f}s, limit {rnd.get('limit')}s)")
    r = s.post(url + "/api/submit", json={"id": rnd["id"], "answers": answers})
    print(f"server: {r.text.strip()}  total {time.time() - t0:.2f}s")
    return r.json()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", default=URL)
    ap.add_argument("--file", nargs="*")
    ap.add_argument("--tries", type=int, default=5)
    a = ap.parse_args()
    if a.file:
        for f in a.file:
            print(f, solve_video(open(f, "rb").read()))
    else:
        for i in range(a.tries):
            if run(a.url.rstrip("/")).get("ok"):
                break
