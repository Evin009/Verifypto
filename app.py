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
    template_folder='frontend/templates',
    static_folder='frontend/static'
)

# Enable CORS with proper configuration
CORS(app, resources={r"/*": {"origins": "*"}})

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
    return render_template('index.html')

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

# Fix: Properly handle email parameter and add error handling
@app.route('/user-history')
def user_history():
    email = request.args.get("email")
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
        
    try:
        history_data = get_by_user(email)
        return jsonify(history_data)
    except Exception as e:
        print(f"Error in user-history: {str(e)}")
        return jsonify({"error": f"Failed to fetch history: {str(e)}"}), 500

# === API Routes for JS/Frontend fetch() ===
@app.route('/verify', methods=['GET'])
def verify():
    wallet = request.args.get("wallet")
    contract = request.args.get("contract")
    email = request.args.get("email")  # Fix: Ensure email is captured
    uid = request.args.get("uid")
    
    print(f"💬 VERIFY ROUTE HIT: Wallet: {wallet}, Contract: {contract}, Email: {email}")

    if not wallet:
        return jsonify({"error": "Missing wallet address"}), 400

    try:
        # Fix: Make sure email gets included in the result
        result = analyze_wallet(wallet, contract)
        if email:
            result["email"] = email
        if uid:
            result["uid"] = uid
            
        save_verification(result)
        print("✅ Sending JSON result:", result)
        return jsonify(result)
    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
@app.route('/history', methods=['GET'])
def history():
    try:
        data = get_all_verifications()
        print("📜 History data retrieved")
        return jsonify(data)
    except Exception as e:
        print("❌ Error in /history:", str(e))
        return jsonify({"error": f"Failed to fetch history: {str(e)}"}), 500

@app.route('/history/<wallet>', methods=['GET'])
def wallet_history(wallet):
    try:
        data = get_by_wallet(wallet)
        return jsonify(data)
    except Exception as e:
        print(f"❌ Error getting wallet history for {wallet}: {str(e)}")
        return jsonify({"error": f"Failed to fetch wallet history: {str(e)}"}), 500

# === Run with Ngrok ===
if __name__ == '__main__':
    port = 5000
    try:
        public_url = ngrok.connect(port)
        print(f"\n🚀 Ngrok tunnel running at: {public_url}\n")
        print("🔁 Use CTRL+C to stop the tunnel\n")
        
        # Update the BACKEND_URL in index.html or provide it as a variable
        print(f"⚠️ Make sure your frontend's BACKEND_URL is set to: {public_url}")
        
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    except Exception as e:
        print(f"❌ Failed to start Ngrok: {str(e)}")
