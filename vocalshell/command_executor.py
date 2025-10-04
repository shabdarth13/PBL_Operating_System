import subprocess
import os
import platform
import logging
import pyttsx3
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

logger = logging.getLogger(__name__)

class CommandExecutor:
    def __init__(self, config=None):
        self.console = Console()
        self.config = config or {}
        self.is_windows = platform.system() == "Windows"
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("rate", self.config.get("tts_rate", 150))
            self.tts_engine.setProperty("volume", self.config.get("tts_volume", 0.8))
        except:
            self.tts_engine = None
    def execute_command(self, command, metadata):
        try:
            if command.lower().startswith("cd "):
                path = command[3:].strip()
                if self.is_windows and path.lower().startswith("/d "):
                    path = path[3:].strip()
                if self.is_windows:
                    from pathlib import Path
                    user_home = Path.home()
                    onedrive_base = user_home / "OneDrive"

                    lower_path = path.lower()

                    if lower_path == "desktop":
                        desktop_path = onedrive_base / "Desktop" if (onedrive_base / "Desktop").exists() else user_home / "Desktop"
                        path = str(desktop_path)

                    elif lower_path == "documents":
                        documents_path = onedrive_base / "Documents" if (onedrive_base / "Documents").exists() else user_home / "Documents"
                        path = str(documents_path)

                    elif lower_path == "downloads":
                        path = str(user_home / "Downloads")

                    elif lower_path == "pictures":
                        pictures_path = onedrive_base / "Pictures" if (onedrive_base / "Pictures").exists() else user_home / "Pictures"
                        path = str(pictures_path)

                else:
                    from pathlib import Path
                    home = Path.home()
                    lower_path = path.lower()
                    if lower_path == "desktop":
                        path = str(home / "Desktop")
                    elif lower_path == "documents":
                        path = str(home / "Documents")
                    elif lower_path == "downloads":
                        path = str(home / "Downloads")
                    elif lower_path == "pictures":
                        path = str(home / "Pictures")

                os.chdir(path)
                return True, f"Changed directory to {os.getcwd()}"
            result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
            )

            if result.returncode == 0:
                return True, result.stdout.strip() or "Command executed successfully"
            else:
                return False, result.stderr.strip() or "Command failed"

        except Exception as e:
            return False, str(e)
    def display_result(self, command, success, output, metadata, use_tts=False):
        style = "green" if success else "red"
        self.console.print(Panel(Text(output, style=style), title=command, border_style=style))
        if use_tts and self.tts_engine:
            self.tts_engine.say(output)
            self.tts_engine.runAndWait()
