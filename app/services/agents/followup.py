from __future__ import annotations

from typing import Any

class FollowUpAgent:
    """
    Agente 3: Marketing Auto Pilot & Follow-up Engine.
    Detecta inactividad y genera borradores de seguimiento con guardrails.
    """
    name: str = "Marketing Auto Pilot"
    version: str = "v1.0.0"

    def generate_followup(
        self,
        company_name: str,
        owner: str = "Alejandro Ruiz",
        days_inactive: int = 3,
        channel: str = "WHATSAPP",
    ) -> dict[str, Any]:
        message_draft = (
            f"Hola, buen día. Te escribe {owner} de ConsultorPRO. "
            f"Quería retomar nuestra conversación sobre el proyecto de {company_name}. "
            "¿Tuviste oportunidad de revisar la propuesta o prefieres que agendemos una breve llamada de 10 minutos hoy?"
        )

        approval_mode = "REQUIRE_APPROVAL" if days_inactive < 5 else "SUGGEST_ONLY"

        return {
            "agent": self.name,
            "version": self.version,
            "company_name": company_name,
            "days_inactive": days_inactive,
            "channel": channel,
            "status": "PENDING",
            "approval_mode": approval_mode,
            "message_draft": message_draft,
            "scheduled_time": "Hoy a las 16:30 hrs",
        }

followup_agent = FollowUpAgent()
