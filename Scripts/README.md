# CableATierra — Pipeline de ensayos

Scripts para procesar grabaciones de ensayo: split automático, fingerprinting y metadata ID3.

## Flujo

```
Samples/Imported/2026.XX.XX. nombre.mp3
        ↓ pipeline.py (diario)
YYYYMMDD. Ensayo - Partes/
  Parte_01.mp3
  Parte_05. Como un cuento.mp3   ← renombrado automáticamente (confianza OK)
  mapping.csv                     ← completar las MANUAL
  fingerprinting_results.md
  CableATierra_Ensayo.m3u
```

## Uso manual

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

## Completar metadata manual

1. Abrir `mapping.csv` en la carpeta de partes
2. Completar la columna `cancion` para las filas con confianza MANUAL
3. Correr: `python3 apply_metadata.py "/ruta/al/Ensayo - Partes/"`

## Configuración

`config.json` — ajustar umbrales de silencio, paths, artista, etc.

## Archivos

| Script | Función |
|--------|---------|
| `pipeline.py` | Orquestador principal |
| `split_ensayo.py` | División por silencios |
| `fingerprint.py` | Comparación por audio features |
| `apply_metadata.py` | Escribe ID3 tags desde mapping.csv |
| `config.json` | Configuración |
| `processed.json` | Log de archivos ya procesados (auto-generado) |
