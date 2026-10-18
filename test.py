import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY", "").strip()
base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").strip()
model = os.getenv("NVIDIA_MODEL", "").strip()

client = OpenAI(base_url=base_url, api_key=api_key)

try:
    print("Sending test request to NVIDIA...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply in 5 words: Is the API working?"}],
        max_tokens=1024,  # Increased so reasoning doesn't exhaust the token limit
        temperature=0.2,
    )
    
    msg = response.choices[0].message
    # Check both normal content and reasoning content
    content = msg.content or getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", "")
    
    print("\n✅ SUCCESS!")
    print("Model response:", content.strip())
except Exception as e:
    print("\n❌ API KEY TEST FAILED:")
    print(e)