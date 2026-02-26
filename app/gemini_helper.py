import os
from typing import List, Dict, Any, Optional
GEMINI_API_KEY="AIzaSyDE8uE5rNSWoFjm04a_gazeoWoEtNdvpcM" #key recomm. 
try:
    import google.generativeai as genai
except Exception:
    genai = None

MODEL = "gemini-3-flash-preview"


def init_gemini():
    api = GEMINI_API_KEY
    if not api or genai is None:
        return None
    genai.configure(api_key=api)
    return genai.GenerativeModel(MODEL)


def get_recommendations_from_gemini(user: Dict[str, Any], schemes: List[Dict[str, Any]]) -> str:
    """
    Gemini is the ONLY source of recommendations.
    No JSON filtering or rule-based matching.
    """

    model = init_gemini()
    if not model:
        return "AI is not active. Please set GEMINI_API_KEY."

    prompt = f"""
You are Yojna Mitra, an assistant who recommends Indian government schemes.

User profile:
{user}

Available schemes:
{schemes}

Your task:
- Analyze ALL schemes.
- Recommend the best schemes.
- Give me link and steps to apply for each recommended scheme.
- Explain why each scheme fits based on the user profile.
- Keep the output short, friendly, and in bullet points.
- Do not mention filtering rules or scoring.
"""

    try:
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception as e:
        return f"Error from Gemini: {e}"