import React from "react";

// Flat 2D cut-out puppets. Local space: origin at the feet, up is negative y, about 1000 units tall.
const OL = "#3b2a24";
const SW = 3.5;

export type Who = "zeynep" | "nermin" | "emre";

export type Pose = {
  mouth?: number; // 0..1 open
  blink?: number; // 0..1 closed
  brow?: "neutral" | "angry" | "sad" | "raised";
  smile?: number; // -1 frown .. 1 smile
  tears?: number; // 0..1
  armL?: [number, number]; // [shoulder outward deg, elbow inward deg]
  armR?: [number, number];
  phone?: boolean; // phone in right hand
  headTilt?: number;
  look?: number; // -1..1 pupils
  breathe?: number;
};

type Look = {
  skin: string;
  hair: string;
  hairDark: string;
  iris: string;
  lips: string;
  sleeve: string;
};

const LOOKS: Record<Who, Look> = {
  zeynep: { skin: "#f4d2b8", hair: "#5b3a2b", hairDark: "#3f281d", iris: "#6b4a2f", lips: "#c4626a", sleeve: "#e9dfcd" },
  nermin: { skin: "#efc7aa", hair: "#cdb284", hairDark: "#a88f63", iris: "#5c6b74", lips: "#a8343f", sleeve: "#7a2132" },
  emre: { skin: "#e8bf9d", hair: "#2a211d", hairDark: "#17110e", iris: "#4b3424", lips: "#b9786f", sleeve: "#2f4062" },
};

const Arm: React.FC<{ side: 1 | -1; angle: [number, number]; look: Look; phone?: boolean }> = ({ side, angle, look, phone }) => {
  const sx = side * 76;
  const [up, bend] = angle;
  return (
    <g transform={`rotate(${-side * up} ${sx} -790)`}>
      <rect x={sx - 19} y={-800} width={38} height={175} rx={19} fill={look.sleeve} stroke={OL} strokeWidth={SW} />
      <g transform={`rotate(${side * bend} ${sx} -640)`}>
        <rect x={sx - 17} y={-655} width={34} height={175} rx={17} fill={look.sleeve} stroke={OL} strokeWidth={SW} />
        <ellipse cx={sx} cy={-462} rx={19} ry={22} fill={look.skin} stroke={OL} strokeWidth={SW} />
        {phone && <rect x={sx - 14} y={-505} width={28} height={58} rx={6} fill="#1f2328" stroke={OL} strokeWidth={2.5} />}
      </g>
    </g>
  );
};

const Face: React.FC<{ who: Who; look: Look; pose: Pose }> = ({ who, look, pose }) => {
  const blink = pose.blink ?? 0;
  const mouth = pose.mouth ?? 0;
  const smile = pose.smile ?? 0;
  const lookX = (pose.look ?? 0) * 4;
  const brow = pose.brow ?? "neutral";
  const ey = -912;
  const browTilt = brow === "angry" ? 7 : brow === "sad" ? -7 : 0;
  const browLift = brow === "raised" ? -6 : brow === "sad" ? -2 : 0;
  const tears = pose.tears ?? 0;
  const old = who === "nermin";

  const eye = (s: 1 | -1) => {
    const cx = s * 25;
    return (
      <g key={s}>
        <g transform={`translate(${cx} ${ey}) scale(1 ${Math.max(0.08, 1 - blink)}) translate(${-cx} ${-ey})`}>
          <ellipse cx={cx} cy={ey} rx={14} ry={10} fill="#ffffff" stroke={OL} strokeWidth={2.5} />
          <circle cx={cx + lookX} cy={ey + 1} r={7.5} fill={look.iris} />
          <circle cx={cx + lookX} cy={ey + 1} r={3.5} fill="#1c1410" />
          <circle cx={cx + lookX + 2.5} cy={ey - 2} r={1.8} fill="#ffffff" />
        </g>
        <path d={`M ${cx - 15} ${ey - 4} Q ${cx} ${ey - 14} ${cx + 15} ${ey - 4}`} fill="none" stroke={OL} strokeWidth={3} />
        {/* brow: inner end is toward x=0 */}
        <path
          d={`M ${cx + s * 16} ${ey - 24 + browLift - (s > 0 ? 0 : 0)} L ${cx - s * 14} ${ey - 24 + browLift + browTilt}`}
          transform={s < 0 ? undefined : undefined}
          stroke={look.hairDark}
          strokeWidth={5}
          strokeLinecap="round"
        />
        {old && <path d={`M ${cx + s * 17} ${ey + 6} l ${s * 7} 4`} stroke={OL} strokeWidth={1.6} opacity={0.6} />}
      </g>
    );
  };

  const my = -862;
  const mw = who === "emre" ? 16 : 14;
  const curve = smile * 7;
  return (
    <g>
      {eye(-1)}
      {eye(1)}
      <path d={`M -3 -900 Q -7 -884 2 -880`} fill="none" stroke={OL} strokeWidth={2.4} opacity={0.75} />
      {who !== "emre" && <ellipse cx={-38} cy={-878} rx={13} ry={7} fill="#e98d8d" opacity={0.45} />}
      {who !== "emre" && <ellipse cx={38} cy={-878} rx={13} ry={7} fill="#e98d8d" opacity={0.45} />}
      {mouth > 0.08 ? (
        <g>
          <path
            d={`M ${-mw} ${my - curve * 0.4} Q 0 ${my + curve * 0.5 - 2} ${mw} ${my - curve * 0.4} Q 0 ${my + 4 + mouth * 15} ${-mw} ${my - curve * 0.4} Z`}
            fill="#6e2a2a"
            stroke={OL}
            strokeWidth={2.2}
          />
          <path d={`M ${-mw * 0.6} ${my + 1 + mouth * 9} Q 0 ${my - 1 + mouth * 6} ${mw * 0.6} ${my + 1 + mouth * 9}`} fill="#d97a7a" opacity={0.8} />
        </g>
      ) : (
        <path d={`M ${-mw} ${my - curve * 0.4} Q 0 ${my + curve} ${mw} ${my - curve * 0.4}`} fill="none" stroke={who === "nermin" ? look.lips : OL} strokeWidth={who === "nermin" ? 4.5 : 3} strokeLinecap="round" />
      )}
      {tears > 0 &&
        ([-1, 1] as const).map((s) => (
          <path
            key={s}
            d={`M ${s * 22} ${ey + 10} q ${s * 3} ${30 * tears} ${s * 1} ${62 * tears}`}
            stroke="#8fc3e8"
            strokeWidth={6}
            fill="none"
            strokeLinecap="round"
            opacity={0.9}
          />
        ))}
    </g>
  );
};

