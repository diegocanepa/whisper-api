import io
import pytest
from fastapi.testclient import TestClient
from app.api import app
from unittest.mock import patch

client = TestClient(app)


def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status():
    response = client.head("/status")
    assert response.status_code == 200


def test_transcribe_no_file():
    response = client.post("/transcribe")
    assert response.status_code == 422


def test_transcribe_invalid_audio():
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", b"not audio")}
    )
    assert response.status_code == 400
    assert "Invalid audio file or corrupted file." in response.json()["detail"]


def test_transcribe_voice_test_ogg_mocked():
    fake_transcription = "Esto es una prueba de voz."
    audio_path = "tests/voice_test.ogg"
    with open(audio_path, "rb") as audio_file:
        with patch("app.api.audio_processor.transcribe", return_value=fake_transcription):
            response = client.post(
                "/transcribe",
                files={"file": ("voice_test.ogg", audio_file, "audio/ogg")}
            )
    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert "prueba de voz" in data["transcription"].lower()

