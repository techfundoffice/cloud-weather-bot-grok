#!/usr/bin/env python3
"""Turn OCR text into a weather beat JSON document.

Usage: beat-from-ocr.py OCR.txt [--engine grok|gemini] [-o beat.json]
Default engine is grok: a local writer. It does not call the network.
Gemini is optional and refuses to run unless GEMINI_API_KEY is set.
The key is never printed.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def beat_from_text(text, source_mode="poc_fox"):
    lines = [ln.strip() for ln in text.splitlines()]
    body = [ln for ln in lines if ln]
    headline = body[0] if body else ""
    subhead = body[1] if len(body) > 1 else ""
    blob = "\n".join(body)
    stale = (not body) or ("STALE" in blob.upper())
    return {
        "schemaVersion": 1,
        "beatId": "",
        "producedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "headline": "" if stale else headline,
        "subhead": "" if stale else subhead,
        "regions": [],
        "temps": {},
        "alert": None,
        "ocrText": blob,
        "captionsExcerpt": "",
        "voiceScript": "" if stale else f"Cloud Computer AI.com. {headline}".strip(),
        "sourceMode": source_mode,
        "stale": stale,
        "segmentPath": "",
        "durationSec": 0,
        "playoutState": "slate" if stale else "live",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ocr")
    p.add_argument("--engine", choices=("grok", "gemini"), default="grok")
    p.add_argument("--source-mode", default="poc_fox")
    p.add_argument("-o", dest="out")
    p.add_argument("--beat-id", default="")
    args = p.parse_args(argv)
    if args.engine == "gemini" and not os.environ.get("GEMINI_API_KEY"):
        print("gemini engine needs GEMINI_API_KEY; key not printed", file=sys.stderr)
        return 2
    text = open(args.ocr, encoding="utf-8").read() if args.ocr != "-" else sys.stdin.read()
    doc = beat_from_text(text, args.source_mode)
    if args.beat_id:
        doc["beatId"] = args.beat_id
    raw = json.dumps(doc, indent=2) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(raw)
    else:
        sys.stdout.write(raw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
