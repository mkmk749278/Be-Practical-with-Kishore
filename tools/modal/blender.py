"""Blender Cycles hero shots on a Modal GPU (PLAYBOOK §10.3, §14.1): the GitHub runner only launches.

    modal run tools/modal/blender.py --script phwr_hero --shot face --frames 0-599 --step 1 --shards 6 \
        --extra "--w 2560 --h 1440 --samples 128 --noise 0.02" --outdir out [--gpu L4]

The frame range is split into --shards contiguous pieces, one GPU container each; every frame comes back as a 16-bit
PNG named <shot>_<frame>.png. bpy 5.2.2 (Python 3.13) with OptiX; textures are fetched from Poly Haven inside the
container (scripts/blender/ph_assets.py). The log prints seconds per frame, so a 10-frame bench gives the cost:
seconds per frame × frames × the GPU's rate (L4 about US$0.80/h, 2026) — written in the handoff before a full run.
"""
import pathlib
import time

import modal

ROOT = pathlib.Path(__file__).resolve().parents[2]
image = (
    modal.Image.debian_slim(python_version="3.13")
    .apt_install("libx11-6", "libxrender1", "libxxf86vm1", "libxfixes3", "libxi6", "libxkbcommon0", "libsm6",
                 "libgl1", "libegl1", "libgomp1")
    .pip_install("bpy==5.2.2", "pillow==11.3.0")
    .add_local_dir(str(ROOT / "scripts" / "blender"), "/work/scripts/blender")
)
app = modal.App("bpk-blender", image=image)


def _render(script, shot, lo, hi, step, extra, gpu):
    import subprocess
    import tempfile

    out = {}
    with tempfile.TemporaryDirectory() as d:
        cmd = ["python", f"/work/scripts/blender/{script}.py", "--shot", shot, "--out", d,
               "--frames", f"{lo}-{hi}", "--step", str(step), *extra.split()] + (["--gpu"] if gpu else [])
        t = time.time()
        subprocess.run(cmd, check=True, cwd="/work")
        files = sorted(pathlib.Path(d).glob("*.png"))
        n = len(files)
        print(f"{shot} {lo}-{hi}: {n} frames in {time.time() - t:.0f} s ({(time.time() - t) / max(n, 1):.1f} s a frame)")
        for f in files:
            out[f.name] = f.read_bytes()
    return out


@app.function(gpu="L4", timeout=6 * 3600)
def render_l4(script: str, shot: str, lo: int, hi: int, step: int, extra: str):
    return _render(script, shot, lo, hi, step, extra, True)


@app.local_entrypoint()
def main(script: str, shot: str, frames: str, outdir: str, step: int = 1, shards: int = 1, extra: str = ""):
    lo, hi = map(int, frames.split("-"))
    n = hi - lo + 1
    size = -(-n // shards)
    jobs = [(script, shot, a, min(a + size - 1, hi), step, extra) for a in range(lo, hi + 1, size)]
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    t = time.time()
    total = 0
    for res in render_l4.starmap(jobs):
        for name, data in res.items():
            (out / name).write_bytes(data)
            total += 1
    print(f"done: {total} frames in {time.time() - t:.0f} s wall, {len(jobs)} L4 containers")
