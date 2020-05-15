import os
from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/terminal', methods=['POST'])
def get_tasks():
    b = request.json['cmd']
    a = (subprocess.check_output(b, shell=True)).decode('utf-8')
    return jsonify(a)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)