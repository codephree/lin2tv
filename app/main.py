from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory store for demo
links = {}

@app.route('/api/generate', methods=['POST'])
def generate():
    link = request.form.get('link') or request.json.get('link')
    if not link:
        return jsonify({'error': 'No link provided'}), 400
    code = str(abs(hash(link)))[:6]
    links[code] = link
    return jsonify({'code': code})

@app.route('/api/retrieve', methods=['GET'])
def retrieve():
    code = request.args.get('code')
    link = links.get(code)
    if not link:
        return jsonify({'error': 'Code not found'}), 404
    return jsonify({'link': link})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
