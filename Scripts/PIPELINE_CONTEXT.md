# CableATierra — Contexto del pipeline automático

Este documento resume cómo Claude (vía tarea programada `cableatierra-pipeline`) ejecuta y monitorea el pipeline de ensayos. Sirve como referencia rápida de directorios, criterios y comportamiento.

## Cómo se ejecuta

El pipeline corre vía `osascript` (`do shell script`) para evitar el deadlock del filesystem que se da al tocar archivos de Dropbox desde el sandbox de Claude:

```bash
/usr/bin/python3 /Users/agustinsackmann/Repos/Personal/CableATierra/Scripts/pipeline.py > /tmp/cableatierra_pipeline.log 2>&1
```

⚠️ Usar siempre `/usr/bin/python3` explícito, **no** `python3` a secas. Dentro de `do shell script`, `PATH` resuelve `python3` a `/opt/homebrew/bin/python3`, que no tiene instalados `numpy`/`librosa`/`whisper` (sí los tiene `/usr/bin/python3`, el que se usó para armar `fingerprint_db.json`/`lyrics_db.json`). Si el log muestra `ModuleNotFoundError`, es este problema.

Luego se lee `/tmp/cableatierra_pipeline.log` para reportar el resultado.

## Directorios y archivos clave

| Qué | Path |
|---|---|
| **Carpeta única de entrada** (acá y sólo acá se dejan los ensayos nuevos) | `/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Musica/Jamming-Ensayos/2026. Cable a Tierra` |
| Carpeta de originales ya procesados (el pipeline mueve el .mp3 acá solo) | `.../Jamming-Ensayos/2026. Cable a Tierra/Procesados` |
| Carpeta de duplicados detectados (revisar y borrar a mano) | `.../Jamming-Ensayos/2026. Cable a Tierra/Duplicados` |
| Carpeta raíz del proyecto (salida de las partes spliteadas) | `/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Ableton/2026. Projects/CableATierra Project` |
| Carpeta de referencia para fingerprinting | `.../CableATierra Project/20260609. Ensayo - Partes` |
| Scripts del pipeline | `/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts/` |
| Orquestador principal | `Scripts/pipeline.py` |
| Configuración (paths, thresholds, artist, ffmpeg, whisper) | `Scripts/config.json` |
| Log de archivos ya procesados (auto-generado) | `Scripts/processed.json` |
| Base de fingerprints | `Scripts/fingerprint_db.json` |
| Log de la última corrida | `/tmp/cableatierra_pipeline.log` |

## Flujo (actualizado 2026-09-14)

1. Cualquier ensayo nuevo (ej. bajado de un mail de WeTransfer) se deja con nombre `YYYY.MM.DD. descripción.mp3` directamente en la carpeta única de entrada (Jamming-Ensayos).
2. `pipeline.py` lo detecta, lo splitea, fingerprintea/matchea letras, taggea, y al terminar **mueve el .mp3 original a `Procesados/`** dentro de esa misma carpeta — así la carpeta raíz siempre muestra sólo lo pendiente.
3. La salida (`Parte_XX.mp3`, `mapping.csv`, `fingerprinting_results.md`, playlist) se sigue generando dentro del proyecto de Ableton, en `YYYYMMDD. Ensayo - Partes/`.
4. Los duplicados detectados manualmente (por tamaño/MD5 idéntico) se mueven a `Duplicados/` — nunca se borran automáticamente, hay que revisarlos y borrarlos a mano.

⚠️ Antes de esta fecha el pipeline leía de `Ableton/.../Samples/Imported`, una carpeta distinta de donde en la práctica caían los ensayos (Jamming-Ensayos). Eso generaba copias duplicadas manuales y el original nunca se archivaba. Ya está unificado — no volver a usar `Samples/Imported` como entrada.

## Criterio para "archivo nuevo"

`pipeline.py` sólo actúa sobre archivos que cumplen:
- Nombre con fecha al inicio, formato `YYYY.MM.DD.*` (ej. `2026.09.14. ensayo.mp3`)
- Duración mayor a 30 minutos (1800 segundos)
- No estar ya registrado en `processed.json`

## Qué hace el pipeline cuando encuentra un ensayo nuevo

1. **Split**: divide el archivo por silencios (`silence_threshold_db: -35dB`, mínimo 8s de silencio, gap de zona 45s, duración mínima de sección 60s) en partes individuales.
2. **Fingerprinting**: compara cada parte contra la carpeta de referencia (`20260609. Ensayo - Partes`) usando audio features, con umbrales `fingerprint_gap_ok: 0.010` y `fingerprint_gap_media: 0.002`.
3. **Lyrics match**: para las partes que no obtienen confianza OK por fingerprint, corre transcripción (Whisper modelo `medium`, 180s desde el segundo 30) y compara letra contra una base de letras.
4. **Niveles de confianza** (de mayor a menor certeza): `DOBLE_OK` (fingerprint + lyrics coinciden) → `OK` (fingerprint) → `LYRICS_OK` (solo letra) → `MANUAL` (sin match automático, requiere completar a mano).
5. **Metadata**: aplica tags ID3 automáticamente a las partes con confianza alta.
6. **Salida**: crea una carpeta `YYYYMMDD. Ensayo - Partes/` con:
   - Partes renombradas (`Parte_01.mp3`, o con nombre de canción si hubo match)
   - `mapping.csv` — completar la columna `cancion` para las filas marcadas `MANUAL`
   - `fingerprinting_results.md`
   - Playlist `CableATierra_Ensayo.m3u`
7. **Archivado**: mueve el .mp3 original de la carpeta de entrada a `Procesados/`.

Para completar metadata manual: llenar `mapping.csv` y correr `python3 apply_metadata.py "/ruta/a/la/carpeta/Ensayo - Partes/"`.

## Troubleshooting

Si el pipeline falla, revisar:
- Que el archivo de Dropbox esté disponible offline (no solo "en la nube")
- Que la carpeta de referencia `20260609. Ensayo - Partes` siga accesible
- Que `Scripts/fingerprint_db.json` exista

## Uso manual (fuera del pipeline automático)

```bash
# Correr pipeline completo sobre archivos nuevos
python3 pipeline.py

# Forzar un archivo aunque ya esté procesado
python3 pipeline.py --force "2026.08.01. nombre.mp3"

# Solo split
python3 split_ensayo.py input.mp3 output_dir/ "Album Name"

# Solo aplicar metadata desde mapping.csv
python3 apply_metadata.py "/ruta/al/Ensayo - Partes/"

# Solo fingerprint
python3 fingerprint.py target_dir/ reference_dir/ output.json
```

---
*Generado automáticamente por Claude a partir de `Scripts/README.md`, `Scripts/config.json` y `Scripts/pipeline.py`.*
