# CableATierra 🎸🥁

Repositorio de trabajo para la banda **CableATierra** — covers de distintos artistas.

Este repositorio sirve como cuaderno de notas para el baterista: BPM, partes de cada canción, cortes y grooves.

## Estructura

```
CableATierra/
├── README.md          → Este archivo
├── tracklist.md       → Lista completa de canciones con info rápida
├── docs/              → Sitio web listo para GitHub Pages
└── canciones/         → Una carpeta por canción con notas detalladas
    ├── _TEMPLATE.md   → Plantilla para agregar nuevas canciones
    └── NN-<cancion>.md→ Notas de cada canción
```

## ¿Cómo usar?

1. Consultar `tracklist.md` para ver el setlist con BPM y estado de cada tema.
2. Abrir el archivo en `canciones/` para ver o editar las notas detalladas de una canción.
3. Para agregar una nueva canción, copiar `canciones/_TEMPLATE.md` con el nombre de la canción y completar los campos.

## Sitio web

El repo ya incluye un sitio estático en `docs/` para publicar con GitHub Pages.

### Qué muestra

- portada con el setlist completo
- navegación por track
- render del markdown real de cada canción
- imágenes de tablaturas cuando existan

### Cómo publicarlo en GitHub

1. Subir el repo a GitHub.
2. Ir a la configuración del repo.
3. En GitHub Pages, elegir publicar desde la rama principal usando la carpeta `docs/`.
4. Guardar la configuración y esperar a que GitHub genere la URL pública.

### Cómo mantenerlo actualizado

- editar las canciones en `canciones/NN-<nombre>.md`
- si cambias el contenido de un track, copiar también el archivo actualizado a `docs/data/canciones/`
- si agregas un track nuevo, actualizar `tracklist.md` y `docs/data/tracks.json`

## Campos por canción

| Campo     | Descripción                                              |
|-----------|----------------------------------------------------------|
| **BPM**   | Tempo de la canción (puede tener variaciones por parte)  |
| **Partes**| Estructura: Intro, Verso, Pre-coro, Coro, Puente, Outro |
| **Cortes**| Momentos de silencio, remates o paradas bruscas         |
| **Grooves**| Patrón rítmico predominante en cada parte               |

## Convenciones de escritura

- Las partes se nombran con mayúscula inicial: `Intro`, `Verso A`, `Coro`.
- Los cortes se indican con ✂️ y la parte en que ocurren.
- Los grooves usan nomenclatura simple: `rock`, `shuffle`, `funk`, `balada`, `medio tiempo`, etc.
- El estado de cada canción puede ser: `🟢 lista`, `🟡 en progreso`, `🔴 pendiente`.
