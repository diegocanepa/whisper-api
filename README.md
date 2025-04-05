# Whisper API - FastAPI + OpenAI Whisper

A simple API for audio transcription using OpenAI's Whisper model.

Deployed on Railway.

---

## Endpoints

### POST `/transcribe`

Transcribes an audio file.

#### Request

- Content-Type: `multipart/form-data`
- Parameters:
  - `file`: Audio file (`wav`, `mp3`, `m4a`, `ogg`, etc.)

#### Response

```json
{
  "text": "Transcribed text"
}
```

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/your-user/whisper-api.git
cd whisper-api
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

---

## Deployment on Railway

1. Create a new project on [Railway](https://railway.app/)
2. Connect this repository
3. Railway will automatically detect the `Dockerfile`
4. Deploy!

Your API will be available at:

```
https://<your-app>.up.railway.app
```

---

## Notes

- By default, the `base` Whisper model is used.
- You can change the model in `app/transcriber.py` to `small`, `medium`, or `large` depending on your needs and resource limits.
- If you are on the free Railway plan (512MB RAM), using larger models is not recommended.

---

## Future Improvements (Optional)

- [ ] Support multiple languages
- [ ] Add proper logging
- [ ] Improve error handling
- [ ] Basic unit tests
- [ ] Multi-stage Docker build optimization