# ================================
# updated_command_executor.py
# ================================

import subprocess
import os
import platform
import logging
import pyttsx3
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re
import shlex

logger = logging.getLogger(__name__)

class CommandExecutor:
    def __init__(self, config=None):
        self.console = Console()
        self.config = config or {}
        self.is_windows = platform.system() == "Windows"
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("rate", self.config.get("tts_rate", 150))
            self.tts_engine.setProperty("volume", self.config.get("tts_volume", 1.0))
        except:
            self.tts_engine = None

    # ==============================
    # Universal read_file with extension fallback
    # ==============================
    def read_file(self, file_name, assets_path="vocalshell/assets", play_audio=True):
        """
        Reads any file. Automatically tries adding common extensions (.txt, .csv, .log, .md, .py)
        """
        possible_paths = []

        # 1️⃣ Exact name in current working directory
        possible_paths.append(os.path.join(os.getcwd(), file_name))
        # 2️⃣ Exact name in assets folder
        possible_paths.append(os.path.join(assets_path, file_name))

        # 3️⃣ Add common extensions if not provided
        if not os.path.splitext(file_name)[1]:
            for ext in [".txt", ".csv", ".log", ".md", ".py"]:
                possible_paths.append(os.path.join(os.getcwd(), file_name + ext))
                possible_paths.append(os.path.join(assets_path, file_name + ext))

        # Find first existing file
        file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break

        if not file_path:
            raise FileNotFoundError(f"File not found: {file_name} (searched with common extensions)")

        # Audio playback
        if play_audio and file_path.endswith((".wav", ".mp3")):
            try:
                from playsound import playsound
                playsound(file_path)
                return f"Played audio: {file_name}"
            except Exception:
                return f"Cannot play audio: {file_name}"

        # Read text
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"Binary file (cannot display content): {file_name}"

    # ==============================
    # execute_command updated
    # ==============================
    def execute_command(self, command, metadata):
        try:
            # ------------------------------
            # Handle change directory (cd)
            # ------------------------------
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

            # ------------------------------
            # Handle read_file commands
            # ------------------------------
            read_patterns = [
                r"read (.*)",
                r"read file (.*)",
                r"display file (.*)",
                r"open (.*) and read",
                r"padho (.*)"
            ]

            file_name = None
            for pattern in read_patterns:
                match = re.match(pattern, command, re.IGNORECASE)
                if match:
                    file_name = match.group(1).strip()
                    break

            if file_name:
                content = self.read_file(file_name)  # Works for any file with extension fallback
                use_tts = not content.startswith("Binary file") and not content.startswith("Played audio")
                self.display_result(f"Reading {file_name}", True, content, metadata, use_tts=use_tts)
                return True, content

            # ------------------------------
            # Fallback: run system command
            # ------------------------------
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

    # ==============================
    # display_result unchanged
    # ==============================
    def display_result(self, command, success, output, metadata, use_tts=False):
        style = "green" if success else "red"
        self.console.print(Panel(Text(output, style=style), title=command, border_style=style))

        if use_tts and self.tts_engine:
            self.tts_engine.say(output)
            self.tts_engine.runAndWait()


# ==============================
# Helper for rename operations
# ==============================
def prepare_rename_command(command_template, params):
    old = params.get("old")
    new = params.get("new")

    if not old or not new:
        return None, "Missing old or new name"

    if not os.path.exists(old):
        return None, f"File not found: {old}"

    old_base, old_ext = os.path.splitext(old)
    new_base, new_ext = os.path.splitext(new)

    if old_ext and not new_ext:
        new = new + old_ext
        params["new"] = new

    old_quoted = f'"{old}"' if ' ' in old else old
    new_quoted = f'"{new}"' if ' ' in new else new

    final_cmd = command_template.format(old=old_quoted, new=new_quoted)
    return final_cmd, None
