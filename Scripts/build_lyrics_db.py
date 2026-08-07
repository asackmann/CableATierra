#!/usr/bin/env python3
"""
build_lyrics_db.py — CableATierra lyrics database builder

Transcribe todos los archivos MP3 nombrados (Parte_XX. Song Name.mp3)
con faster-whisper y construye/actualiza lyrics_db.json.

Uso:
  python3 build_lyrics_db.py                   # procesa todas las carpetas
  python3 build_lyrics_db.py <carpeta_partes>  # solo una carpeta
  python3 build_lyrics_db.py --list            # muestra canciones en la DB
  python3 build_lyrics_db.py --model medium    # especifica modelo (default: medium)
  python3 build_lyrics_db.py --retry-silent    # re-intenta archivos sin voz
"""

import os, sys, json, re, datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPTS_DIR, "config.json")
DB_PATH     = os.path.join(SCRIPTS_DIR, "lyrics_db.json")

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

PROJECT         = CFG["project_root"]
FFMPEG          = CFG.get("ffmpeg", "/opt/homebrew/bin/ffmpeg")
DEFAULT_MODEL   = CFG.get("whisper_model", "medium")
TRANSCRIBE_SECS = CFG.get("transcribe_secs", 180)
TRANSCRIBE_OFF  = CFG.get("transcribe_offset", 30)  # segundos a saltear al inicio


# ── Transcripción ─────────────────────────────────────────────────────────────

def transcribe(path, model, secs=None, offset=None):
    """
    Transcribe `secs` segundos del archivo empezando en `offset`.
    Retorna el texto transcripto (string).
    """
    import subprocess, tempfile

    if secs   is None: secs   = TRANSCRIBE_SECS
    if offset is None: offset = TRANSCRIBE_OFF

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        cmd = [
            FFMPEG, "-y",
            "-ss", str(offset),      # saltear intro instrumental
            "-i", path,
            "-t", str(secs),
            "-ar", "16000",
            "-ac", "1",
            "-f", "wav",
            tmp_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return ""

        segments, info = model.transcribe(
            tmp_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
        )
        text = " ".join(seg.text.strip() for seg in segments).strip()
        return text

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ── DB helpers ────────────────────────────────────────────────────────────────

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f:
            return json.load(f)
    return {}


def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def normalize_name(name):
    name = name.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        name = name.replace(a, b)
    return name


# ── Proceso de carpeta ────────────────────────────────────────────────────────

PARTE_RE = re.compile(r'^Parte_\d+\.\s+(.+)\.mp3$', re.IGNORECASE)


def add_folder(folder_path, model, db, retry_silent=False):
    folder_name = os.path.basename(folder_path)
    print(f"\nCarpeta: {folder_name}")

    files = sorted(f for f in os.listdir(folder_path) if PARTE_RE.match(f))
    if not files:
        print("  (sin archivos nombrados)")
        return 0

    new_count = 0
    for fname in files:
        m = PARTE_RE.match(fname)
        song  = m.group(1).strip()
        key   = normalize_name(song)
        fpath = os.path.join(folder_path, fname)

        existing        = db.get(key, {})
        processed_files = existing.get("files", [])
        transcripts     = existing.get("transcripts", [])

        # Ya procesado con texto → skip
        if fpath in processed_files:
            # Si tenía "sin voz" y pedimos retry, reprocesar
            file_idx = processed_files.index(fpath)
            already_has_text = (file_idx < len(transcripts) and transcripts[file_idx].strip())
            if already_has_text or not retry_silent:
                status = "con texto" if already_has_text else "sin voz (skip)"
                print(f"  (ya procesado, {status}) {song}")
                continue
            else:
                # Reprocesar: sacar el registro anterior
                processed_files.pop(file_idx)
                if file_idx < len(transcripts):
                    transcripts.pop(file_idx)
                db[key]["files"]       = processed_files
                db[key]["transcripts"] = transcripts
                print(f"  Re-intentando (tenía sin voz): {song} ...", end="", flush=True)
        else:
            print(f"  Transcribiendo: {song} ...", end="", flush=True)

        text = transcribe(fpath, model)

        if not text:
            print(" (sin voz detectada)")
        else:
            print(f" {len(text.split())} palabras")

        if key not in db:
            db[key] = {"name": song, "transcripts": [], "files": []}
        elif "files" not in db[key]:
            db[key]["files"] = []

        db[key]["transcripts"].append(text)
        db[key]["files"].append(fpath)
        if text:
            new_count += 1

    return new_count


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if "--list" in args:
        db = load_db()
        if not db:
            print("DB vacía.")
            return
        print(f"\n{'Canción':<40} {'Archivos':>8} {'Con texto':>10}")
        print("─" * 62)
        for key, entry in sorted(db.items()):
            total     = len(entry.get("files", []))
            with_text = len([t for t in entry.get("transcripts", []) if t.strip()])
            print(f"  {entry['name']:<38} {total:>8} {with_text:>10}")
        print(f"\nTotal: {len(db)} canciones")
        return

    retry_silent = "--retry-silent" in args

    model_name = DEFAULT_MODEL
    if "--model" in args:
        idx = args.index("--model")
        model_name = args[idx + 1]

    # Carpetas a procesar
    explicit = [a for a in args if not a.startswith("--") and os.path.isdir(a)]
    target_dirs = explicit if explicit else []

    if not target_dirs:
        for entry in sorted(os.listdir(PROJECT)):
            if "Ensayo - Partes" in entry:
                target_dirs.append(os.path.join(PROJECT, entry))

    if not target_dirs:
        print("No se encontraron carpetas de partes.")
        return

    print(f"Modelo: {model_name} | offset: {TRANSCRIBE_OFF}s | ventana: {TRANSCRIBE_SECS}s")
    print(f"Cargando modelo Whisper '{model_name}'...")
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    print("Modelo listo.")

    db = load_db()
    total_new = 0

    for d in target_dirs:
        total_new += add_folder(d, model, db, retry_silent=retry_silent)
        save_db(db)

    print(f"\n{'─'*50}")
    print(f"Transcripciones nuevas/actualizadas: {total_new}")
    print(f"Total canciones en DB: {len(db)}")
    print(f"DB guardada en: {DB_PATH}")


if __name__ == "__main__":
    main()
