# CRM Inteligente Antigravity

Baseline técnico del CRM de seguimiento comercial con tres agentes de IA:

1. Prospector y Lead Scorer.
2. Coach de ventas y analista de llamadas.
3. Automatización de seguimiento y nutrición.

La arquitectura completa, contratos, escenarios BDD, estrategia TDD y roadmap están en
[`crm_ai_architecture_spec.md`](crm_ai_architecture_spec.md).

## Estado actual

El repositorio contiene el primer vertical visual desplegable. Incluye:

- dashboard CRM con pipeline Kanban interactivo en `/`;
- búsqueda y filtro de oportunidades en riesgo;
- creación demostrativa de leads;
- panel contextual de los tres agentes de IA;
- endpoint de información técnica en `/api/v1/system`;
- liveness check en `/health/live`;
- readiness check de Railway en `/health/ready`;
- OpenAPI en `/docs` y `/openapi.json`;
- Dockerfile no-root;
- configuración de despliegue de Railway;
- pruebas del contrato mínimo.

La interfaz usa datos demostrativos. PostgreSQL, Redis, bucket y los agentes se conectarán por
verticales siguiendo el roadmap de la especificación.

## Desarrollo local

Requiere Python 3.12. Se recomienda `uv`, aunque también funciona con `pip`.

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

Alternativa con `pip`:

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/uvicorn app.main:app --reload
```

Abrir:

- Aplicación: <http://localhost:8000/>
- Swagger: <http://localhost:8000/docs>
- Health: <http://localhost:8000/health/ready>

## Pruebas

```bash
uv run ruff check .
uv run pytest --cov=app --cov-report=term-missing
```

## Despliegue en Railway

1. Crear un proyecto en Railway.
2. Elegir **Deploy from GitHub repo**.
3. Seleccionar `mangoex/yuk`.
4. Railway detectará `railway.json` y construirá el `Dockerfile`.
5. Añadir la variable `APP_ENV=production`.
6. Generar un dominio público desde **Settings > Networking**.
7. Confirmar que `/health/ready` responde `{"status":"ready"}`.

No es necesario configurar `PORT`; Railway lo inyecta automáticamente.

### Servicios de datos posteriores

Cuando se implemente el primer vertical:

- añadir PostgreSQL al proyecto y enlazar `DATABASE_URL`;
- añadir Redis y enlazar `REDIS_URL`;
- configurar un bucket S3-compatible;
- guardar tokens de LLM, Chatwoot y WhatsApp como variables secretas.

No copiar valores de `.env.example` directamente a producción.
