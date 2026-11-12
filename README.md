# SIGR — Sistema Integral de Gestión de Restaurante

Sistema web en Flask + SQLite con 5 módulos:
autenticación, menú digital, pedidos, reservas y cierre de caja/reportes.

## Requisitos
- Python 3.10+
- pip

## Instalación
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Ajusta SECRET_KEY
python app.py

## Versión

**SIGR v1.1.0** — Documentación completa y estabilización (2026-11-10).

Línea base anterior: v1.0.0 (2026-11-09).

## 👥 Equipo de Desarrollo

Este proyecto fue desarrollado y validado por:

*   *Fabián Delgado* - Coordinador de Proyecto, Desarrollo Backend y Control de Versiones.
*   *Felix Andres Betancur Sanchez* - Desarrollo Frontend y Pruebas de Integración.
*   *Karen Lizette Garavito Pinzon* - Análisis de Requerimientos, QA y Documentación.

*Institución:* TECNOLOGICA DEL ORIENTE
*Curso:* INGENIERIA DE SOFTWARE
*Fecha:* Noviembre 2026

