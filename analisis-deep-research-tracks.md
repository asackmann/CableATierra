# Análisis Deep Research del Repo y de Cada Track

Fecha del análisis ajustado: 2026-04-26

## Resumen ejecutivo

Revisé nuevamente el repo después de tus cambios. El análisis anterior quedó desactualizado en varios puntos y ahora la situación cambió bastante:

- `You Really Got Me` ya no aparece como tema mal atribuido: ahora el repo usa `You Really Got Me Now`, que sí corresponde a **Jon Bon Jovi / Bon Jovi**.
- `Alta Suciedad -> Los Chicos` quedó internamente consistente en el repo.
- `La Rubia` ya no forma parte del estado actual del repo, así que esa observación deja de aplicar.
- Los problemas que siguen realmente vigentes son pocos y concretos:
  - una contradicción fuerte en `Arte Infernal`
  - una posible diferencia entre la referencia externa y la versión de banda en `Sobrio a las Piñas`
  - ausencia de material público confiable para los temas de `Justo Alegre`

## Estado actual del repo

### Ajustes que ya quedaron resueltos

- `tracklist.md` y `canciones/you-really-got-me-now.md` ahora están alineados con `You Really Got Me Now`.
- `canciones/alta-suciedad-los-chicos.md` ya no tiene las contradicciones internas de BPM que aparecían antes.
- No encontré `canciones/la-rubia.md` en el estado actual del árbol, así que quité esa parte del análisis.

### Problemas que siguen abiertos

- `canciones/arte-infernal.md` sigue mezclando un track a `135 BPM` con una nota final que habla de `~95`.
- `canciones/sobrio-a-las-pinias.md` ahora es consistente a `120`, pero externamente las referencias más claras siguen marcando `116 BPM` para estudio y `125 BPM` para vivo. No lo llamaría error directo, pero sí una decisión que conviene documentar mejor.
- `Blues del Ataúd` y `Blunders Paradise` siguen sin validación pública sólida ni tabs de batería confiables.

## Evaluación por track

| Track | Validación externa | Evaluación del archivo actual | Tablatura de batería |
|---|---|---|---|
| Alta Suciedad -> Los Chicos | `Alta suciedad` aparece pública a **106-107 BPM** y `Los chicos` a **135 BPM** | Ahora está consistente y bien alineado con la idea del medley | Sí: `Alta suciedad Drum Tab` en Songsterr. No encontré una tab clara del medley completo |
| Blues del Ataúd | No encontré presencia pública sólida del track ni metadata confiable | Sigue siendo material útil como nota interna, pero no validable externamente hoy | No encontré tab pública confiable |
| Honky Tonk Women | Coincide con el original de The Rolling Stones; BPM repo (~120) razonable | Archivo consistente. Buen enfoque de feel laid back | Sí: Songsterr tiene tabs concretas para batería |
| Nadie es Perfecto | Coincide con el tema oficial; encontré referencia pública a ~159 BPM | `~162` sigue siendo razonable para ensayo | Sí: Songsterr tiene tab de batería |
| Pride and Joy | Coincide con el original; referencia pública encontrada a **127 BPM** | El repo lo sigue poniendo en `~120`; no es grave, pero queda algo corto frente a la referencia | Sí: Songsterr tiene varias tabs de batería |
| Blunders Paradise | No encontré presencia pública sólida del track ni metadata confiable | Sigue como transcripción interna no verificable externamente | No encontré tab pública confiable |
| You Really Got Me Now | Coincide con el tema de **Jon Bon Jovi**; encontré referencias públicas a **110-111 BPM** | Cambio correcto. El repo ahora está bien encaminado en nombre, artista y BPM | No encontré una tab pública clara de batería específica para este tema exacto |
| Arte Infernal | Coincide con el tema oficial de La Renga; referencia pública encontrada a **134 BPM** | El valor `135` está bien, pero la nota final que habla de `~95` sigue pareciendo incorrecta | No encontré tab pública de batería confiable; sí hay tabs de guitarra y acordes |
| Born To Be Wild | Coincide con Steppenwolf; referencias públicas encontradas a **145-146 BPM** | Archivo consistente y bien calibrado | Sí: Songsterr tiene tab de batería |
| Sobrio a las Piñas | Coincide con Divididos; referencias públicas a **116 BPM** estudio y **125 BPM** en vivo | El repo ahora es consistente a `120`, que funciona como promedio/intermedio, pero convendría aclarar si es `versión banda` | Sí: Songsterr tiene tab de batería; además apareció una transcripción textual en Cifras |

## Detalle por track

### Alta Suciedad -> Los Chicos

- Lo externo sigue respaldando bien la lógica del medley:
  - `Alta suciedad` ~106/107 BPM
  - `Los chicos` ~135 BPM
