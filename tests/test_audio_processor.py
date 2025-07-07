import tempfile
import pytest
from fastapi import HTTPException
from app.audio_processor import AudioProcessor


class DummyTranscriptionClient:
    def __init__(self):
        self.audio = self
        self.transcriptions = self

    def create(self, model, file):
        return type("Response", (), {"text": "Dummy transcription"})


@pytest.fixture
def processor():
    return AudioProcessor(DummyTranscriptionClient(), "dummy-model")


def test_save_uploaded_file(processor):
    class DummyUploadFile:
        filename = "test.wav"
        file = tempfile.TemporaryFile()
        file.write(b"testdata")
        file.seek(0)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = f"{tmpdir}/test.wav"
        processor.save_uploaded_file(DummyUploadFile(), path)
        with open(path, "rb") as f:
            content = f.read()
        assert content == b"testdata"


def test_get_audio_duration_invalid_file(processor):
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b"invalid audio")
        tmp.flush()
        with pytest.raises(Exception):
            processor.get_audio_duration_seconds(tmp.name)


def test_validate_duration(processor):
    # No max_duration -> no error
    processor.validate_duration(100, None)

    # Duration within limit
    processor.validate_duration(50, 60)

    # Duration exceeding
    with pytest.raises(HTTPException):
        processor.validate_duration(70, 60)


def test_transcribe(processor):
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b"dummy")
        tmp.flush()
        result = processor.transcribe(tmp.name)
        assert result == "Dummy transcription"
