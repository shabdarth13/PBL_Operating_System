from setuptools import setup, find_packages

setup(
    name="vocalshell",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.6",
        "vosk>=0.3.51",
        "pyttsx3>=2.90",
        "speechrecognition>=3.8",
        "rich>=13.0",
        "pyaudio>=0.2.13"
    ],
    entry_points={
        "console_scripts": [
            "vocalshell=vocalshell.main:main"
        ]
    }
)
