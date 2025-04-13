import requests
from config_example import ETHERSCAN_API_KEY

BASE_URL = "https://api.etherscan.io/api"

# checks wallet transaction
def get_wallet_transactions(address):
    url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=txlist"
        f"&address={address}"
        f"&startblock=0&endblock=99999999"
        f"&sort=desc&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    return response.json()

# checks token transfer
def get_token_transfers(address):
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&apikey={ETHERSCAN_API_KEY}"
    return requests.get(url).json()

# checks smart contract
def get_contract_source(address):
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API_KEY}"
    return requests.get(url).json()

def get_token_total_supply(contract_address):
    url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={contract_address}&apikey={ETHERSCAN_API_KEY}"
    return requests.get(url).json()

def is_contract_address(address):
    """
    Returns True if the address is a smart contract (has deployed bytecode).
    Uses Etherscan Proxy API with eth_getCode.
    """
    url = (
        f"https://api.etherscan.io/api"
        f"?module=proxy"
        f"&action=eth_getCode"
        f"&address={address}"
        f"&apikey={ETHERSCAN_API_KEY}"
    )
    try:
        response = requests.get(url)
        result = response.json().get("result", "0x")
        # If bytecode is not empty, it's a contract
        return result != "0x"
    except Exception as e:
        print(f"[ERROR] Checking contract status for {address}: {e}")
        return False


    
def is_verified_contract(address):
    contract_data = get_contract_source(address)
    result = contract_data.get("result", [])

    if isinstance(result, list) and len(result) > 0:
        source = result[0]
        if isinstance(source, dict):
            abi = source.get("ABI", "")
            return abi != "" and abi != "Contract source code not verified"

    return False



