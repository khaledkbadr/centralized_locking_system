from datetime import datetime
from flask import Flask, jsonify, request
from resources.resource_x import ResourceX
from resources.resource_y import ResourceY

app = Flask(__name__)

RESOURCE_IDS = set(['ResourceX', 'ResourceY'])


@app.route('/')
def index():
    return jsonify({'Success': True}), 200


@app.route('/access/resource', methods=['POST'])
def get_access():
    if request.method == 'POST':
        params = request.json
        try:
            acquirer_id = params['id']
            resource = params['resource']
        except KeyError:
            return jsonify({
                'success': False, 'message': 'Could not process this request'
                }), 400

        if resource not in RESOURCE_IDS:
            return jsonify({
                'success': False, 'message': 'Resource not supported'
                }), 400

        resource_instance = eval(resource)()
        if not resource_instance.resource_locked() \
                or resource_instance.get_acquirer() == acquirer_id:
            resource_instance.lock_resource(acquirer_id)
            return jsonify({
                'success': True, 'granted': True
                }), 200

        resource_instance.add_request(acquirer_id)

        timeout = datetime.now() + resource_instance.timeout_in_seconds
        while True:
            if datetime.now() > timeout:
                resource_instance.remove_request()
                return jsonify({
                    'success': False, 'message': 'Request timed out'
                }), 408

            if not resource_instance.resource_locked():
                if resource_instance.next() == acquirer_id:
                    resource_instance.remove_request()
                    return jsonify({
                        'success': True, 'granted': True
                    }), 200

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
