
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pyngrok import ngrok
from verifier import analyze_wallet
from mongodb_setup import save_verification, get_all_verifications, get_by_wallet, get_by_user, get_top_riskiest
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
import os

# === Flask App Setup ===
app = Flask(
    __name__,
    template_folder='frontend/templates',  # Make sure this folder exists
    static_folder='frontend/static'        # For CSS/JS if needed
)

CORS(app)

# === Fix for ObjectId serialization ===
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json_provider_class = CustomJSONProvider
app.json = app.json_provider_class(app)

# === Web Interface Routes ===

@app.route('/')
def index():
    return render_template('index.html')  # Loads the main HTML frontend


@app.route('/auth')
def auth():
    return render_template("auth.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/process', methods=['POST'])
def process_form():
    wallet = request.form.get("wallet")
    contract = request.form.get("token") or None

    if not wallet:
        return "❌ Wallet address is required!", 400

    result = analyze_wallet(wallet, contract)
    save_verification(result)

    return render_template('result.html', result=result)

@app.route('/user-history')
def user_history():
    email = request.args.get("email")
    return jsonify(get_by_user(email))

# === API Routes for JS/Frontend fetch() ===

@app.route('/verify', methods=['GET'])
def verify():
    wallet = request.args.get("wallet")
    contract = request.args.get("contract")
    uid = request.args.get("uid")
    
    print("💬 VERIFY ROUTE HIT:")
    print(f"Wallet: {wallet}, Contract: {contract}")

    if not wallet:
        return jsonify({"error": "Missing wallet address"}), 400

    try:
        result = analyze_wallet(wallet, contract)
        save_verification(result)
        print("✅ Sending JSON result:", result)
        return jsonify(result)
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/history', methods=['GET'])
def history():
    try:
        data = get_all_verifications()
        print("📜 History data:", data)
        return jsonify(data)
    except Exception as e:
        print("❌ Error in /history:", str(e))
        return jsonify({"error": str(e)}), 500
    #     return jsonify(get_all_verifications())
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

@app.route('/history/<wallet>', methods=['GET'])
def wallet_history(wallet):
    try:
        return jsonify(get_by_wallet(wallet))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run with Ngrok ===
if __name__ == '__main__':
    port = 5000
    public_url = ngrok.connect(port)
    print(f"\n🚀 Ngrok tunnel running at: {public_url}\n")
    print("🔁 Use CTRL+C to stop the tunnel\n")

    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
