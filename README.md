# Cloud Computer AI.com Weather Channel — Grok Bot factory (Debian)

Automation + OCR/change-detect scripts that run on the Grok Bot Debian computer.

## FOX fullscreen opener (Playwright)

```bash
cd automation
npm install
DISPLAY=:7 KEEP_OPEN=1 node open-fox-fullscreen.mjs
```

Opens system Chrome → FOX Weather YouTube live → YouTube fullscreen (`f`).

**Note:** On the Grok Bot desktop, live GUI control also goes through the desktop helper; this script is the portable recipe.

## Frame keep policy

Keep a frame whenever pixels change enough to include countdown digits (`scripts/frames-on-change.py`, threshold 0.5). See `docs/FRAME-KEEP-POLICY.md`.

## Capture SOP

Always YouTube **fullscreen** before record. See `docs/CAPTURE-SOP.md`.

Brand spoken name: **Cloud Computer AI.com** (never CCAI/CCIA).
