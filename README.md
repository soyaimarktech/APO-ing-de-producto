# APO — AIMARKTECH Project Organizer

Herramienta interna de AIMARKTECH para **crear, sincronizar y auditar** la estructura de carpetas y
entregables de cada cliente (primer cliente: Alicia Arouesty). Diseñada como **config-driven** para
servir a cualquier cliente sin tocar el motor.

> 🔒 INTERNO (AIMARKTECH). No compartir con el cliente.

---

## Principio rector: contenido ≠ configuración ≠ motor

- **Configuración (INPUT · fuente de verdad de la metodología):** archivos JSON escritos por humanos.
  Viven en `config/<cliente>/` y se versionan en GitHub. **GitHub versiona la verdad; no ES la verdad.**
- **Estado (OUTPUT · generado, regenerable):** archivos que produce el motor (`manifest.json`,
  `index.json`, reportes, bitácora, logs). **Nunca se editan a mano.** Si se pierden, se regeneran
  desde el sistema de archivos + la configuración.
- **Núcleo (código):** `core/` en Python + `launcher/` en PowerShell (Windows). No contiene datos de
  ningún cliente.

---

## Layout del módulo

```
APO/  (raíz de este repositorio)
├── config/                         # INPUT (verdad, versionado)
│   └── <cliente>/
│       ├── project.json            # nombre, carpeta madre, nombres de ramas
│       ├── structure.json          # árbol de carpetas a crear
│       ├── readmes.json            # LEEME por ruta relativa
│       ├── file-map.json           # mapeo exacto archivo → carpeta
│       └── classification-rules.json  # reglas por patrón (clasificador desacoplado)
├── state/                          # OUTPUT generado (NO editar a mano)
│   └── <cliente>/
│       ├── manifest.json           # estado del proyecto (resumen)
│       └── index.json              # índice documental (id, sha256, status, modified)
├── reports/                        # OUTPUT
│   └── <cliente>/
│       ├── reporte_AAAA-MM-DD.csv  # base siempre disponible
│       ├── reporte_AAAA-MM-DD.xlsx # opcional (Python + openpyxl)
│       └── bitacora.md             # histórico humano acumulado
├── logs/                           # OUTPUT técnico por corrida
├── core/                           # núcleo Python de APO (ChatGPT)
├── launcher/                       # lanzador PowerShell (ChatGPT)
├── plugins/                        # (v0.3.0) integraciones vía eventos
└── tests/                          # unit / integration / regression
```

> Arquitectura completa (principios, flujo, eventos, versionado, roadmap): ver **`ARCHITECTURE.md`**.

---

## Orden de clasificación de un archivo

1. **`file-map.json`** — coincidencia exacta por nombre (máxima prioridad).
2. **`classification-rules.json`** — reglas por patrón; gana la de menor `priority` que cumpla.
   Emparejamiento **case-insensitive y accent-insensitive**.
3. **Coincidencia difusa** — SOLO sugiere, nunca copia automáticamente:
   - `90–100%` = alta confianza · `80–89%` = posible coincidencia · `<80%` = ignorar.

Regla de oro: ante la duda, **reportar y no tocar**.

---

## Identificadores de documento (index.json)

- El **identificador estable** de un documento es su **clave lógica** (nombre de archivo en `file-map`),
  no el `DOC-###`.
- `DOC-###` es solo un id de presentación, asignado de forma **determinista** (orden estable) para que
  no cambie entre corridas. Las referencias entre archivos deben usar la clave lógica.

---

## Políticas de copia (onConflict)

- `skip` (por defecto) · `overwrite` · `rename` (`Documento (1).docx`) · `hash` (compara SHA-256; si
  es idéntico no copia, solo registra "duplicado").
- **Nunca** sobrescribir sin flag explícito. La copia es idempotente.

---

## Códigos de salida

| Código | Significado |
|---|---|
| `0` | Todo correcto |
| `1` | Con advertencias |
| `2` | Errores recuperables |
| `3` | Error crítico |

---

## Validaciones previas a copiar

Nombres inválidos (`: / \ * ? " < > |`), longitud de ruta (MAX_PATH 260), archivos bloqueados/abiertos,
permisos, duplicados y nombres repetidos.

---

## Modos de ejecución

- `estructura` (crear carpetas) · `-WithReadme` · `-DryRun`
- `-Inventario` (escanear y reportar) · `-Analyze` (encontrados / no encontrados / ambiguos)
- `-CopyFiles --source <ruta>` (copiar según file-map + rules)

---

## Roles de colaboración

- **Claude — Arquitecto Funcional:** metodología, estructura documental, reglas de negocio, criterios
  de aceptación y **contenido de la configuración** (`config/<cliente>/*.json`).
- **ChatGPT — Arquitecto Técnico:** arquitectura del software, motor Python + lanzador PowerShell,
  validaciones, reportes, modularidad y evolución (plugins, migraciones de `schemaVersion`).

Fuente compartida: este repositorio de GitHub.
