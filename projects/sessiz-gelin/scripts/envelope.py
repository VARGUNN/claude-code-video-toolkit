"""Per-frame loudness envelope (0..1) for each line, used to drive mouth shapes."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
root = Path(__file__).resolve().parent.parent
out = {}
for wav in sorted((root / "public/lines").glob("l*.wav")):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-ar", "24000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop = 24000 // 30
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    env = np.clip((rms / (np.percentile(rms, 90) + 1e-6)), 0, 1)
    out[wav.stem] = {"frames": len(env), "env": [round(float(x), 2) for x in env]}
(root / "src/envelopes.json").write_text(json.dumps(out))
print({k: v["frames"] for k, v in out.items()})