- A diferencia de la revisión anterior, el archivo actual ya está coherente:
  - `canciones/alta-suciedad-los-chicos.md:7` dice `106 -> 135`
  - `:23` mantiene `106 -> 135`
  - `:32` dice `Transición a 135`
  - `:40` dice `transición 106 -> 135`

Conclusión:

- Este punto ya no lo marcaría como error.

Tab batería:

- Songsterr: [Alta suciedad Drum Tab](https://www.songsterr.com/a/wsa/andres-calamaro-alta-suciedad-drum-tab-s646139)

### Blues del Ataúd

- No encontré resultados públicos útiles que permitan validar artista, BPM o tablatura.
- Lo trataría como material de trabajo interno de la banda.

Recomendación:

- Si existe audio propio, demo o grabación de ensayo, conviene referenciarlo dentro del repo.

### Honky Tonk Women

- Sin cambios respecto al análisis anterior.
- La identificación del track es correcta.
- El BPM del repo (`~120`) sigue siendo razonable.

Tabs batería:

- Songsterr: [Honky Tonk Women Drum Tab](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s52278)
- Songsterr alternativa: [Honky Tonk Women Drum Tab](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s242080)

### Nadie es Perfecto

- Sigue bien identificado.
- La referencia pública encontrada lo ubica cerca de **159 BPM**.
- `~162` no me parece un problema real.

Tab batería:

- Songsterr: [Nadie es Perfecto Drum Tab](https://www.songsterr.com/a/wsa/patricio-rey-y-sus-redonditos-de-ricota-nadie-es-perfecto-drum-tab-s1331648)

### Pride and Joy

- Sigue siendo válido.
- La referencia pública encontrada lo sitúa en **127 BPM**.
- El repo sigue usando `~120`, así que lo dejaría marcado como diferencia menor, no como error duro.

Tabs batería:

- Songsterr: [Pride And Joy Drum Tab](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-double-trouble-pride-and-joy-drum-tab-s240)
- Songsterr en vivo: [Pride and Joy (Live Alive) Drum Tab](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-pride-and-joy-live-alive-drum-tab-s1039981)

### Blunders Paradise

- Igual que `Blues del Ataúd`, no encontré validación pública suficiente del tema ni tab de batería usable.

Recomendación:

- Mantenerlo como transcripción interna y, si existe, sumar una fuente privada o audio base.

### You Really Got Me Now

- Este punto cambió por completo respecto a la revisión anterior.
- Ahora sí encontré coincidencia externa con el tema de **Jon Bon Jovi**:
  - referencia pública a **111 BPM**
  - otra referencia pública a **110 BPM**
- El repo usa `~110`, así que quedó razonablemente bien.

Observación menor:

- Las referencias dentro del archivo todavía usan búsquedas genéricas de `You Really Got Me`, no `You Really Got Me Now`.
- No es un error musical, pero sí una referencia mejorable.

Referencias externas:

- SongBPM: [You Really Got Me Now](https://songbpm.com/%40jon-bon-jovi/you-really-got-me-now)
- Shazam: [You Really Got Me Now](https://www.shazam.com/song/1440658020/you-really-got-me-now)
- YouTube oficial: [You Really Got Me Now](https://www.youtube.com/watch?v=Fxhhbn9Mvs8)

### Arte Infernal

- Sigue siendo el hallazgo más claro y vigente.
- La referencia pública encontrada marca **134 BPM**, así que `135` está bien.
- Pero el archivo todavía dice:
  - `canciones/arte-infernal.md:55` `Tempo ~95 muy importante`

Conclusión:

- Esta línea sigue contradiciendo tanto el resto del archivo como la referencia externa.
- Este sí sigue siendo un error real dentro del repo.

### Born To Be Wild

- Sin cambios: muy bien calibrado.
- Las referencias públicas siguen ubicándolo en **145-146 BPM**, alineado con el repo.

Tab batería:

- Songsterr: [Born To Be Wild Drum Tab](https://www.songsterr.com/a/wsa/steppenwolf-born-to-be-wild-drum-tab-s244)

### Sobrio a las Piñas

- El archivo ahora es internamente consistente:
  - `tracklist.md:18` usa `~120`
  - `canciones/sobrio-a-las-pinias.md:7` usa `120 vivo`
  - `:20-25` desarrolla toda la estructura a `120`
- Externamente, las mejores referencias que encontré siguen siendo:
  - estudio: **116 BPM**
  - vivo: **125 BPM**

Conclusión:

- Ya no lo marcaría como contradicción interna.
- Lo marcaría como una decisión de versión:
  - `120` funciona como punto medio práctico
  - convendría explicitar que es tempo de la versión de banda o una referencia intermedia entre estudio y vivo

Observación menor:

- `canciones/sobrio-a-las-pinias.md:55` dice `cómo transiciona de 120`, y la frase quedó algo rara; parece que antes hablaba de un cambio más claro.

Tabs batería:

- Songsterr: [Sobrio a las piñas (drums) Drum Tab](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-drums-drum-tab-s928213)
- Songsterr estudio: [Sobrio a las Piñas (Versión Estudio) Drum Tab](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-version-estudio-drum-tab-s1811672)
- Transcripción textual: [CIFRAS - Sobrio A Las Piñas](https://www.cifras.com.br/cifra/divididos/sobrio-a-las-pinas)

## Prioridad de correcciones sugerida

1. Corregir la nota final de `canciones/arte-infernal.md` para alinearla con `134/135 BPM`.
2. Mejorar las referencias internas de `canciones/you-really-got-me-now.md` para que apunten al tema exacto y no a búsquedas genéricas.
3. Aclarar en `canciones/sobrio-a-las-pinias.md` si `120` es el tempo adoptado por la banda.
4. Reforzar con referencias internas o privadas los temas de `Justo Alegre`, porque siguen sin validación pública clara.

## Fuentes usadas

- Andrés Calamaro - `Alta suciedad` BPM: [SongBPM](https://songbpm.com/%40andres-calamaro/alta-suciedad)
- Andrés Calamaro - `Los chicos` BPM: [SongBPM](https://songbpm.com/%40andres-calamaro/los-chicos-e3db4e45-9797-4077-a257-23a6ae3ef10b)
- Andrés Calamaro - tab de batería `Alta suciedad`: [Songsterr](https://www.songsterr.com/a/wsa/andres-calamaro-alta-suciedad-drum-tab-s646139)
- The Rolling Stones - tab de batería `Honky Tonk Women`: [Songsterr](https://www.songsterr.com/a/wsa/rolling-stones-honky-tonk-women-drum-tab-s52278)
- Patricio Rey y sus Redonditos de Ricota - `Nadie Es Perfecto` oficial: [YouTube](https://www.youtube.com/watch?v=nW32yMoHmok)
- Patricio Rey y sus Redonditos de Ricota - tab de batería `Nadie es Perfecto`: [Songsterr](https://www.songsterr.com/a/wsa/patricio-rey-y-sus-redonditos-de-ricota-nadie-es-perfecto-drum-tab-s1331648)
- Stevie Ray Vaughan - `Pride and Joy` BPM: [SongBPM](https://stg.songbpm.com/%40stevie-ray-vaughan/pride-and-joy)
- Stevie Ray Vaughan - tab de batería `Pride And Joy`: [Songsterr](https://www.songsterr.com/a/wsa/stevie-ray-vaughan-double-trouble-pride-and-joy-drum-tab-s240)
- Jon Bon Jovi - `You Really Got Me Now` BPM: [SongBPM](https://songbpm.com/%40jon-bon-jovi/you-really-got-me-now)
- Jon Bon Jovi - `You Really Got Me Now` créditos/BPM: [Shazam](https://www.shazam.com/song/1440658020/you-really-got-me-now)
- Jon Bon Jovi - `You Really Got Me Now` oficial: [YouTube](https://www.youtube.com/watch?v=Fxhhbn9Mvs8)
- La Renga - `Arte Infernal` oficial: [YouTube](https://www.youtube.com/watch?v=3wAG0QnX1C0)
- La Renga - `Arte Infernal` BPM: [Shazam](https://www.shazam.com/song/1443620085/arte-infernal)
- Steppenwolf - `Born To Be Wild` BPM: [SongBPM](https://songbpm.com/%40steppenwolf/born-to-be-wild)
- Steppenwolf - tab de batería `Born To Be Wild`: [Songsterr](https://www.songsterr.com/a/wsa/steppenwolf-born-to-be-wild-drum-tab-s244)
- Divididos - `Sobrio A Las Piñas/Quien Se Tomó Todo El Vino` BPM: [SongBPM](https://songbpm.com/%40divididos/sobrio-a-las-pinas-quien-se-tomo-todo-el-vino)
- Divididos - `Sobrio a las Piñas / ¿Quién Se Tomó Todo el Vino? - En Vivo` BPM: [SongBPM](https://songbpm.com/%40divididos/sobrio-a-las-pinas-quien-se-tomo-todo-el-vino---en-vivo)
- Divididos - tab de batería `Sobrio a las piñas`: [Songsterr](https://www.songsterr.com/a/wsa/divididos-sobrio-a-las-pinas-drums-drum-tab-s928213)
- Divididos - transcripción textual de batería `Sobrio a las Piñas`: [CIFRAS](https://www.cifras.com.br/cifra/divididos/sobrio-a-las-pinas)
