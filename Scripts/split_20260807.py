#!/usr/bin/env python3
"""
split_20260807.py
Mapeo completo: 20 partes originales → 27 canciones
Ensayo 2026-08-07 - CableATierra
"""
import os
import subprocess

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FOLDER = "/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Ableton/2026. Projects/CableATierra Project/20260807. Ensayo - Partes"
ARTIST = "CableATierra"
ALBUM = "Ensayo 2026-08-07"


def ts(t):
    """MM:SS string to seconds (float)"""
    if t is None:
        return 0.0
    parts = str(t).split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(parts[0])


def process(src_n, dst_n, title, start=None, end=None):
    src = os.path.join(FOLDER, f"ORIG_Parte_{src_n:02d}.mp3")
    dst = os.path.join(FOLDER, f"Parte_{dst_n:02d}. {title}.mp3")

    if not os.path.exists(src):
        print(f"  MISSING: ORIG_Parte_{src_n:02d}.mp3")
        return False

    args = [FFMPEG, "-y"]

    start_s = ts(start)
    if start:
        args += ["-ss", str(start_s)]

    args += ["-i", src]

    if end:
        duration = ts(end) - start_s
        args += ["-t", str(duration)]

    args += [
        "-c:a", "copy",
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={ARTIST}",
        "-metadata", f"album={ALBUM}",
        "-metadata", f"track={dst_n}",
        dst
    ]

    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: Parte_{dst_n:02d}. {title}.mp3")
        print(result.stderr[-300:])
        return False
    else:
        print(f"  OK: Parte_{dst_n:02d}. {title}.mp3")
        return True


# ─── Step 1: Renombrar originales a ORIG_Parte_XX.mp3 ───────────────────────
print("=== Step 1: Renombrando originales ===")
for n in range(1, 21):
    orig = os.path.join(FOLDER, f"Parte_{n:02d}.mp3")
    new  = os.path.join(FOLDER, f"ORIG_Parte_{n:02d}.mp3")
    if os.path.exists(orig):
        os.rename(orig, new)
        print(f"  Parte_{n:02d}.mp3 → ORIG")
    elif os.path.exists(new):
        print(f"  Parte_{n:02d} ya renombrado")
    else:
        print(f"  MISSING: Parte_{n:02d}.mp3")

# ─── Step 2: Procesar todos los partes ──────────────────────────────────────
print("\n=== Step 2: Procesando ===")

# Parte_01 → 01. El Viejo (rename completo)
process(1,  1,  "El Viejo")

# Parte_02 → 02. Tema del Cuti Nuevo (rename completo)
process(2,  2,  "Tema del Cuti Nuevo")

# Parte_03 → 03. Cuando Estes Aca (desde 4:20)
process(3,  3,  "Cuando Estes Aca", start="4:20")

# Parte_04 → 04. Arte Infernal (3:00–11:00) + 05. Alta Suciedad (11:00–fin)
process(4,  4,  "Arte Infernal",  start="3:00", end="11:00")
process(4,  5,  "Alta Suciedad",  start="11:00")

# Parte_05 → 06. Blonders Paradise (rename completo)
process(5,  6,  "Blonders Paradise")

# Parte_06 → 07. El Viejo (5:00–10:15) + 08. Los Chicos (12:29–fin)
process(6,  7,  "El Viejo",       start="5:00",  end="10:15")
process(6,  8,  "Los Chicos",     start="12:29")

# Parte_07 → 09. Alta Suciedad (desde 0:30)
process(7,  9,  "Alta Suciedad",  start="0:30")

# Parte_08 → 5 canciones
process(8,  10, "Tema del Cuti Nuevo",    start="1:00",  end="7:40")
process(8,  11, "Arte Infernal",          start="8:55",  end="12:40")
process(8,  12, "Cuando Estes Aca",       start="12:40", end="20:44")
process(8,  13, "Pride and Joy",          start="23:00", end="26:37")
process(8,  14, "You Really Got Me Now",  start="26:37")

# Parte_09 → 15. Los Chicos (desde 0:13)
process(9,  15, "Los Chicos",     start="0:13")

# Parte_10 → 16. Alta Suciedad (hasta 4:25)
process(10, 16, "Alta Suciedad",  end="4:25")

# Parte_11 → 17. Blonders Paradise (desde 1:10)
process(11, 17, "Blonders Paradise", start="1:10")

# Parte_12 → 18. Blues del Ataud (hasta 2:46)
process(12, 18, "Blues del Ataud", end="2:46")

# Parte_13 → 19. El Viejo (rename completo)
process(13, 19, "El Viejo")

# Parte_14 → 20. Los Chicos (rename completo)
process(14, 20, "Los Chicos")

# Parte_15 → 21. Alta Suciedad (hasta 4:39)
process(15, 21, "Alta Suciedad",  end="4:39")

# Parte_16 → 22. Tema del Cuti Nuevo (rename completo)
process(16, 22, "Tema del Cuti Nuevo")

# Parte_17 → 23. Arte Infernal (desde 0:42)
process(17, 23, "Arte Infernal",  start="0:42")

# Parte_18 → 24. Cuando Estes Aca (rename completo)
process(18, 24, "Cuando Estes Aca")

# Parte_19 → 25. Cuando Estes Aca (rename completo)
process(19, 25, "Cuando Estes Aca")

# Parte_20 → 26. Pride and Joy (0:35–3:50) + 27. You Really Got Me Now (3:50–fin)
process(20, 26, "Pride and Joy",          start="0:35", end="3:50")
process(20, 27, "You Really Got Me Now",  start="3:50")

# ─── Step 3: Eliminar archivos ORIG ─────────────────────────────────────────
print("\n=== Step 3: Limpiando originales ===")
for n in range(1, 21):
    orig = os.path.join(FOLDER, f"ORIG_Parte_{n:02d}.mp3")
    if os.path.exists(orig):
        os.remove(orig)
        print(f"  Deleted ORIG_Parte_{n:02d}.mp3")

print("\n=== Listo: 20 partes → 27 canciones ===")
