"""1. bölümün motorundan 2. bölümün src.html'ini üretir.

Spiker (SPIKER nesnesi), stüdyo, logo, alt bant, altyazı ve ses motoru 1. bölümden birebir gelir.
Bu betik yalnızca bölüme özgü kısımları değiştirir. Çalıştır: python3 make_ep2.py && python3 build.py
"""
import pathlib, re

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "koca-kafalar-aslan" / "src.html").read_text(encoding="utf-8")


def cut(s, start, end, new):
    a = s.index(start)
    b = s.index(end, a)
    return s[:a] + new + s[b:]


def swap(s, old, new):
    assert s.count(old) == 1, (old[:80], s.count(old))
    return s.replace(old, new)


s = SRC

# ---------- başlık ----------
s = swap(s, "<title>Dandik Haber</title>", "<title>Dandik Haber 2</title>")
s = swap(s, "<h1>DANDİK <b>HABER</b></h1>", "<h1>DANDİK <b>HABER</b> · 2</h1>")
s = swap(s, "a.download = `dandik-haber-aslan-bolumu.${ext}`", "a.download = `dandik-haber-bolum-2.${ext}`")

# ---------- senaryo, zaman çizelgesi, metinler ----------
s = cut(s, "const LINES = [", "/* kelime zamanlaması", r'''const LINES = [
  { id: 'L1', who: 'spiker', at: 0.25,
    text: "Son dakika! Aslanımız Kadıköy vapurunda martılarla simit kavgasına tutuştu!",
    seg: [[0.05, 4.67]] },
  { id: 'L2', who: 'spiker', at: 5.35,
    text: "Gelelim diğer haberimize! Bursa'da bir usta, giden kamyonetin motoruna yatıp arıza tespiti yaptı! Muhabirimiz Berk aracın peşinde!",
    seg: [[0.05, 1.40, 3], [1.66, 5.68, 10], [6.00, 7.64, 4]] },
  { id: 'L3', who: 'muhabir', at: 14.20,
    text: "Sayın seyirciler, kamyonet gidiyor, usta motorun üstünde! Usta, ne yapıyorsun?!",
    seg: [[0.05, 3.49, 7], [3.65, 5.30, 3]] },
  { id: 'L4', who: 'usta', at: 19.85,
    text: "Evladım, duran araba arıza vermez! Gidecek ki konuşacak, ben de dinleyeceğim!",
    seg: [[0.05, 2.43, 5], [2.62, 5.05, 6]] },
  { id: 'L5', who: 'esnaf', at: 25.25,
    text: "Sağ olsun ustam, servis kırk bin lira istiyordu!",
    seg: [[0.05, 2.97]] },
  { id: 'L6', who: 'usta', at: 28.85,
    text: "Buldum arızayı!",
    seg: [[0.05, 1.21]] },
  { id: 'L7', who: 'muhabir', at: 30.20,
    text: "Neymiş?",
    seg: [[0.85, 1.52]] },
  { id: 'L8', who: 'usta', at: 31.95,
    text: "Fren tutmuyor! Aaaaa!",
    seg: [[0.05, 1.08, 2], [1.27, 2.30, 1]] },
  { id: 'L9', who: 'spiker', at: 37.45,
    text: "Evet sayın seyirciler, uzmanlar bu yöntemi kesinlikle önermiyor. Bizi takip etmeyi unutmayın!",
    seg: [[0.05, 3.98, 8], [4.25, 5.58, 4]] },
  { id: 'L10', who: 'spiker', at: 44.10,
    text: "Bir dakika... Bu korna... bizim kapının önünden mi geliyor?!",
    seg: [[0.05, 1.11, 2], [1.30, 1.99, 2], [2.36, 4.00, 5]] },
];
const T = {
  glitch1: 13.25, s2: 13.75, fail: 33.10, glitch2: 36.60, s5: 37.10,
  follow: 41.70, empty: 43.40, crash: 48.45, black: 48.95, DUR: 49.6
};
const DUR = T.DUR;
const NAMES = {
  spiker: ['BERKCAN DANDİKOĞLU', 'Ana Haber Spikeri'],
  muhabir: ['BERK', 'Olay Yeri Muhabiri · Bursa'],
  usta: ['RECEP USTA', 'Oto tamirci · Kaput üstü arıza uzmanı'],
  esnaf: ['CEMAL ABİ', 'Kamyonet sahibi · Servise gitmedi'],
};
const NAME_SHOW = [['L1', 'spiker'], ['L3', 'muhabir'], ['L4', 'usta'], ['L5', 'esnaf']];
const HEADLINES = [
  [0, "ASLAN VAPURDA MARTILARLA SİMİT KAVGASINDA"],
  [5.35, "BURSA'DA KAPUT ÜSTÜNDE ARIZA TESPİTİ"],
  [13.75, "CANLI BAĞLANTI · BURSA ÇEVRE YOLU"],
  [19.85, "USTA: 'DURAN ARABA ARIZA VERMEZ'"],
  [25.25, "MÜŞTERİ: 'SERVİS 40 BİN İSTEDİ'"],
  [32.2, "SON DAKİKA: FREN TUTMUYOR!"],
  [34.2, "LÜTFEN EVDE DENEMEYİN"],
  [37.1, "UZMANLAR: 'BU YÖNTEMİ DENEMEYİN'"],
  [43.4, "SON DAKİKA: FRENSİZ KAMYONET STÜDYOYA YAKLAŞIYOR"],
];
const TICKER = "Martılar simit fiyatlarını protesto etti  •  Aslan vapurda 'iskeleye kadar bırak' dedi  •  Bursa'da kaputta yolcu taşıyan araçlar sağ şeritten gitsin  •  Usta: 'Arıza dinlenerek bulunur'  •  Uludağ: 'Bizim yokuştan frensiz inmeyin'  •  ";
const CAP_COL = { spiker: '#ffd400', muhabir: '#5ef2ff', esnaf: '#ffa53a', usta: '#8dff5a', aslan: '#ffd400' };

''')

