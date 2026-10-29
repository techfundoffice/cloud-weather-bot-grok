#!/usr/bin/env python3
"""Keep a frame when enough pixels change to include countdown digits.

Usage: frames-on-change.py SRC_DIR DEST_DIR [--threshold 0.005]
Reads P6 PPM frames in sorted name order. The first frame is always kept.
A later frame is kept when the fraction of changed pixels is >= threshold.
Default threshold is 0.5% (0.005), the locked frame-keep policy.
"""
import argparse
import shutil
import sys
from pathlib import Path


def read_ppm(path):
    data = Path(path).read_bytes()
    if not data.startswith(b"P6"):
        raise ValueError(f"not a P6 PPM: {path}")
    i = 2
    tokens = []
    while len(tokens) < 3:
        while i < len(data) and data[i] in b" \t\r\n":
            i += 1
        if i < len(data) and data[i] == ord("#"):
            while i < len(data) and data[i] not in b"\r\n":
                i += 1
            continue
        start = i
        while i < len(data) and data[i] not in b" \t\r\n":
            i += 1
        tokens.append(data[start:i])
    width, height, maxval = (int(t) for t in tokens)
    if maxval > 255:
        raise ValueError("only 8-bit PPM is supported")
    if i < len(data) and data[i] in b" \t\r\n":
        i += 1
    need = width * height * 3
    pixels = data[i:i + need]
    if len(pixels) != need:
        raise ValueError(f"short PPM pixel data: {path}")
    return width, height, pixels


def change_ratio(a, b):
    if a[0] != b[0] or a[1] != b[1]:
        return 1.0
    pa, pb = a[2], b[2]
    changed = 0
    total = a[0] * a[1]
    for i in range(0, len(pa), 3):
        if pa[i:i + 3] != pb[i:i + 3]:
            changed += 1
    return changed / total if total else 0.0


def select_frames(paths, threshold):
    kept = []
    previous = None
    for path in paths:
        frame = read_ppm(path)
        if previous is None or change_ratio(previous, frame) >= threshold:
            kept.append(path)
            previous = frame
    return kept


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("src")
    p.add_argument("dest")
    p.add_argument("--threshold", type=float, default=0.005)
    args = p.parse_args(argv)
    src = Path(args.src)
    dest = Path(args.dest)
    frames = sorted(x for x in src.iterdir() if x.suffix.lower() == ".ppm")
    if not frames:
        print("no PPM frames", file=sys.stderr)
        return 1
    dest.mkdir(parents=True, exist_ok=True)
    kept = select_frames(frames, args.threshold)
    for path in kept:
        shutil.copy2(path, dest / path.name)
    print(f"kept {len(kept)} of {len(frames)} (threshold {args.threshold})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
