"""Resemble Enhance on a Modal GPU: clean and widen narration takes (PLAYBOOK §7, §14.1).

Run from .github/workflows/modal-enhance.yml (the runner only launches; the GPU does the work), or anywhere with
MODAL_TOKEN_ID / MODAL_TOKEN_SECRET set:
    modal run tools/modal/enhance.py --indir in --outdir out [--nfe 64 --lambd 0.1 --tau 0.5]
Every audio file in --indir comes back as <name>_enh.wav (44.1 kHz mono) in --outdir.

Settings: Resemble's own defaults for clean speech (midpoint solver, 64 steps, prior temperature 0.5) with light
denoising (lambd 0.1): ElevenLabs takes have no room noise, so the job is clarity and top end, not noise removal.
Cost: a T4 at about US$0.59/h; a 10-minute take is a few GPU minutes, about US$0.05 (inside the free credit).
The package's training-only DeepSpeed import is stubbed; inference never touches it.
"""
import pathlib

import modal

MODEL_DIR = "/model"
STUB = {
    "deepspeed/__init__.py": "class DeepSpeedConfig:\n    def __init__(self, *a, **k): pass\n"
                             "def init_distributed(*a, **k): pass\n",
    "deepspeed/accelerator.py": "def get_accelerator():\n    class A:\n"
                                "        def communication_backend_name(self): return 'nccl'\n    return A()\n",
    "deepspeed/runtime/__init__.py": "",
    "deepspeed/runtime/engine.py": "class DeepSpeedEngine: pass\n",
    "deepspeed/runtime/utils.py": "def clip_grad_norm_(*a, **k): pass\n",
}
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libsndfile1")
    .pip_install("torch==2.1.1", "torchaudio==2.1.1", index_url="https://download.pytorch.org/whl/cu121")
    .pip_install("numpy==1.26.2", "scipy==1.11.4", "librosa==0.10.1", "soundfile==0.12.1", "omegaconf==2.3.0",
                 "resampy==0.4.2", "tqdm==4.66.1", "rich==13.7.0", "matplotlib==3.8.1", "pandas==2.1.3",
                 "tabulate==0.8.10", "huggingface_hub==0.26.2")
    .pip_install("resemble-enhance==0.0.1", extra_options="--no-deps")
    .run_commands("python -c \"from huggingface_hub import snapshot_download; "
                  f"snapshot_download('ResembleAI/resemble-enhance', allow_patterns=['enhancer_stage2/*'], "
                  f"local_dir='{MODEL_DIR}')\"")
)
app = modal.App("bpk-enhance", image=image)


@app.function(gpu="T4", timeout=1800)
def enhance_one(name: str, data: bytes, nfe: int, lambd: float, tau: float) -> bytes:
    import io
    import subprocess
    import tempfile
    import sys
    import time

    for path, body in STUB.items():
        f = pathlib.Path("/tmp/stub", path)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body)
    sys.path.insert(0, "/tmp/stub")
    import torch
    import torchaudio
    from resemble_enhance.enhancer.inference import enhance

    with tempfile.TemporaryDirectory() as d:
        src, wav = pathlib.Path(d, name), pathlib.Path(d, "in.wav")
        src.write_bytes(data)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", str(wav)], check=True)
        dwav, sr = torchaudio.load(str(wav))
        t = time.time()
        out, osr = enhance(dwav.mean(0), sr, "cuda", nfe=nfe, solver="midpoint", lambd=lambd, tau=tau,
                           run_dir=pathlib.Path(MODEL_DIR, "enhancer_stage2"))
        print(f"{name}: {dwav.shape[1] / sr:.1f} s of audio in {time.time() - t:.1f} s, {osr} Hz")
        buf = io.BytesIO()
        torchaudio.save(buf, out.unsqueeze(0).cpu(), osr, format="wav", bits_per_sample=24)
        return buf.getvalue()


@app.local_entrypoint()
def main(indir: str, outdir: str, nfe: int = 64, lambd: float = 0.1, tau: float = 0.5):
    files = sorted(p for p in pathlib.Path(indir).iterdir() if p.suffix.lower() in (".mp3", ".wav", ".flac"))
    if not files:
        raise SystemExit(f"no audio in {indir}")
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    args = [(p.name, p.read_bytes(), nfe, lambd, tau) for p in files]
    for p, data in zip(files, enhance_one.starmap(args)):
        dst = out / f"{p.stem.removesuffix('_raw')}_enh.wav"
        dst.write_bytes(data)
        print(f"wrote {dst} ({len(data) / 1e6:.1f} MB)")
