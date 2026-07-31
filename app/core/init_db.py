from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base, engine
from app.models.tenant import Organization
from app.models.user import User
from app.models.crm import PipelineStage, Company, Contact, Lead, Deal, Activity, FollowUp, Product
from app.core.security import get_password_hash
from app.services.calculations import calculate_icp_fit_score

logger = logging.getLogger(__name__)

async def init_db(session: AsyncSession) -> None:
    # 1. Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Check if default tenant exists
    tenant_id = "consultorpro-org"
    res = await session.execute(select(Organization).where(Organization.id == tenant_id))
    org = res.scalars().first()
    
    if not org:
        org = Organization(id=tenant_id, name="ConsultorPRO Demo", slug="consultorpro")
        session.add(org)
        await session.flush()

        # Seed default users
        users = [
            User(id="usr-1", tenant_id=tenant_id, email="admin@consultorpro.es", password_hash=get_password_hash("admin123"), full_name="Alejandro Ruiz", role="TENANT_ADMIN", avatar_url="https://randomuser.me/api/portraits/men/32.jpg"),
            User(id="usr-2", tenant_id=tenant_id, email="mariana@consultorpro.es", password_hash=get_password_hash("demo123"), full_name="Mariana Cruz", role="SALES_REP", avatar_url="https://randomuser.me/api/portraits/women/44.jpg"),
            User(id="usr-3", tenant_id=tenant_id, email="ricardo@consultorpro.es", password_hash=get_password_hash("demo123"), full_name="Ricardo López", role="SALES_REP", avatar_url="https://randomuser.me/api/portraits/men/46.jpg"),
            User(id="usr-4", tenant_id=tenant_id, email="sofia@consultorpro.es", password_hash=get_password_hash("demo123"), full_name="Sofía Herrera", role="SALES_REP", avatar_url="https://randomuser.me/api/portraits/women/68.jpg"),
            User(id="usr-5", tenant_id=tenant_id, email="paula@consultorpro.es", password_hash=get_password_hash("demo123"), full_name="Paula Sánchez", role="SALES_REP", avatar_url="https://randomuser.me/api/portraits/women/65.jpg"),
        ]
        session.add_all(users)

        # Seed stages
        stages = [
            PipelineStage(id="new", tenant_id=tenant_id, title="Nuevo", stage_order=1, color="#1769e8", sla_inactivity_days=3, win_probability_pct=20.0),
            PipelineStage(id="qualified", tenant_id=tenant_id, title="Calificado", stage_order=2, color="#f0c419", sla_inactivity_days=3, win_probability_pct=45.0),
            PipelineStage(id="proposal", tenant_id=tenant_id, title="Propuesta", stage_order=3, color="#27a65a", sla_inactivity_days=3, win_probability_pct=70.0),
            PipelineStage(id="negotiation", tenant_id=tenant_id, title="Negociación", stage_order=4, color="#8b5cf6", sla_inactivity_days=3, win_probability_pct=85.0),
        ]
        session.add_all(stages)

        # Seed initial deals matching visual prototype
        deals = [
            Deal(id="1", tenant_id=tenant_id, stage_id="new", company="Grupo Constructor del Bajío", value=850000.0, owner="Ricardo López", score=62, inactivity="2 días", inactivity_days=2, risk=False),
            Deal(id="2", tenant_id=tenant_id, stage_id="new", company="Distribuidora del Valle", value=620000.0, owner="Mariana Cruz", score=71, inactivity="1 día", inactivity_days=1, risk=False),
            Deal(id="3", tenant_id=tenant_id, stage_id="new", company="ServiPlast México", value=1250000.0, owner="Alejandro Ruiz", score=58, inactivity="4 días", inactivity_days=4, risk=True),
            Deal(id="4", tenant_id=tenant_id, stage_id="new", company="Logística del Norte", value=980000.0, owner="Paula Sánchez", score=75, inactivity="Hoy", inactivity_days=0, risk=False),
            Deal(id="5", tenant_id=tenant_id, stage_id="new", company="Alimentos Selectos", value=450000.0, owner="Ricardo López", score=64, inactivity="3 días", inactivity_days=3, risk=False),
            
            Deal(id="6", tenant_id=tenant_id, stage_id="qualified", company="Industrias Molina", value=1850000.0, owner="Mariana Cruz", score=76, inactivity="2 días", inactivity_days=2, risk=False),
            Deal(id="7", tenant_id=tenant_id, stage_id="qualified", company="Farmacéutica del Centro", value=1620000.0, owner="Alejandro Ruiz", score=82, inactivity="Hoy", inactivity_days=0, risk=False),
            Deal(id="8", tenant_id=tenant_id, stage_id="qualified", company="Grupo Textil Águila", value=2300000.0, owner="Sofía Herrera", score=45, inactivity="5 días", inactivity_days=5, risk=True),
            Deal(id="9", tenant_id=tenant_id, stage_id="qualified", company="Tiendas del Sol", value=1240000.0, owner="Ricardo López", score=63, inactivity="2 días", inactivity_days=2, risk=False),
            Deal(id="10", tenant_id=tenant_id, stage_id="qualified", company="Metalúrgica del Pacífico", value=470000.0, owner="Paula Sánchez", score=70, inactivity="Hoy", inactivity_days=0, risk=False),
            
            Deal(id="11", tenant_id=tenant_id, stage_id="proposal", company="Hospital San Gabriel", value=2150000.0, owner="Alejandro Ruiz", score=60, inactivity="3 días", inactivity_days=3, risk=False),
            Deal(id="12", tenant_id=tenant_id, stage_id="proposal", company="Universidad del Noroeste", value=1980000.0, owner="Sofía Herrera", score=78, inactivity="2 días", inactivity_days=2, risk=False),
            Deal(id="13", tenant_id=tenant_id, stage_id="proposal", company="Cementos del Centro", value=1750000.0, owner="Ricardo López", score=72, inactivity="Hoy", inactivity_days=0, risk=False),
            Deal(id="14", tenant_id=tenant_id, stage_id="proposal", company="Energía Sustentable", value=1240000.0, owner="Mariana Cruz", score=59, inactivity="4 días", inactivity_days=4, risk=False),
            Deal(id="15", tenant_id=tenant_id, stage_id="proposal", company="Grupo Hotelero Pacífico", value=670000.0, owner="Ricardo López", score=61, inactivity="2 días", inactivity_days=2, risk=False),
            
            Deal(id="16", tenant_id=tenant_id, stage_id="negotiation", company="Telecom del Bajío", value=2800000.0, owner="Alejandro Ruiz", score=38, inactivity="6 días", inactivity_days=6, risk=True),
            Deal(id="17", tenant_id=tenant_id, stage_id="negotiation", company="Automotriz del Norte", value=1950000.0, owner="Sofía Herrera", score=57, inactivity="4 días", inactivity_days=4, risk=False),
            Deal(id="18", tenant_id=tenant_id, stage_id="negotiation", company="Servicios Integrales México", value=900000.0, owner="Ricardo López", score=74, inactivity="Hoy", inactivity_days=0, risk=False),
            Deal(id="19", tenant_id=tenant_id, stage_id="negotiation", company="Aceros y Perfiles", value=450000.0, owner="Paula Sánchez", score=60, inactivity="3 días", inactivity_days=3, risk=False),
        ]
        session.add_all(deals)

        # Seed initial Companies
        companies = [
            Company(id="cmp-1", tenant_id=tenant_id, name="Grupo Textil Águila", industry="Textil", size_range="201-500", annual_revenue=23000000.0, location="Puebla, MX"),
            Company(id="cmp-2", tenant_id=tenant_id, name="Farmacéutica del Centro", industry="Farmacéutica", size_range="51-200", annual_revenue=16200000.0, location="CDMX, MX"),
            Company(id="cmp-3", tenant_id=tenant_id, name="Telecom del Bajío", industry="Tecnología", size_range="500+", annual_revenue=45000000.0, location="León, GTO"),
        ]
        session.add_all(companies)

        # Seed initial Contacts
        contacts = [
            Contact(id="cnt-1", tenant_id=tenant_id, company_id="cmp-1", first_name="Roberto", last_name="Navarro", email="rnavarro@textilaguila.com", phone="+52 22 2341 9900", position="Director General", is_decision_maker=True),
            Contact(id="cnt-2", tenant_id=tenant_id, company_id="cmp-2", first_name="Laura", last_name="Mendoza", email="lmendoza@farmacentro.mx", phone="+52 55 5612 3344", position="VP de Operaciones", is_decision_maker=True),
        ]
        session.add_all(contacts)

        # Seed initial Activities
        activities = [
            Activity(id="act-1", tenant_id=tenant_id, deal_id="8", title="Reunión de alineación con Grupo Textil Águila", activity_type="MEETING", due_date="Hoy a las 16:30", completed=False),
            Activity(id="act-2", tenant_id=tenant_id, deal_id="7", title="Enviar cotización a Farmacéutica del Centro", activity_type="EMAIL", due_date="Mañana 10:00", completed=True),
            Activity(id="act-3", tenant_id=tenant_id, deal_id="16", title="Llamada de seguimiento por inactividad Telecom", activity_type="CALL", due_date="Hoy", completed=False),
        ]
        session.add_all(activities)

        # Seed initial FollowUps
        followups = [
            FollowUp(id="flw-1", tenant_id=tenant_id, deal_id="8", company_name="Grupo Textil Águila", channel="WHATSAPP", status="PENDING", scheduled_at="Hoy 16:30", message_draft="Hola Roberto. Te escribo de ConsultorPRO para confirmar nuestra llamada de revisión de propuesta.", approval_mode="REQUIRE_APPROVAL"),
            FollowUp(id="flw-2", tenant_id=tenant_id, deal_id="16", company_name="Telecom del Bajío", channel="EMAIL", status="PENDING", scheduled_at="Hoy 17:00", message_draft="Estimado Alejandro, derivado de la inactividad de 6 días, enviamos resumen ejecutivo.", approval_mode="SUGGEST_ONLY"),
        ]
        session.add_all(followups)

        # Seed Products
        products = [
            Product(id="prd-1", tenant_id=tenant_id, name="Implementación CRM Inteligente", sku="YUK-IMP-01", price_mxn=450000.0, category="Implementación", description="Configuración y setup de agentes IA y conectores."),
            Product(id="prd-2", tenant_id=tenant_id, name="Licencia Mensual SuperProspector", sku="YUK-AGT-01", price_mxn=25000.0, category="Suscripción", description="Agente de scoring y prospección con Apify."),
            Product(id="prd-3", tenant_id=tenant_id, name="Auditoría de Ventas SuperSales", sku="YUK-AUD-01", price_mxn=120000.0, category="Consultoría", description="Análisis automatizado de llamadas y coaching comercial."),
        ]
        session.add_all(products)

        await session.commit()
        logger.info("Base de datos inicializada y poblada con datos iniciales.")
