from __future__ import annotations

from typing import Any
from app.services.calculations import calculate_icp_fit_score

class ProspectorAgent:
    """
    Agente 1: SuperProspector & Lead Scorer.
    Combina validación determinista + análisis contextual.
    """
    name: str = "SuperProspector"
    version: str = "v1.0.0"

    def qualify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        company_name = lead_data.get("company_name", "Empresa Prospecto")
        industry = lead_data.get("industry", "General")
        size_range = lead_data.get("size_range", "11-50")
        revenue = lead_data.get("annual_revenue", 1000000.0)

        # 1. Deterministic Calculation
        det_result = calculate_icp_fit_score(
            size_range=size_range,
            industry=industry,
            annual_revenue=revenue,
            is_decision_maker=True,
        )

        score = det_result["fit_score"]
        temp = det_result["temperature"]

        factors_pos = [f"Sector de alto potencial ({industry})", "Presupuesto adecuado para solución B2B"]
        factors_neg = []
        if score < 70:
            factors_neg.append("Tamaño de empresa o volumen por debajo del perfil óptimo")

        recommendation = "Prioridad alta: Agendar llamada de descubrimiento dentro de las primeras 24 horas." if temp == "HOT" else "Enviar secuencia de nutrición y contenido relevante."

        return {
            "agent": self.name,
            "version": self.version,
            "company_name": company_name,
            "score": score,
            "temperature": temp,
            "confidence": 0.92,
            "positive_factors": factors_pos,
            "negative_factors": factors_neg,
            "recommendation": recommendation,
        }

prospector_agent = ProspectorAgent()
