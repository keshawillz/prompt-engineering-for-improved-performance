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
# # CLIP (Modernizing a Legacy Prompt)
# # ---------------------------------------------------------------------------

# Legacy Prompt
legacy_prompt = """
Extract customer complaints from these reviews:

1. "I love the product, but checkout fails with error code 502."
2. "Great support, but shipping took three weeks."
3. "App crashes every time I try to log in."
"""

legacy_response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": legacy_prompt}]
)
print("=== Legacy Prompt Output ===")
print(legacy_response.choices[0].message.content)

# Modernized Prompt with structured output
modern_prompt = """
You are a support triage agent. Extract ONLY complaints from the reviews.

Return JSON with the following schema:
{
  "review_id": "",
  "complaint_category": "",
  "severity": "",
  "recommendations": ""
}

If the review has no complaint, skip it. Do not guess.

Here are the reviews:

1. "I love the product, but checkout fails with error code 502."
2. "Great support, but shipping took three weeks."
3. "App crashes every time I try to log in."
"""

modern_response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": modern_prompt}],
    response_format={"type": "json_object"}
)
print("\n=== Modernized Prompt Output ===")
print(modern_response.choices[0].message.content)