# ---------- yeni efektler ----------
s = swap(s, "  outro(w) {", r'''  engine(w, d, off) {
    const o = AC.createOscillator(); o.type = 'sawtooth'; o.frequency.value = 52;
    const o2 = AC.createOscillator(); o2.type = 'square'; o2.frequency.value = 104;
    const fl = AC.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = 320;
    const g = AC.createGain();
    const tf = w + (T.fail - T.s2 - (off || 0));
    g.gain.setValueAtTime(0.0001, w); g.gain.linearRampToValueAtTime(0.16, w + 0.4);
    if (tf > w + 0.4) {
      [o.frequency, o2.frequency].forEach((p, i) => { p.setValueAtTime(i ? 104 : 52, tf); p.exponentialRampToValueAtTime(i ? 250 : 125, tf + 1.2); });
      fl.frequency.setValueAtTime(320, tf); fl.frequency.exponentialRampToValueAtTime(1100, tf + 1.2);
      g.gain.setValueAtTime(0.16, tf + 0.9); g.gain.linearRampToValueAtTime(0.0001, Math.min(w + d, tf + 2.6));
    } else { g.gain.setValueAtTime(0.16, w + Math.max(0.5, d - 0.4)); g.gain.linearRampToValueAtTime(0.0001, w + d); }
    const lfo = AC.createOscillator(); lfo.frequency.value = 17; const lg = AC.createGain(); lg.gain.value = 0.05; lfo.connect(lg); lg.connect(g.gain);
    o.connect(fl); o2.connect(fl); fl.connect(g); g.connect(S.s);
    [o, o2, lfo].forEach(n => { n.start(w); n.stop(w + d + 0.05); });
  },
  wind(w, d) { noiseHit(w, d, 0.06, S.s, 'bandpass', 900, { q: 0.4, a: 0.4, r: 0.4 }); },
  clack(w) { noiseHit(w, 0.05, 0.5, S.s, 'lowpass', 1400, { r: 0.04 }); tone('square', 160, w, 0.04, 0.15, S.s, { lp: 800 }); },
  slideDown(w) { tone('sine', 1700, w, 0.7, 0.28, S.s, { f1: 220, ft: 0.65 }); },
  rev(w) { tone('sawtooth', 90, w, 1.6, 0.18, S.s, { f1: 260, ft: 1.2, lp: 900, r: 0.5 }); },
  hornApproach(w, d) { for (let k = 0; k < d - 0.2; k += 0.62) { const v = 0.03 + 0.3 * Math.pow(k / d, 2); tone('square', 392, w + k, 0.34, v, S.s, { lp: 2200 }); tone('square', 494, w + k, 0.34, v * 0.8, S.s, { lp: 2200 }); } },
  rattle(w, d) { for (let k = 0; k < d; k += 0.045) noiseHit(w + k + Math.random() * 0.01, 0.012, 0.05 + 0.3 * (k / d), S.s, 'highpass', 4500, { r: 0.01 }); },
  crash(w) {
    noiseHit(w, 0.9, 0.9, S.s, 'lowpass', 2500, { f1: 200, ft: 0.9, r: 0.7 });
    tone('sine', 90, w, 0.9, 0.9, S.s, { f1: 28, ft: 0.6, r: 0.5 });
    for (let i = 0; i < 14; i++) noiseHit(w + 0.05 + Math.random() * 0.6, 0.03, 0.4, S.s, 'highpass', 5000 + Math.random() * 4000, { r: 0.02 });
    tone('triangle', 310, w, 0.8, 0.25, S.s, { r: 0.7 }); tone('triangle', 473, w + 0.02, 0.8, 0.2, S.s, { r: 0.7 });
  },
  outro(w) {''')

# ---------- olay listesi ----------
s = cut(s, "function buildEvents() {", "let EVENTS = buildEvents();", r'''function buildEvents() {
  const E = []; const add = (t, f, dur = 0) => E.push({ t, f, dur });
  add(0.0, w => SFX.stinger(w));
  bed(E, 1.3, T.glitch1, 'news');
  add(1.2, w => SFX.gull(w)); add(2.9, w => SFX.gull(w)); add(3.7, w => SFX.crunch(w));
  add(T.glitch1, w => SFX.glitch(w, 0.5)); add(T.s2 - 0.2, w => SFX.whoosh(w, 0.45));
  add(T.s2, (w, off) => SFX.engine(w, T.glitch2 - T.s2 - off, off), T.glitch2 - T.s2);
  add(T.s2, (w, off) => SFX.wind(w, T.fail + 0.8 - T.s2 - off), T.fail + 0.8 - T.s2);
  bed(E, T.s2, T.fail, 'street');
  add(T.s2 + 0.5, w => SFX.horn(w, 0.15));
  add(LINES[5].at + 0.1, w => SFX.ding(w));
  for (let k = 0; k < 3; k++) add(T.fail - 0.5 + k * 0.15, w => SFX.clack(w));
  add(T.fail, w => SFX.slideDown(w)); add(T.fail + 0.05, w => SFX.rev(w)); add(T.fail + 0.3, w => SFX.hit(w));
  add(T.fail + 1.6, w => SFX.gulp(w));
  add(T.glitch2, w => SFX.glitch(w, 0.45));
  bed(E, T.s5 + 0.3, T.empty, 'news');
  add(T.follow, w => SFX.pop(w)); add(T.follow + 0.25, w => SFX.ding(w));
  add(T.empty, w => SFX.glitch(w, 0.25));
  add(T.empty + 0.2, w => SFX.drone(w, T.crash - T.empty - 0.2));
  add(T.empty + 0.4, w => SFX.hornApproach(w, T.crash - T.empty - 0.4));
  add(T.empty + 1.2, w => SFX.rattle(w, T.crash - T.empty - 1.2));
  for (let k = T.empty + 0.8; k < T.crash - 0.2; k += 0.6) add(k, w => SFX.heart(w));
  add(T.crash, w => SFX.crash(w));
  for (const L of LINES) add(L.at, (w, off) => playVoice(L, w, off), L.dur);
  return E.sort((a, b) => a.t - b.t);
}
''')

s = swap(s, "esnaf: { pitch: 0.75 }, aslan: { pitch: 0.2 } };", "esnaf: { pitch: 0.75 }, usta: { pitch: 0.6 }, aslan: { pitch: 0.2 } };")

# ---------- Cemal direksiyonda (file yok), aslanın elinde simit ----------
s = swap(s, "    const h = st.netHand || [84, -6];",
         "    if (st.noNet) { armTo(1, 76, 20 + Math.sin((st.time || 0) * 3) * 4, '#f4f1ea', this.F.skin); return; }\n    const h = st.netHand || [84, -6];")
s = swap(s, "    else tesbih(rh[0], rh[1] + 6, st.time || 0, st.tesbihSw ?? 1);",
         "    else if (st.simit) simit(rh[0] + 4, rh[1] - 20, 24);\n    else tesbih(rh[0], rh[1] + 6, st.time || 0, st.tesbihSw ?? 1);")

