# Guía de contribución

"Este proyecto fue iniciado por Fabián Delgado (Coordinador / Líder de Proyecto) y posteriormente validado por Felix Andres Betancur Sanchez (Desarrollador Frontend / QA) y Karen Lizette Garavito Pinzon  (Desarrollador / QA)."

## Ramas
- `main`      → producción (protegida, solo merges de release/hotfix)
- `develop`   → integración
- `feature/*` → nuevas funcionalidades
- `release/*` → preparación de release
- `hotfix/*`  → correcciones urgentes sobre main

## Commits convencionales
`tipo(alcance): descripción` donde tipo ∈ {feat, fix, docs, style, refactor, test, chore}.

Ejemplo: `feat(pedidos): agregar endpoint de seguimiento en tiempo real`

## Flujo
1. Crear rama desde `develop`: `git checkout -b feature/mi-feature`
2. Commitear cambios atómicos.
3. Push y Pull Request a `develop`.
4. Al aprobar release: merge a `main` + tag `vX.Y.Z`.
