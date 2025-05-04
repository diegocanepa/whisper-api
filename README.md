# 🗣️ FastAPI OpenAI Transcription Service

This is a lightweight FastAPI-based API service that uses [OpenAI's Speech-to-Text API](https://platform.openai.com/docs/guides/speech-to-text) (Whisper / GPT-4o Transcribe) to transcribe audio files to text.

## 🚀 Features

- Transcribe `.mp3` audio using OpenAI Whisper or GPT-4o
- Upload audio via HTTP POST
- Returns clean, accurate transcription
- Includes logging and error handling
- Loads API key from `.env`
- Docker-ready for easy deployment


---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/openai-transcription-api.git
cd openai-transcription-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `.env` file

Create a `.env` file in the root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ▶️ Run Locally

```bash
uvicorn main:app --reload
```

Access interactive docs at:  
http://localhost:8000/docs

---

## 🐳 Run with Docker

### Build the image

```bash
docker build -t transcriber .
```

### Run the container

```bash
docker run -p 8000:8000 --env-file .env transcriber
```

---

## 📤 API Usage

### `POST /transcribe/`

Uploads an audio file and returns transcription.

#### Form Data:

- `file`: audio file (.mp3 format recommended)

#### Example (using `curl`):

```bash
curl -X POST http://localhost:8000/transcribe/ \
  -F "file=@/path/to/audio.mp3"
```

#### Response:

```json
{
  "transcription": "Hello, this is a transcribed message."
}
```

---

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/)
- [Python 3.11](https://www.python.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)
