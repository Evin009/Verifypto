import google.generativeai as genai
from config_example import GEMINI_API_KEY

# Configure Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini Pro model once (reuse for efficiency)
model = genai.GenerativeModel("models/gemini-2.0-flash")

def analyze_with_gemini(data):
    """
    Uses Gemini to analyze on-chain Ethereum data (wallets, tokens, contracts)
    and returns a structured risk assessment.
    """
    # Clean and formatted prompt
    prompt = f"""
You are a blockchain security AI trained to assess Ethereum wallets and token contracts.

You will receive extracted on-chain data such as:
- Risk score (computed heuristically)
- Flags like 'blacklist', 'onlyOwner', 'unverified contract'
- Activity level (txs and token transfers)
- Token supply, contract type, and metadata

Your task:
✅ Analyze the input below
✅ Return ONLY this JSON format:

{{
  "verdict": "Safe" | "Medium Risk" | "Likely Scam",
  "score": 0–10,
  "summary": "Concise reason"
}}

Guidelines:
- If the address matches known trusted tokens (e.g., USDT, USDC, WETH), mark as "Safe" even if 'blacklist' or 'onlyOwner' are present — those are expected.
- If 'blacklist', 'onlyOwner', and 'unverified contract' are present in unknown or low-activity contracts, raise the risk significantly.
- If there are fewer than 5 transactions and no token transfers, classify at least as "Medium Risk".
- If 'risk_score' is 6 or higher, default to "Likely Scam" unless trusted.
- Never include markdown or explanation outside the JSON.
- Be decisive — never say "could be".

On-chain wallet and contract input:
```json
{data}


"""

    try:
        response = model.generate_content(prompt)
        analysis_text = response.candidates[0].content.parts[0].text

        # Optional: Try to parse it to a dict (if you want to return it as structured data)
        # import json
        # result = json.loads(analysis_text)
        # return result

        return analysis_text  # Raw JSON string (as returned by Gemini)

    except Exception as e:
        return {
            "error": "Gemini analysis failed.",
            "details": str(e)
        }

