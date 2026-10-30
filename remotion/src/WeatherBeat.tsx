// Remotion WeatherBeat composition
// Consumes beat JSON produced by scripts/beat-from-ocr.py
// Brand: Cloud Computer AI.com only

import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

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
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a1628',
        color: 'white',
        fontFamily: 'system-ui, sans-serif',
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      <div style={{ opacity }}>
        <div style={{ fontSize: 48, fontWeight: 700, marginBottom: 20 }}>
          Cloud Computer AI.com
        </div>
        <h1 style={{ fontSize: 72, margin: 0 }}>{props.headline || 'Weather Beat'}</h1>
        <h2 style={{ fontSize: 48, fontWeight: 400, margin: '10px 0 30px' }}>{props.subhead || ''}</h2>
        {props.stale && (
          <div style={{ color: '#ffaa00', fontSize: 36, fontWeight: 700 }}>STALE — SAFE SLATE</div>
        )}
        <div style={{ marginTop: 40, fontSize: 24, opacity: 0.7 }}>
          Source: {props.sourceMode || 'poc_fox'} · Frame {frame}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export default WeatherBeat;
