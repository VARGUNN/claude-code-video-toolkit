import React from "react";
import { AbsoluteFill, Audio, Easing, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Puppet, Pose, Who } from "./Puppet";
import { Hallway, Salon, Suitcase } from "./Sets";
import envelopes from "./envelopes.json";

export const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);

type Line = { id: keyof typeof envelopes; who: Who | "kemal"; at: number; text: string; name?: string };

// The timeline: every line starts at a second, its length is its audio.
export const LINES: Line[] = [
  { id: "l01", who: "nermin", at: 0.25, text: "Topla eşyalarını. Bu evde senin gibi birine yer yok!", name: "Nermin Hanım" },
  { id: "l02", who: "zeynep", at: 3.65, text: "Nermin Hanım... Ben ne yaptım ki?", name: "Zeynep" },
  { id: "l03", who: "nermin", at: 6.45, text: "Fakir bir kızın oğlumu benden almasına izin vermeyeceğim." },
  { id: "l04", who: "emre", at: 10.3, text: "Anne, yeter artık!", name: "Emre" },
  { id: "l05", who: "nermin", at: 12.0, text: "Sen karışma Emre. Ya o gider, ya ben." },
  { id: "l06", who: "zeynep", at: 15.7, text: "Demek... susuyorsun." },
  { id: "l07", who: "kemal", at: 20.6, text: "Zeynep Hanım, babanızın vasiyeti açıldı. Holding artık sizin.", name: "Avukat Kemal (telefonda)" },
  { id: "l08", who: "zeynep", at: 25.6, text: "Yarın sabah dokuzda toplantı ayarlayın." },
  { id: "l09", who: "nermin", at: 28.3, text: "Oğlum, yarın yeni patronunla tanışıyorsun. Sakın beni mahcup etme." },
];

export const DURATION = s(37);

const lineAt = (frame: number) =>
  LINES.find((l) => frame >= s(l.at) && frame < s(l.at) + envelopes[l.id].frames);

const mouthOf = (who: Who, frame: number) => {
  const l = lineAt(frame);
  if (!l || l.who !== who) return 0;
  const env = envelopes[l.id].env;
  const i = frame - s(l.at);
  const v = ((env[i] ?? 0) + (env[i - 1] ?? 0)) / 2;
  return v < 0.15 ? 0 : Math.min(1, v * 1.1);
};

const blinkOf = (frame: number, offset: number) => {
  const p = (frame + offset) % 113;
  return p < 2 ? 0.6 : p < 4 ? 1 : p < 6 ? 0.5 : 0;
};

const ramp = (frame: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(frame, [s(a), s(b)], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });

const base = (who: Who, frame: number, offset: number): Pose => ({
  mouth: mouthOf(who, frame),
  blink: blinkOf(frame, offset),
  breathe: frame / 14 + offset,
});

