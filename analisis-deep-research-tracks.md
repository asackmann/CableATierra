# Análisis Deep Research del Repo y de Cada Track

Fecha del análisis ajustado: 2026-04-27

## Resumen ejecutivo

Revisé nuevamente el repo después de los últimos cambios. El estado general mejoró bastante:

- `You Really Got Me Now` sigue bien encaminado como track de Bon Jovi.
- `Alta Suciedad -> Los Chicos` sigue consistente.
- `Arte Infernal` ya no tiene la contradicción más fuerte de BPM: ahora la nota final quedó alineada con `~135`.
- La mejora más visible del repo es que ahora varios temas incluyen tablaturas embebidas en formato similar al template, con links e imágenes.

Los puntos que hoy sí merecen ajuste ya no son tanto de metadata musical sino de consistencia editorial y calidad de las tablaturas cargadas:

- algunas imágenes de tablatura están bien asociadas al track
- otras quedaron apuntando a una imagen equivocada
- en algunos temas el patrón escrito debajo de la imagen parece demasiado genérico o incluso idéntico entre secciones donde debería variar
- `Justo Alegre` sigue sin validación pública confiable

## Estado actual del repo

### Ajustes que ya quedaron resueltos

- `canciones/08-arte-infernal.md` ya no dice `~95`; ahora la nota final quedó alineada con `~135`.
- `canciones/01-alta-suciedad-los-chicos.md` sigue consistente con la transición `106 -> 135`.
- `tracklist.md` y `canciones/07-you-really-got-me-now.md` siguen alineados.

### Problemas que siguen abiertos

- `canciones/05-pride-and-joy.md` muestra una imagen equivocada: referencia `tab-honky-tonk-women.png` en vez de `tab-pride-and-joy.png`.
- `canciones/10-sobrio-a-las-pinias.md` quedó consistente a `120`, pero todavía convendría documentar si ese valor es `versión banda`.
- `canciones/03-honky-tonk-women.md` tiene una tablatura escrita más ambiciosa, pero la línea de caja/bombo del groove base quedó difícil de leer y no mantiene el mismo nivel de claridad que el resto del repo.
- `canciones/10-sobrio-a-las-pinias.md` usa tres grooves prácticamente idénticos, lo que hace que la sección aporte menos información de la que podría.
- `Blues del Ataúd` y `Blunders Paradise` siguen sin validación pública sólida ni tabs externas confiables.

## Evaluación por track

| Track | Validación externa | Estado actual del archivo | Tablatura de batería |
|---|---|---|---|
| Alta Suciedad -> Los Chicos | `Alta suciedad` pública a **106-107 BPM** y `Los chicos` a **135 BPM** | Bien alineado y además ahora tiene tab embebida + patrón escrito | Sí: Songsterr + imagen local |
| Blues del Ataúd | Sin presencia pública sólida encontrada | Sigue siendo una nota interna útil; groove agregado correctamente | No encontré tab pública confiable |
| Honky Tonk Women | Correcto respecto al original y BPM razonable | Mejoró con imagen embebida, pero el groove base quedó más confuso de leer que en otros temas | Sí: Songsterr + imagen local |
| Nadie es Perfecto | Coincide con el tema oficial; `~162` sigue razonable | Archivo sano; groove escrito claro | Sí: Songsterr en análisis previo |
| Pride and Joy | Coincide con el original; referencia pública cercana a **127 BPM** | Tiene tab embebida, pero la imagen referenciada hoy es la equivocada | Sí: Songsterr + imagen local mal referenciada |
| Blunders Paradise | Sin validación pública sólida | Sigue como transcripción interna; groove útil | No encontré tab pública confiable |
| You Really Got Me Now | Coincide con Bon Jovi; **110-111 BPM** encontrado externamente | Bien encaminado en nombre, artista y groove escrito | No encontré tab pública clara específica embebida |
| Arte Infernal | Coincide con La Renga; referencia externa cerca de **134 BPM** | Punto corregido: ya no veo contradicción fuerte de BPM | No encontré tab pública de batería confiable |
| Born To Be Wild | Coincide con Steppenwolf; **145-146 BPM** | Muy bien resuelto; imagen y groove escrito están alineados | Sí: Songsterr + imagen local |
| Sobrio a las Piñas | Coincide con Divididos; referencias públicas a **116 estudio / 125 vivo** | Internamente consistente a `120`, pero los tres grooves escritos están casi calcados | Sí: Songsterr + imagen local |

## Hallazgos principales

### 1. `Arte Infernal` quedó corregido

En la revisión anterior este era el error más claro del repo. Ahora ya no lo es.

- `canciones/08-arte-infernal.md:55` pasó a `Tempo ~135 muy importante`
- Eso ya está alineado con el BPM del archivo y con la referencia externa

Conclusión:

- Este punto debe salir de la lista de errores.

### 2. `Pride and Joy` tiene una referencia de imagen equivocada

Este es hoy el problema más claro dentro de las nuevas tablaturas embebidas.

