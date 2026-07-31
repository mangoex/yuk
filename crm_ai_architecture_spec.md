# CRM Inteligente Antigravity
## Marco rector de producto e ingeniería

**Documento:** SDD + SDK/API Specs + BDD + TDD + Roadmap  
**Versión:** 1.0.0  
**Estado:** Propuesta base para validación  
**Fecha:** 2026-07-24  
**Propietarios:** Product Management, Arquitectura de Software y Operaciones Antigravity  
**Audiencia:** Producto, ingeniería, QA, DevOps, seguridad, ventas y operaciones  

---

## Control del documento

### Propósito

Este documento es el contrato inicial desde el cual se diseñará, implementará, probará y desplegará el CRM Inteligente Antigravity. Define:

- qué problema de negocio resuelve el producto;
- qué responsabilidades pertenecen al CRM y cuáles a proveedores externos;
- cómo se organizan los componentes, datos, APIs y eventos;
- qué pueden hacer de forma autónoma los tres agentes de IA;
- qué acciones requieren aprobación humana;
- cómo se verificará el comportamiento antes de liberar cada incremento;
- cómo se desplegará y operará la plataforma.

Una modificación que cambie contratos de API, modelo de datos, reglas de negocio, autonomía de agentes o criterios de aceptación debe actualizar este documento y sus pruebas en el mismo cambio.

### Fuentes de negocio

El alcance se alinea con el sistema de ventas predictivas de ConsultorPRO:

- **SuperProspector:** prospección y cualificación con IA.
- **SuperSales:** análisis y mejora de llamadas de venta.
- **Marketing Auto Pilot:** seguimiento automatizado para evitar que los leads se enfríen.
- **Principio operativo:** medición + análisis = resultados.
- **Objetivo de implantación:** habilitar una primera operación comercial utilizable en semanas, y evolucionarla durante la ejecución conjunta de mercado.

### Supuestos que requieren validación de producto

| ID | Supuesto inicial | Decisión requerida |
|---|---|---|
| AS-01 | La plataforma será multiempresa y cada cliente será un `tenant`. | Confirmar si el MVP inicia con un solo tenant o SaaS multi-tenant. |
| AS-02 | WhatsApp se operará mediante Chatwoot y/o Meta Cloud API. | Elegir integración primaria y responsable de las plantillas aprobadas. |
| AS-03 | Las llamadas pueden llegar como audio, URL firmada o transcripción. | Confirmar fuentes: telefonía, reuniones, carga manual o todas. |
| AS-04 | La IA propone y clasifica; no cierra deals ni cambia importes de forma autónoma. | Confirmar límites comerciales y legales. |
| AS-05 | El envío automático sólo ocurre con consentimiento y reglas horarias válidas. | Definir jurisdicciones, políticas de opt-in y horario por tenant. |
| AS-06 | El proveedor LLM será intercambiable. | Seleccionar proveedor inicial, región y política de retención. |
| AS-07 | El frontend web no forma parte de la primera especificación de componentes detallados. | Confirmar framework y alcance de dashboard. |

### Glosario

| Término | Definición |
|---|---|
| Tenant | Organización cliente cuyos datos y configuración están aislados. |
| ICP | Perfil de Cliente Ideal usado como referencia para scoring. |
| Lead | Persona o empresa potencialmente interesada. |
| Deal | Oportunidad comercial asociada a un lead. |
| Interaction | Mensaje, llamada, correo, nota o evento relacionado con un lead/deal. |
| AI Run | Ejecución trazable de un agente, incluyendo entradas, versión, salida y costo. |
| Human-in-the-loop | Punto explícito de revisión o aprobación humana. |
| Outbox | Patrón transaccional para publicar eventos sin perder consistencia con la BD. |
| Idempotencia | Propiedad por la cual repetir una petición no duplica efectos. |
| PII | Información personal identificable. |
| RPO / RTO | Pérdida máxima aceptable de datos / tiempo objetivo de recuperación. |

---

# 1. MARCO DE REFERENCIA Y ARQUITECTURA GENERAL (SDD)

## 1.1 Visión del producto

Antigravity será un sistema operativo comercial que centraliza el pipeline, observa la actividad de vendedores y prospectos, y utiliza tres agentes especializados para priorizar oportunidades, elevar la calidad de las conversaciones y mantener el seguimiento.

El producto no debe ser un chatbot aislado ni una colección de prompts. Debe ser un CRM transaccional con:

- datos fuente confiables;
- automatizaciones auditables;
- agentes limitados por políticas;
- ejecución asíncrona resiliente;
- explicación de decisiones;
- medición de impacto comercial.

### Objetivos de negocio

1. Reducir el tiempo entre ingreso y primera cualificación del lead.
2. Priorizar la atención comercial con un score explicable y configurable.
3. Convertir cada llamada en datos y coaching accionable.
4. Evitar pérdidas por ausencia de seguimiento.
5. Dar a gerentes visibilidad de actividad, calidad y conversión por vendedor.
6. Medir la contribución de la IA a citas, avance de etapa e ingresos.

### Indicadores de éxito iniciales

| Indicador | Línea base | Meta MVP / piloto | Fuente |
|---|---:|---:|---|
| Leads cualificados dentro de 60 s | Por medir | >= 95% | `ai_runs`, `leads` |
| Tiempo a primera acción comercial | Por medir | Reducción >= 30% | `interactions` |
| Llamadas analizadas dentro de 10 min | Por medir | >= 90% | `ai_runs` |
| Deals elegibles con seguimiento ejecutado o revisado | Por medir | >= 95% | `followup_executions` |
| Mensajes duplicados por reintentos | N/A | 0 | idempotency/outbox |
| Acciones autónomas sin política válida | N/A | 0 | audit log |
| Disponibilidad mensual API | N/A | >= 99.5% en producción | observabilidad |

Las metas comerciales definitivas se fijarán después de medir una línea base real durante el piloto.

## 1.2 Alcance

### Incluido en MVP

- autenticación, autorización por roles y aislamiento por tenant;
- usuarios, equipos de ventas y asignación de leads;
- pipeline, etapas, leads, deals e interacciones;
- ingreso de leads vía API y webhook;
- scoring automático con reglas deterministas + LLM;
- carga/ingesta de llamada o transcripción;
- análisis post-llamada y coaching;
- detección de inactividad y secuencias de seguimiento;
- integración Chatwoot/WhatsApp con trazabilidad;
- bandeja de tareas/aprobaciones para vendedores;
- auditoría, métricas operativas y costos de IA;
- despliegue containerizado con PostgreSQL, Redis y bucket S3-compatible.

### Fuera de alcance inicial

- marcador telefónico propio;
- facturación y contabilidad;
- automatización de campañas publicitarias;
- envío masivo sin consentimiento;
- entrenamiento de modelos fundacionales;
- modificación autónoma de precios, contratos o descuentos;
- decisión autónoma irreversible de descartar un lead;
- data warehouse empresarial completo;
- aplicación móvil nativa.

## 1.3 Principios de arquitectura

1. **Monolito modular primero:** una aplicación FastAPI separada por dominios y uno o más workers. Evita complejidad prematura de microservicios sin impedir extracción futura.
2. **PostgreSQL como fuente de verdad:** Redis acelera y coordina; nunca es la única copia de estado comercial.
3. **Asíncrono para trabajos costosos:** scoring enriquecido, transcripción, análisis y envíos se ejecutan por cola y exponen estado consultable.
4. **Eventos confiables:** cambios de negocio y eventos de integración se persisten mediante outbox.
5. **Proveedor de IA intercambiable:** el dominio consume interfaces internas, no SDKs concretos.
6. **Resultados estructurados:** toda salida LLM se valida contra esquema y política antes de persistir o ejecutar.
7. **Autonomía acotada:** los agentes actúan sólo dentro de permisos, presupuesto, consentimiento y reglas horarias.
8. **Seguridad y privacidad por diseño:** mínimo privilegio, cifrado, reducción de PII, retención configurable y auditoría.
9. **Observabilidad de extremo a extremo:** cada petición, job, webhook y AI Run comparte `correlation_id`.
10. **Configuración sobre código:** ICP, umbrales, SLA, etapas, tono, horarios y políticas pertenecen al tenant.

## 1.4 Vista de contexto

```mermaid
flowchart LR
    Lead["Prospecto"] --> WA["WhatsApp / Chatwoot"]
    Rep["Vendedor"] --> Web["CRM Web"]
    Manager["Gerente"] --> Web
    WA --> API["Antigravity API"]
    Web --> API
    Phone["Telefonía / Reuniones"] --> API
    API --> Agents["Motor de agentes"]
    Agents --> LLM["Proveedor LLM"]
    Agents --> STT["Proveedor STT"]
    API --> Data["PostgreSQL / Redis / Bucket"]
    Agents --> WA
    API --> Obs["Logs / métricas / alertas"]
```

## 1.5 Vista de contenedores y módulos

```mermaid
flowchart TB
    subgraph Clients["Canales"]
        Dashboard["Dashboard web"]
        Chatwoot["Chatwoot"]
        WhatsApp["WhatsApp Cloud API"]
        Telephony["Telefonía / Meet / Zoom"]
    end

    subgraph Platform["Plataforma Antigravity"]
        Ingress["TLS / Reverse proxy"]
        API["FastAPI API"]
        Worker["ARQ workers"]
        Scheduler["Scheduler"]

        subgraph Modules["Módulos de dominio"]
            Identity["Identity & Tenancy"]
            CRM["CRM Core"]
            Interactions["Interactions"]
            AgentRuntime["Agent Runtime & Policies"]
            Integrations["Integration Hub"]
            Reporting["Reporting & Audit"]
        end
    end

    subgraph Persistence["Persistencia"]
        PG[("PostgreSQL 16 + pgvector")]
        Redis[("Redis 7")]
        Bucket[("S3-compatible bucket")]
    end

    subgraph Providers["Proveedores"]
        LLM["LLM"]
        STT["Speech-to-text"]
        Email["Email"]
    end

    Dashboard --> Ingress --> API
    Chatwoot --> Ingress
    WhatsApp --> Ingress
    Telephony --> Ingress
    API --> Modules
    API --> PG
    API --> Redis
    API --> Bucket
    API --> Worker
    Scheduler --> Redis --> Worker
    Worker --> Modules
    AgentRuntime --> LLM
    AgentRuntime --> STT
    Integrations --> Chatwoot
    Integrations --> WhatsApp
    Integrations --> Email
    Modules --> PG
```

