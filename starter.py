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
import numpy as np

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

# --- Example Texts ---
text_to_summarize = ''' Pluralsight recently introduced Iris, an AI-powered assistant that transforms how technologists discover 
                        and engage with learning content. Iris provides personalized learning paths by understanding your unique 
                        goals and guiding you through the vast Pluralsight catalog using conversational guidance. It helps learners
                        pinpoint the right combination of courses, labs, and skill assessments—whether you're targeting technical 
                        skill gaps, career milestones, or solving a real-time challenge. For team leaders, Iris can curate learning 
                        journeys tailored to organizational objectives, ensuring teams stay aligned with business goals and 
                        progress more efficiently.'''
review_text = "The app is great but crashes every time I open settings."
ticket_text = "Customer: John Doe reported checkout failing with error code 502."

# --- Naïve Prompts ---
naive_prompts = {
    "summarization": f"Summarize this text: {text_to_summarize}",
    "classification": f"Classify this review: {review_text}",
    "extraction": f"Extract data from this ticket: {ticket_text}",
    "rag": "Tell me about Pluralsight and AI."
}

# TODO: Replace with your improved, agent-style prompt:
# - Define a role & audience (e.g., executive summary).
# - Set constraints (word limit, bullet count).
# - Require structured format (e.g., 3 bullets + 1 risk).
# improved_prompts = {
#     "summarization": TODO
#     "classification": TODO
#     "extraction": TODO
#     "rag": TODO
# }

# --- Summarization, Classification, Extraction ---
for task, prompt in naive_prompts.items():
    if task == "rag":
        continue
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"\n=== {task.upper()} (Naïve) ===")
    print(response.choices[0].message.content)

# --- Simple RAG Setup ---
documents = [
    "Pluralsight launched AI learning paths for developers.",
    "AI is being integrated into Pluralsight's platform to personalize learning.",
    "Courses include generative AI, prompt engineering, and applied machine learning."
]

# Fake vector embeddings (random for demo)
embeddings = {doc: np.random.rand(5) for doc in documents}
query = "What is Pluralsight doing with AI?"
query_vector = np.random.rand(5)

# Find most relevant doc (cosine similarity)
def cosine_similarity(vector_a, vector_b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b))

# Select the most relevant document based on similarity
most_relevant_doc = max(
    embeddings, 
    key=lambda doc: cosine_similarity(query_vector, embeddings[doc])
)

rag_prompt = f"Tell me about Pluralsight and AI. Context: {most_relevant_doc}"

rag_response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": rag_prompt}]
)
print("\n=== RAG (Naïve) ===")
print(rag_response.choices[0].message.content)