const Head: React.FC<{ who: Who; look: Look; pose: Pose }> = ({ who, look, pose }) => {
  return (
    <g transform={`rotate(${pose.headTilt ?? 0} 0 -830)`}>
      <rect x={-17} y={-845} width={34} height={60} fill={look.skin} stroke={OL} strokeWidth={SW} />
      {who === "emre" && (
        <>
          <ellipse cx={-62} cy={-905} rx={10} ry={17} fill={look.skin} stroke={OL} strokeWidth={SW} />
          <ellipse cx={62} cy={-905} rx={10} ry={17} fill={look.skin} stroke={OL} strokeWidth={SW} />
        </>
      )}
      <ellipse cx={0} cy={-905} rx={62} ry={78} fill={look.skin} stroke={OL} strokeWidth={SW} />
      <Face who={who} look={look} pose={pose} />
      {who === "zeynep" && (
        <path d="M -66 -915 Q -70 -990 5 -986 Q 70 -986 66 -912 Q 40 -965 -8 -952 Q -30 -948 -48 -925 Q -58 -905 -66 -880 Z" fill={look.hair} stroke={OL} strokeWidth={SW} />
      )}
      {who === "nermin" && (
        <path d="M -68 -900 Q -78 -992 4 -988 Q 78 -990 68 -905 Q 52 -948 14 -950 Q -28 -955 -46 -935 Q -60 -920 -68 -900 Z" fill={look.hair} stroke={OL} strokeWidth={SW} />
      )}
      {who === "nermin" && <path d="M -30 -975 Q 0 -962 34 -970" stroke={look.hairDark} strokeWidth={3} fill="none" />}
      {who === "emre" && (
        <path d="M -64 -915 Q -72 -1000 0 -992 Q 72 -1000 64 -915 Q 58 -950 30 -955 Q 0 -945 -30 -956 Q -56 -948 -64 -915 Z" fill={look.hair} stroke={OL} strokeWidth={SW} />
      )}
    </g>
  );
};

const BackHair: React.FC<{ who: Who; look: Look; pose: Pose }> = ({ who, look, pose }) => (
  <g transform={`rotate(${pose.headTilt ?? 0} 0 -830)`}>
    {who === "zeynep" && (
      <path d="M -78 -930 Q -92 -1010 0 -1000 Q 92 -1010 78 -930 L 92 -660 Q 0 -630 -92 -660 Z" fill={look.hair} stroke={OL} strokeWidth={SW} />
    )}
    {who === "nermin" && <circle cx={0} cy={-1000} r={40} fill={look.hair} stroke={OL} strokeWidth={SW} />}
  </g>
);

