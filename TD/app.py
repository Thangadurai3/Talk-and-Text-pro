from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)

OUTPUT_DIR = os.path.join(os.getcwd(), "static")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('language', 'en')

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        output_file = os.path.join(OUTPUT_DIR, "output.mp3")
        tts = gTTS(text, lang=lang)
        tts.save(output_file)

        return jsonify({
            "audio_url": f"http://localhost:5000/static/output.mp3",
            "download_url": f"http://localhost:5000/download/output.mp3"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to process text: {str(e)}"}), 500

@app.route('/static/<path:filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/download/<path:filename>', methods=['GET'])
def download_audio(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
