#!/usr/bin/env python3
"""
sync_bpm_canciones.py
Detecta BPM de cada canción usando librosa y actualiza los archivos
del cancionero en /Repos/Personal/CableATierra/canciones/.

- Promedia el BPM entre múltiples grabaciones de la misma canción.
- Si el campo BPM en el markdown ya tiene valor, agrega "(auto: X)" como referencia.
- Si está vacío, lo completa directamente.
- Guarda resultados en bpm_db.json para consulta rápida futura.

Uso:
  python3 sync_bpm_canciones.py        # procesa todo
  python3 sync_bpm_canciones.py --list # muestra BPMs detectados
"""

import os, sys, json, re
import numpy as np

SCRIPTS_DIR = "/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts"
CANCIONES   = "/Users/agustinsackmann/Repos/Personal/CableATierra/canciones"
PROJECT     = "/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Ableton/2026. Projects/CableATierra Project"
BPM_DB      = os.path.join(SCRIPTS_DIR, "bpm_db.json")

PARTE_RE = re.compile(r'^Parte_\d+\.\s+(.+)\.mp3$', re.IGNORECASE)
LOAD_SECS = 60   # segundos a cargar por archivo (suficiente para tempo)


# ── Normalización ─────────────────────────────────────────────────────────────

def normalize(text):
    text = text.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9\s]", " ", text).strip()

def tokenize(text):
    return set(normalize(text).split())


# ── Detección de BPM ──────────────────────────────────────────────────────────