# ---------- yeni karakter: Recep Usta + yardımcı çizimler ----------
s = swap(s, "function drawCat(x, y, sc, t, mode) {", r'''const USTA = {
  F: { w: 98, top: -120, chin: 118, cw: 50, chinR: 14, skin: '#d9a07a', my: 62, mw: 44, jw: 58, jawMax: 42 },
  ears() { for (const s of [-1, 1]) { C.beginPath(); ell(s * 98, 4, 18, 27); fs(this.F.skin); C.beginPath(); ell(s * 99, 6, 7, 13); C.strokeStyle = 'rgba(130,60,40,.5)'; C.lineWidth = 4; C.stroke(); } },
  upper(st) {
    C.beginPath(); C.moveTo(-106, -34); C.bezierCurveTo(-112, -120, -50, -152, 8, -148); C.bezierCurveTo(72, -144, 114, -110, 106, -34); C.quadraticCurveTo(0, -64, -106, -34); C.closePath(); fs('#c8102e');
    C.fillStyle = '#fff'; for (let i = 0; i < 12; i++) { C.beginPath(); ell(-80 + (i % 6) * 32 + (i > 5 ? 16 : 0), -110 + (i > 5 ? 34 : 0), 5, 5); C.fill(); }
    C.beginPath(); C.moveTo(-104, -44); C.lineTo(-138, -64); C.lineTo(-130, -30); C.closePath(); fs('#c8102e', 4);
    C.beginPath(); C.moveTo(-104, -40); C.lineTo(-140, -22); C.lineTo(-112, -14); C.closePath(); fs('#c8102e', 4);
    C.fillStyle = 'rgba(40,30,25,.35)'; C.beginPath(); ell(56, 34, 16, 9, 0.4); ell(-34, -42, 12, 6, -0.3); C.fill();
    C.fillStyle = 'rgba(240,110,100,.25)'; C.beginPath(); ell(-62, 30, 17, 10); C.fill();
    eye(-36, -8, 21, 24, st, this.F.skin, 0.1); eye(36, -8, 21, 24, st, this.F.skin, 0.1);
    brows(st, 36, -44, 38, 11, '#2a1a10');
    C.beginPath(); C.moveTo(-6, -22); C.quadraticCurveTo(30, 10, 24, 34); C.quadraticCurveTo(4, 46, -14, 34); C.quadraticCurveTo(-4, 10, -6, -22); fs('#c98a62');
    C.fillStyle = 'rgba(40,30,25,.4)'; C.beginPath(); ell(8, 36, 9, 5); C.fill();
  },
  jaw() { C.fillStyle = 'rgba(40,25,20,.45)'; for (let i = 0; i < 55; i++) { C.beginPath(); ell((hash(i + 31) * 2 - 1) * 52, 74 + hash(i + 97) * 44, 1.9, 1.9); C.fill(); } },
  front() {
    C.beginPath(); C.moveTo(-60, 54); C.quadraticCurveTo(-30, 32, 0, 42); C.quadraticCurveTo(30, 32, 60, 54); C.quadraticCurveTo(30, 68, 0, 60); C.quadraticCurveTo(-30, 68, -60, 54); C.closePath(); fs('#1b120c');
  },
  body(st, ph) {
    const col = '#2f5d8c', skin = this.F.skin;
    if (ph === 'back') {
      legs(st, col, '#1a1a1a');
      torso(col, 54, 50);
      C.fillStyle = 'rgba(20,20,20,.35)'; C.beginPath(); ell(-20, 60, 16, 10); ell(26, 30, 10, 7); ell(10, 80, 12, 6); C.fill();
      C.beginPath(); rrect(-42, 12, 46, 24, 10); fs('#fff', 3); txt('RECEP', -19, 25, `900 12px ${FONT_UI}`, '#c8102e');
      C.beginPath(); C.moveTo(-20, -3); C.lineTo(0, 22); C.lineTo(20, -3); C.lineWidth = 4; C.strokeStyle = OUT; C.stroke();
      arm(-1, st.armL ?? 0.35, 0.5, col, skin);
      return;
    }
    const h = st.wrenchHand || [62, 40];
    armTo(1, h[0], h[1], col, skin, 84);
    wrench(h[0], h[1], st.wrenchAng ?? 0.4);
    C.beginPath(); ell(h[0], h[1], 15, 15); fs(skin);
  }
};
function wrench(x, y, ang) { C.save(); C.translate(x, y); C.rotate(ang); C.beginPath(); rrect(-7, -78, 14, 92, 5); fs('#a8b0ba', 4); C.beginPath(); ell(0, -86, 18, 16); fs('#a8b0ba', 4); C.fillStyle = '#3a3d44'; C.fillRect(-6, -104, 12, 18); C.restore(); }
function simit(x, y, r) {
  C.beginPath(); C.arc(x, y, r, 0, Math.PI * 2); C.moveTo(x + r * 0.45, y); C.arc(x, y, r * 0.45, 0, Math.PI * 2, true);
  C.fillStyle = '#b5651d'; C.fill('evenodd'); C.lineWidth = 3; C.strokeStyle = OUT; C.stroke();
  C.fillStyle = '#f6e7b8'; for (let i = 0; i < 10; i++) { const a = i / 10 * Math.PI * 2; C.beginPath(); ell(x + Math.cos(a) * r * 0.72, y + Math.sin(a) * r * 0.72, 1.8, 1.1, a); C.fill(); }
}
function gull(x, y, t, sc = 1, flip = 1, beakSimit = false) {
  C.save(); C.translate(x, y); C.scale(sc * flip, sc);
  const f = Math.sin(t * 10) * 18;
  C.beginPath(); C.moveTo(-6, 0); C.quadraticCurveTo(-26, -14 - f, -52, -6 - f * 1.4); C.moveTo(6, 0); C.quadraticCurveTo(26, -14 - f, 52, -6 - f * 1.4);
  C.lineCap = 'round'; C.lineWidth = 10; C.strokeStyle = OUT; C.stroke(); C.lineWidth = 6; C.strokeStyle = '#e9edf2'; C.stroke();
  C.beginPath(); ell(0, 2, 17, 10); fs('#fff', 3);
  C.beginPath(); ell(15, -4, 9, 8); fs('#fff', 3);
  C.beginPath(); C.moveTo(22, -4); C.lineTo(34, -1); C.lineTo(22, 1); C.closePath(); fs('#f2a71b', 2);
  C.fillStyle = OUT; C.beginPath(); ell(17, -6, 1.8, 1.8); C.fill();
  if (beakSimit) simit(40, 2, 12);
  C.restore();
}
function drawKamyonet(ox, oy, sc, t, o = {}) {
  C.save(); C.translate(ox, oy); C.scale(sc, sc); C.translate(0, -(o.bounce || 0));
  C.beginPath(); ell(0, 6, 470, 22); C.fillStyle = 'rgba(0,0,0,.25)'; C.fill();
  const blue = '#3d7cc9';
  C.beginPath(); rrect(-430, -250, 420, 150, 10); fs(blue);
  C.beginPath(); rrect(-410, -340, 130, 92, 4); fs('#c8955a'); txt('BAKKAL', -345, -306, `900 22px ${FONT_UI}`, '#7a3b12'); txt('CEMAL', -345, -279, `900 22px ${FONT_UI}`, '#7a3b12');
  C.beginPath(); rrect(-268, -318, 110, 70, 4); fs('#d9a86a'); txt('KIRILIR', -213, -283, `900 18px ${FONT_UI}`, '#c8102e');
  C.fillStyle = 'rgba(0,0,0,.15)'; C.fillRect(-430, -170, 420, 8);
  C.beginPath(); C.moveTo(-20, -100); C.lineTo(-20, -420); C.quadraticCurveTo(-20, -444, 4, -444); C.lineTo(150, -444); C.quadraticCurveTo(196, -444, 236, -262); C.lineTo(252, -252); C.lineTo(252, -100); C.closePath(); fs(blue);
  C.beginPath(); C.moveTo(8, -272); C.lineTo(8, -414); C.lineTo(144, -414); C.quadraticCurveTo(176, -414, 210, -276); C.closePath(); fs('#a9d6f2', 4);
  if (o.cemal) { C.save(); C.beginPath(); C.rect(-80, -1000, 420, 728); C.clip(); drawChar(ESNAF, 96, -150, 0.95, { ...o.cemal, noShadow: true }); C.restore(); }
  C.beginPath(); C.moveTo(-6, -268); C.lineTo(-6, -112); C.lineTo(236, -112); C.lineTo(236, -268); C.strokeStyle = 'rgba(0,0,0,.35)'; C.lineWidth = 4; C.stroke();
  C.beginPath(); rrect(150, -240, 40, 12, 5); fs('#d0d5dd', 3);
  C.beginPath(); rrect(252, -252, 180, 152, 10); fs(blue);
  C.beginPath(); rrect(262, -290, 150, 46, 8); fs('#4a4d55');
  C.strokeStyle = '#c0c4cc'; C.lineWidth = 6; C.beginPath(); C.moveTo(280, -290); C.quadraticCurveTo(300, -320, 330, -292); C.moveTo(350, -290); C.quadraticCurveTo(372, -316, 394, -290); C.stroke();
  C.save(); C.translate(252, -258); C.rotate(-(o.hoodA ?? 1.1)); C.beginPath(); rrect(0, -12, 182, 18, 6); fs(blue); C.restore();
  if (o.usta) { C.save(); C.translate(236, -286); C.rotate(1.4); drawChar(USTA, 0, 0, 1.05, { ...o.usta, tilt: -1.4 + (o.usta.tilt || 0), noShadow: true }); C.restore(); }
  C.beginPath(); rrect(240, -116, 220, 26, 10); fs('#b9bec7');
  C.beginPath(); rrect(410, -200, 34, 40, 8); fs(o.lights ? '#fffbd0' : '#ffe9a0', 4);
  if (o.lights) { C.fillStyle = 'rgba(255,245,180,.35)'; C.beginPath(); C.moveTo(444, -190); C.lineTo(1300, -480); C.lineTo(1300, 80); C.closePath(); C.fill(); }
  C.beginPath(); rrect(300, -112, 104, 24, 3); fs('#fff', 3); C.fillStyle = '#1f4fa8'; C.fillRect(300, -112, 12, 24); txt('16 RC 1616', 358, -99, `900 15px ${FONT_UI}`, '#111');
  for (const wx of [-290, 300]) {
    C.save(); C.translate(wx, -62); C.beginPath(); ell(0, 0, 64, 64); fs('#1b1b1f'); C.beginPath(); ell(0, 0, 28, 28); fs('#a9aeb6', 4);
    C.rotate(o.spin || 0); C.strokeStyle = '#555'; C.lineWidth = 6; for (let k = 0; k < 3; k++) { C.rotate(Math.PI * 2 / 3); C.beginPath(); C.moveTo(0, 0); C.lineTo(0, 26); C.stroke(); }
    C.restore();
  }
  C.restore();
}
function drawCat(x, y, sc, t, mode) {''')

