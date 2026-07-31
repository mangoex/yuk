from __future__ import annotations

from typing import Any
from app.services.calculations import calculate_call_audio_metrics

class SuperSalesAgent:
    """
    Agente 2: SuperSales & Call Analyst.
    Analiza llamadas comerciales, ratios de diálogo y rúbrica de coaching.
    """
    name: str = "SuperSales"
    version: str = "v1.0.0"

    def analyze_call(
        self,
        company_name: str,
        turns: list[dict[str, Any]] | None = None,
        duration_seconds: int = 420,
    ) -> dict[str, Any]:
        if not turns:
            turns = [
                {"speaker": "rep", "duration_seconds": 120, "text": "Presentación de la propuesta de valor"},
                {"speaker": "prospect", "duration_seconds": 210, "text": "Explicación de sus requerimientos operacionales y objeciones de costo"},
                {"speaker": "rep", "duration_seconds": 60, "text": "Cierre con acuerdo de enviar cotización"},
            ]

        # 1. Deterministic Metrics
        metrics = calculate_call_audio_metrics(turns, duration_seconds)

        return {
            "agent": self.name,
            "version": self.version,
            "company_name": company_name,
            "duration_formatted": f"{duration_seconds // 60}m {duration_seconds % 60}s",
            "talk_listen_ratio_pct": f"{int(metrics['talk_listen_ratio'] * 100)}% / {int((1 - metrics['talk_listen_ratio']) * 100)}%",
            "score_1_to_10": metrics["score_1_to_10"],
            "strengths": ["Buena indagación de necesidades iniciales", "Escucha activa adecuada"],
            "coaching_tip": "Al abordar la objeción de presupuesto, refuerza el ROI estimado antes de ofrecer un descuento.",
            "actionable_next_step": "Enviar propuesta ajustada destacando el período de retorno de inversión.",
        }

supersales_agent = SuperSalesAgent()
