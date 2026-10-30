// Minimal Remotion WeatherBeat composition scaffold
// Consumes beat JSON produced by scripts/beat-from-ocr.py
// Next: full React components, branding, render pipeline per SOFTWARE-SPEC.md

import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export interface BeatProps {
  schemaVersion?: string;
  beatId?: string;
  headline?: string;
  subhead?: string;
  ocrText?: string;
  voiceScript?: string;
  sourceMode?: 'poc_fox' | 'licensed';
  stale?: boolean;
}

export const WeatherBeat: React.FC<BeatProps> = (props) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a1628', color: 'white', padding: 40 }}>
      <h1>{props.headline || 'Weather Beat'}</h1>
      <h2>{props.subhead || ''}</h2>
      <p>Frame: {frame}</p>
      <p>Source: {props.sourceMode || 'poc_fox'}</p>
      {props.stale && <p style={{ color: 'orange' }}>STALE</p>}
    </AbsoluteFill>
  );
};

export default WeatherBeat;
