# Cloud Computer AI.com Weather Channel — Software Specification

**Document status:** Locked plan (2026-09-10) — Architect revision: YouTube LIVE end deliverable  
**Product name:** Cloud Computer AI.com Weather Channel  
**End deliverable (production goal):** A **YouTube LIVE weather station** — continuous LIVE stream, Cloud Computer AI.com branded, corporation-ready  
**Orchestrator / software architect agent:** Grok Cloud Computer AI Weather Bot (this machine)  
**Brand speech rule:** On-air audio always says **Cloud Computer AI.com** in full (never CCAI / CCIA).  
**This document is a software spec, not legal advice.**

---

## 0. Primary deliverable

| | |
|--|--|
| **Goal** | Generate and operate a **YouTube LIVE weather station** (24/7 capable) |
| **On-air look** | Owned React → Remotion → video (not a third-party network rebroadcast) |
| **Operator** | Grok Cloud Computer AI Weather Bot oversees the whole factory |
| **POC fuel** | FOX Weather YouTube live (temporary only) |
| **POC playout** | **gods-eye-view (Replit)** — already written; use it to prove the factory end-to-end |
| **Production fuel** | Paid weather data/video license (FOX removed) |
| **Production playout (LAST step)** | **YouTube LIVE** weather station (after POC on gods-eye-view works) |

Factory first → gods-eye-view POC air → **YouTube LIVE last**.

---

## 1. Purpose

Build the software factory that:

1. Ingests weather (POC: FOX capture; PROD: licensed feed)  
2. Structures beats (OCR → Gemini → JSON)  
3. Renders owned channel segments (Remotion h264)  
4. **POC:** Ship segments into **gods-eye-view** (already built) to prove air  
5. **LAST:** Continuous **YouTube LIVE** weather station (same segments / playout contract)  

gods-eye-view is the **POC playout + control surface**. YouTube LIVE is the **final** production playout step — not skipped, just last.

---

## 2. Scope

### 2.1 In scope
- Agent-orchestrated pipeline on Grok Bot’s Debian computer  
- POC screen capture (`ffmpeg` / optional OBS)  
- Local OCR (Tesseract) before Gemini  
- Gemini → JSON-serializable weather beat props  
- Self-hosted Remotion (React → h264 MP4 segments)  
- **YouTube LIVE encoder / continuous playout** (RTMP or WHIP)  
- Failover safe slate, STALE policy, start/stop ownership  
- Ship/mirror to gods-eye-view  
- Remotion license awareness (free ≤3-person for-profit; company license at 4+)  
- Cutover path: FOX → paid weather license without rewriting Remotion contracts  

### 2.2 Out of scope (POC)
- Lecture video→PPT tools as core  
- PNG-only final air product  
- Watcher/Hermes as primary Remotion factory  
- Marketing POC as copyright-clear corporate LIVE  

### 2.3 Non-goals for production LIVE
- FOX (or any network) pixels/audio in the YouTube LIVE air chain  
- LIVE without written weather license after POC  
- Silent failures that keep a black/stale stream on YouTube  

---

## 3. Actors & systems

| ID | System | Role |
|----|--------|------|
| A1 | Grok Cloud Computer AI Weather Bot | Software architect + overseer: start/stop, retries, STALE, quality, LIVE health |
| A2 | Grok Bot computer (Debian) | Capture, OCR, Node, Remotion, encode/playout worker |
| A3 | Chrome (box) | POC only: FOX Weather YouTube (`wt6SIE7BXS8`) |
| A4 | Gemini API | Beat JSON from frames+OCR(+captions) or licensed data |
| A5 | Remotion (self-hosted) | React weather comps → h264 segments |
| A6 | gods-eye-view (Replit) | **POC playout** (already written) + ADMIN / control — not Remotion host |
| A7 | YouTube LIVE | **Final production playout** (weather station stream) — last step after POC |
| A8 | Paid weather license vendor | Production source (replaces FOX) |
| A9 | YouTube channel (company-owned) | Destination LIVE key / stream |

---

## 4. Environments & prerequisites

| Item | Requirement |
|------|-------------|
| OS | Debian, glibc ≥ 2.35 |
| Node | ≥ 16 (present v20.19.x) |
| Chrome | Present (POC + Remotion) |
| `ffmpeg` | Present (capture + **LIVE encode/restream**) |
| OBS | Optional GUI capture |
| Remotion | Scaffold under `/workspace/cloud-weather-bot/remotion` |
| Tesseract | Install for OCR |
| YouTube | LIVE enabled channel + stream key (company account for prod) |
| Gemini | Existing billing/keys |

---

## 5. Source strategy

### 5.1 POC (temporary)
FOX live on bot Chrome → prove factory → Remotion MP4s → optional test loop / dry-run playout.

### 5.2 Production (YouTube LIVE weather station)
- Remove FOX  
- Paid weather data/video license (written commercial + LIVE redistribution rights)  
- Same beat-JSON → Remotion → **continuous YouTube LIVE**  

---

## 6. End-to-end pipeline (YouTube LIVE oriented)

```
[Overseer: Cloud Weather Bot]
        |
        v
[1] Source ingest     POC: Chrome+FOX | PROD: licensed weather feed
[2] Capture/normalize POC: ffmpeg → 480p chunks ~30–45s
[3] Frame sample      ffmpeg → N frames
[4] Local OCR         Tesseract
[5] Beat author       Grok Bot (default on this computer) → beat JSON; Gemini optional
[6] Remotion compose  React Cloud Computer AI.com comps
[7] Remotion render   h264 segment MP4
[8] Quality gate      STALE/black/fail → safe slate (do not push junk LIVE)
[9] POC playout      ship segments → gods-eye-view (proof of concept air)
[10] FINAL playout    ffmpeg/RTMP|WHIP → YouTube LIVE (last step, production)
```