# ---------- stüdyo ekranı, spiker durumu, stüdyo kamerası ----------
s = cut(s, "function drawStudioScreen(t, late) {", "/* ============================================================\n   SAHNE: SOKAK", r'''function drawStudioScreen(t) {
  const x = 140, y = 232, w = 800, h = 250;
  C.save();
  C.beginPath(); rrect(x - 10, y - 10, w + 20, h + 20, 14); fs('#9fb6d9', 6);
  C.beginPath(); C.rect(x, y, w, h); C.clip();
  if (t < LINES[1].at) { // 1. bölümün devamı: aslan vapurda martılarla
    C.fillStyle = '#8fd0f5'; C.fillRect(x, y, w, h); C.fillStyle = '#2f7fb5'; C.fillRect(x, y + 120, w, 130);
    C.fillStyle = '#7d93ad'; C.fillRect(x, y + 104, w, 18);
    C.fillStyle = '#efe7d6'; C.fillRect(x, y + 205, w, 45);
    C.strokeStyle = '#fff'; C.lineWidth = 6; C.beginPath(); C.moveTo(x, y + 168); C.lineTo(x + w, y + 168); C.stroke();
    for (let k = 0; k < 12; k++) { C.beginPath(); C.moveTo(x + k * 70, y + 168); C.lineTo(x + k * 70, y + 210); C.stroke(); }
    const tug = Math.sin(t * 14) * 6;
    drawChar(ASLAN, x + 300, y + 246, 0.42, { time: t, simit: true, rHand: [86 + tug, -40], blink: blinkAt(t, 3), noShadow: true, browR: 12, jaw: Math.floor(t * 8) % 2 ? 0.3 : 0 });
    gull(x + 384 + tug * 0.4, y + 148, t, 0.8, -1);
    gull(x + 470 + Math.sin(t * 2) * 40, y + 60 + Math.cos(t * 3) * 14, t + 1, 0.7, -1, true);
    gull(x + 140 + Math.sin(t * 2.4) * 30, y + 70, t + 2, 0.7, 1);
    gull(x + 610 + Math.cos(t * 1.7) * 30, y + 110, t + 3, 0.6, -1);
    txt('KADIKÖY VAPURU · ÖZEL GÖRÜNTÜ', x + w / 2, y + 26, `900 22px ${FONT_UI}`, '#fff', 'center', '#000', 6);
  } else if (t < T.empty) { // Bursa: kaputta usta
    C.fillStyle = '#8fd0f5'; C.fillRect(x, y, w, h);
    C.fillStyle = '#7d8fa8'; C.beginPath(); C.moveTo(x, y + 170); C.lineTo(x + 260, y + 50); C.lineTo(x + 420, y + 120); C.lineTo(x + 560, y + 70); C.lineTo(x + w, y + 170); C.closePath(); C.fill();
    C.fillStyle = '#fff'; C.beginPath(); C.moveTo(x + 220, y + 70); C.lineTo(x + 260, y + 50); C.lineTo(x + 300, y + 70); C.closePath(); C.fill();
    C.fillStyle = '#50535b'; C.fillRect(x, y + 200, w, 50);
    drawKamyonet(x + 420 + Math.sin(t * 2) * 10, y + 238, 0.29, t, { spin: t * 12, hoodA: 1.15, bounce: Math.abs(Math.sin(t * 17)) * 5, usta: ustaState(20.5), cemal: cemalState(18) });
    if (t >= T.s5) { C.fillStyle = '#e30613'; C.fillRect(x, y, w, 44); txt('LÜTFEN EVDE DENEMEYİN', x + w / 2, y + 23, `32px ${FONT_BIG}`, '#fff'); }
    else txt('BURSA · ÖZEL GÖRÜNTÜ', x + w / 2, y + 26, `900 22px ${FONT_UI}`, '#fff', 'center', '#000', 6);
  } else { // cliffhanger: trafik kamerası, frensiz kamyonet stüdyoya iniyor
    if (t < T.empty + 0.2) { C.fillStyle = Math.floor(t * 40) % 2 ? '#fff' : '#111'; C.fillRect(x, y, w, h); C.restore(); return; }
    C.fillStyle = '#6d8296'; C.fillRect(x, y, w, h);
    C.fillStyle = '#50535b'; C.beginPath(); C.moveTo(x, y + 40); C.lineTo(x + w, y + 170); C.lineTo(x + w, y + 236); C.lineTo(x, y + 106); C.closePath(); C.fill();
    C.strokeStyle = '#f2f2f2'; C.lineWidth = 4; C.setLineDash([24, 18]); C.beginPath(); C.moveTo(x, y + 73); C.lineTo(x + w, y + 203); C.stroke(); C.setLineDash([]);
    C.beginPath(); rrect(x + 600, y + 120, 190, 130, 6); fs('#0b2a66', 4);
    C.fillStyle = '#e30613'; C.fillRect(x + 610, y + 130, 170, 34); txt('DANDİK HABER', x + 695, y + 148, `22px ${FONT_BIG}`, '#fff'); txt('STÜDYO', x + 695, y + 196, `26px ${FONT_BIG}`, '#ffd400');
    const p = clamp(inv(T.empty + 0.2, T.crash, t));
    C.save(); C.translate(x + 40 + p * 560, y + 96 + p * 92); C.rotate(0.16);
    drawKamyonet(0, 0, 0.13, t, { spin: t * 40, hoodA: 1.1, lights: true, usta: ustaState(T.crash), cemal: cemalState(T.crash) }); C.restore();
    if ((t % 1) < 0.6) { C.beginPath(); ell(x + 24, y + 24, 8, 8); C.fillStyle = '#ff2a2a'; C.fill(); }
    txt('CANLI · TRAFİK KAMERASI', x + 40, y + 25, `900 20px ${FONT_UI}`, '#fff', 'left', '#000', 6);
  }
  C.restore();
}
function spikerState(t) {
  const late = t >= T.s5;
  const st = { time: t, blink: blinkAt(t, 1), jaw: jawOf('spiker', t) };
  const tk = talking('spiker', t);
  st.tilt = Math.sin(t * 6.3) * 0.05 * tk + vnoise(t * 0.7) * 0.02;
  st.hy = -Math.abs(Math.sin(t * 6.3)) * 4 * tk;
  if (!late) {
    st.eyeS = 1.1; st.brow = 0.6; st.browAng = 0.25; st.look = [vnoise(t * 0.9) * 0.3, 0];
    if (t < LINES[1].at) { st.eyeS = 1.15; st.brow = 0.9; st.panic = 1; st.tilt += Math.sin(t * 13) * 0.02; }
  } else {
    st.eyeS = 1.05; st.brow = 0.3; st.look = [0, 0];
    if (t > T.follow) { st.smile = 1; st.brow = 0.4; }
    if (t > T.empty) {
      const hear = eio(inv(T.empty + 0.3, T.empty + 0.8, t));
      st.smile = 1 - hear; st.look = [0.9 * hear, -0.1 * hear]; st.eyeS = lerp(1.05, 1.25, hear); st.brow = lerp(0.4, 0.9, hear);
      const b = wordStart('L10', 'Bu'), turn = eio(inv(b, b + 0.6, t));
      if (turn > 0) { st.look = [0.9 * (1 - turn), -0.1]; st.eyeS = lerp(1.25, 1.55, turn); st.pupil = lerp(1, 0.5, turn); }
      const bz = wordStart('L10', 'bizim'), alarm = inv(bz - 0.1, bz + 0.3, t);
      if (alarm > 0) { st.eyeS = lerp(1.55, 1.8, alarm); st.brow = 1.4; st.browAng = 0.45; st.sweat = true; st.pupil = 0.4; }
      st.tilt += Math.sin(t * 50) * 0.015 * inv(T.empty, T.crash, t);
    }
    if (t > T.crash) { st.eyeS = 1.9; st.jaw = 1; st.tilt = Math.sin(t * 40) * 0.15; }
  }
  return st;
}
function drawStudioFixed(t) {
  const late = t >= T.s5;
  const keys = late ? [[T.s5, 540, 820, 1.35], [T.s5 + 1.2, 540, 860, 1.1], [T.empty, 540, 860, 1.13], [T.crash, 540, 830, 1.32]] : [[0, 540, 900, 1.0], [T.glitch1, 540, 840, 1.13]];
  const k = keyed(keys, t);
  let z = k[3];
  if (!late && t < 0.6) z += (1 - eout(t / 0.6)) * 0.35;
  let sh = late && t < T.s5 + 0.4 ? 12 : 3;
  if (t > T.empty) sh = lerp(3, 16, inv(T.empty, T.crash, t));
  if (t > T.crash) sh = 50 * (1 - inv(T.crash, T.black, t)) + 10;
  const cx = k[1] + vnoise(t * 1.2) * sh + (t > T.empty ? Math.sin(t * 47) * sh * 0.3 : 0), cy = k[2] + vnoise(t * 1.1 + 7) * sh;
  C.save(); C.setTransform(1, 0, 0, 1, 0, 0); C.translate(W / 2, H / 2); C.scale(z, z); C.translate(-cx, -cy);
  C.drawImage(BG.studio, 0, 0);
  drawStudioScreen(t);
  const st = spikerState(t), sc = 1.8, fx = 540, fy = 1056 + 160 * sc;
  C.save(); C.translate(fx, fy); C.scale(sc, sc); C.translate(0, -160);
  SPIKER.body(st, 'back');
  C.save(); C.rotate(st.tilt || 0); C.translate(0, -SPIKER.F.chin + 10 + (st.hy || 0));
  C.beginPath(); rrect(-16, SPIKER.F.chin - 22, 32, 30, 6); fs(SPIKER.F.skin); drawHead(SPIKER, st); C.restore();
  C.restore();
  C.drawImage(BG.desk, 0, 0);
  for (let i = 0; i < 3; i++) { C.save(); C.translate(300 + i * 8, 1182 - i * 3); C.rotate(-0.08 + i * 0.05); C.beginPath(); rrect(-80, -14, 160, 22, 3); fs('#fbfbf6', 3); C.restore(); }
  const rat = t > T.empty ? inv(T.empty + 0.8, T.crash, t) : 0;
  for (let i = 0; i < 2; i++) {
    C.save(); C.translate(770 + i * 74 + Math.sin(t * 70 + i * 2) * 5 * rat, 1176 - Math.abs(Math.sin(t * 55 + i)) * 7 * rat); C.rotate(Math.sin(t * 60 + i) * 0.08 * rat);
    C.beginPath(); ell(0, 2, 34, 8); fs('#fff', 3);
    C.beginPath(); C.moveTo(-15, -50); C.quadraticCurveTo(-6, -26, -13, 0); C.lineTo(13, 0); C.quadraticCurveTo(6, -26, 15, -50); C.closePath(); fs('rgba(184,68,28,.9)', 3);
    C.fillStyle = 'rgba(255,255,255,.35)'; C.fillRect(-10, -46, 4, 30); C.restore();
  }
  C.save(); C.translate(fx, fy); C.scale(sc, sc); C.translate(0, -160); SPIKER.body(st, 'front'); C.restore();
  if (t > T.crash) { const p = eout(inv(T.crash, T.crash + 0.28, t)); drawKamyonet(lerp(-1300, -330, p), 1830, 2.1, t, { spin: t * 25, hoodA: 1.1, lights: true, usta: ustaState(t), cemal: cemalState(t) }); }
  C.restore();
  C.setTransform(1, 0, 0, 1, 0, 0);
}

''')

