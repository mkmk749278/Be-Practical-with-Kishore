#!/usr/bin/env python3
"""Upload a finished film to the channel from its youtube/metadata.json (PLAYBOOK §15). Rebuilt 27 NOV 2026 (the old
script was lost with `Creator`).

  python3 scripts/yt_upload.py projects/<slug> FILM.mp4 [--publish-at 2026-11-27T19:00+05:30] [--dry-run]

Uploads as Private (resumable, 64 MB chunks), sets title, description, tags, category, language, made-for-kids No,
the AI-use answer (`containsSyntheticMedia`, §8), and, with --publish-at, schedules it (Private until then). Then the
main thumbnail, our SRT (as "English") and the film's playlist. Prints the video id; writes it to youtube/upload.json.
Not possible through the API, so left for Studio: Test & Compare challengers, the end screen, pinning a comment.

  python3 scripts/yt_upload.py projects/<slug> --comment VIDEO_ID   posts the pinned comment and its sources reply

Needs YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE (scope youtube.force-ssl).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.googleapis.com/youtube/v3/"
UP = "https://www.googleapis.com/upload/youtube/v3/"
CHUNK = 64 * 1024 * 1024
_tok = {"t": None, "exp": 0}


def token() -> str:
    if time.time() < _tok["exp"]:
        return _tok["t"]
    d = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                "refresh_token": os.environ["YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE"],
                                "grant_type": "refresh_token"}).encode()
    r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=60))
    _tok.update(t=r["access_token"], exp=time.time() + r.get("expires_in", 3600) - 300)
    return _tok["t"]


def call(method: str, url: str, body=None, ctype="application/json", headers=None, raw=False):
    data = json.dumps(body).encode() if isinstance(body, (dict, list)) else body
    h = {"Authorization": "Bearer " + token(), **(headers or {})}
    if data is not None:
        h["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    for attempt in range(5):
        try:
            resp = urllib.request.urlopen(req, timeout=600)
            return resp if raw else json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            if raw and e.code == 308:
                return e
            msg = e.read()[:500]
            if e.code >= 500 and attempt < 4:
                time.sleep(2 ** attempt * 5)
                continue
            sys.exit(f"{method} {url.split('?')[0]} -> {e.code}: {msg!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 4:
                time.sleep(2 ** attempt * 5)
                continue
            raise


def upload_video(path: Path, meta: dict, publish_at: str | None) -> str:
    snippet = {"title": meta["title"], "description": meta["description"], "tags": meta.get("tags", []),
               "categoryId": meta.get("category_id", "28"), "defaultLanguage": meta.get("default_language", "en"),
               "defaultAudioLanguage": meta.get("default_audio_language", "en")}
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": bool(meta.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(meta.get("contains_synthetic_media", False)), "embeddable": True,
              "license": "youtube"}
    if publish_at:
        status["publishAt"] = publish_at
    size = path.stat().st_size
    start = call("POST", UP + "videos?uploadType=resumable&part=snippet,status", {"snippet": snippet, "status": status},
                 headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, raw=True)
    session = start.headers["Location"]
    sent = 0
    with path.open("rb") as f:
        while sent < size:
            f.seek(sent)
            chunk = f.read(CHUNK)
            end = sent + len(chunk) - 1
            r = call("PUT", session, chunk, ctype="video/mp4", raw=True,
                     headers={"Content-Range": f"bytes {sent}-{end}/{size}"})
            if getattr(r, "code", getattr(r, "status", 0)) in (200, 201):
                vid = json.loads(r.read())["id"]
                print(f"  uploaded {size / 1e9:.2f} GB -> {vid}")
                return vid
            rng = r.headers.get("Range")
            sent = int(rng.split("-")[1]) + 1 if rng else 0
            print(f"  {sent / size:5.1%}", flush=True)
    sys.exit("upload ended without a video id")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--publish-at")
    ap.add_argument("--comment", metavar="VIDEO_ID")
    ap.add_argument("--finish", metavar="VIDEO_ID", help="only the steps after the upload (thumbnail, SRT, playlist)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    film = Path(a.film)
    meta = json.loads((film / "youtube/metadata.json").read_text())
    if a.comment:
        top = call("POST", API + "commentThreads?part=snippet", {"snippet": {"videoId": a.comment, "topLevelComment": {
            "snippet": {"textOriginal": meta["pinned_comment"]}}}})
        cid = top["id"]
        call("POST", API + "comments?part=snippet", {"snippet": {"parentId": cid, "textOriginal": meta["pinned_reply"]}})
        print("comment", cid, "and its sources reply posted; pin it in Studio")
        return
    if len(meta["title"]) > 100 or "<" in meta["description"]:
        sys.exit("title over 100 characters or '<' in the description")
    if a.dry_run:
        print(json.dumps({k: meta[k] for k in ("title", "tags", "playlist")}, ensure_ascii=False, indent=1))
        return
    vid = a.finish or upload_video(Path(a.video), meta, a.publish_at)
    th = film / meta["thumbnails"]["main"]
    call("POST", UP + f"thumbnails/set?videoId={vid}&uploadType=media", th.read_bytes(), ctype="image/jpeg")
    print("  thumbnail set")
    if meta.get("captions"):
        boundary = "srtboundary"
        body = (f"--{boundary}\r\nContent-Type: application/json\r\n\r\n" + json.dumps(
            {"snippet": {"videoId": vid, "language": "en", "name": "English"}}) +
            f"\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + \
            (film / meta["captions"]).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        call("POST", UP + "captions?uploadType=multipart&part=snippet", body, ctype=f"multipart/related; boundary={boundary}")
        print("  captions uploaded")
    if meta.get("playlist", {}).get("id"):
        call("POST", API + "playlistItems?part=snippet", {"snippet": {"playlistId": meta["playlist"]["id"],
                                                                     "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        print("  added to", meta["playlist"]["title"])
    if a.finish and (film / "youtube/upload.json").exists():
        print(f"https://youtu.be/{vid}")
        return
    (film / "youtube/upload.json").write_text(json.dumps({"video_id": vid, "publish_at": a.publish_at,
                                                          "uploaded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=1) + "\n")
    print(f"https://youtu.be/{vid}")


if __name__ == "__main__":
    main()
