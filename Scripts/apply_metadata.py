"""
apply_metadata.py — CableATierra pipeline
Lee mapping.csv de la carpeta de partes y aplica ID3 tags con ffmpeg.

Formato mapping.csv:
  parte,cancion,confianza
  Parte_01,Alta Suciedad,MANUAL
  Parte_05,Como un cuento,OK

Uso: python3 apply_metadata.py <partes_dir> [mapping.csv]
     Si no se especifica mapping.csv, busca uno en partes_dir.
"""
import subprocess, os, sys, csv, shutil, tempfile, re

FFMPEG = "/opt/homebrew/bin/ffmpeg"

def apply_tag(mp3_path, title, artist="CableATierra", album=None, year="2026"):
    tmp = mp3_path + ".tmp.mp3"
    cmd = [
        FFMPEG, "-y", "-i", mp3_path,
        "-c:a", "copy",
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"date={year}",
        tmp
    ]
    if album:
        cmd.extend(["-metadata", f"album={album}"])
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0:
        os.replace(tmp, mp3_path)
        return True
    if os.path.exists(tmp):
        os.remove(tmp)
    return False

def rename_file(old_path, new_name):
    """Renombra el archivo MP3 con el nombre de la canción.
    Idempotente: si el archivo ya viene renombrado (ej. "Parte_03. Viejo Nombre.mp3"),
    toma solo el número/letra de parte y descarta el nombre viejo, en vez de
    concatenarlo (evita "Parte_03. Viejo Nombre. Nuevo Nombre.mp3").
    """
    dirn = os.path.dirname(old_path)
    base = os.path.basename(old_path)
    m = re.match(r"Parte_([0-9]+[a-zA-Z]?)", base)
    num = m.group(1) if m else "00"
    safe_name = new_name.replace("/", "-").replace(":", "-")
    new_fname = f"Parte_{num}. {safe_name}.mp3"
    new_path = os.path.join(dirn, new_fname)
    if old_path != new_path:
        os.rename(old_path, new_path)
    return new_path, new_fname

def update_m3u(partes_dir, renamed):
    """Refleja en el/los .m3u los Parte_NN que se renombraron con nombre de canción.
    renamed: lista de (num_str, song), ej. [("01", "Alta Suciedad"), ...]
    """
    if not renamed:
        return
    m3u_files = [f for f in os.listdir(partes_dir) if f.endswith(".m3u")]
    for m3u_name in m3u_files:
        m3u_path = os.path.join(partes_dir, m3u_name)
        lines = []
        with open(m3u_path, encoding="utf-8") as f:
            for line in f.readlines():
                line = line.rstrip("\n")
                for num, song in renamed:
                    safe = song.replace("/", "-").replace(":", "-")
                    old_file = f"Parte_{num}.mp3"
                    new_file = f"Parte_{num}. {safe}.mp3"
                    if line.strip() == old_file:
                        line = new_file
                    m = re.match(rf"(#EXTINF:\d+,)Parte {num}(\s.*)?$", line)
                    if m:
                        line = f"{m.group(1)}Parte {num}. {safe}"
                lines.append(line)
        with open(m3u_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")


def apply_from_mapping(partes_dir, mapping_csv=None, artist="CableATierra",
                       year="2026", rename=True):
    if mapping_csv is None:
        mapping_csv = os.path.join(partes_dir, "mapping.csv")

    if not os.path.exists(mapping_csv):
        print(f"No se encontró mapping.csv en {partes_dir}")
        return

    # Leer mapping
    mapping = {}
    with open(mapping_csv, encoding="utf-8") as f:
        for row in csv.DictReader(row for row in f if not row.startswith("#")):
            if row.get("cancion", "").strip():
                mapping[row["parte"].strip()] = row["cancion"].strip()

    if not mapping:
        print("mapping.csv no tiene canciones completadas. Llenalo primero.")
        return

    print(f"Aplicando metadata a {len(mapping)} partes...")
    album = os.path.basename(partes_dir)

    renamed = []
    for fname in sorted(os.listdir(partes_dir)):
        if not fname.endswith(".mp3"):
            continue
        base = fname.replace(".mp3", "")
        # Soporta "Parte_01" y "Parte_01. Nombre"
        parte_key = base.split(".")[0].strip() if "." in base else base

        if parte_key not in mapping:
            continue

        song = mapping[parte_key]
        mp3_path = os.path.join(partes_dir, fname)

        ok = apply_tag(mp3_path, song, artist, album, year)
        if ok and rename:
            new_path, new_fname = rename_file(mp3_path, song)
            print(f"  ✓ {fname} → {new_fname}")
            renamed.append((parte_key.split("_")[1], song))
        elif ok:
            print(f"  ✓ {fname} (tag: {song})")
        else:
            print(f"  ✗ {fname} (error al aplicar tag)")

    update_m3u(partes_dir, renamed)
    if renamed:
        print("Playlist(s) actualizado(s).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 apply_metadata.py <partes_dir> [mapping.csv]")
        sys.exit(1)
    mapping = sys.argv[2] if len(sys.argv) > 2 else None
    apply_from_mapping(sys.argv[1], mapping)
