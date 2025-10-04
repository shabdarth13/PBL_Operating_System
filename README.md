# 🎤 VocalShell - Voice Controlled Command Line Assistant

A powerful voice-controlled interface for Linux and Windows command lines that converts natural language into shell commands.

![VocalShell Logo](assets/icons/microphone.png)

## ✨ Features

- **🎤 Voice Recognition** - Both online (Google) and offline (Vosk) speech recognition
- **🧠 Natural Language Processing** - Understands natural language commands using spaCy
- **🖥️ Cross-Platform** - Works on Windows, Linux, and macOS
- **⚡ Real-time Execution** - Execute commands instantly with voice
- **🛡️ Safety First** - Confirmation for dangerous commands
- **📜 Command History** - Track all executed commands with timestamps
- **🔊 Voice Feedback** - Text-to-speech response and audio cues
- **📝 Script Generation** - Create batch scripts from voice commands
- **🎨 Beautiful UI** - Rich terminal interface with colors and panels
- **🔧 Customizable** - Easy to add custom voice commands

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Microphone
- Speakers (for voice feedback)

### Installation

#### Windows
```bash
# Method 1: Automated setup
setup_windows.bat

# Method 2: Manual installation
git clone https://github.com/your-username/vocalshell.git
cd vocalshell
pip install -r requirements.txt
python models/download_vosk_model.py
python -m spacy download en_core_web_sm