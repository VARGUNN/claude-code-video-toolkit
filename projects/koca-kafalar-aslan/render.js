// Dandik Haber bölümünü MP4'e render eder (tarayıcıda Render Al düğmesine gerek kalmadan).
// Görüntü: render(t) her kare için ayrı çizilir (60 fps, kare düşmez).
// Ses: sayfanın kendi miksi (recDest) gerçek zamanlı kaydedilir, sonra görüntüyle birleştirilir.
//
//   node render.js <index.html> <çıktı.mp4> [--stills 3,20,55]
//
// Ses ve görüntünün başlangıcı aynı AudioContext saatinden hizalanır.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const [, , html, out, ...rest] = process.argv;
if (!html || !out) { console.error('kullanım: node render.js <index.html> <çıktı.mp4> [--stills 3,20,55]'); process.exit(1); }
const stillsArg = rest.indexOf('--stills') >= 0 ? rest[rest.indexOf('--stills') + 1] : null;
const FPS = 60;

(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await p.goto('file://' + path.resolve(html));
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 60000 });
  const DUR = await p.evaluate(() => window.__kafa.T.DUR);

  if (stillsArg) {
    const dir = out.replace(/\.mp4$/, '') + '-stills';
    fs.mkdirSync(dir, { recursive: true });
    for (const t of stillsArg.split(',').map(Number)) {
      const d = await p.evaluate(t => { window.__kafa.render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, t);
      fs.writeFileSync(path.join(dir, `t${t}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
    }
    console.log('kareler:', dir);
    await b.close(); return;
  }

  // 1) ses: sayfanın miksini gerçek zamanlı kaydet
  console.log(`ses kaydı (${DUR} sn gerçek zamanlı)...`);
  const audio = await p.evaluate(async (DUR) => {
    await AC.resume();
    const r = new MediaRecorder(recDest.stream, { mimeType: 'audio/webm;codecs=opus', audioBitsPerSecond: 256000 });
    const chunks = []; r.ondataavailable = e => e.data.size && chunks.push(e.data);
    const done = new Promise(res => r.onstop = res);
    r.start(); const recAt = AC.currentTime;
    await startPlayback(0); const offset = ctxStart - recAt;
    await new Promise(res => setTimeout(res, (DUR + 0.6) * 1000));
    stopPlayback(); r.stop(); await done;
    const buf = await new Blob(chunks).arrayBuffer();
    let s = ''; const u = new Uint8Array(buf); for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode(...u.subarray(i, i + 0x8000));
    return { b64: btoa(s), offset };
  }, DUR);
  const tmp = out.replace(/\.mp4$/, '');
  fs.writeFileSync(tmp + '.audio.webm', Buffer.from(audio.b64, 'base64'));

  // 2) görüntü: her kareyi ayrı çiz
  const silent = tmp + '.video.mp4';
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(DUR * FPS), BATCH = 30;
  for (let i = 0; i < N; i += BATCH) {
    const frames = await p.evaluate(([i0, n, fps, DUR]) => {
      const o = []; for (let k = i0; k < Math.min(i0 + 30, n); k++) { window.__kafa.render(Math.min(k / fps, DUR - 0.001)); o.push(document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]); } return o;
    }, [i, N, FPS, DUR]);
    for (const f of frames) if (!ff.stdin.write(Buffer.from(f, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 600 === 0) console.log(`kare ${i}/${N}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await b.close();

  // 3) birleştir: sesi başlangıç farkı kadar kırp, AAC'ye çevir
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, '-ss', Math.max(0, audio.offset).toFixed(3), '-i', tmp + '.audio.webm',
    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', DUR.toFixed(3), '-movflags', '+faststart', out]);
  fs.unlinkSync(silent); fs.unlinkSync(tmp + '.audio.webm');
  console.log('bitti:', out, `(ses kayması ${audio.offset.toFixed(3)} sn)`);
})();
