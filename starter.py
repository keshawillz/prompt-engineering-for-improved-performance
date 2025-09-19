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

# Starter Prompts
summarization = """
  Summarize this text: [text here]
"""

classification = """
  Classify this review: [review here]
"""

extraction = """
  Extract data from this: [text here]
"""

rag = """
  Tell me about a topic: [topic here]
"""

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": summarization}]
)
print("=== Starter Prompt Output ===")
print(response.choices[0].message.content)
