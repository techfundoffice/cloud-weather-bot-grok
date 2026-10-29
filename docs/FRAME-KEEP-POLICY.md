# Frame keep policy

Keep a frame when the fraction of changed pixels is at least **0.5%** (`0.005`).

That threshold is low enough to catch countdown digits and high enough to drop a duplicate still.

`scripts/frames-on-change.py` reads P6 PPM frames in name order. The first frame is always kept. Later frames are kept only when they cross the threshold. The script does not call a network.

```bash
python3 scripts/frames-on-change.py data/frames data/kept --threshold 0.005
```
