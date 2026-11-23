import React from "react";
import { Composition } from "remotion";
import { Bolum1, DURATION, FPS } from "./Bolum1";

export const RemotionRoot: React.FC = () => (
  <Composition id="Bolum1" component={Bolum1} durationInFrames={DURATION} fps={FPS} width={1080} height={1920} />
);
