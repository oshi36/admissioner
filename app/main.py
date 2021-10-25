"""Validating webhook for the Kubernetes admission controller."""
from flask import Flask, request, jsonify

admission_controller = Flask(__name__)

@admission_controller.route('/validate/deployments', methods=['POST'])

def deployment_webhook():
    """Handler for the validate route."""
    req_info = request.get_json()["request"]["object"]["metadata"]

    if req_info["labels"].get("production"):
        if req_info["labels"]["production"] != "true" or req_info["labels"]["production"] != "false":
            return admission_response(False, f"Invalid value for `production` label in Deployment {req_info['name']}")
        return admission_response(True, f"Deployment {req_info['name']} has `production` label.")
        
    
    return admission_response(False, f"Deployment {req_info['name']} doesn't have `production` label.")

def admission_response(allowed, message):
    """Create admission response."""
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})

if __name__ == '__main__':
    """Running flask server with TLS certs"""
    admission_controller.run(host='0.0.0.0', port=443, ssl_context=("./certs/server.crt", "./certs/server.key"))
