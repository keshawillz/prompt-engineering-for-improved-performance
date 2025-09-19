"""
Prompt Engineering for Improved Performance
All examples use Python and the OpenAI client.

Prereqs:
  pip install openai
  pip install python-dotenv
  export API_KEY = os.environ[...]
"""

import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# read local .env file
_ = load_dotenv(find_dotenv()) 

# ---- Configuration ----
# Generate an OpenAI API Key at https://platform.openai.com/api-keys
key = os.environ['OPENAI_API_KEY']
if not key:
    raise SystemExit("Error: Missing API key. Set OPENAI_API_KEY.")

# ---- Client ----
client = OpenAI(
    api_key=key
)

# # ---------------------------------------------------------------------------
# # CLIP (Investigating with Model Metadata)
# # ---------------------------------------------------------------------------

# ---- Prompt ----
prompt = """
    Generate a comprehensive guide to every planet in our solar system. 
    For each planet, include: 
    (1) its physical characteristics (size, mass, composition), 
    (2) discovery history and key missions, 
    (3) notable moons or rings, 
    (4) impact on science fiction or popular culture, and 
    (5) major open scientific questions. 
    Write in full paragraphs and provide as much detail as possible.
"""

# ---- Request with metadata ----
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}],
    logprobs=True,                # enable token-level confidence
    max_tokens=150,
    temperature=0.3,
    seed=42                       # reproducibility
)

# ---- Inspect response ----
choice = response.choices[0]

print("=== Model Response ===")
print(choice.message.content)

print("\n=== Metadata ===")
print("Finish reason:", choice.finish_reason)
print("System fingerprint:", response.system_fingerprint)
print("Token usage:", response.usage)

# Show logprobs for first few tokens
if choice.logprobs and choice.logprobs.content:
    print("\n=== Logprobs (first 5 tokens) ===")
    for token_info in choice.logprobs.content[:5]:
        print(f"Token: {token_info.token}, Logprob: {token_info.logprob}")