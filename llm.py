import os
# from config import Config
# from config import Config
from task_2.config import Config



from dotenv import load_dotenv
load_dotenv()


import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


USER_PROMPT_TEMPLATE = """
You are a friendly customer support agent.

Customer rating: {rating} star(s)
Customer review: "{review}"

Write a short, empathetic response directly addressing the customer.
Tone:
- Polite
- Concise
- Human-like
- Match the sentiment (apologetic for low ratings, thankful for high ratings)

Return only the response text, no explanations.
"""

ADMIN_PROMPT_TEMPLATE = """
You are an internal quality analyst for a retail platform.

Given this rating and review:

Rating: {rating} star(s)
Review: "{review}"

1. Summarize the core customer issue or compliment in ONE concise sentence.
2. Suggest ONE concrete action item for the internal team (e.g., "Improve delivery speed", "Praise the support team", etc.).

Return your answer in JSON:

{{
  "summary": "<one-sentence summary>",
  "recommended_action": "<one-sentence action>"
}}
"""


def _call_llm(prompt: str, json_mode: bool = False):
    
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt)
    return resp.text


def generate_user_response(rating: int, review: str) -> str:
    prompt = USER_PROMPT_TEMPLATE.format(rating=rating, review=review)
    return _call_llm(prompt, json_mode=False).strip()


def generate_admin_summary_and_action(rating: int, review: str):
    import json, re

    prompt = ADMIN_PROMPT_TEMPLATE.format(rating=rating, review=review)
    raw = _call_llm(prompt, json_mode=False)

    # Attempt JSON extraction
    try:
        obj = json.loads(raw)
        return obj.get("summary", "").strip(), obj.get("recommended_action", "").strip()
    except Exception:
        # Fallback: try to loosely parse {...}
        try:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                obj = json.loads(match.group(0))
                return obj.get("summary", "").strip(), obj.get("recommended_action", "").strip()
        except Exception:
            pass
    return "", ""
