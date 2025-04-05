from flask import Flask, request, jsonify
from app.transcriber import transcribe_audio
import uuid
import os

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"})

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    audio_path = f"/tmp/{uuid.uuid4()}.wav"
    file.save(audio_path)

    text = transcribe_audio(audio_path)
    os.remove(audio_path)

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
