# Remotion WeatherBeat

Minimal self-hosted Remotion composition for Cloud Computer AI.com weather beats.

## Setup

```bash
cd remotion
npm install
```

## Preview

```bash
npm start
```

## Render

```bash
npm run render
# or with custom props:
# npx remotion render src/index.ts WeatherBeat out/beat.mp4 --props='{"headline":"Clear skies"}'
```

Brand rule: spoken and on-screen name is always **Cloud Computer AI.com**.

See parent SOFTWARE-SPEC.md for full pipeline.
