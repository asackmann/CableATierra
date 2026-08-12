#!/usr/bin/env python3
"""
sync_lyrics_canciones.py
Lee lyrics_db.json y sincroniza las transcripciones con los archivos
en /Repos/Personal/CableATierra/canciones/.

- Si el archivo existe: busca la sección ## Letra y la agrega/actualiza.
- Si no existe: crea un archivo nuevo mínimo con la sección ## Letra.

Uso:
  python3 sync_lyrics_canciones.py           # sincroniza todo
  python3 sync_lyrics_canciones.py <cancion> # solo una canción
"""

import os, sys, json, re

SCRIPTS_DIR  = "/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts"
CANCIONES    = "/Users/agustinsackmann/Repos/Personal/CableATierra/canciones"
DB_PATH      = os.path.join(SCRIPTS_DIR, "lyrics_db.json")
MIN_WORDS    = 15  # no escribir letras con menos de esto


# ── Normalización ─────────────────────────────────────────────────────────────

def normalize(text):
    text = text.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.strip()

def tokenize(text):
    return set(normalize(text).split())


# ── Matching de archivo ───────────────────────────────────────────────────────

def find_canciones_file(song_name):
    """
    Busca el archivo .md en canciones/ que mejor coincide con song_name.
    Retorna (path, score) o (None, 0) si no hay match.
    """
    song_tokens = tokenize(song_name)
    best_path, best_score = None, 0

    for fname in os.listdir(CANCIONES):
        if not fname.endswith(".md") or fname.startswith("_"):
            continue
        # Extraer slug: quitar prefijo numérico y extensión
        slug = re.sub(r"^\d+-", "", fname[:-3])
        slug_tokens = tokenize(slug.replace("-", " "))

        # Overlap de tokens
        overlap = len(song_tokens & slug_tokens)
        # Score: overlap / max(len) para penalizar matches parciales
        score = overlap / max(len(song_tokens), len(slug_tokens), 1)

        if score > best_score:
            best_score = score
            best_path  = os.path.join(CANCIONES, fname)

    return (best_path, best_score) if best_score >= 0.4 else (None, 0)


def next_file_number():
    """Retorna el siguiente número disponible para un archivo nuevo."""
    nums = []
    for fname in os.listdir(CANCIONES):
        m = re.match(r"^(\d+)-", fname)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def song_to_slug(name):
    slug = normalize(name)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return slug


# ── Sección Letra ─────────────────────────────────────────────────────────────

LETRA_HEADER  = "## Letra (transcripción automática)"
LETRA_WARNING = "> ⚠️ Generada por Whisper + Demucs — puede contener errores o fragmentos de charla de ensayo. Revisar y limpiar."

def has_letra_section(content):
    return "## Letra" in content

def build_letra_section(transcript):
    return f"""{LETRA_HEADER}

{LETRA_WARNING}

{transcript}

---"""

def update_letra_in_content(content, transcript):
    """Reemplaza o agrega la sección ## Letra en el contenido."""
    new_section = build_letra_section(transcript)

    if has_letra_section(content):
        # Reemplazar sección existente
        # Captura desde ## Letra hasta el próximo ## o fin de archivo
        pattern = r"## Letra.*?(?=\n## |\Z)"
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        return new_content
    else:
        # Agregar al final
        return content.rstrip() + "\n\n" + new_section + "\n"


def create_new_file(song_name, transcript):
    """Crea un archivo nuevo mínimo con nombre y sección Letra."""
    num  = next_file_number()
    slug = song_to_slug(song_name)
    fname = f"{num:02d}-{slug}.md"
    path  = os.path.join(CANCIONES, fname)

    content = f"""# {song_name}

## Info General

| Campo        | Valor         |
|--------------|---------------|
| **Estado**   | 🔴 pendiente  |

---

{build_letra_section(transcript)}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path, fname


# ── Main ──────────────────────────────────────────────────────────────────────

def sync_song(song_name, transcript, verbose=True):
    """
    Sincroniza una canción. Retorna ('created'|'updated'|'skipped', path).
    """
    words = len(transcript.split()) if transcript.strip() else 0
    if words < MIN_WORDS:
        if verbose:
            print(f"  SKIP (solo {words} palabras)")
        return "skipped", None

    path, score = find_canciones_file(song_name)

    if path:
        if verbose:
            print(f"  Archivo: {os.path.basename(path)} (match={score:.2f})")
        with open(path, encoding="utf-8") as f:
            content = f.read()

        action = "actualizada" if has_letra_section(content) else "agregada"
        new_content = update_letra_in_content(content, transcript)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        if verbose:
            print(f"  Letra {action} ({words} palabras)")
        return "updated", path
    else:
        if verbose:
            print(f"  Sin archivo existente — creando nuevo")
        path, fname = create_new_file(song_name, transcript)
        if verbose:
            print(f"  Creado: {fname} ({words} palabras)")
        return "created", path


def main():
    with open(DB_PATH) as f:
        db = json.load(f)

    filter_song = sys.argv[1].lower() if len(sys.argv) > 1 else None

    created = updated = skipped = 0

    for key, entry in sorted(db.items()):
        song_name   = entry.get("name", key)
        transcripts = entry.get("transcripts", [])

        if filter_song and filter_song not in song_name.lower():
            continue

        # Combinar todos los transcripts en uno (el más largo gana)
        best_text = max(transcripts, key=lambda t: len(t.split()) if t else 0, default="")

        print(f"\n{song_name}")
        action, path = sync_song(song_name, best_text)

        if action == "created":   created  += 1
        elif action == "updated": updated  += 1
        else:                     skipped  += 1

    print(f"\n{'─'*50}")
    print(f"Creados: {created} | Actualizados: {updated} | Saltados: {skipped}")


if __name__ == "__main__":
    main()
