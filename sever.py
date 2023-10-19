from flask import Flask, jsonify
import browser_cookie3

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    # Your existing code to get secure_1psid_cookie44444444444444 
    url = 'https://bard.google.com/'
    cj = browser_cookie3.firefox()
    secure_1psid_cookie = None

    for cookie in cj:
        if cookie.name == '__Secure-1PSID':
            secure_1psid_cookie = cookie.value
            break

    return jsonify({'msg': secure_1psid_cookie})

if __name__ == '__main__':
    # Change the host from 'localhost' to '0.0.0.0' to allow access from any device on the network.
    app.run(debug=True, host='192.168.1.44', port=5001)
 