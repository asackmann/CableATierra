"""
fingerprint.py — CableATierra pipeline
Compara partes sin nombre contra el maestro de fingerprints (fingerprint_db.json).
Si no existe la DB, cae a comparar contra archivos MP3 de referencia directamente.

Uso: python3 fingerprint.py <target_dir> [reference_dir] [output.json]
"""
import subprocess, os, json, sys, datetime
import numpy as np

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH     = os.path.join(SCRIPTS_DIR, "fingerprint_db.json")
CONFIG_PATH = os.path.join(SCRIPTS_DIR, "config.json")

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

FFMPEG = CFG.get("ffmpeg", "/opt/homebrew/bin/ffmpeg")
SR     = 22050
SECS   = 120

# ── Feature extraction ─────────────────────────────────────────────────────────

def get_audio(path):
    r = subprocess.run(
        [FFMPEG, "-v", "quiet", "-i", path,
         "-t", str(SECS), "-f", "f32le", "-ar", str(SR), "-ac", "1", "pipe:1"],
        capture_output=True
    )
    return np.frombuffer(r.stdout, dtype=np.float32).copy()

def chroma(y, sr, hop=512, fft_size=2048):
    freqs = np.fft.rfftfreq(fft_size, 1/sr)
    mat = []
    for i in range(0, len(y)-fft_size, hop):
        frame = y[i:i+fft_size] * np.hanning(fft_size)
        mag = np.abs(np.fft.rfft(frame))
        cf = np.zeros(12)
        for j, f in enumerate(freqs[1:], 1):
            if 80 <= f <= 4000:
                pc = int(round(12 * np.log2(f / 440) + 69)) % 12
                cf[pc] += mag[j]
        mat.append(cf)
    return np.array(mat) if mat else np.zeros((1, 12))

def spectral_features(y, sr, hop=512, fft_size=2048):
    freqs = np.fft.rfftfreq(fft_size, 1/sr)
    feats = []
    for i in range(0, len(y)-fft_size, hop):
        frame = y[i:i+fft_size] * np.hanning(fft_size)
        mag = np.abs(np.fft.rfft(frame))
        power = mag**2
        total = power.sum() + 1e-10
        centroid = (freqs * power).sum() / total
        ri = np.searchsorted(np.cumsum(power), 0.85 * total)
        rolloff = freqs[min(ri, len(freqs)-1)]
        bass   = power[freqs < 300].sum() / total
        mid    = power[(freqs >= 300) & (freqs < 2000)].sum() / total
        treble = power[freqs >= 2000].sum() / total
        feats.append([centroid/sr, rolloff/sr, bass, mid, treble])
    return np.array(feats) if feats else np.zeros((1, 5))

def get_features(path):
    y = get_audio(path)
    if len(y) < SR * 5:
        return None
    rms = np.sqrt((y**2).mean())
    if rms > 0:
        y = y / (rms * 10)
    ch = chroma(y, SR)
    sp = spectral_features(y, SR)
    return np.concatenate([ch.mean(0), ch.std(0), sp.mean(0), sp.std(0)])

def cosine_sim(a, b):
    d = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / d) if d > 1e-9 else 0.0

# ── Cargar referencias ─────────────────────────────────────────────────────────

def load_refs_from_db():
    """Carga la DB y devuelve {song: feature_vector_promediado}."""
    if not os.path.exists(DB_PATH):
        return None
    with open(DB_PATH) as f:
        db = json.load(f)
    refs = {}
    for song, data in db["songs"].items():
        vecs = [np.array(v) for v in data["features"]]
        refs[song] = np.mean(vecs, axis=0)   # promedio de todas las grabaciones
    n = sum(len(data["features"]) for data in db["songs"].values())
    print(f"  DB: {len(refs)} canciones, {n} grabaciones en total")
    return refs

def load_refs_from_dir(ref_dir):
    """Fallback: extrae features de archivos MP3 nombrados en ref_dir."""
    refs = {}
    for f in sorted(os.listdir(ref_dir)):
        if not f.endswith(".mp3"):
            continue
        parts = f.replace(".mp3", "").split(".", 1)
        if len(parts) < 2 or not parts[1].strip():
            continue
        song = parts[1].strip()
        feat = get_features(os.path.join(ref_dir, f))
        if feat is not None:
            refs[song] = feat
            print(f"  ✓ {song}")
    return refs

# ── Fingerprinting ─────────────────────────────────────────────────────────────

def fingerprint(target_dir, ref_dir=None, out_json=None,
                gap_ok=0.010, gap_media=0.002):

    # Preferir DB, fallback a directorio
    print("Cargando referencias...")
    refs = load_refs_from_db()
    if refs:
        print(f"  → Usando maestro de fingerprints ({DB_PATH})")
    elif ref_dir and os.path.isdir(ref_dir):
        print(f"  → DB no encontrada, usando directorio: {ref_dir}")
        refs = load_refs_from_dir(ref_dir)
    else:
        print("ERROR: No hay DB ni directorio de referencia disponible.")
        print("  Correr: python3 build_db.py")
        return []

    print(f"\nAnalizando partes en: {target_dir}")
    results = []
    for f in sorted(os.listdir(target_dir)):
        if not f.endswith(".mp3"):
            continue
        # Ignorar archivos ya nombrados (tienen un punto después del número)
        base = f.replace(".mp3", "")
        if re.search(r"Parte_\d+\.", base):
            continue

        feat = get_features(os.path.join(target_dir, f))
        if feat is None:
            continue

        scores = {s: cosine_sim(feat, rf) for s, rf in refs.items()}
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        best, best_sc = ranked[0]
        sec_sc = ranked[1][1] if len(ranked) > 1 else 0
        gap = best_sc - sec_sc
        conf = "OK" if gap >= gap_ok else ("MEDIA" if gap >= gap_media else "BAJA")
        results.append({
            "file": f,
            "song": best,
            "score": round(best_sc, 4),
            "gap": round(gap, 4),
            "confidence": conf,
            "top3": [[s, round(sc, 4)] for s, sc in ranked[:3]]
        })
        icon = "✅" if conf == "OK" else ("⚠️ " if conf == "MEDIA" else "❌")
        print(f"  {icon} {f:30s} → {best:35s} gap={gap:.4f}")

    if out_json:
        with open(out_json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2, ensure_ascii=False)
        print(f"\nGuardado: {out_json}")

    return results

import re  # necesario para el regex dentro de fingerprint()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 fingerprint.py <target_dir> [reference_dir] [output.json]")
        sys.exit(1)
    tgt  = sys.argv[1]
    ref  = sys.argv[2] if len(sys.argv) > 2 else None
    out  = sys.argv[3] if len(sys.argv) > 3 else os.path.join(tgt, "fingerprinting_results.json")
    sys.path.insert(0, SCRIPTS_DIR)
    fingerprint(tgt, ref, out)