### Responsabilidades

| Componente | Responsabilidad | No debe hacer |
|---|---|---|
| FastAPI API | Validar, autorizar, persistir comandos, consultar recursos, recibir webhooks. | Esperar transcripciones o LLMs largos dentro de la petición. |
| CRM Core | Reglas de leads, deals, asignación, pipeline y SLA. | Conocer detalles de SDKs externos. |
| Agent Runtime | Orquestar herramientas, prompts versionados, validación y políticas. | Escribir directamente sin pasar por servicios de dominio. |
| Workers ARQ | Ejecutar jobs idempotentes y reintentables. | Conservar estado sólo en memoria. |
| Scheduler | Crear jobs por SLA/horario. | Enviar mensajes directamente. |
| Integration Hub | Adaptadores Chatwoot, WhatsApp, email, STT, LLM y bucket. | Propagar payloads externos sin normalizar. |
| PostgreSQL | Fuente de verdad y auditoría. | Funcionar como cola de trabajos de alta frecuencia salvo outbox. |
| Redis | Cola, locks, rate limit y caché temporal. | Almacenar el único registro de una decisión. |
| Bucket | Audio, adjuntos, transcripciones extensas y exportaciones. | Exponer objetos públicamente. |

## 1.6 Decisiones tecnológicas

| Área | Selección base | Razón |
|---|---|---|
| Lenguaje | Python 3.12+ | Ecosistema FastAPI/IA y tipado moderno. |
| API | FastAPI + Pydantic v2 | OpenAPI 3.1, async y validación estructurada. |
| Persistencia | SQLAlchemy 2 async + Alembic | Transacciones y migraciones reproducibles. |
| BD | PostgreSQL 16 + pgvector | Integridad relacional y búsqueda semántica opcional. |
| Cola | Redis 7 + ARQ | Encaje async y operación simple para MVP. |
| Storage | S3 / MinIO | Portabilidad entre local y cloud. |
| HTTP | `httpx` | Cliente asíncrono, timeouts y testing. |
| Pruebas | Pytest, pytest-asyncio, pytest-cov, testcontainers | Pirámide de pruebas reproducible. |
| Observabilidad | OpenTelemetry + logs JSON + métricas Prometheus-compatible | Correlación y portabilidad. |
| Packaging | `pyproject.toml` + `uv` | Instalación y locks rápidos/reproducibles. |

No se fija un proveedor LLM en el dominio. Se implementará un adaptador inicial y, al menos, un adaptador fake determinista.

## 1.7 Flujos principales

### Ingreso y cualificación

```mermaid
sequenceDiagram
    autonumber
    participant Source as Canal
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Q as Redis/ARQ
    participant A1 as Agente 1
    participant LLM as LLM

    Source->>API: POST /leads + Idempotency-Key
    API->>DB: Crear lead + outbox
    API-->>Source: 201 Lead(status=NEW)
    DB-->>Q: Publicador outbox encola qualify
    Q->>A1: qualify_lead(lead_id)
    A1->>DB: Cargar ICP + contexto
    A1->>LLM: Solicitar salida estructurada
    LLM-->>A1: Score + factores + confianza
    A1->>A1: Validar esquema y políticas
    A1->>DB: Guardar qualification + ai_run
    A1->>DB: Actualizar prioridad/estado si aplica
```

### Análisis post-llamada

1. La API valida `tenant`, lead/deal, tipo, tamaño y procedencia del archivo.
2. El audio se guarda con cifrado y checksum; la URL no se confía como fuente permanente.
3. Un worker transcribe o normaliza la transcripción recibida.
4. Se redacta PII no necesaria antes de enviar texto al LLM, según política.
5. El agente calcula métricas deterministas donde sea posible y usa el LLM para extracción/feedback.
6. La salida se valida, se persiste y se notifica al vendedor.
7. Un gerente puede marcar el feedback como útil, incorrecto o revisado.

### Seguimiento por inactividad

1. El scheduler identifica deals elegibles mediante reglas por etapa y `last_meaningful_interaction_at`.
2. Un lock por `tenant_id + deal_id + rule_id` evita ejecuciones concurrentes.
3. El agente reúne contexto mínimo, consentimiento, zona horaria, quiet hours y frecuencia.
4. Genera un borrador estructurado.
5. La política determina `AUTO_SEND`, `REQUIRE_APPROVAL` o `BLOCK`.
6. El adaptador de canal envía con clave idempotente.
7. Se registra intento y estado del proveedor.
8. `last_meaningful_interaction_at` sólo cambia cuando existe una interacción real; el mero job no debe simular actividad del prospecto.

## 1.8 Especificación de agentes

### Contrato común

Todo agente implementa conceptualmente:

```python
from typing import Protocol, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class Agent(Protocol[InputT, OutputT]):
    name: str
    version: str

    async def run(
        self,
        input: InputT,
        *,
        tenant_id: str,
        correlation_id: str,
    ) -> OutputT: ...
```

Cada ejecución debe registrar:

- `agent_name`, `agent_version`, `prompt_version` y `policy_version`;
- IDs de tenant, lead, deal e interacción aplicables;
- hash de entrada y salida;
- modelo, proveedor, latencia, tokens y costo estimado;
- herramientas invocadas;
- resultado validado, confianza y motivos;
- decisión de política;
- error sanitizado y número de intento;
- timestamps y `correlation_id`.

Los prompts completos pueden contener PII y no deben almacenarse indiscriminadamente. Se guardará una versión redactada o cifrada de acuerdo con la política de retención.

### Agente 1: Prospector / Lead Scorer

**Objetivo:** convertir señales iniciales en una prioridad explicable y una siguiente acción, sin excluir automáticamente oportunidades por una inferencia opaca.

**Entradas:**

- lead y empresa;
- fuente, campaña y UTMs;
- mensaje inicial e interacciones disponibles;
- ICP y matriz de scoring del tenant;
- capacidad y especialidad de vendedores;
- señales de consentimiento y calidad de datos.

**Proceso híbrido:**

1. Validaciones deterministas y deduplicación.
2. Cálculo de sub-scores configurables: fit, intención, urgencia, autoridad, necesidad y presupuesto.
3. Extracción estructurada por LLM de señales no tabulares.
4. Combinación ponderada y calibrada.
5. Asignación de categoría y confianza.
6. Recomendación de vendedor; la asignación efectiva respeta reglas de capacidad.

**Salida mínima:**

- score 0-100;
- `HOT`, `WARM` o `COLD`;
- confianza 0-1;
- factores positivos/negativos;
- campos faltantes;
- resumen y siguiente acción;
- versión de reglas.

**Reglas iniciales configurables:**

| Categoría | Score | Acción por defecto |
|---|---:|---|
| HOT | 80-100 | Prioridad alta y SLA corto. |
| WARM | 50-79 | Nutrición o contacto estándar. |
| COLD | 0-49 | Revisión/nutrición; no descartar automáticamente. |

**Guardrails:**

- no inferir atributos sensibles;
- no penalizar por lenguaje, género, origen o discapacidad;
- no cambiar a `LOST` o `UNQUALIFIED` sin regla verificable o revisión;
- si confianza < 0.60, marcar `REVIEW_REQUIRED`;
- si el LLM falla, conservar el lead y aplicar scoring determinista, no un score arbitrario fijo.

### Agente 2: Coach de ventas / Analista de llamadas

**Objetivo:** transformar conversaciones en evidencia y recomendaciones privadas, accionables y medibles.

**Entradas:**

- audio o transcripción;
- idioma y participantes conocidos;
- lead, deal, etapa y objetivo de llamada;
- guion comercial y rúbrica del tenant;
- consentimiento y política de retención.

**Proceso:**

1. Verificar consentimiento, formato, checksum, duración y malware.
2. Transcribir y diarizar.
3. Calcular métricas objetivas: duración, turnos, silencios, ratio habla/escucha.
4. Extraer pain points, necesidades, preguntas, objeciones, compromisos y próximos pasos.
5. Evaluar contra una rúbrica versionada.
6. Generar feedback con referencias temporales a la conversación.

**Salida mínima:**

- estado de transcripción;
- ratio habla/escucha;
- sentimiento con advertencia de confianza;
- objeciones y respuesta observada;
- score por dimensión y score global 1-10;
- fortalezas, oportunidades y acciones;
- compromisos y fecha sugerida;
- citas breves con timestamps, sujetas a permisos.

**Guardrails:**

- coaching no se usa como única base para sanciones laborales;
- distinguir hecho observado de inferencia;
- no inventar citas ni próximos pasos;
- no exponer llamadas de un vendedor a otro sin rol;
- fallo de diarización reduce confianza y solicita revisión;
- audio no consentido se bloquea y registra sin procesar.

### Agente 3: Automatización de seguimiento / Marketing

**Objetivo:** mantener continuidad comercial con mensajes pertinentes, consentidos y no duplicados.

**Entradas:**

