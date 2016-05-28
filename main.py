from flask import Flask, jsonify
from resources.resource_x import ResourceX
from resources.resource_y import ResourceY

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'Success': True}), 200


@app.route('/access', methods=['POST'])
def get_access():
    if request.method == 'POST':
        pass


if __name__ == "__main__":
    app.run(debug=True)
