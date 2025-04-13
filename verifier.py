from etherscan_helper import (
    get_wallet_transactions,
    get_token_transfers,
    get_contract_source,
    get_token_total_supply,
    is_contract_address
)
from gemini_helper import analyze_with_gemini
import json
import re

# ✅ Known trusted tokens that should not be flagged as scams
TRUSTED_CONTRACTS = {
    "0xdAC17F958D2ee523a2206206994597C13D831ec7": "USDT",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "WETH",
    "0xF977814e90dA44bFA03b6295A0616a897441aceC": "Binance Cold Wallet"
}

def clean_gemini_json(text):
    return re.sub(r"```json|```", "", text).strip()

def analyze_wallet(wallet_address, contract_address=None):
    is_contract = is_contract_address(wallet_address)
    if contract_address is None and is_contract:
        contract_address = wallet_address

    report = {
        "wallet": wallet_address,
        "contract": contract_address,
        "verdicts": [],
        "risk_score": 0,
        "is_contract": is_contract,
        "score_breakdown": [],
        "tags": []
    }

    # Wallet activity
    tx_data = get_wallet_transactions(wallet_address)
    txs = tx_data.get("result", [])
    if len(txs) < 5:
        report["verdicts"].append("🔍 Wallet is newly created or has low activity")
        report["risk_score"] += 2
        report["score_breakdown"].append({"reason": "Low transaction count", "points": 2})

    # Token transfers
    token_data = get_token_transfers(wallet_address)
    tokens = token_data.get("result", [])
    if len(tokens) == 0:
        report["verdicts"].append("❌ No ERC-20 token transfers found")
        report["risk_score"] += 1
        report["score_breakdown"].append({"reason": "No ERC-20 token transfers", "points": 1})

    # Contract analysis
    if contract_address:
        contract_data = get_contract_source(contract_address)
        source_list = contract_data.get("result", [])
        if source_list and isinstance(source_list[0], dict):
            source = source_list[0]
            abi_status = source.get("ABI", "")
            if abi_status == "Contract source code not verified":
                report["verdicts"].append("🚫 Smart contract is unverified")
                report["risk_score"] += 5
                report["score_breakdown"].append({"reason": "Smart contract is unverified", "points": 5})
            else:
                code = source.get("SourceCode", "").lower()
                if "blacklist" in code:
                    report["verdicts"].append("⚠️ 'blacklist' function found in contract")
                    report["risk_score"] += 3
                    report["score_breakdown"].append({"reason": "'blacklist' function found in contract", "points": 3})
                if "onlyowner" in code:
                    report["verdicts"].append("⚠️ 'onlyOwner' privilege detected")
                    report["risk_score"] += 3
                    report["score_breakdown"].append({"reason": "'onlyOwner' privilege detected", "points": 3})

    # Token supply
    if contract_address:
        supply_data = get_token_total_supply(contract_address)
        total_supply = supply_data.get("result", "0")
        report["total_supply"] = total_supply

    # ✅ Override risk if this is a trusted contract
    if contract_address in TRUSTED_CONTRACTS:
        report["verdicts"].append(f"✅ Trusted contract: {TRUSTED_CONTRACTS[contract_address]}")
        report["score_breakdown"] = []
        report["risk_score"] = 0
        report["tags"].append("trusted")
        report["tags"].append("centralized-control")
        report["verdict"] = "Safe"
        report["summary"] = f"{TRUSTED_CONTRACTS[wallet_address]} — known safe entity"

    # Call Gemini
    gemini_input = {
        "wallet": wallet_address,
        "contract": contract_address,
        "risk_score": report["risk_score"],
        "verdicts": report["verdicts"],
        "total_supply": report.get("total_supply", "N/A")
    }

    gemini_input_json = json.dumps(gemini_input)
    gemini_response = analyze_with_gemini(gemini_input_json)

    if isinstance(gemini_response, str):
        try:
            clean_response = clean_gemini_json(gemini_response)
            gemini_result = json.loads(clean_response)
        except json.JSONDecodeError as e:
            gemini_result = {
                "verdict": "Could not parse",
                "score": 0,
                "summary": gemini_response,
                "error": str(e)
            }
    else:
        gemini_result = gemini_response

    if isinstance(gemini_result, dict) and gemini_result.get("score", 0) < report["risk_score"]:
        gemini_result["score"] = report["risk_score"]
        gemini_result["verdict"] = "Likely Scam" if report["risk_score"] >= 6 else "Medium Risk"
        gemini_result["summary"] += " (Adjusted based on on-chain risk signals.)"

    # Final response
    report["gemini_analysis"] = gemini_result
    report["verdict"] = gemini_result.get("verdict", "Unknown")
    report["summary"] = gemini_result.get("summary", "")
    report["ai_score"] = gemini_result.get("score", 0)

    return report


