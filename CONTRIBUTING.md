# CONTRIBUTING — APO (AIMARKTECH Project Organizer)

APO es una herramienta interna de AIMARKTECH. Aunque hoy el equipo es reducido, seguimos una
disciplina profesional para que el producto escale con calidad.

## Custodias (quién decide qué)
- **Claude — Arquitecto Funcional:** `config/`, `config/_schema/`, reglas de negocio, contenido y
  el dominio en `ARCHITECTURE.md`. Define qué significa "válido" y "correcto".
- **ChatGPT — Arquitecto Técnico:** `core/`, `launcher/`, `tests/`, reportes, eventos, migraciones y
  plugins. Define cómo se implementa y evoluciona.
- **José (AIMARKTECH) — Negocio:** prioridades, clientes y uso real.

## Reglas de contribución
1. **Arquitectura congelada por versión.** Cambios estructurales pasan por **revisión de arquitectura**
   entre los dos arquitectos. `ARCHITECTURE.md` es la fuente de la verdad de diseño (RFC interna):
   si hay una duda de cómo debe funcionar APO, la respuesta vive ahí, no en el código.
2. **Cambios de dominio: aditivos antes que destructivos.** Agregar propiedades/reglas > renombrar o
   eliminar. Lo destructivo exige **migración** y subir `schemaVersion`.
3. **`config/` es solo-lectura para el motor.** Todo lo generado va a `state/`, `reports/`, `logs/`.
   El *state* se regenera; nunca se edita a mano.
4. **Ningún módulo se cierra sin pruebas** (unit + las de integración/regresión que apliquen).
5. **Determinismo.** Mismas entradas ⇒ mismas salidas (salvo timestamps).
6. **Todo cambio relevante se anota en `CHANGELOG.md`.**

## Documentos oficiales
| Documento | Propósito |
|---|---|
| `README.md` | Cómo usar APO. |
| `ARCHITECTURE.md` | Cómo está diseñado (RFC interna). |
| `CHANGELOG.md` | Qué cambió, por versión. |
| `CONTRIBUTING.md` | Cómo contribuir (este documento). |
