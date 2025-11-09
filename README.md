
# Nombre del proyecto

preprocesamiento-ciencia-datos

## Objetivo

Proveer un conjunto de recursos, scripts y buenas prácticas para el preprocesamiento de datos en proyectos de ciencia de datos. El objetivo es facilitar la limpieza, transformación, normalización y generación de características para dejar datasets listos para entrenamiento y evaluación de modelos.

## Estructura básica de carpetas

Este es un esqueleto recomendado para mantener el proyecto organizado:

- `data/`
	- `raw/` — Datos originales (sin tocar).
	- `processed/` — Datos transformados listos para modelado.
- `notebooks/` — Jupyter notebooks para EDA y prototipado.
- `src/` o `scripts/` — Código fuente (funciones y scripts de preprocesamiento).
- `models/` — Artefactos de modelos (opcional).
- `tests/` — Pruebas unitarias y casos de ejemplo.
- `docs/` — Documentación y notas del proyecto.
- `.github/` — Flujos de trabajo de CI/CD y configuraciones (opcional).