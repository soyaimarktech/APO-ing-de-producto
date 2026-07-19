# DECISIONS — APO (Architecture Decision Records)

Registro de decisiones de arquitectura (ADR). Cada entrada explica **por qué** se decidió algo, no
solo qué. En seis meses, esto es lo que evita rediscutir lo ya resuelto.

Formato: Contexto · Decisión · Consecuencias · Estado.

---

## ADR-001 · Separar Config y State
- **Contexto:** mezclar entrada humana con salida generada provoca corrupción y ediciones a mano.
- **Decisión:** `config/` es INPUT (verdad, solo-lectura para el motor). `state/`, `reports/`, `logs/`
  son OUTPUT regenerable.
- **Consecuencias:** el estado se puede borrar y regenerar; el motor nunca escribe en `config/`.
- **Estado:** Aceptada.

## ADR-002 · `core/` en lugar de `engine/`
- **Contexto:** "engine" sugiere un bloque monolítico.
- **Decisión:** el núcleo se llama `core/` y expone la API interna; nada fuera del Core toca el FS.
- **Estado:** Aceptada.

## ADR-003 · Event Bus desacoplado
- **Contexto:** conectar Drive/GitHub/dashboard sin acoplar el núcleo.
- **Decisión:** el Core **emite** eventos; los plugins **escuchan**. El bus **no ejecuta lógica** y el
  Core **no conoce** a los plugins.
- **Estado:** Aceptada (diseñado; implementación en v0.3.0).

## ADR-004 · Config-driven + JSON Schema como contrato del dominio
- **Contexto:** evitar hardcodear metodología en el motor.
- **Decisión:** estructura, mapeos, LEEME y reglas viven en JSON; los JSON Schema (draft-07) son el
  contrato. El motor pregunta al schema, nunca supone.
- **Estado:** Aceptada.

## ADR-005 · GitHub versiona; el Core es agnóstico al control de versiones
- **Contexto:** no atar el producto a una plataforma.
- **Decisión:** GitHub versiona la configuración pero no es base de datos. El Core **no invoca git** ni
  consulta Issues/Commits/PRs; solo lee archivos locales. Si se cambia a GitLab/Azure, APO sigue igual.
- **Estado:** Aceptada.

## ADR-006 · Product Version ≠ schemaVersion
- **Contexto:** el software y el formato de las configs evolucionan a ritmos distintos.
- **Decisión:** `VERSION` (estado de APO) y `schemaVersion` (formato de config) son independientes.
- **Estado:** Aceptada.

## ADR-007 · Cambios aditivos antes que destructivos
- **Contexto:** renombrar/eliminar campos rompe compatibilidad y obliga a migraciones.
- **Decisión:** en el dominio se agregan propiedades/reglas; lo destructivo exige migración + subir
  `schemaVersion`.
- **Estado:** Aceptada.

## ADR-008 · APO es un producto independiente
- **Contexto:** vivía dentro del repo de un cliente (Alicia), contradiciendo su independencia.
- **Decisión:** repo propio `soyaimarktech/APO-ing-de-producto`. Los repos de clientes son
  **consumidores** de APO, no su hogar.
- **Estado:** Aceptada.

## ADR-009 · Custodias del proyecto
- **Decisión:** Claude = Arquitecto Funcional (dominio/config/contratos) · ChatGPT = Arquitecto Técnico
  (core/tests/evolución) · José (AIMARKTECH) = visión de negocio.
- **Estado:** Aceptada.

---

# Decisiones técnicas (TD)

Decisiones de implementación, propiedad del **Arquitecto Técnico** (no afectan el dominio).

## TD-001 · Organización del Core por paquetes
- **Contexto:** definir la organización interna del código del Core antes de escribir el primer módulo.
- **Decisión:** `core/` se organiza **por paquetes** (`config/`, `validation/`, `filesystem/`,
  `reporting/`, `shared/`, `cli/`), no por archivos planos. **Congelada para la serie 0.1.x.**
- **Consecuencias:** no cambia el dominio, los contratos ni las responsabilidades; solo la organización
  del código para que cada área crezca sin archivos enormes. Mejoras estructurales futuras van al
  backlog de una versión mayor (0.2.0 / 1.0.0), no interrumpen el desarrollo en curso.
- **Estado:** Aceptada (Arquitecto Técnico).
