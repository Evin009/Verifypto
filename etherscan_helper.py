import requests
from config import ETHERSCAN_API_KEY

BASE_URL = "https://api.etherscan.io/api"

# checks wallet transaction
def get_wallet_transactions(wallet_address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    return requests.get(BASE_URL, params=params).json()

# checks token transfer
def get_token_transfers(wallet_address):
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    return requests.get(BASE_URL, params=params).json()

# checks smart contract
def get_contract_source(contract_address):
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }
    return requests.get(BASE_URL, params=params).json()

#checks token suppy
def get_token_total_supply(contract_address):
    params = {
        "module": "stats",
        "action": "tokensupply",
        "contractaddress": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }
    return requests.get(BASE_URL, params=params).json()