**Order:** prove on gods-eye-view first (program already exists). **YouTube LIVE is the last step** once the factory is proven.  
**Production loop (M3):** render next segment while current segment/slate holds YouTube LIVE continuity.

---

## 7. Functional requirements

### Factory
- **FR-1 Overseer** — bot owns pipeline + LIVE health  
- **FR-2 POC capture** — `ffmpeg` 480p chunks  
- **FR-3 Frame sample** — small N / chunk  
- **FR-4 OCR before Gemini**  
- **FR-5 Beat JSON** — serializable props only  
- **FR-6 Remotion compositions** — `Root.tsx`, `inputProps`, optional `calculateMetadata`  
- **FR-7 Render** — h264 via CLI or `renderMedia`/`selectComposition`  

### Playout
- **FR-8 Branding** — Cloud Computer AI.com only on air  
- **FR-9 POC playout** — ship proven MP4s into **gods-eye-view** (already written) as the POC air path  
- **FR-10 YouTube LIVE (LAST)** — after POC works, continuous RTMP/WHIP playout to YouTube LIVE  
- **FR-11 Stream health** — disconnect / silence / black → safe slate + alert (required for M3)  
- **FR-12 Failover** — backup encode or branded slate while rebuild  
- **FR-13 Cutover** — licensed ingest same JSON contract; FOX modules disabled  
- **FR-14 Independence** — Remotion stays on the bot; gods-eye-view does not host Remotion  

---

## 8. Remotion hosting & license

Self-host on bot (Node/React + Chrome). Remotion License: free ≤3-person for-profit; company license at 4+. No mandatory Remotion SaaS.

---

## 9. Data contracts

**Beat props:** `schemaVersion`, `beatId`, `producedAt`, `headline`, `subhead`, `regions[]`, `temps`, `alert`, `ocrText`, `captionsExcerpt`, `voiceScript`, `sourceMode` (`poc_fox`|`licensed`), `stale`.

**LIVE ops fields (add):** `segmentPath`, `durationSec`, `playoutState` (`live`|`slate`|`error`).

**Disk:**
```
/workspace/cloud-weather-bot/
  SOFTWARE-SPEC.md
  remotion/
  data/beats|chunks|frames|ocr/
  out/*.mp4
  live/          # playlist, slate, stream config (no secrets in git)
```

---

## 10. Non-functional

- POC on one machine  
- POC 480p–720p; LIVE resolution TBD (recommend 720p60 or 1080p30)  
- Restart-safe artifacts  
- Honest STALE — never present dead POC as LIVE weather  
- Audit logs for corp  
- Stream keys / API secrets never in git  

---

## 11. Acceptance

### POC factory
Start/stop capture; one full path to branded Remotion MP4; visible failures.

### POC playout (gods-eye-view)
1. Factory produces branded Remotion MP4s  
2. Segments air on gods-eye-view (existing program)  
3. Start/stop + STALE visible  

### YouTube LIVE weather station (final deliverable — last)
1. FOX removed; licensed source on same JSON contract  
2. Stable YouTube LIVE under Cloud Computer AI.com branding  
3. Failover slate works  
4. 24/7 ops checklist passes  
5. Corp/IP/YouTube ownership review with counsel  

---

## 12. Modes

| Mode | Name | Source | Output |
|------|------|--------|--------|
| M0 | Scaffold | — | Remotion + OCR + folders + live/ |
| M1 | POC factory | FOX (temporary) | Branded Remotion MP4s |
| M1b | POC playout | FOX → factory | **Air on gods-eye-view** (already written) |
| M2 | Licensed factory | Paid license | Same MP4s from clean data |
| M3 | **YouTube LIVE weather station** | Licensed only | **Continuous YouTube LIVE + ops (LAST step)** |

**M3 is the end-result deliverable; gods-eye-view is the POC air step (M1b), not the final substitute for YouTube LIVE.**

---

## 13. Rejected as core

Lecture slide repos; PNG-only air; Watcher-as-Remotion-host; “LIVE” that is only gods-eye-view without YouTube.

---

## 14. Open decisions

- Weather license vendor  
- Remotion seats if headcount ≥ 4  
- LIVE resolution / GOP / bitrate  
- Hermes voice mux into Remotion vs sidecar audio  
- Primary encoder: `ffmpeg` RTMP vs WHIP vs OBS  
- Multi-region backup bot  

---

## 15. Next build (when go)

1. Scaffold Remotion + `live/` layout  
2. Install Tesseract  
3. POC `ffmpeg` capture  
4. OCR → Gemini → `beat.json`  
5. `WeatherBeat` Composition + render  
6. Quality gate  
7. Ship to **gods-eye-view** (POC air — program already written)  
8. After factory+GEV POC: licensed ingest → cut FOX  
9. **LAST:** YouTube LIVE dry-run → M3 continuous LIVE  

---

*End of software specification. Architect: Grok Cloud Computer AI Weather Bot.*

### Beat author (2026-09-10)

On the **Grok Bot computer** factory, the default beat writer is **Grok Bot / Cloud Weather Bot** (`scripts/beat-from-ocr.py --engine grok`). Gemini remains optional (`--engine gemini`) and is still what gods-eye-view Hermes/Watcher uses on Replit.

### Capture SOP (locked)

**Always YouTube fullscreen before record** — no tabs, chat, or browser chrome in frame. See `docs/CAPTURE-SOP.md`.
