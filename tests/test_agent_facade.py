import pytest
from datetime import datetime
from engine.agent_facade import get_agent_payload

def test_agent_payload():
    dt = datetime(2025, 6, 20, 10, 0)
    payload = get_agent_payload(dt=dt, question="Test AI Agent query", gender=1)
    
    assert payload["schema_version"] == "2.2.0-agent"
    assert "data" in payload
    data = payload["data"]
    
    assert "time_coords" in data
    assert "iching" in data
    assert "bazi" in data
    assert "tuvi" in data
    assert "halac" in data
    assert "kymon" in data
    assert "reasoning_scaffolding" in payload
    assert len(payload["reasoning_scaffolding"]) >= 3
