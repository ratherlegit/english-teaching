#!/usr/bin/env python3
"""Transcribe a WAV locally with faster-whisper (nothing is uploaded).

Usage: transcribe.py <lesson.wav> <out.txt> [--model DIR_OR_NAME] [--glossary FILE]
Output lines look like "[mm:ss] text". Long lessons take roughly 10-20 minutes
on CPU, so run it in the background. Run with `python3 -I`.
--glossary FILE: a text file of names and terms that Whisper tends to mishear for this
student (client and team names, acronyms, places, jargon), separated by commas or new
lines. They are passed to faster-whisper as hotwords on every audio window, which makes
the model much more likely to spell them correctly. Keep it short (about 30 terms).
Default model: ~/.cache/whisper/faster-whisper-large-v3-turbo (falls back to the
model name "large-v3-turbo", which downloads once).
"""
import sys
from pathlib import Path
from faster_whisper import WhisperModel

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    wav, out = args[0], args[1]
    model = None
    if "--model" in args:
        model = args[args.index("--model") + 1]
    if model is None:
        local = Path.home() / ".cache/whisper/faster-whisper-large-v3-turbo"
        model = str(local) if local.exists() else "large-v3-turbo"
    hotwords = None
    if "--glossary" in args:
        raw = Path(args[args.index("--glossary") + 1]).expanduser().read_text(encoding="utf-8")
        terms = [t.strip() for t in raw.replace("\n", ",").split(",") if t.strip()]
        hotwords = ", ".join(terms[:40]) or None
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="en", vad_filter=True, beam_size=5,
                           condition_on_previous_text=False, hotwords=hotwords)
    with open(out, "w") as f:
        for s in segs:
            f.write(f"[{int(s.start // 60):02d}:{int(s.start % 60):02d}] {s.text.strip()}\n")
            f.flush()
    print("done")

if __name__ == "__main__":
    main()