# ---------- sokak sahnesi yerine Bursa yolu ----------
s = cut(s, "/* ============================================================\n   SAHNE: SOKAK", "/* ============================================================\n   EKRAN ÜSTÜ", r'''/* ============================================================
   SAHNE: BURSA ÇEVRE YOLU (kayan arka plan, giden kamyonet)
   ============================================================ */
const RD = { feet: 1480, msc: 1.4, mx: 200, vx0: 380, vy: 1392 };
function buildRoadBG() {
  BG.roadFar = mk(2160, 1400); let g = BG.roadFar.getContext('2d');
  let gr = g.createLinearGradient(0, 0, 0, 1300); gr.addColorStop(0, '#78c1ee'); gr.addColorStop(1, '#d8efff'); g.fillStyle = gr; g.fillRect(0, 0, 2160, 1400);
  g.fillStyle = '#7d8fa8'; g.beginPath(); g.moveTo(0, 1050); g.lineTo(300, 760); g.lineTo(520, 840); g.lineTo(900, 430); g.lineTo(1250, 700); g.lineTo(1500, 610); g.lineTo(1900, 900); g.lineTo(2160, 1050); g.lineTo(2160, 1400); g.lineTo(0, 1400); g.closePath(); g.fill();
  g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(760, 580); g.lineTo(900, 430); g.lineTo(1060, 580); g.lineTo(1000, 560); g.lineTo(950, 600); g.lineTo(890, 555); g.lineTo(830, 600); g.closePath(); g.fill();
  g.beginPath(); g.moveTo(1400, 660); g.lineTo(1500, 610); g.lineTo(1600, 680); g.lineTo(1540, 670); g.lineTo(1490, 700); g.closePath(); g.fill();
  g.fillStyle = '#6f8f6a'; g.beginPath(); g.moveTo(0, 1100); for (let x = 0; x <= 2160; x += 60) g.lineTo(x, 1090 - Math.sin(x / 2160 * Math.PI * 4) * 30); g.lineTo(2160, 1400); g.lineTo(0, 1400); g.closePath(); g.fill();
  for (let i = 0; i < 26; i++) { const bx = i * 84 + (hash(i) * 30), bh = 50 + hash(i + 5) * 70; g.fillStyle = ['#e8d9b8', '#d9c3a0', '#f0e6d2', '#c9b79a'][i % 4]; g.fillRect(bx, 1160 - bh, 70, bh + 40); g.fillStyle = 'rgba(60,80,110,.5)'; for (let r = 0; r < bh - 20; r += 22) for (let c = 8; c < 60; c += 20) g.fillRect(bx + c, 1160 - bh + 10 + r, 10, 12); }
  g.fillStyle = '#c9c2b0'; g.fillRect(900, 1090, 300, 80);
  for (let i = 0; i < 10; i++) { g.beginPath(); g.arc(915 + i * 30, 1090, 14, Math.PI, 0); g.fill(); }
  g.fillRect(880, 1000, 10, 170); g.fillRect(1210, 1000, 10, 170);
  g.beginPath(); g.moveTo(876, 1002); g.lineTo(885, 972); g.lineTo(894, 1002); g.fill(); g.beginPath(); g.moveTo(1206, 1002); g.lineTo(1215, 972); g.lineTo(1224, 1002); g.fill();
  BG.roadMid = mk(2160, 400); g = BG.roadMid.getContext('2d');
  for (let i = 0; i < 24; i++) {
    const x = i * 90 + hash(i + 40) * 40, tall = hash(i + 60) > 0.6;
    g.fillStyle = '#6b4a2b'; g.fillRect(x + 26, tall ? 140 : 250, 10, tall ? 260 : 150);
    g.fillStyle = ['#3f8f47', '#4fa354', '#357a3c'][i % 3];
    if (tall) { g.beginPath(); g.ellipse(x + 31, 170, 26, 120, 0, 0, Math.PI * 2); g.fill(); }
    else { g.beginPath(); g.arc(x + 31, 240, 46, 0, Math.PI * 2); g.fill(); g.beginPath(); g.arc(x + 6, 260, 32, 0, Math.PI * 2); g.fill(); g.beginPath(); g.arc(x + 58, 262, 30, 0, Math.PI * 2); g.fill(); }
  }
}
function tileX(img, off, y) { const w = img.width; let x = -(((off % w) + w) % w) - 600; for (; x < 1800; x += w) C.drawImage(img, x, y); }
function roadScroll(t) { const v = 650; if (t < T.fail) return v * (t - T.s2); const d = Math.min(t - T.fail, 0.8); return v * (T.fail - T.s2) + v * (d - d * d / 1.6); }
function vanDX(t) { const df = t - T.fail; if (df <= 0) return 0; const d = Math.min(df, 0.8); let x = 1106 * d * d; if (df > 0.8) { const e = df - 0.8; x += 1770 * e + 700 * e * e; } return x; }
function ustaState(t) {
  const st = { time: t, blink: blinkAt(t, 6), jaw: jawOf('usta', t) };
  const tk = talking('usta', t);
  st.tilt = Math.sin(t * 5.5) * 0.06 * tk + vnoise(t * 0.8 + 2) * 0.03 + (tk ? 0 : 0.16);
  st.look = tk ? [-0.7, 0.1] : [0.3, 0.7]; st.lidAdd = tk ? 0 : 0.22; st.brow = tk ? 0.5 : -0.2; st.browAng = tk ? 0.1 : -0.3;
  st.wrenchHand = [84, 6 + Math.sin(t * 9) * 8]; st.wrenchAng = 1.2 + Math.sin(t * 9) * 0.2;
  const L6 = LINES[5];
  if (t > L6.at && t < L6.at + 1.7) { st.wrenchHand = [-100, -40]; st.wrenchAng = -0.3 + Math.sin(t * 12) * 0.2; st.eyeS = 1.2; st.brow = 0.9; st.lidAdd = 0; st.look = [-0.6, 0]; st.tilt = vnoise(t) * 0.03; }
  const fr = wordStart('L8', 'tutmuyor');
  if (t > fr) {
    const p = inv(fr, fr + 0.3, t);
    st.eyeS = lerp(1, 1.75, p); st.pupil = 0.45; st.brow = 1.4; st.browAng = 0.5; st.sweat = true; st.lidAdd = 0; st.look = [-0.2, -0.3];
    st.tilt = Math.sin(t * 40) * 0.05; st.walk = t * 22; st.walkAmp = 1;
    if (t > LINES[7].at + 1.25) st.jaw = 0.85 + 0.15 * Math.sin(t * 30);
  }
  return st;
}
function cemalState(t) {
  const st = { time: t, blink: blinkAt(t, 4), jaw: jawOf('esnaf', t), noNet: true };
  const tk = talking('esnaf', t);
  st.tilt = Math.sin(t * 6.1) * 0.06 * tk + vnoise(t * 0.7 + 5) * 0.03;
  st.look = [0.85, 0]; st.brow = 0.1;
  if (tk) { st.look = [-0.7, 0.1]; st.hx = -8; st.brow = 0.5; }
  const L5 = LINES[4];
  if (t > L5.at + L5.dur && t < L5.at + L5.dur + 1.5) { st.smile = 1; st.look = [-0.6, 0]; }
  const fr = wordStart('L8', 'tutmuyor');
  if (t > fr) {
    const p = inv(fr, fr + 0.4, t);
    st.eyeS = lerp(1, 1.8, p); st.pupil = 0.45; st.brow = 1.4; st.browAng = 0.6; st.sweat = true; st.look = [0.3, -0.2]; st.tilt = Math.sin(t * 36) * 0.05;
    if (t > LINES[7].at + 1.25) st.jaw = 0.8 + 0.2 * Math.sin(t * 27 + 1);
  }
  return st;
}
function muhabirRoad(t, uM, cM) {
  const st = { time: t, blink: blinkAt(t, 2), jaw: jawOf('muhabir', t) };
  const tk = talking('muhabir', t);
  st.tilt = Math.sin(t * 7.1) * 0.05 * tk + vnoise(t * 0.8 + 3) * 0.03;
  const runAmt = t < T.fail + 0.4 ? 1 : 1 - inv(T.fail + 0.4, T.fail + 1.1, t);
  st.walk = t * 15; st.walkAmp = runAmt; st.bob = Math.abs(Math.sin(t * 15)) * 10 * runAmt; st.armL = 0.4 + Math.sin(t * 15) * 0.7 * runAmt;
  st.eyeS = 1.08; st.brow = 0.6; st.browAng = 0.25; st.sweat = true;
  const tb = (wx, wy) => [(wx - RD.mx) / RD.msc, (wy - (RD.feet - 160 * RD.msc)) / RD.msc];
  const L7 = LINES[6];
  const toU = talking('usta', t) || (t > LINES[5].at - 0.2 && t < T.fail + 0.3);
  const toC = talking('esnaf', t);
  if (tk && !(t > L7.at && t < L7.at + L7.dur)) { st.micHand = [40, 34]; st.micAim = [0, -70]; st.look = [0.7, -0.2]; }
  else if (toC) { st.micHand = [104, -10]; st.micAim = tb(cM[0], cM[1]); st.look = [0.8, -0.3]; }
  else if (toU || tk) { st.micHand = [108, -14]; st.micAim = tb(uM[0], uM[1]); st.look = [0.9, -0.3]; }
  else { st.micHand = [60, 20]; st.micAim = [120, -80]; st.look = [0.8, -0.2]; }
  if (t > T.fail + 0.4) {
    const p = inv(T.fail + 0.4, T.fail + 0.9, t);
    st.look = [1, -0.1]; st.eyeS = lerp(1.08, 1.6, p); st.pupil = 0.45; st.brow = 1.3; st.browAng = 0.5; st.jaw = 0.66; st.hairUp = p;
    st.micHand = [lerp(108, 50, p), lerp(-14, 50, p)]; st.micAim = [160, 40];
  }
  if (t > T.fail + 1.9) { const p = eio(inv(T.fail + 1.9, T.fail + 2.4, t)); st.look = [1 - p, -0.1 * (1 - p)]; st.jaw = 0.34 + 0.32 * (1 - p); st.hx = -6 * p; }
  return st;
}
function drawRoad(t) {
  if (!BG.roadFar) buildRoadBG();
  const keys = [[T.s2, 470, 980, 1.08], [14.2, 420, 1000, 1.0], [19.85, 750, 960, 1.45, 'cut'], [25.25, 490, 980, 1.45, 'cut'], [28.85, 470, 1000, 1.06, 'cut'], [T.fail, 470, 1000, 1.06], [T.fail + 1.2, 380, 1030, 1.15], [T.s5, 300, 1060, 1.36]];
  const k = keyed(keys, t);
  const moving = t < T.fail + 0.8 ? 1 : 0;
  const sh = 5 + 4 * moving;
  const cx = k[1] + vnoise(t * 1.4) * sh, cy = k[2] + vnoise(t * 1.3 + 9) * sh + Math.sin(t * 23) * 2 * moving;
  const rot = t > T.fail ? -0.05 * eio(inv(T.fail, T.fail + 0.8, t)) : 0;
  C.save(); C.translate(W / 2, H / 2); C.rotate(rot); C.scale(k[3], k[3]); C.translate(-cx, -cy);
  const s = roadScroll(t);
  C.fillStyle = '#78c1ee'; C.fillRect(-600, -400, 2400, 2800);
  tileX(BG.roadFar, s * 0.06, 0);
  tileX(BG.roadMid, s * 0.4, 910);
  for (let x = -(((s * 1.0) % 700) + 700) % 700 - 600; x < 1800; x += 700) { C.fillStyle = '#3a3d44'; C.fillRect(x, 760, 14, 560); C.fillRect(x, 760, 90, 12); C.fillStyle = '#ffe9a8'; C.fillRect(x + 70, 770, 26, 10); }
  C.fillStyle = '#b9bec7'; C.fillRect(-600, 1296, 2400, 22); C.fillStyle = OUT; C.fillRect(-600, 1316, 2400, 4);
  for (let x = -((s % 160) + 160) % 160 - 600; x < 1800; x += 160) { C.fillStyle = '#8a8f98'; C.fillRect(x, 1290, 12, 46); }
  C.fillStyle = '#50535b'; C.fillRect(-600, 1336, 2400, 900);
  C.fillStyle = '#f2f2f2'; C.fillRect(-600, 1344, 2400, 6);
  for (let x = -((s % 240) + 240) % 240 - 600; x < 1800; x += 240) C.fillRect(x, 1600, 130, 12);
  if (moving) { C.strokeStyle = 'rgba(255,255,255,.45)'; C.lineWidth = 4; for (let i = 0; i < 12; i++) { const y = 820 + hash(i) * 700, x = 1700 - ((t * 2400 + hash(i + 3) * 3000) % 2600); C.beginPath(); C.moveTo(x, y); C.lineTo(x + 180 + hash(i + 7) * 120, y); C.stroke(); } }
  const dx = vanDX(t), vx = RD.vx0 + dx;
  for (let i = 0; i < 6; i++) { const ph = (t * 1.5 + i / 6) % 1; C.globalAlpha = (1 - ph) * 0.5; C.beginPath(); ell(vx - 440 - ph * 260, RD.vy - 120 - ph * 60, 20 + ph * 40, 16 + ph * 30); C.fillStyle = '#c9c9c9'; C.fill(); }
  C.globalAlpha = 1;
  const bounce = moving ? Math.abs(Math.sin(t * 19)) * 6 + vnoise(t * 6) * 3 : 0;
  drawKamyonet(vx, RD.vy, 1.0, t, { spin: (s + dx) / 64, hoodA: 1.15 + Math.sin(t * 8) * 0.06 * moving, bounce, usta: ustaState(t), cemal: cemalState(t) });
  if (t > T.fail) { const p = inv(T.fail, T.fail + 1.6, t); C.globalAlpha = 0.5 * (1 - p); C.fillStyle = '#d8cbb0'; for (let i = 0; i < 6; i++) { C.beginPath(); ell(vx - 480 - i * 60, RD.vy - 30 - hash(i) * 50, 50 + p * 80, 30 + p * 40); C.fill(); } C.globalAlpha = 1; }
  const uM = [vx + 402, RD.vy - 363], cM = [vx + 96, RD.vy - 342];
  drawChar(MUHABIR, RD.mx, RD.feet, RD.msc, muhabirRoad(t, uM, cM));
  C.restore();
}

''')

