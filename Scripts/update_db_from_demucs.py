#!/usr/bin/env python3
"""
update_db_from_demucs.py
Corre Demucs + Whisper en todos los archivos de 20260807
con menos de 15 palabras y actualiza lyrics_db.json.
"""
import os, json, re, subprocess, shutil

FFMPEG   = "/opt/homebrew/bin/ffmpeg"
DEMUCS   = "/Users/agustinsackmann/Library/Python/3.9/bin/demucs"
SCRIPTS  = "/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts"
DB_PATH  = os.path.join(SCRIPTS, "lyrics_db.json")
FOLDER   = "/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Ableton/2026. Projects/CableATierra Project/20260807. Ensayo - Partes"
TMP_IN   = "/tmp/demucs_in.mp3"
TMP_OUT  = "/tmp/demucs_out"
MIN_WORDS_THRESHOLD = 15

PARTE_RE = re.compile(r'^Parte_\d+\.\s+(.+)\.mp3$', re.IGNORECASE)

def normalize(name):
    name = name.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        name = name.replace(a, b)
    return name

def separate_vocals(fpath):
    if os.path.exists(TMP_OUT):
        shutil.rmtree(TMP_OUT)
    shutil.copy2(fpath, TMP_IN)
    result = subprocess.run(
        [DEMUCS, "--two-stems=vocals", "-o", TMP_OUT, TMP_IN],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"    Demucs ERROR: {result.stderr[-200:]}")
        return None
    for root, dirs, files in os.walk(TMP_OUT):
        for f in files:
            if f == "vocals.wav":
                return os.path.join(root, f)
    return None

def transcribe(path, whisper_model):
    segs, _ = whisper_model.transcribe(
        path, beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    return " ".join(s.text.strip() for s in segs).strip()

print("Cargando Whisper medium...")
from faster_whisper import WhisperModel
whisper = WhisperModel("medium", device="cpu", compute_type="int8")
print("Listo.\n")

with open(DB_PATH) as f:
    db = json.load(f)

to_process = []
for fname in sorted(os.listdir(FOLDER)):
    m = PARTE_RE.match(fname)
    if not m:
        continue
    song  = m.group(1).strip()
    key   = normalize(song)
    fpath = os.path.join(FOLDER, fname)

    entry       = db.get(key, {})
    files       = entry.get("files", [])
    transcripts = entry.get("transcripts", [])

    if fpath in files:
        idx   = files.index(fpath)
        text  = transcripts[idx] if idx < len(transcripts) else ""
        words = len(text.split()) if text.strip() else 0
        if words < MIN_WORDS_THRESHOLD:
            to_process.append((fname, fpath, song, key, words))
    else:
        to_process.append((fname, fpath, song, key, 0))

print(f"Archivos a reprocesar con Demucs: {len(to_process)}\n")

updated = 0
for fname, fpath, song, key, old_words in to_process:
    print(f"\n{'='*55}")
    print(f"{fname} (tenía {old_words} palabras)")

    print(f"  Separando vocals...", end="", flush=True)
    vocals_path = separate_vocals(fpath)
    if not vocals_path:
        print(" FALLÓ")
        continue
    print(" OK")

    print(f"  Transcribiendo...", end="", flush=True)
    text  = transcribe(vocals_path, whisper)
    words = len(text.split()) if text.strip() else 0
    print(f" {words} palabras")
    if text:
        print(f"  → {text[:120]}")

    if words <= old_words:
        print(f"  Sin mejora.")
        continue

    # Actualizar DB — FIX: manejar transcripts más corto que files
    if key not in db:
        db[key] = {"name": song, "transcripts": [], "files": []}

    files       = db[key].get("files", [])
    transcripts = db[key].get("transcripts", [])

    if fpath in files:
        idx = files.index(fpath)
        # Extender lista si es necesario
        while len(transcripts) <= idx:
            transcripts.append("")
        transcripts[idx]       = text
        db[key]["transcripts"] = transcripts
    else:
        db[key]["files"].append(fpath)
        db[key]["transcripts"].append(text)

    print(f"  DB actualizada: {old_words} → {words} palabras")
    updated += 1

    with open(DB_PATH, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

print(f"\n{'='*55}")
print(f"Entradas mejoradas: {updated}")
print("DB guardada.")
