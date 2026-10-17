import streamlit as st
from config.settings import get_settings, is_configured
from document_processing.extract import extract_document
from agents.cost_agent import estimate
from agents.compliance_agent import screen
from proposal_generation.docx_generator import build

st.set_page_config(page_title="OmniRFP", page_icon="📑", layout="wide")
st.title("📑 OmniRFP")
st.caption("Multi-agent enterprise RFP proposal engine — first working milestone")
st.warning("Draft only: a human must verify requirements, architecture, costs, and compliance before submission.")
settings = get_settings()

with st.sidebar:
    st.header("AI connection")
    if is_configured(settings):
        st.success("NVIDIA configuration found")
        st.caption("Model: " + settings["model"])
    else:
        st.info("Demo mode. Configure NVIDIA_API_KEY and NVIDIA_MODEL in .env.")
    st.divider()
    st.header("Illustrative cost assumptions")
    team = st.number_input("Team size", 1, 100, 3)
    weeks = st.number_input("Duration (weeks)", 1, 260, 12)
    rate = st.number_input("Hourly rate (USD)", min_value=0.0, value=60.0, step=5.0)
    cloud = st.number_input("Cloud cost/month (USD)", min_value=0.0, value=500.0, step=50.0)
    months = st.number_input("Cloud months", 0, 120, 12)
    contingency = st.slider("Contingency (%)", 0, 50, 15)

uploaded = st.file_uploader("Upload an RFP document", type=["pdf", "docx", "txt"])
if uploaded and st.button("Analyze RFP", type="primary", use_container_width=True):
    try:
        full_text, records = extract_document(uploaded.name, uploaded.getvalue())
        st.session_state["rfp_text"] = full_text
        with st.spinner("Running analysis..."):
            if is_configured(settings):
                from agents.requirements_agent import run as requirements_run
                from agents.architect_agent import run as architect_run
                from services.llm_service import generate_text
                requirements = requirements_run(full_text)
                solution = architect_run(requirements)
                summary = generate_text(
                    "Write a 150-200 word executive summary for a draft proposal. Do not invent facts.",
                    f"Requirements:\n{requirements[:9000]}\n\nSolution:\n{solution[:9000]}"
                )
                mode = "NVIDIA model"
            else:
                requirements = "DEMO MODE — not AI-generated. Configure the NVIDIA model to extract structured requirements.\n\n" + "\n".join(
                    f"- {r['source']} / {r['location']}: {len(r['text'])} characters extracted" for r in records
                )
                solution = "DEMO MODE — no AI architecture generated. Configure NVIDIA to generate a solution draft."
                summary = "The document text was extracted successfully. Configure NVIDIA to generate the executive summary and technical proposal."
                mode = "Demo"
            cost = estimate(int(team), int(weeks), float(rate), float(contingency), float(cloud), int(months))
            compliance = screen(full_text, solution)
            st.session_state["result"] = {
                "title": uploaded.name, "summary": summary, "requirements": requirements,
                "solution": solution, "cost": cost, "compliance": compliance, "mode": mode
            }
    except Exception as exc:
        st.error(f"Analysis failed: {exc}")
        st.info("Check the file type and, if using NVIDIA, confirm the exact model ID, base URL, API key, and rate limits.")

if "result" in st.session_state:
    r = st.session_state["result"]
    st.success(f"Workflow finished in {r['mode']} mode.")
    t1, t2, t3, t4 = st.tabs(["Executive summary", "Requirements", "Solution", "Cost & compliance"])
    with t1:
        st.markdown(r["summary"])
    with t2:
        st.text(r["requirements"])
    with t3:
        st.markdown(r["solution"])
    with t4:
        c = r["cost"]
        a, b, d = st.columns(3)
        a.metric("Labor", f"${c['labor_cost']:,.2f}")
        b.metric("Cloud", f"${c['cloud_cost']:,.2f}")
        d.metric("Estimated total", f"${c['total']:,.2f}")
        st.caption(c["disclaimer"])
        st.dataframe(r["compliance"], use_container_width=True)
    document = build(r["title"], r["summary"], r["requirements"], r["solution"], r["cost"], r["compliance"])
    st.download_button("Download draft proposal (.docx)", document, "OmniRFP_Draft_Proposal.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       type="primary")
