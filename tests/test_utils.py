import os
import tempfile
import pytest
from app import utils


def test_needs_conversion():
    assert utils.needs_conversion("mp3") is False
    assert utils.needs_conversion("wav") is False
    assert utils.needs_conversion("m4a") is False
    assert utils.needs_conversion("ogg") is True
    assert utils.needs_conversion("flac") is True


def test_remove_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"test")
    assert os.path.exists(tmp_path)
    utils.remove_file(tmp_path)
    assert not os.path.exists(tmp_path)


def test_remove_nonexistent_file(caplog):
    utils.remove_file("nonexistent.file")
    assert "does not exist" in caplog.text


def test_convert_to_mp3_invalid_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"not an audio file")
    with pytest.raises(Exception):
        utils.convert_to_mp3(tmp_path)
