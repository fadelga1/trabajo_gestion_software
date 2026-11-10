# Acta de Línea Base — SIGR v1.0.0

## Identificación
- **Versión:** v1.0.0
- **Fecha de aprobación:** 2026-11-09
- **Tag Git:** v1.0.0 (anotado)
- **Commit:** 
- **Rama de referencia:** master
- **Tagger:** fadel1 <fabiandelgado33@gmail.com>

## Alcance
1. Módulo de autenticación con roles (admin, mesero, cliente)
2. Módulo de menú digital con CRUD de categorías y platos
3. Módulo de pedidos con seguimiento en tiempo real (polling 4s)
4. Módulo de reservas por fecha y hora
5. Módulo de cierre de caja y reportes diarios de ventas

## Criterios de aceptación aprobados
| Módulo | Pruebas | Estado |
|---|---|---|
| Autenticación | 7/7 | ✅ |
| Menú digital | 10/10 | ✅ |
| Pedidos | 13/13 | ✅ |
| Reservas | 14/14 | ✅ |
| Caja y reportes | 16/16 | ✅ |
| **Total** | **60/60** | ✅ |

## Métricas del repositorio
- **Archivos versionados:** 20
- **Commits de feature mergeados:** 5 (uno por módulo)
- **Commits de merge explícitos (`--no-ff`):** 6 (5 módulos + release)
- **Tags:** 1 (`v1.0.0`)
- **Ramas activas:** 2 (`master`, `develop`)
- **Sin basura versionada:** verificado (`.db`, `venv/`, `.bak`, `.env`)

## Historia de commits clave
| Etapa | Commit |
|---|---|
| Inicial | c5b08aa |
| Evidencias iniciales | 39e04bb |
| Módulo auth | aff9232 |
| Merge auth | e81f3f3 |
| Módulo menú | 02314dc |
| Merge menú | d6514d6 |
| Módulo pedidos | 2ed0700 |
| Merge pedidos | 92f0a95 |
| Fix reservas | 52b38de |
| Merge reservas | ff9d8f8 |
| Módulo caja/reportes | 76a03ce |
| Merge caja/reportes | 6b31f0a |
| Preparación release | 35a67d8 |
| **Release v1.0.0** | **fc012d7** 🏷️ |
| Sincronización develop | 4d40288 |
| Acta de línea base | bf1dab2 |

## Aprobación
- **Estado:** ✅ APROBADO para QA y despliegue
- **Aprobado por:** fadel1
- **Próxima revisión:** al finalizar sprint de QA
