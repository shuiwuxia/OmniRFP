from openai import OpenAI
from config.settings import get_settings, is_configured

def generate_text(system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 4096):
    s = get_settings()
    if not is_configured(s):
        raise RuntimeError("Nemotron is not configured. Set NVIDIA_API_KEY and NVIDIA_MODEL in .env.")
    client = OpenAI(api_key=s["api_key"], base_url=s["base_url"], timeout=s["timeout"], max_retries=2)
    response = client.chat.completions.create(
        model=s["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")
    return content.strip()