# Capture SOP

Always put YouTube in **fullscreen** before record. No tabs, chat, or browser chrome in the frame.

1. Open the FOX Weather live video `wt6SIE7BXS8` in system Chrome.
2. Press `f` so the player is fullscreen.
3. Record only after fullscreen is up.
4. Brand speech is **Cloud Computer AI.com**. Never say CCAI or CCIA.

```bash
cd automation
npm install
DRY_RUN=1 node open-fox-fullscreen.mjs
DISPLAY=:7 KEEP_OPEN=1 node open-fox-fullscreen.mjs
```

`DRY_RUN=1` prints the URL and exits. It does not launch a browser.
