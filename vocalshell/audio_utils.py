import os
import platform
import logging
import subprocess

logger = logging.getLogger(__name__)


class AudioPlayer:
    def __init__(self, assets_path="vocalshell/assets/sounds"):
        self.assets_path = assets_path

        # FILES REQUIRED
        self.required_sounds = [
            "listen_start.wav",
            "command_success.wav"
        ]

        # CHECK IF ALL SOUND FILES EXIST
        self.sounds_available = all(
            os.path.exists(os.path.join(self.assets_path, f))
            for f in self.required_sounds
        )

        #if not self.sounds_available:
            #logger.warning(f"Some sound files missing in: {self.assets_path}")

    def play_sound(self, name: str):
        """Cross-platform audio playback with safe fallback."""
        if not self.sounds_available:
             #logger.warning("Sound assets missing, skipping playback.")
            return False

        path = os.path.join(self.assets_path, name)

        if not os.path.exists(path):
             #logger.error(f"Sound file not found: {path}")
            return False

        try:
            system = platform.system()

            # WINDOWS
            if system == "Windows":
                try:
                    import winsound
                except Exception as e:
                     #logger.error(f"winsound unavailable: {e}")
                    return False

                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return True

            # MACOS
            elif system == "Darwin":
                subprocess.run(["afplay", path], check=False)
                return True

            # LINUX
            else:
                # Try paplay
                result = subprocess.run(["paplay", path], check=False)
                if result.returncode != 0:
                    # Try a fallback player
                    subprocess.run(["aplay", path], check=False)
                return True

        except Exception as e:
             #logger.error(f"Error playing sound: {e}")
            return False


# -------------------------------------------------------------------------
# SAFE GLOBAL INSTANCE
# -------------------------------------------------------------------------
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


