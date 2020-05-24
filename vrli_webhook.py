from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/vrli_webhook', methods=['POST'])
def return_ok():
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)