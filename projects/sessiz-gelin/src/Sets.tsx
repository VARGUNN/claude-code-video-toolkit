import React from "react";

const OL = "#3b2a24";

const Wallpaper: React.FC<{ id: string; base: string; motif: string; h: number }> = ({ id, base, motif, h }) => (
  <>
    <defs>
      <pattern id={id} width={90} height={110} patternUnits="userSpaceOnUse">
        <rect width={90} height={110} fill={base} />
        <path d="M 45 30 l 7 12 l -7 12 l -7 -12 Z" fill={motif} />
        <path d="M 0 85 l 7 12 l -7 12 l -7 -12 Z M 90 85 l 7 12 l -7 12 l -7 -12 Z" fill={motif} />
      </pattern>
    </defs>
    <rect x={0} y={0} width={1080} height={h} fill={`url(#${id})`} />
  </>
);

const Floor: React.FC<{ y: number }> = ({ y }) => (
  <g>
    <rect x={0} y={y} width={1080} height={1920 - y} fill="#b9895c" />
    {Array.from({ length: 10 }).map((_, i) => (
      <line key={i} x1={0} x2={1080} y1={y + 40 + i * i * 9 + i * 18} y2={y + 40 + i * i * 9 + i * 18} stroke="#9c7149" strokeWidth={3} />
    ))}
    {Array.from({ length: 14 }).map((_, i) => (
      <line key={`v${i}`} x1={i * 90 + (i % 2) * 40} y1={y} x2={(i * 90 + (i % 2) * 40 - 540) * 1.8 + 540} y2={1920} stroke="#a77b50" strokeWidth={2} />
    ))}
    <rect x={0} y={y - 26} width={1080} height={30} fill="#efe6d3" stroke={OL} strokeWidth={3} />
  </g>
);

export const Salon: React.FC = () => (
  <svg width={1080} height={1920} viewBox="0 0 1080 1920">
    <Wallpaper id="wp-salon" base="#efe1c6" motif="#e2cfa9" h={1400} />
    <rect x={0} y={1000} width={1080} height={400} fill="#e7d6b5" />
    <line x1={0} x2={1080} y1={1000} y2={1000} stroke="#d1bb92" strokeWidth={8} />
    {/* window with curtains */}
    <rect x={700} y={330} width={290} height={480} fill="#cfe3ee" stroke={OL} strokeWidth={5} />
    <line x1={845} x2={845} y1={330} y2={810} stroke={OL} strokeWidth={5} />
    <line x1={700} x2={990} y1={560} y2={560} stroke={OL} strokeWidth={5} />
    <path d="M 670 300 L 760 300 Q 735 560 770 860 L 670 860 Z" fill="#8c2f3c" stroke={OL} strokeWidth={4} />
    <path d="M 1020 300 L 930 300 Q 955 560 920 860 L 1020 860 Z" fill="#8c2f3c" stroke={OL} strokeWidth={4} />
    <rect x={655} y={285} width={380} height={22} rx={10} fill="#5b3b28" stroke={OL} strokeWidth={4} />
    {/* framed painting */}
    <rect x={120} y={360} width={300} height={220} fill="#7d6a4a" stroke={OL} strokeWidth={6} />
    <rect x={140} y={380} width={260} height={180} fill="#9fb59a" />
    <path d="M 140 520 Q 220 450 290 500 Q 340 470 400 510 L 400 560 L 140 560 Z" fill="#6f8f6a" />
    <circle cx={330} cy={430} r={22} fill="#f2e2a6" />
    {/* lamp */}
    <path d="M 70 1050 L 150 1050 L 128 960 L 92 960 Z" fill="#f3e2b8" stroke={OL} strokeWidth={4} />
    <rect x={105} y={1050} width={10} height={290} fill="#5b3b28" />
    <ellipse cx={110} cy={1345} rx={48} ry={10} fill="#5b3b28" />
    <Floor y={1400} />
    {/* rug */}
    <ellipse cx={540} cy={1700} rx={470} ry={120} fill="#9a3a3f" opacity={0.85} />
    <ellipse cx={540} cy={1700} rx={410} ry={95} fill="none" stroke="#d8b46a" strokeWidth={6} />
  </svg>
);

export const Hallway: React.FC<{ doorOpen?: number }> = () => (
  <svg width={1080} height={1920} viewBox="0 0 1080 1920">
    <Wallpaper id="wp-hall" base="#ece3cf" motif="#ddd0b3" h={1400} />
    {/* door */}
    <rect x={150} y={520} width={360} height={880} fill="#f7f1e2" stroke={OL} strokeWidth={6} />
    <rect x={150} y={520} width={60} height={880} fill="#6d4a33" stroke={OL} strokeWidth={5} />
    <rect x={130} y={500} width={400} height={28} fill="#5b3b28" stroke={OL} strokeWidth={5} />
    <circle cx={198} cy={980} r={9} fill="#d9b85c" stroke={OL} strokeWidth={2} />
    {/* coat rack */}
    <rect x={720} y={520} width={260} height={18} rx={8} fill="#5b3b28" stroke={OL} strokeWidth={4} />
    <path d="M 760 538 L 740 860 L 800 860 L 790 538 Z" fill="#4b5563" stroke={OL} strokeWidth={4} />
    <path d="M 880 538 L 860 800 L 925 800 L 910 538 Z" fill="#a0603a" stroke={OL} strokeWidth={4} />
    {/* mirror */}
    <ellipse cx={850} cy={1050} rx={90} ry={130} fill="#d8e6ea" stroke="#8a6a3a" strokeWidth={14} />
    <Floor y={1400} />
    <rect x={160} y={1385} width={340} height={40} fill="#7a5a44" opacity={0.6} />
  </svg>
);

export const Suitcase: React.FC<{ x: number; y: number; color?: string; s?: number }> = ({ x, y, color = "#2f8a7a", s = 1 }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-10} y={-230} width={20} height={70} fill="none" stroke={OL} strokeWidth={6} />
    <rect x={-70} y={-165} width={140} height={160} rx={16} fill={color} stroke={OL} strokeWidth={4} />
    <line x1={-25} x2={-25} y1={-160} y2={-10} stroke={OL} strokeWidth={3} opacity={0.5} />
    <line x1={25} x2={25} y1={-160} y2={-10} stroke={OL} strokeWidth={3} opacity={0.5} />
    <circle cx={-50} cy={0} r={8} fill="#222" />
    <circle cx={50} cy={0} r={8} fill="#222" />
  </g>
);
