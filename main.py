from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)
application = app  # ← Esta línea es clave para Render con Gunicorn

SECRET_KEY = os.getenv("BINGX_SECRET_KEY")

@app.route('/')
def home():
    return jsonify({"message": "Server is running"})

@app.route('/sign', methods=['POST'])
def sign():
    data = request.get_json(force=True)
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query = data["query"]
    signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return jsonify({"signature": signature})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
