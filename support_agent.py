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
from agents import Agent, Runner, function_tool 
from dataclasses import dataclass
from typing import List, Dict
import json
from datetime import datetime

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
# # CLIP (Anatomy of an Agent Prompt)
# # ---------------------------------------------------------------------------
@dataclass
class KBArticle:
    title: str
    url: str
    tags: List[str]

# --- Tool: Knowledge Base Search (stub) -------------------------------------
@function_tool
def kb_search(query: str) -> str:
    """
    Search the internal KB and return a small JSON list of {title, url}.
    This is a stub implementation for demo purposes. In the real world, you 
    would access a datastore via an API call.
    """
    demo_kb: List[KBArticle] = [
        KBArticle(
            title="Stripe 5xx during checkout after deploy",
            url="https://kb.internal/company/stripe-5xx-deploy",
            tags=["stripe", "502", "deploy", "checkout"]
        ),
        KBArticle(
            title="Browser cache issues on Chrome login",
            url="https://kb.internal/company/safari-login-cache",
            tags=["safari", "login", "cache"]
        ),
        KBArticle(
            title="Intermittent gateway errors (502/504) playbook",
            url="https://kb.internal/company/gateway-5xx-playbook",
            tags=["gateway", "502", "504", "playbook"]
        ),
    ]

    query = query.lower()

    search_results = [
        {"title": article.title, "url": article.url}
        for article in demo_kb
            if any(tag in query for tag in article.tags) or any(token in article.tags for token in query.split())
    ]

    if not search_results:
        search_results = [{"title": "No direct KB match", "url": ""}]

    return json.dumps(search_results)

# --- Tool: Ticket Note / Update (stub) --------------------------------------
@function_tool
def ticket_update(ticket_id: str, status: str, note: str) -> str:
    """
    Propose a status change and internal note. 
    """
    timestamp = datetime.timezone.utc
    return json.dumps({
        "ticket_id": ticket_id,
        "status_proposed": status,
        "note_preview": note[:240],
        "timestamp_utc": timestamp
    })

# --- Tool: Draft Customer Email (stub) --------------------------------------
@function_tool
def email_draft(to: str, subject: str, points: List[str]) -> str:
    """
    Draft a customer-ready email from bullet points. 
    """
    greeting = f"Hi {to.split('@')[0].title()},"
    bullets = "\n".join([f"- {p}" for p in points])
    body = (
        f"{greeting}\n\n"
        f"Thanks for your patience while we look into your report.\n\n"
        f"Summary:\n{bullets}\n\n"
        f"Best,\nSupport Team"
    )
    return json.dumps({"to": to, "subject": subject, "body": body})

# ---------------------------------------------------------------------------
# Agent: Customer Support Triage
# ---------------------------------------------------------------------------
support_agent = Agent(
    name="Support Triage Agent",
    model="gpt-5",   
    instructions=(
        "You triage customer tickets. Work step-by-step: outline a brief Plan, "
        "use available tools conceptually, then return ONLY the JSON schema.\n\n"
        "GOAL:\n"
        "- Review a support ticket, check for known issues, and propose next steps.\n\n"
        "TOOLS:\n"
        "- kb_search(query): find relevant KB articles (title, url) as JSON.\n"
        "- ticket_update(ticket_id, status, note): propose an internal note/status.\n"
        "- email_draft(to, subject, points): draft a customer email (JSON result).\n\n"
        "CONSTRAINTS & POLICIES:\n"
        "- Do not guess. If info is missing, list exact clarifications.\n"
        "- Prefer existing KB fixes before custom workarounds.\n"
        "- Keep recommendations under 150 words. No PII in output.\n\n"
        "RETURN FORMAT (JSON only):\n"
        "{\n"
        '  "issue_summary": "",\n'
        '  "likely_cause": "",\n'
        '  "proposed_resolutions": ["", "", ""],\n'
        '  "kb_refs": [{"title":"", "url":""}],\n'
        '  "customer_reply_draft": {"to":"", "subject":"", "body":""},\n'
        '  "next_actions": ["ticket_note","wait_for_customer","escalate"],\n'
        '  "confidence": 0.0\n'
        "}\n\n"
        "AUTONOMY & PLANNING:\n"
        "- First output a one-paragraph 'Plan:' (1–3 sentences). Then output ONLY the JSON.\n"
        "- If blocked, state the clarification in Plan, then return best-effort JSON with confidence adjusted."
    ),
    tools=[kb_search, ticket_update, email_draft]
)

# ---------------------------------------------------------------------------
# Kickoff: Provide a ticket & run
# ---------------------------------------------------------------------------
ticket_id = "ticket_472"
ticket_text = (
    "Customer reports intermittent 502 errors during Stripe checkout after the latest deployment. "
    "Plan: Business tier. Browser: Chrome 126. Region: US-East."
)
# ticket_text = (
#     "Customer reports the main company website is returning 404 Not Found."
#     "Plan: Free tier. Browser: Safari. Region: EU-West-2."
# )

user_prompt = f"""
Triage this ticket.

TICKET_ID: {ticket_id}
TICKET_TEXT:
\"\"\"{ticket_text}\"\"\"

Requirements:
- Use kb_search() to look for known issues (e.g., 'stripe', '502', 'deploy', 'checkout').
- If appropriate, propose a ticket update via ticket_update() (status & short note).
- Draft a concise customer email via email_draft() with 2–3 bullet points.
- Return ONLY the JSON specified in the instructions.
"""

result = Runner.run_sync(support_agent, user_prompt)
print(result.final_output)