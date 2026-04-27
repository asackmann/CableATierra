# Análisis Deep Research del Repo y de Cada Track

Fecha del análisis: 2026-04-26

## Resumen ejecutivo

El repo está bien orientado como cuaderno de trabajo para batería, pero al contrastarlo con fuentes externas aparecen varios problemas de precisión:

- Hay al menos un error claro de atribución: `You Really Got Me` figura como tema de Bon Jovi, pero el original es de **The Kinks**.
- Hay inconsistencias internas de BPM en varios archivos: `Alta Suciedad -> Los Chicos`, `Arte Infernal` y `Sobrio a las Piñas`.
- `La Rubia` existe como archivo pero no está en `tracklist.md`; además, por letra, créditos y BPM, parece corresponder a **La Rubia Tarada** y no a un tema original llamado solo `La Rubia`.
- En los temas de `Justo Alegre` no encontré presencia pública sólida ni tablaturas de batería confiables; hoy dependen casi por completo de transcripción propia.
- En general, el repo mezcla links de búsqueda genéricos con notas internas. Conviene pasar a referencias estables por track.

## Hallazgos globales del repo

### 1. Error de artista original

- `tracklist.md:15` y `canciones/you-really-got-me.md:1` atribuyen `You Really Got Me` a `Bon Jovi`.
- La canción original es de **The Kinks** (single de 1964). Si la banda toca una versión influida por Bon Jovi, Van Halen u otra, conviene aclararlo como `versión de ... / original de The Kinks`.

### 2. Inconsistencias de BPM dentro de los mismos archivos

- `canciones/alta-suciedad-los-chicos.md:7` indica `106 -> 135`, pero en `:32` dice `Transición a 116` y en `:40` habla de `124 -> 116`.
- `canciones/arte-infernal.md:7` y la estructura usan `135`, pero en `:55` la nota de transcripción dice `Tempo ~95 muy importante`.
- `canciones/sobrio-a-las-pinias.md:7` dice `~92 / 118 vivo`, mientras toda la estructura en `:20-25` está armada a `116`.

### 3. Canción huérfana / posible problema de naming

- `canciones/la-rubia.md` existe, pero no aparece en `tracklist.md`.
- Las letras y créditos públicos apuntan a **La Rubia Tarada**; además los BPM públicos rondan ~122-123, no 148.
- Si ese archivo corresponde a la versión en vivo de Divididos del tema de Sumo, conviene renombrarlo y ajustar artista original / versión.

### 4. Calidad desigual de referencias

- Algunos tracks tienen solo links a búsquedas de YouTube.
- Otros ya tienen tablaturas concretas disponibles en Songsterr.
- Para ensayo conviene priorizar: tema oficial + tab de batería + una versión en vivo de referencia.

## Evaluación por track

