# CableATierra 🎸🥁

Repositorio de trabajo para la banda **CableATierra** — covers de distintos artistas.

Este repositorio sirve como cuaderno de notas para el baterista: BPM, partes de cada canción, cortes y grooves.

## Estructura

```
CableATierra/
├── README.md          → Este archivo
├── tracklist.md       → Lista completa de canciones con info rápida
└── canciones/         → Una carpeta por canción con notas detalladas
    ├── _TEMPLATE.md   → Plantilla para agregar nuevas canciones
    └── <cancion>.md   → Notas de cada canción
```

## ¿Cómo usar?

1. Consultar `tracklist.md` para ver el setlist con BPM y estado de cada tema.
2. Abrir el archivo en `canciones/` para ver o editar las notas detalladas de una canción.
3. Para agregar una nueva canción, copiar `canciones/_TEMPLATE.md` con el nombre de la canción y completar los campos.

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