- `canciones/05-pride-and-joy.md:40-41` referencia Songsterr de `Pride and Joy`
- pero la imagen insertada es `tab-honky-tonk-women.png`
- en la carpeta sí existe `canciones/tab-pride-and-joy.png`

Conclusión:

- No es un problema musical del track, pero sí un error concreto del repo.

### 3. `Sobrio a las Piñas` está más prolijo, pero la sección de grooves aporta poco diferencial

Ahora el archivo está mucho más consistente que antes:

- `tracklist.md:18` usa `~120`
- `canciones/10-sobrio-a-las-pinias.md:7` usa `120 vivo`
- la estructura desarrolla todo a `120`

Eso ya no es una contradicción.

Lo que sí veo ahora:

- `Groove base`, `Puente con silencios` y `Final abierto` en `canciones/10-sobrio-a-las-pinias.md:42-63` usan prácticamente el mismo patrón escrito
- cambia la descripción, pero casi no cambia la tablatura

Conclusión:

- Conviene diferenciar más las tres secciones o dejar menos secciones pero más precisas.

### 4. `Honky Tonk Women` ganó una tab embebida, pero quedó menos legible que el resto

- `canciones/03-honky-tonk-women.md:44-50` tiene una notación más larga para caja y bombo
- comparado con el resto del repo, esa tablatura quedó menos clara visualmente
- además el `CB` del groove base figura vacío en la línea escrita, aunque la descripción menciona que el cowbell ayuda a sostener el feel

Conclusión:

- No lo marcaría como error duro, pero sí como sección mejorable.

### 5. Las nuevas tablaturas embebidas mejoran mucho el repo

Esto sí vale remarcarlo porque cambia la calidad general del material:

- [tab-alta-suciedad-los-chicos.png](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/tab-alta-suciedad-los-chicos.png)
- [tab-born-to-be-wild.png](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/tab-born-to-be-wild.png)
- [tab-honky-tonk-women.png](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/tab-honky-tonk-women.png)
- [tab-pride-and-joy.png](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/tab-pride-and-joy.png)
- [tab-sobrio-a-las-pinias.png](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/tab-sobrio-a-las-pinias.png)

Conclusión:

- El repo pasó de ser solo textual a tener apoyo visual real para varios temas.

## Detalle por track

### Alta Suciedad -> Los Chicos

- Sigue bien resuelto.
- La transición `106 -> 135` está consistente.
- Ahora además tiene imagen local y groove escrito útil.

No lo marcaría como problema.

### Blues del Ataúd

- Sigue sin validación pública sólida.
- El groove agregado está bien como guía de ensayo.

Recomendación:

- Si existe demo o grabación privada, conviene sumarla como referencia interna.

### Honky Tonk Women

- El tema está bien identificado y la imagen local existe.
- La integración visual suma.
- El punto flojo es la lectura del groove base, que quedó menos clara que en los demás archivos.

### Nadie es Perfecto

- Archivo estable y consistente.
- El groove escrito es simple y utilizable.

No veo errores relevantes nuevos.

### Pride and Joy

- El archivo sigue bien como contenido musical.
- El error concreto está en la imagen:
  - referencia `tab-honky-tonk-women.png`
  - debería ser `tab-pride-and-joy.png`

Ese es hoy uno de los ajustes más claros para hacer.

### Blunders Paradise

- Sigue siendo track no verificable externamente con lo que hay público.
- El groove agregado funciona bien como guía.

### You Really Got Me Now

- Sigue bien alineado con Bon Jovi.
- El groove escrito está bien.
- Todavía no tiene imagen/tab embebida como otros temas.

No es un error, pero sí una diferencia respecto al nivel de detalle de otros tracks.

### Arte Infernal

- Quedó corregido.
- BPM del archivo, estructura y nota final ahora apuntan todos a la misma zona.

Ya no lo listaría como problema.

### Born To Be Wild

- De los mejores resueltos del repo hoy.
- Tiene:
  - BPM consistente
  - imagen local correcta
  - groove base y coro bien diferenciados

### Sobrio a las Piñas

- Mucho mejor que antes desde lo editorial.
- El punto a revisar no es el BPM interno sino la utilidad diferencial de los tres grooves escritos.

Recomendación:

- Diferenciar más el `Puente con silencios` y el `Final abierto` o simplificar la sección.

## Prioridad de correcciones sugerida

1. Corregir en [05-pride-and-joy.md](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/05-pride-and-joy.md:41) la imagen `tab-honky-tonk-women.png` por `tab-pride-and-joy.png`.
2. Mejorar la legibilidad del groove base en [03-honky-tonk-women.md](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/03-honky-tonk-women.md:44).
3. Hacer que las tres secciones de grooves de [10-sobrio-a-las-pinias.md](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/10-sobrio-a-las-pinias.md:42) se distingan más entre sí.
4. Si quieren mantener un criterio uniforme, agregar imagen/tab embebida también a [07-you-really-got-me-now.md](/Users/agustinsackmann/Repos/Personal/CableATierra/canciones/07-you-really-got-me-now.md:37).
5. Reforzar con referencias privadas o internas los temas de `Justo Alegre`.

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
