import re

RULES = [
    ("security", r"\b(encryption|data security|security controls|access control)\b"),
    ("privacy", r"\b(personal data|privacy|PII|GDPR|data protection)\b"),
    ("availability", r"\b(availability|uptime|SLA|disaster recovery|business continuity)\b"),
    ("accessibility", r"\b(accessibility|WCAG|screen reader)\b"),
    ("support", r"\b(support|maintenance|incident response|help desk)\b"),
    ("delivery", r"\b(delivery date|milestone|implementation schedule|go-live)\b"),
]

def screen(text, proposal=""):
    results = []
    for area, pattern in RULES:
        if re.search(pattern, text, re.I):
            addressed = bool(proposal and re.search(pattern, proposal, re.I))
            results.append({"area": area, "status": "keyword found in draft" if addressed else "needs review",
                            "basis": "Keyword screening only; human verification required."})
    return results or [{"area": "general", "status": "needs review",
                        "basis": "No configured rule matched; this does not imply there are no requirements."}]
