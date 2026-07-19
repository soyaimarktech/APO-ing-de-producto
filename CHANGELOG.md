# CHANGELOG — APO (AIMARKTECH Project Organizer)

Formato inspirado en *Keep a Changelog*. Versionado **de producto** (ver `VERSION`).
Independiente de `schemaVersion` (formato de las configs).

## [0.1.0] — En desarrollo · MVP (valida la arquitectura con el proyecto Alicia Arouesty)

### Arquitectura (congelada)
- Principios (incl. "Config es verdad. State se regenera.", determinismo, plugins no modifican config,
  cambios aditivos antes que destructivos), custodias, layout (`core/`), flujo, contrato de eventos,
  códigos de salida y políticas de copia (`onConflict`: skip/overwrite/rename/hash).
- `ARCHITECTURE.md` como RFC interna; `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`.

### Dominio (funcional · listo)
- Config-driven: `project` · `structure` · `readmes` · `file-map` · `classification-rules`.
- JSON Schemas (draft-07) de las 5 configs + reglas de **validación funcional cruzada**.
- Configs de Alicia validadas contra sus esquemas (5/5 OK).

### Pendiente (técnico · Arquitecto Técnico)
- `core/` (config, filesystem, inventory, classifier, validator, migration, events, reports, logger,
  manifest, index, cli), `launcher/` (PowerShell), `tests/`, reportes CSV, inventario, copia, `state/`.
