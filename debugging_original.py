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
# # CLIP (Hands-On Debugging with Python)
# # ---------------------------------------------------------------------------
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "List three benefits of cloud computing for startups."}
        ],
        logprobs=True,
        max_tokens=150
    )

    print("\n=== Model Response ===")
    print(response.choices[0].message.content)

    print("\n=== Metadata ===")
    print(f"Finish reason: {response.choices[0].finish_reason}")
    print(f"Token usage: {response.usage}")

    print("\n=== Logprobs (confidence scores) ===")
    # Show logprobs for first few tokens only
    if response.choices[0].logprobs and response.choices[0].logprobs.content:
        print("\n=== Logprobs (first 5 tokens) ===")
        for token_info in response.choices[0].logprobs.content[:5]:
            print(f"Token: {token_info.token}, Logprob: {token_info.logprob}")    

except Exception as e:
    print(f"[Error] API call failed: {e}")





