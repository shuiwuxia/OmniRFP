import pytest
from agents.cost_agent import estimate
from agents.compliance_agent import screen
from document_processing.extract import chunk_text

def test_cost_math():
    result = estimate(2, 2, 50, 10, 100, 1)
    assert result["engineering_hours"] == 160
    assert result["total"] == 8910

def test_cost_validation():
    with pytest.raises(ValueError):
        estimate(0, 2, 50, 10, 100, 1)

def test_compliance_rules():
    areas = {item["area"] for item in screen("Encryption and uptime SLA are required.")}
    assert {"security", "availability"} <= areas

def test_chunking():
    chunks = chunk_text("x" * 20000, 9000, 500)
    assert len(chunks) == 3
    assert all(len(chunk) <= 9000 for chunk in chunks)
