# Historial de Cambios (Chorderizer)

## [1.1.0] - 2026-03-29

### Añadido
- Soporte para colores en la terminal en Windows mediante la integración de `colorama`.
- Nuevo sistema de construcción basado en `pyproject.toml` (PEP 621).
- Directorio de pruebas unitarias (`tests/`) con validación de lógica de teoría musical.
- Comprobaciones de seguridad para asegurar que las notas MIDI se mantengan en el rango válido [0, 127].
- Dependencia de `colorama` añadida para una mejor experiencia de usuario en terminales Windows.

### Cambiado
- Reorganización masiva del código: la lógica de transposición se movió de `chorderizer.py` a `theory_utils.py`.
- Mejorada la lógica de análisis de nombres de acordes (separación de raíz y sufijo).
- Actualizada la documentación (`README.md`) para reflejar los cambios en el proceso de instalación y dependencias.
- Eliminado el archivo `setup.py` en favor de `pyproject.toml`.

### Corregido
- Posibles fallos al trasponer acordes con raíces de dos caracteres (ej. C#, Bb).
- Advertencias sobre la creación de directorios para exportación MIDI.

## [1.0.1] - 2025-03-01
- Versión inicial estable con generación de escalas y exportación MIDI básica.
