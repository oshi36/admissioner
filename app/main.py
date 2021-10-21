from flask import Flask, request, jsonify

admission_controller = Flask(__name__)

@admission_controller.route('/validate/deployments', methods=['POST'])
def validate_webhook():
    req_info = request.get_json()["request"]["object"]["metadata"]

    if req_info["labels"].get("env"):
        return admission_response(True, "%s will be deployed in %s environment." % (req_info["name"], req_info["labels"].get("env")))
    
    return admission_response(False, "Label `env` is not defined for application %s" % req_info["name"])

@admission_controller.route('/mutate/deployments', methods=['POST'])
def mutate_webhook():
    req_info = request.get_json()["request"]["object"]["metadata"]

    if req_info["labels"].get("bound"):
        bound = req_info["labels"]["bound"]
        if bound == "cpu":
            return admission_response_patch("%s uses cpu-bound schedulder" % req_info["name"], json_patch = jsonpatch.JsonPatch([{"op": "add", "path": "/spec/schedulerName", "value": "cpu-bound"}]))
        elif bound == "memory":
            return admission_response_patch("%s uses memory-bound schedulder" % req_info["name"], json_patch = jsonpatch.JsonPatch([{"op": "add", "path": "/spec/schedulerName", "value": "memory-bound"}]))
        else:
            return admission_response_patch("%s uses storage-bound schedulder" % req_info["name"], json_patch = jsonpatch.JsonPatch([{"op": "add", "path": "/spec/schedulerName", "value": "storage-bound"}]))

def admission_response_patch(message, json_patch):
    base64_patch = base64.b64encode(json_patch.to_string().encode("utf-8")).decode("utf-8")
    return jsonify({"response": {"status": {"message": message},
                                 "patchType": "JSONPatch",
                                 "patch": base64_patch}})

def admission_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})

if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', port=443, ssl_context=("./certs/server.crt", "./certs/server.key"))
