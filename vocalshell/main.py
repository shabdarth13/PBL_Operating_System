=#!/usr/bin/env python3
import logging
import platform
from vocalshell.speech_engine import SpeechRecognizer
from vocalshell.nlp_parser import NLPCommandParser
from vocalshell.command_executor import CommandExecutor
from vocalshell.audio_utils import AudioPlayer, play_listen_sound, play_success_sound
from vocalshell.utils import load_config, setup_logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class VocalShell:
    def __init__(self, config_path="config/system_config.json"):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.config = load_config(config_path)

        self.speech_recognizer = SpeechRecognizer(
            model_path=self.config["system"]["model_path"],
            use_online=not self.config["speech"].get("prefer_offline", True),
            config=self.config.get("speech", {})
        )
        self.parser = NLPCommandParser(self.config["system"]["commands_config"])
        self.executor = CommandExecutor(self.config.get("executor", {}))
        self.is_windows = platform.system() == "Windows"
        self.history = []
    def run(self):
        console.print(Panel(Text(" VocalShell - Say 'exit' to quit", style="bold green"), border_style="green"))
        while True:
            play_listen_sound()
            text = self.speech_recognizer.listen()
            if not text:
                console.print("[yellow]No speech detected[/yellow]")
                continue
            console.print(f"[green]Heard:[/green] {text}")
            if text.lower() in ["exit", "quit", "stop"]:
                break
            command, params, description, metadata = self.parser.parse_command(text)
            while command is None and "missing" in metadata:
                missing_params = metadata["missing"]
                for param in missing_params:
                    console.print(f"[yellow]Please provide value for '{param}':[/yellow]")
                    play_listen_sound()
                    value = self.speech_recognizer.listen()
                    if not value:
                        console.print(f"[red]No input detected for '{param}', cancelling command.[/red]")
                        break
                    params[param] = value.strip()
                try:
                    command_template = (
                        self.parser.command_mappings[metadata["category"]]["windows_command"]
                        if self.is_windows
                        else self.parser.command_mappings[metadata["category"]].get("linux_command")
                    )
                    command = command_template.format(**params)
                except KeyError as e:
                    console.print(f"[red]Still missing parameters: {e}, cancelling command.[/red]")
                    command = None
                    break

            if command is None:
                continue
            success, output = self.executor.execute_command(command, metadata)
            self.executor.display_result(command, success, output, metadata, use_tts=True)
            play_success_sound()
            self.history.append({
                "original": text,
                "command": command,
                "success": success,
                "output": output
            })

if __name__ == "__main__":
    shell = VocalShell()
    shell.run()
