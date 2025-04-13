from flask import Flask, request, jsonify
from verifier import analyze_wallet

app = Flask(__name__)

@app.route('/verify', methods=['GET'])
def verify():
    wallet = request.args.get("wallet")
    contract = request.args.get("contract")  # optional

    if not wallet:
        return jsonify({"error": "Missing wallet address"}), 400

    result = analyze_wallet(wallet, contract)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
