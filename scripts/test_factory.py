#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames-on-change.py"
BEAT = ROOT / "beat-from-ocr.py"


def ppm(w, h, rgb):
    header = f"P6\n{w} {h}\n255\n".encode()
    pixel = bytes(rgb)
    return header + pixel * (w * h)


def run(cmd):
    return subprocess.run([sys.executable, *cmd], capture_output=True, text=True)


def test_frames():
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src"
        dest = Path(tmp) / "dest"
        src.mkdir()
        black = ppm(4, 4, (0, 0, 0))
        (src / "a.ppm").write_bytes(black)
        (src / "b.ppm").write_bytes(black)
        changed = bytearray(black)
        changed[-3:] = b"\xff\xff\xff"
        (src / "c.ppm").write_bytes(changed)
        r = run([str(FRAMES), str(src), str(dest), "--threshold", "0.005"])
        assert r.returncode == 0, r.stderr
        names = sorted(p.name for p in dest.iterdir())
        assert names == ["a.ppm", "c.ppm"], names


def test_beat():
    with tempfile.TemporaryDirectory() as tmp:
        ocr = Path(tmp) / "ocr.txt"
        out = Path(tmp) / "beat.json"
        ocr.write_text("Storms west of Dallas\nWind 40 mph\n", encoding="utf-8")
        r = run([str(BEAT), str(ocr), "--beat-id", "b1", "-o", str(out)])
        assert r.returncode == 0, r.stderr
        doc = json.loads(out.read_text())
        assert doc["headline"] == "Storms west of Dallas"
        assert doc["stale"] is False
        assert doc["playoutState"] == "live"
        assert doc["voiceScript"].startswith("Cloud Computer AI.com.")
        assert "CCAI" not in doc["voiceScript"]
        ocr.write_text("STALE frame\n", encoding="utf-8")
        r = run([str(BEAT), str(ocr), "-o", str(out)])
        assert r.returncode == 0
        doc = json.loads(out.read_text())
        assert doc["stale"] is True
        assert doc["playoutState"] == "slate"
        r = run([str(BEAT), str(ocr), "--engine", "gemini"])
        assert r.returncode == 2
        assert "GEMINI" not in r.stdout


if __name__ == "__main__":
    test_frames()
    test_beat()
    print("ok")
