from __future__ import annotations

from datetime import datetime, timezone, timedelta
from app.services.calculations import (
    calculate_icp_fit_score,
    calculate_call_audio_metrics,
    calculate_deal_risk_and_inactivity,
    calculate_weighted_forecast,
)

def test_icp_fit_score_hot():
    result = calculate_icp_fit_score(
        size_range="201-500",
        industry="Farmacéutica",
        annual_revenue=10_000_000.0,
        is_decision_maker=True,
    )
    assert result["fit_score"] >= 80
    assert result["temperature"] == "HOT"

def test_icp_fit_score_cold():
    result = calculate_icp_fit_score(
        size_range="1-10",
        industry="Servicios Varios",
        annual_revenue=100_000.0,
        is_decision_maker=False,
    )
    assert result["fit_score"] < 60
    assert result["temperature"] in ("WARM", "COLD")

def test_call_audio_metrics():
    turns = [
        {"speaker": "rep", "duration_seconds": 180},
        {"speaker": "prospect", "duration_seconds": 220},
    ]
    metrics = calculate_call_audio_metrics(turns, total_duration_seconds=410)
    assert metrics["talk_listen_ratio"] == 0.45
    assert metrics["silence_seconds"] == 10
    assert metrics["score_1_to_10"] >= 8.0

def test_deal_risk_and_inactivity():
    past_date = datetime.now(timezone.utc) - timedelta(days=5)
    days, str_val, at_risk = calculate_deal_risk_and_inactivity(past_date, sla_days=3)
    assert days == 5
    assert at_risk is True
    assert str_val == "5 días"

def test_weighted_forecast():
    deals = [
        {"value": 1_000_000.0, "win_probability_pct": 50.0, "score": 80},
        {"value": 500_000.0, "win_probability_pct": 20.0, "score": 70},
    ]
    res = calculate_weighted_forecast(deals)
    assert res["total_deals_count"] == 2
    assert res["total_pipeline_value_mxn"] == 1_500_000.0
    assert res["weighted_forecast_value_mxn"] > 0
