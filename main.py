from datetime import datetime
from flask import Flask, jsonify, request
from resources.resource_x import ResourceX
from resources.resource_y import ResourceY
from config import RESOURCE_IDS

app = Flask(__name__)


@app.route('/')
def index():
    """Home route, returns success json object"""
    return jsonify({'Success': True}), 200


@app.route('/resource/access', methods=['POST'])
def get_access():
    """Route to acquire access to a resource, grant the access or returns timeout"""
    if request.method == 'POST':
        params = request.json
        try:
            # Get params sent
            acquirer_id = params['id']
            resource = params['resource']
        except KeyError:
            # If params not found returns success=false
            return jsonify({
                'success': False, 'message': 'Could not process this request'
                }), 400

        # If resource is not supported, returns success=false
        if resource not in RESOURCE_IDS:
            return jsonify({
                'success': False, 'message': 'Resource not supported'
                }), 400

        # get an instance of obtained resource
        resource_instance = eval(resource)()

        # Grant access if resource not locked, or it is locked but by the same client
        if not resource_instance.resource_locked() \
                or resource_instance.get_acquirer() == acquirer_id:
            resource_instance.lock_resource(acquirer_id)
            return jsonify({
                'success': True, 'granted': True
                }), 200

        # If resource is locked add caller id to the resource's queue
        resource_instance.add_request(acquirer_id)

        # Check if request has timeout or resource is released
        timeout = datetime.now() + resource_instance.timeout_in_seconds
        while True:
            if datetime.now() > timeout:
                resource_instance.remove_request(acquirer_id)
                return jsonify({
                    'success': False, 'message': 'Request timed out'
                }), 408

            # grant access if resource is released and acquirer is the next in the resource queue
            if not resource_instance.resource_locked():
                if resource_instance.next() == acquirer_id:
                    resource_instance.lock_resource(acquirer_id)
                    # remove request from queue
                    resource_instance.remove_request(acquirer_id)
                    return jsonify({
                        'success': True, 'granted': True
                    }), 200


@app.route('/resource/release', methods=['POST'])
def release_resource():
    """Route to release resource"""
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

        # Release resource if it was held by the caller
        if eval(resource).release_resource(acquirer_id):
            return jsonify({
                'success': True, 'message': 'Resource is released'
            }), 200

        # Return success=False if the caller was not the holder of the resource
        return jsonify({
            'success': False, 'message': 'Resource is not acquired by the caller'
        }), 400


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