| Track | Validación externa | Evaluación del archivo actual | Tablatura de batería |
|---|---|---|---|
| Alta Suciedad -> Los Chicos | `Alta suciedad` aparece pública a **106-107 BPM** y `Los chicos` a **135 BPM** | BPM general bien orientado, pero el archivo tiene contradicciones internas (`106 -> 135` vs `116` y `124 -> 116`) | Sí: `Alta suciedad Drum Tab` en Songsterr. No encontré una tab clara del medley completo |
| Blues del Ataúd | No encontré presencia pública sólida del track ni metadata confiable | El archivo sirve como nota interna, pero hoy no pude validar BPM, duración ni estructura contra fuentes externas | No encontré tab pública confiable |
| Honky Tonk Women | Coincide con el original de The Rolling Stones; BPM repo (~120) razonable | Archivo consistente. Buen enfoque de feel laid back | Sí: Songsterr tiene tabs concretas para batería |
| Nadie es Perfecto | Coincide con el tema oficial; encontré referencia pública a ~159 BPM | Repo marca `~162`; está cerca y es utilizable, aunque quizá convenga normalizarlo a 159-160 | Sí: Songsterr tiene tab de batería |
| Pride and Joy | Coincide con el original; referencia pública encontrada a **127 BPM** | El repo lo pone en `~120`; no está lejísimos para shuffle de ensayo, pero queda subestimado | Sí: Songsterr tiene varias tabs de batería, incluida la versión principal |
| Blunders Paradise | No encontré presencia pública sólida del track ni metadata confiable | El archivo hoy no se puede validar externamente; queda como transcripción interna | No encontré tab pública confiable |
| You Really Got Me | Original confirmado de **The Kinks**; el repo lo atribuye mal | Error claro de artista original. Si la referencia real es otra versión, hay que explicitarla | Sí: Songsterr tiene tab de batería de The Kinks |
| Arte Infernal | Coincide con el tema oficial de La Renga; referencia pública encontrada a **134 BPM** | El valor `135` está bien, pero la nota final que habla de `~95` se contradice y parece incorrecta | No encontré tab pública de batería confiable; sí hay tabs de guitarra y acordes |
| Born To Be Wild | Coincide con Steppenwolf; referencias públicas encontradas a **145-146 BPM** | Archivo consistente y bien calibrado | Sí: Songsterr tiene tab de batería |
| Sobrio a las Piñas | Coincide con Divididos; referencias públicas a **116 BPM** estudio y **125 BPM** en vivo | El cuerpo del archivo está alineado a 116, pero el encabezado `~92 / 118 vivo` no coincide | Sí: Songsterr tiene tab de batería; además apareció una transcripción textual en Cifras |
| La Rubia | Lo público apunta a **La Rubia Tarada**; Divididos la toca en vivo alrededor de **123 BPM** y el original de Sumo ronda **122 BPM** | El archivo parece mal nombrado o mal identificado. `148 BPM` no coincide con lo encontrado | Sí, pero con advertencia: hay tabs en Songsterr para `La Rubia Tarada`, varias marcadas como AI |

## Detalle por track

### Alta Suciedad -> Los Chicos

- Lo externo respalda bien la idea general del medley: `Alta suciedad` ~106/107 BPM y `Los chicos` 135 BPM.
- El problema está en la coherencia interna del archivo:
  - `canciones/alta-suciedad-los-chicos.md:7` dice `106 -> 135`
  - `:32` dice `Transición a 116`
  - `:40` dice `124 -> 116`
- Recomendación: unificar todo a una sola lógica de tempo. Si el medley real en ensayo está modificado, anotar explícitamente `versión de banda`.

Tab batería:

