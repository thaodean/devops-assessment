import os
from flask import Flask, jsonify, request

app = Flask(__name__)

config_store = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": "1.0.0"}), 200

@app.route('/env', methods=['GET'])
def env():
    current_env = os.environ.get("ENVIRONMENT", "dev")
    return jsonify({"environment": current_env}), 200

@app.route('/config', methods=['POST'])
def create_config():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    value = data.get("value")
    
    if not name:
        return jsonify({"error": "field 'name' is required"}), 400
        
    config_store[name] = value
    return jsonify({"name": name, "value": value}), 200

@app.route('/config/<name>', methods=['GET'])
def get_config(name):
    if name in config_store:
        return jsonify({"name": name, "value": config_store[name]}), 200
    return jsonify({"error": "config item not found"}), 404

@app.route('/config/<name>', methods=['DELETE'])
def delete_config(name):
    config_store.pop(name, None)
    return jsonify({"deleted": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
