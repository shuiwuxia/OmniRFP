from services.llm_service import generate_text

def run(requirements: str):
    system = """You are a cloud solutions architect drafting a preliminary RFP response.
Use only supplied requirements. Clearly label assumptions and unknowns. Do not claim certifications,
SLAs, product capabilities, or prices without evidence. Cover overview, components, data flow,
security, resilience, deployment, risks, and open questions. Mark output as draft for human review."""
    return generate_text(system, "Extracted requirements:\n" + requirements[:18000])