def detect_bpm(path, duration=LOAD_SECS):
    """
    Detecta el BPM de un archivo de audio.
    Usa los primeros `duration` segundos para velocidad.
    Retorna float o None si falla.
    """
    import librosa
    try:
        y, sr = librosa.load(path, duration=duration, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # beat_track puede retornar array en versiones nuevas
        if hasattr(tempo, '__len__'):
            tempo = float(tempo[0])
        else:
            tempo = float(tempo)
        # Sanity check: BPM razonable para música de banda (50-250)
        if 50 <= tempo <= 250:
            return round(tempo, 1)
        # Intentar doble/mitad si está fuera de rango
        if tempo < 50 and tempo * 2 <= 250:
            return round(tempo * 2, 1)
        if tempo > 250 and tempo / 2 >= 50:
            return round(tempo / 2, 1)
        return None
    except Exception as e:
        print(f"    ERROR detectando BPM: {e}")
        return None


# ── Matching de archivo canciones ─────────────────────────────────────────────

def find_canciones_file(song_name):
    song_tokens = tokenize(song_name)
    best_path, best_score = None, 0
    for fname in os.listdir(CANCIONES):
        if not fname.endswith(".md") or fname.startswith("_"):
            continue
        slug = re.sub(r"^\d+-", "", fname[:-3])
        slug_tokens = tokenize(slug.replace("-", " "))
        overlap = len(song_tokens & slug_tokens)
        score = overlap / max(len(song_tokens), len(slug_tokens), 1)
        if score > best_score:
            best_score = score
            best_path  = os.path.join(CANCIONES, fname)
    return (best_path, best_score) if best_score >= 0.4 else (None, 0)


# ── Actualizar BPM en markdown ────────────────────────────────────────────────

def update_bpm_in_file(path, bpm, song_name):
    """
    Busca la fila **BPM** en el archivo markdown y actualiza el valor.
    Si ya tiene valor de usuario, agrega referencia auto.
    Retorna True si actualizó algo.
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()

    bpm_str = f"{bpm:.0f} BPM"

    # Buscar fila del BPM en tabla markdown
    # Formato: | **BPM** | valor |
    pattern = r'(\|\s*\*\*BPM\*\*\s*\|\s*)([^|\n]*)(\s*\|)'

    m = re.search(pattern, content)
    if not m:
        print(f"    Sin campo BPM en {os.path.basename(path)}")
        return False

    current_val = m.group(2).strip()

    if not current_val:
        # Campo vacío → completar directamente
        new_row = m.group(1) + f" {bpm_str} " + m.group(3)
        print(f"    BPM completado: {bpm_str}")
    elif "auto:" in current_val:
        # Ya tiene auto → actualizar solo el auto
        new_val = re.sub(r"\(auto:[^)]+\)", f"(auto: {bpm_str})", current_val)
        new_row = m.group(1) + f" {new_val} " + m.group(3)
        print(f"    BPM auto actualizado: {bpm_str}")
    else:
        # Tiene valor de usuario → agregar referencia sin pisar
        new_row = m.group(1) + f" {current_val} (auto: {bpm_str}) " + m.group(3)
        print(f"    BPM existente '{current_val}' → agregado referencia (auto: {bpm_str})")

    new_content = content[:m.start()] + new_row + content[m.end():]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "--list" in sys.argv:
        if os.path.exists(BPM_DB):
            with open(BPM_DB) as f:
                db = json.load(f)
            print(f"\n{'Canción':<35} {'BPMs detectados':>30} {'Promedio':>10}")
            print("─" * 78)
            for song, data in sorted(db.items()):
                bpms = data.get("bpms", [])
                avg  = round(sum(bpms) / len(bpms), 1) if bpms else "—"
                print(f"  {song:<33} {str([round(b) for b in bpms]):>30} {str(avg):>10}")
        else:
            print("bpm_db.json no existe todavía.")
        return

    # Cargar o iniciar DB
    bpm_db = {}
    if os.path.exists(BPM_DB):
        with open(BPM_DB) as f:
            bpm_db = json.load(f)

    # Recopilar todos los archivos nombrados de todas las carpetas
    all_files = []
    for entry in os.listdir(PROJECT):
        if "Ensayo - Partes" not in entry:
            continue
        folder = os.path.join(PROJECT, entry)
        for fname in sorted(os.listdir(folder)):
            m = PARTE_RE.match(fname)
            if m:
                all_files.append((m.group(1).strip(), os.path.join(folder, fname)))

    print(f"Archivos a analizar: {len(all_files)}\n")

    # Detectar BPM por archivo
    for song_name, fpath in all_files:
        key = normalize(song_name)
        print(f"  {os.path.basename(fpath)}", end="", flush=True)

        # Chequear si ya lo procesamos (mismo path)
        existing = bpm_db.get(key, {})
        if fpath in existing.get("files", []):
            bpms = existing.get("bpms", [])
            idx  = existing["files"].index(fpath)
            print(f" → ya procesado ({bpms[idx] if idx < len(bpms) else '?'} BPM)")
            continue

        bpm = detect_bpm(fpath)
        if bpm is None:
            print(f" → no detectado")
            continue

        print(f" → {bpm} BPM")

        if key not in bpm_db:
            bpm_db[key] = {"name": song_name, "bpms": [], "files": []}
        bpm_db[key]["bpms"].append(bpm)
        bpm_db[key]["files"].append(fpath)

        # Guardar progresivamente
        with open(BPM_DB, "w") as f:
            json.dump(bpm_db, f, ensure_ascii=False, indent=2)

    # Actualizar archivos del cancionero con BPM promedio
    print(f"\n{'─'*55}")
    print("Actualizando cancionero...\n")

    updated = 0
    for key, data in bpm_db.items():
        bpms = data.get("bpms", [])
        if not bpms:
            continue
        avg_bpm = round(sum(bpms) / len(bpms))
        song_name = data["name"]

        path, score = find_canciones_file(song_name)
        if not path:
            print(f"  {song_name}: sin archivo en cancionero (score bajo)")
            continue

        print(f"  {song_name} → {avg_bpm} BPM (promedio de {len(bpms)} grabaciones)")
        print(f"    Archivo: {os.path.basename(path)}")
        if update_bpm_in_file(path, avg_bpm, song_name):
            updated += 1

    print(f"\n{'─'*55}")
    print(f"Archivos del cancionero actualizados: {updated}")
    print(f"BPM DB guardada en: {BPM_DB}")


if __name__ == "__main__":
    main()
