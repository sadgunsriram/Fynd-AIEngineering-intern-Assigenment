import os
from task_2.config import Config
from dotenv import load_dotenv
load_dotenv()
model_name="gemini-2.5-flash"
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print("DEBUG KEY:", os.getenv("GEMINI_API_KEY"))         

USER_PROMPT_TEMPLATE = """
You are a friendly customer support agent.

Customer rating: {rating} star(s)
Customer review: "{review}"

Write a short, empathetic response directly addressing the customer.
Tone:
- Polite
- Concise
- Human-like
- Match the sentiment
"""

ADMIN_PROMPT_TEMPLATE = """
You are an internal quality analyst for a retail platform.

Rating: {rating}
Review: "{review}"

1. One-sentence summary.
2. One recommended action.

Return JSON:

{
 "summary": "",
 "recommended_action": ""
}
"""

def _call_llm(prompt: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_user_response(rating, review):
    prompt = USER_PROMPT_TEMPLATE.format(rating=rating, review=review)
    return _call_llm(prompt)

def generate_admin_summary_and_action(rating, review):
    import json, re

    raw = _call_llm(ADMIN_PROMPT_TEMPLATE.format(rating=rating, review=review))
    try:
        return json.loads(raw)["summary"], json.loads(raw)["recommended_action"]
    except:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            obj = json.loads(match.group(0))
            return obj.get("summary", ""), obj.get("recommended_action", "")
    return "", ""