// Camera: zoom around a scene point, placed at a screen point.
const Camera: React.FC<{ zoom: number; fx: number; fy: number; children: React.ReactNode }> = ({ zoom, fx, fy, children }) => {
  // keep the scene covering the frame: no empty edges
  const tx = Math.min(0, Math.max(1080 - 1080 * zoom, 540 - fx * zoom));
  const ty = Math.min(0, Math.max(1920 - 1920 * zoom, 760 - fy * zoom));
  return (
    <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${zoom})`, transformOrigin: "0 0" }}>
      {children}
    </AbsoluteFill>
  );
};

const Layer: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    <svg width={1080} height={1920} viewBox="0 0 1080 1920">
      {children}
    </svg>
  </AbsoluteFill>
);

const FEET = 1720;
const face = (x: number, sc = 1) => ({ fx: x, fy: FEET - 880 * sc });

// Shot boundaries in seconds.
const SH = { A: 0, B: 3.5, C: 6.3, D: 9.5, E: 15.6, F: 18.3, G: 28.0, H: 33.0, END: 37 };

const SalonScene: React.FC<{ frame: number }> = ({ frame }) => {
  const t = frame / FPS;
  const inD = t >= SH.D;
  const zTears = ramp(frame, 4.4, 6.0);
  const emreX = interpolate(frame, [s(9.5), s(10.3)], [1250, 900], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const walk = t > 9.5 && t < 10.3 ? Math.sin(frame * 0.9) * 6 : 0;
  const nerminX = inD ? 280 : 330;
  const zeynepX = inD ? 640 : 760;
  const nerminPoint = t < 3.4 || (t > 12 && t < 14.6);
  const emreDown = t > 14.6;
  return (
    <AbsoluteFill>
      <Salon />
      <Layer>
        <Suitcase x={inD ? 470 : 560} y={1740} color="#2f8a7a" />
        <Puppet
          who="nermin"
          x={nerminX}
          y={FEET}
          pose={{
            ...base("nermin", frame, 7),
            brow: "angry",
            smile: -0.6,
            armR: nerminPoint ? [72, 8] : [8, 132],
            armL: nerminPoint ? [8, 6] : [8, 132],
            look: t > 10.2 && t < 15 ? 1 : 0.6,
          }}
        />
        <Puppet
          who="zeynep"
          x={zeynepX}
          y={FEET}
          flip
          pose={{
            ...base("zeynep", frame, 40),
            brow: "sad",
            smile: -0.4,
            tears: zTears,
            armL: [8, 128],
            headTilt: inD && t > 15 ? 6 : -3,
            look: inD && t > 15 ? -1 : 0.6,
          }}
        />
        {t >= 9.5 && (
          <Puppet
            who="emre"
            x={emreX}
            y={FEET + walk}
            flip
            pose={{
              ...base("emre", frame, 70),
              brow: emreDown ? "sad" : "angry",
              smile: -0.3,
              blink: emreDown ? 0.55 : blinkOf(frame, 70),
              headTilt: emreDown ? -8 : 0,
              armR: t > 10.3 && t < 11.8 ? [35, 40] : [6, 6],
              look: 0.8,
            }}
          />
        )}
      </Layer>
    </AbsoluteFill>
  );
};

const NerminEmre: React.FC<{ frame: number }> = ({ frame }) => (
  <AbsoluteFill>
    <Salon />
    <Layer>
      <Puppet
        who="nermin"
        x={400}
        y={FEET}
        pose={{ ...base("nermin", frame, 7), brow: "raised", smile: 0.7, armR: [30, 70], armL: [8, 132], look: 1 }}
      />
      <Puppet
        who="emre"
        x={700}
        y={FEET}
        flip
        pose={{ ...base("emre", frame, 70), brow: "sad", smile: -0.2, look: 0.7 }}
      />
    </Layer>
  </AbsoluteFill>
);

const HallScene: React.FC<{ frame: number; ending?: boolean }> = ({ frame, ending }) => {
  const raise = ramp(frame, 20.0, 20.5);
  const wipe = frame > s(24.9) && frame < s(25.5);
  const tears = ending ? 0 : interpolate(frame, [s(24.9), s(25.5)], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const phone = !ending && frame >= s(20.0);
  return (
    <AbsoluteFill>
      <Hallway />
      <Layer>
        <Suitcase x={820} y={1740} color="#2f8a7a" />
        <Puppet
          who="zeynep"
          x={600}
          y={FEET}
          pose={{
            ...base("zeynep", frame, 40),
            brow: ending ? "raised" : frame > s(25.4) ? "neutral" : "sad",
            smile: ending ? 0.55 : frame > s(25.4) ? 0.1 : -0.3,
            tears,
            phone,
            armR: phone ? [6 + 14 * raise, 6 + 178 * raise] : [6, 6],
            armL: wipe ? [20, 165] : [6, 8],
            look: ending ? 0 : -0.4,
          }}
        />
      </Layer>
    </AbsoluteFill>
  );
};

const STROKE = "-4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000, 0 4px 0 #000, 0 -4px 0 #000, 4px 0 0 #000, -4px 0 0 #000";
const SERIF = "'DejaVu Serif', Georgia, serif";

const Subtitles: React.FC<{ frame: number }> = ({ frame }) => {
  const l = lineAt(frame);
  if (!l) return null;
  const local = frame - s(l.at);
  const pop = interpolate(local, [0, 4], [0.92, 1], { extrapolateRight: "clamp" });
  const phone = l.who === "kemal";
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", top: 1270 }}>
      {l.name && local < 75 && (
        <div style={{ fontFamily: SERIF, fontSize: 40, color: "#ffd98a", textShadow: STROKE, fontWeight: 700, marginBottom: 14 }}>{l.name}</div>
      )}
      <div
        style={{
          fontFamily: SERIF,
          fontSize: 62,
          lineHeight: 1.2,
          fontWeight: 700,
          fontStyle: phone ? "italic" : "normal",
          color: "#ffffff",
          textAlign: "center",
          width: 900,
          textShadow: STROKE,
          transform: `scale(${pop})`,
        }}
      >
        {l.text}
      </div>
    </AbsoluteFill>
  );
};

const SeriesTag: React.FC<{ frame: number }> = ({ frame }) => {
  const o = frame > s(SH.H) ? 0 : 1;
  return (
    <AbsoluteFill style={{ alignItems: "center", top: 120, opacity: o }}>
      <div style={{ fontFamily: SERIF, fontSize: 38, fontWeight: 700, color: "#fff", textShadow: STROKE, letterSpacing: 2 }}>SESSİZ GELİN</div>
      <div style={{ fontFamily: SERIF, fontSize: 32, color: "#ffd98a", textShadow: STROKE, marginTop: 6 }}>Bölüm 1</div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC<{ frame: number }> = ({ frame }) => {
  const a = ramp(frame, 33.3, 33.7);
  const b = ramp(frame, 34.4, 34.8);
  return (
    <AbsoluteFill style={{ alignItems: "center", top: 1230 }}>
      <div style={{ fontFamily: SERIF, fontSize: 92, fontWeight: 700, color: "#fff", textShadow: STROKE, opacity: a, transform: `scale(${0.85 + 0.15 * a})` }}>
        Yeni patron kim?
      </div>
      <div style={{ fontFamily: SERIF, fontSize: 50, fontWeight: 700, color: "#ffd98a", textShadow: STROKE, opacity: b, marginTop: 30 }}>
        Bölüm 2 yarın
      </div>
    </AbsoluteFill>
  );
};

export const Bolum1: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;

  let shot: React.ReactNode;
  if (t < SH.B) {
    const z = interpolate(frame, [0, s(SH.B)], [1.0, 1.12]);
    shot = (
      <Camera zoom={z} fx={540} fy={1000}>
        <SalonScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.C) {
    const z = interpolate(frame, [s(SH.B), s(SH.C)], [2.2, 2.4]);
    shot = (
      <Camera zoom={z} {...face(760)}>
        <SalonScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.D) {
    const z = interpolate(frame, [s(SH.C), s(SH.D)], [2.2, 2.45]);
    shot = (
      <Camera zoom={z} {...face(330)}>
        <SalonScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.E) {
    const toNermin = ramp(frame, 11.8, 12.3);
    const z = 1.0 + 0.45 * toNermin;
    shot = (
      <Camera zoom={z} fx={540 - 120 * toNermin} fy={1000 - 120 * toNermin}>
        <SalonScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.F) {
    const z = interpolate(frame, [s(SH.E), s(SH.F)], [2.3, 2.6]);
    shot = (
      <Camera zoom={z} {...face(640)}>
        <SalonScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.G) {
    const z = interpolate(frame, [s(SH.F), s(SH.G)], [1.05, 2.1], { easing: Easing.inOut(Easing.quad) });
    const f = face(600);
    shot = (
      <Camera zoom={z} fx={interpolate(z, [1.05, 2.1], [540, f.fx])} fy={interpolate(z, [1.05, 2.1], [1000, f.fy])}>
        <HallScene frame={frame} />
      </Camera>
    );
  } else if (t < SH.H) {
    const z = interpolate(frame, [s(SH.G), s(SH.H)], [1.35, 1.6]);
    shot = (
      <Camera zoom={z} fx={550} fy={930}>
        <NerminEmre frame={frame} />
      </Camera>
    );
  } else {
    const z = interpolate(frame, [s(SH.H), s(SH.END)], [2.6, 2.9]);
    shot = (
      <Camera zoom={z} {...face(600)}>
        <HallScene frame={frame} ending />
      </Camera>
    );
  }

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1412" }}>
      {shot}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 220px rgba(0,0,0,0.45)" }} />
      <SeriesTag frame={frame} />
      {t < SH.H ? <Subtitles frame={frame} /> : <EndCard frame={frame} />}

      <Audio src={staticFile("sfx/pad.wav")} volume={0.35} />
      <Sequence from={s(0.15)}>
        <Audio src={staticFile("sfx/hit.wav")} volume={0.5} />
      </Sequence>
      <Sequence from={s(18.7)}>
        <Audio src={staticFile("sfx/ring.wav")} volume={0.45} />
      </Sequence>
      <Sequence from={s(SH.H)}>
        <Audio src={staticFile("sfx/sting.wav")} volume={0.6} />
      </Sequence>
      {LINES.map((l) => (
        <Sequence key={l.id} from={s(l.at)}>
          <Audio src={staticFile(`lines/${l.id}.wav`)} volume={1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
