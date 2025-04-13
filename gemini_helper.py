import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_with_gemini(data):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
You are a blockchain security analyst AI.

Analyze the following Etherscan-derived data and return:
1. "verdict" (Safe / Medium Risk / Likely Scam)
2. "score" (0-10, higher = riskier)
3. "summary" (brief human-readable summary)

Data:
{data}
"""

    response = model.generate_content(prompt)
    return response.text

