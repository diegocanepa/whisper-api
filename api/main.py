from fastapi import FastAPI, UploadFile, File
from app.transcriber import transcribe_audio

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_path = f"/tmp/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    
    text = transcribe_audio(audio_path)
    return {"text": text}