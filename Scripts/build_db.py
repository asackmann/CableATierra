"""
build_db.py — CableATierra fingerprint database builder
Procesa carpetas de partes con nombre (Parte_XX. Nombre de cancion.mp3)
y construye/actualiza un maestro de fingerprints en fingerprint_db.json.

Si una cancion ya tiene entradas previas, promedia las features (más robusto).

Uso:
  python3 build_db.py                          # procesa todas las carpetas en project_root
  python3 build_db.py <carpeta_partes>         # agrega una carpeta específica
  python3 build_db.py --list                   # muestra canciones en la DB actual
"""
import os, sys, json, re, subprocess, datetime
import numpy as np

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPTS_DIR, "config.json")
DB_PATH     = os.path.join(SCRIPTS_DIR, "fingerprint_db.json")

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

PROJECT = CFG["project_root"]
FFMPEG  = CFG.get("ffmpeg", "/opt/homebrew/bin/ffmpeg")
SR      = 22050
SECS    = 120

# ── Feature extraction (igual que fingerprint.py) ──────────────────────────────

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

# ── DB helpers ─────────────────────────────────────────────────────────────────

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f:
            db = json.load(f)
        # Convertir listas a numpy arrays
        for song in db["songs"]:
            db["songs"][song]["features"] = [
                np.array(v) for v in db["songs"][song]["features"]
            ]
        return db
    return {"songs": {}, "updated": None, "sources": []}

def save_db(db):
    # Serializar numpy arrays como listas
    out = {"songs": {}, "updated": datetime.date.today().isoformat(),
           "sources": db.get("sources", [])}
    for song, data in db["songs"].items():
        out["songs"][song] = {
            "features": [v.tolist() for v in data["features"]],
            "n_recordings": len(data["features"]),
            "sources": data.get("sources", [])
        }
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

def song_from_filename(fname):
    """
    Extrae nombre de cancion de:
      'Parte_01. Alta Suciedad.mp3'  → 'Alta Suciedad'
      'Parte_01.mp3'                 → None
    """
    base = fname.replace(".mp3", "")
    if "." in base:
        parts = base.split(".", 1)
        name = parts[1].strip()
        return name if name else None
    return None

def find_named_parts_dirs():
    """Busca subcarpetas con partes nombradas en el proyecto."""
    dirs = []
    for entry in os.listdir(PROJECT):
        full = os.path.join(PROJECT, entry)
        if not os.path.isdir(full):
            continue
        if "Ensayo - Partes" not in entry and "Partes" not in entry:
            continue
        # Verificar que tiene al menos un archivo con nombre de cancion
        named = [f for f in os.listdir(full)
                 if f.endswith(".mp3") and song_from_filename(f)]
        if named:
            dirs.append(full)
    return dirs

# ── Main ───────────────────────────────────────────────────────────────────────

def add_folder(db, folder_path, verbose=True):
    """Agrega todos los MP3 nombrados de una carpeta a la DB."""
    added = 0
    folder_name = os.path.basename(folder_path)

    for fname in sorted(os.listdir(folder_path)):
        if not fname.endswith(".mp3"):
            continue
        song = song_from_filename(fname)
        if not song:
            continue  # sin nombre → no es referencia

        mp3_path = os.path.join(folder_path, fname)
        source_key = f"{folder_name}/{fname}"

        # No re-procesar el mismo archivo
        if song in db["songs"]:
            if source_key in db["songs"][song].get("sources", []):
                if verbose:
                    print(f"  (ya en DB) {song}")
                continue

        if verbose:
            print(f"  → Procesando: {song}  [{fname}]")

        feat = get_features(mp3_path)
        if feat is None:
            if verbose:
                print(f"     ✗ audio insuficiente, saltando")
            continue

        if song not in db["songs"]:
            db["songs"][song] = {"features": [], "sources": []}

        db["songs"][song]["features"].append(feat)
        db["songs"][song]["sources"].append(source_key)
        added += 1

    return added

def list_db(db):
    print(f"\n{'─'*55}")
    print(f"{'Cancion':40s} {'Grabaciones':>10}")
    print(f"{'─'*55}")
    for song in sorted(db["songs"]):
        n = len(db["songs"][song]["features"])
        print(f"  {song:40s} {n:>10}")
    print(f"{'─'*55}")
    print(f"Total: {len(db['songs'])} canciones\n")

def main():
    db = load_db()

    if "--list" in sys.argv:
        list_db(db)
        return

    # Carpeta específica o todas las disponibles
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        folders = [os.path.abspath(sys.argv[1])]
    else:
        folders = find_named_parts_dirs()
        if not folders:
            print("No se encontraron carpetas de partes con nombre en el proyecto.")
            return

    total = 0
    for folder in folders:
        print(f"\nCarpeta: {os.path.basename(folder)}")
        n = add_folder(db, folder)
        total += n
        print(f"  {n} nuevas entradas")

    if total > 0:
        save_db(db)
        print(f"\nDB actualizada: {DB_PATH}")
        print(f"  {total} entradas nuevas")
    else:
        print("\nSin entradas nuevas (todo ya estaba en la DB).")

    list_db(db)

if __name__ == "__main__":
    sys.path.insert(0, SCRIPTS_DIR)
    main()
