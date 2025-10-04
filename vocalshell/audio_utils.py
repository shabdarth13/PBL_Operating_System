import os
import platform
import logging

logger = logging.getLogger(__name__)

class AudioPlayer:
    def __init__(self, assets_path="vocalshell/assets/sounds"):
        self.assets_path = assets_path
        self.sounds_available = all(os.path.exists(os.path.join(assets_path, f)) for f in ["listen_start.wav", "command_success.wav"])

    def play_sound(self, name):
        if not self.sounds_available:
            return False
        path = os.path.join(self.assets_path, name)
        try:
            system = platform.system()
            if system == "Windows":
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif system == "Darwin":
                import subprocess
                subprocess.run(["afplay", path])
            else:
                import subprocess
                subprocess.run(["paplay", path])
            return True
        except:
            return False

_audio_player = None
def get_audio_player():
    global _audio_player
    if _audio_player is None:
        _audio_player = AudioPlayer()
    return _audio_player

def play_listen_sound():
    return get_audio_player().play_sound("listen_start.wav")
def play_success_sound():
    return get_audio_player().play_sound("command_success.wav")
