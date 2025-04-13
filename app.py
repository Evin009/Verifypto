from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
from verifier import analyze_wallet
from mongodb_setup import save_verification, get_all_verifications, get_by_wallet
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider  # ✅ NEW!

# === Flask App Setup ===
app = Flask(__name__)
CORS(app)

# ✅ Fix for ObjectId serialization (for Flask ≥ 2.3)
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json_provider_class = CustomJSONProvider
app.json = app.json_provider_class(app)

# === Routes ===

@app.route('/')
def home():
    return "🎉 Flask backend is working with Ngrok!"

@app.route('/verify', methods=['GET'])
def verify():
    wallet = request.args.get("wallet")
    contract = request.args.get("contract")

    if not wallet:
        return jsonify({"error": "Missing wallet address"}), 400

    result = analyze_wallet(wallet, contract)
    save_verification(result)
    return jsonify(result)

@app.route('/history', methods=['GET'])
def history():
    return jsonify(get_all_verifications())

@app.route('/history/<wallet>', methods=['GET'])
def wallet_history(wallet):
    return jsonify(get_by_wallet(wallet))

# === Run with Ngrok ===
if __name__ == '__main__':
    port = 5000
    public_url = ngrok.connect(port)
    print(f"\n🚀 Ngrok tunnel running at: {public_url}\n")
    print("🔁 Use CTRL+C to stop the tunnel\n")

    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
