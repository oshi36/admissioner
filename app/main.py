from flask import Flask, request, jsonify

admission_controller = Flask(__name__)

@admission_controller.route('/validate/deployments', methods=['POST'])

def deployment_webhook():
    req_info = request.get_json()["request"]["object"]["metadata"]

    if req_info["labels"].get("production"):
        return admission_response(True, "Deployment %s has `production` label." % req_info["name"])
    
    return admission_response(False, "Deployment %s doesn't have `production` label." % req_info["name"])

def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})

if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', port=443, ssl_context=("./certs/server.crt", "./certs/server.key"))
