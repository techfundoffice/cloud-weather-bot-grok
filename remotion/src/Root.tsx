import React from 'react';
import { Composition } from 'remotion';
import { WeatherBeat, BeatProps } from './WeatherBeat';

const defaultProps: BeatProps = {
  schemaVersion: '1.0',
  beatId: 'demo-001',
  headline: 'Storms west of Dallas',
  subhead: 'Wind 40 mph',
  sourceMode: 'poc_fox',
  stale: false,
  voiceScript: 'Cloud Computer AI.com. Storms west of Dallas with winds of 40 miles per hour.',
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="WeatherBeat"
        component={WeatherBeat}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={defaultProps}
      />
    </>
  );
};
