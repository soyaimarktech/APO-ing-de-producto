# APO · Esquemas y reglas de validación (dominio)

Estos JSON Schema (draft-07) definen la **forma válida** de cada archivo de configuración. Los
mantiene el Arquitecto Funcional (Claude); el motor (ChatGPT) solo los **consume**.

> Nota: se omitieron las claves `$schema`/`$id` con URL remota; usa un validador draft-07 explícito
> (p. ej. en Python `jsonschema.Draft7Validator`). Las claves `_draft`, `_id` y `_nota` son
> informativas y los validadores las ignoran.

## Archivos
| Config | Esquema |
|---|---|
| `project.json` | `project.schema.json` |
| `structure.json` | `structure.schema.json` |
| `readmes.json` | `readmes.schema.json` |
| `file-map.json` | `file-map.schema.json` |
| `classification-rules.json` | `classification-rules.schema.json` |

---

## Validación en 2 capas

`validate.py` debe aplicar **ambas**:

### 1) Validación estructural (estos JSON Schema)
Tipos, campos requeridos, enums, caracteres inválidos en nombres, etc.

### 2) Validación funcional (reglas de negocio — cruzan varios archivos)
Estas NO se pueden expresar en un solo schema; el motor debe implementarlas:

1. **Ramas raíz coherentes:** `clientFolder` e `internalFolder` de `project.json` deben existir como
   claves de primer nivel en `structure.json/tree`.
2. **Destinos existentes:** todo `destination` en `file-map.json` y en `classification-rules.json`
   (cuando no es `null`) debe corresponder a una **ruta que exista en `structure.json`**.
3. **Claves de LEEME válidas:** toda clave de `readmes.json/readmes` debe ser una **ruta relativa que
   exista en `structure.json`** (incluye las carpetas raíz).
4. **Sin destinos duplicados por archivo:** en `file-map.json` no puede haber dos entradas que
   apunten al mismo archivo de origen (comparación **case-insensitive + accent-insensitive**).
5. **Prioridades:** en `classification-rules.json`, advertir (warning, no error) si dos reglas con
   patrones solapables comparten `priority` (ambigüedad de orden).
6. **Regla de respaldo:** debe existir al menos una regla con `match.type = "any"` (o `"none"`) y
   `destination = null` como último recurso, para que ningún archivo se clasifique "por accidente".
7. **Compatibilidad de versión:** si `schemaVersion` de una config es **mayor** que la soportada por
   el motor → error crítico (config más nueva que APO). Si es menor → intentar `migrations.py`.
8. **Longitud de ruta:** advertir si `rootFolderName` + la ruta más profunda del árbol puede exceder
   MAX_PATH (260) en Windows.

Severidades sugeridas: reglas 1–4, 6, 7 = **error**; reglas 5, 8 = **advertencia**.

---

## Contrato de estado generado (para referencia del motor)

`state/<cliente>/manifest.json` y `state/<cliente>/index.json` son **salida** (no llevan schema de
entrada). Se recomienda que el motor les ponga su propio `schemaVersion` y un `generatedAt` ISO-8601,
y que **nunca** se editen a mano.


---

## Project Aggregate ↔ contrato (para DT-003 / DT-004)

Al cargar `config/<cliente>/`, el `ConfigLoader` construye un `ProjectConfig` (agregado) a partir de
**archivos con nombre fijo**. Mapeo autoritativo:

| Modelo del agregado | Archivo | Claves de nivel superior |
|---|---|---|
| `ProjectMetadata` | `project.json` | `schemaVersion` (int), `name` (str, **nombre de negocio**), `rootFolderName`, `clientFolder`, `internalFolder` |
| `StructureConfig` | `structure.json` | `schemaVersion`, `tree` (objeto recursivo) |
| `ReadmeConfig` | `readmes.json` | `schemaVersion`, `readmes` (ruta relativa → texto) |
| `FileMapConfig` | `file-map.json` | `schemaVersion`, `files` (nombre de archivo → `{destination, onConflict?, id?}`) |
| `ClassificationRules` | `classification-rules.json` | `schemaVersion`, `matchOptions?`, `rules[]` |

### Archivos obligatorios vs opcionales (decisión de dominio)
- **Obligatorios:** `project.json` y `structure.json`. Si falta alguno → `ConfigurationError`.
- **Opcionales** (con comportamiento por defecto si faltan):
  - `readmes.json` ausente → no se generan LEEME (aunque se pida `-WithReadme`, se advierte).
  - `file-map.json` ausente → sin mapeos exactos; la clasificación usa solo reglas + difusa.
  - `classification-rules.json` ausente → por defecto "sin clasificar" (todo va a pendientes/reporte).
- **Archivo desconocido** en la carpeta del cliente → **advertencia** (se ignora), no error.

> Estas son reglas de dominio (custodia funcional). La implementación del Aggregate/Loader queda del
> lado técnico; si algo aquí necesitara cambiar, se reporta y lo ajusto en el dominio.
