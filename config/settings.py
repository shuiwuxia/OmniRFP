import os
from dotenv import load_dotenv

load_dotenv()

def _get_val(key: str, default: str = "") -> str:
    # 1. Check Streamlit cloud secrets first
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    # 2. Check local environment variables / .env
    return os.getenv(key, default).strip()

def get_settings():
    return {
        "api_key": _get_val("NVIDIA_API_KEY", ""),
        "base_url": _get_val("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        "model": _get_val("NVIDIA_MODEL", ""),
        "timeout": float(_get_val("LLM_TIMEOUT_SECONDS", "90")),
    }

def is_configured(s=None):
    s = s or get_settings()
    return bool(s["api_key"] and s["model"])