- deal, etapa y propietario;
- historial reciente y resumen aprobado;
- SLA y reglas de secuencia;
- canal, consentimiento, zona horaria y quiet hours;
- plantillas aprobadas y límites de frecuencia.

**Proceso:**

1. Evaluar elegibilidad.
2. Seleccionar objetivo de contacto y plantilla.
3. Generar personalización limitada a hechos existentes.
4. Validar tono, claims, longitud, PII y palabras prohibidas.
5. Aplicar política de aprobación.
6. Enviar o crear tarea/borrador.
7. Observar delivery y respuesta.

**Modos:**

| Modo | Uso |
|---|---|
| `SUGGEST_ONLY` | Crea borrador para el vendedor. |
| `REQUIRE_APPROVAL` | Encola aprobación antes de enviar. |
| `AUTO_SEND` | Envía sólo si todas las políticas son válidas. |
| `BLOCKED` | No envía y explica la regla incumplida. |

**Guardrails:**

- máximo configurable de mensajes por periodo;
- exclusión inmediata tras opt-out;
- quiet hours por zona horaria;
- no prometer descuentos, disponibilidad o condiciones no presentes;
- no enviar si existe una respuesta entrante posterior al snapshot usado;
- no duplicar ante reintentos;
- una falla final crea tarea humana y alerta, no un bucle infinito.

## 1.9 Modelo de datos

