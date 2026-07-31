from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

def calculate_icp_fit_score(
    size_range: str | None = None,
    industry: str | None = None,
    annual_revenue: float | None = None,
    is_decision_maker: bool = False,
) -> dict[str, Any]:
    """
    Cálculo determinista de adecuación al Perfil de Cliente Ideal (ICP).
    Combina factores ponderados cuantitativos en Python.
    """
    # 1. Puntuación por tamaño de empresa (30%)
    size_scores = {
        "1-10": 40,
        "11-50": 65,
        "51-200": 90,
        "201-500": 100,
        "500+": 95,
    }
    size_score = size_scores.get(size_range or "", 50)

    # 2. Puntuación por industria (30%)
    target_industries = {
        "construcción": 95,
        "farmacéutica": 95,
        "tecnología": 95,
        "logística": 90,
        "manufactura": 90,
        "alimentos": 85,
        "textil": 85,
        "energía": 90,
        "educación": 80,
    }
    ind_key = (industry or "").lower()
    industry_score = 60
    for key, val in target_industries.items():
        if key in ind_key:
            industry_score = val
            break

    # 3. Puntuación por ingresos anuales (20%)
    rev = annual_revenue or 0.0
    if rev >= 5_000_000:
        revenue_score = 100
    elif rev >= 1_000_000:
        revenue_score = 80
    elif rev >= 500_000:
        revenue_score = 65
    else:
        revenue_score = 50

    # 4. Puntuación por nivel de decisión (20%)
    decision_score = 100 if is_decision_maker else 55

    # Cálculo ponderado
    fit_score = int(
        round(
            0.30 * size_score
            + 0.30 * industry_score
            + 0.20 * revenue_score
            + 0.20 * decision_score
        )
    )

    if fit_score >= 80:
        temperature = "HOT"
    elif fit_score >= 55:
        temperature = "WARM"
    else:
        temperature = "COLD"

    return {
        "fit_score": fit_score,
        "temperature": temperature,
        "breakdown": {
            "size_score": size_score,
            "industry_score": industry_score,
            "revenue_score": revenue_score,
            "decision_score": decision_score,
        },
    }

def calculate_call_audio_metrics(
    turns: list[dict[str, Any]], total_duration_seconds: int
) -> dict[str, Any]:
    """
    Cálculo determinista de métricas de audio/diálogo de llamadas de venta.
    """
    rep_duration = sum(t.get("duration_seconds", 0) for t in turns if t.get("speaker") == "rep")
    prospect_duration = sum(t.get("duration_seconds", 0) for t in turns if t.get("speaker") == "prospect")
    
    spoken_total = rep_duration + prospect_duration
    if spoken_total > 0:
        talk_listen_ratio = round(rep_duration / spoken_total, 2)
    else:
        talk_listen_ratio = 0.50

    silence_seconds = max(0, total_duration_seconds - spoken_total)
    turn_count = len(turns)

    # Penalizaciones deterministas si el vendedor domina > 65% del tiempo o si hay silencios largos
    base_score = 9.0
    if talk_listen_ratio > 0.65:
        base_score -= 1.5
    elif talk_listen_ratio < 0.30:
        base_score -= 1.0

    if silence_seconds > 25:
        base_score -= 1.0

    final_score = round(max(1.0, min(10.0, base_score)), 1)

    return {
        "duration_seconds": total_duration_seconds,
        "rep_talk_seconds": rep_duration,
        "prospect_talk_seconds": prospect_duration,
        "talk_listen_ratio": talk_listen_ratio,
        "silence_seconds": silence_seconds,
        "turn_count": turn_count,
        "score_1_to_10": final_score,
    }

def calculate_deal_risk_and_inactivity(
    last_interaction_at: datetime, sla_days: int = 3
) -> tuple[int, str, bool]:
    """
    Calcula deterministamente días transcurridos desde última interacción y bandera de riesgo.
    """
    now = datetime.now(timezone.utc)
    # Ensure offset-aware comparison
    if last_interaction_at.tzinfo is None:
        last_interaction_at = last_interaction_at.replace(tzinfo=timezone.utc)
    
    delta_days = (now - last_interaction_at).days
    if delta_days <= 0:
        inactivity_str = "Hoy"
    elif delta_days == 1:
        inactivity_str = "1 día"
    else:
        inactivity_str = f"{delta_days} días"

    is_at_risk = delta_days >= sla_days
    return delta_days, inactivity_str, is_at_risk

def calculate_weighted_forecast(deals: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Calcula el valor pronosticado ponderado del pipeline comercial.
    """
    total_pipeline = 0.0
    total_weighted = 0.0

    for d in deals:
        val = float(d.get("value", 0.0))
        prob = float(d.get("win_probability_pct", 20.0)) / 100.0
        score_factor = float(d.get("score", 70)) / 100.0
        
        weighted = val * prob * score_factor
        total_pipeline += val
        total_weighted += weighted

    return {
        "total_deals_count": len(deals),
        "total_pipeline_value_mxn": round(total_pipeline, 2),
        "weighted_forecast_value_mxn": round(total_weighted, 2),
    }
