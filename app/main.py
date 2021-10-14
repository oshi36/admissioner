from flask import Flask, request, jsonify

admission_controller = Flask(__name__)

@admission_controller.route('/validate/deployments', methods=['POST'])

def deployment_webhook():
    req_info = request.get_json()["request"]["object"]["metadata"]

    if req_info["labels"].get("env"):
        return admission_response(True, "%s will be deployed in %s environment." % (req_info["name"], req_info["labels"].get("env")))
    
    return admission_response(False, "Label `env` is not defined for application %s" % req_info["name"])

def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})

if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', port=443, ssl_context=("/server.crt", "/server.key"))
