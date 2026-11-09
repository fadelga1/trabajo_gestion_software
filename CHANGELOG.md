# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.0.0] - 2026-11-09

### Added
- Módulo de autenticación con roles (admin, mesero, cliente).
- Módulo de menú digital con CRUD de categorías y platos.
- Módulo de pedidos con seguimiento en tiempo real (polling cada 4s).
- Módulo de reservas por fecha y hora con validación de duplicados.
- Módulo de cierre de caja y reportes diarios de ventas.
- Seed automático de usuarios demo y menú inicial.
- Control de acceso por rol (403 en rutas protegidas).
- Endpoint `/api/pedidos/seguimiento` para polling en tiempo real.

### Changed
- `requirements.txt`: añadida dependencia `Flask-SQLAlchemy==3.1.1`.
- Documentado Python 3.11/3.12 como versión requerida.

### Fixed
- Bloque huérfano en `app.py` que causaba `SyntaxError` en el módulo de reservas.
- Sincronización de `develop` con `release/1.0.0` tras merges de features.