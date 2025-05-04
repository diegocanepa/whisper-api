import whisper

class WhisperTranscriber:
    """
    A class to transcribe audio to text using OpenAI's Whisper model.

    This class loads a Whisper model upon initialization and provides a method
    to transcribe audio files in Spanish.
    """

    def __init__(self, model_size: str = "tiny"):
        """
        Initialize the transcriber by loading the specified Whisper model.

        Args:
            model_size (str): The size of the Whisper model to load.
                              Options include: 'tiny', 'base', 'small', 'medium', 'large'.
        """
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe an audio file to text in Spanish.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Transcribed text from the audio.
        """
        result = self.model.transcribe(audio_path, language="es")
        return result["text"]
