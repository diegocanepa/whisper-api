import whisper

model = whisper.load_model("tiny")

def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe(audio_path, language="es")
    return result["text"]