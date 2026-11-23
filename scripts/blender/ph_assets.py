"""Poly Haven (CC0) textures and HDRIs for the Blender hero shots, fetched on demand into library/ph/ (gitignored).

  python scripts/blender/ph_assets.py metal_plate rusty_metal_02 ...      # prefetch (also runs inside Blender)

Every file comes from the Poly Haven API at a fixed resolution; the runners fetch the same files, so a render is the
same in a session and on GitHub. Licence: CC0 (https://polyhaven.com/license); logged in library/manifest.csv.
"""
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "library", "ph")
UA = {"User-Agent": "CreatorDocBot/1.0 (documentary renders)"}
MAPS = {"diff": ("Diffuse", "jpg"), "rough": ("Rough", "jpg"), "nor": ("nor_gl", "jpg"), "disp": ("Displacement", "png"),
        "metal": ("Metal", "jpg"), "arm": ("arm", "jpg")}


def _get(url, dest):
    for k in range(5):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r, open(dest + ".part", "wb") as f:
                f.write(r.read())
            os.replace(dest + ".part", dest)
            return dest
        except Exception as e:  # noqa: BLE001 - retried, then raised
            if k == 4:
                raise RuntimeError(f"Poly Haven fetch failed: {url}: {e}")
            time.sleep(3 * (k + 1))


def _files(asset):
    p = os.path.join(CACHE, f"{asset}.files.json")
    if not os.path.exists(p):
        os.makedirs(CACHE, exist_ok=True)
        _get(f"https://api.polyhaven.com/files/{asset}", p)
    return json.load(open(p))


def texture(asset, res="2k"):
    """{map: path} for the maps the asset has (diff, rough, nor, disp, metal)."""
    fl, out = _files(asset), {}
    for key, (name, ext) in MAPS.items():
        if name not in fl or res not in fl[name] or ext not in fl[name][res]:
            continue
        dest = os.path.join(CACHE, f"{asset}_{key}_{res}.{ext}")
        if not os.path.exists(dest):
            _get(fl[name][res][ext]["url"], dest)
        out[key] = dest
    return out


def hdri(asset, res="2k"):
    dest = os.path.join(CACHE, f"{asset}_{res}.hdr")
    if not os.path.exists(dest):
        _get(_files(asset)["hdri"][res]["hdr"]["url"], dest)
    return dest


if __name__ == "__main__":
    for a in sys.argv[1:]:
        kind, name = a.split(":") if ":" in a else ("tex", a)
        print(a, hdri(name) if kind == "hdri" else texture(name))
