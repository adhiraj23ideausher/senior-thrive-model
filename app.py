from flask import Flask, request, jsonify
from img_recog import caption_image
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'msg': 'Welcome to SeniorThrive model API!'})

@app.route('/scan', methods=['POST'])
def scan_image():
    if not request.json or 'img_url' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'No img_url provided'}), 400
    img_url = request.json['img_url']
    prompt = caption_image(img_url)
    return jsonify({
        'prompt': prompt
    })
    

if __name__ == "__main__":
    app.run(debug=True)