### Diagrama ER lógico

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : contains
    ORGANIZATIONS ||--o{ PIPELINES : configures
    PIPELINES ||--|{ PIPELINE_STAGES : contains
    ORGANIZATIONS ||--o{ LEADS : owns
    USERS ||--o{ LEADS : assigned
    LEADS ||--o{ DEALS : creates
    PIPELINE_STAGES ||--o{ DEALS : classifies
    USERS ||--o{ DEALS : owns
    LEADS ||--o{ INTERACTIONS : has
    DEALS ||--o{ INTERACTIONS : relates
    INTERACTIONS ||--o| CALL_ANALYSES : produces
    LEADS ||--o{ LEAD_QUALIFICATIONS : receives
    ORGANIZATIONS ||--o{ AGENT_CONFIGS : defines
    AGENT_CONFIGS ||--o{ AI_RUNS : executes
    DEALS ||--o{ FOLLOWUP_EXECUTIONS : triggers
    INTERACTIONS ||--o{ FOLLOWUP_EXECUTIONS : records
    ORGANIZATIONS ||--o{ WEBHOOK_EVENTS : receives
    ORGANIZATIONS ||--o{ AUDIT_LOGS : audits
```

### Entidades y reglas

| Entidad | Campos esenciales | Reglas |
|---|---|---|
| `organizations` | `id`, `name`, `slug`, `timezone`, `settings`, timestamps | `slug` único; raíz del aislamiento. |
| `users` | `id`, `organization_id`, `email`, `role`, `is_active` | email único por tenant; password gestionado por IdP/hash seguro. |
| `pipelines` | `id`, `organization_id`, `name`, `is_default` | un default por tenant. |
| `pipeline_stages` | `id`, `pipeline_id`, `name`, `position`, `sla_hours`, `terminal_type` | posición única; terminal `WON/LOST/NONE`. |
| `leads` | identidad, contacto, estado, score actual, owner, metadata | al menos un medio de contacto; dedupe normalizado por tenant. |
| `lead_qualifications` | score, categoría, confianza, factores, rule version, `ai_run_id` | historial inmutable; `leads` conserva proyección actual. |
| `deals` | lead, pipeline/stage, owner, value, currency, close date, activity timestamps | transición validada; dinero usa decimal. |
| `interactions` | direction, channel, content, media key, external IDs, occurred_at | único por tenant/proveedor/external ID. |
| `call_analyses` | interaction, transcript key, metrics, rubric version, scores | uno activo por versión; reprocesos conservan historial. |
| `agent_configs` | agent, version, mode, prompt ref, policy, budget | configuración versionada por tenant. |
| `ai_runs` | estado, contexto, output, tokens, cost, error, trace | append-only salvo transición de estado. |
| `followup_sequences` | etapas, delay, canal, plantilla, reglas | versionadas; activación explícita. |
| `followup_executions` | deal, sequence step, status, idempotency key, provider IDs | clave idempotente única. |
| `webhook_events` | provider, event ID, headers sanitizados, payload, status | dedupe antes de efectos. |
| `outbox_events` | aggregate, event type, payload, published_at | escrito en misma transacción del agregado. |
| `audit_logs` | actor, action, resource, before/after redactado, IP, trace | inmutable y con retención mayor. |

### Convenciones SQL

- UUIDv7 para IDs de negocio; no exponer secuencias internas.
- `TIMESTAMPTZ` en UTC; convertir a zona del tenant sólo en bordes.
- toda tabla de negocio incluye `organization_id`.
- índices compuestos comienzan por `organization_id`.
- soft delete sólo donde exista obligación de recuperación; auditoría nunca se borra por cascada.
- RLS en PostgreSQL es defensa adicional, no sustituto de autorización en servicio.
- embeddings referencian contenido y modelo; no mezclar dimensiones.

### Índices mínimos

```sql
CREATE UNIQUE INDEX uq_leads_tenant_phone
  ON leads (organization_id, normalized_phone)
  WHERE normalized_phone IS NOT NULL AND deleted_at IS NULL;

CREATE INDEX ix_deals_sla_scan
  ON deals (organization_id, stage_id, last_meaningful_interaction_at)
  WHERE status = 'OPEN';

CREATE UNIQUE INDEX uq_interactions_external
  ON interactions (organization_id, provider, external_reference_id)
  WHERE external_reference_id IS NOT NULL;

CREATE UNIQUE INDEX uq_webhook_provider_event
  ON webhook_events (organization_id, provider, external_event_id);

CREATE UNIQUE INDEX uq_followup_idempotency
  ON followup_executions (organization_id, idempotency_key);
```

## 1.10 Estados y consistencia

### Estados de un AI Run

`QUEUED -> RUNNING -> SUCCEEDED | FAILED | BLOCKED | CANCELLED`

- sólo un worker adquiere el run mediante lock/compare-and-set;
- un retry crea `attempt` nuevo bajo el mismo run lógico;
- `FAILED` es terminal cuando se agota la política;
- `BLOCKED` significa que una política evitó la ejecución, no un error técnico.

### Transiciones de deal

Las transiciones son configurables por pipeline. Toda transición registra actor, motivo y versión. Un agente puede recomendar una transición, pero sólo ejecutarla si una política explícita lo permite.

### Semántica de tiempo

- `created_at`: registro creado.
- `occurred_at`: evento ocurrió en la fuente.
- `received_at`: webhook recibido.
- `last_interaction_at`: cualquier interacción registrada.
- `last_meaningful_interaction_at`: contacto con valor comercial según regla; evita que jobs y notas técnicas reinicien el SLA.

## 1.11 Requisitos no funcionales

| Categoría | Requisito |
|---|---|
| Disponibilidad | API producción >= 99.5% mensual, excluyendo mantenimiento comunicado. |
| Latencia | p95 lecturas < 400 ms; comandos síncronos < 800 ms sin incluir jobs. |
| Webhooks | confirmar recepción válida < 2 s y procesar asíncronamente. |
| Scoring | 95% de runs finaliza < 60 s bajo carga objetivo. |
| Call analysis | 90% finaliza < duración del audio + 10 min. |
| Escalabilidad | escalar API y workers horizontalmente sin afinidad de sesión. |
| Consistencia | cero efectos duplicados por reintentos conocidos. |
| Recuperación | objetivo inicial RPO <= 15 min y RTO <= 4 h. |
| Seguridad | TLS, secretos fuera de imagen, RBAC, auditoría y cifrado de storage. |
| Privacidad | retención y borrado por tenant; exportación de datos; PII minimizada. |
| Accesibilidad | frontend objetivo WCAG 2.2 AA. |
| Compatibilidad | API versionada y cambios incompatibles sólo en versión mayor. |

## 1.12 Seguridad, privacidad y gobierno de IA

### Autenticación y autorización

- OIDC/OAuth2 recomendado; JWT de acceso corto con `sub`, `org_id`, `roles`, `aud`, `exp`.
- roles base: `ADMIN`, `MANAGER`, `SALES_REP`, `INTEGRATION`.
- permisos por recurso y tenant; no confiar en IDs del cliente.
- service accounts separadas para webhooks y workers.
- MFA para administradores cuando el IdP lo permita.

### Protección de integraciones

- verificar firma y timestamp de webhooks;
- limitar tamaño de body y content type;
- almacenar evento antes de procesarlo;
- rechazar replay fuera de ventana y deduplicar event ID;
- URLs firmadas con expiración para bucket;
- tokens por tenant cifrados mediante KMS/secret manager.

### Retención propuesta

| Dato | Retención inicial | Configurable |
|---|---:|---|
| Audio original | 90 días | Sí |
| Transcripción | 12 meses | Sí |
| Interacciones comerciales | Vigencia contractual + política legal | Sí |
| Prompt/output redactado | 90 días | Sí |
| Métricas agregadas | 24 meses | Sí |
| Auditoría de seguridad | 24 meses | Según regulación |

### Amenazas prioritarias

- prompt injection desde mensajes o transcripciones;
- cross-tenant data leakage;
- envío a destinatario incorrecto;
- webhooks falsificados o repetidos;
- URLs de audio maliciosas/SSRF;
- exposición de PII en logs;
- abuso de costos LLM;
- instrucciones del modelo que intenten saltar políticas.

Mitigaciones: allowlists de herramientas, fetcher seguro, validación estructurada, presupuestos, rate limits, políticas fuera del prompt, separación por tenant, logs redactados y pruebas adversariales.

## 1.13 Observabilidad y operación

### Logs estructurados

Campos mínimos: `timestamp`, `level`, `service`, `environment`, `organization_id` redactado/hash, `correlation_id`, `request_id`, `job_id`, `ai_run_id`, `event`, `duration_ms`, `status`, `error_code`.

No registrar tokens, contraseñas, audio, transcripciones completas ni payloads con PII sin redacción.

### Métricas

- request rate, error rate y duración por endpoint;
- profundidad/edad de cola, jobs exitosos/fallidos/reintentados;
- webhook duplicates, invalid signatures y processing lag;
- AI runs por agente/modelo/estado;
- tokens, costo, latencia, schema failures y fallback rate;
- mensajes enviados, bloqueados, entregados y respondidos;
- conversión por score/category y calidad de calibración.

### Alertas iniciales

- p95 5xx > 2% durante 5 min;
- job más antiguo > 5 min;
- webhook signature failures por encima de umbral;
- `FAILED` de un agente > 10% durante 15 min;
- presupuesto LLM diario >= 80%;
- error de entrega de canal > 10%;
- backup o restore test fallido.

---

# 2. ESPECIFICACIONES TÉCNICAS Y FUNCIONALES (SDK & API SPECS)

## 2.1 Convenciones API

- Base URL: `/api/v1`.
- JSON `application/json`; uploads mediante flujo presigned.
- timestamps ISO 8601 UTC.
- IDs UUID.
- `Authorization: Bearer <token>`.
- `X-Correlation-ID` aceptado o generado.
- `Idempotency-Key` obligatorio en creaciones con efectos externos.
- paginación cursor: `limit` (1-100) y `cursor`.
- filtros explícitos; orden estable por `created_at,id`.
- OpenAPI es fuente publicable del contrato; clientes se generan desde una versión etiquetada.

### Respuestas asíncronas

- `201 Created`: recurso persistido y disponible.
- `202 Accepted`: run/job creado; devuelve `operation_id` o `ai_run_id`.
- `200 OK`: consulta o comando completado.
- `204 No Content`: comando sin representación.

### Errores

```json
{
  "error": {
    "code": "LEAD_PHONE_INVALID",
    "message": "El teléfono no cumple el formato E.164.",
    "details": [
      {"field": "phone", "reason": "invalid_format"}
    ],
    "correlation_id": "01J4Z9D6RQ2K5Y7M8N9P0Q1R2S",
    "retryable": false
  }
}
```

| HTTP | Uso |
|---:|---|
| 400 | Payload semánticamente inválido. |
| 401 | Falta o falla autenticación. |
| 403 | Actor sin permiso. |
| 404 | Recurso inexistente dentro del tenant. |
| 409 | Conflicto, transición o idempotencia incompatible. |
| 413 | Archivo/payload excede límite. |
| 422 | Validación de esquema. |
| 429 | Rate limit o presupuesto. |
| 502/503 | Proveedor no disponible cuando no es posible diferir. |

## 2.2 Catálogo de endpoints

### Leads y cualificación

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/leads` | Crea/deduplica lead; opcionalmente encola scoring. |
| `GET` | `/leads` | Lista filtrada por owner, estado, categoría, fuente. |
| `GET` | `/leads/{lead_id}` | Detalle y proyección de cualificación actual. |
| `PATCH` | `/leads/{lead_id}` | Actualiza campos permitidos con control de versión. |
| `POST` | `/leads/{lead_id}/qualifications` | Inicia recualificación; `202`. |
| `GET` | `/leads/{lead_id}/qualifications` | Historial explicable. |
| `POST` | `/leads/{lead_id}/assignments` | Asigna owner con auditoría. |

### Deals y pipeline

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/deals` | Crea oportunidad. |
| `GET` | `/deals` | Lista por etapa, owner, SLA o actividad. |
| `GET` | `/deals/{deal_id}` | Detalle consolidado. |
| `POST` | `/deals/{deal_id}/transitions` | Cambia etapa con motivo y control de versión. |
| `POST` | `/deals/{deal_id}/followups` | Crea run manual de seguimiento. |
| `GET` | `/deals/{deal_id}/followups` | Historial de borradores/envíos. |

### Interacciones y coaching

| Método | Ruta | Resultado |
|---|---|---|
| `POST` | `/interactions` | Registra mensaje, email, nota o metadato de llamada. |
| `POST` | `/uploads/presign` | URL firmada para audio/adjunto. |
| `POST` | `/calls` | Registra audio/transcripción y encola análisis; `202`. |
| `GET` | `/calls/{interaction_id}/analysis` | Estado y análisis autorizado. |
| `POST` | `/calls/{interaction_id}/analysis/retry` | Reprocesa con nueva versión. |
| `GET` | `/coaching/users/{user_id}/insights` | Agregados autorizados; no expone audio por defecto. |

### Agentes y operaciones

| Método | Ruta | Resultado |
|---|---|---|
| `GET` | `/ai-runs/{ai_run_id}` | Estado, salida validada y telemetría permitida. |
| `POST` | `/ai-runs/{ai_run_id}/cancel` | Cancela si aún es cancelable. |
| `GET` | `/agent-configs` | Configuración efectiva por tenant. |
| `PUT` | `/agent-configs/{agent_name}` | Nueva versión de configuración. |
| `POST` | `/approvals/{approval_id}/approve` | Aprueba acción pendiente. |
| `POST` | `/approvals/{approval_id}/reject` | Rechaza con motivo. |

### Webhooks

| Método | Ruta | Seguridad |
|---|---|---|
| `POST` | `/webhooks/chatwoot` | firma/token + dedupe event ID. |
| `POST` | `/webhooks/whatsapp` | verificación Meta + firma. |
| `GET` | `/webhooks/whatsapp` | challenge de suscripción. |
| `POST` | `/webhooks/telephony/{provider}` | firma específica + allowlist. |

## 2.3 Contratos Pydantic v2

```python
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    model_validator,
)

E164 = Annotated[
    str,
    StringConstraints(pattern=r"^\+[1-9]\d{7,14}$", min_length=9, max_length=16),
]
TrackingCode = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Za-z0-9]{8,12}$"),
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class LeadCategory(StrEnum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"


class RunStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class LeadCreateRequest(StrictModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: E164 | None = None
    company_name: str | None = Field(default=None, max_length=150)
    initial_message: str | None = Field(default=None, max_length=10_000)
    source: str = Field(min_length=2, max_length=50)
    tracking_code: TrackingCode | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    qualify_async: bool = True

    @model_validator(mode="after")
    def require_contact(self):
        if self.email is None and self.phone is None:
            raise ValueError("email o phone es obligatorio")
        return self


class LeadResponse(StrictModel):
    id: UUID
    status: str
    score: int | None = Field(default=None, ge=0, le=100)
    category: LeadCategory | None = None
    qualification_status: RunStatus | None = None
    created_at: datetime
    version: int


class QualificationRequest(StrictModel):
    reason: Literal["NEW_LEAD", "DATA_CHANGED", "MANUAL", "SCHEDULED"]
    force: bool = False


class QualificationResult(StrictModel):
    lead_id: UUID
    score: int = Field(ge=0, le=100)
    category: LeadCategory
    confidence: float = Field(ge=0, le=1)
    positive_factors: list[str] = Field(max_length=20)
    negative_factors: list[str] = Field(max_length=20)
    missing_fields: list[str] = Field(max_length=20)
    summary: str = Field(max_length=2_000)
    suggested_action: str = Field(max_length=1_000)
    rules_version: str
    review_required: bool


class CallCreateRequest(StrictModel):
    lead_id: UUID
    deal_id: UUID | None = None
    sales_rep_id: UUID
    audio_object_key: str | None = Field(default=None, max_length=500)
    transcript: str | None = Field(default=None, max_length=500_000)
    language: str = Field(default="es", min_length=2, max_length=10)
    duration_seconds: int | None = Field(default=None, gt=0, le=21_600)
    consent_confirmed: bool

    @model_validator(mode="after")
    def require_audio_or_transcript(self):
        if self.transcript is None and self.audio_object_key is None:
            raise ValueError("audio_object_key o transcript es obligatorio")
        return self


class Objection(StrictModel):
    text: str = Field(max_length=1_000)
    rep_response: str | None = Field(default=None, max_length=2_000)
    effectiveness_score: int | None = Field(default=None, ge=1, le=10)
    evidence_start_seconds: int | None = Field(default=None, ge=0)
    confidence: float = Field(ge=0, le=1)


class CallAnalysisResult(StrictModel):
    interaction_id: UUID
    talk_ratio_rep: float | None = Field(default=None, ge=0, le=1)
    sentiment: str | None = None
    objections: list[Objection]
    performance_score: int = Field(ge=1, le=10)
    strengths: list[str]
    improvement_areas: list[str]
    actionable_feedback: list[str]
    next_steps: list[str]
    confidence: float = Field(ge=0, le=1)
    review_required: bool


class FollowUpRequest(StrictModel):
    channel: Literal["WHATSAPP", "EMAIL"]
    mode: Literal["SUGGEST_ONLY", "REQUIRE_APPROVAL", "AUTO_SEND"] | None = None
    context_override: str | None = Field(default=None, max_length=2_000)
    expected_deal_version: int


class FollowUpResult(StrictModel):
    deal_id: UUID
    execution_id: UUID
    policy_decision: Literal[
        "SUGGEST_ONLY", "REQUIRE_APPROVAL", "AUTO_SEND", "BLOCKED"
    ]
    message: str | None = Field(default=None, max_length=4_096)
    status: str
    blocked_reasons: list[str] = Field(default_factory=list)
    external_message_id: str | None = None
    created_at: datetime


class DealTransitionRequest(StrictModel):
    to_stage_id: UUID
    reason: str = Field(min_length=3, max_length=1_000)
    expected_version: int


class DealMoney(StrictModel):
    value: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    currency: Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
```

**Nota de implementación:** el fragmento ilustra el contrato y no sustituye las pruebas del esquema.

## 2.4 SDK interno

La aplicación debe consumir puertos internos para mantener el dominio aislado:

```python
from typing import Protocol

class LLMPort(Protocol):
    async def generate_structured(
        self,
        *,
        schema: type[BaseModel],
        messages: list[dict[str, str]],
        model: str,
        timeout_seconds: float,
        trace_context: dict[str, str],
    ) -> BaseModel: ...


class SpeechToTextPort(Protocol):
    async def transcribe(
        self,
        *,
        object_key: str,
        language: str,
        diarize: bool,
    ) -> "TranscriptResult": ...


class MessagingPort(Protocol):
    async def send(
        self,
        *,
        recipient: str,
        content: str,
        idempotency_key: str,
        context: "ExternalContext",
    ) -> "DeliveryReceipt": ...


class ObjectStoragePort(Protocol):
    async def create_upload_url(
        self, *, key: str, content_type: str, expires_seconds: int
    ) -> str: ...


class AgentClient:
    async def qualify_lead(self, lead_id: UUID) -> UUID:
        """Devuelve ai_run_id."""

    async def analyze_call(self, interaction_id: UUID) -> UUID:
        """Devuelve ai_run_id."""

    async def trigger_followup(self, deal_id: UUID) -> UUID:
        """Devuelve execution_id."""
```

### Política de compatibilidad

- SDK `1.x` es compatible con API `/v1`.
- nuevos campos de respuesta son aditivos.
- campos eliminados requieren deprecación documentada.
- enums no se amplían sin clientes tolerantes o versión nueva.
- cada release publica OpenAPI y changelog.

## 2.5 Contexto y preservación de datos en pasarelas

### Sobre interno normalizado

```json
{
  "schema_version": "1.0",
  "event_id": "01J4Z9RN3T3Q5K5F4T7Q8V9W0X",
  "event_type": "interaction.message.created",
  "occurred_at": "2026-07-24T18:20:11Z",
  "received_at": "2026-07-24T18:20:12Z",
  "organization_id": "0190d0cc-b12d-7fab-a0d1-94b9a706a680",
  "correlation_id": "01J4Z9RQVDP5M0PR9PQFX2D1Z4",
  "source": {
    "provider": "CHATWOOT",
    "account_id": "42",
    "inbox_id": "7",
    "conversation_id": "84920",
    "message_id": "991823"
  },
  "references": {
    "lead_id": "0190d0dc-59c8-7d94-bdd7-37725b842e01",
    "deal_id": "0190d0e4-ccea-7384-96db-aa9d42918e8f",
    "user_id": null,
    "tracking_code": "AGQ8821X"
  },
  "message": {
    "direction": "INBOUND",
    "content": "Me interesa agendar la demo para el jueves",
    "sender": "+5215512345678"
  },
  "raw_payload_object_key": "webhooks/2026/07/24/01J4Z9RN.json"
}
```

### Reglas de mapeo

1. Conservar IDs externos como strings; no asumir que son enteros.
2. Nunca usar teléfono como único ID permanente.
3. Guardar `occurred_at` y `received_at`.
4. Persistir el payload raw cifrado sólo durante la ventana de diagnóstico.
5. Extraer referencias de atributos personalizados cuando existan; si no, resolver por tabla de mapeo.
6. Si dos candidatos coinciden, no adivinar: enviar a conciliación.
7. Responder rápido al proveedor y procesar después.
8. Toda salida lleva IDs internos en metadata compatible con el canal.

### Idempotencia

- webhook: `organization_id + provider + external_event_id`;
- mensaje: `organization_id + provider + external_message_id`;
- creación API: hash de `Idempotency-Key + actor + route`;
- seguimiento: `tenant + deal + sequence_version + step + eligibility_window`;
- la misma key con payload distinto responde `409 IDEMPOTENCY_KEY_REUSED`.

## 2.6 Eventos de dominio

| Evento | Productor | Consumidores |
|---|---|---|
| `lead.created.v1` | CRM Core | Agent 1, notifications |
| `lead.qualified.v1` | Agent 1 | assignment, reporting |
| `deal.stage_changed.v1` | CRM Core | Agent 3, reporting |
| `interaction.created.v1` | Interactions | Agent 1/3, timeline |
| `call.ready_for_analysis.v1` | Interactions | Agent 2 |
| `call.analyzed.v1` | Agent 2 | coaching, notifications |
| `deal.followup_due.v1` | Scheduler | Agent 3 |
| `followup.sent.v1` | Integrations | CRM timeline, reporting |
| `followup.failed.v1` | Integrations | tasks, alerts |

Cada evento incluye `event_id`, `event_type`, `schema_version`, `aggregate_id`, `organization_id`, `occurred_at`, `correlation_id` y payload mínimo.

---

# 3. CRITERIOS DE ACEPTACIÓN E HISTORIAS DE USUARIO (BDD)

Los escenarios son ejecutables conceptualmente mediante `pytest-bdd` o Behave. Los valores de SLA son objetivos y deben parametrizarse por entorno.

## 3.1 Agente 1: cualificación

```gherkin
# language: es
Característica: Cualificación automática y explicable de leads
  Como gerente de ventas
  Quiero priorizar leads usando reglas e IA
  Para atender primero las oportunidades con mayor intención sin perder trazabilidad

  Antecedentes:
    Dado un tenant activo con una matriz ICP versión "icp-3"
    Y un umbral HOT de 80 y WARM de 50

  Escenario: Lead de alta intención se cualifica como HOT
    Dado un lead nuevo con teléfono E.164 válido
    Y el mensaje indica presupuesto, autoridad y necesidad dentro de 30 días
    Cuando se publica el evento "lead.created.v1"
    Entonces se crea exactamente un AI Run del Agente 1
    Y el AI Run termina en "SUCCEEDED"
    Y la cualificación contiene un score entre 80 y 100
    Y la categoría es "HOT"
    Y incluye factores, confianza y versión "icp-3"
    Y se crea una tarea comercial dentro del SLA configurado

  Escenario: Reintento del mismo webhook no duplica el lead ni el scoring
    Dado un evento externo ya procesado con ID "evt-9001"
    Cuando el mismo proveedor entrega nuevamente "evt-9001"
    Entonces el API responde exitosamente
    Y existe un solo lead
    Y existe un solo AI Run originado por ese evento

  Escenario: Baja confianza exige revisión humana
    Dado que faltan empresa, necesidad y urgencia
    Y el resultado del scoring tiene confianza 0.42
    Cuando el Agente 1 valida la salida
    Entonces la cualificación se guarda con "review_required" verdadero
    Y el lead no cambia automáticamente a "UNQUALIFIED"
    Y se crea una tarea de revisión

  Escenario: El proveedor LLM falla y se conserva el flujo
    Dado que el proveedor LLM excede su timeout
    Cuando el worker agota los reintentos permitidos
    Entonces se aplica únicamente el score determinista disponible
    Y el resultado indica degradación y revisión requerida
    Y se registra el error sin contenido personal en logs
    Y el lead permanece visible y asignable

  Esquema del escenario: Validación del código de tracking
    Cuando se intenta crear un lead con tracking_code "<codigo>"
    Entonces la respuesta HTTP es "<estado>"

    Ejemplos:
      | codigo       | estado |
      | ABCD1234     | 201    |
      | ABCDEFGH1234 | 201    |
      | ABC123       | 422    |
      | ABCD-1234    | 422    |
      | ABCDEFGH12345| 422    |
```

## 3.2 Agente 2: análisis y coaching

```gherkin
# language: es
Característica: Coaching post-llamada basado en evidencia
  Como vendedor
  Quiero recibir feedback privado y accionable después de una llamada
  Para mejorar mi siguiente conversación

  Escenario: Audio consentido produce análisis con evidencias
    Dado un audio válido de 18 minutos con consentimiento confirmado
    Y una rúbrica comercial versión "sales-2"
    Cuando se registra la llamada
    Entonces el API responde 202 con un ai_run_id
    Y el audio se procesa de forma asíncrona
    Y el resultado incluye ratio habla/escucha, objeciones y próximos pasos
    Y cada objeción reportada tiene confianza y referencia temporal cuando existe
    Y el vendedor propietario puede consultar el resultado

  Escenario: Llamada sin consentimiento no se procesa
    Dado un audio con "consent_confirmed" falso
    Cuando se intenta registrar la llamada
    Entonces el sistema rechaza el análisis
    Y no envía audio ni texto a proveedores de IA
    Y registra el bloqueo de política

  Escenario: Diarización incierta evita afirmaciones categóricas
    Dado que el proveedor no separa de forma confiable a vendedor y prospecto
    Cuando el Agente 2 genera el análisis
    Entonces "review_required" es verdadero
    Y las métricas dependientes de hablante son nulas o marcadas como inciertas
    Y no se inventan citas atribuidas al vendedor

  Escenario: Un vendedor no accede al audio de otro equipo
    Dado un vendedor autenticado del equipo A
    Y una llamada propiedad del equipo B
    Cuando solicita el análisis por ID
    Entonces la respuesta es 404 o 403 según la política de ocultación
    Y no se filtran metadatos del recurso

  Escenario: Reprocesamiento conserva historial
    Dado un análisis completado con rúbrica "sales-1"
    Cuando un gerente autorizado reprocesa con "sales-2"
    Entonces se crea un nuevo AI Run
    Y el análisis anterior permanece auditable
    Y la proyección activa apunta al resultado nuevo
```

## 3.3 Agente 3: seguimiento

```gherkin
# language: es
Característica: Seguimiento automatizado seguro por inactividad
  Como responsable comercial
  Quiero recuperar oportunidades inactivas
  Para mantener continuidad sin enviar spam ni mensajes duplicados

  Antecedentes:
    Dado una regla activa para deals "IN_NEGOTIATION" después de 72 horas
    Y un máximo de 2 mensajes de seguimiento por 7 días

  Escenario: Deal elegible crea un seguimiento por WhatsApp
    Dado un deal abierto cuya última interacción significativa ocurrió hace 73 horas
    Y el contacto tiene consentimiento vigente para WhatsApp
    Y la hora local está fuera de quiet hours
    Cuando el scheduler evalúa el deal
    Entonces se crea una sola ejecución de seguimiento
    Y el mensaje usa únicamente hechos presentes en el CRM
    Y la política determina "AUTO_SEND"
    Y el adaptador envía con una clave idempotente
    Y la interacción saliente conserva el ID externo

  Escenario: Opt-out bloquea cualquier envío
    Dado un contacto que respondió "STOP"
    Cuando el scheduler evalúa su deal
    Entonces la decisión es "BLOCKED"
    Y el motivo incluye "CONSENT_REVOKED"
    Y no se invoca la API de WhatsApp

  Escenario: Quiet hours difiere el envío
    Dado un deal elegible cuyo contacto está en horario restringido
    Cuando el scheduler evalúa el deal
    Entonces no se envía el mensaje
    Y se programa para la siguiente ventana permitida

  Escenario: Respuesta reciente invalida un borrador pendiente
    Dado un borrador creado para aprobación
    Y el prospecto responde antes de que el vendedor lo apruebe
    Cuando el vendedor intenta aprobarlo
    Entonces la aprobación responde 409
    Y el borrador queda "STALE"
    Y no se envía el mensaje

  Escenario: Timeout del proveedor no duplica mensajes
    Dado que WhatsApp acepta un mensaje pero la respuesta HTTP expira
    Cuando el worker reintenta con la misma clave idempotente
    Entonces existe a lo sumo un mensaje en el proveedor
    Y una sola interacción saliente en el CRM

  Escenario: Límite de frecuencia bloquea el tercer contacto
    Dado que se enviaron 2 seguimientos en los últimos 7 días
    Cuando el scheduler vuelve a evaluar el deal
    Entonces la decisión es "BLOCKED"
    Y el motivo incluye "FREQUENCY_CAP_REACHED"
```

## 3.4 CRM, webhooks y seguridad

```gherkin
# language: es
Característica: Integridad y aislamiento de la plataforma

  Escenario: Un ID de otro tenant no expone datos
    Dado un usuario autenticado del tenant A
    Y un lead existente en el tenant B
    Cuando solicita el lead por su UUID
    Entonces no recibe datos del lead
    Y el intento queda disponible para auditoría de seguridad

  Escenario: Firma inválida de Chatwoot
    Dado un payload con firma inválida
    Cuando llega al webhook de Chatwoot
    Entonces el API responde 401
    Y no crea interacciones ni jobs

  Escenario: Evento válido se confirma antes del procesamiento largo
    Dado un webhook firmado y no duplicado
    Cuando el API lo recibe
    Entonces persiste el evento
    Y responde dentro de 2 segundos
    Y procesa la normalización en background

  Escenario: Conflicto optimista evita sobrescribir un deal
    Dado un deal en versión 7
    Y otro actor lo actualiza a versión 8
    Cuando un cliente intenta cambiar la etapa esperando versión 7
    Entonces el API responde 409
    Y conserva la versión 8
```

## 3.5 Criterio transversal de terminado

Una historia está terminada sólo si:

- criterios Gherkin están automatizados o existe justificación documentada;
- pruebas unitarias, integración y contrato requeridas pasan;
- migración tiene upgrade y estrategia de rollback;
- permisos y aislamiento por tenant fueron probados;
- logs, métricas y alertas relevantes existen;
- errores no filtran secretos/PII;
- documentación OpenAPI y este contrato están alineados;
- `git diff --check`, lint, tipos y cobertura pasan;
- existe evidencia en staging del camino productivo.

---

# 4. PLAN DE PRUEBAS Y CALIDAD DE CÓDIGO (TDD)

## 4.1 Ciclo TDD

Para cada regla:

1. **Red:** escribir una prueba que falle por el comportamiento faltante.
2. **Green:** implementar el mínimo comportamiento.
3. **Refactor:** mejorar diseño manteniendo verde.
4. **Contract:** verificar API/evento contra esquema.
5. **Productive path:** demostrar el flujo desde entrada real hasta efecto observable.

No se aceptará como prueba suficiente un test que invoque sólo un helper si el riesgo está en endpoint, transacción, worker o integración.

## 4.2 Pirámide y cobertura

| Capa | Herramientas | Objetivo |
|---|---|---|
| Unitarias | pytest, hypothesis | reglas, políticas, schemas, scoring, parsers. |
| Componentes | pytest + fakes | servicios con puertos/adaptadores simulados. |
| Integración | TestClient/httpx, PostgreSQL/Redis/MinIO testcontainers | endpoints, repositorios, outbox, jobs. |
| Contrato | OpenAPI validation, JSON Schema, fixtures de proveedores | compatibilidad interna/externa. |
| E2E | stack staging + sandbox de proveedor | caminos productivos críticos. |
| No funcional | k6/Locust, OWASP tooling, restore drills | carga, seguridad y recuperación. |

Umbrales iniciales:

- cobertura global >= 85%;
- dominios y políticas de agentes >= 95%;
- branches >= 80%;
- 100% de transiciones críticas, validaciones de autorización e idempotencia;
- no usar cobertura como sustituto de calidad de assertions.

## 4.3 Organización de tests

```text
tests/
├── unit/
│   ├── crm/
│   ├── agents/
│   ├── policies/
│   └── schemas/
├── component/
│   ├── services/
│   └── workers/
├── integration/
│   ├── api/
│   ├── repositories/
│   ├── outbox/
│   └── webhooks/
├── contract/
│   ├── openapi/
│   ├── chatwoot/
│   ├── whatsapp/
│   └── llm/
├── bdd/
│   ├── features/
│   └── steps/
├── e2e/
└── fixtures/
```

## 4.4 Matriz de pruebas por riesgo

| ID | Riesgo | Prueba obligatoria |
|---|---|---|
| T-01 | Duplicar lead por webhook | dos entregas concurrentes, un lead/run. |
| T-02 | Fuga cross-tenant | acceso por ID, listados, exports y background jobs. |
| T-03 | Output LLM inválido | JSON truncado, enum nuevo, campos extra y texto no JSON. |
| T-04 | Hallucination en follow-up | facts allowlist y validador de claims. |
| T-05 | Mensaje duplicado | timeout ambiguo + retry con misma idempotency key. |
| T-06 | Pérdida de evento | commit de negocio + outbox atómico; caída antes/después de publish. |
| T-07 | SSRF por audio URL | IP privada, redirect, esquema no HTTPS, host no permitido. |
| T-08 | PII en logs | captura de logs y assertions de redacción. |
| T-09 | Race de aprobación | respuesta entrante entre draft y approve produce `STALE`. |
| T-10 | Quiet hours erróneas | DST, zonas horarias y límites de día. |
| T-11 | Score no calibrado | dataset versionado y métricas por cohortes. |
| T-12 | Costo fuera de control | budget limiter y 429/blocked al alcanzar cuota. |

## 4.5 Fakes, mocks y stubs

### Principios

- mockear en el puerto usado por el servicio, no dentro del SDK del proveedor;
- fakes deterministas y sin red en unit/component tests;
- fixtures versionadas y sanitizadas de payloads reales;
- contract tests detectan cambios de proveedor;
- sandbox externo sólo en suite separada, con presupuesto y credenciales de CI protegidas;
- congelar tiempo para SLA, quiet hours y backoff.

```python
class FakeLLM:
    def __init__(self, responses: list[BaseModel | Exception]):
        self.responses = responses
        self.calls: list[dict] = []

    async def generate_structured(self, **kwargs):
        self.calls.append(kwargs)
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class FakeMessaging:
    def __init__(self):
        self.sent_by_key: dict[str, DeliveryReceipt] = {}

    async def send(self, *, idempotency_key: str, **kwargs):
        if idempotency_key not in self.sent_by_key:
            self.sent_by_key[idempotency_key] = DeliveryReceipt(
                external_message_id=f"fake-{len(self.sent_by_key) + 1}",
                status="ACCEPTED",
            )
        return self.sent_by_key[idempotency_key]
```

### Fallas simuladas

- connect/read timeout;
- HTTP 429 con `Retry-After`;
- 500/502/503/504;
- respuesta exitosa tardía;
- JSON/schema inválido;
- stream interrumpido;
- Redis temporalmente no disponible;
- deadlock/transacción abortada;
- objeto de audio ausente o checksum diferente;
- webhook duplicado, desordenado y con timestamp antiguo.

## 4.6 Ejemplos TDD

```python
@pytest.mark.asyncio
async def test_low_confidence_never_auto_disqualifies(
    lead_factory, qualification_service, fake_llm
):
    lead = await lead_factory(status="NEW")
    fake_llm.responses.append(
        QualificationResult(
            lead_id=lead.id,
            score=22,
            category="COLD",
            confidence=0.41,
            positive_factors=[],
            negative_factors=["No hay intención explícita"],
            missing_fields=["need", "timing", "budget"],
            summary="Información insuficiente.",
            suggested_action="Solicitar contexto.",
            rules_version="icp-3",
            review_required=True,
        )
    )

    await qualification_service.qualify(lead.id)

    refreshed = await qualification_service.get_lead(lead.id)
    assert refreshed.status != "UNQUALIFIED"
    assert refreshed.review_required is True


@pytest.mark.asyncio
async def test_retry_after_ambiguous_timeout_sends_once(
    followup_service, fake_messaging, eligible_deal
):
    key = followup_service.idempotency_key(eligible_deal, step=1)
    fake_messaging.raise_after_accept_once = True

    await followup_service.execute_with_retry(eligible_deal.id)

    assert list(fake_messaging.sent_by_key) == [key]
    assert await followup_service.count_interactions(eligible_deal.id) == 1
```

## 4.7 Casos de borde

### Datos y formatos

- `tracking_code`: sólo alfanumérico ASCII, 8-12 caracteres.
- teléfono: E.164, `+` y 8-15 dígitos; normalización antes de dedupe.
- nombres Unicode y dobles apellidos.
- email con mayúsculas y alias.
- mensajes vacíos, 10k caracteres, emojis, RTL y contenido HTML.
- montos con moneda distinta y precisión decimal.
- timestamps futuros, antiguos, DST y sin timezone.

### IA

- salida vacía, parcial o con campos extra;
- score fuera de rango;
- explicación contradictoria con score;
- prompt injection en mensaje/transcripción;
- contexto mayor a ventana;
- modelo no disponible;
- cambio de versión de modelo;
- embeddings con dimensión incorrecta;
- baja confianza y falta de evidencia.

### Integraciones

- firma inválida;
- duplicados y orden invertido;
- proveedor acepta pero responde timeout;
- 429 con y sin `Retry-After`;
- media expirada;
- conversación externa reasignada;
- contacto fusionado;
- delivery/read receipts antes del ack interno.

### Fallbacks

| Falla | Comportamiento |
|---|---|
| LLM Agente 1 | score determinista + revisión; no perder lead. |
| STT | aceptar transcripción manual o crear tarea; no inventar análisis. |
| LLM Agente 2 | conservar transcripción/métricas objetivas; marcar pendiente. |
| LLM Agente 3 | usar plantilla aprobada sin personalización o requerir humano según política. |
| WhatsApp/Chatwoot | retry acotado; luego tarea/alerta, preservando idempotencia. |
| Redis | API persiste comando/outbox; publisher recupera al restablecerse. |
| Bucket | rechazar run con error recuperable y no enviar URL rota al proveedor. |

## 4.8 Reintentos y timeouts

Valores iniciales, configurables:

- HTTP connect: 3 s;
- HTTP read LLM/STT: por operación, máximo explícito;
- webhook response: 2 s;
- retries: sólo errores transitorios y operaciones idempotentes;
- backoff exponencial con jitter, por ejemplo 2 s, 8 s, 32 s;
- respetar `Retry-After`;
- circuit breaker por proveedor;
- dead-letter o estado final visible tras agotar intentos.

Nunca reintentar automáticamente errores 400/401/403/404/422 ni violaciones de política.

## 4.9 Calidad estática y CI

Pipeline mínimo:

```bash
uv sync --frozen
uv run ruff format --check .
uv run ruff check .
uv run mypy app
uv run pytest tests/unit tests/component -q \
  --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=85
uv run pytest tests/integration tests/contract -q
uv run pytest tests/bdd -q
alembic upgrade head
alembic downgrade -1
git diff --check
```

En pull requests:

- escaneo de secretos;
- análisis de dependencias y SBOM;
- build de imagen;
- migraciones en BD efímera;
- pruebas de seguridad/tenant;
- OpenAPI diff para cambios incompatibles;
- no se requieren credenciales reales para la suite estándar.

## 4.10 Pruebas no funcionales

### Carga inicial

Perfil de referencia a validar con negocio:

- 50 req/s de lectura;
- 10 req/s de escritura;
- ráfaga de 100 webhooks/s durante 1 min;
- 1,000 deals evaluados por scheduler por minuto;
- 20 análisis de audio concurrentes por worker pool controlado.

### Seguridad

- OWASP API Top 10;
- autorización por objeto;
- fuzz de uploads/webhooks;
- SSRF;
- replay;
- rate limiting;
- secret scanning;
- dependencia vulnerable;
- prompt injection y data exfiltration.

### Recuperación

Trimestralmente:

1. restaurar backup en entorno aislado;
2. validar checksums y migraciones;
3. ejecutar smoke tests;
4. medir RPO/RTO;
5. documentar resultado y remediación.

---

# 5. PLAN DE EJECUCIÓN Y TAREAS (ROADMAP DE DESARROLLO)

## 5.1 Estrategia de entrega

Se propone un MVP en cuatro sprints de dos semanas, precedido por una Semana 0 de decisiones. Las fechas exactas se fijan al aprobar alcance, equipo e integraciones. El objetivo es entregar verticales utilizables, no capas técnicas aisladas.

### Semana 0: Descubrimiento y decisiones

**Producto**

- validar personas: administrador, gerente, vendedor y operador;
- mapear pipeline real, ICP, SLA y guion;
- seleccionar caso piloto y métricas base;
- confirmar consentimientos, jurisdicción y políticas de contacto;
- definir qué acciones son automáticas.

**Arquitectura**

- ADR de tenancy, autenticación, LLM, STT, WhatsApp/Chatwoot y hosting;
- threat model;
- contratos sandbox con proveedores;
- presupuesto de IA;
- modelo de ownership operativo.

**Salida:** backlog priorizado, ADRs aceptados, dataset de prueba sanitizado y Definition of Ready.

## 5.2 WBS por sprint

### Sprint 1: Foundation + CRM vertical

**Objetivo demostrable:** un usuario autorizado crea y consulta un lead aislado por tenant; el evento queda auditable.

1. Repositorio, `pyproject`, CI y convenciones.
2. FastAPI, settings por entorno y health endpoints.
3. PostgreSQL, Alembic, organizaciones, usuarios y RBAC.
4. Pipelines, etapas, leads, deals e interacciones.
5. Redis/ARQ, outbox y publisher.
6. Logs JSON, correlation IDs y métricas base.
7. OpenAPI, errores e idempotencia.
8. Tests unitarios/integración y primer flujo E2E.

**Criterio de salida:** creación/dedupe de lead, aislamiento tenant, outbox recuperable y despliegue staging.

### Sprint 2: Agente 1 + ingesta de canales

**Objetivo demostrable:** un lead real/sandbox entra por webhook, se cualifica y aparece priorizado con explicación.

1. Configuración ICP versionada.
2. Motor de scoring determinista.
3. `LLMPort`, fake y adaptador inicial.
4. Agente 1 y validación estructurada.
5. Webhooks Chatwoot/WhatsApp, firma y dedupe.
6. Reglas de asignación y tareas.
7. Métricas de scoring, costo y latencia.
8. BDD de cualificación, fallas y reintentos.

**Criterio de salida:** flujo productivo sandbox desde webhook hasta cualificación consultable.

### Sprint 3: Agente 2 + coaching

**Objetivo demostrable:** una llamada consentida produce un reporte privado con evidencias.

1. Bucket, presigned upload, checksum y límites.
2. Ingesta de telefonía/reunión priorizada.
3. `SpeechToTextPort`, fake y adaptador.
4. Transcripción, diarización y métricas objetivas.
5. Rúbrica de coaching versionada.
6. Agente 2 y referencias temporales.
7. Autorización de reportes y feedback de utilidad.
8. Retención/borrado y pruebas de privacidad.

**Criterio de salida:** flujo productivo de audio/transcripción hasta coaching visible.

### Sprint 4: Agente 3 + endurecimiento + piloto

**Objetivo demostrable:** un deal elegible genera seguimiento seguro y trazable, con aprobación o autoenvío según política.

1. Secuencias, scheduler y elegibilidad.
2. Consentimiento, quiet hours y frequency cap.
3. Generación/validación de mensajes.
4. Aprobaciones y detección de borrador obsoleto.
5. Adaptador de envío y receipts.
6. Dashboards/alertas operativas.
7. Carga, seguridad, restore drill y runbooks.
8. UAT, capacitación, piloto y plan de rollback.

**Criterio de salida:** casos BDD críticos verdes y evidencia de piloto controlado.

## 5.3 Dependencias y camino crítico

```mermaid
flowchart LR
    Decisions["ADRs + políticas"] --> Foundation["Tenancy + CRM Core"]
    Foundation --> Events["Outbox + jobs"]
    Events --> A1["Agente 1"]
    Foundation --> Storage["Bucket + consentimiento"]
    Storage --> A2["Agente 2"]
    Foundation --> Channels["Chatwoot / WhatsApp"]
    Events --> A3["Agente 3"]
    Channels --> A3
    A1 --> Pilot["Piloto"]
    A2 --> Pilot
    A3 --> Pilot
```

Camino crítico: decisiones de integración y consentimiento -> foundation multi-tenant -> eventos confiables -> adaptadores -> agentes -> piloto.

## 5.4 Backlog priorizado

### P0 - Bloquea piloto

- tenancy/RBAC;
- leads/deals/interactions;
- outbox/idempotencia;
- configuración y guardrails;
- webhooks firmados;
- Agente 1;
- ingesta/análisis de llamada;
- seguimiento con aprobación;
- auditoría y observabilidad;
- backups y rollback.

### P1 - Mejora operación

- autoasignación avanzada;
- autoenvío de bajo riesgo;
- dashboards de coaching;
- embeddings/búsqueda semántica;
- evaluación y calibración continua;
- email como canal adicional.

### P2 - Escala

- SSO empresarial;
- data warehouse;
- marketplace de integraciones;
- experimentación A/B;
- recomendaciones cross-tenant sólo con datos agregados y privacidad aprobada;
- extracción de módulos a servicios si métricas lo justifican.

## 5.5 Roles sugeridos

| Rol | Responsabilidad |
|---|---|
| Product Lead | alcance, métricas, backlog, UAT y adopción. |
| Tech Lead/Architect | decisiones, contratos, calidad y riesgos. |
| Backend Engineer(s) | dominio, APIs, workers e integraciones. |
| Frontend Engineer | CRM, pipeline, coaching y aprobaciones. |
| AI Engineer | evaluación, prompts, guardrails y adaptadores. |
| QA/SDET | estrategia TDD/BDD, integración, E2E y no funcional. |
| DevOps/SRE | CI/CD, infraestructura, observabilidad y recuperación. |
| Sales SME | ICP, guiones, rúbricas y aceptación funcional. |
| Privacy/Security | consentimiento, retención y threat model. |

## 5.6 Riesgos y mitigación

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Calidad variable LLM | Alta | Alto | outputs estructurados, evals, fallback y revisión. |
| Datos CRM incompletos | Alta | Alto | completeness score, tareas y reglas deterministas. |
| Restricciones WhatsApp | Media | Alto | plantillas, opt-in, sandbox y adaptador desacoplado. |
| Costos IA | Media | Alto | presupuestos, modelos por tarea, caché y métricas. |
| Privacidad de llamadas | Media | Crítico | consentimiento, retención, acceso y región. |
| Duplicados por webhooks | Alta | Alto | dedupe, idempotencia y outbox. |
| Alcance excesivo | Alta | Alto | verticales por sprint y P0/P1/P2. |
| Adopción baja | Media | Alto | vendedor en diseño, feedback útil y piloto. |

## 5.7 Entornos

| Entorno | Datos | Proveedores | Propósito |
|---|---|---|---|
| Local | sintéticos | fakes/MinIO | desarrollo rápido. |
| CI | efímeros | fakes | pruebas reproducibles. |
| Staging | sanitizados | sandbox | integración, UAT y carga controlada. |
| Producción | reales | reales | operación, acceso restringido. |

Nunca copiar una BD de producción a local. Staging usa datos sintéticos o anonimizados.

## 5.8 Configuración

`.env.example` debe enumerar nombres sin secretos:

```dotenv
APP_ENV=local
APP_BASE_URL=http://localhost:8000
DATABASE_URL=postgresql+asyncpg://antigravity:change-me@postgres:5432/antigravity
REDIS_URL=redis://redis:6379/0
S3_ENDPOINT_URL=http://minio:9000
S3_REGION=us-east-1
S3_BUCKET_AUDIO=antigravity-audio
S3_ACCESS_KEY_ID=change-me
S3_SECRET_ACCESS_KEY=change-me
JWT_ISSUER=https://idp.example.com/
JWT_AUDIENCE=antigravity-api
LLM_PROVIDER=fake
LLM_MODEL=provider-model-name
LLM_API_KEY=
STT_PROVIDER=fake
STT_API_KEY=
CHATWOOT_BASE_URL=
CHATWOOT_TOKEN=
CHATWOOT_WEBHOOK_SECRET=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_APP_SECRET=
OTEL_EXPORTER_OTLP_ENDPOINT=
```

Producción usa secret manager/plataforma; no archivos `.env` dentro de imágenes.

## 5.9 Docker Compose de desarrollo

```yaml
services:
  api:
    build: .
    command: uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    env_file: .env
    ports: ["8000:8000"]
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_started

  worker:
    build: .
    command: uv run arq app.workers.settings.WorkerSettings
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  scheduler:
    build: .
    command: uv run python -m app.scheduler
    env_file: .env
    depends_on:
      redis:
        condition: service_healthy

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: antigravity
      POSTGRES_PASSWORD: change-me
      POSTGRES_DB: antigravity
    volumes: ["postgres_data:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U antigravity -d antigravity"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes: ["redis_data:/data"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: local-admin
      MINIO_ROOT_PASSWORD: local-change-me
    ports: ["9000:9000", "9001:9001"]
    volumes: ["minio_data:/data"]

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

Para producción se deben fijar imágenes por digest/tag probado; `latest` sólo se muestra para desarrollo local.

## 5.10 Despliegue

### Docker genérico

1. Construir imagen multi-stage como usuario no root.
2. Ejecutar tests y escaneo antes de publicar.
3. Firmar/etiquetar imagen con commit SHA.
4. Ejecutar migración como release job único.
5. Desplegar API, workers y scheduler por separado.
6. Validar `/health/live` y `/health/ready`.
7. Ejecutar smoke test productivo sin envío real.
8. Habilitar tráfico y observar métricas.

### Railway

- servicios: `api`, `worker`, `scheduler`;
- PostgreSQL y Redis administrados;
- bucket externo S3-compatible;
- variables por entorno, no compartidas innecesariamente;
- healthcheck de API;
- migration command previo al release;
- volúmenes locales no son fuente durable para audio;
- escalar workers independientemente.

### Easypanel

- crear proyecto con servicios separados desde la misma imagen;
- provisionar PostgreSQL, Redis y MinIO/S3;
- red privada para datos;
- dominio y TLS sólo para API/frontend;
- no publicar puertos de PostgreSQL, Redis o MinIO internamente;
- ejecutar Alembic como tarea controlada;
- configurar backups fuera del host y probar restauración.

### Estrategia de migración

- migraciones expand/contract;
- no eliminar/renombrar una columna usada en el mismo release que introduce el reemplazo;
- backfills reanudables y observables;
- rollback de aplicación compatible con esquema;
- snapshot/backup antes de cambios de alto riesgo.

### Rollback

1. detener promoción;
2. revertir a imagen anterior compatible;
3. pausar scheduler/envíos si el incidente afecta automatizaciones;
4. no ejecutar downgrade destructivo automático;
5. reconciliar outbox/jobs;
6. documentar impacto y causa.

## 5.11 Runbooks mínimos

- proveedor LLM degradado;
- cola Redis acumulada;
- webhook inválido o duplicado;
- mensajes de seguimiento incorrectos;
- posible fuga cross-tenant;
- costo diario anormal;
- fallo de migración;
- restauración de PostgreSQL;
- revocación/rotación de credenciales;
- derecho de acceso/borrado de datos.

## 5.12 Hitos de aprobación

| Gate | Evidencia |
|---|---|
| G0 Arquitectura | ADRs, threat model, alcance y políticas aprobadas. |
| G1 Foundation | tenancy, CRM vertical, CI y staging. |
| G2 Agente 1 | webhook -> scoring explicable en sandbox. |
| G3 Agente 2 | llamada consentida -> coaching privado. |
| G4 Agente 3 | elegibilidad -> aprobación/envío idempotente. |
| G5 Piloto | BDD crítico verde, UAT, monitoreo, backups y rollback. |

---

# 6. TRAZABILIDAD Y DECISIONES PENDIENTES

## 6.1 Matriz de trazabilidad

| Requisito | API/evento | BDD | Pruebas |
|---|---|---|---|
| Cualificar lead | `POST /leads`, `lead.created.v1` | 3.1 | T-01, T-03, T-11 |
| Analizar llamada | `POST /calls`, `call.ready_for_analysis.v1` | 3.2 | T-03, T-07, T-08 |
| Seguimiento por SLA | `POST /deals/{id}/followups`, `deal.followup_due.v1` | 3.3 | T-04, T-05, T-09, T-10 |
| Preservar contexto | webhooks + sobre normalizado | 3.4 | T-01, T-06 |
| Aislar tenants | todas las rutas/queries | 3.4 | T-02 |
| Operar con fallas | AI runs/outbox | 3.1-3.3 | T-03, T-05, T-06, T-12 |

## 6.2 ADRs por crear

1. ADR-001: monolito modular y criterios de extracción.
2. ADR-002: estrategia multi-tenant y RLS.
3. ADR-003: IdP y autorización.
4. ADR-004: proveedor LLM inicial y residencia de datos.
5. ADR-005: proveedor STT y consentimiento.
6. ADR-006: Chatwoot vs WhatsApp como integración primaria.
7. ADR-007: ARQ, scheduler y outbox.
8. ADR-008: storage y retención.
9. ADR-009: observabilidad y gestión de secretos.
10. ADR-010: política de autonomía por agente.

## 6.3 Preguntas que bloquean implementación productiva

1. ¿Quiénes son los primeros tenants y cuántos vendedores/lead volume tendrán?
2. ¿Cuál es el pipeline real y qué etapa dispara cada SLA?
3. ¿Qué datos forman el ICP y cómo se ponderan?
4. ¿Qué proveedor/cuenta controla WhatsApp y qué plantillas están aprobadas?
5. ¿Cómo se obtiene y registra consentimiento de mensajes y grabaciones?
6. ¿De dónde provienen los audios y qué formatos/duración son habituales?
7. ¿Qué acciones del Agente 3 pueden ser `AUTO_SEND` en el piloto?
8. ¿Qué región de datos, retención y borrado exige el contrato?
9. ¿Qué proveedor LLM/STT satisface costo, calidad y privacidad?
10. ¿Qué métricas comerciales base permitirán demostrar impacto?

---

# 7. CRITERIO DE APROBACIÓN DEL DOCUMENTO

Este marco queda aprobado cuando Producto, Arquitectura, Operaciones Comerciales y Seguridad:

- validan los supuestos AS-01 a AS-07;
- resuelven o calendarizan los ADRs;
- aceptan alcance MVP y fuera de alcance;
- confirman políticas de consentimiento y autonomía;
- aceptan métricas y gates;
- convierten el WBS P0 en backlog estimado;
- identifican responsables por integración y entorno.

Una vez aprobado, la siguiente entrega debe ser el esqueleto ejecutable del repositorio con PRD priorizado, ADRs, OpenAPI inicial, migraciones y la primera historia TDD/BDD del Sprint 1.
