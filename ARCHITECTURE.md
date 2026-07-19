# APO — AIMARKTECH Project Organizer · ARCHITECTURE

- **Versión de producto:** `0.1.0` (MVP · valida arquitectura con el proyecto Alicia Arouesty)
- **Estado:** arquitectura base **congelada**. Cambios estructurales requieren revisión de arquitectura.
- **Custodias:** Claude = Arquitecto Funcional · ChatGPT = Arquitecto Técnico · José (AIMARKTECH) = visión de negocio y uso real.

> APO no es un script para Alicia. Alicia es el **primer proyecto que valida la arquitectura** de una
> herramienta interna reutilizable de AIMARKTECH.

---

## 1. Principios

1. **Config es verdad. State se regenera.**
2. **El motor pregunta al Schema; nunca supone.** `config → schema → validate → core`.
3. **`config/` es de solo lectura para APO.** Todo lo generado va a `state/`, `reports/`, `logs/`.
4. **Contenido ≠ Configuración ≠ Motor.** El motor no contiene datos de ningún cliente.
5. **GitHub versiona; no es base de datos.** APO solo lee archivos locales; no consulta Issues,
   Commits ni PRs. Así funciona igual con GitHub, GitLab o Azure DevOps.
6. **Ante la duda, reportar y no tocar.**
7. **Compatibilidad hacia atrás:** cambios de formato se manejan con `schemaVersion` + migraciones.
8. **Determinismo:** mismas configs + archivos + parámetros ⇒ mismo resultado (manifest, index,
   reporte; log idéntico salvo timestamp). Facilita las pruebas.
9. **Los plugins nunca modifican `config/`.** Pueden leer, publicar y sincronizar; jamás alterar la verdad.
10. **Cambios aditivos antes que destructivos.** En el dominio se agregan propiedades/reglas; renombrar
    o eliminar solo vía migración con subida de `schemaVersion`.

---

## 2. Responsabilidades (custodias)

| Área | Custodio | Alcance |
|---|---|---|
| Metodología, `config/`, `_schema/`, reglas de negocio, contenido | **Claude (Funcional)** | Qué significa "válido" y "correcto" para AIMARKTECH |
| `core/`, `launcher/`, validaciones, reportes, eventos, migraciones, plugins, tests | **ChatGPT (Técnico)** | Cómo se implementa y evoluciona el software |
| Prioridades, clientes, uso real | **José (Negocio)** | Qué se construye y para quién |

---

## 3. Layout

```
APO/
├── core/          # núcleo Python (API interna; NADA fuera del Core toca el FS):
│                  #   config, filesystem, inventory, classifier, validator,
│                  #   migration, events, reports, logger, manifest, index, cli
├── launcher/      # lanzador PowerShell (invoca el core en Windows)
├── config/        # INPUT humano (verdad, versionado)
│   ├── _schema/   #   JSON Schemas (dominio · Claude)
│   └── <cliente>/ #   project / structure / readmes / file-map / classification-rules
├── state/         # OUTPUT generado (manifest.json, index.json) — no editar a mano
├── reports/       # OUTPUT (CSV siempre; XLSX/Word opcional; bitacora.md)
├── logs/          # OUTPUT técnico por corrida
├── plugins/       # (v0.3.0) integraciones vía eventos (drive, github, dashboard)
└── tests/         # unit / integration / regression
```

---

## 4. Flujo de ejecución

```
config/<cliente>/*.json
        │
        ▼
   _schema/*  ──►  validate.py  (Capa 1 estructural + Capa 2 funcional)
        │                 │ falla ► exit 2/3 + evento ValidationFailed
        ▼                 ▼
      core  ──►  filesystem / inventory / classifier
        │
        ├─► crea estructura + LEEME
        ├─► clasifica y copia (file-map → rules → difusa → sin clasificar)
        ├─► escribe state/ (manifest, index)
        └─► escribe reports/ + logs/  + emite eventos
```

