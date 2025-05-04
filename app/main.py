import logging
from flask import Flask, request, jsonify
from app.transcriber import WhisperTranscriber
import tempfile
import os

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

transcriber = WhisperTranscriber(model_size="tiny")


@app.route("/status", methods=["GET"])
def status():
    """
    Health check endpoint.
    """
    logging.info("Status check requested.")
    return jsonify({"status": "ok"}), 200


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Endpoint for transcribing an uploaded audio file.
    """
    logging.info("Received transcription request.")

    if 'file' not in request.files:
        logging.warning("No file part in the request.")
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        logging.warning("Uploaded file has empty filename.")
        return jsonify({"error": "Empty filename"}), 400

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            file.save(tmp.name)
            audio_path = tmp.name
            logging.info(f"Saved uploaded file to: {audio_path}")

        text = transcriber.transcribe(audio_path)
        logging.info("Transcription completed successfully.")

    except Exception as e:
        logging.exception("Error during transcription:")
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logging.info(f"Temporary file deleted: {audio_path}")

    return jsonify({"text": text})


if __name__ == "__main__":
    logging.info("Starting Flask app on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=False)
