import speech_recognition as sr
import logging
from vocalshell.audio_utils import play_listen_sound

logger = logging.getLogger(__name__)

class SpeechRecognizer:
    def __init__(self, model_path=None, use_online=False, config=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.use_online = use_online

    def listen(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            if self.use_online:
                return self.recognizer.recognize_google(audio)
            else:
                from vosk import Model, KaldiRecognizer
                import json
                model = Model("models/vosk-model-en-us-0.22")
                rec = KaldiRecognizer(model, 16000)
                rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
                result = json.loads(rec.Result())
                return result.get("text", "")
        except Exception as e:
            logger.error(f"Speech recognition failed: {e}")
            return ""