const Body: React.FC<{ who: Who; look: Look }> = ({ who, look }) => {
  if (who === "zeynep") {
    return (
      <g>
        <rect x={-42} y={-150} width={30} height={135} fill={look.skin} stroke={OL} strokeWidth={SW} />
        <rect x={12} y={-150} width={30} height={135} fill={look.skin} stroke={OL} strokeWidth={SW} />
        <ellipse cx={-30} cy={-12} rx={26} ry={13} fill="#8a5a44" stroke={OL} strokeWidth={SW} />
        <ellipse cx={30} cy={-12} rx={26} ry={13} fill="#8a5a44" stroke={OL} strokeWidth={SW} />
        <path d="M -70 -795 Q 0 -812 70 -795 L 54 -600 L 118 -130 Q 0 -112 -118 -130 L -54 -600 Z" fill="#f1e9da" stroke={OL} strokeWidth={SW} />
        <path d="M -54 -600 Q 0 -588 54 -600" fill="none" stroke="#cdbfa6" strokeWidth={6} />
        <path d="M -24 -800 Q 0 -770 24 -800" fill="#ffffff" stroke={OL} strokeWidth={2.5} />
      </g>
    );
  }
  if (who === "nermin") {
    return (
      <g>
        <rect x={-40} y={-230} width={30} height={215} fill="#d9b29a" stroke={OL} strokeWidth={SW} />
        <rect x={10} y={-230} width={30} height={215} fill="#d9b29a" stroke={OL} strokeWidth={SW} />
        <ellipse cx={-28} cy={-12} rx={25} ry={12} fill="#1d1b1f" stroke={OL} strokeWidth={SW} />
        <ellipse cx={28} cy={-12} rx={25} ry={12} fill="#1d1b1f" stroke={OL} strokeWidth={SW} />
        <path d="M -66 -600 L 66 -600 L 100 -225 Q 0 -212 -100 -225 Z" fill="#2c2a30" stroke={OL} strokeWidth={SW} />
        <path d="M -78 -796 Q 0 -814 78 -796 L 68 -560 Q 0 -548 -68 -560 Z" fill={look.sleeve} stroke={OL} strokeWidth={SW} />
        <path d="M -22 -798 L 0 -690 L 22 -798" fill="#2c2a30" stroke={OL} strokeWidth={2.5} />
        <path d="M 0 -690 L 0 -560" stroke={OL} strokeWidth={2.5} />
        <circle cx={-10} cy={-650} r={5} fill="#d9c08a" stroke={OL} strokeWidth={1.5} />
        <circle cx={-10} cy={-605} r={5} fill="#d9c08a" stroke={OL} strokeWidth={1.5} />
        {Array.from({ length: 9 }).map((_, i) => {
          const t = i / 8;
          const x = -26 + t * 52;
          const y = -800 + Math.sin(t * Math.PI) * 24;
          return <circle key={i} cx={x} cy={y} r={5} fill="#f8f4ea" stroke={OL} strokeWidth={1.4} />;
        })}
      </g>
    );
  }
  return (
    <g>
      <path d="M -62 -560 L 62 -560 L 56 -20 L 6 -20 L 0 -420 L -6 -20 L -56 -20 Z" fill="#6c6c72" stroke={OL} strokeWidth={SW} />
      <ellipse cx={-32} cy={-14} rx={30} ry={13} fill="#2a2420" stroke={OL} strokeWidth={SW} />
      <ellipse cx={32} cy={-14} rx={30} ry={13} fill="#2a2420" stroke={OL} strokeWidth={SW} />
      <path d="M -82 -800 Q 0 -816 82 -800 L 66 -545 Q 0 -535 -66 -545 Z" fill={look.sleeve} stroke={OL} strokeWidth={SW} />
      <path d="M -22 -804 L 0 -775 L 22 -804" fill="#e8e8ec" stroke={OL} strokeWidth={2.5} />
      <path d="M 0 -775 L 0 -548" stroke={OL} strokeWidth={2} opacity={0.7} />
      <rect x={-64} y={-560} width={128} height={14} fill="#3a2c24" stroke={OL} strokeWidth={2} />
    </g>
  );
};

export const Puppet: React.FC<{ who: Who; x: number; y: number; scale?: number; flip?: boolean; pose?: Pose }> = ({
  who,
  x,
  y,
  scale = 1,
  flip = false,
  pose = {},
}) => {
  const look = LOOKS[who];
  const b = 1 + 0.006 * Math.sin(pose.breathe ?? 0);
  return (
    <g transform={`translate(${x} ${y}) scale(${flip ? -scale : scale} ${scale * b})`}>
      <ellipse cx={0} cy={0} rx={110} ry={16} fill="#000" opacity={0.12} />
      <BackHair who={who} look={look} pose={pose} />
      <Body who={who} look={look} />
      <Arm side={-1} angle={pose.armL ?? [6, 6]} look={look} />
      {!pose.phone && <Arm side={1} angle={pose.armR ?? [6, 6]} look={look} />}
      <Head who={who} look={look} pose={pose} />
      {pose.phone && <Arm side={1} angle={pose.armR ?? [25, 186]} look={look} phone />}
    </g>
  );
};