Orden del clasificador: **file-map exacto → reglas por patrón (por `priority`) → difusa (solo sugiere) → sin clasificar (`destination: null`)**. Matching case/accent-insensitive.

---

## 5. Contrato de eventos (Event Bus — diseñado, no implementado en v0.1.0)

Forma mínima de un evento:

```
Event {
  timestamp   # ISO-8601
  type        # ver catálogo
  payload     # objeto libre según el tipo
}
```

Catálogo inicial: `RunStarted`, `FolderCreated`, `FileCopied`, `DuplicateDetected`,
`ConflictFound`, `ValidationFailed`, `ReportGenerated`, `RunFinished` (incluye `exitCode`).

Regla: el `core` **emite** eventos; los `plugins/` los **escuchan**. El core nunca conoce a los plugins.
El Event Bus **nunca ejecuta lógica**: solo publica.

---

## 6. Estado generado (contrato de salida)

- `state/<cliente>/manifest.json` — resumen del estado del proyecto (carpetas, documentos,
  pendientes, advertencias, `schemaVersion`, `generatedAt`).
- `state/<cliente>/index.json` — índice documental. **Identificador estable = clave lógica**
  (nombre de archivo del file-map); `DOC-###` es solo un id de presentación determinista.
- Nunca se editan a mano; si se pierden, se regeneran desde el sistema de archivos + `config/`.

---

## 7. Códigos de salida

| Código | Significado |
|---|---|
| `0` | Todo correcto |
| `1` | Con advertencias |
| `2` | Errores recuperables |
| `3` | Error crítico |

---

## 8. Políticas de copia (`onConflict`)

`skip` (default) · `overwrite` · `rename` (`Documento (1).docx`) · `hash` (SHA-256; si es idéntico no
copia, registra "duplicado"). Copia idempotente; nunca sobrescribe sin flag.

---

## 9. Convenciones

- Nombres sin `: / \ * ? " < > |`; vigilar **MAX_PATH (260)** en Windows.
- Todo UTF-8. En PowerShell 5.1, `.ps1` en UTF-8 con BOM.
- `schemaVersion` obligatorio en cada config; si la config es más nueva que el core → error crítico.

---

## 10. Política de pruebas

- **Unit:** por módulo (`filesystem`, `inventory`, `classifier`, `validate`, `reports`, `config`).
- **Integration:** carpeta temporal → crear proyecto → copiar → reportar → verificar.
- **Regression:** ante un bug, primero la prueba que lo reproduce, luego el fix.
- **Regla:** ningún módulo se cierra sin pruebas (aunque sean pocas).

---

## 11. Versionado de PRODUCTO y roadmap

| Versión | Alcance |
|---|---|
| **0.1.0 — MVP (Alicia)** | Leer `config/`, validar (estructural+funcional), crear estructura, inventario, copiar, `LEEME.txt`, reportes CSV, logs, `state/`, pruebas básicas. |
| **0.2.0** | Reportes Excel/Word, coincidencia difusa, `onConflict` avanzado (hash/rename), rendimiento. |
| **0.3.0** | Event Bus, plugins, APO Registry, estadísticas de ejecución. |
| **1.0.0** | Interfaz gráfica, gestión multicliente, integración con el ecosistema AIMARKTECH. |

> El versionado es **del producto**, no del código. Cualquier cambio importante (módulos nuevos,
> cambios de estructura) pasa por revisión de arquitectura entre los dos arquitectos.

**Product Version ≠ Schema Version.** `VERSION` (estado de APO) y `schemaVersion` (formato de cada
config) evolucionan de forma **independiente**: APO puede ir en 0.5.0 con Schema 1. **APO Registry**
se considera un **producto aparte**, fuera del alcance de la v1.

---

## 12. Referencias

- Contrato operativo y modos de ejecución: `README.md`.
- Esquemas y reglas de validación del dominio: `config/_schema/README.md`.
