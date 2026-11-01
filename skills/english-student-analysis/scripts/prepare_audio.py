#!/usr/bin/env python3
"""Turn a lesson recording into one 16 kHz mono WAV ready for transcription.

Handles: a single audio/video file, a folder of chunks, or a zip archive (even
one with no .zip extension, like exported "lesson_recordings" bundles of
part_01.webm ... part_20.webm). Chunks are joined in natural sort order.

Usage: prepare_audio.py <input> <out_dir>
Creates <out_dir>/raw (extracted files) and <out_dir>/lesson.wav.
<out_dir> must be new or empty. Run with `python3 -I`.
"""
import re, subprocess, sys, zipfile
from pathlib import Path

AUDIO = {".webm", ".m4a", ".mp3", ".wav", ".mp4", ".mov", ".ogg", ".aac", ".flac", ".mkv"}

def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty; use a new folder (downloads are untrusted data)")
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        files = [p for p in src.rglob("*") if p.suffix.lower() in AUDIO]
    elif zipfile.is_zipfile(src):
        with zipfile.ZipFile(src) as z:
            for m in z.namelist():  # reject path traversal
                if m.startswith("/") or ".." in Path(m).parts:
                    sys.exit(f"unsafe path in archive: {m}")
            z.extractall(raw)
        files = [p for p in raw.rglob("*") if p.suffix.lower() in AUDIO]
    else:
        files = [src]
    files = sorted(files, key=natural)
    if not files:
        sys.exit("no audio or video files found")
    print(f"{len(files)} file(s):", ", ".join(f.name for f in files))

    lst = out / "list.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    wav = out / "lesson.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-ac", "1", "-ar", "16000", str(wav)], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout.strip()
    print(f"wrote {wav} ({float(dur)/60:.1f} min)")

if __name__ == "__main__":
    main()
