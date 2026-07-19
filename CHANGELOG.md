# CHANGELOG — APO (AIMARKTECH Project Organizer)

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[Versionado Semántico (SemVer)](https://semver.org/lang/es/). Versionado **de producto** (ver
`VERSION`), independiente de `schemaVersion` (formato de las configs).

## [Unreleased]
### Pendiente (Core · Arquitecto Técnico)
- `core/` (config, filesystem, inventory, classifier, validator, migration, events, reports, logger,
  manifest, index, cli), `launcher/` (PowerShell), `tests/`, reportes CSV, inventario, copia, `state/`.

## [0.1.0] — En desarrollo · MVP (valida la arquitectura con el proyecto Alicia Arouesty)
### Added
- Fundación del producto en repo propio: `README.md`, `ARCHITECTURE.md` (RFC interna),
  `CONTRIBUTING.md`, `CHANGELOG.md`, `DECISIONS.md` (ADR), `VERSION`, `.gitignore`.
- Dominio config-driven: `project` · `structure` · `readmes` · `file-map` · `classification-rules`.
- JSON Schemas (draft-07) de las 5 configs + reglas de **validación funcional cruzada**; configs de
  Alicia validadas contra sus esquemas (5/5 OK).
- Estructura del producto: `core/`, `launcher/`, `plugins/`, `tests/`, `state/`, `reports/`, `logs/`,
  `docs/`, `examples/`.
- Ejemplo funcional en `examples/demo/` (config genérica, sin depender de un cliente real).
### Principios establecidos
- "Config es verdad. State se regenera.", determinismo, idempotencia, cambios aditivos primero,
  Event Bus desacoplado, Core agnóstico al VCS, Product Version ≠ schemaVersion.