# ---------- geçişler ve render ----------
s = cut(s, "function glitchAmt(t) {", "function applyGlitch(t, a) {", r'''function glitchAmt(t) {
  const g1 = t > T.glitch1 && t < T.s2 + 0.25 ? Math.sin(inv(T.glitch1, T.s2 + 0.25, t) * Math.PI) : 0;
  const g2 = t > T.glitch2 && t < T.s5 + 0.2 ? Math.sin(inv(T.glitch2, T.s5 + 0.2, t) * Math.PI) : 0;
  const g3 = t > T.crash && t < T.crash + 0.35 ? 0.9 : 0;
  return Math.max(g1, g2, g3);
}
function cracks() {
  const cx0 = 610, cy0 = 860; C.save(); C.strokeStyle = 'rgba(255,255,255,.9)'; C.lineWidth = 4;
  for (let i = 0; i < 14; i++) { let a = i / 14 * Math.PI * 2 + hash(i) * 0.3, x = cx0, y = cy0; C.beginPath(); C.moveTo(x, y); for (let s2 = 0; s2 < 6; s2++) { a += (hash(i * 7 + s2) - 0.5) * 0.6; const L = 60 + hash(i * 3 + s2) * 120; x += Math.cos(a) * L; y += Math.sin(a) * L; C.lineTo(x, y); } C.stroke(); }
  C.lineWidth = 2; for (const r of [60, 140]) { C.beginPath(); for (let i = 0; i <= 14; i++) { const a = i / 14 * Math.PI * 2, rr = r * (0.8 + hash(i + r) * 0.4); i ? C.lineTo(cx0 + Math.cos(a) * rr, cy0 + Math.sin(a) * rr) : C.moveTo(cx0 + Math.cos(a) * rr, cy0 + Math.sin(a) * rr); } C.stroke(); }
  C.restore();
}
''')
s = cut(s, "function render(t) {", "/* ============================================================\n   OYNATMA", r'''function render(t) {
  C.setTransform(1, 0, 0, 1, 0, 0);
  C.fillStyle = '#000'; C.fillRect(0, 0, W, H);
  if (t < T.s2 || t >= T.s5) drawStudioFixed(t); else drawRoad(t);
  C.setTransform(1, 0, 0, 1, 0, 0);
  C.globalAlpha = 0.6; C.drawImage(BG.vig, 0, 0); C.globalAlpha = 1;
  if (t > T.crash) cracks();
  if (t > T.crash && t < T.crash + 0.15) { C.fillStyle = `rgba(255,255,255,${1 - (t - T.crash) / 0.15})`; C.fillRect(0, 0, W, H); }
  drawLive(t); drawKJ(t);
  drawCaptions(t);
  drawFollow(t);
  drawHook(t);
  drawMark(t);
  if (t >= T.black) { C.fillStyle = '#000'; C.fillRect(0, 0, W, H); }
  const g = glitchAmt(t); if (g > 0.02) applyGlitch(t, g);
  C.globalAlpha = 0.045; C.fillStyle = BG.grain[Math.floor(t * 60) % 4]; C.save(); C.translate(Math.floor(hash(t) * 256), Math.floor(hash(t + 1) * 256)); C.fillRect(-256, -256, W + 512, H + 512); C.restore(); C.globalAlpha = 1;
}

''')

