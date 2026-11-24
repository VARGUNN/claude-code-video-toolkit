"""src.html + audio/L*.mp3 -> index.html (tek dosya, sesler gömülü)."""
import base64, json, pathlib
d = pathlib.Path(__file__).parent
aud = {f"L{i}": "data:audio/mpeg;base64," + base64.b64encode((d / f"audio/L{i}.mp3").read_bytes()).decode() for i in range(1, 11)}
src = (d / "src.html").read_text(encoding="utf-8")
(d / "index.html").write_text(src.replace("__AUDIO_JSON__", json.dumps(aud)), encoding="utf-8")
print("index.html", round((d / "index.html").stat().st_size / 1e6, 2), "MB")