- Songsterr: [Alta suciedad Drum Tab](https://www.songsterr.com/a/wsa/andres-calamaro-alta-suciedad-drum-tab-s646139)

### Blues del Ataúd

- No encontré resultados públicos útiles que me permitan validar artista, BPM o tablatura.
- Puede ser material propio, material muy local o una grabación no indexada.

Recomendación:

- Si existe demo/drive/audio privado, este tema necesita una referencia interna propia más fuerte: BPM real, duración exacta, conteo de compases y un groove escrito.

### Honky Tonk Women

- La identificación del track es correcta.
- El BPM del repo (`~120`) es razonable para el feel del tema.
- Es uno de los archivos más sanos del repo.

Tabs batería:

- Songsterr: [Honky Tonk Women Drum Tab](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s52278)
- Songsterr alternativa: [Honky Tonk Women Drum Tab](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s242080)

### Nadie es Perfecto

- El track y el artista están bien.
- Encontré una referencia pública que lo sitúa cerca de **159 BPM**; el repo usa `~162`, que puede servir perfectamente en contexto de ensayo.
- No encontré una inconsistencia grave dentro del archivo.

Tab batería:

- Songsterr: [Nadie es Perfecto Drum Tab](https://www.songsterr.com/a/wsa/patricio-rey-y-sus-redonditos-de-ricota-nadie-es-perfecto-drum-tab-s1331648)

### Pride and Joy

- El track está bien identificado.
- La referencia pública encontrada lo sitúa en **127 BPM**, así que el `~120` del repo queda un poco corto.
- Como es shuffle, la diferencia puede sentirse bastante.

Tabs batería:

- Songsterr: [Pride And Joy Drum Tab](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-double-trouble-pride-and-joy-drum-tab-s240)
- Songsterr en vivo: [Pride and Joy (Live Alive) Drum Tab](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-pride-and-joy-live-alive-drum-tab-s1039981)

### Blunders Paradise

- No encontré validación pública suficiente del tema ni tab de batería usable.
- Hoy lo trataría como material no verificable externamente.

Recomendación:

- Igual que con `Blues del Ataúd`, conviene agregar una referencia interna más cerrada y quizás un audio base.

### You Really Got Me

- Este es el error más claro del repo.
- El original es **The Kinks**, no Bon Jovi.
- Si la versión que están montando se parece más a otra interpretación, habría que escribirlo así:
  - `Original: The Kinks`
  - `Versión de referencia: ...`

Tab batería:

- Songsterr: [You Really Got Me Drum Tab](https://www.songsterr.com/a/wsa/kinks-you-really-got-me-drum-tab-s10803)

### Arte Infernal

- La identificación del tema y artista es correcta.
- La referencia pública encontrada marca **134 BPM**, así que `135` está bien.
- El error está en la nota final:
  - `canciones/arte-infernal.md:55` dice `Tempo ~95 muy importante`
- Esa línea contradice tanto el archivo como la referencia externa.

Recomendación:

- Corregir la nota final para que quede alineada con 134/135 BPM.

### Born To Be Wild

- Muy bien calibrado.
- Las referencias públicas encontradas lo ubican en **145-146 BPM**, clavado con el repo.
- No vi errores relevantes.

Tab batería:

- Songsterr: [Born To Be Wild Drum Tab](https://www.songsterr.com/a/wsa/steppenwolf-born-to-be-wild-drum-tab-s244)

### Sobrio a las Piñas

- La referencia pública del estudio encontrada marca **116 BPM**.
- También apareció una referencia en vivo cerca de **125 BPM**.
- Eso hace que el cuerpo del archivo esté razonablemente bien, pero el encabezado actual no:
  - `canciones/sobrio-a-las-pinias.md:7` dice `~92 / 118 vivo`
  - `:20-25` desarrolla todo el tema a `116`

Tabs batería:

- Songsterr: [Sobrio a las piñas (drums) Drum Tab](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-drums-drum-tab-s928213)
- Songsterr estudio: [Sobrio a las Piñas (Versión Estudio) Drum Tab](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-version-estudio-drum-tab-s1811672)
- Transcripción textual: [CIFRAS - Sobrio A Las Piñas](https://www.cifras.com.br/cifra/divididos/sobrio-a-las-pinas)

### La Rubia

- Este archivo necesita revisión fuerte.
- Lo encontrado públicamente indica que el tema real es **La Rubia Tarada**:
  - versión original de Sumo ~122 BPM
  - versión en vivo de Divididos ~123 BPM
- El repo lo pone en `148 BPM`, y el naming queda ambiguo.

Recomendación:

- Confirmar si el tema es:
  - `La Rubia Tarada` de Sumo, versionada por Divididos
  - o una variante/arreglo interno distinto
- Si es la primera opción, conviene renombrar archivo y corregir BPM.

Tabs batería:

- Songsterr Divididos: [La Rubia Tarada Drum Tab](https://www.songsterr.com/a/wsa/divididos-la-rubia-tarada-drum-tab-s4343797)
- Songsterr Sumo: [La Rubia Tarada Drum Tab](https://www.songsterr.com/a/wsa/sumo-la-rubia-tarada-drum-tab-s686665)

## Prioridad de correcciones sugerida

1. Corregir artista original de `You Really Got Me`.
2. Unificar BPM de `Alta Suciedad -> Los Chicos`.
3. Corregir contradicción de BPM en `Arte Infernal`.
4. Unificar encabezado y estructura de `Sobrio a las Piñas`.
5. Decidir si `La Rubia` debe renombrarse a `La Rubia Tarada` y si entra o no al `tracklist.md`.
6. Reforzar con referencias internas los temas de `Justo Alegre`, porque hoy no tienen validación pública clara.

## Fuentes usadas

- The Kinks - `You Really Got Me`: [Wikipedia](https://en.wikipedia.org/wiki/You_Really_Got_Me)
- The Kinks - tab de batería: [Songsterr](https://www.songsterr.com/a/wsa/kinks-you-really-got-me-drum-tab-s10803)
- Andrés Calamaro - `Alta suciedad` BPM: [SongBPM](https://songbpm.com/%40andres-calamaro/alta-suciedad)
- Andrés Calamaro - `Los chicos` BPM: [SongBPM](https://songbpm.com/%40andres-calamaro/los-chicos-e3db4e45-9797-4077-a257-23a6ae3ef10b)
- Andrés Calamaro - tab de batería `Alta suciedad`: [Songsterr](https://www.songsterr.com/a/wsa/andres-calamaro-alta-suciedad-drum-tab-s646139)
- The Rolling Stones - tab de batería `Honky Tonk Women`: [Songsterr](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s52278)
- Patricio Rey y sus Redonditos de Ricota - `Nadie Es Perfecto` oficial: [YouTube](https://www.youtube.com/watch?v=nW32yMoHmok)
- Patricio Rey y sus Redonditos de Ricota - tab de batería `Nadie es Perfecto`: [Songsterr](https://www.songsterr.com/a/wsa/patricio-rey-y-sus-redonditos-de-ricota-nadie-es-perfecto-drum-tab-s1331648)
- Stevie Ray Vaughan - `Pride and Joy` BPM: [SongBPM](https://stg.songbpm.com/%40stevie-ray-vaughan/pride-and-joy)
- Stevie Ray Vaughan - tab de batería `Pride And Joy`: [Songsterr](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-double-trouble-pride-and-joy-drum-tab-s240)
- La Renga - `Arte Infernal` oficial: [YouTube](https://www.youtube.com/watch?v=3wAG0QnX1C0)
- La Renga - `Arte Infernal` BPM: [Shazam](https://www.shazam.com/song/1443620085/arte-infernal)
- Steppenwolf - `Born To Be Wild` BPM: [SongBPM](https://songbpm.com/%40steppenwolf/born-to-be-wild)
- Steppenwolf - tab de batería `Born To Be Wild`: [Songsterr](https://www.songsterr.com/a/wsa/steppenwolf-born-to-be-wild-drum-tab-s244)
- Divididos - `Sobrio A Las Piñas/Quien Se Tomó Todo El Vino` BPM: [SongBPM](https://songbpm.com/%40divididos/sobrio-a-las-pinas-quien-se-tomo-todo-el-vino)
- Divididos - tab de batería `Sobrio a las piñas`: [Songsterr](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-drums-drum-tab-s928213)
- Divididos - transcripción textual de batería `Sobrio a las Piñas`: [CIFRAS](https://www.cifras.com.br/cifra/divididos/sobrio-a-las-pinas)
- Sumo - `La Rubia Tarada` BPM: [SongBPM](https://songbpm.com/%40sumo/la-rubia-tarada)
- Divididos - `La Rubia Tarada (En Vivo)` BPM/créditos: [Shazam](https://www.shazam.com/song/1811628199/la-rubia-tarada)
- Divididos - tab de batería `La Rubia Tarada`: [Songsterr](https://www.songsterr.com/a/wsa/divididos-la-rubia-tarada-drum-tab-s4343797)