# ---------- panel ----------
s = cut(s, "(function buildPanel() {", "  $('script').innerHTML", r'''(function buildPanel() {
  const who = { spiker: 'Spiker Berkcan', muhabir: 'Muhabir Berk', esnaf: 'Cemal Abi', usta: 'Recep Usta', aslan: 'Aslan' };
  const rows = [[0, 'Hook: SON DAKİKA damgası. Ekranda aslan vapurda martılarla (1. bölümün devamı)'], ...LINES.map(L => [L.at, `<b>${who[L.who]}:</b> ${L.text}`]),
    [T.glitch1, 'Parazitli geçiş, Bursa çevre yolu: giden kamyonet, kaputta usta, yanında koşan muhabir'],
    [T.fail, 'Fren boşalır, kamyonet uçar, muhabir arkada kalır'], [T.glitch2, 'Stüdyoya dönüş'],
    [T.follow, 'Takip et butonu ve @dandikhaber'],
    [T.empty, 'Cliffhanger: ekranda frensiz kamyonet stüdyoya iniyor, korna yaklaşıyor, çay bardakları titriyor'],
    [T.crash, 'KÜT: kamyonet stüdyoya dalar, ekran çatlar, kararır']].sort((a, b) => a[0] - b[0]).map(r => [r[0].toFixed(1), r[1]]);
''')

# 1. bölüme ait kalıntılar kalmasın
for bad in ["drawStreet(", "T.dun", "T.drop", "T.whip", "T.l6", "akbil') + 0.4", "VAPURDAYIM"]:
    assert bad not in s, bad
(HERE / "src.html").write_text(s, encoding="utf-8")
print("src.html", len(s), "chars")
