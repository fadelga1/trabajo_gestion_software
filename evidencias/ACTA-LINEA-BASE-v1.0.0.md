# Acta de Línea Base — SIGR v1.0.0

- **Fecha de aprobación:** 2026-11-09
- **Tag Git:** v1.0.0
- **Commit:** <hash de git rev-parse v1.0.0^{commit}>
- **Rama de referencia:** master
- **Alcance:** 5 módulos del sistema
  - Autenticación (admin, mesero, cliente)
  - Menú digital (CRUD categorías y platos)
  - Pedidos en tiempo real (polling)
  - Reservas por fecha y hora
  - Cierre de caja y reportes diarios
- **Criterios de aceptación:**
  - Autenticación: 7/7 pruebas
  - Menú: 10/10 pruebas
  - Pedidos: 13/13 pruebas
  - Reservas: 14/14 pruebas
  - Caja/Reportes: 16/16 pruebas
- **Archivos versionados:** 20
- **Sin basura** (`.db`, `venv/`, `.bak`, `.env`): verificado
- **Aprobado por:** [Tu nombre]
- **Estado:** APROBADO para QA y despliegue
- **Próxima revisión:** al finalizar sprint de QA

## Commits clave

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
| Módulo reservas (fix) | 52b38de |
| Merge reservas | ff9d8f8 |
| Módulo caja/reportes | 76a03ce |
| Merge caja/reportes | 6b31f0a |
| Preparación release | 35a67d8 |
| **Release v1.0.0** | **fc012d7** 🏷️ |
| Sincronización develop | 4d40288 |
| Acta de línea base | bf1dab2 |
