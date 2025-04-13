from etherscan_helper import (
    get_wallet_transactions,
    get_token_transfers,
    get_contract_source,
    get_token_total_supply
)
from gemini_helper import analyze_with_gemini
import json

def analyze_wallet(wallet_address, contract_address=None):
    report = {
        "wallet": wallet_address,
        "contract": contract_address,
        "verdicts": [],
        "risk_score": 0
    }

    # 1. Wallet Transaction Activity
    tx_data = get_wallet_transactions(wallet_address)
    txs = tx_data.get("result", [])
    if len(txs) < 5:
        report["verdicts"].append("🔍 Wallet is newly created or has low activity")
        report["risk_score"] += 2

    # 2. Token Transfers (ERC-20)
    token_data = get_token_transfers(wallet_address)
    tokens = token_data.get("result", [])
    if len(tokens) == 0:
        report["verdicts"].append("❌ No ERC-20 token transfers found")
        report["risk_score"] += 1

    # 3. Contract Source Code
    if contract_address:
        contract_data = get_contract_source(contract_address)
        source = contract_data.get("result", [])[0]

        if source.get("ABI") == "Contract source code not verified":
            report["verdicts"].append("🚫 Smart contract is unverified")
            report["risk_score"] += 3
        else:
            code = source.get("SourceCode", "").lower()
            if "blacklist" in code:
                report["verdicts"].append("⚠️ 'blacklist' function found in contract")
                report["risk_score"] += 2
            if "onlyowner" in code:
                report["verdicts"].append("⚠️ 'onlyOwner' privilege detected")
                report["risk_score"] += 2

    # 4. Token Supply
    if contract_address:
        supply_data = get_token_total_supply(contract_address)
        total_supply = supply_data.get("result", "0")
        report["total_supply"] = total_supply

    # Prepare for Gemini
    gemini_input = {
        "wallet": wallet_address,
        "contract": contract_address,
        "risk_score": report["risk_score"],
        "verdicts": report["verdicts"],
        "total_supply": report.get("total_supply", "N/A")
    }

    gemini_response = analyze_with_gemini(json.dumps(gemini_input))
    try:
        gemini_result = json.loads(gemini_response)
    except:
        gemini_result = {
            "verdict": "Could not parse",
            "score": 0,
            "summary": gemini_response
        }

    report["gemini_analysis"] = gemini_result
    return report
