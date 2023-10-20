from flask import Flask, jsonify
import browser_cookie3
import socket

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    # Your existing code to get secure_1psid_cookie
    cj = browser_cookie3.firefox()
    secure_1psid_cookie = None

    for cookie in cj:
        if cookie.name == '__Secure-1PSID':
            secure_1psid_cookie = cookie.value
            break

    return jsonify({'msg': secure_1psid_cookie})

if __name__ == '__main__':
    # Get the local IP address of the machine
    host = socket.gethostbyname(socket.gethostname())
    app.run(debug=True, host=host, port=5001)
