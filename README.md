# OmniRFP — Multi-Agent RFP Proposal Engine

A runnable first milestone: upload an RFP (PDF/DOCX/TXT), extract text, optionally call NVIDIA Nemotron, create a transparent illustrative estimate, run basic compliance screening, and export a DOCX draft.

## Windows setup
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Configure NVIDIA
Edit `.env` locally:
```env
NVIDIA_API_KEY=your_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=exact_model_id_from_your_NVIDIA_page
```
Use the exact model ID and base URL from the API example for the model you selected. Do not share your key or commit `.env`.

## Run
```powershell
streamlit run app.py
```

## Current limitations
- AI output is a draft and must be reviewed by a human.
- Cost numbers are planning assumptions, not vendor quotes.
- Compliance checks are keyword-based triage, not proof of compliance.
- Scanned PDFs without selectable text need OCR, which is not yet included.
- Gemini fallback and Neuro-SAN orchestration are later integration milestones; we will not pretend they are connected until verified.
