# CableATierra — Backlog

## Separación de stems + Ableton + Mastering

**Idea:** usar Demucs para separar los 4 stems de cada parte de ensayo (batería, bajo, guitarra, voz) y a partir de eso:

1. **Armar proyecto Ableton automáticamente**
   - Crear un proyecto `.als` con 4 pistas de audio (Drums, Bass, Guitar, Vocals)
   - Cargar los stems correspondientes a cada pista
   - Sincronizar BPM detectado del ensayo
   - Un proyecto por ensayo, carpeta organizada por fecha

2. **Masterizar el ensayo**
   - Aplicar EQ + compresión básica por stem (preset por instrumento)
   - Balancear niveles automáticamente
   - Exportar mezcla final en WAV/MP3

3. **Posibles herramientas**
   - `demucs` → separación de stems (ya instalado para vocals/Whisper)
   - `python-ableton` o generación de `.als` vía XML → crear proyectos Ableton
   - `pydub` / `ffmpeg` → normalización y mezcla básica
   - `pyloudnorm` → loudness normalization (estándar LUFS)
   - Ableton MCP (ya disponible en el sistema) → cargar stems directamente en sesión abierta

4. **Flujo tentativo**
   ```
   Parte_XX.mp3
     → Demucs (4 stems)
       → drums.wav / bass.wav / guitar.wav / vocals.wav
         → Ableton project (.als) con 4 tracks
         → Mezcla automática + normalización
         → Export: Parte_XX_mastered.mp3
   ```

5. **Notas**
   - El modelo `htdemucs_ft` de Demucs es el mejor para calidad de separación
   - Para Ableton: el MCP de AbletonMCP ya está conectado, se puede explorar
   - Considerar separar solo los temas "buenos" (ensayos donde el audio estuvo bien)
   - Potencial para crear "demo" de la banda con stems limpiados

---

## Mejora de audio — Declipping y procesamiento

**Problema observado:** en el ensayo 20260807 hay momentos donde la voz/audio se satura o "frita" (clipping digital — señal que supera 0dBFS).

**Objetivo:** pipeline de mejora automática de audio por parte, aplicable antes de armar el proyecto Ableton o exportar.

1. **Detección y corrección de clipping**
   - Detectar muestras saturadas (exactamente en ±1.0) con `scipy.signal`
   - Interpolación para reconstruir la onda original en picos cortos
   - El clipping sostenido (mucho tiempo seguido) es más difícil de recuperar

2. **Procesamiento por stem (post-Demucs)**
   - Vocals: compressor suave + de-esser para reducir harshness
   - Drums: transient shaper, gate para cortar ruido entre golpes
   - Bass/Guitar: EQ para limpiar frecuencias sucias

3. **Normalización final**
   - Loudness normalization a estándar LUFS (Spotify: -14 LUFS, referencia)
   - Limiter de seguridad para evitar clipping en el export

4. **Librerías a usar**
   - `pedalboard` (Spotify) → compressor, limiter, EQ, de-esser, noise gate, soporte VST3/AU
   - `noisereduce` → filtrado de ruido ambiental / hiss de fondo
   - `pyloudnorm` → normalización LUFS estándar broadcasting
   - `scipy.signal` → detección e interpolación de clipping (ya instalada)

5. **Flujo tentativo**
   ```
   Parte_XX.mp3
     → Detectar clipping (scipy)
     → Declipping / interpolación
     → Demucs (stems)
       → vocals: compressor + de-esser (pedalboard)
       → drums: gate + transient (pedalboard)
       → bass/guitar: EQ limpieza (pedalboard)
     → Mezcla + normalización LUFS (pyloudnorm)
     → Export: Parte_XX_mejorada.mp3
   ```

6. **Notas**
   - Probar primero en un fragmento del 20260807 para medir mejora real
   - `pedalboard` soporta cargar plugins VST3/AU — se podrían usar presets de Ableton
   - El gain staging en el ensayo es la causa raíz — hablar con quien graba

---

*Anotado: 2026-08-07*
